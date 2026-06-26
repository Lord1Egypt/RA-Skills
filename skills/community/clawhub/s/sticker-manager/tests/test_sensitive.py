from pathlib import Path

from scripts import check_sensitive


def test_allowlisted_placeholder_line_passes():
    assert check_sensitive.is_allowed('target="<chat_id>"')


def test_sensitive_pattern_matches_github_token():
    line = 'token = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcd"'
    matched = any(pattern.search(line) for _label, pattern in check_sensitive.BLOCK_PATTERNS)
    assert matched is True


def test_private_path_pattern_matches_root_path():
    line = '/root/EXAMPLE_PATH/secret.txt'
    matched = any(pattern.search(line) for _label, pattern in check_sensitive.BLOCK_PATTERNS)
    assert matched is True
