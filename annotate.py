import cv2
import pickle 
import numpy as np 


img = cv2.imread('carParkImg.png')
polygonList = []
currentPolygon = []

def mouseClick(events, x ,y,  flags, params):
    global currentPolygon, PolygonList
    if events == cv2.EVENT_LBUTTONDOWN:
        currentPolygon.append((x,y))
        
    elif events == cv2.EVENT_RBUTTONDOWN:
        if len(currentPolygon) >= 3:
            polygonList.append(currentPolygon.copy())
        currentPolygon.clear()

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouseClick)

while True:
    img_copy = img.copy()
    
    for poly in polygonList:
        cv2.polylines(img_copy, [np.array(poly)], True, (0, 255, 0), 2)
        
    if currentPolygon:
        cv2.polylines(img_copy, [np.array(currentPolygon)], False, (255, 255, 0), 1)
        for point in currentPolygon:
            cv2.circle(img_copy, point, 5, (0, 255, 255), cv2.FILLED)
            
    cv2.imshow("Image", img_copy)
    key = cv2.waitKey(1)
    if key == ord('s'):
        with open('annotations/CarParkPolygons', 'wb') as f:
            pickle.dump(polygonList, f)
        print("Polygons saved.")
        break
    elif key == ord('q'):
        break

cv2.destroyALLWindows()