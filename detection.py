"""
author: Asim Aryal
version: 020420

This is a part of Dissertation+Project submitted in partial fulfilment for the degree of
Bachelor of Science with Honours in Computing Science @ University of Stirling
The code uses ImageAI library and is to be paired with vibrations.py

Project Supervisor: Dr Kevin Swingler
"""

import math
from matplotlib import path
import msvcrt
from imageai.Detection import VideoObjectDetection
import os
import cv2
import vibrations

execution_path = os.getcwd()
# Get ImageAI video detection module
detector = VideoObjectDetection()
# set objects to detect
custom_objects = detector.CustomObjects(person=True, bottle=True, wine_glass=True, cup=True, fork=True, knife=True,
                                        spoon=True, bowl=True, banana=True, apple=True, sandwich=True, orange=True,
                                        broccoli=True, carrot=True, hot_dog=True, pizza=True, donut=True, cake=True,
                                        cell_phone=True)
# Set model type
detector.setModelTypeAsYOLOv3()
# Uncomment below as required for RetinaNet, set type and path
# detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "yolo.h5"))
# detector.setModelPath(os.path.join(execution_path, "resnet_coco_best_v2.0.1.h5"))
detector.loadModel()

camera = cv2.VideoCapture(0)
print("Camera open now.")


def process_per_frame(position_num, objects_array, object_count, c):

    """
    This function executes after each frame detected. The function is passed through in per_frame_function in
    detectCustomObjectsFromVideo ImageAI function.


    :param position_num: Position number of the frame
    :param objects_array: Array of dictionaries, with each dictionary corresponding to each object detected.
                        Each dictionary contains 'name', 'percentage_probability' and 'box_points'
    :param object_count: A dictionary with with keys being the name of each unique objects and
                         value are the number of instances of the object present
    :param c: Unused Parameter - Numpy array of the frame
    :return: None
    """

    print(objects_array)

    for detected_objects in objects_array:

        # Button press to exit
        if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
            release_detection()
            set_return_detected_frame(False)
            vibrations.close_glove()
            return None

        # Hand detection - model detects body parts as "person" with high accuracy
        if detected_objects.get("name") == "person":
            # X and Y coordinates in order of (x1, y1, x2, y2).
            # x1 and y1 refers to the lower left and x2 and y2 refers to the upper right.
            box_points_person = detected_objects.get("box_points")
            x1, y1, x2, y2 = get_box_points(box_points_person)
            # getting the vertices
            top_left_x_person, top_left_y_person = x1, y2
            top_right_x_person, top_right_y_person = x2, y2
            bottom_left_x_person, bottom_left_y_person = x1, y1
            bottom_right_x_person, bottom_right_y_person = x2, y1
            # getting the diagonal centre of the hand
            centre_x_person, centre_y_person = midpoint(box_points_person)
            ref_x_person, ref_y_person = centre_x_person, centre_y_person
            # getting midpoints for each side of the hand so the reference can be set later
            right_midpoint_x_person, right_midpoint_y_person = midpoint([x2, y2, x2, y1])
            left_midpoint_x_person, left_midpoint_y_person = midpoint([x1, y2, x1, y1])
            bottom_midpoint_x_person, bottom_midpoint_y_person = midpoint([x1, y1, x2, y1])
            top_midpoint_x_person, top_midpoint_y_person = midpoint([x1, y1, x2, y2])

            # Loop again to find object while processing the same frame
            for detected_objects_again in objects_array:
                if detected_objects_again.get("name") == object_name_input:
                    print("Found ", object_name_input, " and Person")
                    name_object = detected_objects_again.get("name")
                    box_points_object = detected_objects_again.get("box_points")
                    # Getting reference points for objects
                    centre_x_object, centre_y_object = midpoint(box_points_object)
                    x1, y1, x2, y2 = get_box_points(box_points_object)
                    # getting the vertices of the object
                    top_left_x_object, top_left_y_object = x1, y2
                    top_right_x_object, top_right_y_object = x2, y2
                    bottom_left_x_object, bottom_left_y_object = x1, y1
                    bottom_right_x_object, bottom_right_y_object = x2, y1
                    ref_x_object, ref_y_object = centre_x_object, centre_y_object
                    # getting midpoints for each side of the object so the reference can be set
                    right_midpoint_x_object, right_midpoint_y_object = midpoint([x2, y2, x2, y1])
                    left_midpoint_x_object, left_midpoint_y_object = midpoint([x1, y2, x1, y1])
                    bottom_midpoint_x_object, bottom_midpoint_y_object = midpoint([x1, y1, x2, y1])
                    top_midpoint_x_object, top_midpoint_y_object = midpoint([x1, y1, x2, y2])

                    # setting a reference point for hand, based on where the object is located
                    # e.g. if located towards the top-left, i.e. object's x coordinate will be lesser than person's
                    # and object's y coordinate will be bigger than person's
                    # hence, taking top left vertex of the hand and bottom right vertex of the object as references

                    # top left
                    if centre_x_object < centre_x_person and centre_y_object > centre_y_person:
                        ref_x_person, ref_y_person = top_left_x_person, top_left_y_person
                        ref_x_object, ref_y_object = bottom_right_x_object, bottom_right_y_object
                        print(object_name_input, " is on the top left")
                        vibrations.buzz_top_left(50, name_object)
                    # top right
                    elif centre_x_object > centre_x_person and centre_y_object > centre_y_person:
                        ref_x_person, ref_y_person = top_right_x_person, top_right_y_person
                        ref_x_object, ref_y_object = bottom_left_x_object, bottom_left_y_object
                        print(object_name_input, " is on the top right")
                        vibrations.buzz_top_right(50, name_object)
                    # bottom right
                    elif centre_x_object < centre_x_person and centre_y_object < centre_y_person:
                        ref_x_person, ref_y_person = bottom_right_x_person, bottom_right_y_person
                        ref_x_object, ref_y_object = top_left_x_object, top_left_y_object
                        print(object_name_input, " is on the bottom right")
                        vibrations.buzz_bottom_right(50, name_object)
                    # bottom left
                    elif centre_x_object < centre_x_person and centre_y_object < centre_y_person:
                        ref_x_person, ref_y_person = bottom_left_x_person, bottom_left_y_person
                        ref_x_object, ref_y_object = top_right_x_object, top_right_y_object
                        print(object_name_input, " is on the bottom left")
                        vibrations.buzz_bottom_left(50, name_object)
                    # left
                    elif centre_x_object < centre_x_person:
                        ref_x_person, ref_y_person = left_midpoint_x_person, left_midpoint_y_person
                        ref_x_object, ref_y_object = right_midpoint_x_object, right_midpoint_y_object
                        print(object_name_input, " is on the left")
                        vibrations.buzz("l", 50, name_object)
                    # right
                    elif centre_x_object > centre_x_person:
                        ref_x_person, ref_y_person = right_midpoint_x_person, right_midpoint_y_person
                        ref_x_object, ref_y_object = left_midpoint_x_object, left_midpoint_y_object
                        print(object_name_input, " is on the right")
                        vibrations.buzz("r", 50, name_object)
                    # above
                    elif centre_y_object > centre_y_person:
                        ref_x_person, ref_y_person = top_midpoint_x_person, top_midpoint_y_person
                        ref_x_object, ref_y_object = bottom_midpoint_x_object, bottom_midpoint_y_object
                        print(object_name_input, " is above")
                        vibrations.buzz("t", 50, name_object)
                    # below
                    elif centre_y_object < centre_y_person:
                        ref_x_person, ref_y_person = bottom_midpoint_x_person, bottom_midpoint_y_person
                        ref_x_object, ref_y_object = top_midpoint_x_object, top_midpoint_y_object
                        print(object_name_input, " is below")
                        vibrations.buzz("b", 50, name_object)
                    # finding the distance between object and person, using reference point set above
                    distance_to_object = manhattan_distance(ref_x_person, ref_y_person, ref_x_object,
                                                            ref_y_object)
                    print("Manhattan DISTANCE BETWEEN ", name_object, " AND Person: ", distance_to_object)
                    print("Euclidean Distance: ",
                          euclidean_distance(ref_x_person, ref_y_person, ref_x_object, ref_y_object))

                    # From a height of 152 cm using a field of vision of 78 degrees
                    # Additional distance checks and longer vibrations based on distance
                    if distance_to_object < 50:
                        vibrations.buzz("a", 100, detected_objects_again.get("name"))
                        print("Hand has reached", object_name_input)
                        # Return False sets return_detected_
                        set_return_detected_frame(False)
                        vibrations.close_glove()
                        release_detection()
                        return None

                    # Monitoring the distance
                    if distance_to_object < 200:
                        print("Hand is closer to ", name_object)
                        send_vibrations(75, detected_objects_again.get("name"), ref_x_object,
                                        ref_y_object, ref_x_person, ref_y_person)

                    elif distance_to_object < 300:
                        print("Hand is close to", name_object)
                        send_vibrations(60, detected_objects_again.get("name"), ref_x_object,
                                        ref_y_object, ref_x_person, ref_y_person)
    if "person" not in object_count:
        print("Could not find Person in Frame number:  ", position_num)
    if object_name_input not in object_count:
        print("Could not find: ", object_name_input, "in Frame number: ", position_num)
    return None


