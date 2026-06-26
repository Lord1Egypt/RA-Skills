#!/usr/bin/env python3
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

CORE_FILES = ['AGENTS.md', 'SOUL.md', 'USER.md', 'MEMORY.md', 'TOOLS.md']
DUPLICATE_THEMES = {
    'ask-first': ['先确认', '先问', '拿不准就问', '不确定先问', '先确认再做'],
    'privacy-export': ['隐私', '不外泄', '外发前', '默认不公开', '公开前'],
    'style-clarity': ['简洁', '说清', '逻辑优先', '冷静', '关键处'],
    'skill-loading': ['SKILL.md', '任务匹配时先读', '先读对应', '技能怎么用'],
}
FILE_ROLE_HINTS = {
    'AGENTS.md': 'workspace rules and execution norms',
    'SOUL.md': 'voice and style principles',
    'USER.md': 'user preferences and interaction style',
    'MEMORY.md': 'long-term stable rules',
    'TOOLS.md': 'machine-local environment details',
}

@dataclass
class Issue:
    severity: str
    file: str
    kind: str
    detail: str
    suggestion: str = ''


def load_text(path: Path) -> str:
    try:
        return path.read_text()
    except Exception:
        return ''


def get_paths(scope: str, custom: List[str]) -> List[Path]:
    root = Path.cwd()
    if scope == 'custom':
        return [root / p for p in custom if (root / p).exists()]
    paths = [root / f for f in CORE_FILES]
    if scope == 'core+memory':
        mem = root / 'memory'
        if mem.exists():
            paths.extend(sorted(mem.glob('*.md'))[-2:])
    return [p for p in paths if p.exists()]


def split_sections(text: str) -> List[Tuple[str, List[str]]]:
    lines = text.splitlines()
    sections = []
    current_title = 'preamble'
    current_lines: List[str] = []
    for line in lines:
        if line.strip().startswith('#'):
            sections.append((current_title, current_lines))
            current_title = line.strip('# ').strip() or 'untitled'
            current_lines = []
        else:
            current_lines.append(line)
    sections.append((current_title, current_lines))
    return [(title, body) for title, body in sections if title != 'preamble' or any(x.strip() for x in body)]


def file_role_summary(path: Path, text: str) -> str:
    base = FILE_ROLE_HINTS.get(path.name, 'custom context file')
    lines = len(text.splitlines())
    headings = sum(1 for line in text.splitlines() if line.strip().startswith('#'))
    return f'{path.name}: {base}; {lines} lines; {headings} headings'


def match_theme_hits(text: str, needles: List[str]) -> List[str]:
    lower = text.lower()
    return [n for n in needles if n.lower() in lower]


def duplicate_severity(theme: str, matched: List[str]) -> Tuple[str, str]:
    matched_set = set(matched)
    if theme == 'privacy-export':
        if matched_set == {'AGENTS.md', 'SOUL.md', 'MEMORY.md'}:
            return 'low', 'This may be partially justified overlap across values, execution boundaries, and durable export defaults.'
    if theme == 'style-clarity':
        if matched_set.issubset({'SOUL.md', 'USER.md', 'AGENTS.md', 'MEMORY.md'}):
            return 'low', 'This may be partially justified overlap across tone, user preference, and concise-operating defaults.'
    return 'medium', 'Keep one file as the main source and trim repeated wording elsewhere.'


def find_duplicates(paths: List[Path]) -> List[Issue]:
    issues = []
    texts: Dict[str, str] = {p.name: load_text(p) for p in paths}
    for theme, needles in DUPLICATE_THEMES.items():
        matched = []
        evidence = {}
        for name, text in texts.items():
            hits = match_theme_hits(text, needles)
            if hits:
                matched.append(name)
                evidence[name] = ', '.join(sorted(set(hits))[:3])
        if len(matched) >= 2:
            severity, suggestion = duplicate_severity(theme, matched)
            detail = f'duplicate theme `{theme}` appears across ' + ', '.join(f'{name} ({evidence[name]})' for name in matched)
            issues.append(Issue(severity, ', '.join(matched), 'duplicate', detail, suggestion))
    return issues


def find_overweight(paths: List[Path]) -> List[Issue]:
    issues = []
    for p in paths:
        text = load_text(p)
        lines = text.splitlines()
        sections = split_sections(text)
        allow_list_heavy = p.name in {'TOOLS.md', 'USER.md'}
        if len(lines) > 80:
            issues.append(Issue('medium', p.name, 'overweight', f'file is relatively heavy for always-loaded context ({len(lines)} lines)', 'Move detailed procedures or examples into a reference or project-specific file.'))
        for title, body in sections:
            nonempty = [x for x in body if x.strip()]
            bullet_count = sum(1 for x in nonempty if x.strip().startswith(('-', '*')))
            if not allow_list_heavy and len(nonempty) >= 10 and bullet_count >= 8:
                issues.append(Issue('low', p.name, 'overweight', f'section `{title}` is list-heavy and may be better as a reference/checklist', 'Keep only the top-level rule here and move detailed list items into a reference or project note.'))
            if len(nonempty) >= 18:
                issues.append(Issue('medium', p.name, 'overweight', f'section `{title}` is long for always-loaded context ({len(nonempty)} non-empty lines)', 'Consider compressing the section or moving detailed procedural content elsewhere.'))
    return dedupe_issues(issues)


