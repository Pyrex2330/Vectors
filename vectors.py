import matplotlib.pyplot as plt
from math import radians, sin, cos
import numpy as np


def draw_vectors_bot(angles: dict):
    colors, scales = ['r', 'g', 'b'], [0.18, 0.14, 0.1]
    fig, ax = plt.subplots()

    angles_sorted = sorted(angles, key=lambda x: x, reverse=True)
    for voltage, color, scale in zip(angles_sorted, colors, scales):
        angle_a, angle_b, angle_c = angles[voltage]

        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.grid()
        plt.gca().yaxis.set_ticks_position('right')
        x_ticks = [0]
        x_label = ['-90']
        plt.xticks(ticks=x_ticks, labels=x_label)
        y_ticks = [0]
        y_label = ['0']
        plt.yticks(ticks=y_ticks, labels=y_label)

        aligment_a = 'right' if angle_a in range(150, 290) else 'left'
        aligment_b = 'right' if angle_b in range(150, 290) else 'left'
        aligment_c = 'right' if angle_c in range(150, 290) else 'left'

        plt.quiver(0, 0, cos(radians(angle_a)), sin(radians(angle_a)), scale_units='xy', angles='xy', scale=scale,
                   color=color)
        plt.text(cos(radians(angle_a)) / scale, sin(radians(angle_a)) / scale, s=f'Ia{voltage}', ha=aligment_a)
        plt.quiver(0, 0, cos(radians(angle_b)), sin(radians(angle_b)), scale_units='xy', angles='xy', scale=scale,
                   color=color)
        plt.text(cos(radians(angle_b)) / scale, sin(radians(angle_b)) / scale, s=f'Ib{voltage}', ha=aligment_b)
        plt.quiver(0, 0, cos(radians(angle_c)), sin(radians(angle_c)), scale_units='xy', angles='xy', scale=scale,
                   color=color)
        plt.text(cos(radians(angle_c)) / scale, sin(radians(angle_c)) / scale, s=f'Ic{voltage}', ha=aligment_c)

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close()

    return image


def rotation_check(angle_a, angle_b, angle_c):
    flag = False
    quadrant_1 = range(0, 90)
    quadrant_2 = range(90, 181)
    quadrant_3 = range(-180, -90)
    quadrant_4 = range(-90, 0)

    if angle_a in quadrant_1:
        if angle_b in quadrant_3 and angle_c in quadrant_2:
            flag = True
        elif angle_b in quadrant_4 and angle_c in quadrant_2:
            flag = True
        elif angle_b in quadrant_4 and angle_c in quadrant_3:
            flag = True

    elif angle_a in quadrant_2:
        if angle_b in quadrant_4 and angle_c in quadrant_3:
            flag = True
        elif angle_b in quadrant_1 and angle_c in quadrant_3:
            flag = True
        elif angle_b in quadrant_1 and angle_c in quadrant_4:
            flag = True

    elif angle_a in quadrant_3:
        if angle_b in quadrant_1 and angle_c in quadrant_4:
            flag = True
        elif angle_b in quadrant_2 and angle_c in quadrant_4:
            flag = True
        elif angle_b in quadrant_2 and angle_c in quadrant_1:
            flag = True

    elif angle_a in quadrant_4:
        if angle_b in quadrant_2 and angle_c in quadrant_4:
            flag = True
        elif angle_b in quadrant_3 and angle_c in quadrant_4:
            flag = True
        elif angle_b in quadrant_3 and angle_c in quadrant_2:
            flag = True

    return flag
