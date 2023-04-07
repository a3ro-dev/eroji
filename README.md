# Eroji

This project is a Python script that uses the DeepFace package to perform real-time face analysis on a video stream from a webcam. The script uses OpenCV to capture frames from the webcam, detect faces in the frames, and then use the DeepFace package to analyze each face and predict its gender, race, and facial expression. The script then displays the predictions in real-time on the screen, along with a bounding box around each detected face.

## Requirements

- Python 3.x
- OpenCV
- DeepFace
- haarcascade_frontalface_default.xml

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages using pip: `pip install -r requirements.txt`
3. Download the `haarcascade_frontalface_default.xml` file and place it in the same directory as the Python script. You can download the file from [here](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml).

## Usage

1. Open a terminal and navigate to the directory where the script is located.
2. Run the script using the following command: `python main.py`
3. The script will open a window displaying the webcam feed, with bounding boxes around each detected face and the predicted gender, race, and facial expression displayed below each bounding box.
4. Press the 'q' key to exit the program.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses the [DeepFace](https://github.com/serengil/deepface) package for face analysis.
- The face detection model used in this project is the `haarcascade_frontalface_default.xml` model from OpenCV.
