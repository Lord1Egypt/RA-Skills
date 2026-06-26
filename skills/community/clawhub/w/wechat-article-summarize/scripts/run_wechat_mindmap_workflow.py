#!/usr/bin/env python3
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
READ = SCRIPT_DIR / 'read_wechat_article.py'
FIX = SCRIPT_DIR / 'fix_wechat_body.py'
SUM = SCRIPT_DIR / 'summarize_cn.py'
BATCH = SCRIPT_DIR / 'build_batch_report.py'
SINGLE = SCRIPT_DIR / 'build_mindmap_markdown.py'


def run(cmd, **kwargs):
    proc = subprocess.run(cmd, text=True, capture_output=True, **kwargs)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout)
        raise SystemExit(proc.returncode)
    return proc.stdout.strip()


def truthy(v: str) -> bool:
    return str(v).strip().lower() in {'1', 'true', 'yes', 'y', '要'}


def resolve_output_dir(s: str) -> Path:
    if s in {'下载文件夹', 'downloads', '~/Downloads'}:
        return Path('~/Downloads').expanduser()
    return Path(s).expanduser()


def verify_summarize(env_file=None, model=None):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / 'probe.txt'
        out = Path(td) / 'probe.json'
        p.write_text('测试 summarize 是否可用。', encoding='utf-8')
        cmd = ['python3', str(SUM), str(p), '--out', str(out), '--length', 'short']
        if env_file:
            cmd += ['--env-file', env_file]
        if model:
            cmd += ['--model', model]
        run(cmd)
        payload = json.loads(out.read_text())
        if not payload.get('summary'):
            raise SystemExit('summarize probe failed')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('urls', nargs='+')
    ap.add_argument('--include-images', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--env-file', default=None)
    ap.add_argument('--report-label', default='微信文章日报')
    ap.add_argument('--model', default=None)
    ap.add_argument('--work-dir', default=None)
    args = ap.parse_args()

    verify_summarize(args.env_file, args.model)

    include_images = truthy(args.include_images)
    output_dir = resolve_output_dir(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    base = Path(args.work_dir or (Path.cwd() / 'tmp' / 'wechat-workflow-run'))
    base.mkdir(parents=True, exist_ok=True)
    article_dirs = []

    for idx, url in enumerate(args.urls, 1):
        d = base / f'a{idx}'
        d.mkdir(parents=True, exist_ok=True)
        run(['python3', str(READ), url, '--out', str(d)])
        raw = d / 'raw.html'
        body = d / 'body-fixed.txt'
        run(['python3', str(FIX), str(raw), '--out', str(body)])
        summary = d / 'summary.json'
        cmd = ['python3', str(SUM), str(body), '--out', str(summary), '--length', 'short']
        if args.env_file:
            cmd += ['--env-file', args.env_file]
        if args.model:
            cmd += ['--model', args.model]
        run(cmd)
        article_dirs.append(d)

    if len(article_dirs) == 1:
        d = article_dirs[0]
        cmd = [
            'python3', str(SINGLE),
            '--result', str(d / 'result.json'),
            '--body', str(d / 'body-fixed.txt'),
            '--summary', str(d / 'summary.json'),
            '--output-dir', str(output_dir),
            '--include-images', 'true' if include_images else 'false',
        ]
        print(run(cmd))
        return 0

    combined_input = base / 'combined-input.md'
    chunks = ['# 微信文章汇总输入', '']
    for i, d in enumerate(article_dirs, 1):
        result = json.loads((d / 'result.json').read_text())
        title = result.get('meta', {}).get('title') or f'文章 {i}'
        summary = json.loads((d / 'summary.json').read_text()).get('summary', '').strip()
        chunks += [f'## 文章 {i}', f'标题：{title}', f'摘要：{summary}', '']
    combined_input.write_text('\n'.join(chunks), encoding='utf-8')

    combined_summary = base / 'combined-summary.json'
    cmd = ['python3', str(SUM), str(combined_input), '--out', str(combined_summary), '--length', 'medium']
    if args.env_file:
        cmd += ['--env-file', args.env_file]
    if args.model:
        cmd += ['--model', args.model]
    run(cmd)

    cmd = ['python3', str(BATCH), '--inputs'] + [str(x) for x in article_dirs] + [
        '--output-dir', str(output_dir),
        '--include-images', 'true' if include_images else 'false',
        '--report-label', args.report_label,
        '--combined-summary', str(combined_summary),
    ]
    print(run(cmd))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
