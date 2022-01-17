import argparse
import os

import cv2

# initialize the list of reference points
refPt = []
r = None


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    global r
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


def select_area(event, x, y, flags, param):
    # grab references to the global variables
    global refPt
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        refPt.append((x, y))
        # draw a rectangle around the region of interest
        cv2.rectangle(resize, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", resize)


def save_and_close():
    with open(args["annotate"], 'a') as file:
        for d in data:
            file.write('\n'+d)
    file.close()


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="Path to the images")
ap.add_argument("-a", "--annotate", required=False, help="Path to save annotations", default="train.txt")
ap.add_argument("-l", "--label", required=True, help="Label for region")
args = vars(ap.parse_args())

data = []
for f in os.listdir(args["path"]):
    if not f.lower().endswith(('.bmp', '.jpeg', '.jpg', '.png', '.tif', '.tiff')):
        continue
    fullpath = f'{args["path"]}/{f}'

    # load the image, clone it, and setup the mouse callback function
    image = cv2.imread(fullpath)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", select_area)
    confirm = False
    while not confirm:
        try:
            # keep looping until the 'q' key is pressed or confirmed
            # display the image and wait for a keypress
            resize = ResizeWithAspectRatio(image, height=790)
            cv2.imshow("image", resize)
            key = cv2.waitKey() & 0xFF
            # if the 'c' key is pressed, confirm & continue
            if key == ord("c"):
                if len(refPt) > 0:
                    x1 = max(refPt[0][0] if refPt[0][0] < refPt[1][0] else refPt[1][0], 0)
                    x2 = min(refPt[0][0] if refPt[0][0] > refPt[1][0] else refPt[1][0], resize.shape[:2][1])
                    y1 = max(refPt[0][1] if refPt[0][1] < refPt[1][1] else refPt[1][1], 0)
                    y2 = min(refPt[0][1] if refPt[0][1] > refPt[1][1] else refPt[1][1], resize.shape[:2][0])
                    if r is None:
                        data.append(','.join([fullpath, str(x1), str(y1), str(x2), str(y2), args["label"]]))
                    else:
                        data.append(
                            ','.join([fullpath, str(int(x1 / r)), str(int(y1 / r)), str(int(x2 / r)), str(int(y2 / r)),
                                      args["label"]]))
                confirm = True
            # if the 'r' key is pressed, reset selection
            elif key == ord("r"):
                refPt = []
                image = clone.copy()
            # Quit
            elif key == ord('q'):
                # close all open windows
                cv2.destroyAllWindows()
                save_and_close()
                exit()
        except Exception as e:
            print(e)
            image = clone.copy()
save_and_close()
