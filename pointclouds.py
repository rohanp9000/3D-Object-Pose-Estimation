import pyzed.sl as sl
import math
import numpy as np
import sys

def main():
    # Create a Camera object
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

    # Capture 50 images and depth, then stop
    i = 0
    image = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat()

    mirror_ref = sl.Transform()
    mirror_ref.set_translation(sl.Translation(2.75,4.0,0))
    tr_np = mirror_ref.m

    while i < 50:
        # A new image is available if grab() returns SUCCESS
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.VIEW.LEFT)
            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)


            x = round(image.get_width() / 2)
            y = round(image.get_height() / 2)
            print("width: ", x)
            print("height: ", y)
            err, point_cloud_value = point_cloud.get_value(x, y)

            #distance formula
            distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                                 point_cloud_value[1] * point_cloud_value[1] +
                                 point_cloud_value[2] * point_cloud_value[2])

            point_cloud_np = point_cloud.get_data()
            point_cloud_np.dot(tr_np)

            if not np.isnan(distance) and not np.isinf(distance):
                distance = round(distance)
                print("Distance to Camera at ({0}, {1}): {2} mm\n".format(x, y, distance))
                # Increment the loop
                i = i + 1
            else:
                print("invalid\n")
            sys.stdout.flush()


    zed.close()


if __name__ == "__main__":
    main()
