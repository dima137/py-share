import numpy as np


def positive(a):
    """
    return  a if a > 0
            0 if a <= 0
    """
    return (np.sign(a) + 1.) * a / 2.


def logPlotData(data, err, epsilon):
    """
    avoid negative values for the down errors on loglog plots
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

