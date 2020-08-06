"""
Main module of opencv part 1 final exercise
"""
import argparse
import sys

import cv2 as cv
import numpy as np

import const
import logo_drawer_helper as drawer
import plotting


def init_logo_images():
    """
    Initialize default array images (black screen) for display opencv logos.
    """
    logo_images = np.empty((const.NUM_OF_BEANS, const.LOGO_HEIGHT, const.LOGO_WIDTH, 3), dtype=np.uint8)
    for idx in range(const.NUM_OF_BEANS):
        logo_images[idx, :, :] = np.zeros((const.LOGO_HEIGHT, const.LOGO_WIDTH, 3), np.uint8)

    return logo_images


# Get original area of one logo shape
original_area = drawer.calculate_default_shape_area()

# Initialize list with default logo images
logos = init_logo_images()

# Initialize Matplotlib plots and turn on interactive mode
line_blue, line_green, line_red = plotting.init_line_plot()
bars_blue, bars_green, bars_red = plotting.init_bar_plot()


def _calculate_interpolation(original_height, resized_height):
    """
    Calculate optimal interpolation for downscaling or upscaling video frame.
    """
    if original_height <= resized_height:
        return cv.INTER_CUBIC

    return cv.INTER_LINEAR


def resize_frame_keep_aspect_ratio(frame, resize_height):
    """
    Resize frame on given height but keep aspect ratio.
    Method return resized frame.
    """
    (height, width) = frame.shape[:2]
    resize_width = int((resize_height / height) * width)  # maintain aspect ratio
    interpolation = _calculate_interpolation(height, resize_height)
    frame_dimension = (resize_width, resize_height)

    return cv.resize(frame, frame_dimension, interpolation=interpolation)


def calculate_histogram_diffs(hist):
    """
    Method search for highest value in given histogram array and
    subtract other elements with max value to get difference.
    """
    max_value = np.max(hist)
    hist_diff = max_value - hist

    return hist_diff


def process_one_frame(frame, frame_height):
    """
    Method that process one frame of the video.
    :param frame: frame to process
    :param frame_height: frame height to resize
    """
    # 1.) Resize frame to height, if specified, or use default 360px
    resized_frame = resize_frame_keep_aspect_ratio(frame, frame_height)
    cv.imshow('video', resized_frame)

    # 2.) For each frame calculate and display histogram for all pixels and 3 color channels.
    hist_blue = cv.calcHist([resized_frame], [0], None, [const.MAX_PIXEL_VAL], const.HIST_RANGE)
    hist_green = cv.calcHist([resized_frame], [1], None, [const.MAX_PIXEL_VAL], const.HIST_RANGE)
    hist_red = cv.calcHist([resized_frame], [2], None, [const.MAX_PIXEL_VAL], const.HIST_RANGE)

    line_blue.set_ydata(hist_blue)
    line_green.set_ydata(hist_green)
    line_red.set_ydata(hist_red)

    # 3.) Calculate histogram with 5 bins and display values on stacked bar plot (for every channel)
    hist_blue = cv.calcHist([resized_frame], [0], None, const.HIST_SIZE, const.HIST_RANGE)  # 102 µs ± 151 ns per loop
    hist_green = cv.calcHist([resized_frame], [1], None, const.HIST_SIZE, const.HIST_RANGE)
    hist_red = cv.calcHist([resized_frame], [2], None, const.HIST_SIZE, const.HIST_RANGE)

    blue_diff = calculate_histogram_diffs(hist_blue)
    green_diff = calculate_histogram_diffs(hist_green)
    red_diff = calculate_histogram_diffs(hist_red)

    for idx in range(0, const.NUM_OF_BEANS):
        bars_blue[idx].set_height(hist_blue[idx])
        bars_green[idx].set_y(hist_blue[idx])
        bars_green[idx].set_height(hist_green[idx])
        bars_red[idx].set_y(hist_blue[idx] + hist_green[idx])
        bars_red[idx].set_height(hist_red[idx])

        diffs_sorted = sorted([(blue_diff[idx], 'B'), (green_diff[idx], 'G'), (red_diff[idx], 'R')], key=lambda a: a[0])
        res = [lis[0] for lis in diffs_sorted]
        col = [lis[1] for lis in diffs_sorted]

        logo_img = logos[idx]

        # For the biggest diff shape calculate new radius
        radius = drawer.calculate_radius(original_area, int(res[2]))
        drawer.draw_shape(logo_img, col[2], radius)  # Draw first shape with default angle (60)

        angle_green = drawer.calculate_angle(int(res[2]) - int(res[1]), radius) + 60
        drawer.draw_shape(logo_img, col[1], radius, angle_green)

        angle_blue = drawer.calculate_angle(int(res[0]), radius) + 60
        drawer.draw_shape(logo_img, col[0], radius, angle_blue)

    mask = np.arange(const.NUM_OF_BEANS)
    logos_horizontal_stack = np.hstack(logos[mask])
    cv.imshow('opencv_logo_draw', logos_horizontal_stack)

    # clear "canvas" for next iteration
    logos[:, :, :, :] = 0


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Path to video file (if empty, using camera)')
    parser.add_argument('-height', type=int, default=360,
                        help='Resize video to specified height in pixels (maintains aspect). Default value is 360px')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-img', help='Path to image')
    group.add_argument('-frame_no', type=int, help='Number of the frame')

    return parser.parse_args()


def main():
    """
    Application opens video file and calculate histograms frame by frame.
    Histogram is displayed as stacked bar chart.
    For every frame of the video calculate size and shape of 5 OpenCV
    logos with each logo's intensity adjusted for respective bin.
    """
    args = parse_arguments()

    # Configure VideoCapture class instance for using camera or file input.
    if not args.file:
        capture = cv.VideoCapture(0)
    else:
        capture = cv.VideoCapture(args.file)

    if not capture.isOpened():
        print("Cannot open camera or find file on given path")
        sys.exit(1)

    # Initialize opencv windows
    cv.namedWindow('video', cv.WINDOW_NORMAL)
    cv.namedWindow('opencv_logo_default', cv.WINDOW_NORMAL)
    cv.namedWindow('opencv_logo_draw', cv.WINDOW_NORMAL)

    # Draw default opencv logo
    opencv_logo = drawer.draw_opencv_logo()
    cv.imshow('opencv_logo_default', opencv_logo)

    plotting.turn_on_interactive_and_show()

    if args.frame_no:
        capture.set(1, args.frame_no)
        ret, frame = capture.read()
        process_one_frame(frame, args.height)
        cv.waitKey(0)
    elif args.img:
        frame = cv.imread(args.img)
        process_one_frame(frame, args.height)
        cv.waitKey(0)
    else:
        while True:
            (ret, frame) = capture.read()

            if not ret:
                break

            process_one_frame(frame, args.height)

            if cv.waitKey(1) & 0xFF == 27:  # exit with ESC
                break

    capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
