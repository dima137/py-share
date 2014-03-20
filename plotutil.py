# utility plotting functions

import numpy as np
from matplotlib import pyplot


def positive(a):
    """
    return  a if a > 0
            0 if a <= 0
    """
    return (np.sign(a) + 1.) * a / 2.


def logPlotData(data, err, epsilon):
    """
    avoid negative values for the down errors on loglog plots
    useful for systematic uncertainty ranges
    INPUT:
        data - data
        err - errors
        epsilon - lower cutoff
    OUTPUT:
        makes data and errors small-positive for plotting in logplots
    """
    err += epsilon
    if err.ndim == 1:
        dnErr = 1. * err
        upErr = 1. * err
    else:
        dnErr = 1. * err[0]
        upErr = 1. * err[1]
    Min = positive(data - dnErr - epsilon) + epsilon
    Med = positive(data - 2 * epsilon) + 2 * epsilon
    Max = positive(data + upErr - 3 * epsilon) + 3 * epsilon
    return Med, [Med - Min, Max - Med]



def plotLimLog(xs, fs, ferrs, sigma=2.0, 
               headw=0.1, arrowl=0.35, epsilon=1.e-15, **kwargs):
    """ 
    Plot limit when value is less than sigma*error away from zero
    Input:
        xs - array, x-values
        fs - array, y-values
        ferrs - array, y-errors
        sigma - number, plot limit if  f[i] < sigma * ferrs[i]
            Default: 2.
        headw - number, the width of the arrow head relative to xs[i]
                        and the hight of the arrow head relative to ys[i]
            Default: 0.1
        arrowl - number, the length of the arrow line relative to fs[i]
            Default: 0.2
        epsilon - number, smallest number, should be outside of the y range
            Default: 1.e-15
        **kwargs - arguments for pyplot.errobar function
    Output:
        plots errorbars
        plots arrows
        returns errorbars object - the same as output of pyplot.errorbars function

    Comments:
        only works for log-log plots

    Created: Anna Franckowiak and Dmitry Malyshev, SLAC, 03/20/2014

    """

    fs = np.array(fs)
    ferrs = np.array(ferrs)
    xs = np.array(xs)
    upper_limits = fs + ferrs * sigma

    # find indices where the points are OK
    point_inds = (ferrs * sigma <= fs)
    upper_limits[point_inds] = epsilon

    # find the indices where the points have to be substituted with limits
    lim_inds = (ferrs * sigma > fs)
    fs[lim_inds] = epsilon
    ferrs[lim_inds] = epsilon

    # plot error bars
    errorbars = pyplot.errorbar(xs, fs, ferrs, ls='', **kwargs)
    color = errorbars[0].get_color()

    # plot arrows
    for i, ul in enumerate(upper_limits):
        # parameters of the arrow
        dx = 0
        dy = ul * arrowl
        #al = np.power(10,np.log10(ul[u])-arrowl)-ul[u]
        alh = dy * headw
        alw = xs[i] * headw

        # bar at the top of the arrow
        delta = 0.5 * headw
        xx = xs[i] * np.array([1 - delta, 1 + delta])
        yy = ul * np.ones(2)

        pyplot.arrow(xs[i], ul, dx, -dy, shape='full',
                     length_includes_head=True, head_width=alw, head_length=alh,
                     edgecolor=color, facecolor=color)
        pyplot.plot(xx, yy, c=color)
    
    return errorbars

if __name__ == '__main__':
    xs = 10.**np.arange(0., 3., 0.2)
    fs = xs**1.3
    ferrs = xs
    ferrs = ferrs[::-1]

    pyplot.figure()

    plotLimLog(xs, fs, ferrs, headw=0.1, arrowl=0.35, marker='s', color='r')
    pyplot.xscale('log')
    pyplot.yscale('log')
    pyplot.ylim(10, 10**4.)
    pyplot.show()
    
