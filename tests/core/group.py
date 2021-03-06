# -*- coding: utf-8 -*-

from pyknyx.core.group import *
import unittest

# Mute logger
from pyknyx.services.logger import logging
logger = logging.getLogger(__name__)
logging.getLogger("pyknyx").setLevel(logging.ERROR)


class GroupTestCase(unittest.TestCase):

    def setUp(self):
        self.group = Group("1/1/1", None)

    def tearDown(self):
        pass

    def test_display(self):
        assert repr(self.group) == "<Group(gad='1/1/1')>"
        assert str(self.group) == "<Group('1/1/1')>"

    def test_constructor(self):
        pass

