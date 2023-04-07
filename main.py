import cv2
import os
from deepface import DeepFace

class Eroji:

    def __init__(self):
        self.face_cascade_model = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
        image_path = os.path.join(os.getcwd(), 'Photo.jpg')
        self.frame = cv2.imread(image_path)

    def detect_faces(self):
        grayscale = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade_model.detectMultiScale(grayscale, 1.3, 5)

        for (x, y, w, h) in faces:
            face = self.frame[y:y+h, x:x+w]
            resized_face_224 = cv2.resize(face, (224, 224))
            predicted_results = DeepFace.analyze(resized_face_224, actions=['gender', 'race', 'emotion'])

            cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            for i in range(len(predicted_results)):
                predictions = f"{predicted_results[i]['gender']}, \n{predicted_results[i]['race']}, \n{predicted_results[i]['emotion']}"
                cv2.putText(self.frame, predictions, (x, y+h+20+20*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                print(predictions)
        cv2.imshow('Eroji', self.frame)
        cv2.waitKey(0)

    def close(self):
        cv2.destroyAllWindows()

if __name__ == '__main__':
    fd = Eroji()
    fd.detect_faces()
    fd.close()
