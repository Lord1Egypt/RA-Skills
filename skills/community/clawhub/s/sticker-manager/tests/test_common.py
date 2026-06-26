import os

from common import get_lang, t


def test_get_lang_prefers_explicit_value():
    assert get_lang('zh') == 'zh'
    assert get_lang('en') == 'en'


def test_get_lang_uses_lang_env(monkeypatch):
    monkeypatch.delenv('STICKER_MANAGER_LANG', raising=False)
    monkeypatch.setenv('LANG', 'zh_CN.UTF-8')
    assert get_lang() == 'zh'


def test_translate_returns_chinese_message():
    msg = t('library_empty', 'zh')
    assert '表情包库为空' in msg


def test_translate_returns_english_message():
    msg = t('library_empty', 'en')
    assert 'Sticker library is empty' in msg