def send_vibrations(lengthms, name, ref_x_obj, ref_y_obj, ref_x_per, ref_y_per):
    """
    Sends vibrations based on location of x,y coordinates of object and person
    :param lengthms: length of vibration
    :param name: name of object
    :param ref_x_obj: x coordinate of object reference point
    :param ref_y_obj: y coordinate of object reference point
    :param ref_x_per: x coordinate of person reference point
    :param ref_y_per: y coordinate of person reference point
    :return: None
    """
    if ref_x_obj > ref_x_per:
        vibrations.buzz("r", lengthms, name)
    if ref_x_obj < ref_x_per:
        vibrations.buzz("l", lengthms, name)
    if ref_y_obj > ref_y_per:
        vibrations.buzz("t", lengthms, name)
    if ref_y_obj < ref_y_per:
        vibrations.buzz("b", lengthms, name)


def get_box_points(box_points):
    """
    Gets split box points
    :param box_points: list of box-plots [x1,y1,x2,y2]
    :return: individual plot points in order of x1, y1, x2, y2
    """
    x1 = box_points[0]
    y1 = box_points[1]
    x2 = box_points[2]
    y2 = box_points[3]
    return x1, y1, x2, y2


def euclidean_distance(x1, y1, x2, y2):
    """
    Returns euclidean distance
    :param x1: first x coordinate
    :param y1: first y coordinate
    :param x2: second x coordinate
    :param y2: second y coordinate
    :return: euclidean distance between x1,y1 and x2,y2
    """
    return round(math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)), 2)


