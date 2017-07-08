# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2017 Ryan Roden-Corrent (rcorre) <ryan@rcorre.net>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for CompletionFilterModel."""

from unittest import mock

import pytest

from qutebrowser.completion.models import listcategory
from qutebrowser.commands import cmdexc


@pytest.mark.parametrize('pattern, before, after', [
    ('foo',
     [('foo', ''), ('bar', '')],
     [('foo', '')]),

    ('foo',
     [('foob', ''), ('fooc', ''), ('fooa', '')],
     [('fooa', ''), ('foob', ''), ('fooc', '')]),

    # prefer foobar as it starts with the pattern
    ('foo',
     [('barfoo', ''), ('foobar', '')],
     [('foobar', ''), ('barfoo', '')]),

    ('foo',
     [('foo', 'bar'), ('bar', 'foo'), ('bar', 'bar')],
     [('foo', 'bar'), ('bar', 'foo')]),
])
def test_set_pattern(pattern, before, after, validate_model):
    """Validate the filtering and sorting results of set_pattern."""
    cat = listcategory.ListCategory('Foo', before)
    cat.set_pattern(pattern)
    validate_model(cat, after)


def test_delete_cur_item(validate_model):
    func = mock.Mock(spec=[])
    cat = listcategory.ListCategory('Foo', [('a', 'b'), ('c', 'd')],
                                    delete_func=func)
    idx = cat.index(0, 0)
    cat.delete_cur_item(idx)
    func.assert_called_once_with(['a', 'b'])
    validate_model(cat, [('c', 'd')])


def test_delete_cur_item_no_func(validate_model):
    cat = listcategory.ListCategory('Foo', [('a', 'b'), ('c', 'd')])
    idx = cat.index(0, 0)
    with pytest.raises(cmdexc.CommandError, match="Cannot delete this item."):
        cat.delete_cur_item(idx)
    validate_model(cat, [('a', 'b'), ('c', 'd')])
