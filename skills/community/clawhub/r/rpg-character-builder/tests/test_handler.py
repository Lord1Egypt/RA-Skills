#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_grounded_build_sections_exist():
    result = handle({
        'skill_name': 'rpg-character-builder',
        'input': {
            'current_state': 'parent learning AI at home',
            'ideal_role': 'a calm strategist who can teach others',
            'values': 'growth, family, clarity',
            'strengths': ['analysis', 'care', 'curiosity'],
            'weaknesses': ['consistency', 'overthinking'],
            'desired_skills': ['shipping small projects', 'clear teaching'],
        },
    })['result']
    assert 'Character Card' in result
    assert 'Build Route' in result
    assert "This Week's Level-Up Actions" in result
    assert ('Strategist' in result) or ('Guide' in result)


def test_string_input_supported():
    result = handle({
        'skill_name': 'rpg-character-builder',
        'input': 'Current state: changing careers\nIdeal role: builder who teaches clearly\nStrengths: writing, systems\nWeaknesses: stamina\nDesired skills: shipping, facilitation',
    })['result']
    assert 'Grounded RPG Build' in result
    assert 'Attribute Points' in result


def test_prompt_mode_returns_template():
    result = handle({'skill_name': 'rpg-character-builder', 'mode': 'prompt'})['result']
    assert 'grounded rpg build' in result.lower()
    assert 'weekly upgrade actions' in result.lower()


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
