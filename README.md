# 🏁 Robot Maze Game – Hand Gesture Controlled

🚀 **A fun and interactive robot maze game where users navigate through a maze using hand gestures captured via a camera. Built with Flask, OpenCV, and JavaScript.**

---

## 📌 Features

- 🖐 **Hand Gesture Controls** – Navigate the robot character using real-time hand movements.
- 🏎 **Adjustable Sensitivity** – Dead zone and movement speed tuning for smooth control.
- 🗺 **Multiple Levels** – Progress through increasingly difficult maze layouts.
- 🎮 **Real-Time Feedback** – Visual indicators for detected gestures.

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript (with `game.js` for maze logic)
- **Backend:** Python (Flask)
- **Computer Vision:** OpenCV, MediaPipe

---

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AlexCRosa/maze_game.git
   cd robot-maze-game
   ```

2. **Set up a virtual environment** *(recommended)*:
   ```bash
   python -m venv .venv
   source venv/bin/activate  # On macOS/Linux
   .\.venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**:
   ```bash
   python app.py
   ```

5. **Access the game** in your browser at `http://localhost:5000`.

---

## 🎮 How to Play

1. Stand in front of the camera and position your hand within the detection area.
2. Move your hand **up, down, left, or right** to guide the robot.
3. Navigate through the maze and reach the exit to progress to the next level.
4. Enjoy the challenge of progressively harder mazes!

---

## 🛠️ Troubleshooting

- **Gesture sensitivity too high?**
  - Adjust the **dead zone value** in `app.py` and **movement update rate** in `game.js`.

- **Maze not loading?**
  - Check if the maze definition file is correctly linked.

---

## 🚀 Future Enhancements

- 🔹 More levels with increasing complexity.
- 🔹 Customizable controls and maze design.
- 🔹 Sound effects and animations.

---

## 📜 License

This project is licensed under the **MIT License** – feel free to modify and enhance it!

---

## 🤝 Contributing

Have ideas or improvements? Fork the repository and submit a pull request! 🎉

---

## 📬 Contact

For any inquiries, reach out via [*alex_cesar20@hotmail.com*] or open an issue on GitHub.
