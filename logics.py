import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm
import matplotlib
from pylab import rcParams


matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

rcParams['figure.figsize'] = 18, 7

def movingAverage(Country):
    # MA = moving average
    # MSE = mean squared error
    MA3 = np.zeros(26)
    error3 = np.zeros(26)
    MA4 = np.zeros(26)
    error4 = np.zeros(26)
    MA5 = np.zeros(26)
    error5 = np.zeros(26)
    MA6 = np.zeros(26)
    error6 = np.zeros(26)

    country = Country.rename_axis("Country Name").values

    for i in range(3, 26):
        MA3[i] = (country[i - 3] + country[i - 2] + country[i - 1]) / 3
    for i in range(3, 26):
        error3[i] = (MA3[i] - country[i]) ** 2

    for i in range(4, 26):
        MA4[i] = (country[i - 4] + country[i - 3] + country[i - 2] + country[i - 1]) / 4
    for i in range(4, 26):
            error4[i] = (MA4[i] - country[i]) ** 2

    for i in range(5, 26):
        MA5[i] = (country[i - 5] + country[i - 4] + country[i - 3] + country[i - 2] + country[i - 1]) / 5
    for i in range(5, 26):
            error5[i] = (MA5[i] - country[i]) ** 2

    for i in range(6, 26):
        MA6[i] = (country[i - 6] + country[i - 5] + country[i - 4] + country[i - 3] + country[i - 2] + country[i - 1]) / 6
    for i in range(6, 26):
            error6[i] = (MA6[i] - country[i]) ** 2

    error3 = np.delete(error3, [0, 1, 2])
    error4 = np.delete(error4, [0, 1, 2, 3])
    error5 = np.delete(error5, [0, 1, 2, 3, 4])
    error6 = np.delete(error6, [0, 1, 2, 3, 4, 5])
    MSE3 = np.mean(error3)
    MSE4 = np.mean(error4)
    MSE5 = np.mean(error5)
    MSE6 = np.mean(error6)

    array = [MSE3, MSE4, MSE5, MSE6]
    MSEArray= np.around(array, decimals = 3)

    print("SMA called: ")
    print(MSEArray)

    # prog1, prog2 = Prognozed values. We choose the n value that returns the lowest MSE value

    if(MSE3 < MSE4 and MSE3 < MSE5 and MSE3 < MSE6):
        prog1 = (country[23] + country[24] + country[25]) / 3
        prog2 = (country[24] + country[25] + prog1) / 3
        prog3 = (country[25] + prog1 + prog2) / 3
        plotWithMovingAverage(Country, MA3, prog1, prog2, prog3)
    else:
        if(MSE4 < MSE3 and MSE4 < MSE5 and MSE4 < MSE6):
            prog1 = (country[22] + country[23] + country[24] + country[25]) / 4
            prog2 = (country[23] + country[24] + country[25] + prog1) / 4
            prog3 = (country[24] + country[25] + prog1 + prog2) / 4
            plotWithMovingAverage(Country, MA4, prog1, prog2, prog3)
        else:
            if(MSE5 < MSE3 and MSE5 < MSE4 and MSE5 < MSE6):
                prog1 = (country[21] + country[22] + country[23] + country[24] + country[25]) / 5
                prog2 = (country[22] + country[23] + country[24] + country[25] + prog1) / 5
                prog3 = (country[23] + country[24] + country[25] + prog1 + prog2) / 5
                plotWithMovingAverage(Country, MA5, prog1, prog2, prog3)
            else:
                if(MSE6 < MSE3 and MSE6 < MSE4 and MSE6 < MSE5):
                    prog1 = (country[20] + country[21] + country[22] + country[23] + country[24] + country[25]) / 6
                    prog2 = (country[21] + country[22] + country[23] + country[24] + country[25] + prog1) / 6
                    prog3 = (country[22] + country[23] + country[24] + country[25] + prog1 + prog2) / 6
                    plotWithMovingAverage(Country, MA6, prog1, prog2, prog3)

def plotWithMovingAverage(Country, ma, prog1, prog2, prog3):
    plt.plot(Country, label = 'Observed data')
    plt.xlabel("Years")
    plt.ylabel("%")
    t2 = np.arange(26, 29)
    plt.plot(t2, np.array([prog1,prog2, prog3]), 'o-', label = 'Prognozed data')
    plt.plot(ma,'*-', label = 'Averaged Data')

    maximum = max(Country.max(), prog1, prog2, prog3)
    if maximum + 2 < 100:
        plt.ylim(0, maximum + 2)
    else:
        plt.ylim(0, 100)
    print("Prognozed values: ")
    print(prog1,prog2,prog3)
    plt.legend()
    plt.show()

