"""
module for drawing OpenCV logo and shapes
"""
import math
import numpy as np
import cv2
import const


def _calculate_area(radius_outer):
    """
    Calculates area of annulus shape
    :param radius_outer: outer radius of the annulus
    :return: annulus area
    """
    r_inner = round(radius_outer * const.INNER_CIRCLE_ASPECT)
    return round(math.pi * (radius_outer * radius_outer - r_inner * r_inner))


def _calculate_area_sector(radius_outer, ang):
    """
    Calculates area of the annulus sector shape
    :param radius_outer: outer radius of the annulus
    :param ang: angle of the annulus sector
    :return: annulus sector area
    """
    r_inner = round(radius_outer * const.INNER_CIRCLE_ASPECT)
    return (ang / 360) * math.pi * (radius_outer * radius_outer - r_inner * r_inner)


def _calculate_distance(radius_outer):
    """
    Calculate distance between shapes.
    :param radius_outer: outer radius of the annulus
    :return: return new distance
    """
    change_in_radius = (radius_outer - const.DEFAULT_OUTER_RADIUS) / const.DEFAULT_OUTER_RADIUS
    change_in_distance = (const.DEFAULT_DISTANCE * change_in_radius)

    return round(change_in_distance + const.DEFAULT_DISTANCE)


def calculate_radius(old_area, new_area):
    """
    Calculate radius of the new shape by maintaining aspect ratio.
    For example, if area is increased by 50%, then radius is also increased by 50%.
    :param old_area: area of default shape
    :param new_area: area of the shape that is changed
    :return: calculated radius
    """
    change_in_area = new_area / old_area
    change_in_radius = (const.DEFAULT_OUTER_RADIUS * change_in_area)

    return round(change_in_radius + const.DEFAULT_OUTER_RADIUS)


def calculate_angle(area, radius):
    """
    Calculate angle of OpenCV shape
    :param area: area of shape
    :param radius: outer radius of shape
    :return: angel of the shape
    """
    return (area / ((radius * radius) * math.pi)) * 360


def calculate_default_shape_area():
    """
    Calculates area of one shape in default OpenCV logo
    :return:  area of one shape in default logo
    """
    area = _calculate_area(const.DEFAULT_OUTER_RADIUS)
    sector_area = _calculate_area_sector(const.DEFAULT_OUTER_RADIUS, const.DEFAULT_ANGLE)

    return round(area - sector_area)


def draw_opencv_logo(radius_outer=const.DEFAULT_OUTER_RADIUS, ang=const.DEFAULT_ANGLE):
    """
    Draws default OpenCV logo
    """
    distance = const.DEFAULT_DISTANCE
    height = int(distance / 2 * math.sqrt(3))

    center_red = const.CENTER_OF_RED
    center_green = (center_red[0] - distance//2, center_red[1] + height)
    center_blue = (center_red[0] + distance//2, center_red[1] + height)

    img = np.zeros((const.LOGO_HEIGHT, const.LOGO_WIDTH, 3), np.uint8)

    draw_s(img, center_red, radius_outer, const.RED, ang, ang)
    draw_s(img, center_green, radius_outer, const.GREEN, ang, 360-ang)
    draw_s(img, center_blue, radius_outer, const.BLUE, ang, 360-2*ang)

    return img


def draw_s(img, center, radius_outer, color, ang, start_ang):
    """
    helper for drawing one opencv shape
    :param img:
    :param center: center of shape
    :param radius_outer: outer radius of the annulus
    :param color: color of the shape
    :param ang: angle of sector
    :param start_ang: start point of angle
    """
    radius_inner = round(radius_outer * const.INNER_CIRCLE_ASPECT)

    cv2.circle(img, center, radius_outer, color, const.FULL_SHAPE)
    cv2.circle(img, center, radius_inner, const.BLACK, const.FULL_SHAPE)
    cv2.ellipse(img, center, (radius_outer, radius_outer), start_ang, 0, ang, const.BLACK, const.FULL_SHAPE)


def draw_shape(img, color, radius_outer=const.DEFAULT_OUTER_RADIUS, ang=const.DEFAULT_ANGLE):
    """
    Draw one OpenCV circle/shape
    """
    radius_inner = round(radius_outer * const.INNER_CIRCLE_ASPECT)
    distance = _calculate_distance(radius_outer)
    height = int(distance / 2 * math.sqrt(3))

    center = const.CENTER_OF_RED
    if color == 'R':
        color = const.RED
        start_ang = ang
    elif color == 'G':
        center = (center[0] - distance//2, center[1] + height)
        color = const.GREEN
        start_ang = 360 - ang
    else:
        center = (center[0] + distance//2, center[1] + height)
        color = const.BLUE
        start_ang = 360 - (2 * ang)

    cv2.circle(img, center, radius_outer, color, const.FULL_SHAPE)
    cv2.circle(img, center, radius_inner, const.BLACK, const.FULL_SHAPE)
    cv2.ellipse(img, center, (radius_outer, radius_outer), start_ang, 0, ang, const.BLACK, const.FULL_SHAPE)

    return img
