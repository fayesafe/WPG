#!/usr/bin/env python3
"""Script to create a random wallpaper based on a single input color
Example: wpirify.py 1920 1080 -c "#4B9A62" -e "#CAEFC7"
"""

import argparse
from math import gcd
from random import choice, randint
import string
import numpy as np
from PIL import Image


def main():
    """Main function
    """
    args = parse_args()
    block_size = get_block_size(
        args.width, args.height, args.block_size)
    end = '#FFFFFF'
    if args.end_color:
        end = args.end_color
    grid = create_grid(args.width, args.height, block_size, args.color, end)
    result_grid = create_result_grid(args.width, args.height, block_size, grid)
    image = Image.fromarray(result_grid, 'RGB')

    file_name = ''.join(choice(
        string.ascii_letters + string.digits) for _ in range(10)) + '.png'
    image.save(file_name)
    print(file_name)


def get_block_size(width, height, block_size):
    """Calculation of the desired block size for the wallpaper
    """
    result_block_size = 1
    if block_size:
        if gcd(width, height) < block_size:
            result_block_size = gcd(width, height)
        else:
            common_divs = [
                x for x in range(1, min(width, height)+1)
                if width % x == 0 and height % x == 0]
            result_block_size = min(
                common_divs, key=lambda x: abs(x-block_size))
    else:
        result_block_size = gcd(width, height)

    return result_block_size


def create_grid(width, height, block_size, color, end):
    """Creation of the wallpaper grid
    """
    grid = []
    for _ in range(0, width//block_size):
        col = []
        for _ in range(0, height//block_size):
            col.append(hex_to_rgb("#FFFFFF"))
        grid.append(col)
    rand_indecis = [randint(0, len(grid)-1), randint(0, len(grid[0])-1)]
    grid[rand_indecis[0]][rand_indecis[1]] = hex_to_rgb(color)
    gradient_h = lin_gradient(color, end, height//block_size)

    # Create upper half of the grid
    i = rand_indecis[1]
    j = 0
    while i >= 0:
        grid[rand_indecis[0]][i] = gradient_h[j]
        w_i = rand_indecis[0] - 1
        w_j = 1
        gradient_w_tmp = lin_gradient(
            rgb_to_hex(gradient_h[j]), end, width//block_size)
        while w_i >= 0:
            grid[w_i][i] = gradient_w_tmp[w_j]
            w_i -= 1
            w_j += 1
        w_i = rand_indecis[0] + 1
        w_j = 1
        while w_i < len(grid):
            grid[w_i][i] = gradient_w_tmp[w_j]
            w_i += 1
            w_j += 1
        i -= 1
        j += 1

    # Create lower half of the grid
    i = rand_indecis[1]
    j = 0
    while i < len(grid[0]):
        grid[rand_indecis[0]][i] = gradient_h[j]
        w_i = rand_indecis[0] - 1
        w_j = 1
        gradient_w_tmp = lin_gradient(
            rgb_to_hex(gradient_h[j]), end, width//block_size)
        while w_i >= 0:
            grid[w_i][i] = gradient_w_tmp[w_j]
            w_i -= 1
            w_j += 1
        w_i = rand_indecis[0] + 1
        w_j = 1
        while w_i < len(grid):
            grid[w_i][i] = gradient_w_tmp[w_j]
            w_i += 1
            w_j += 1
        i += 1
        j += 1

    return grid


def create_result_grid(width, height, block_size, grid):
    """Creation of the final result grid for PIL using numpy
    """
    result_grid = np.zeros((height, width, 3), 'uint8')
    for i in range(0, height):
        for j in range(0, width):
            for k in range(0, 3):
                result_grid[i, j, k] = grid[j//block_size][i//block_size][k]
    return result_grid


def lin_gradient(start, finish="#FFFFFF", times=30):
    """Calculation of the linear gradient
    """
    start = hex_to_rgb(start)
    finish = hex_to_rgb(finish)
    rgb_list = [start]
    times *= 2
    for i in range(1, times):
        curr_vector = [
            int(start[j] + (float(i)/(times-1))*(finish[j]-start[j]))
            for j in range(3)
        ]
        rgb_list.append(curr_vector)
    return rgb_list


def rgb_to_hex(rgb):
    """ [255,255,255] -> "#FFFFFF" """
    rgb = [int(x) for x in rgb]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                        "{0:x}".format(v) for v in rgb])


def hex_to_rgb(color):
    """ "#FFFFFF" -> [255,255,255] """
    return [int(color[i:i+2], 16) for i in range(1, 6, 2)]


def parse_args():
    """Parsing the command line arguments
    """
    argument_parser = argparse.ArgumentParser(
        description='Generation of Wallpapers based on fancy Color Gradients')
    argument_parser.add_argument(
        'width',
        type=int,
        help='Width of your Wallpaper'
    )
    argument_parser.add_argument(
        'height',
        type=int,
        help='Width of your Wallpaper'
    )
    argument_parser.add_argument(
        '-c',
        '--color',
        type=str,
        dest='color',
        help='Basic color to start with',
        required=True
    )
    argument_parser.add_argument(
        '-e',
        '--end-color',
        type=str,
        dest='end_color',
        help='Color to end with',
        required=False
    )
    argument_parser.add_argument(
        '-b',
        '--block-size',
        type=int,
        dest='block_size',
        help='Size of desired Block Size (Square)',
        required=False
    )
    return argument_parser.parse_args()


if __name__ == '__main__':
    main()
