import cv2
import mediapipe as mp
import pyautogui
import time
import math
import numpy as np
import alsaaudio

mixer = alsaaudio.Mixer()

def calculate_distance(pt1, pt2):
    """
    Calculate Euclidean distance between two points.

    Args:
        pt1: A point object with attributes 'x' and 'y' representing the first point.
        pt2: A point object with attributes 'x' and 'y' representing the second point.
    
    Returns:
        The Euclidean distance between pt1 and pt2.
    """
    dx = pt1.x - pt2.x
    dy = pt1.y - pt2.y
    return math.sqrt(dx**2 + dy**2)

def get_extended_count_fingers(hand_landmarks):
    """Count the number of extended fingers based on hand landmarks.

    This function checks the extension of each finger using the hand landmarks, which 
    are typically detected by a hand-tracking model like MediaPipe. It calculates the 
    number of extended fingers by comparing the relative positions of finger tips and 
    their corresponding bases. Additionally, it checks whether the thumb is extended 
    based on a horizontal distance threshold.

    Args:
        hand_landmarks (object): An object containing hand landmark points, with each 
        landmark having x, y, and z coordinates. The key landmarks used are:
            - landmark[0] (Wrist)
            - landmark[4], landmark[5] (Thumb base and joint)
            - landmark[6], landmark[8], landmark[10], landmark[12], landmark[14], landmark[16], landmark[18], landmark[20] (Base, joints, and tips of fingers).

    Returns:
        int: The number of extended fingers (including thumb).

    Logic:
        1. Palm Length Calculation:
            - Measures the distance between the wrist (landmark[0]) and middle of the palm (landmark[9]) to calculate palm length.
        
        2. Finger Extension Check:
            - Compares the y-coordinate of the finger tips with the y-coordinate of the corresponding base landmarks. 
            - If the tip’s y-coordinate is smaller than the base’s, the finger is considered extended.

        3. Thumb Extension Check:
            - Compares the horizontal distance between the thumb base (landmark[4]) and thumb joint (landmark[5]) to half the palm length. 
            - If this distance is greater than half the palm length, the thumb is considered extended.

    Example:
        # Assuming hand_landmarks is an object containing the landmarks of the hand
        num_extended_fingers = get_extended_count_fingers(hand_landmarks)
        print(f"Number of extended fingers: {num_extended_fingers}")
    """
    cnt = 0

    # Calculate the palm length for thumb gesture threshold
    palm_length = calculate_distance(hand_landmarks.landmark[0], hand_landmarks.landmark[9])

    # Check extended fingers (Index to Pinky) by comparing y-coordinates
    for tip, base in zip([8, 12, 16, 20], [6, 10, 14, 18]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y:
            cnt += 1

    # Check if Thumb is extended (using x-coordinate comparison)
    if calculate_distance(hand_landmarks.landmark[4], hand_landmarks.landmark[5]) > palm_length * 0.5:
        cnt += 1

    return cnt

def draw_landmark_circle(frame, landmark, radius=5, color=(255, 255, 255)):
    """
    Draws a circle on a given frame at the specified landmark position.

    Parameters:
        frame: ndarray
            The image frame on which the circle will be drawn.
        landmark: object
            The landmark object containing x and y coordinates.
        radius: int, optional
            The radius of the circle to be drawn. Default is 5.
        color: tuple, optional
            The color of the circle in BGR format. Default is white (255, 255, 255).

    Returns:
        tuple: (x, y) coordinates of the landmark on the frame.
    """
    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
    cv2.circle(frame, (x, y), radius, color, -1)
    return x, y

def draw_line_on_frame(frame, start, end, color=(255, 255, 255), thickness=2):
    """
    Draws a line on the given frame.

    Args:
        frame: The image/frame to draw on.
        start: A tuple (x1, y1) representing the starting point of the line.
        end: A tuple (x2, y2) representing the ending point of the line.
        color: A tuple (B, G, R) for the line color (default is white).
        thickness: The thickness of the line (default is 2).
    
    Returns:
        The updated frame with the drawn line.
    """
    cv2.line(frame, start, end, color, thickness)
    return frame

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Start Video Capture
cap = cv2.VideoCapture(0)

prev_gesture = -1  # Previous gesture to avoid repeats
start_time = None  # Timer for gesture debounce
volume_debounce_time = time.time()  # Debounce timer for volume control

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for a mirror-like effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Handedness ("Left" or "Right")
            handedness = results.multi_handedness[idx].classification[0].label

            if handedness == "Left":  # Only process the left hand
                # Count Fingers
                finger_count = get_extended_count_fingers(hand_landmarks)

                # Display the gesture on the frame
                label = f"{handedness} Hand: {finger_count} Fingers"
                cv2.putText(frame, label, (10, 50 + idx * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Gesture Handling
                current_time = time.time()
                if prev_gesture != finger_count:
                    if start_time is None:
                        start_time = current_time
                    elif current_time - start_time > 0.3:  # Debounce threshold
                        if finger_count == 1:
                            pyautogui.press("right")
                        elif finger_count == 2:
                            pyautogui.press("left")
                        elif finger_count == 3:
                            pyautogui.press("up")
                        elif finger_count == 4:
                            pyautogui.press("down")
                        elif finger_count == 5:
                            pyautogui.press("space")

                        prev_gesture = finger_count
                        start_time = None

                # Draw Landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            elif handedness == "Right":  # Process the right hand for volume control
                
                # Calculate palm ratio
                palm_length = calculate_distance(hand_landmarks.landmark[0], hand_landmarks.landmark[9])
                hand_width = calculate_distance(hand_landmarks.landmark[8], hand_landmarks.landmark[4])
                palm_ratio = hand_width  /  palm_length if hand_width != 0 else 0
                x1, y1 = draw_landmark_circle(frame=frame, landmark=hand_landmarks.landmark[8])
                x2, y2 = draw_landmark_circle(frame=frame, landmark=hand_landmarks.landmark[4])
                draw_line_on_frame(frame=frame, start=(x1, y1), end=(x2,y2), color=(0, 0, 0))
                # Map palm ratio to volume (assuming typical ratios between 1.0 and 2.0)
                volume = int(np.interp(palm_ratio, [0.2, 1.50], [0, 100]))

                # Add debounce logic for volume control
                current_time = time.time()
                if current_time - volume_debounce_time > 0.3:  # 300ms debounce
                    mixer.setvolume(volume)
                    volume_debounce_time = current_time

                # Display the volume level
                cv2.putText(frame, f"Volume: {volume}%", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the Frame
    cv2.imshow("Hand Gesture Control", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
