from scipy.stats import beta, binom
import scipy.stats as stat
from scipy.misc import comb
from util import *
from numpy import *
from node import *

from util2 import *

from phySCNAClonal import constants

class StripeNode(Node):

    initMean = 0.5
    minConc = 0.01
    maxConc = 0.1

    def __init__(self, parent=None, tssb=None, conc=0.1):
        super(alleles, self).__init__(parent=parent, tssb=tssb)

        if tssb is not None:
            ntps = len(tssb.data[0].a)

        # pi is a first-class citizen
        self.pi = 0.0
        self.param = 0.0
        self.param1 = 0.0
        self.pi1 = 0.0  # used in MH	to store old state

        self.path = None  # set of nodes from root to this node
        self.ht = 0.0

        if parent is None:
            self._conc = conc
            self.pi = 1.0
            self.param = 1.0

        else:
            self.pi = rand(1)*parent.pi
            parent.pi = parent.pi - self.pi
            self.param = self.pi

    def conc(self):
        if self.parent() is None:
            return self._conc
        else:
            return self.parent().conc()

    def kill(self):
        if self._parent is not None:
            self._parent._children.remove(self)
        self._parent.pi = self._parent.pi + self.pi
        self._parent = None
        self._children = None

    def logprob(self, x):
        return x[0]._log_likelihood(self.param)

    def logprob_restricted(self, x):
        lowerNode, upperNode = self.__find_neighbor_datum_n(x)

        lFlag = True
        uFlag = True
        if lowerNode is not None:
            lFlag = self.__is_good_gap(lowerNode, x, "lower")
        else:
            lFlag = True

        if upperNode is not None:
            uFlag = self.__is_good_gap(lowerNode, x, "upper")
        else:
            uFlag = True
        if lFlag and uFlag:
            return self.logprob(x)
        else:
            return -float('Inf')

    def complete_logprob(self):
        return sum([self.logprob([data]) for data in self.get_data()])

    def __find_neighbor_datum_n(self, x):
        datums = self.get_data()
        if x not in datums:
            datums.append(x)

        datumsSortedL = sorted(datums,
            key=lambda item: 1.0*item.tReadNum/item.nReadNum)

        idx = datumsSortedL.index(x)
        if 0 == idx:
            return (None, datumsSortedL[1])
        elif len(datumsSortedL) - 1 == idx:
            return (datumsSortedL[idx-1], None)
        else:
            return (datumsSortedL[idx-1], datumsSortedL[idx+1])

    def __is_good_gap(self, lowerNode, upperNode, position):
        varpi = constants.VARPI

        rdrLower = 1.0*lowerNode.tReadNum/lowerNode.nReadNum
        rdrUpper = 1.0*upperNode.tReadNum/upperNode.nReadNum
        L = np.exp(rdrUpper - rdrLower)

        if "lower" == position:
            cn = lowerNode.copyNumber
        elif "upper" == position:
            cn = upperNode.copyNumber - 1

        if cn < 0:
            return False
        else:
            return L >= varpi * (1.0 + (self.param /
                    (cn * self.param + 2 * (1 - self.param))))
