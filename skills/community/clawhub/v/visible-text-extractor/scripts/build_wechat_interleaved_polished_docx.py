#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path

DOCX = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts/build_transcript_docx.js')
ENGLISH_HEAVY = {4, 7, 8, 9, 10, 11}

COMMON_FIXES = {
    'Loweris': 'Lower is',
    'validationRMSE': 'Validation RMSE',
    'TrainingSteps': 'Training Steps',
    'Manageyour': 'Manage your',
    'wating': 'waiting',
    'resdy': 'ready',
    'Fesoling': 'Resolving',
    'Fecring': 'Fetching',
    'Bonciaw': 'BohrClaw',
    'BorCtaw': 'BohrClaw',
    'BohrClaw-s': 'BohrClaw-5',
    'Expl': 'Exp1',
    'Tiaining': 'Training',
    'RMSEimproved': 'RMSE improved',
    '0.191to': '0.191 to',
}


def compact(s: str):
    return re.sub(r'[\s\-—_.,，。:：;；|｜\[\]()（）<>《》]+', '', (s or '').strip()).lower()


def clean_general(text: str):
    lines = []
    seen = set()
    for raw in (text or '').splitlines():
        line = re.sub(r'\s+', ' ', raw).strip()
        if not line:
            if lines and lines[-1] != '':
                lines.append('')
            continue
        key = compact(line)
        if len(key) >= 8 and key in seen:
            continue
        if key:
            seen.add(key)
        lines.append(line)
    while lines and lines[-1] == '':
        lines.pop()
    return '\n'.join(lines).strip()


def polish_english_chart(text: str):
    t = clean_general(text)
    for a, b in COMMON_FIXES.items():
        t = t.replace(a, b)
    lines = []
    for raw in t.splitlines():
        line = raw.strip()
        if not line:
            if lines and lines[-1] != '':
                lines.append('')
            continue
        # 去掉夹杂在英文图表中的单个中文/符号噪点
        if len(line) <= 2 and re.search(r'[\u4e00-\u9fff]', line):
            continue
        if re.fullmatch(r'[\u4e00-\u9fff\W_]+', line) and len(line) <= 4:
            continue
        line = re.sub(r'(?<=[A-Za-z])(?=[A-Z][a-z])', ' ', line)
        line = re.sub(r'\bIr\b', 'lr', line)
        line = re.sub(r'\bNMA\b', 'N/A', line)
        line = re.sub(r'\bNA\b', 'N/A', line)
        line = re.sub(r'\s+', ' ', line).strip()
        if not line:
            continue
        lines.append(line)
    # 去重
    out = []
    seen = set()
    for line in lines:
        key = compact(line)
        if len(key) >= 8 and key in seen:
            continue
        if key:
            seen.add(key)
        out.append(line)
    return '\n'.join(out).strip()


def build_markdown(title: str, flow):
    parts = [f'# {title}', '']
    for block in flow:
        txt = (block.get('text') or '').strip()
        if not txt:
            continue
        parts.append(txt)
        parts.append('')
    return '\n'.join(parts).strip() + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-json', required=True)
    ap.add_argument('--output-prefix', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.input_json).read_text(encoding='utf-8'))
    title = data.get('title', 'Article')
    flow = data.get('flow', [])

    polished = []
    for block in flow:
        if block.get('type') != 'image_text':
            polished.append(block)
            continue
        idx = block.get('index')
        text = block.get('text', '')
        if idx in ENGLISH_HEAVY:
            text = polish_english_chart(text)
        else:
            text = clean_general(text)
        polished.append({'type': block.get('type'), 'index': idx, 'src': block.get('src'), 'text': text})

    prefix = Path(args.output_prefix)
    md_path = Path(str(prefix) + '.md')
    json_path = Path(str(prefix) + '.json')
    docx_path = Path(str(prefix) + '.docx')
    md_path.write_text(build_markdown(title, polished), encoding='utf-8')
    json_path.write_text(json.dumps({'title': title, 'flow': polished}, ensure_ascii=False, indent=2), encoding='utf-8')

    proc = subprocess.run(['node', str(DOCX), str(md_path), str(docx_path)], capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit((proc.stderr or proc.stdout or 'docx build failed').strip())
    print(json.dumps({'ok': True, 'md': str(md_path), 'json': str(json_path), 'docx': str(docx_path)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
