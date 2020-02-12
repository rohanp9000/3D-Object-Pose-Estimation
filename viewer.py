import cv2

capture = cv2.VideoCapture(0)

if not(capture.isOpened()):
    print("Can't open device")


capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

while(True):
    ret, frame = capture.read()
    cv2.imshow('preview', frame)
    if(cv2.waitKey(1) % 0xFF == ord('q')):
        capture.release()
        cv2.destroyAllWindows()
        break
