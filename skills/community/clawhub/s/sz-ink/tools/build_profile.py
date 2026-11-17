#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sz-ink - build_profile.py 风格档案提取器 (v0.1)
用法: python build_profile.py <样例文本文件...> [--name 档案名] [--out 输出.json]
输入用户自己写的 3-5 段文字，输出风格档案 JSON（L6 资产）：
词汇偏好/句长分布/语气温度/留白度/节奏特征 + 推荐语体。
改写时作为目标参照系（"像谁"）。
"""
import sys, json, re, argparse
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))
from check_metrics import run  # 复用体检脚本的指标

CN_WORD_RE = re.compile(r'[\u4e00-\u9fff]{2,6}')


def split_sentences(text):
    parts = re.split(r'[。！？!?]+', text)
    return [p.strip() for p in parts if p.strip()]


def extract_profile(texts):
    joined = '\n'.join(texts)
    n_chars = len(re.sub(r'\s', '', joined))

    # 句长分布
    sents = split_sentences(joined)
    lens = [len(re.sub(r'[，、；：""''（）\s]', '', s)) for s in sents]
    lens = [l for l in lens if l > 0]
    avg_len = sum(lens) / len(lens) if lens else 0

    # 语气/留白偏好
    prof = run(joined, 'colloquial_media')  # 用最敏感的阈值组测倾向
    m = prof['metrics']

    # 高频实词（词汇偏好）
    words = CN_WORD_RE.findall(joined)
    stop = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一',
            '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着',
            '没有', '看', '好', '自己', '这', '那', '但', '还', '被', '把', '让'}
    top_words = [(w, c) for w, c in Counter(words).most_common(30)
                 if w not in stop and len(w) >= 2][:15]

    # 语体判定建议（粗判：本人写作时套话密度最低的语体组即其惯用语体）
    reg_scores = {}
    for reg in ['colloquial_media', 'official_doc', 'explanatory']:
        try:
            reg_scores[reg] = run(joined, reg)['metrics']['cliche_density']
        except Exception:
            reg_scores[reg] = None
    valid = {r: v for r, v in reg_scores.items() if v is not None}
    best_reg = min(valid, key=valid.get) if valid else 'colloquial_media'

    return {
        'sample_count': len(texts),
        'char_count': n_chars,
        'sentence': {
            'count': len(lens),
            'avg_len': round(avg_len, 1),
            'len_min': min(lens) if lens else 0,
            'len_max': max(lens) if lens else 0,
        },
        'metrics_baseline': {
            'rhythm_cv': m['rhythm_cv'],
            'short_burst_ratio': m['short_burst_ratio'],
            'cliche_density': m['cliche_density'],
            'modal_temp': m['modal_temp'],
            'hedge_density': m['hedge_density'],
        },
        'vocab_preference': [{'word': w, 'count': c} for w, c in top_words],
        'register_guess': best_reg,
        'register_scores': reg_scores,
        'note': '改写时目标：指标不超本人基线1.5倍；词汇偏好只作参照不强行植入',
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+', help='样例文本文件（1个或多个）')
    ap.add_argument('--name', default='user_profile', help='档案名')
    ap.add_argument('--out', default=None, help='输出JSON路径（默认stdout）')
    a = ap.parse_args()

    texts = []
    for f in a.files:
        p = Path(f)
        if not p.exists():
            print(f'跳过不存在的文件: {f}', file=sys.stderr)
            continue
        texts.append(p.read_text(encoding='utf-8'))
    if not texts:
        sys.exit('错误: 无可用样例文本')

    total_chars = sum(len(t) for t in texts)
    if total_chars < 200:
        print(f'警告: 样例总量仅{total_chars}字（建议>=800字），档案可信度低', file=sys.stderr)

    profile = {'name': a.name, **extract_profile(texts)}
    out = json.dumps(profile, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(out, encoding='utf-8')
        print(f'风格档案已生成: {a.out}')
    else:
        print(out)


if __name__ == '__main__':
    main()
