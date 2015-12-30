#!/usr/bin/env python
# coding=utf-8
import json
from abc import ABCMeta, abstractproperty, abstractmethod
from collections import defaultdict

from future.utils import with_metaclass


class TraceRootAbstract(with_metaclass(ABCMeta)):
    _root_ = NotImplemented

    @property
    @abstractproperty
    def _is_root(self):
        pass

    @property
    @abstractproperty
    def _root(self):
        pass

    @_root.setter
    @abstractproperty
    def _root(self, value):
        pass


class PrettyFormatAbstract(with_metaclass(ABCMeta)):
    pformat_indent = NotImplemented
    pformat_sort_keys = NotImplemented

    @abstractmethod
    def pformat(self):
        pass


class SaveFileAbstract(with_metaclass(ABCMeta)):
    config_file = NotImplemented

    @abstractmethod
    def save(self):
        pass


class TraceRootMixin(TraceRootAbstract):
    @property
    def _is_root(self):
        return self._root is self

    @property
    def _root(self):
        return self._root_[0]

    @_root.setter
    def _root(self, value):
        if isinstance(value, (list, tuple)):
            self._root_ = value
        else:
            self._root_ = [value]


class AutoDict(TraceRootMixin, defaultdict):
    def __init__(self, obj=None, _root=None):
        super(AutoDict, self).__init__()

        if obj is not None:
            self.update(obj)

        if _root is None:
            self._root = self
        else:
            self._root = _root

    def __missing__(self, key):
        AutoDict = self.__class__
        self[key] = value = AutoDict(_root=self._root)
        return value

    def __setitem__(self, key, value):
        _AutoDict = self.__class__

        # convert dicts to AutoDicts
        is_dict = not isinstance(value, _AutoDict) and isinstance(value, dict)
        if is_dict:
            value = _AutoDict(obj=value, _root=self._root)

        super(AutoDict, self).__setitem__(key, value)

    def __repr__(self):
        if self._is_root:
            cls_name = self.__class__.__name__
            return '%s(%s)' % (cls_name, dict(self))

        return repr(dict(self))


class AutoSyncMixin(SaveFileAbstract, TraceRootAbstract, PrettyFormatAbstract):
    def __init__(self, *args, **kwargs):
        config_file = kwargs.pop('config_file', None)
        """:type config_file: str|None"""

        if config_file is not None:
            self.config_file = config_file

            with open(config_file) as f:
                obj = json.load(f)
                kwargs.setdefault('obj', obj)

        super(AutoSyncMixin, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        # noinspection PyUnresolvedReferences
        super(AutoSyncMixin, self).__setitem__(key, value)

        if not isinstance(value, self.__class__):
            self._root.save()

    def save(self):
        if not self._is_root:
            raise RuntimeError('Trying to save from wrong node.')
        with open(self.config_file, 'w') as f:
            f.write(self.pformat())

    def pformat(self):
        return str(dict(self))


class PrettyFormatMixin(PrettyFormatAbstract):
    pformat_indent = 2
    pformat_sort_keys = True

    def pformat(self, **options):
        options.setdefault('indent', self.pformat_indent)
        options.setdefault('sort_keys', self.pformat_sort_keys)
        options.setdefault('separators', (',', ': '))

        return json.dumps(dict(self), **options)
