# -*- coding: utf-8 -*-
import json

import classifier.category_map as cm
from classifier.category_map import get_category


def test_exact_match():
    assert get_category('问财选A股') == ('同花顺平台', '同花顺-选股与筛选')


def test_rule_match():
    assert get_category('tavily')[0] == '搜索工具'


def test_fallback():
    assert get_category('totally-unknown-skill') == ('其他', '其他')


def test_overlay(tmp_path, monkeypatch):
    overlay = tmp_path / 'skill_categories.json'
    overlay.write_text(json.dumps({'totally-unknown-skill': ['开发工具', '代码分析']}),
                       encoding='utf-8')
    monkeypatch.setattr(cm, 'CATEGORY_OVERLAY_FILE', str(overlay))
    cm._overlay_cache['mtime'] = None  # 强制重载
    assert get_category('totally-unknown-skill') == ('开发工具', '代码分析')
    assert get_category('tavily')[0] == '搜索工具'  # 覆盖层不影响命中映射表的技能


def test_overlay_invalid_entries_ignored(tmp_path, monkeypatch):
    overlay = tmp_path / 'skill_categories.json'
    overlay.write_text(json.dumps({'bad': ['只有一个元素'], 'ok': ['a', 'b']}), encoding='utf-8')
    monkeypatch.setattr(cm, 'CATEGORY_OVERLAY_FILE', str(overlay))
    cm._overlay_cache['mtime'] = None
    data = cm.load_category_overlay()
    assert 'bad' not in data and data['ok'] == ('a', 'b')
