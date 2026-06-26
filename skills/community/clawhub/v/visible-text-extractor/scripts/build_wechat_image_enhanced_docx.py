#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40'
BASE = Path('/root/.openclaw/workspace/skills/visible-text-extractor/scripts')
DOCX = BASE / 'build_deliverable_docx.js'
OCR_LOCAL = Path('/root/.openclaw/workspace/skills/ocr-local/scripts/ocr.js')
FEISHU_SENDER = Path('/root/.openclaw/workspace/skills/feishu-file-sender/scripts/feishu_file_sender.py')

NOISE_PATTERNS = [
    '@@', 'BOOM', 'MAIN POINT', 'TOPSIS', '从零开始学数学建模', '课程', '课表', '公众号',
    '群文件', 'b站课件', '钨往期回顾', '研究二习', '不正经科普大赛', '点赞', '转发', '关注'
]
PRIORITY_PATTERNS = [
    '评审', '评分', '标准', '奖项', '答辩', '校赛', '省赛', '国赛', '论文', '注意事项', '流程',
    '盆底肌', '漏尿', '妊娠', '分娩', '功能障碍', '凯格尔', '训练', '尿失禁', '快感'
]
REPLACEMENTS = {
    '盆席肌': '盆底肌',
    '僵底肌': '盆底肌',
    '金底肌': '盆底肌',
    '多底肌': '盆底肌',
    '人铭底肌': '盆底肌',
    '侈腔器官脱垂': '盆腔器官脱垂',
    '纵腔露宫脱重': '盆腔器官脱垂',
    '打喷吨': '打喷嚏',
    '怜起来': '爬起来',
    '盆席肌': '盆底肌',
    '吊网': '吊网',
    '咱俩再失误的话': '咱俩再失误的话',
}


def log(msg):
    print(msg, flush=True)


def run(cmd, timeout=300):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def download(url: str, out_dir: Path, idx: int):
    req = Request(url, headers={'User-Agent': UA})
    with urlopen(req, timeout=120) as resp:
        data = resp.read()
        ctype = resp.headers.get('Content-Type', '')
    ext = '.bin'
    if 'png' in ctype or 'wx_fmt=png' in url:
        ext = '.png'
    elif 'jpeg' in ctype or 'jpg' in ctype or 'wx_fmt=jpeg' in url or 'wx_fmt=jpg' in url:
        ext = '.jpg'
    p = out_dir / f'image-{idx:02d}{ext}'
    p.write_bytes(data)
    return p


def build_variants(image_path: Path, out_dir: Path):
    variants = [image_path]
    specs = [
        ('gray2x', 'scale=iw*2:ih*2:flags=lanczos,format=gray'),
        ('gray3x', 'scale=iw*3:ih*3:flags=lanczos,format=gray'),
        ('sharp3x', 'scale=iw*3:ih*3:flags=lanczos,format=gray,eq=contrast=1.4:brightness=0.03,unsharp=5:5:1.2:5:5:0.0'),
        ('sharp4x', 'scale=iw*4:ih*4:flags=lanczos,format=gray,eq=contrast=1.5:brightness=0.04,unsharp=7:7:1.8:7:7:0.0'),
    ]
    for name, vf in specs:
        dst = out_dir / f'{image_path.stem}-{name}.png'
        proc = run(['ffmpeg', '-y', '-i', str(image_path), '-vf', vf, str(dst)], timeout=240)
        if proc.returncode == 0 and dst.exists():
            variants.append(dst)
    return variants


def run_local_ocr(image_path: Path):
    proc = run(['node', str(OCR_LOCAL), str(image_path), '--lang', 'chi_sim+eng', '--json'], timeout=1800)
    if proc.returncode != 0:
        return {'ok': False, 'error': (proc.stderr or proc.stdout or 'ocr failed').strip(), 'path': str(image_path)}
    try:
        data = json.loads(proc.stdout)
    except Exception as e:
        return {'ok': False, 'error': f'bad ocr json: {e}', 'path': str(image_path)}
    return {'ok': True, 'path': str(image_path), 'text': data.get('text', '')}


def compact(line: str):
    return re.sub(r'[\s\-—_.,，。:：;；|｜\[\]()（）<>《》]+', '', line).lower()


def normalize_cn_spacing(line: str):
    s = line.strip()
    if sum(1 for ch in s if '\u4e00' <= ch <= '\u9fff') >= 2:
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', s)
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[，。！？：；、）》】])', '', s)
        s = re.sub(r'(?<=[（《【])\s+(?=[\u4e00-\u9fff])', '', s)
        s = re.sub(r'(?<=[0-9])\s+(?=[月日%岁级次分秒点])', '', s)
    s = re.sub(r'\(\s+', '(', s)
    s = re.sub(r'\s+\)', ')', s)
    s = re.sub(r'\s{2,}', ' ', s)
    return s.strip()


def apply_replacements(line: str):
    s = line
    for a, b in REPLACEMENTS.items():
        s = s.replace(a, b)
    s = s.replace('BMI>30 、 腰 围 这 88cm', 'BMI>30，腰围≥88cm')
    s = s.replace('做忍大便动作 10s', '做忍大便动作10s')
    s = s.replace('每天 2 次， 每次 50 站', '每天2次，每次50下')
    s = s.replace('缩紧盆底肌 > 3s， 再放松', '缩紧盆底肌 >3s，再放松')
    s = s.replace('每天 3 次， 每次 20 分钟', '每天3次，每次20分钟')
    s = s.replace('丁丁', '阴茎')
    return s