def manhattan_distance(x1, y1, x2, y2):
    """
    Returns manhattan distance
    :param x1: first x coordinate
    :param y1: first y coordinate
    :param x2: second x coordinate
    :param y2: second y coordinate
    :return: manhattan distance between x1,y1 and x2 y2
    """
    return abs(x2 - x1) + abs(y2 - y1)


def midpoint(box_points):
    """
    Returns midpoint from box points
    :param box_points: a list of coordinate points in order of (x1, y1, x2, y2)
    :return: midpoint between x1,y1 and x2,y2
    """
    # The box_points contains values for the X and Y coordinates in order of (x1, y1, x2, y2).
    mid_x = int((box_points[0] + box_points[2]) / 2)
    mid_y = int((box_points[1] + box_points[3]) / 2)
    return mid_x, mid_y


def viewing_angle(perpendicular_height, base_length):
    """
    If the camera is not in an overhead position and perpendicular height and base length are known

    :param perpendicular_height: Height from Table to Camera
    :param base_length: Distance between Centre of Table and Camera
    :return: angle of sight from the camera i.e. 90 - (inverse of tan (p/b))
    """
    return 90 - math.atan(perpendicular_height / base_length)


def distance_from_camera(perpendicular_height, base_length):
    """
    If the camera is not in an overhead position and the distance from base of camera and height to camera are known

    :param perpendicular_height: Height from Table to Camera
    :param base_length: Distance between Centre of Table and Camera
    :return: Distance between the camera and the object
    """
    return math.sqrt(perpendicular_height ^ 2 + base_length ^ 2)


