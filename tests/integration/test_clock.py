# vim:ts=4:sw=4:et:
# Copyright 2012-present Facebook, Inc.
# Licensed under the Apache License, Version 2.0

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# no unicode literals

import WatchmanTestCase


@WatchmanTestCase.expand_matrix
class TestClock(WatchmanTestCase.WatchmanTestCase):

    def test_clock(self):
        root = self.mkdtemp()
        self.watchmanCommand('watch', root)
        clock = self.watchmanCommand('clock', root)

        self.assertRegexpMatches(clock['clock'], '^c:\d+:\d+:\d+:\d+$')

    def test_clock_sync(self):
        root = self.mkdtemp()
        self.watchmanCommand('watch', root)
        clock1 = self.watchmanCommand('clock', root, {'sync_timeout': 100})
        self.assertRegexpMatches(clock1['clock'], '^c:\d+:\d+:\d+:\d+$')

        clock2 = self.watchmanCommand('clock', root, {'sync_timeout': 100})
        self.assertRegexpMatches(clock2['clock'], '^c:\d+:\d+:\d+:\d+$')

        self.assertNotEqual(clock1, clock2)
