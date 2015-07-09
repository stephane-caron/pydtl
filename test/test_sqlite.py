#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Stéphane Caron
#
# This file is part of PyDTL.
#
# PyDTL is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# PyDTL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with PyDTL. If not, see <http://www.gnu.org/licenses/>.

import pydtl
import unittest


class TestSQLite(unittest.TestCase):
    def setUp(self):
        self.db = pydtl.SQLiteDB('sample.sqlite')
        self.loc_table = self.db.dump_table('events')
        self.rem_table = pydtl.SQLiteTable('events', self.db)

    def test_count(self):
        self.assertEqual(self.loc_table.count(), self.rem_table.count())

    def test_mean(self, attr='activity'):
        lmean = self.loc_table.mean(attr)
        rmean = self.rem_table.mean(attr)
        self.assertTrue(abs(lmean - rmean) < 1e-5)

    def test_variance(self, attr='activity'):
        lvar = self.loc_table.variance(attr)
        rvar = self.rem_table.variance(attr)
        self.assertTrue(abs(lvar - rvar) < 1e-5)

    def test_sample(self, attr='activity'):
        rl = self.rem_table.sample_attr(attr, 31)
        self.assertEqual(len(rl), 31)

    def test_split(self):
        lt, rt, nt = self.rem_table.split('completion', 2)
        self.assertEqual(lt.count(), self.loc_table.count())
        self.assertEqual(rt.count(), 0)
        self.assertEqual(nt.count(), 0)

    def test_split_both(self):
        lt1, rt1, nt1 = self.loc_table.split('completion', .4)
        lt2, rt2, nt2 = self.rem_table.split('completion', .4)
        self.assertEqual(lt1.count(), lt2.count())
        self.assertEqual(rt1.count(), rt2.count())
        self.assertEqual(nt1.count(), nt2.count())

    def test_tree(self):
        tree = pydtl.RegressionTree(self.rem_table, 'activity',
                                    min_count=200, split_sampling=10)
        samples = self.rem_table.sample_rows(10)
        return [tree.predict(inst) for inst in samples]


if __name__ == '__main__':
    unittest.main()