def weightedMovingAverage(Country):
    # MA = moving average
    # MSE = mean squared error
    MA3 = np.zeros(26)
    error3 = np.zeros(26)
    MA4 = np.zeros(26)
    error4 = np.zeros(26)
    MA5 = np.zeros(26)
    error5 = np.zeros(26)
    MA6 = np.zeros(26)
    error6 = np.zeros(26)

    country = Country.rename_axis("Country Name").values

    for i in range(3, 26):
        MA3[i] = (1 * country[i - 3] + 2 * country[i - 2] + 3 * country[i - 1]) / 6
    for i in range(3, 26):
        error3[i] = (MA3[i] - country[i]) ** 2

    for i in range(4, 26):
        MA4[i] = (1 * country[i - 4] + 2 * country[i - 3] + 3 * country[i - 2] + 4 * country[i - 1]) / 10
    for i in range(4, 26):
        error4[i] = (MA4[i] - country[i]) ** 2

    for i in range(5, 26):
        MA5[i] = (1 * country[i - 5] + 2 * country[i - 4] + 3 * country[i - 3] + 4 * country[i - 2] +
                  5 * country[i - 1]) / 15
    for i in range(5, 26):
        error5[i] = (MA5[i] - country[i]) ** 2

    for i in range(6, 26):
        MA6[i] = (1 * country[i - 6] + 2 * country[i - 5] + 3 * country[i - 4] + 4 * country[i - 3] +
                  5 * country[i - 2] + 6 * country[i - 1]) / 21
    for i in range(6, 26):
        error6[i] = (MA6[i] - country[i]) ** 2

    error3 = np.delete(error3,[0,1,2])
    error4 = np.delete(error4,[0,1,2,3])
    error5 = np.delete(error5, [0, 1, 2, 3, 4])
    error6 = np.delete(error6, [0, 1, 2, 3, 4, 5])
    MSE3 = np.mean(error3)
    MSE4 = np.mean(error4)
    MSE5 = np.mean(error5)
    MSE6 = np.mean(error6)

    array = [MSE3, MSE4, MSE5, MSE6]
    MSEArray = np.around(array, decimals=3)

    print("WMA called: ")
    print(MSEArray)

    # prog1, prog2, prog3 = Prognozed values. We choose the n value that returns the lowest MSE value

    if (MSE3 < MSE4 and MSE3 < MSE5 and MSE3 < MSE6):
        prog1 = (country[23] + country[24] + country[25]) / 3
        prog2 = (country[24] + country[25] + prog1) / 3
        prog3 = (country[25] + prog1 + prog2) / 3
        plotWithMovingAverage(Country, MA3, prog1, prog2, prog3)
    else:
        if (MSE4 < MSE3 and MSE4 < MSE5 and MSE4 < MSE6):
            prog1 = (country[22] + country[23] + country[24] + country[25]) / 4
            prog2 = (country[23] + country[24] + country[25] + prog1) / 4
            prog3 = (country[24] + country[25] + prog1 + prog2) / 4
            plotWithMovingAverage(Country, MA4,prog1, prog2, prog3)
        else:
            if (MSE5 < MSE3 and MSE5 < MSE4 and MSE5 < MSE6):
                prog1 = (country[21] + country[22] + country[23] + country[24] + country[25]) / 5
                prog2 = (country[22] + country[23] + country[24] + country[25] + prog1) / 5
                prog3 = (country[23] + country[24] + country[25] + prog1 + prog2) / 5
                plotWithMovingAverage(Country, MA5, prog1, prog2, prog3)
            else:
                if (MSE6 < MSE3 and MSE6 < MSE4 and MSE6 < MSE5):
                    prog1 = (country[20] + country[21] + country[22] + country[23] + country[24] + country[25]) / 6
                    prog2 = (country[21] + country[22] + country[23] + country[24] + country[25] + prog1) / 6
                    prog3 = (country[22] + country[23] + country[24] + country[25] + prog1 + prog2) / 6
                    plotWithMovingAverage(Country, MA6,prog1, prog2, prog3)


def simplePlot(Country):
    plt.plot(Country)
    if Country.max() + 2 < 100:
        plt.ylim(0, Country.max()+2)
    else:
        plt.ylim(0,100)
    plt.show()