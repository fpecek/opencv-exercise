"""
Module used for initializing plots to draw histograms.
"""
import numpy as np
import matplotlib.pyplot as plt
import const


def init_bar_plot():
    """
    Initialize histogram stacked bar plot.
    """
    _fig, axis = plt.subplots()
    axis.set_title('Stacked bar plot histogram (BGR)')
    axis.set_xlabel('Bin')
    axis.set_ylabel('Frequency (num of pixels)')
    axis.set_ylim(0, 700000)

    _n, _bins, bars_blue = axis.hist(0, const.BINS, rwidth=const.BAR_WIDTH,
                                     histtype='bar', stacked=True, color='blue', label='Blue')
    _n, _bins, bars_green = axis.hist(0, const.BINS, rwidth=const.BAR_WIDTH,
                                      histtype='bar', stacked=True, color='green', label='Green')
    _n, _bins, bars_red = axis.hist(0, const.BINS, rwidth=const.BAR_WIDTH,
                                    histtype='bar', stacked=True, color='red', label='Red')

    axis.legend()

    return bars_blue, bars_green, bars_red


def init_line_plot():
    """
    Initialize line plot histogram of all 3 channels
    """
    _fig, axis = plt.subplots()
    axis.set_title('Line histogram (BGR)')
    axis.set_xlabel('Bin')
    axis.set_ylabel('Frequency (num of pixels)')
    axis.set_xlim(0, const.MAX_PIXEL_VAL-1)
    axis.set_ylim(0, 54000)

    line_blue, = axis.plot(const.FULL_BINS, np.zeros((const.MAX_PIXEL_VAL,)), color='b', label='Blue')
    line_green, = axis.plot(const.FULL_BINS, np.zeros((const.MAX_PIXEL_VAL,)), color='g', label='Green')
    line_red, = axis.plot(const.FULL_BINS, np.zeros((const.MAX_PIXEL_VAL,)), color='r', label='Red')

    axis.legend()

    return line_blue, line_green, line_red


def turn_on_interactive_and_show():
    """
    Turn on interactive plotting and show plot.
    """
    plt.ion()
    plt.show()
