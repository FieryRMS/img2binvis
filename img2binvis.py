import math
import os
import random

import cv2 as cv
import numpy as np
import numpy.typing as npt
from hilbertcurve.hilbertcurve import HilbertCurve  # type: ignore


def black() -> int:
    return 0


def green() -> int:
    res = random.randint(1, 31)
    while res in [9, 10, 13]:
        res = random.randint(1, 31)
    return res


def blue() -> int:
    res = random.randint(32 - 3, 126)
    if res < 32:
        res = 31 - res
        return [9, 10, 13][res]
    return res


def red() -> int:
    return random.randint(127, 254)


def white() -> int:
    return 255


color_codes = [black, green, blue, red, white]


colors = [(0, 0, 0), (77, 175, 74), (16, 114, 184), (228, 26, 28), (255, 255, 255)]
curves = {2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8}

# convert RGB to BGR
for i in range(len(colors)):
    colors[i] = (colors[i][2], colors[i][1], colors[i][0])


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


def color2idx(color: npt.NDArray[np.uint8]):
    for i in range(len(colors)):
        if (color == colors[i]).all():
            return i
    return -1


def random_data(x: int, y: int = -1):
    if y == -1:
        y = x * 4
    data = np.zeros((x * y), np.uint8)
    for i in range(x * y):
        color = random.randint(0, 4)
        data[i] = color_codes[color]()
    return data


def dis2point(hilbert_curve: HilbertCurve, dis: int):
    x, y = hilbert_curve.point_from_distance(dis % (hilbert_curve.max_h + 1))
    x += (dis // (hilbert_curve.max_h + 1)) * (hilbert_curve.max_x + 1)
    return x, y


def point2dis(hilbert_curve: HilbertCurve, x: int, y: int):
    x_mod = x % (hilbert_curve.max_x + 1)
    dis = hilbert_curve.distance_from_point([x_mod, y])
    dis += (x // (hilbert_curve.max_x + 1)) * (hilbert_curve.max_h + 1)
    return dis


def get_size(filesize: int):
    return 256
    size = 0
    for i in sorted(curves.keys(), reverse=True):
        if i * i * 4 <= filesize:
            size = i
            break
    if size == 0:
        raise ValueError("Invalid filesize")
    return size


def img_to_binary(
    img: npt.NDArray[np.uint8],
    filename: str,
    data: npt.NDArray[np.uint8],
    offset_start: int = 0,
    offset_end: int = math.inf,  # pyright: ignore[reportArgumentType]
):
    # make a new image with the same size as the original image
    offset_end = min(offset_end, data.shape[0])
    filesize = offset_end - offset_start
    size = get_size(filesize)
    ratio = size * size * 4 / filesize

    # use the hilbert curve to traverse the original image
    hilbert_curve = HilbertCurve(curves[size], 2)

    for i in range(size * 4):
        for j in range(size):
            dis = point2dis(hilbert_curve, i, j)
            idx = math.floor(dis / ratio) + offset_start
            if (bin2color(int(data[idx])) != img[i, j]).all():
                data[idx] = color_codes[color2idx(img[i, j])]()

    with open(filename, "wb") as f:
        f.write(data)


def binary_to_img(
    data: npt.NDArray[np.uint8],
    offset_start: int = 0,
    offset_end: int = math.inf,  # pyright: ignore[reportArgumentType]
):
    offset_end = min(offset_end, data.shape[0])
    filesize = offset_end - offset_start
    size = get_size(filesize)
    hilbert_curve = HilbertCurve(curves[size], 2)
    ratio = size * size * 4 / filesize
    img = np.zeros((size * 4, size, 3), np.uint8)
    for i in range(size * 4):
        for j in range(size):
            dis = point2dis(hilbert_curve, i, j)
            idx = math.floor(dis / ratio)
            img[i, j] = bin2color(int(data[offset_start + idx]))
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
    data = get_binary("temp/sample.jpg")  # get binary data from file
    offset_start = 36928
    offset_end = 82457
    img = binary_to_img(data, offset_start, offset_end)

    # save then show the image
    cv.imwrite("temp/reconstructed.png", img)
    cv.imshow("image", img)

    # you can now edit the image file, and then close the opencv window to use the edited file
    cv.waitKey(0)

    img = cv.imread("temp/reconstructed.png").astype(np.uint8)
    img_to_binary(img, "temp/processed.jpg", data, offset_start, offset_end)
