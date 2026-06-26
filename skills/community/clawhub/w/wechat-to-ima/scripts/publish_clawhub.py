#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INCLUDE = [
    'SKILL.md',
    'package.json',
    'package-lock.json',
    'scripts/errors.js',
    'scripts/extract.js',
    'scripts/save_wechat_to_ima.py',
    'scripts/publish_clawhub.py',
]


def copy_one(src_root: Path, rel: str, dst_root: Path):
    src = src_root / rel
    if not src.exists():
        return
    dst = dst_root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def build_stage_dir() -> Path:
    stage = Path(tempfile.mkdtemp(prefix='wechat-to-ima-publish-'))
    for rel in DEFAULT_INCLUDE:
        copy_one(ROOT, rel, stage)
    return stage


def main():
    ap = argparse.ArgumentParser(description='Stage and publish a sanitized ClawHub copy of this skill.')
    ap.add_argument('--version', help='ClawHub version to publish, e.g. 1.2.3')
    ap.add_argument('--changelog', default='Update skill', help='Changelog text for ClawHub publish')
    ap.add_argument('--slug', default='wechat-to-ima')
    ap.add_argument('--name', default='WeChat to IMA')
    ap.add_argument('--stage-only', action='store_true', help='Only create the sanitized stage directory')
    args = ap.parse_args()

    stage = build_stage_dir()
    print(stage)

    if args.stage_only:
        return

    if not args.version:
        raise SystemExit('--version is required unless --stage-only is used')

    cmd = [
        'clawhub', 'publish', str(stage),
        '--slug', args.slug,
        '--name', args.name,
        '--version', args.version,
        '--changelog', args.changelog,
    ]
    raise SystemExit(subprocess.run(cmd).returncode)


if __name__ == '__main__':
    main()
