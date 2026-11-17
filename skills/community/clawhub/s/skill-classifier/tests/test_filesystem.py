# -*- coding: utf-8 -*-
import data.filesystem as fs


def test_nested_leaf_shadows_top_level(tmp_path, monkeypatch):
    """嵌套技能叶子名不得吞掉顶层同名技能（SkillSpector 审查整改的回归测试）"""
    skills_dir = tmp_path / 'skills'
    nested = skills_dir / 'bundle' / 'weather'
    nested.mkdir(parents=True)
    (nested / 'SKILL.md').write_text('# nested', encoding='utf-8')
    top = skills_dir / 'weather'
    top.mkdir()
    (top / 'SKILL.md').write_text('# top', encoding='utf-8')
    monkeypatch.setattr(fs, 'SKILLS_DIR', str(skills_dir))
    found = fs.scan_skills_directory()
    assert len(found) == 2
    assert {f['name'] for f in found} == {'weather'}
    assert {f['dir_path'] for f in found} == {str(nested), str(top)}


def test_plain_top_level_scan(tmp_path, monkeypatch):
    skills_dir = tmp_path / 'skills'
    for name in ('alpha', 'beta'):
        d = skills_dir / name
        d.mkdir(parents=True)
        (d / 'SKILL.md').write_text(f'# {name}', encoding='utf-8')
    plain = skills_dir / 'not-a-skill'
    plain.mkdir()
    monkeypatch.setattr(fs, 'SKILLS_DIR', str(skills_dir))
    found = fs.scan_skills_directory()
    assert {f['name'] for f in found} == {'alpha', 'beta'}


def test_dir_to_name_map(tmp_path, monkeypatch):
    skills_dir = tmp_path / 'skills'
    d = skills_dir / 'alpha'
    d.mkdir(parents=True)
    (d / 'SKILL.md').write_text('# A', encoding='utf-8')
    monkeypatch.setattr(fs, 'SKILLS_DIR', str(skills_dir))
    mapping = fs.get_dir_to_name_map()
    assert mapping.get('alpha') == 'alpha'
