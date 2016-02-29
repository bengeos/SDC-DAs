import cv2
cap = cv2.VideoCapture()
cap.open("http://192.168.173.192:8080/video?.mjpeg")
while cap.isOpened:
    ret, frame = cap.read()
    cv2.imshow('Mobile IP Camera',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()