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



def plotLimLog(e, f, fe, sigma=2.0, c=None, headw=0.2, arrowl=0.3, **kwargs):
    """ 
    Usage: plot limits when value is less than sigma*error away from zero
    Comment: only works for log-log plots
    Input: e: array of x-values
           f: array of y-values
           fe: array of y-errors
           sigma: plot limit if  f<sigma*fe
           headw, arrowl: use to control size of errors
    Created: Anna Franckowiak and Dmitry Malyshev, SLAC, 03/20/2014

    """

    epsilon = np.ones_like(f)*1e-10
    f = np.array(f)
    fe = np.array(fe)
    e = np.array(e)
    ul = f+fe*sigma
    ul[fe*sigma<=f] = epsilon[fe*sigma<=f]

    f[fe*sigma>f] = epsilon[fe*sigma>f]
    fe[fe*sigma>f] = epsilon[fe*sigma>f]

    if c is None:
        eerb = pyplot.errorbar(e, f, fe, ls='', **kwargs)
    else:
        eerb = pyplot.errorbar(e, f, fe, ls='', c=c, **kwargs)

    c = eerb[0].get_color()

    for u in range(len(ul)):
        al = np.power(10,np.log10(ul[u])-arrowl)-ul[u]
        alh = -al*headw
        alw = e[u]*headw
        delta = 0.5 * headw
        x = e[u] * np.array([1 - delta, 1 + delta])
        y = ul[u] * np.ones(2)

        pyplot.arrow(e[u],ul[u],0,al,shape='full', length_includes_head=True, head_width=alw, head_length=alh,edgecolor=c,facecolor=c)
        pyplot.plot(x,y,c=c)
    
    return eerb