def is_noise_line(line: str):
    if not line:
        return True
    cjk = sum(1 for ch in line if '\u4e00' <= ch <= '\u9fff')
    digits = sum(1 for ch in line if ch.isdigit())
    letters = sum(1 for ch in line if ch.isalpha())
    key = compact(line)
    if key in {'', 'r', 'rt', 'me', 'eee', 'dn', '台', '4', '7'}:
        return True
    if len(key) <= 3 and cjk == 0 and digits == 0:
        return True
    if letters > cjk * 2 and cjk < 4 and digits < 2:
        return True
    if any(p.lower() in line.lower() for p in NOISE_PATTERNS):
        return True
    return False


def refine_image_text(text: str):
    raw_lines = [x.strip() for x in (text or '').splitlines()]
    out = []
    seen = set()
    for raw in raw_lines:
        if not raw:
            if out and out[-1] != '':
                out.append('')
            continue
        line = normalize_cn_spacing(apply_replacements(raw))
        if is_noise_line(line):
            continue
        key = compact(line)
        if len(key) >= 8 and key in seen:
            continue
        if key:
            seen.add(key)
        out.append(line)
    while out and out[-1] == '':
        out.pop()
    return '\n'.join(out).strip()


def score_text(text: str):
    if not text:
        return 0
    score = 0
    for pat in PRIORITY_PATTERNS:
        score += text.count(pat) * 6
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    digits = sum(1 for ch in text if ch.isdigit())
    lines = [x for x in text.splitlines() if x.strip()]
    score += cjk * 0.35 + digits * 0.25 + len(lines) * 2
    for pat in NOISE_PATTERNS:
        score -= text.lower().count(pat.lower()) * 10
    return int(score)


def best_ocr_for_image(image_path: Path, variant_dir: Path):
    best = None
    for variant in build_variants(image_path, variant_dir):
        ocr = run_local_ocr(variant)
        if not ocr.get('ok'):
            continue
        refined = refine_image_text(ocr.get('text', ''))
        score = score_text(refined)
        candidate = {
            'ok': True,
            'path': str(image_path),
            'variant': str(variant),
            'text': ocr.get('text', ''),
            'refined_text': refined,
            'score': score,
        }
        if best is None or candidate['score'] > best['score']:
            best = candidate
    if best:
        return best
    return {'ok': False, 'path': str(image_path), 'error': 'all variants failed'}


def keep_image(result):
    if not result.get('ok'):
        return False
    text = result.get('refined_text', '')
    if not text:
        return False
    score = result.get('score', 0)
    if score < 25:
        return False
    if sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff') < 20:
        return False
    return True


def build_markdown(title: str, body_text: str, image_results):
    parts = [f'# {title}', '']
    parts += ['## 文章原文', body_text or '(无)', '']
    parts += ['## 图片提取文字']
    kept = [x for x in image_results if keep_image(x)]
    if not kept:
        parts += ['(本次未提取到足够可靠的图片文字)', '']
    else:
        for i, item in enumerate(kept, 1):
            parts.append(f'### 图片 {i}')
            parts.append(item.get('refined_text', ''))
            parts.append('')
    return '\n'.join(parts).strip() + '\n'


def send_docx(docx: Path, receive_id: str):
    if not receive_id:
        return None
    proc = run(['python3', str(FEISHU_SENDER), '--file', str(docx), '--receive-id', receive_id], timeout=300)
    if proc.returncode != 0:
        raise SystemExit((proc.stderr or proc.stdout or 'send failed').strip())
    return json.loads(proc.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw-json', required=True)
    ap.add_argument('--output-prefix', required=True)
    ap.add_argument('--send-feishu-receive-id')
    args = ap.parse_args()

    raw = json.loads(Path(args.raw_json).read_text(encoding='utf-8'))
    title = raw.get('page', {}).get('title', 'WeChat Article')
    body_text = raw.get('body_text', '')
    images = raw.get('images', []) or []

    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    work_dir = Path(tempfile.mkdtemp(prefix='wechat-img-enhanced-'))
    image_dir = work_dir / 'images'
    variant_dir = work_dir / 'variants'
    image_dir.mkdir(parents=True, exist_ok=True)
    variant_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for idx, img in enumerate(images, 1):
        url = img.get('url')
        log(f'[image] {idx}/{len(images)} download')
        try:
            local = download(url, image_dir, idx)
        except Exception as e:
            results.append({'ok': False, 'url': url, 'error': f'download failed: {e}'})
            continue
        log(f'[image] {idx}/{len(images)} ocr-multivariant')
        res = best_ocr_for_image(local, variant_dir)
        res['url'] = url
        results.append(res)

    md = build_markdown(title, body_text, results)
    md_path = Path(str(prefix) + '.md')
    docx_path = Path(str(prefix) + '.docx')
    json_path = Path(str(prefix) + '.json')
    md_path.write_text(md, encoding='utf-8')
    json_path.write_text(json.dumps({'title': title, 'body_text': body_text, 'images': results}, ensure_ascii=False, indent=2), encoding='utf-8')

    proc = run(['node', str(DOCX), str(md_path), str(docx_path)], timeout=300)
    if proc.returncode != 0 or not docx_path.exists():
        raise SystemExit((proc.stderr or proc.stdout or 'docx build failed').strip())

    send_result = send_docx(docx_path, args.send_feishu_receive_id)
    print(json.dumps({
        'ok': True,
        'markdown': str(md_path),
        'json': str(json_path),
        'docx': str(docx_path),
        'sent': bool(send_result),
        'send_result': send_result,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
