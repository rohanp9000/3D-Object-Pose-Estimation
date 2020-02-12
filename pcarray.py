import pyzed.sl as sl
from matplotlib import pyplot as plt
import math
import numpy as np
import sys
import cv2
def main():

    zed = sl.Camera()

    #init
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE  # Use PERFORMANCE depth mode
    init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use milliliter units (for depth measurements)

    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.sensing_mode = sl.SENSING_MODE.STANDARD  # Use STANDARD sensing mode

    image = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat()
    # A new image is available if grab() returns SUCCESS
    print(type(point_cloud))

    #pcarray =  [[0 for a in range(x)] for b in range(y)]

    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        # Retrieve left image
        zed.retrieve_image(image, sl.VIEW.LEFT)
        zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
        zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)


        x = image.get_width()
        y = image.get_height()

        zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)

        pcdata = point_cloud.get_data()

        print(pcdata.shape)


        if(cv2.waitKey(0) % 0xFF == ord('q')):
            capture.release()
            cv2.destroyAllWindows()

        pcdata2 = np.nan_to_num(pcdata,0)
        channel = 2
        plt.imshow("frame", pcdata[:,:,0])


    zed.close()



if __name__ == "__main__":
    main()
