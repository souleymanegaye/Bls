from math import log, sqrt, exp
from pandas import DataFrame
from scipy.stats import norm


class Blackscholes:
    def __init__(self,Spot, Strike, Taux, Vol, Time, Div=0, type = "CALL"):
        self.S = Spot
        self.K = Strike
        self.rf = Taux
        self.v = Vol
        self.T = Time
        self.D = Div
        if type == "CALL":
            self.z = 1
        elif type == "PUT":
            self.z = -1
        self.d1 = (log(self.S/self.K)+(self.rf + self.v**2*0.5)*self.T)/(self.v*sqrt(self.T))
        self.d2 = self.d1 - self.v*sqrt(self.T)

    def price(self, type = "Call"):
        return self.z*self.S*norm.cdf(self.d1*self.z)*exp(-self.T*self.D) - self.z*self.K*norm.cdf(self.d2*self.z)*exp(-self.T*self.rf)

    def delta(self):
        if self.z == 1:
            return norm.cdf(self.d1)
        elif self == -1:
            return norm.cdf(self.d1) - 1

    def gamma(self): #gamma du put et du call sont identique
        return exp(-self.D*self.T)*(norm.pdf(self.d1)/(self.S*self.v*self.T**0.5))

    def vega(self): #vega du call et du put sont identiques
        return self.S*exp(-self.D*self.T)*norm.pdf(self.d1)*self.T**0.5

    def theta(self,type = 'Call'):
        return ((self.v*self.S*exp(-self.D*self.T)*norm.pdf(self.d1)))/(2*self.T**0.5) -self.z* self.D*self.S*exp(-self.D*self.T)*norm.cdf(self.d1*self.z) + \
               self.z*self.rf*self.K*exp(-self.rf*self.T)*norm.pdf(self.d2*self.z)

    def rho(self):
        return self.z*self.T*exp(-self.rf*self.T)*norm.cdf(self.d2*self.z)

    def phi(self):
        return -self.z*self.S*exp(-self.D*self.T)*norm.cdf(self.d1*self.z)
    # def Allin(self):
    #     specs = DataFrame(columns=["Prix", "Delta", "Gamma", "Vega", "Theta", "Rho"])
    #     specs = self.price(),self.delta(), self.gamma(),self.vega(), self.theta(),self.rho()



