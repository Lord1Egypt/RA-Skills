# -*- coding: utf-8 -*-
import json
import os

import data.toggle as toggle


def _make_cfg(tmp_path):
    cfg = tmp_path / 'openclaw.json'
    cfg.write_text(json.dumps({'agents': {'defaults': {'workspace': '~/ws'}}}), encoding='utf-8')
    return cfg


def test_set_enabled_disables(tmp_path, monkeypatch):
    cfg = _make_cfg(tmp_path)
    monkeypatch.setattr(toggle, 'OPENCLAW_CONFIG', str(cfg))
    monkeypatch.setattr(toggle, 'OPENCLAW_DIR', str(tmp_path))
    backup, changed = toggle.set_enabled(['alpha', 'beta'], False)

    new = json.loads(cfg.read_text(encoding='utf-8'))
    assert new['skills']['entries']['alpha']['enabled'] is False
    assert changed == {'alpha': False, 'beta': False}
    assert os.path.exists(backup)
    # 原有配置键不丢
    assert new['agents']['defaults']['workspace'] == '~/ws'


def test_set_enabled_enables_and_idempotent(tmp_path, monkeypatch):
    cfg = _make_cfg(tmp_path)
    monkeypatch.setattr(toggle, 'OPENCLAW_CONFIG', str(cfg))
    monkeypatch.setattr(toggle, 'OPENCLAW_DIR', str(tmp_path))
    toggle.set_enabled(['alpha'], True)
    toggle.set_enabled(['alpha'], True)
    new = json.loads(cfg.read_text(encoding='utf-8'))
    assert new['skills']['entries']['alpha']['enabled'] is True


def test_toggle_preserves_existing_entries(tmp_path, monkeypatch):
    cfg_path = tmp_path / 'openclaw.json'
    cfg_path.write_text(json.dumps({
        'skills': {'entries': {'keep-me': {'enabled': True, 'env': {'K': 'V'}}}},
    }), encoding='utf-8')
    monkeypatch.setattr(toggle, 'OPENCLAW_CONFIG', str(cfg_path))
    monkeypatch.setattr(toggle, 'OPENCLAW_DIR', str(tmp_path))
    toggle.set_enabled(['another'], False)
    new = json.loads(cfg_path.read_text(encoding='utf-8'))
    assert new['skills']['entries']['keep-me']['env'] == {'K': 'V'}
    assert new['skills']['entries']['another']['enabled'] is False
