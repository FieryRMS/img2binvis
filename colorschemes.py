import math
import random
from typing import Tuple

from colormath.color_conversions import convert_color  # type: ignore
from colormath.color_diff import delta_e_cie2000  # type: ignore
from colormath.color_objects import LabColor, sRGBColor  # type: ignore

type Color = Tuple[int, int, int]


import numpy


def patch_asscalar(a):  # type: ignore
    return a.item()  # type: ignore


# patch numpy.asscalar
setattr(numpy, "asscalar", patch_asscalar)


def HEX2RGB(lst: list[str]):
    res: list[Color] = []
    for i in lst:
        hx = i.lstrip("#")
        res.append((int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)))
    return res


def arr2dict(lst: list[Color]) -> dict[Color, list[int]]:
    d: dict[Color, list[int]] = {}
    for i, v in enumerate(lst):
        if v not in d:
            d[v] = []
        d[v].append(i)
    return d


class ColorScheme:
    colors = [(0, 0, 0)]
    colormap = {(0, 0, 0): [0]}

    @classmethod
    def byte2color(cls, byte: int) -> Color:
        if byte < 0 or byte > 255:
            raise ValueError("Byte out of range")
        return cls.colors[byte]

    @classmethod
    def color2byte(cls, color: Color, closest: bool = False, byte: int = -1) -> int:
        if closest:
            mindiff = math.inf
            minclr = (0, 0, 0)
            for c in cls.colormap.keys():
                diff = cls.colordiff(c, color)
                if diff < mindiff:
                    mindiff = diff
                    minclr = c

            if byte == -1:
                return random.choice(cls.colormap[minclr])

            mindiff = math.inf
            minbyte = -1
            for b in cls.colormap[minclr]:
                diff = abs(b - byte)
                if diff < mindiff:
                    mindiff = diff
                    minbyte = b
            return minbyte

        if color not in cls.colormap:
            return -1
        return random.choice(cls.colormap[color])

    @classmethod
    def randColor(cls) -> Color:
        return random.choice(list(cls.colormap.keys()))

    @staticmethod
    def colordiff(c1: Color, c2: Color) -> float:
        rgb1 = sRGBColor(c1[2], c1[1], c1[0], is_upscaled=True)
        rgb2 = sRGBColor(c2[2], c2[1], c2[0], is_upscaled=True)
        lab1: LabColor = convert_color(rgb1, LabColor)  # type: ignore
        lab2: LabColor = convert_color(rgb2, LabColor)  # type: ignore
        return delta_e_cie2000(lab1, lab2)  # type: ignore


class ByteClass(ColorScheme):
    colors = HEX2RGB(
        [
            (
                "#000000"
                if i == 0
                else (
                    "#ffffff"
                    if i == 255
                    else (
                        "#1072b8"
                        if (i >= 32 and i <= 126) or i in [9, 10, 13]
                        else "#4daf4a" if i < 32 else "#e41a1c"
                    )
                )
            )
            for i in range(256)
        ]
    )

    colormap = arr2dict(colors)


