# vim:ts=4:sw=4:et:
# Copyright 2012-present Facebook, Inc.
# Licensed under the Apache License, Version 2.0

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# no unicode literals

import WatchmanTestCase
import os
import pywatchman


@WatchmanTestCase.expand_matrix
class TestNameExpr(WatchmanTestCase.WatchmanTestCase):
    def test_name_expr(self):
        root = self.mkdtemp()

        self.touchRelative(root, 'foo.c')
        os.mkdir(os.path.join(root, 'subdir'))
        self.touchRelative(root, 'subdir', 'bar.txt')

        self.watchmanCommand('watch', root)

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'expression': ['iname', 'FOO.c'],
                'fields': ['name']})['files'],
            ['foo.c'])

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'expression': ['iname', ['FOO.c', 'INVALID.txt']],
                'fields': ['name']})['files'],
            ['foo.c'])

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'expression': ['name', 'foo.c'],
                'fields': ['name']})['files'],
            ['foo.c'])

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'expression': ['name', ['foo.c', 'invalid']],
                'fields': ['name']})['files'],
            ['foo.c'])

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'expression': ['name', 'foo.c', 'wholename'],
                'fields': ['name']})['files'],
            ['foo.c'])

        if self.isCaseInsensitive():
            self.assertFileListsEqual(
                self.watchmanCommand('query', root, {
                    'expression': ['name', 'Foo.c', 'wholename'],
                    'fields': ['name']})['files'],
                ['foo.c'])

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'expression': ['name', 'bar.txt', 'wholename'],
                'fields': ['name']})['files'],
            [])

        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'expression': ['name', 'bar.txt', 'wholename'],
                'relative_root': 'subdir',
                'fields': ['name']})['files'],
            ['bar.txt'])

        # foo.c is not in subdir so this shouldn't return any matches
        self.assertFileListsEqual(
            self.watchmanCommand('query', root, {
                'expression': ['name', 'foo.c', 'wholename'],
                'relative_root': 'subdir',
                'fields': ['name']})['files'],
            [])

        with self.assertRaises(pywatchman.WatchmanError) as ctx:
            self.watchmanCommand('query', root, {
                'expression': 'name'})

        self.assertRegexpMatches(
            str(ctx.exception),
            "Expected array for 'i?name' term")

        with self.assertRaises(pywatchman.WatchmanError) as ctx:
            self.watchmanCommand('query', root, {
                'expression': ['name', 'one', 'two', 'three']})

        self.assertRegexpMatches(
            str(ctx.exception),
            "Invalid number of arguments for 'i?name' term")

        with self.assertRaises(pywatchman.WatchmanError) as ctx:
            self.watchmanCommand('query', root, {
                'expression': ['name', 2]})

        self.assertRegexpMatches(
            str(ctx.exception),
            ("Argument 2 to 'i?name' must be either a string "
            "or an array of string"))

        with self.assertRaises(pywatchman.WatchmanError) as ctx:
            self.watchmanCommand('query', root, {
                'expression': ['name', 'one', 2]})

        self.assertRegexpMatches(
            str(ctx.exception),
            "Argument 3 to 'i?name' must be a string")

        with self.assertRaises(pywatchman.WatchmanError) as ctx:
            self.watchmanCommand('query', root, {
                'expression': ['name', 'one', 'invalid']})

        self.assertRegexpMatches(
            str(ctx.exception),
            "Invalid scope 'invalid' for i?name expression")
