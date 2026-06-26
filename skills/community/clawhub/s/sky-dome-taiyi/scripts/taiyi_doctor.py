#!/usr/bin/env python3
"""Practical project/skill doctor: inspect files, risks, publish readiness, and next actions."""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys
from pathlib import Path

RUNTIME_DIRS={'.git','node_modules','__pycache__','.pytest_cache','.mypy_cache','state','backups','backup','reports','logs','tmp','temp','context-checkpoints'}
SECRET_PATTERNS=[
    re.compile(r'sk-[A-Za-z0-9_-]{20,}'),
    re.compile(r'(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*["\']?[^"\'\s]{8,}'),
    re.compile(r'(?i)bearer\s+[A-Za-z0-9._-]{20,}'),
]
TEXT_SUFFIX={'.md','.txt','.json','.yaml','.yml','.py','.sh','.js','.ts','.toml'}

def git_status(path: Path):
    try:
        r=subprocess.run(['git','-C',str(path),'status','--short'],capture_output=True,text=True,timeout=5)
        if r.returncode==0: return r.stdout.strip().splitlines()
    except Exception: pass
    return None

def is_text(p: Path):
    return p.suffix.lower() in TEXT_SUFFIX or p.name in {'SKILL.md'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('path', nargs='?', default='.')
    ap.add_argument('--json', action='store_true')
    args=ap.parse_args()
    root=Path(args.path).resolve()
    if not root.exists(): raise SystemExit(f'not found: {root}')
    files=[]; runtime=[]; secrets=[]; large=[]; skill=False
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if p.is_dir(): continue
        files.append(str(rel))
        if any(part in RUNTIME_DIRS for part in rel.parts): runtime.append(str(rel))
        try:
            size=p.stat().st_size
            # Large optional reference manuals are allowed when kept under references/.
            if size>500_000 and not (len(rel.parts) >= 2 and rel.parts[0] == 'references'):
                large.append({'file':str(rel),'bytes':size})
            if is_text(p) and size<300_000:
                # Avoid self-flagging scanner source files that contain example regexes.
                if p.name in {'taiyi_doctor.py', 'taiyi_memory.py'}:
                    continue
                txt=p.read_text(errors='ignore')
                for pat in SECRET_PATTERNS:
                    if pat.search(txt):
                        secrets.append(str(rel)); break
        except Exception: pass
    if (root/'SKILL.md').exists(): skill=True
    issues=[]; actions=[]
    if skill and 'SKILL.md' not in files: issues.append('SKILL.md missing from manifest unexpectedly')
    if runtime:
        issues.append(f'runtime/noisy files present: {len(runtime)}')
        actions.append('stage with taiyi_stage.py before publishing')
    if secrets:
        issues.append(f'possible secrets in files: {len(secrets)}')
        actions.append('review and remove possible secrets before sharing')
    if large:
        issues.append(f'large files present: {len(large)}')
        actions.append('confirm large files are required')
    if skill:
        text=(root/'SKILL.md').read_text(errors='ignore')
        if 'description:' not in text.split('---',2)[1]: issues.append('frontmatter description missing')
        if len(text.splitlines())>500: actions.append('consider moving optional detail into references')
        if 'Verification' not in text and '验证' not in text: actions.append('add verification gates')
    gs=git_status(root)
    result={'path':str(root),'is_skill':skill,'file_count':len(files),'runtime_files':runtime[:50],'possible_secret_files':secrets,'large_files':large,'git_status':gs,'issues':issues,'recommended_actions':actions or ['no immediate action']}
    if args.json:
        print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print(f'# Taiyi Doctor: {root}')
        print(f'- Files: {len(files)}')
        print(f'- Skill: {skill}')
        print(f'- Issues: {len(issues)}')
        for x in issues: print(f'  - {x}')
        print('- Recommended actions:')
        for x in result['recommended_actions']: print(f'  - {x}')
        if runtime:
            print('- Runtime/noisy examples:')
            for x in runtime[:10]: print(f'  - {x}')
        if secrets:
            print('- Possible secret files:')
            for x in secrets: print(f'  - {x}')
if __name__=='__main__': main()
