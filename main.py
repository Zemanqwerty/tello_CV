import cv2
from djitellopy import Tello

tello = Tello()
tello.connect()

tello.takeoff()
tello.move_up(80)
print(tello.get_battery())
tello.streamon()


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def fly(x, y, w, h):
    x_move = 0
    y_move = 0
    z_move = 0
    yaw_move = 0

    if w * h < 10000:
        y_move = 30
    elif w * h > 20000:
        y_move = -30
    else:
        y_move = 0
    

    return tello.send_rc_control(
        x_move,
        y_move,
        z_move,
        yaw_move
    )


while True:
    frame = tello.get_frame_read().frame
    r_frame = cv2.resize(frame, (720, 480))

    gray = cv2.cvtColor(r_frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        cv2.rectangle(r_frame, (x, y), (x+w, y+h), (255, 0, 0), 4)
        fly(x, y, w, h)
    else:
        tello.send_rc_control(0, 0, 0, 0)

    cv2.imshow('TELLO AI', r_frame)

    if cv2.waitKey(1) == ord('q'):
        break

tello.streamoff()
tello.land()
tello.end()
cv2.destroyAllWindows()
