import random

import cv2 as cv
import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve  # type: ignore


def black():
    return 0


def green():
    return random.randint(1, 31)


def blue():
    return random.randint(32, 127)


def red():
    return random.randint(128, 255)


def white():
    return 255


color_codes = [black, green, blue, red, white]

colors = [(0, 0, 0), (77, 175, 74), (16, 114, 184), (228, 26, 28), (255, 255, 255)]
curves = {2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8}


for i in range(len(colors)):
    colors[i] = (colors[i][2], colors[i][1], colors[i][0])


def random_color_img(x: int, y: int = -1):
    if y == -1:
        y = x
    img = np.zeros((x, y, 3), np.uint8)
    for i in range(x):
        for j in range(y):
            color = random.choice(colors)
            img[i, j] = color
    return img


def point(hilbert_curve: HilbertCurve, dis: int):
    x, y = hilbert_curve.point_from_distance(dis % (hilbert_curve.max_h + 1))
    x += dis // (hilbert_curve.max_h + 1) * (hilbert_curve.max_x + 1)
    return x, y


def img_to_binary(img: np.ndarray, size: int):  # type: ignore
    # make a new image with the same size as the original image
    img2 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    # use the hilbert curve to traverse the original image
    hilbert_curve = HilbertCurve(curves[size], 2)
    print(hilbert_curve.max_h, hilbert_curve.max_x)

    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            x, y = point(hilbert_curve, i * img2.shape[1] + j)

            # print(x, y)
            img2[i, j] = img[x, y]

    with open("binary.bin", "wb") as f:
        for i in range(img2.shape[0]):
            for j in range(img2.shape[1]):
                for k in range(len(colors)):
                    if (img2[i, j] == colors[k]).all():
                        f.write(color_codes[k]().to_bytes(1, "big"))
                        break


if __name__ == "__main__":
    img = random_color_img(512, 128)
    cv.imwrite("random_color_square_img.png", img)
    cv.imshow("image", img)
    cv.waitKey(0)
    img = cv.imread("random_color_square_img.png")
    cv.imshow("image", img)
    cv.waitKey(0)
    img_to_binary(img, 128)
