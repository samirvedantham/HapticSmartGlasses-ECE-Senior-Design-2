import numpy as np
import cv2
import cv2.aruco as aruco
import time
import calibrate_camera_online

print(cv2.__version__)
vidcap = cv2.VideoCapture('samplearucovideo.mp4')
start_time = time.time()
# with np.load('webcam_calibration_output.npz') as X:
#     mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
success, frame = vidcap.read()
success = True

retval, mtx, dist, rvecs, tvecs = calibrate_camera_online.calibrate()
print("matrix:")
print(mtx)

print("dist")
print(dist)

length = 0.5 * (min(8,5) * 0.1)

while success:
    # Capture frame-by-frame
    frame_start_time = time.time()
    ret, frame = vidcap.read()
    if ret == False:
        break
    # frame = cv2.imread("aruco_0_1_4_5.jpg")
    # print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()

    # print(parameters)

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
    # lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    rvecs_curr, tvecs_curr = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
    # print(corners)
    # print(ids)
    # print(rejectedImgPoints)

    if ids != None:
        for rvec, tvec in zip(rvecs_curr, tvecs_curr):
            aruco.drawAxis(frame, mtx, dist, rvec, tvec, 0.05)  # Draw Axis

        aruco.drawDetectedMarkers(frame, corners)  # Draw A square around the markers
        # print(ids)
        # print(corners)

    # It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs

    print("Frame Time: " + str(time.time() - frame_start_time))
    # gray = aruco.drawDetectedMarkers(gray, corners)

    # print(rejectedImgPoints)
    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
print("Total Time: " + str(time.time() - start_time))
# vidcap.release()
# cv2.destroyAllWindows()
