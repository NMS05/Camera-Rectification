from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


# Pi Camera is used here. Replace with OpenCV VideoCapture() if necessary.
camera = PiCamera()
camera.resolution = (1296, 972)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1296, 972))

time.sleep(1)


# Replace the following parameters after camera calibration. For monocular camera calibration, refer to https://docs.mrpt.org/reference/latest/app_camera-calib.html

# Image Dimensions
DIM=(1296,972)
# Camera Matrix
K=np.array([[875.83478, 0.0, 636.48126], [0.0, 870.85405, 500.86536], [0.0, 0.0, 1.0]])
# Distortion Parameters
D=np.array([[-4.069951e-01],[2.257140e-01],[1.209394e-03],[5.652785e-04],[-7.829103e-02]])


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	img = frame.array
	map1, map2 = cv2.initUndistortRectifyMap(K, D, None, K, DIM, cv2.CV_16SC2)
	rectified_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

	cv2.imshow("Frame", rectified_img)
	cv2.waitKey(10)

	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key == ord("x"):
		break

cv2.destroyAllWindows()
