import cv2
from cvzone.HandTrackingModule import HandDetector

# Set up camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Initialize the hand detector
detector = HandDetector(detectionCon=0.5, maxHands=2)

class DragDropRect:
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size
        self.colorR = (255, 165,0)

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        cursorX, cursorY = cursor
        if cx - w // 2 < cursorX < cx + w // 2 and cy - h // 2 < cursorY < cy + h // 2:
            self.colorR = (0, 0, 255)
            self.posCenter = cursor
        else:
            self.colorR = (255, 165, 0)

rectList = [DragDropRect([x*250 + 150, 150]) for x in range(5)]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    
    if hands:
        for hand in hands:
            lmList = hand["lmList"]  # List of 21 landmarks
            if lmList:
                point1 = lmList[8][:2]
                point2 = lmList[12][:2]
                length, info, img = detector.findDistance(point1, point2, img)
                print(length)
                if length < 30:
                    cursor = lmList[8][:2]  # Get the tip of the index finger
                    for rect in rectList:
                        rect.update(cursor)

    # Draw the rectangles
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), rect.colorR, cv2.FILLED)
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
