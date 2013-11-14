from trinamic_3d_printer.gcode import GCode, decode_gcode_line
from hamcrest import *

__author__ = 'marcus'
import unittest

class GCodeTest(unittest.TestCase):

    def testGCodeCodeDecoding(self):
        line="M107"
        result = decode_gcode_line(line)
        assert_that(result.code,equal_to("M107"))

    def testGCodeParameterDecoding(self):
        line="G1 X94.100 Y84.157 E1.44607"
        result = decode_gcode_line(line)
        assert_that(result.code,equal_to("G1"))
        assert_that(result.options,has_length(3))
        assert_that(result.options,has_item("Y84.157"))
        assert_that(result.options,has_item("X94.100"))
        assert_that(result.options,has_item("E1.44607"))

    def testGCodeComment(self):
        line="G21 ; set units to millimeters"
        result = decode_gcode_line(line)
        assert_that(result.code,equal_to("G21"))
        assert_that(result.options,none())

        line = "; generated by Slic3r 0.9.10b on 2013-11-13 at 13:21:08"
        result = decode_gcode_line(line)
        assert_that(result,none())

    def testGCodeRobustness(self):
        line="G1 X94.100 \tY84.157  E1.44607"
        result = decode_gcode_line(line)
        assert_that(result.code,equal_to("G1"))
        assert_that(result.options,has_length(3))
        assert_that(result.options,has_item("Y84.157"))
        assert_that(result.options,has_item("X94.100"))
        assert_that(result.options,has_item("E1.44607"))

        line = " ; generated by Slic3r 0.9.10b on 2013-11-13 at 13:21:08"
        result = decode_gcode_line(line)
        assert_that(result,none())

        line="M107\n"
        result = decode_gcode_line(line)
        assert_that(result.code,equal_to("M107"))
