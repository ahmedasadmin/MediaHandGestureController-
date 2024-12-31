# Hand Gesture Controller with OpenCV and MediaPipe

This Python script uses OpenCV, MediaPipe, and PyAutoGUI to enable hand gesture recognition. By tracking hand landmarks, the program allows users to perform various actions, such as controlling the system volume or simulating keypresses based on the detected hand gestures. Below is a detailed explanation of the script and its functionality.

---

## Features

1. **Gesture Recognition**:
    Detects the number of extended fingers for both hands.
    Performs actions like navigating slides or controlling media playback based on finger gestures.

2. **Volume Control**:
    Adjusts system volume using right-hand gestures based on palm size and relative landmark positions.

3. **Real-Time Processing**:
    Processes video frames in real-time using OpenCV and MediaPipe.

4. **Debounce Mechanism**:
    Prevents repetitive gesture recognition by adding a time-based debounce mechanism.

---

## Dependencies

- **Python Libraries**:
  - OpenCV (`cv2`)
  - MediaPipe
  - PyAutoGUI
  - ALSA Audio (`alsaaudio`)
  - NumPy

Install the dependencies using:
```bash
pip install opencv-python mediapipe pyautogui numpy pyalsaaudio
```

---

## How It Works

### 1. **Hand Tracking**
The script uses MediaPipe's `Hands` solution to detect hand landmarks. It identifies key points on the hand, such as fingertips and the wrist, to track movements and gestures.

### 2. **Gesture Recognition**
- The number of extended fingers is calculated by comparing the relative positions of the fingertip and its base joint.
- Thumb extension is determined based on horizontal distance.

### 3. **Volume Control**
- The distance between the thumb and index finger is measured.
- This distance is mapped to a volume percentage and adjusts the system volume using the ALSA Audio mixer.

### 4. **Action Mapping**
The following actions are performed based on the number of extended fingers:

| Extended Fingers | Action          |
|------------------|-----------------|
| 1                | Press `Right`   |
| 2                | Press `Left`    |
| 3                | Press `Up`      |
| 4                | Press `Down`    |
| 5                | Press `Space`   |

---

## Code Walkthrough

### Class: `HandGestureController`
The main class encapsulates all the functionality for gesture recognition and control.

#### Methods:

1. **`__init__()`**  
   Initializes MediaPipe Hands and ALSA Audio mixer.

2. **`calculate_distance(pt1, pt2)`**  
   Computes Euclidean distance between two points.

3. **`get_extended_count_fingers(hand_landmarks)`**  
   Calculates the number of extended fingers based on hand landmarks.

4. **`process_frame(frame)`**  
   Processes a video frame to detect hand gestures.

5. **`handle_left_hand(frame, hand_landmarks, idx)`**  
   Handles gestures for the left hand.  
   Maps gestures to keypress actions.

6. **`handle_right_hand(frame, hand_landmarks)`**  
   Handles gestures for the right hand.  
   Adjusts system volume based on hand movements.

7. **`release_resources()`**  
   Releases MediaPipe resources.

---

## How to Run

1. Connect a webcam to your computer.
2. Run the script:
   ```bash
   python hand_gesture_control.py
   ```
3. Use gestures to perform actions:
   - Extend one finger to simulate a `Right` key press.
   - Extend two fingers to simulate a `Left` key press.
   - Adjust volume by changing the distance between your thumb and index finger (right hand).

4. Press `q` to quit the application.

---

## Example Output
When the script runs, a window will display the webcam feed with the following annotations:

- Hand landmarks connected by lines.
- Text indicating detected gestures and volume levels.

---

## Customization

- **Gesture Mapping**:
  Modify the `perform_gesture_action()` method to change actions for specific gestures.

- **Volume Control**:
  Adjust the volume range in the `handle_right_hand()` method by modifying the `np.interp` mapping.

---

## Notes

- Ensure the environment is well-lit for accurate hand tracking.
- The script is tested on Ubuntu with ALSA Audio but can be adapted for other platforms.

---

## Troubleshooting

1. **Webcam Not Detected**:
   - Ensure the webcam is properly connected.
   - Check if another application is using the webcam.

2. **Low Gesture Detection Accuracy**:
   - Improve lighting conditions.
   - Ensure your hand is fully visible in the frame.

3. **Volume Control Not Working**:
   - Verify ALSA Audio is properly installed and configured.

---

## Future Enhancements

- Add support for more complex gestures.
- Implement a calibration mode for dynamic gesture thresholds.
- Extend compatibility to non-ALSA audio systems.

---

## Acknowledgements
- [MediaPipe](https://google.github.io/mediapipe/) for hand tracking.
- [OpenCV](https://opencv.org/) for video processing.
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) for simulating keyboard input.
- [ALSA Audio](https://www.alsa-project.org/) for volume control.