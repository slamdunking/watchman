# vim:ts=4:sw=4:et:
# Copyright 2012-present Facebook, Inc.
# Licensed under the Apache License, Version 2.0

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# no unicode literals

import WatchmanTestCase
import os


@WatchmanTestCase.expand_matrix
class TestPathGenerator(WatchmanTestCase.WatchmanTestCase):
    def test_path_generator_dot(self):
        root = self.mkdtemp()

        self.watchmanCommand('watch', root)
        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'path': ['.']})['files'],
            [])

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'relative_root': '.',
                'path': ['.']})['files'],
            [])

    def test_path_generator_case(self):
        root = self.mkdtemp()

        os.mkdir(os.path.join(root, 'foo'))
        self.touchRelative(root, 'foo', 'bar')
        self.watchmanCommand('watch', root)

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'fields': ['name'],
                'path': ['foo']})['files'],
            ['foo/bar'])

        if self.isCaseInsensitive():
            os.rename(os.path.join(root, 'foo'), os.path.join(root, 'Foo'))

            self.assertFileListsEqual(
                self.watchmanCommand('query', root, {
                    'fields': ['name'],
                    'path': ['foo'],  # not Foo!
                })['files'],
                [],
                message="Case insensitive matching not implemented \
                        for path generator")

    def test_path_generator_relative_root(self):
        root = self.mkdtemp()

        os.mkdir(os.path.join(root, 'foo'))
        self.touchRelative(root, 'foo', 'bar')
        self.watchmanCommand('watch', root)

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'fields': ['name'],
                'relative_root': 'foo',
                'path': ['bar']})['files'],
            ['bar'])

        if self.isCaseInsensitive():
            os.rename(os.path.join(root, 'foo'), os.path.join(root, 'Foo'))

            self.assertFileListsEqual(
                self.watchmanCommand('query', root, {
                    'fields': ['name'],
                    'path': ['foo'],  # not Foo!
                })['files'],
                [],
                message="Case insensitive matching not implemented \
                        for path relative_root")
