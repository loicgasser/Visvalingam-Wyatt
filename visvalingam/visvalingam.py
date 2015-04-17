#!/usr/bin/python
# This script was written by Ralf Klammer, 24.10.2013
# Re-Implementation of Visvalingam-Wyatt-Algorithm
# Inspired by these descriptions: http://bost.ocks.org/mike/simplify/

# Simple Maths:
# http://de.wikipedia.org/wiki/Dreiecksfl%C3%A4che
# http://www.serlo.org/math/wiki/article/view/abstand-zweier-punkte-berechnen

import math


class VisvalingamSimplification:

    def __init__(self, line_):
        self.line = line_
        self.indizes = []
        for i in xrange(len(self.line)):
            self.indizes.append(i)
        self.enriched = False

    # Calculate the area of one triangle
    def getTriangleArea(self, prevP_, P_, nextP_):
        # Get the points of the triangle
        prevP = map(float, prevP_)
        P = map(float, P_)
        nextP = map(float, nextP_)
        # Calculate the triangle sites
        a = math.sqrt(pow(prevP[0] - P[0], 2) + pow(prevP[1] - P[1], 2))
        b = math.sqrt(pow(P[0] - nextP[0], 2) + pow(P[1] - nextP[1], 2))
        c = math.sqrt(pow(nextP[0] - prevP[0], 2) + pow(nextP[1] - prevP[1], 2))
        # Calculate the area of the triangle
        s = (a + b + c) / 2.0
        area_0 = s * (s - a) * (s - b) * (s - c)
        area_0 = abs(area_0)
        area = math.sqrt(area_0)
        return area

    # Add the area of the triangle to each point
    def enrichPoints(self):
        minArea = float("infinity")
        for i in range(1, len(self.indizes) - 1):
            this = self.indizes[i]
            prev = self.indizes[i - 1]
            next = self.indizes[i + 1]
            area = self.getTriangleArea(self.line[prev], self.line[this], self.line[next])
            # Reset min value for the area, if current is smaller than all previous
            if(area < minArea):
                minArea = area
            # Save the area of the triangle as a 3rd coordinate
            if(len(self.line[this]) < 3):     # Add if it does not exist
                self.line[this].append(area)
            else:                           # Replace if it does exist already
                self.line[this][2] = area
        return minArea

    # Look for the smallest triangles and remove the corresponding points from the index
    def removeSmallestAreaIndex(self, minArea):
        newIndizes = []
        for i in range(1, len(self.indizes) - 1):
            index = self.indizes[i]
            if(self.line[index][2] > minArea):
                newIndizes.append(index)
        newIndizes.insert(0, self.indizes[0])
        newIndizes.append(self.indizes[len(self.indizes) - 1])
        self.indizes = newIndizes

    # Do Visvalingam-Calculations until only the start & end points are left
    def enrichLineString(self):
        while(len(self.indizes) > 2):
            minArea_ = self.enrichPoints()
            self.removeSmallestAreaIndex(minArea_)
        self.enriched = True

    # Simplify a linestring corresponding to a given tolerance (depends on data projection)
    def simplifyLineString(self, tolerance_):
        tolerance = tolerance_
        # It is enough to enrich the line once
        minArea_ = self.enrichPoints()
        self.removeSmallestAreaIndex(minArea_)
        # Build the new line
        newLine = []
        for p in self.line:
            if(len(p) > 2):
                if(p[2] > tolerance):
                    newLine.append(p[0:2])
            else:
                newLine.append(p)
        return newLine
