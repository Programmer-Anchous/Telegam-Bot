from PIL import Image, ImageFilter

import numpy as np


def blur(im):
    im = im.filter(ImageFilter.BLUR)
    return im


def contour(im):
    im = im.filter(ImageFilter.CONTOUR)
    return im


def detail(im):
    im = im.filter(ImageFilter.DETAIL)
    return im


def edge_enhance(im):
    im = im.filter(ImageFilter.EDGE_ENHANCE)
    return im


def emboss(im):
    im = im.filter(ImageFilter.EMBOSS)
    return im


def find_edges(im):
    im = im.filter(ImageFilter.FIND_EDGES)
    return im


def sharpen(im):
    im = im.filter(ImageFilter.SHARPEN)
    return im


def smooth(im):
    im = im.filter(ImageFilter.SMOOTH)
    return im


def unsharp_mask(im, radius=2, percent=300, threshold=3):
    filter1 = ImageFilter.UnsharpMask(
        radius=radius, percent=percent, threshold=threshold
    )
    im = im.filter(filter1)
    return im


def stereo_effect(im, delta=10):
    # creates a stereo effect
    delta //= 2
    pixels_im = im.load()
    new_im = im.copy()
    pixels_new_im = new_im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            colors = list(pixels_im[i, j])
            colors[0] = pixels_im[i - delta, j][0]
            pixels_new_im[i, j] = tuple(colors)
    return new_im


def lightest_pixel(pixels, i, j, x, y, area):
    # changes the color of a pixel to the color of the lightest pixel in the near area
    r = g = b = 0
    for row in range(i - area, i + area):
        for col in range(j - area, j + area):
            if 0 <= row < x and 0 <= col < y:
                if sum(pixels[row, col]) > r + g + b:
                    r, g, b = pixels[row, col]
    return r, g, b


def lightest_pixel_effect(im, area=3):
    im = im.convert("RGB")
    pixels_im = im.load()
    new_im = im.copy()
    pixels_new_im = new_im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            pixels_new_im[i, j] = lightest_pixel(pixels_im, i, j, x, y, area)
    return new_im


def black_and_white_effect(im):
    im = im.convert("L")
    im = im.convert("RGB")
    return im


def negative_effect(im):
    img_data = np.array(im)
    img_reversed_data = 255 - img_data
    img_reversed = Image.fromarray(img_reversed_data)
    return img_reversed


def two_colors(im):
    new_im = im.copy()
    pixels_new_im = new_im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels_new_im[i, j]
            pixels_new_im[i, j] = r, g, b
    return


filters_and_effects = (
    negative_effect,
    black_and_white_effect,
    blur,
    lightest_pixel_effect,
    stereo_effect,
    contour,
    detail,
    edge_enhance,
    emboss,
    find_edges,
    sharpen,
    smooth,
    unsharp_mask,
)