def find_misplaced(paths: List[Path]) -> List[Issue]:
    issues = []
    for p in paths:
        text = load_text(p)
        lower = text.lower()
        sections = split_sections(text)

        if p.name != 'TOOLS.md' and any(tok in lower for tok in ['/opt/homebrew', 'ssh ', 'speaker', 'display', '摄像头', '设备名', '房间名', '外设', '本机环境']):
            issues.append(Issue('medium', p.name, 'misplaced', 'contains machine-local or environment-specific details', 'Move machine-specific details into TOOLS.md.'))

        if p.name == 'MEMORY.md' and any(tok in text for tok in ['今天', '昨天', '刚刚', '这次', '随后', '一度', '已完成', '后来', '随后又']):
            issues.append(Issue('medium', p.name, 'misplaced', 'contains time-local wording that may belong in daily memory instead of long-term memory', 'Move temporary facts into memory/YYYY-MM-DD.md and keep only durable rules in MEMORY.md.'))

        if p.name == 'TOOLS.md' and any(tok in lower for tok in ['长期', '默认流程', '稳定规则', '上下文阈值', '外发前', '默认不公开']):
            issues.append(Issue('medium', p.name, 'misplaced', 'contains stable operating rules instead of machine-local details', 'Move stable rules into MEMORY.md and keep TOOLS.md environment-specific.'))

        if p.name in {'SOUL.md', 'USER.md'}:
            for title, body in sections:
                nonempty = [x for x in body if x.strip()]
                bullet_count = sum(1 for x in nonempty if x.strip().startswith(('-', '*')))
                if len(nonempty) >= 8 and bullet_count >= 6:
                    issues.append(Issue('low', p.name, 'misplaced', f'section `{title}` looks operationally dense for a style/preference file', 'Keep style/preference files lean; move operational detail into AGENTS.md, MEMORY.md, or a reference as appropriate.'))
                    break
                if any(tok in '\n'.join(nonempty).lower() for tok in ['skill.md', 'workflow', 'checklist', '脚本', 'reference', '导出目录', '发布目录']):
                    issues.append(Issue('low', p.name, 'misplaced', f'section `{title}` contains workflow-like guidance inside a style/preference file', 'Move reusable process detail into AGENTS.md, MEMORY.md, or a skill reference.'))
                    break

        if p.name == 'AGENTS.md':
            for title, body in sections:
                block = '\n'.join(body)
                if any(tok in block for tok in ['冷静', '温柔', '御姐感', '称呼用户']) and title.lower() not in {'group chats'}:
                    issues.append(Issue('low', p.name, 'misplaced', f'section `{title}` includes style/persona detail that may belong in SOUL.md or USER.md', 'Keep AGENTS.md focused on operating rules; move style/persona wording into SOUL.md or USER.md.'))
                    break
                if any(tok in block for tok in ['设备名', '房间名', '扬声器', '显示器', 'SSH 主机']) :
                    issues.append(Issue('low', p.name, 'misplaced', f'section `{title}` includes machine-local detail that likely belongs in TOOLS.md', 'Move local environment details into TOOLS.md.'))
                    break
    return dedupe_issues(issues)


def dedupe_issues(issues: List[Issue]) -> List[Issue]:
    seen = set()
    out = []
    for i in issues:
        key = (i.file, i.kind, i.detail)
        if key in seen:
            continue
        seen.add(key)
        out.append(i)
    return out


def top_priorities(issues: List[Issue]) -> List[Issue]:
    severity_rank = {'high': 0, 'medium': 1, 'low': 2}
    return sorted(issues, key=lambda x: (severity_rank.get(x.severity, 9), x.kind, x.file))[:3]


def render(paths: List[Path], roles: List[str], duplicates: List[Issue], overweight: List[Issue], misplaced: List[Issue]) -> str:
    all_issues = duplicates + overweight + misplaced
    priorities = top_priorities(all_issues)
    lines = [
        'Workspace Context Linter Report',
        f'Scope: {len(paths)} files',
        '',
        'Summary',
        f'- duplicates: {len(duplicates)}',
        f'- overweight sections/files: {len(overweight)}',
        f'- misplaced items: {len(misplaced)}',
        '',
        'File role summary',
    ]
    lines.extend([f'- {r}' for r in roles] or ['- None.'])
    lines += ['', 'Top priorities']
    lines.extend([f'- [{i.severity}] {i.file}: {i.detail}' for i in priorities] or ['- None.'])
    lines += ['', 'Duplicates']
    lines.extend([f'- [{i.severity}] {i.detail}' for i in duplicates] or ['- None found.'])
    lines += ['', 'Overweight sections']
    lines.extend([f'- [{i.severity}] {i.file}: {i.detail}' for i in overweight] or ['- None found.'])
    lines += ['', 'Misplaced content']
    lines.extend([f'- [{i.severity}] {i.file}: {i.detail}' for i in misplaced] or ['- None found.'])
    lines += ['', 'Suggested moves']
    suggestions = [i for i in all_issues if i.suggestion]
    lines.extend([f'- {i.file}: {i.suggestion}' for i in suggestions] or ['- None.'])
    return '\n'.join(lines) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser(description='Lint core workspace context files.')
    ap.add_argument('--scope', choices=['core', 'core+memory', 'custom'], default='core')
    ap.add_argument('--paths', nargs='*', default=[])
    ap.add_argument('--output')
    args = ap.parse_args()

    paths = get_paths(args.scope, args.paths)
    roles = [file_role_summary(p, load_text(p)) for p in paths]
    duplicates = find_duplicates(paths)
    overweight = find_overweight(paths)
    misplaced = find_misplaced(paths)
    report = render(paths, roles, duplicates, overweight, misplaced)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report)
    print(report, end='')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
