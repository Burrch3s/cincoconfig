from unittest.mock import MagicMock
from cincoconfig.abc import Field
from cincoconfig.config import Schema, Config


class TestConfig:

    def test_setattr_protected(selF):
        schema = Schema()
        schema._add_field = MagicMock()
        schema._blah = 2
        assert schema._blah == 2
        assert not schema._add_field.called

    def test_setattr_field(self):
        field = Field()
        field.__setkey__ = MagicMock()
        schema = Schema()
        schema.field = field

        assert field.__setkey__.called_once_with(schema, 'field')
        assert schema._fields['field'] is field

    def test_getattr(self):
        schema = Schema()
        field = Field()
        schema.field = field

        assert schema.field is field

    def test_getattr_new(self):
        schema = Schema()
        field = schema.field
        assert isinstance(field, Schema)
        assert field._key == 'field'

    def test_iter(self):
        schema = Schema()
        subfield = Field()
        topfield = Field()
        schema.sub.field = subfield
        schema.field = topfield
        items = sorted(list(schema.__iter__()), key=lambda x: x[0])
        assert items == [('field', topfield), ('sub', schema.sub)]

    def test_call(self):
        schema = Schema()
        cfg = schema()
        assert isinstance(cfg, Config)
        assert cfg._schema is schema