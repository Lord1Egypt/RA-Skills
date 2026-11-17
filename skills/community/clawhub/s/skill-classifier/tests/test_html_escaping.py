# -*- coding: utf-8 -*-
from exporter.html_exporter import generate_html, _deps_svg


def _skills():
    return [
        {'name': 'good-skill', 'status': 'ready', 'version': '1.0', 'source': 'openclaw-bundled',
         'emoji': '🔥', 'homepage': 'https://example.com', 'description': 'safe'},
        {'name': 'evil"/><script>alert(1)</script>', 'status': 'needsetup', 'version': '<b>9</b>',
         'source': 'openclaw-workspace', 'emoji': '', 'homepage': 'javascript:alert(1)',
         'description': '<img src=x onerror=alert(1)>', 'big_category': '其他', 'sub_category': '其他'},
    ]


def test_homepage_javascript_scheme_dropped():
    page = generate_html(_skills(), 't')
    assert 'javascript:alert(1)' not in page


def test_esc_helper_applied_to_metadata():
    import re
    page = generate_html(_skills(), 't')
    # JS 渲染层对名称/版本/分类/通用列做转义（innerHTML XSS 整改）
    assert re.search(r'esc\(.+skill\.name\)', page)
    assert 'esc(skill.version)' in page
    assert 'esc(skill.big_category)' in page
    assert 'esc(skill.homepage)' in page
    assert ': esc(v)' in page
    assert 'rel="noopener noreferrer"' in page


def test_json_script_break_neutralized():
    page = generate_html(_skills(), 't')
    assert '</script>alert' not in page


def test_deps_svg_escapes_names():
    edges = [{'skill': 'a<b>c', 'dep': 'ffmpeg', 'kind': 'bin'}]
    svg = _deps_svg(edges)
    assert 'a<b>c' not in svg
    assert 'a&lt;b&gt;c' in svg


def test_normal_rendering_unaffected():
    page = generate_html(_skills(), 't')
    assert 'good-skill' in page
    assert 'https://example.com' in page
    assert 'searchInput' in page
