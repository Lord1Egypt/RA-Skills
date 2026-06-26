#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_combo_profile_selected():
    result = handle({
        'skill_name': 'tcg-strategy-advisor',
        'input': {
            'archetype': 'combo',
            'win_condition': 'assemble two engine pieces and protect them',
            'turns_to_win': 6,
            'core_components': 'engine piece A, engine piece B',
        },
    })['result']
    assert 'Combo / Engine Assembly' in result
    assert 'Build Structure' in result
    assert 'Common Mistakes' in result


def test_aggro_string_input_supported():
    result = handle({
        'skill_name': 'tcg-strategy-advisor',
        'input': 'Style: aggro\nGoal: win before slower decks stabilize\nKey turn: 4\nRisks: too many expensive cards',
    })['result']
    assert 'Aggro / Tempo Pressure' in result
    assert 'Match Tempo' in result


def test_prompt_mode_returns_template():
    result = handle({'skill_name': 'tcg-strategy-advisor', 'mode': 'prompt'})['result']
    assert 'win condition' in result.lower()
    assert 'live metagame' in result.lower()


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
