import cv2
import pickle
import numpy as np

cap = cv2.VideoCapture('carPark.mp4')

with open('annotations/CarParkPolygons', 'rb') as f:
    polygonList = pickle.load(f)

while True:
    success, frame = cap.read()
    if not success:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for poly in polygonList:
        mask = np.zeros_like(gray)
        cv2.fillPoly(mask, [np.array(poly)], 255)

        mean_val, stddev = cv2.meanStdDev(gray, mask=mask)
        mean_val = mean_val[0][0]
        std_val = stddev[0][0]

        contour_area = cv2.countNonZero(cv2.Canny(gray, 80, 150) & mask)
        # Experiment with both mean and std
        if mean_val < 110 or std_val > 12 or contour_area > 500:
            status = "Occupied"
            color = (0, 0, 255)
        else:
            status = "Empty"
            color = (0, 255, 0)

        cv2.polylines(frame, [np.array(poly)], True, color, 2)
        cv2.putText(frame, status, tuple(poly[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Parking Detection", frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()