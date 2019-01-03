import numpy as np
from datetime import datetime
from math import sqrt
from scipy.stats import norm
from pandas_datareader import data
import pandas as pd

def moments(data):
    matrix = np.matrix(data)
    result = np.array()
    result[0] = np.mean(matrix, axis=0)
    result[1] = np.std(matrix,axis=0)
    result[3] = 0

class Stocks(object):
    # Teste
    def __init__(self):
        self._name = list
        self._from = str
        self._to = str
        self._prices = pd.DataFrame()

    def get_prices(self, name : list , beginDate , endDate ):
        # Dates should be in "26/05/2017" format
        self._name = name
        self._from = datetime.strptime(beginDate, "%d/%m/%Y")
        self._to = datetime.strptime(endDate, "%d/%m/%Y")
        self._prices = data.DataReader(self._name,"google",self._from, self._to)
        return self._prices.Close[self._name]


class VaR(Stocks):
    def __init__(self,_name : list, _from, _to):
        Stocks.__init__(self)
        self.eqt = _name
        self._from = _from
        self._to = _to
        self._hist_prices = self.get_prices(self.eqt,self._from, self._to)

    def get_historical(self, quantil, weights):
        matrix = self._hist_prices.pct_change().dropna()
        w = np.matrix(weights)
        wmoy = np.dot(matrix,w.transpose())
        return np.percentile(wmoy,quantil)

    def get_parametrics(self, seuil, weights):
        """ weights est un vecteur ligne
         """
        data = self._hist_prices.pct_change().dropna()
        rdts = np.matrix(data)
        moyportf = np.mean(rdts, axis = 0)
        covar = np.cov(rdts, rowvar=False)
        p = np.matrix(weights)
        wmoy = np.dot(moyportf,p.transpose())
        wsig = np.dot(p, covar)
        varportef = np.dot(wsig, p.transpose())
        var_parametric = norm.ppf(seuil)*sqrt(varportef) - wmoy
        return var_parametric

    def get_cornishfisher(self):
        """ To Do """










