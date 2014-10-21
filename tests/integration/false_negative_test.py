# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

from nab.scorer import Scorer, scoreCorpus
import pandas

import unittest2 as unittest
import datetime



def generateTimestamps(start, increment, length):
  timestamps = pandas.Series([start])
  for i in xrange(length - 1):
    timestamps.loc[i + 1] = timestamps.loc[i] + increment
  return timestamps


def generateWindows(timestamps, numWindows, windowSize):
  start = timestamps[0]
  delta = timestamps[1] - timestamps[0]
  length = len(timestamps)
  diff = int(round((length - numWindows * windowSize) / float(numWindows + 1)))
  windows = []
  for i in xrange(numWindows):
    t1 = start + delta * diff * (i + 1) + (delta * windowSize * i)
    t2 = t1 + (delta) * (windowSize - 1)
    if not any(timestamps == t1) or not any(timestamps == t2):
      raise ValueError("You got the wrong times from the window generator")
    windows.append([t1, t2])
  return windows


def generateLabels(timestamps, windows):
  labels = pandas.Series([0]*len(timestamps))
  for t1, t2 in windows:
    subset = timestamps[timestamps >= t1][timestamps <= t2]
    indices = subset.loc[:].index
    labels.values[indices] = 1
  return labels


class FalseNegativeTests(unittest.TestCase):


  def test_FalseNegativeCausesNegativeScore(self):
    start = datetime.datetime.now()
    increment = datetime.timedelta(minutes=5)
    length = 1000
    numWindows = 1
    windowSize = 10

    timestamps = generateTimestamps(start, increment, length)

    predictions = pandas.Series([0]*length)

    labels = pandas.Series([0]*length)

    windows = generateWindows(timestamps, numWindows, windowSize)

    costMatrix = {"tpWeight": 1.0,
    "fnWeight": 2.0,
    "fpWeight": 3.0,
    "tnWeight": 4.0}

    probationaryPeriod = 0

    scorer = Scorer(timestamps, predictions, labels, windows, costMatrix,
      probationaryPeriod)

    self.assertTrue(scorer.getScore() < 0)

if __name__ == '__main__':
  unittest.main()