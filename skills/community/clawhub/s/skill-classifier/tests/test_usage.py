# -*- coding: utf-8 -*-
import sqlite3

import data.usage as usage


def test_from_state_db(tmp_path, monkeypatch):
    db = tmp_path / 'state.sqlite'
    con = sqlite3.connect(db)
    con.execute('CREATE TABLE skill_usage (skill_name TEXT, use_count INTEGER, last_used_at_ms INTEGER)')
    con.execute('INSERT INTO skill_usage VALUES (?, ?, ?)', ('alpha', 5, 1700000000000))
    con.commit()
    con.close()
    monkeypatch.setattr(usage, 'STATE_DB', str(db))
    stats = usage._from_state_db()
    assert stats['alpha']['calls'] == 5
    assert stats['alpha']['last_used'] is not None


def test_from_state_db_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(usage, 'STATE_DB', str(tmp_path / 'missing.sqlite'))
    assert usage._from_state_db() is None


def test_get_usage_stats_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(usage, 'STATE_DB', str(tmp_path / 'missing.sqlite'))
    monkeypatch.setattr(usage, '_from_curator', lambda: None)
    assert usage.get_usage_stats() == {}


def test_from_curator(monkeypatch):
    class FakeOut:
        returncode = 0
        stdout = '{"skills": [{"name": "alpha", "useCount": 7, "lastUsedAtMs": 1700000000000}]}'

    monkeypatch.setattr('subprocess.run', lambda *a, **k: FakeOut())
    stats = usage._from_curator()
    assert stats['alpha']['calls'] == 7
