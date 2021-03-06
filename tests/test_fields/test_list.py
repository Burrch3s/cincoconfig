#
# Copyright (C) 2019 Adam Meily
#
# This file is subject to the terms and conditions defined in the file 'LICENSE', which is part of
# this source code package.
#
from typing import List
import pytest
from cincoconfig.fields import ListField, ListProxy, IntField
from cincoconfig.config import Schema, Config


class MockConfig:

    def __init__(self):
        self._data = {}


class TestListProxy:

    def test_create(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        assert wrap._items == [1, 2, 3]

    def test_len(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        assert len(wrap) == 3

    def test_eq_list(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        assert wrap == [1, 2, 3]

    def test_eq_proxy(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap2 = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        assert wrap == wrap2

    def test_eq_not_list(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        assert wrap != 'hello'

    def test_append(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap.append('4')
        assert wrap._items == [1, 2, 3, 4]

    def test_add_list(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap2 = wrap + [4, 5]
        assert wrap2._items == [1, 2, 3, 4, 5]

    def test_add_wrapper(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap2 = ListProxy(MockConfig(), IntField(), [4, '5'])
        wrap3 = wrap + wrap2
        assert wrap3._items == [1, 2, 3, 4, 5]

    def test_iadd(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap += [4, 5]
        assert wrap._items == [1, 2, 3, 4, 5]

    def test_getitem(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        assert wrap[1] == 2

    def test_getitem_error(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        with pytest.raises(IndexError):
            _ = wrap[4]

    def test_setitem(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap[1] = '5'
        assert wrap._items == [1, 5, 3]

    def test_clear(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap.clear()
        assert wrap._items == []

    def test_copy(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap2 = wrap.copy()
        assert wrap._items == wrap2._items
        assert wrap.field is wrap2.field
        assert wrap.cfg is wrap2.cfg

    def test_count(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        assert wrap.count(2) == 1

    def test_index(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        assert wrap.index(3) == 2

    def test_insert(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap.insert(1, '6')
        assert wrap._items == [1, 6, 2, 3]

    def test_pop_none(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        val = wrap.pop()
        assert val == 3
        assert wrap._items == [1, 2]

    def test_pop_index(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        val = wrap.pop(1)
        assert val == 2
        assert wrap._items == [1, 3]

    def test_remove(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap.remove(2)
        assert wrap._items == [1, 3]

    def test_reverse(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap.reverse()
        assert wrap._items == [3, 2, 1]

    def test_sort(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        wrap.sort(reverse=True)
        assert wrap._items == [3, 2, 1]

    def test_iter(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        content = list(iter(wrap))
        assert content == [1, 2, 3]

    def test_delitem(self):
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        del wrap[1]
        assert wrap._items == [1, 3]

    def test_to_basic_schema(self):
        schema = Schema()
        schema.x = IntField(default=1)
        schema.y = IntField(default=2)
        field = ListProxy(MockConfig(), schema)
        field.append(schema())
        assert field.to_basic() == [{'x': 1, 'y': 2}]

    def test_validate_schema_dict(self):
        schema = Schema()
        schema.x = IntField(default=1)
        schema.y = IntField(default=2)
        cfg = MockConfig()
        proxy = ListProxy(cfg, schema)

        check = proxy._validate({'x': 10})
        assert isinstance(check, Config)
        assert check.x == 10
        assert check.y == 2
        assert check._parent is cfg
        assert check._schema is schema

    def test_validate_schema_config(self):
        schema = Schema()
        schema.x = IntField(default=1)
        schema.y = IntField(default=2)
        cfg = MockConfig()
        proxy = ListProxy(cfg, schema)

        val = schema()
        val.x = 10
        check = proxy._validate(val)
        assert isinstance(check, Config)
        assert check is val
        assert check._parent is cfg
        assert check._schema is schema

    def test_validate_schema_invalid(self):
        schema = Schema()
        schema.x = IntField(default=1)
        schema.y = IntField(default=2)
        cfg = MockConfig()
        proxy = ListProxy(cfg, schema)

        with pytest.raises(ValueError):
            proxy._validate(100)


class TestListField:

    def test_storage_type_str(self):
        field = ListField(IntField())
        assert field.storage_type == List[int]

    def test_storage_type_custom(self):
        field = ListField(type)
        assert field.storage_type is List

    def test_storage_type_schema(self):
        schema = Schema()
        field = ListField(schema)
        assert field.storage_type == List[Schema]

    def test_required_not_empty(self):
        field = ListField(IntField(), required=True)
        value = field._validate(MockConfig(), [1, 2, '3'])
        assert value._items == [1, 2, 3]
        assert value.field is field.field

    def test_required_empty(self):
        field = ListField(IntField(), required=True)
        with pytest.raises(ValueError):
            field._validate(MockConfig(), [])

    def test_non_list(self):
        field = ListField(IntField())
        with pytest.raises(ValueError):
            field._validate(MockConfig(), 'asdf')

    def test_any_validate(self):
        field = ListField()
        value = field.validate(MockConfig(), [1, 2, 3])
        assert value == [1, 2, 3]
        assert isinstance(value, list)

    def test_to_basic(self):
        field = ListField(IntField(), required=True)
        wrap = ListProxy(MockConfig(), IntField(), [1, 2, '3'])
        assert field.to_basic(MockConfig(), wrap) == [1, 2, 3]

    def test_to_python(self):
        field = ListField(IntField(), required=True)
        wrap = field.to_python(MockConfig(), [1, 2, '3'])
        assert wrap.field is field.field
        assert wrap._items == [1, 2, 3]

    def test_to_basic_any(self):
        field = ListField()
        value = field.to_basic(MockConfig(), [1, 2, 3])
        assert value == [1, 2, 3]
        assert isinstance(value, list)

    def test_to_python_any(self):
        field = ListField()
        value = field.to_python(MockConfig(), [1, 2, 3])
        assert value == [1, 2, 3]
        assert isinstance(value, list)

    def test_validate_list_proxy(self):
        field = ListField(IntField())
        orig = ListProxy(MockConfig(), IntField(), [1, 2, 3])
        check = field._validate(MockConfig(), ListProxy(MockConfig(), IntField(), orig))
        assert isinstance(check, ListProxy)
        assert check._items == orig
        assert check is not orig
        assert check._items is not orig._items
