# -*- coding: utf-8 -*-
from utils.translator import translate_description, extract_untranslated


def test_translate_known():
    assert translate_description('Set up and use the CLI').startswith('设置和使用')


def test_translate_unknown_kept():
    text = 'Completely unknown words here'
    assert translate_description(text) == text


def test_extract_untranslated():
    words = extract_untranslated(['Completely unknown words here', ''])
    assert 'completely' in words
    # 长度 <=3 的词被过滤
    assert 'the' not in words
