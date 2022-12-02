from collections import deque

import cv2
import mediapipe as mp
import numpy as np

bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

b_idx = 0
g_idx = 0
r_idx = 0
y_idx = 0
color_idx = 0

kernel = np.ones((5, 5), dtype=np.uint)

color = [(255, 0, 0), [0, 255, 0], [0, 0, 255], (0, 255, 255)]

paintWindow = np.zeros((471, 636, 3))+255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), (255,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), (0,255,0), 2)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), (0,0,255), 2)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), (0,255,255), 2)

cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
ret = True
# ret, frame = cap.read()
while(ret):
    ret, frame = cap.read()
    
    # x, y, c = frame.shape
    frame = cv2.flip(frame, 1)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = cv2.rectangle(frame, (40,1), (140,65), (0,0,0), 2)
    frame = cv2.rectangle(frame, (160,1), (255,65), (255,0,0), 2)
    frame = cv2.rectangle(frame, (275,1), (370,65), (0,255,0), 2)
    frame = cv2.rectangle(frame, (390,1), (485,65), (0,0,255), 2)
    frame = cv2.rectangle(frame, (505,1), (600,65), (0,255,255), 2)
    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    result = hands.process(framergb)

    if result.multi_hand_landmarks :
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lms in handslms.landmark:
                lmx = lms.x*640
                lmy = lms.y*480
                landmarks.append([lmx, lmy])
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        forefinger = (int(landmarks[8][0]),int(landmarks[8][1]))
        center = forefinger
        # print(center)
        midfinger = (landmarks[12][0], landmarks[12][1])
        # center = forefinger
        cv2.circle(frame, center, 3, (0, 255, 0), -1)
        if (midfinger[1]-center[1] < 30 and midfinger[0]-center[0] < 30):
            bpoints.append(deque(maxlen=512))
            b_idx += 1
            gpoints.append(deque(maxlen=512))
            g_idx += 1
            rpoints.append(deque(maxlen=512))
            r_idx += 1
            ypoints.append(deque(maxlen=512))
            y_idx += 1

        elif center[1] <= 65:
            if 40 <= center[0] <= 140:
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                b_idx = 0
                g_idx = 0
                r_idx = 0
                y_idx = 0
                paintWindow[67:, :, :] = 255
            elif 160 <= center[0] <= 255:
                color_idx = 0
            elif 275 <= center[0] <= 370:
                color_idx = 1
            elif 390 <= center[0] <= 485:
                color_idx = 2
            elif 505 <= center[0] <= 600:
                color_idx = 3

        else :
            if color_idx == 0:
                bpoints[b_idx].appendleft(center)
            elif color_idx == 1:
                gpoints[g_idx].appendleft(center)
            elif color_idx == 2:
                rpoints[r_idx].appendleft(center)
            elif color_idx == 3:
                ypoints[y_idx].appendleft(center)

    else :
        bpoints.append(deque(maxlen=512))
        b_idx += 1
        gpoints.append(deque(maxlen=512))
        g_idx += 1
        rpoints.append(deque(maxlen=512))
        r_idx += 1
        ypoints.append(deque(maxlen=512))
        y_idx += 1
    
    points = [bpoints, gpoints, rpoints, ypoints]

    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k-1], points[i][j][k], color[i], 2)
                cv2.line(paintWindow, points[i][j][k-1], points[i][j][k], color[i], 2)
    
    cv2.imshow("OUTPUT", frame)
    cv2.imshow("Paint", paintWindow)
    if(cv2.waitKey(1) == ord('q')):
        break
cap.release()
cv2.destroyAllWindows()
