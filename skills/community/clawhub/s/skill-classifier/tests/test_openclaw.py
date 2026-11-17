# -*- coding: utf-8 -*-
from data.openclaw import get_skill_status


def test_ready():
    assert get_skill_status({'disabled': False, 'missing': {}}) == 'ready'


def test_any_bins_missing_marks_needsetup():
    skill = {'disabled': False, 'missing': {'anyBins': ['spotify_player', 'spotify']}}
    assert get_skill_status(skill) == 'needsetup'


def test_disabled():
    assert get_skill_status({'disabled': True, 'missing': {}}) == 'disabled'


def test_env_missing():
    assert get_skill_status({'disabled': False, 'missing': {'env': ['OP_TOKEN']}}) == 'needsetup'
