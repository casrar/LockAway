import cv2

class FacialRecognizer:
    def __init__(self, classifier: cv2.CascadeClassifier):
        self.classifier = classifier

    def detect_facial_presence(self, frame) -> bool:   
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
        if len(faces) > 0:
            return True
        return False
