import numpy as np


class ContingencyTable:
    def __init__(self, a, b, c, d):
        """Initializes a contingency table of the following form:
                       Event
                       Yes No
        Forecast    Yes  a  b
                    No   c  d
        """
        self.table = np.array([[a, b], [c, d]], dtype=float)
        self.N = self.table.sum()

    def update(self, a, b, c, d):
        self.table.ravel()[:] = [a, b, c, d]
        self.N = self.table.sum()

    def pod(self):
        """Returns Probability of Detection (POD) or Hit Rate.
           Formula:  a/(a+c)"""
        return self.table[0, 0] / (self.table[0, 0] + self.table[1, 0])

    def foh(self):
        """Returns Frequency of Hits (FOH) or Success Ratio.
           Formula:  a/(a+b)"""
        return self.table[0, 0] / (self.table[0, 0] + self.table[0, 1])

    def far(self):
        """Returns False Alarm Ratio (FAR).
           Formula:  b/(a+b)"""
        return self.table[0, 1] / (self.table[0, 0] + self.table[0, 1])

    def pofd(self):
        """Returns Probability of False Detection (POFD).
           b/(b+d)"""
        return self.table[0, 1] / (self.table[0, 1] + self.table[1, 1])

    def fom(self):
        """Returns Frequency of Misses (FOM).
           Formula:  c/(a+c)."""
        return self.table[1, 0] / (self.table[0, 0] + self.table[1, 0])

    def dfr(self):
        """Returns Detection Failure Ratio (DFR).
           Formula:  c/(c+d)"""
        return self.table[1, 0] / (self.table[1, 0] + self.table[1, 1])

    def pon(self):
        """Returns Probability of Null (PON).
           Formula:  d/(b+d)"""
        return self.table[1, 1] / (self.table[0, 1] + self.table[1, 1])

    def focn(self):
        """Returns Frequency of Correct Null (FOCN).
           Formula:  d/(c+d)"""
        return self.table[1, 1] / (self.table[1, 0] + self.table[1, 1])

    def bias(self):
        """Returns Frequency Bias.  Formula:  (a+b)/(a+c)"""
        return (self.table[0, 0] + self.table[0, 1]) / (self.table[0, 0] + self.table[1, 0])

    def accuracy(self):
        """Finley's measure, fraction correct, accuracy (a+d)/N"""
        return (self.table[0, 0] + self.table[1, 1]) / self.N

    def csi(self):
        """Gilbert's Score or Threat Score or Critical Success Index a/(a+b+c)"""
        return self.table[0, 0] / (self.table[0, 0] + self.table[0, 1] + self.table[1, 0])

    def ets(self):
        """Equitable Threat Score, Gilbert Skill Score, v, (a - R)/(a + b + c - R), R=(a+b)(a+c)/N"""
        r = (self.table[0, 0] + self.table[0, 1]) * (self.table[0, 0] + self.table[1, 0]) / self.N
        return (self.table[0, 0] - r) / (self.table[0, 0] + self.table[0, 1] + self.table[1, 0] - r)

    def hss(self):
        """Doolittle (Heidke) Skill Score.  2(ad-bc)/((a+b)(b+d) + (a+c)(c+d))"""
        return 2 * (self.table[0, 0] * self.table[1, 1] - self.table[0, 1] * self.table[1, 0]) / (
            (self.table[0, 0] + self.table[0, 1]) * (self.table[0, 1] + self.table[1, 1]) +
            (self.table[0, 0] + self.table[1, 0]) * (self.table[1, 0] + self.table[1, 1]))

    def pss(self):
        """Peirce (Hansen-Kuipers, True) Skill Score (ad - bc)/((a+c)(b+d))"""
        return (self.table[0, 0] * self.table[1, 1] - self.table[0, 1] * self.table[1, 0]) / \
               ((self.table[0, 0] + self.table[1, 0]) * (self.table[0, 1] + self.table[1, 1]))

    def css(self):
        """Clayton Skill Score (ad - bc)/((a+b)(c+d))"""
        return (self.table[0, 0] * self.table[1, 1] - self.table[0, 1] * self.table[1, 0]) / \
               ((self.table[0, 0] + self.table[0, 1]) * (self.table[1, 0] + self.table[1, 1]))

    def __str__(self):
        table_string = '\tEvent\n\tYes\tNo\nYes\t%d\t%d\nNo\t%d\t%d\n' % (
            self.table[0, 0], self.table[0, 1], self.table[1, 0], self.table[1, 1])
        return table_string


if __name__ == "__main__":
    table = ContingencyTable(1, 2, 3, 4)
    print table
    print getattr(table, "pss")()
