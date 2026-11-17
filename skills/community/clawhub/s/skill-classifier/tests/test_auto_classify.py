# -*- coding: utf-8 -*-
from classifier.auto_classify import find_duplicate_skills


def _s(name, desc):
    return {'name': name, 'description': desc}


def test_name_pattern():
    skills = [_s('eastmoney-helper', 'a' * 40), _s('mx-helper', 'b' * 40)]
    dup = find_duplicate_skills(skills)
    assert any('东方财富' in reason for _, _, reason in dup)


def test_similar_description():
    d1 = 'Monitor blogs and RSS feeds for updates using a CLI tool'
    d2 = 'Monitor blogs and RSS feeds for updates using a CLI utility'
    dup = find_duplicate_skills([_s('alpha', d1), _s('beta', d2)])
    assert any('相似' in reason for _, _, reason in dup)


def test_different_not_flagged():
    dup = find_duplicate_skills([
        _s('alpha', 'one tool doing things very well'),
        _s('beta', 'another thing entirely different here'),
    ])
    assert dup == []


def test_short_descriptions_skipped():
    assert find_duplicate_skills([_s('alpha', 'short one'), _s('beta', 'short one')]) == []
