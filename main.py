import cv2
from deepface import DeepFace

class Eroji:

    def __init__(self):
        self.face_cascade_model = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)

    def detect_faces(self):
        while True:
            ret, frame = self.cap.read()
            grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade_model.detectMultiScale(grayscale, 1.3, 5)

            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
                resized_face_224 = cv2.resize(face, (224, 224))
                predicted_results = DeepFace.analyze(resized_face_224, actions=['gender', 'race', 'emotion'])

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                for i in range(len(predicted_results)):
                    predictions = f"{predicted_results[i]['gender']}, {predicted_results[i]['race']}, {predicted_results[i]['emotion']}"
                    cv2.putText(frame, predictions, (x, y+h+20+20*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            cv2.imshow('Eroji', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    fd = Eroji()
    fd.detect_faces()
    fd.close()
