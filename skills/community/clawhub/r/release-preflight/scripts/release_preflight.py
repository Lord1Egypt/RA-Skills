#!/usr/bin/env python3
import argparse
from collections import defaultdict
from pathlib import Path

PRIVATE_DIR_NAMES = {'memory', '.openclaw', 'tmp'}
PRIVATE_DIR_PREFIXES = ('.venv',)
PRIVATE_PATH_PREFIXES = ('logs/audit',)
PRIVATE_FILE_NAMES = {'.DS_Store'}
TEXT_EXTS = {'.md', '.txt', '.json', '.yml', '.yaml', '.sh', '.py', '.js', '.ts', '.toml'}
USER_HOME_TOKEN = '/' + 'Users/'
SYSTEM_PRIVATE_TOKEN = '/' + 'private/'
HOMEBREW_TOKEN = '/' + 'opt/' + 'homebrew/'
OPENCLAW_TOKEN = '.open' + 'claw/'


def infer_type(path: Path) -> str:
    if (path / 'SKILL.md').exists():
        return 'skill'
    if (path / '.git').exists():
        return 'repo'
    return 'bundle'


def list_paths(root: Path):
    return sorted(p for p in root.rglob('*') if p != root)


def rel(root: Path, path: Path) -> str:
    return str(path.relative_to(root))


def is_private_artifact(root: Path, path: Path) -> bool:
    rp = rel(root, path)
    parts = path.relative_to(root).parts
    if path.name in PRIVATE_FILE_NAMES:
        return True
    if any(part in PRIVATE_DIR_NAMES for part in parts):
        return True
    if any(part.startswith(PRIVATE_DIR_PREFIXES) for part in parts):
        return True
    return any(rp == prefix or rp.startswith(prefix + '/') for prefix in PRIVATE_PATH_PREFIXES)


def summarize_private_hits(root: Path):
    groups = defaultdict(int)
    singles = []
    for path in list_paths(root):
        if not is_private_artifact(root, path):
            continue
        rp = rel(root, path)
        parts = path.relative_to(root).parts
        group = None
        for part in parts:
            if part in PRIVATE_DIR_NAMES or part.startswith(PRIVATE_DIR_PREFIXES):
                group = part
                break
        if group is None:
            for prefix in PRIVATE_PATH_PREFIXES:
                if rp == prefix or rp.startswith(prefix + '/'):
                    group = prefix
                    break
        if group:
            groups[group] += 1
        else:
            singles.append(rp)
    summary = []
    for group, count in sorted(groups.items()):
        if count == 1:
            summary.append(group)
        else:
            summary.append(f'{group}/ ({count} nested private items)')
    summary.extend(sorted(set(singles)))
    return summary


def find_overscope(root: Path, target_type: str):
    warnings = []
    minimal = []
    optional = []
    if target_type == 'skill':
        minimal = ['SKILL.md', 'references/', 'scripts/']
        optional = ['README.md', 'CHANGELOG.md']
        top = {p.name for p in root.iterdir()}
        allowed = {'SKILL.md', 'references', 'scripts', 'README.md', 'CHANGELOG.md'}
        extras = sorted(x for x in top if x not in allowed)
        if extras:
            warnings.append(
                'Found extra top-level items outside the usual minimal skill surface: ' + ', '.join(extras)
            )
    elif target_type == 'repo':
        minimal = ['project root files needed for understanding/use', 'source directories', 'docs needed for public use']
    else:
        minimal = ['only files intentionally meant to be shared']
    return warnings, minimal, optional


def scan_text_file(path: Path):
    try:
        return path.read_text(errors='ignore')
    except Exception:
        return ''


def should_skip_identity_scan(root: Path, path: Path) -> bool:
    parts = path.relative_to(root).parts
    if any(part in PRIVATE_DIR_NAMES for part in parts):
        return True
    if any(part.startswith(PRIVATE_DIR_PREFIXES) for part in parts):
        return True
    rp = rel(root, path)
    return any(rp == prefix or rp.startswith(prefix + '/') for prefix in PRIVATE_PATH_PREFIXES)


def find_identity_leaks(root: Path):
    hits = []
    for path in list_paths(root):
        if should_skip_identity_scan(root, path):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTS:
            continue
        text = scan_text_file(path)
        if not text:
            continue
        markers = []
        if USER_HOME_TOKEN in text:
            markers.append('absolute macOS user path')
        if SYSTEM_PRIVATE_TOKEN in text:
            markers.append('private system path')
        if HOMEBREW_TOKEN in text:
            markers.append('homebrew host path')
        if ('/' + OPENCLAW_TOKEN) in text or OPENCLAW_TOKEN in text:
            markers.append('openclaw local path')
        if markers:
            hits.append({'path': rel(root, path), 'markers': markers})
    return hits


