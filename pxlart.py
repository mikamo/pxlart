from PIL import Image
import numpy as np
import colorgram
from copy import copy


def majority_voting(pxl_list):
    return max(set(pxl_list), key=pxl_list.count)


def get_closest_color(pixel, color_palette):
    closest_color_of_pxl = None
    cost_init = 195075  # squared e. dist. between black & white
    pixel = np.array(pixel)
    for color in color_palette:
        color = np.array(color)
        cost = np.sum((color - pixel) ** 2)
        if cost < cost_init:
            cost_init = cost
            closest_color_of_pxl = color
    return closest_color_of_pxl


class PxlArt:

    def __init__(self, image_input_path, image_output_path):
        self.image_input_path = image_input_path
        self.image_output_path = image_output_path

        self.image = Image.open(image_input_path)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.image_array = np.asarray(self.image)

        self.color_set_rgb = None

    def __update(self, image):
        if image is not None:
            self.image = image
            self.width = image.size[0]
            self.height = image.size[1]
            self.image_array = np.asarray(image)

    def resize(self, scaling):
        scaling = int(scaling)
        image = None
        if scaling >= 1:
            image = self.image.resize(
                (self.image.width * scaling, self.image.height * scaling),
                Image.NEAREST
            )

        elif scaling <= -1:
            image = self.image.resize(
                (
                    self.image.width // np.abs(scaling),
                    self.image.height // np.abs(scaling)
                ),
                Image.NEAREST
            )

        self.__update(image)

        print("image resized")

    def extract_color_palette(self, palette_size):
        colors = colorgram.extract(self.image_input_path, palette_size)
        color_set_rgb = [
            (color.rgb[0], color.rgb[1], color.rgb[2]) for color in colors
        ]
        self.color_set_rgb = color_set_rgb
        print("color palette extracted: ", self.color_set_rgb)

    def assign_colors(self):
        if self.color_set_rgb is None:
            print("Set up color palette before assigning colors!")
        else:
            new_image_array = np.zeros((self.height, self.width, 3))
            for y in range(0, self.height):
                for x in range(0, self.width):
                    closest_color_of_pxl = \
                        get_closest_color(self.image_array[y, x],
                                        self.color_set_rgb)
                    new_image_array[y, x] = closest_color_of_pxl
            image = Image.fromarray(np.uint8(new_image_array)).convert('RGB')
            self.__update(image)
            print("colors from palette assigned to image pixels")

    def combine_pxls(self, iteration):
        new_image_array = np.zeros((self.height - 1, self.width - 1, 3))
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                neighbors = self.image_array[y-1:y+2, x-1:x+2, :].reshape(9, 3)
                neighbors = [tuple(x.astype('int')) for x in neighbors]
                neighbors.pop(4)  # pop center pixel of the block
                majority_neighbor = majority_voting(neighbors)
                new_image_array[y, x] = majority_neighbor

        new_image_array = np.rot90(new_image_array)
        image = Image.fromarray(np.uint8(new_image_array)).convert('RGB')
        self.__update(image)

        print(iteration - 1, " iterations left")

        if iteration > 1:
            self.combine_pxls(iteration - 1)
        else:
            print("pixel combining done...")

    def rotate(self, iteration):
        image_array = self.image_array
        for i in range(iteration):
            image_array = np.rot90(image_array)
        image = Image.fromarray(np.uint8(image_array)).convert('RGB')
        self.__update(image)
        print("image rotated")

    def save_image(self):
        self.image.save(self.image_output_path)
        print("image saved to: ", self.image_output_path)