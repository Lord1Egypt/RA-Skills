# -*- coding: utf-8 -*-
import json

import data.updates as updates


def test_check_updates_git_outdated(tmp_path, monkeypatch):
    skill_dir = tmp_path / 'skills' / 'demo'
    (skill_dir / '.openclaw').mkdir(parents=True)
    origin = {'git': {'url': 'https://github.com/x/demo', 'commit': 'a' * 40}}
    (skill_dir / '.openclaw' / 'source-origin.json').write_text(json.dumps(origin))
    monkeypatch.setattr(updates, 'SKILLS_DIR', str(tmp_path / 'skills'))
    monkeypatch.setattr(updates, '_remote_head', lambda url: 'b' * 40)
    monkeypatch.setattr(updates, '_local_head', lambda d: '')
    rows = updates.check_updates([])
    assert rows[0]['status'] == 'outdated'


def test_check_updates_git_up_to_date(tmp_path, monkeypatch):
    sha = 'c' * 40
    skill_dir = tmp_path / 'skills' / 'demo'
    (skill_dir / '.openclaw').mkdir(parents=True)
    origin = {'git': {'url': 'https://github.com/x/demo', 'commit': sha}}
    (skill_dir / '.openclaw' / 'source-origin.json').write_text(json.dumps(origin))
    monkeypatch.setattr(updates, 'SKILLS_DIR', str(tmp_path / 'skills'))
    monkeypatch.setattr(updates, '_remote_head', lambda url: sha)
    monkeypatch.setattr(updates, '_local_head', lambda d: '')
    rows = updates.check_updates([])
    assert rows[0]['status'] == 'up_to_date'


def test_check_updates_clawhub_track():
    rows = updates.check_updates([
        {'name': 'some-skill', 'source': 'openclaw-clawhub'},
    ])
    assert rows[0]['track'] == 'clawhub' and rows[0]['status'] == 'managed'


def test_safe_git_url():
    assert updates._safe_git_url('https://github.com/x/y')
    assert not updates._safe_git_url('http://github.com/x/y')
    assert not updates._safe_git_url('https://192.168.1.1/x/y')
    assert not updates._safe_git_url('https://localhost/x/y')
