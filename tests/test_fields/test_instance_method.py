from unittest.mock import MagicMock
import pytest
from cincoconfig.fields import InstanceMethodField


class MockConfig:

    def __init__(self, data=None):
        self._data = data or {}


class TestInstanceMethodField:

    def setup_method(self, method=None):
        self.cfg = MockConfig()

    def _meth(self, cfg, x, y, z=None):
        return (cfg, x, y, z)

    def test_call_wrapper(self):
        field = InstanceMethodField(self._meth)
        wrapper = field.__getval__(self.cfg)
        assert wrapper.__name__ == '_meth'
        assert wrapper(1, y=2) == (self.cfg, 1, 2, None)

    def test_setval(self):
        field = InstanceMethodField(self._meth)
        with pytest.raises(TypeError):
            field.__setval__(self.cfg, self._meth)

    def test_default_error(self):
        with pytest.raises(TypeError):
            field = InstanceMethodField(self._meth, default=1)

    def test_no_setdefault(self):
        getter = MagicMock()
        getter.return_value = 'hello'
        cfg = MockConfig()
        field = InstanceMethodField(getter)
        field.__setdefault__(cfg)
        assert cfg._data == {}
