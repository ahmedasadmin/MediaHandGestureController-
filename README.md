
# Hand Gesture Control Using OpenCV and MediaPipe

This project implements a hand gesture control system using OpenCV, MediaPipe, and PyAutoGUI. It allows users to control various actions on their computer based on detected hand gestures. For example, the left hand can be used for gesture-based commands like navigation, and the right hand can control system volume dynamically.

## Features

- **Left Hand Gestures**:
  - 1 finger: Navigate right (e.g., next slide ).
  - 2 fingers: Navigate left (e.g., previous slide).
  - 3 fingers: Volume up.
  - 4 fingers: Volume down.
  - 5 fingers: Play/Pause (space key).

- **Right Hand Gestures**:
  - Dynamically control system volume by changing the distance between the thumb and index finger.

## Requirements

- Python 3.6 or higher
- OpenCV
- MediaPipe
- PyAutoGUI
- ALSA Audio Library (`pyalsaaudio`)
- NumPy

Install the required libraries using the following command:

```bash
pip install opencv-python mediapipe pyautogui numpy pyalsaaudio
```

## How It Works

- **Hand Detection**:
  - Uses MediaPipe to detect hand landmarks in real-time from a webcam feed.
  
- **Gesture Recognition**:
  - Compares specific landmark positions to detect extended fingers.
  - Calculates the distance between landmarks for gesture-based volume control.

- **Action Mapping**:
  - Maps the number of extended fingers to specific keyboard commands.
  - Adjusts system volume based on the thumb-index distance ratio.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hand-gesture-control.git
   cd hand-gesture-control
   ```

2. Run the script:
   ```bash
   python hand_gesture_control.py
   ```

3. Perform gestures in front of the webcam:
   - Use the **left hand** for navigation commands.
   - Use the **right hand** for volume control.

4. Press `q` to quit the application.

## Key Functions

- **Hand Detection**:
  - Utilizes MediaPipe's `Hands` solution to identify landmarks and determine handedness.

- **Gesture Handling**:
  - `get_extended_count_fingers`: Calculates the number of extended fingers using landmark positions.
  - `handle_left_hand`: Maps left-hand gestures to keyboard commands.
  - `handle_right_hand`: Dynamically adjusts the system volume based on thumb-index distance.

- **Drawing Utilities**:
  - Annotates the video feed with landmarks, lines, and labels for better visualization.

## System Compatibility

- Developed and tested on Ubuntu with ALSA for audio control.
- Compatible with any system that supports the required libraries.

## Future Enhancements

- Support for additional gestures.
- Customizable gesture-to-action mapping.
- Cross-platform volume control (e.g., for Windows and macOS).

## Acknowledgements

- [MediaPipe](https://mediapipe.dev/) for providing robust hand tracking.
- [OpenCV](https://opencv.org/) for video processing.
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for automating keyboard actions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.