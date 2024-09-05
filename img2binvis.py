import math
import os
import random

import cv2 as cv
import numpy as np
import numpy.typing as npt
from hilbertcurve.hilbertcurve import HilbertCurve  # type: ignore


def black():
    return 0


def green():
    res = random.randint(1, 31)
    while res in [9, 10, 13]:
        res = random.randint(1, 31)
    return res


def blue():
    res = random.randint(32 - 3, 126)
    if res < 32:
        res = 31 - res
        return [9, 10, 13][res]
    return res


def red():
    return random.randint(127, 254)


def white():
    return 255


color_codes = [black, green, blue, red, white]


colors = [(0, 0, 0), (77, 175, 74), (16, 114, 184), (228, 26, 28), (255, 255, 255)]
curves = {2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8}


def bin2color(bin: int):
    if bin == 0:
        return colors[0]
    if bin in [9, 10, 13]:
        return colors[2]
    if bin >= 1 and bin <= 31:
        return colors[1]
    if bin >= 32 and bin <= 126:
        return colors[2]
    if bin >= 127 and bin <= 254:
        return colors[3]
    return colors[4]


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


def dis2point(hilbert_curve: HilbertCurve, dis: int):
    x, y = hilbert_curve.point_from_distance(dis % (hilbert_curve.max_h + 1))
    x += (dis // (hilbert_curve.max_h + 1)) * (hilbert_curve.max_x + 1)
    return x, y


def point2dis(hilbert_curve: HilbertCurve, x: int, y: int):
    x_mod = x % (hilbert_curve.max_x + 1)
    dis = hilbert_curve.distance_from_point([x_mod, y])
    dis += (x // (hilbert_curve.max_x + 1)) * (hilbert_curve.max_h + 1)
    return dis


def img_to_binary(
    img: npt.NDArray[np.uint8],
    filename: str,
    size: int,
    ori_data: npt.NDArray[np.uint8] | None = None,
):
    # make a new image with the same size as the original image
    img2 = np.zeros_like(img)  # type: ignore

    # use the hilbert curve to traverse the original image
    hilbert_curve = HilbertCurve(curves[size], 2)

    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            x, y = dis2point(hilbert_curve, i * size + j)
            img2[i, j] = img[x, y]

    if ori_data is not None:
        filesize = ori_data.shape[0]
        ratio = size * size * 4 / filesize
    else:
        filesize = None
        ratio = None

    with open(filename, "wb") as f:
        for i in range(img2.shape[0]):
            for j in range(img2.shape[1]):
                for k in range(len(colors)):
                    if (img2[i, j] == colors[k]).all():
                        if ori_data is None:
                            f.write(color_codes[k]().to_bytes(1, "big"))
                        else:
                            dis = point2dis(hilbert_curve, i, j)
                            idx = math.floor(dis / ratio)
                            if idx == i * size + j or colors[k] != bin2color(
                                int(ori_data[idx])
                            ):
                                f.write(color_codes[k]().to_bytes(1, "big"))
                            else:
                                f.write(int(ori_data[idx]).to_bytes(1, "big"))
                        break


def binary_to_img(data: npt.NDArray[np.uint8], size: int):
    hilbert_curve = HilbertCurve(curves[size], 2)
    filesize = data.shape[0]
    ratio = size * size * 4 / filesize
    img = np.zeros((size * 4, size, 3), np.uint8)
    for i in range(size * 4):
        for j in range(size):
            dis = point2dis(hilbert_curve, i, j)
            idx = math.floor(dis / ratio)
            img[i, j] = bin2color(int(data[idx]))
    return img


def get_binary(filepath: str):
    filesize = os.path.getsize(filepath)
    data = np.zeros((filesize), np.uint8)
    with open(filepath, "rb") as f:
        distance = 0
        while byte := f.read(1):
            data[distance] = int.from_bytes(byte, "big")
            distance += 1
    return data


if __name__ == "__main__":
    # img = random_color_img(512, 128)
    # # cv.imwrite("random_color_square_img.png", img)
    # cv.imshow("image", img)
    # cv.waitKey(0)
    # img = cv.imread("random_color_square_img.png")
    # img_to_binary(img, "binary.bin", 128)
    data = get_binary(".cph/main.bin")
    img = binary_to_img(data, 256)
    cv.imwrite("reconstructed.png", img)
    cv.imshow("image", img)
    cv.waitKey(0)
    img = cv.imread("reconstructed.png")
    img_to_binary(img, "binaryreq.bin", 256, data)  # type: ignore
