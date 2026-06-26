#!/usr/bin/env python3
import argparse, json, os, re, subprocess, sys
from pathlib import Path


def chinese_ratio(text: str) -> float:
    if not text:
        return 0.0
    zh = len(re.findall(r'[\u4e00-\u9fff]', text))
    return zh / max(len(text), 1)


def load_env_file(path: str):
    if not path:
        return
    p = Path(path).expanduser()
    if not p.exists():
        return
    for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input')
    ap.add_argument('--out', required=True)
    ap.add_argument('--length', default='short')
    ap.add_argument('--env-file', default=None)
    ap.add_argument('--model', default=None)
    args = ap.parse_args()

    load_env_file(args.env_file)

    data = Path(args.input).read_text(encoding='utf-8', errors='replace')
    cmd = ['summarize', '-', '--length', args.length, '--json', '--no-cache', '--language', 'zh']
    if args.model:
        cmd += ['--model', args.model]
    proc = subprocess.run(cmd, input=data, text=True, capture_output=True, env=os.environ.copy())
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout)
        raise SystemExit(proc.returncode)

    payload = json.loads(proc.stdout)
    summary = (payload.get('summary') or '').strip()
    if not summary:
        raise SystemExit('summarize returned empty summary')
    if chinese_ratio(summary) < 0.15:
        raise SystemExit('summary is not Chinese enough')

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
