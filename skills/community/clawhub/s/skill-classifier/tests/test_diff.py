# -*- coding: utf-8 -*-
import utils.diff as diff


def test_compare_added_changed(tmp_path, monkeypatch):
    monkeypatch.setattr(diff, 'SNAPSHOT_FILE', str(tmp_path / 'snapshot.json'))
    monkeypatch.setattr(diff, 'DIFF_HISTORY_FILE', str(tmp_path / 'history.json'))

    old = [{'name': 'a', 'status': 'ready', 'version': '1.0', 'description': 'x'}]
    diff.save_snapshot(old)

    current = [
        {'name': 'a', 'status': 'ready', 'version': '2.0', 'description': 'x'},
        {'name': 'b', 'status': 'ready', 'version': '1.0', 'description': 'y'},
    ]
    result = diff.compare_skills(current)
    assert [s['name'] for s in result['added']] == ['b']
    assert [c['name'] for c in result['changed']] == ['a']


def test_compare_removed(tmp_path, monkeypatch):
    monkeypatch.setattr(diff, 'SNAPSHOT_FILE', str(tmp_path / 'snapshot.json'))
    monkeypatch.setattr(diff, 'DIFF_HISTORY_FILE', str(tmp_path / 'history.json'))

    diff.save_snapshot([
        {'name': 'gone', 'status': 'ready', 'version': '1.0', 'description': 'x'},
        {'name': 'kept', 'status': 'ready', 'version': '1.0', 'description': 'x'},
    ])
    result = diff.compare_skills([
        {'name': 'kept', 'status': 'ready', 'version': '1.0', 'description': 'x'},
    ])
    assert [s['name'] for s in result['removed']] == ['gone']


def test_hash_stable():
    assert diff.generate_skill_hash({'a': 1}) == diff.generate_skill_hash({'a': 1})