def release_detection():
    """
    Releases OpenCV camera
    :return: None
    """
    print("Camera released")
    camera.release()


def set_return_detected_frame(keep_detecting):
    """
    Used to set return_detected_frame in imageAI detectObjectsFromVideo to true/false
    :param keep_detecting: boolean
    :return: boolean
    """
    if keep_detecting is True:
        return True
    else:
        return False


def in_polygon(query_x, query_y, vertices_x, vertices_y):
    """
    Checks if query points are inside the vertices of quadrilateral i.e. space between the object and the hand
    :param query_x: numpy array of x co-ordinates to be checked | match index to query_y
    :param query_y: numpy array of co-ordinates to be checked | match index to query_x
    :param vertices_x: numpy array of x vertices to be checked |  match index to vertices_y
    :param vertices_y: numpy array of y vertices to be checked | match index to vertices_x
    :return: query points that are within the vertices points, matched indices for x and y
    """
    # get current shape of x vertices
    shape = query_x.shape
    # check if numpy arrays are compatible
    query_x = query_x.reshape(-1)
    query_y = query_y.reshape(-1)
    vertices_x = vertices_x.reshape(-1)
    vertices_y = vertices_y.reshape(-1)
    # get each query point
    q = [(query_x[i], query_y[i]) for i in range(query_x.shape[0])]
    # get the closed path between the vertices
    p = path.Path([(vertices_x[i], vertices_y[i]) for i in range(vertices_x.shape[0])])
    # return query points q if they are within p
    return p.contains_points(q).reshape(shape)


def test_manhattan():
    if manhattan_distance(2, 8, 10, 2) == 14:
        return True
    else:
        return False


def test_euclidean():
    if euclidean_distance(2, 8, 10, 2) == 10:
        return True
    else:
        return False


def test_midpoint():
    x, y = midpoint([2, 8, 10, 2])
    if x is 6 and y is 5:
        return True
    else:
        return False


print("Calculation Checks:")
print("Manhattan: ", test_manhattan())
print("Euclidean: ", test_euclidean())
print("Mid Point:", test_midpoint())

# For next detection
continue_detection = "Y"
object_name_input = ""
# Run until user wants to continue
while continue_detection.upper() == "Y":
    # Get object name to find
    object_name_input = input("Enter object name: ")
    """
    Calls ImageAI detectCustomObjectsFromVideo and passes per_frame_function to process_per_frame
    The video file obtained from    the detection is saved in the working directory as detected_video.avi
    @:param: custom_objects: dictionary of objects enabled for detection
    @:param: return_detected_frame : To obtain the last detected video frame into the per_per_frame_function
    @:param: per_frame_function : see process_per_frame documentation
    @:param: camera_input : live camera input
    @:param: save_detected_video : Option to save detected video
    @:param: output_file_path : path and filename for saving detected video
    @:param: minimum_percentage_probability : minimum percentage probability for nominating a detected object
    @:param: frames_per_second: Frames per second
    @:param: log_process : states if the progress of the frame processed is to be logged to console
    """
    video_path = detector.detectCustomObjectsFromVideo(custom_objects=custom_objects,
                                                       return_detected_frame=set_return_detected_frame(True),
                                                       per_frame_function=process_per_frame,
                                                       camera_input=camera,
                                                       save_detected_video=True, output_file_path="detected_video",
                                                       minimum_percentage_probability=50,
                                                       frames_per_second=2, log_progress=True)
    continue_detection = input("Find another object?(Y/N) ")

    if continue_detection.upper() == "Y":
        vibrations.open_glove()
        camera = cv2.VideoCapture(0)
    else:
        print("Shutting down")

# EOF
