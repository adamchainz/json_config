#!/usr/bin/env python
# coding=utf-8
from textwrap import dedent

from pytest import fixture

from json_config.main import PrettyFormatMixin, AutoDict


@fixture
def pretty():
    class Pretty(PrettyFormatMixin, AutoDict):
        pass

    _pretty = Pretty()
    _pretty['this']['is']['a']['test'] = 'success'
    _pretty['completely']['different']['tree']['and']['different']['depth'] = 'hello'
    _pretty['this']['is']['not']['a']['test'] = 'more success'
    _pretty['this']['is']['a']['different']['test'] = 'still good'
    return _pretty


def test_can_pformat_dict(pretty):
    expected = dedent("""
        {
          "completely": {
            "different": {
              "tree": {
                "and": {
                  "different": {
                    "depth": "hello"
                  }
                }
              }
            }
          },
          "this": {
            "is": {
              "a": {
                "different": {
                  "test": "still good"
                },
                "test": "success"
              },
              "not": {
                "a": {
                  "test": "more success"
                }
              }
            }
          }
        }
        """)[1:-1]

    assert pretty.pformat() == expected


def test_pformat_with_different_indent(pretty):
    expected = dedent("""
        {
            "completely": {
                "different": {
                    "tree": {
                        "and": {
                            "different": {
                                "depth": "hello"
                            }
                        }
                    }
                }
            },
            "this": {
                "is": {
                    "a": {
                        "different": {
                            "test": "still good"
                        },
                        "test": "success"
                    },
                    "not": {
                        "a": {
                            "test": "more success"
                        }
                    }
                }
            }
        }
        """)[1:-1]

    assert pretty.pformat(indent=4) == expected
