from setuptools import setup, find_packages

setup(
    name="hand_gesture_project",  # Name of your project
    version="0.1",  # Project version
    description="A hand gesture controller using MediaPipe and OpenCV.",  # Short description
    author="Ahmed M. Nagi",  # Your name
    author_email="your_email@example.com",  # Your email (optional)
    url="https://github.com/your-repo",  # URL to the project (e.g., GitHub repo)
    packages=find_packages(where="src"),  # Automatically find packages in the src folder
    package_dir={"": "src"},  # Specify the src folder as the package root
    install_requires=[
        "opencv-python",
        "mediapipe",
        "pyautogui",
        "numpy",
        "pyalsaaudio",  # Replace with alsaaudio if necessary
    ],  # Dependencies required for your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version required
)
