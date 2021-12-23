import numpy as np
import drawSvg as draw
from numpy.random.mtrand import random


def draw_roulette(billes=[], numbers=None, americaine=False, margin = 0.2, handles=5, phase=0, h_phase=30, random_seed=None):
    board_margin = 0.025
    inner_rays_factor = 2.5
    l_handle, w_handle = 0.2, 0.05
    sw_ring = 0.004

    k_border = 'ivory'
    k_outside = '#B68969'
    k_red = '#DD4444'
    k_black = '#222222'
    k_green = '#119933'

    if random_seed is not None:
        np.random.seed(random_seed)
        
    def convert_numbers(n_max, n_zeros):
        n = np.arange(1, n_max + 1)
        np.random.shuffle(n)
        n = list(n)
        if n_zeros == 2:
            i1 = n_max // 2
            return [0] + n[:i1] + [-1] + n[i1:]
        elif n_zeros == 3:
            i1, i2 = n_max // 3, 2 * n_max // 3
            return [0] + n[:i1] + [-1] + n[i1:i2] + [-2] + n[i2:]
        return [0] + n

    if numbers is None:
        if americaine:
            # Americaine
            numbers = [0, 2, 14, 35, 23, 4, 16, 33, 21, 6, 18, 31, 19, 8, 12, 29, 25, 10, 27, -1, 1, 13, 36, 24, 3, 15, 34, 22, 5, 17, 32, 20, 7, 11, 30, 26, 9, 28]
        else:
            # Française
            numbers = [0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32]
    elif type(numbers) is tuple:
        if len(numbers) > 1:
            n_zeros = max(1, min(3, numbers[1]))
        else:
            n_zeros = 1 + americaine
        n_max = max(n_zeros, n_zeros * (min(36, numbers[0]) // n_zeros))
        numbers = convert_numbers(n_max, n_zeros)
    elif type(numbers) is int:
        n_zeros = 1 + americaine
        n_max = max(2, n_zeros * (min(36, numbers) // n_zeros))
        numbers = convert_numbers(n_max, n_zeros)
        
    def written_number(n):
        if n > 0:
            return str(n)[::-1]
        else:
            return (1 - n) * '0'

    r_out, r_mid, r_in = 1, 0.85, 0.7
    nb_width = 360 / len(numbers)
    d = draw.Drawing(2 * (1 + board_margin + margin), 2 * (1 + board_margin + margin), origin='center', displayInline=False)
    # Board
    d.append(draw.Circle(0, 0, (1 + board_margin)* r_out, fill=k_outside))
    # Draw multiple circular arcs
    angle = 90 + phase
    red = True
    ps = []
    for n in numbers:
        if n > 0:
            if red:
                stroke = k_red
            else:
                stroke = k_black
        else:
            stroke = k_green
        d.append(draw.Arc(0, 0, (r_out + r_in) / 2, angle - 1.001 * nb_width / 2, angle + 1.001 * nb_width / 2, stroke=stroke, stroke_width=r_out - r_in, fill_opacity=0))
        ps.append(draw.Arc(0, 0, (r_out + r_in) / 2, 180 + angle - nb_width / 2, 180 + angle + nb_width / 2, fill_opacity=0))
        angle += nb_width
        red ^= True

    for n in numbers:
        path = ps.pop(0)
        d.append(draw.Line(r_in * np.cos((angle - nb_width / 2) / 180 * np.pi), r_in * np.sin((angle - nb_width / 2) / 180 * np.pi), r_mid * np.cos((angle - nb_width / 2) / 180 * np.pi), r_mid * np.sin((angle - nb_width / 2) / 180 * np.pi), stroke=k_border, stroke_width=3 * sw_ring))
        d.append(draw.Text(written_number(n), 0.09, fill=k_border, path=path, center=True, lineOffset=-19.75))
        b = billes.count(n)
        if b:
            d.append(draw.Circle((r_mid + r_in) / 2 * np.cos(angle / 180 * np.pi), (r_mid + r_in) / 2 * np.sin(angle / 180 * np.pi), 0.035, fill=k_border, stroke=k_border, stroke_width=2 * sw_ring))
            if b > 1:
                d.append(draw.Text(written_number(b) + 'x', 0.05, fill=k_black, path=path, center=True, lineOffset=-32.625))
        angle += nb_width

    for n in range(int(len(numbers) // inner_rays_factor + 2)):
        d.append(draw.Line(0, 0, r_in * np.cos(angle / 180 * np.pi), r_in * np.sin(angle / 180 * np.pi), stroke=k_border, stroke_width=2 * sw_ring))
        angle += 360 / (len(numbers) // inner_rays_factor + 2)
            
    # Outer ring
    d.append(draw.Circle(0, 0, r_out - sw_ring / 3, stroke=k_border, stroke_width=2 * sw_ring, fill_opacity=0))
    # Middle ring
    d.append(draw.Circle(0, 0, r_mid - sw_ring / 2, stroke=k_border, stroke_width=5 * sw_ring, fill_opacity=0))
    # Inner ring
    d.append(draw.Circle(0, 0, r_in + sw_ring / 3, stroke=k_border, stroke_width=5 * sw_ring, fill_opacity=0))

    # Lower Handle
    d.append(draw.Circle(0, 0, 0.075 * r_out, fill=k_border))

    pos = np.array([[0, l_handle, l_handle, 0], [-w_handle / 3, -w_handle / 2, w_handle / 2, w_handle / 3]])
    rot = lambda theta: np.array([[np.cos(theta / 180 * np.pi), -np.sin(theta / 180 * np.pi)], [np.sin(theta / 180 * np.pi), np.cos(theta / 180 * np.pi)]])
    theta = 90 + phase + h_phase
    for h in range(handles):
        theta += 360 / handles
        rp = rot(theta) @ pos
        d.append(draw.Lines(rp[0, 0], rp[1, 0], rp[0, 1], rp[1, 1], rp[0, 2], rp[1, 2], rp[0, 3], rp[1, 3], close=True, fill=k_border, stroke=k_outside, stroke_width=sw_ring))

    # Upper Handle
    d.append(draw.Circle(0, 0, 0.05 * r_out, fill=k_border, stroke=k_outside, stroke_width=2 * sw_ring))

    return d