class ByteMagnitude(ColorScheme):
    # fmt: off
    colors = HEX2RGB(
        [
            "#000000","#020101","#050103","#070204","#0a0306","#0c0407","#0e0409","#10050a",
            "#12060c","#13070d","#15070e","#16080f","#170910","#180a11","#1a0b12","#1b0b13",
            "#1c0c14","#1d0d15","#1e0d16","#1e0e17","#1f0f18","#200f18","#211019","#22101a",
            "#23111b","#24111c","#25121c","#26121d","#27121e","#29131f","#2a1320","#2b1420",
            "#2c1421","#2d1422","#2e1523","#2f1524","#301624","#311625","#321726","#321727",
            "#331728","#341829","#351829","#36192a","#37192b","#381a2c","#391a2d","#3a1b2e",
            "#3b1b2f","#3c1c2f","#3d1c30","#3e1d31","#3f1d32","#401e33","#411e34","#411f34",
            "#421f35","#432036","#442137","#452138","#462239","#47223a","#48233b","#48233c",
            "#49243c","#4a253d","#4b253e","#4c263f","#4d2740","#4d2741","#4e2842","#4f2843",
            "#502943","#512a44","#512a45","#522b46","#532c47","#542c48","#552d49","#552e4a",
            "#562e4b","#572f4c","#58304d","#58314d","#59314e","#5a324f","#5a3350","#5b3351",
            "#5c3452","#5d3553","#5d3654","#5e3655","#5f3756","#5f3857","#603958","#613959",
            "#613a5a","#623b5a","#633c5b","#633c5c","#643d5d","#643e5e","#653f5f","#664060",
            "#664061","#674162","#674263","#684364","#694465","#694466","#6a4567","#6a4668",
            "#6b4769","#6b486a","#6c496b","#6c496c","#6d4a6d","#6d4b6d","#6e4c6e","#6e4d6f",
            "#6f4e70","#6f4f71","#704f72","#705073","#715174","#715275","#725376","#725477",
            "#725578","#735679","#73577a","#74577b","#74587c","#74597d","#755a7e","#755b7f",
            "#765c80","#765d81","#765e82","#775f83","#776084","#776185","#786186","#786287",
            "#786388","#786489","#79658a","#79668b","#79678c","#79688d","#7a698e","#7a6a8f",
            "#7a6b90","#7a6c91","#7b6d92","#7b6e93","#7b6f94","#7b7095","#7b7196","#7b7297",
            "#7c7398","#7c7499","#7c759a","#7c769b","#7c779c","#7c789d","#7c799e","#7c7a9f",
            "#7c7ba0","#7c7ca2","#7c7da2","#7c7ea4","#7c7fa5","#7c80a6","#7c81a7","#7c82a8",
            "#7c83a9","#7c84aa","#7c85ab","#7c86ac","#7c87ad","#7c88ae","#7c89af","#7c8ab0",
            "#7c8bb1","#7c8cb2","#7b8db3","#7b8eb4","#7b8fb5","#7b90b6","#7b91b7","#7a92b8",
            "#7a93b9","#7a94bb","#7a95bc","#7996bd","#7997be","#7998bf","#789ac0","#789bc1",
            "#789cc2","#779dc3","#779ec4","#769fc5","#76a0c6","#75a1c7","#75a2c8","#74a3c9",
            "#74a4ca","#73a5cc","#73a6cd","#72a7ce","#71a9cf","#71aad0","#70abd1","#6facd2",
            "#6fadd3","#6eaed4","#6dafd5","#6cb0d6","#6cb1d7","#6bb2d8","#6ab4da","#69b5db",
            "#68b6dc","#67b7dd","#66b8de","#65b9df","#64bae0","#63bbe1","#61bce2","#60bee3",
            "#5fbfe4","#5ec0e6","#5cc1e7","#5bc2e8","#59c3e9","#58c4ea","#56c5eb","#55c7ec",
            "#53c8ed","#51c9ee","#4fcaef","#4dcbf1","#4bccf2","#49cdf3","#46cff4","#44d0f5",
            "#41d1f6","#3ed2f7","#3bd3f8","#38d4f9","#34d5fb","#30d7fc","#2cd8fd","#27d9fe",
        ]
    )
    # fmt: on
    colormap = arr2dict(colors)


