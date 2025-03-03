import { maze } from "./maze.js";

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const cellSize = 40;
const cols = maze[0].length;
const rows = maze.length;

canvas.width = cols * cellSize;
canvas.height = rows * cellSize;

let character = {
    x: 1, // Start position in grid
    y: 1
};

function drawMaze() {
    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
            ctx.fillStyle = maze[row][col] === 1 ? "black" : "white";
            ctx.fillRect(col * cellSize, row * cellSize, cellSize, cellSize);
            ctx.strokeRect(col * cellSize, row * cellSize, cellSize, cellSize);
        }
    }
}

function drawCharacter() {
    ctx.fillStyle = "blue";
    ctx.beginPath();
    ctx.arc(
        character.x * cellSize + cellSize / 2,
        character.y * cellSize + cellSize / 2,
        cellSize / 4,
        0,
        Math.PI * 2
    );
    ctx.fill();
}

function moveCharacter(direction) {
    let newX = character.x;
    let newY = character.y;

    if (direction === "up") newY--;
    if (direction === "down") newY++;
    if (direction === "left") newX--;
    if (direction === "right") newX++;

    if (maze[newY] && maze[newY][newX] === 0) {
        character.x = newX;
        character.y = newY;
        console.log(`✅ Character moved to: (${character.x}, ${character.y})`); // Debugging
    } else {
        console.log(`⛔ Blocked move: (${newX}, ${newY})`);
    }
}




function updateGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawMaze();
    drawCharacter();
    requestAnimationFrame(updateGame);
}


// Fetch movement commands from Flask every 200ms
setInterval(() => {
    fetch("/get_movement")
        .then(response => response.json())
        .then(data => {
            if (data.command !== "none") {
                console.log(`📡 Received from server: ${data.command}`);
                moveCharacter(data.command);
            }
        })
        .catch(error => console.error("❌ Fetch error:", error));
}, 200);


updateGame();
