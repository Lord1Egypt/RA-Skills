#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QiBook 查企业查老板 - 统一入口
"""


def __getattr__(name):
    """延迟导入，避免 python -m scripts.combined_query 时的 RuntimeWarning"""
    _exports = {
        'fetch', 'fetch_entity_id', 'fetch_enterprise',
        'fetch_person_summary', 'fetch_person_detail',
    }
    if name in _exports:
        from . import combined_query
        return getattr(combined_query, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'fetch',
    'fetch_entity_id',
    'fetch_enterprise',
    'fetch_person_summary',
    'fetch_person_detail',
]
