from flask import Flask, render_template, jsonify
import cv2
import mediapipe as mp
import threading

app = Flask(__name__)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
movement_command = "none"  # Store detected movement

def detect_hand():
    global movement_command

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        frame = cv2.flip(frame, 1)  
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        prev_command = movement_command  # Store previous state
        movement_command = "none"  # Reset before checking

        # Get frame dimensions
        frame_height, frame_width, _ = frame.shape
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2
        dead_zone = 80  # Your updated dead zone size

        # Draw the dead zone square (green)
        top_left = (frame_center_x - dead_zone, frame_center_y - dead_zone)
        bottom_right = (frame_center_x + dead_zone, frame_center_y + dead_zone)
        
        overlay = frame.copy()
        cv2.rectangle(overlay, top_left, bottom_right, (255, 255, 0), 10)  # Blue border
        frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)  # Apply transparency

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                x_index = int(hand_landmarks.landmark[8].x * frame.shape[1])
                y_index = int(hand_landmarks.landmark[8].y * frame.shape[0])

                frame_center_x = frame.shape[1] // 2
                frame_center_y = frame.shape[0] // 2
                dead_zone = 70

                if y_index < frame_center_y - dead_zone:
                    movement_command = "up"
                elif y_index > frame_center_y + dead_zone:
                    movement_command = "down"
                elif x_index < frame_center_x - dead_zone:
                    movement_command = "left"
                elif x_index > frame_center_x + dead_zone:
                    movement_command = "right"

                cv2.circle(frame, (x_index, y_index), 10, (0, 0, 255), -1)
                cv2.putText(frame, f"Move: {movement_command}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

                if movement_command != prev_command:
                    if movement_command == "none":
                        continue
                    print(f"📸 Detected Movement: {movement_command}")

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_movement')
def get_movement():
    global movement_command
    print("🔍 /get_movement route was accessed")  

    if movement_command != "none":
        last_command = movement_command
        movement_command = "none"  # Reset AFTER sending
        print(f"📡 Sent to JS: {last_command}")  
        return jsonify({"command": last_command})
    
    return jsonify({"command": "none"})

if __name__ == '__main__':
    # Start hand tracking thread
    hand_thread = threading.Thread(target=detect_hand, daemon=True)
    hand_thread.start()

    app.run(debug=True, use_reloader=False)  # Prevent double execution in Flask
