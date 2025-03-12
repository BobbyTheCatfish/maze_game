import cv2
import mediapipe as mp
import numpy as np
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from configparser import ConfigParser
import utils as u

# Fancy text for the lols
print(open("./splash.txt").read())

# Configuration
config = ConfigParser()

def load_config():
        config.read('config.ini')
        print("Loaded config")

load_config()

# Hot reload configuration
class ConfigLoader(FileSystemEventHandler):
    def on_modified(self, event: FileSystemEvent) -> None:
        if (event.src_path == ".\config.ini"):
            load_config()

observer = Observer()
observer.schedule(ConfigLoader(), ".", recursive=False)
observer.start()

# Keyboard color swapping codes
num_codes = []

for i in range(10):
    num_codes.append(ord(str(i)))

splash = cv2.imread("splash.jpg")
cv2.imshow("Hand Tracking", splash)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=config.getfloat("config", "min_detection"), min_tracking_confidence=config.getfloat("config", "min_tracking"))

# Start webcam
cap = cv2.VideoCapture(config.getint("config", "camera_id"))


def detect_hand():

    # Create the drawing canvas
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    drawing = np.zeros((height,width,3), np.uint8)

    x_prev = 0
    y_prev = 0
    drawMode = False

    window_width, window_height = u.calc_window_size(config, width, height)

    while True:
        ret, frame = cap.read()
        # If the camera feed couldn't be read
        if not ret:
            drawMode = False
            continue
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        # If it detects someone's hand
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                x_index = int(hand_landmarks.landmark[8].x * frame.shape[1])
                y_index = int(hand_landmarks.landmark[8].y * frame.shape[0])
                z_index = int(hand_landmarks.landmark[8].z * config.getint("config", "z_scale"))

                # Z Position based drawing. It works, but not well. Gotta find another way
                # if z_index < config.getint("config", "z_cutoff"):
                #     drawMode = False
                #     continue

                # Display hand position, for debugging.
                if (config.getboolean("config", "debug") == True):
                    cv2.putText(frame, f"X: {x_index}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                    cv2.putText(frame, f"Y: {y_index}", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                    cv2.putText(frame, f"Z: {z_index}", (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

                # Prevent pauses in drawing from creating unwanted brush strokes
                if drawMode == False:
                    x_prev = x_index
                    y_prev = y_index

                # Draw on the canvas
                cv2.line(drawing, (x_prev, y_prev), (x_index, y_index), (0, 0, 255), 10)
                drawMode = True

                # Update the hand position
                x_prev = x_index
                y_prev = y_index

        # No hand detected, drawing has stopped
        else:
            drawMode = False

        # Overlay the drawing on the camera
        gray = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
        ret, invert = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)
        invert = cv2.cvtColor(invert, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, invert)
        frame = cv2.bitwise_or(frame, drawing)
        frame = cv2.resize(frame, (window_width, window_height))
        # Show the result
        cv2.imshow("Hand Tracking", frame)
        

        ###################
        # BACKUP KEYBINDS #
        ###################

        # Q: Quit
        # C: Clear
        # B: Toggle Background (toggles overlaying on the camera vs the canvas)
        # [: Brush Smaller
        # ]: Brush Larger
        # 1-9: Color Select

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        elif key == ord("c"):
            print("Clearing...")
            drawing = np.zeros((height,width,3), np.uint8)

        elif key == ord("b"):
            print("Background Toggled")
            # background_mode = not background_mode

        elif key == ord("["):
            print("Brush Smaller")
            # brush_size = brush_size - 1
        elif key == ord("]"):
            print("Brush Larger")
            # brush_size = brush_size + 1

        elif key in num_codes:
            print("Color Swap")
            # color = new_color

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    # Start hand tracking thread
    detect_hand()