#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_timing_push_profile_for_deadline_case():
    result = handle({
        'skill_name': 'strategy-game-mentor',
        'input': {
            'situation': 'one week before an exam with too many unfinished review tasks',
            'goal': 'secure the highest-yield topics before exam day',
            'resources': '2 focused hours each morning, class notes',
            'constraints': 'low energy at night, family logistics',
            'resistance': 'panic and jumping between topics',
            'deadline': 'exam day next week',
        },
    })['result']
    assert 'Timing Push' in result
    assert 'Three-Phase Plan' in result
    assert 'Decision Reminders' in result


def test_string_input_supported():
    result = handle({
        'skill_name': 'strategy-game-mentor',
        'input': 'Situation: too many parallel home admin tasks\nGoal: regain control this month\nResources: evenings, checklist habit\nConstraints: low energy\nPressure: scattered obligations',
    })['result']
    assert 'Board State' in result
    assert 'Recommended Stance' in result


def test_prompt_mode_returns_template():
    result = handle({'skill_name': 'strategy-game-mentor', 'mode': 'prompt'})['result']
    assert 'strategy game board' in result.lower()
    assert 'opening, midgame, endgame' in result.lower()


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
