import cv2
from djitellopy import Tello

tello = Tello()
tello.connect()

tello.takeoff()
tello.move_up(80)
print(tello.get_battery())
tello.streamon()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def check_battery():
    current_battery = tello.get_battery()
    string_battery = ''
    battery_color = (0, 0, 0)

    for i in range(current_battery // 10):
        string_battery += '-'

    if current_battery > 75:
        battery_color = (35, 210, 22)
    elif current_battery > 50:
        battery_color = (47, 225, 207)
    elif current_battery > 25:
        battery_color = (0, 128, 255)
    else:
        battery_color = (0, 0, 255)

    return battery_color, string_battery


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

    if x + w / 2 < 200:
        yaw_move = -30
    elif x + w / 2 > 520:
        yaw_move = 30
    else:
        yaw_move = 0

    if y + h / 2 < 160:
        z_move = 30
    elif y + h / 2 > 320:
        z_move = -30
    else:
        z_move = 0

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
        cv2.rectangle(r_frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
        fly(x, y, w, h)
    else:
        tello.send_rc_control(0, 0, 0, 0)

    b_c, b_v = check_battery()

    cv2.putText(r_frame, f'BATTERY:', (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 230, 100), 4)
    cv2.putText(r_frame, f'{b_v}', (160, 475), cv2.FONT_HERSHEY_SIMPLEX, 1, b_c, 4)
    cv2.putText(r_frame, f'{b_v}', (160, 465), cv2.FONT_HERSHEY_SIMPLEX, 1, b_c, 4)
    cv2.putText(r_frame, f'HEIGHT: {tello.get_height()}sm', (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 230, 100), 4)
    cv2.putText(r_frame, f'TOTAL TIME: {tello.get_flight_time()}s', (10, 370), cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 230, 100),
                4)
    cv2.imshow('TELLO AI', r_frame)


    if cv2.waitKey(1) == ord('q'):
        break

tello.streamoff()
tello.land()
tello.end()
cv2.destroyAllWindows()