class ByteDetail(ColorScheme):
    # fmt: off
    colors = HEX2RGB(
        [
            "#000000","#002020","#203f1f","#3f1f20","#400000","#602000","#7f1f20","#5f203f",
            "#400040","#602040","#7f1f60","#5f207f","#3f007f","#1f005f","#202040","#1f3f60",
            "#3f407f","#1f405f","#206040","#1f7f60","#407f7f","#605f7f","#7f605f","#5f5f40",
            "#407f3f","#605f3f","#7f601f","#5f5f00","#3f7f00","#3f5f20","#1f401f","#006020",
            "#008000","#20a000","#3f9f20","#1fa03f","#008040","#208060","#1fa07f","#20bf5f",
            "#00c040","#20c060","#1fe07f","#20ff5f","#00ff3f","#00df1f","#20c020","#3fe01f",
            "#40ff3f","#40df1f","#60c020","#7fe01f","#7fff40","#5fff60","#60df7f","#5fc05f",
            "#7fbf40","#5fbf60","#609f7f","#5f805f","#7f803f","#5fa03f","#409f1f","#60a000",
            "#808000","#a0a000","#bf9f20","#9fa03f","#808040","#a08060","#9fa07f","#a0bf5f",
            "#80c040","#a0c060","#9fe07f","#a0ff5f","#80ff3f","#80df1f","#a0c020","#bfe01f",
            "#c0ff3f","#c0df1f","#e0c020","#ffe01f","#ffff40","#dfff60","#e0df7f","#dfc05f",
            "#ffbf40","#dfbf60","#e09f7f","#df805f","#ff803f","#dfa03f","#c09f1f","#e0a000",
            "#ff7f00","#df7f20","#e05f3f","#df401f","#ff3f00","#ff1f20","#df001f","#c02020",
            "#bf3f00","#bf1f20","#9f001f","#802020","#804000","#a06000","#bf5f20","#9f603f",
            "#804040","#a06040","#bf5f60","#9f607f","#803f7f","#801f5f","#a00060","#bf205f",
            "#c03f7f","#c01f5f","#e00060","#ff205f","#ff407f","#df405f","#e06040","#df7f60",
            "#ff7f80","#df7fa0","#e05fbf","#df409f","#ff3f80","#ff1fa0","#df009f","#c020a0",
            "#bf3f80","#bf1fa0","#9f009f","#8020a0","#804080","#a06080","#bf5fa0","#9f60bf",
            "#8040c0","#a060c0","#bf5fe0","#9f60ff","#803fff","#801fdf","#a000e0","#bf20df",
            "#c03fff","#c01fdf","#e000e0","#ff20df","#ff40ff","#df40df","#e060c0","#df7fe0",
            "#ff80ff","#dfa0ff","#c09fdf","#e0a0c0","#ff80bf","#df809f","#e0a080","#dfbfa0",
            "#ffc0bf","#dfc09f","#e0e080","#dfffa0","#ffffc0","#ffdfe0","#dfc0df","#c0e0e0",
            "#bfffc0","#bfdfe0","#9fc0df","#80e0e0","#80ffbf","#a0ff9f","#9fdf80","#a0c0a0",
            "#80bfbf","#a0bf9f","#9f9f80","#a080a0","#8080c0","#a0a0c0","#bf9fe0","#9fa0ff",
            "#7f80ff","#5fa0ff","#409fdf","#60a0c0","#7f80bf","#5f809f","#60a080","#5fbfa0",
            "#7fc0bf","#5fc09f","#60e080","#5fffa0","#7fffc0","#7fdfe0","#5fc0df","#40e0e0",
            "#3fffc0","#3fdfe0","#1fc0df","#00e0e0","#00ffbf","#20ff9f","#1fdf80","#20c0a0",
            "#00bfbf","#20bf9f","#1f9f80","#2080a0","#0080c0","#20a0c0","#3f9fe0","#1fa0ff",
            "#007fff","#005fdf","#2040e0","#3f60df","#407fff","#605fff","#7f60df","#5f5fc0",
            "#407fbf","#605fbf","#7f609f","#5f5f80","#3f7f80","#1f7fa0","#205fbf","#1f409f",
            "#3f3f80","#1f3fa0","#201fbf","#1f009f","#400080","#602080","#7f1fa0","#5f20bf",
            "#4000c0","#6020c0","#7f1fe0","#5f20ff","#3f00ff","#3f20df","#1f3fe0","#ffffff"
        ]
    )
    # fmt: on
    colormap = arr2dict(colors)