def readiness_checks(root: Path, target_type: str):
    blocking = []
    warnings = []
    if target_type == 'skill':
        if not (root / 'SKILL.md').exists():
            blocking.append('Missing required SKILL.md for skill target.')
        if not (root / 'references').exists() and not (root / 'scripts').exists():
            warnings.append('Skill has neither references/ nor scripts/; verify the public surface is intentionally minimal.')
    elif target_type == 'repo':
        candidates = ['README.md', 'readme.md', 'package.json', 'pyproject.toml']
        if not any((root / c).exists() for c in candidates):
            warnings.append('Repo has no obvious entry or explanation file at the root.')
    else:
        candidates = ['README.md', 'readme.md', 'manifest.json']
        top_entries = list(root.iterdir())
        if not top_entries:
            warnings.append('Bundle appears empty.')
        elif not any((root / c).exists() for c in candidates):
            warnings.append('Bundle has no obvious explanation file; verify recipients will understand its purpose.')
    return blocking, warnings


def decide(blocking, warnings):
    if blocking:
        return 'not_ready'
    if warnings:
        return 'ready_after_fixes'
    return 'ready'


def render_report(root: Path, target_type: str, publish_target: str, decision: str, blocking, warnings, exclusions, minimal, optional, leaks):
    lines = [
        'Release Preflight Report',
        f'Target: {root}',
        f'Type: {target_type}',
        f'Publish target: {publish_target}',
        f'Decision: {decision}',
        '',
        'Summary',
        f'- blocking issues: {len(blocking)}',
        f'- warnings: {len(warnings)}',
        f'- suggested exclusions: {len(exclusions)}',
        f'- identity leakage hits: {len(leaks)}',
        '',
        'Blocking issues',
    ]
    lines.extend([f'- {x}' for x in blocking] or ['- None.'])
    lines += ['', 'Warnings']
    lines.extend([f'- {x}' for x in warnings] or ['- None.'])
    lines += ['', 'Suggested exclusions']
    lines.extend([f'- {x}' for x in exclusions] or ['- None.'])
    lines += ['', 'Minimal publish surface']
    lines.extend([f'- {x}' for x in minimal] or ['- None suggested.'])
    if optional:
        lines += ['', 'Optional public files']
        lines.extend([f'- {x}' for x in optional])
    lines += ['', 'Identity leakage review']
    if leaks:
        for hit in leaks:
            lines.append(f"- {hit['path']} :: {', '.join(hit['markers'])}")
    else:
        lines.append('- No obvious local identity leakage found.')
    lines += ['', 'Action hints']
    hints = [
        'Run an export safety review before publication.',
        'Record external_publish after release completes.',
    ]
    if publish_target in {'github', 'clawhub'}:
        hints.append('If visibility changes during release, record repo_visibility_change.')
    lines.extend([f'- {x}' for x in hints])
    return '\n'.join(lines) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser(description='Pre-release safety and scope checker.')
    ap.add_argument('target_path')
    ap.add_argument('--type', choices=['auto', 'skill', 'repo', 'bundle'], default='auto')
    ap.add_argument('--publish-target', choices=['generic', 'github', 'clawhub', 'manual-export'], default='generic')
    ap.add_argument('--output', help='Optional path to write the text report.')
    args = ap.parse_args()

    root = Path(args.target_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit('Target path must exist and be a directory.')

    target_type = infer_type(root) if args.type == 'auto' else args.type
    blocking, warnings = [], []

    private_hits = summarize_private_hits(root)
    if private_hits:
        for hit in private_hits:
            msg = f'Private/local artifact included in target surface: {hit}'
            if target_type in {'skill', 'bundle'}:
                blocking.append(msg)
            else:
                warnings.append(msg)

    extra_warnings, minimal, optional = find_overscope(root, target_type)
    warnings.extend(extra_warnings)

    leak_hits = find_identity_leaks(root)
    if leak_hits:
        warnings.append('Found possible local identity leakage in text files; inspect the listed files below.')

    more_blocking, more_warnings = readiness_checks(root, target_type)
    blocking.extend(more_blocking)
    warnings.extend(more_warnings)

    decision = decide(blocking, warnings)
    report = render_report(root, target_type, args.publish_target, decision, blocking, warnings, private_hits, minimal, optional, leak_hits)

    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report)
    print(report, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
