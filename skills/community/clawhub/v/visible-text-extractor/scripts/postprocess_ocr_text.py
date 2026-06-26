#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter
from pathlib import Path

CJK_RE = re.compile(r'[\u4e00-\u9fff]')
PRICE_RE = re.compile(r'(?:￥|¥|RMB\s*)?[Yy]?\d{1,6}(?:\.\d{1,2})?\s*元?')
DATE_RE = re.compile(r'(?:\d{4}[./-]\d{1,2}[./-]\d{1,2}|\d{1,2}[./-]\d{1,2}|\d{1,2}月\d{1,2}日(?:\s*[—\-~至到]\s*\d{1,2}月\d{1,2}日)?|即日起|长期有效)')
TIME_RE = re.compile(r'(?:[01]?\d|2[0-3])[:：][0-5]\d(?:\s*[-—~至到]\s*(?:[01]?\d|2[0-3])[:：][0-5]\d)?')
CONTACT_RE = re.compile(r'(?:电话|微信|VX|V信|报名|咨询|联系|客服|二维码|扫码|地址|地点|集合地点|导航|主办|承办|协办|适合|对象|年龄|名额|限购|使用时间|有效期|预约|说明|规则|须知|权益|包含|套餐|课程|目录|流程|步骤|景点|亮点|特色|发车|入园|退改|费用)')
AIRLINE_RE = re.compile(r'(?:上海|武汉|温州|大连|杭州|西安|浦东机场|接送机|送机|接机|托运行李|经济舱|改签|退票)')
HOTEL_RE = re.compile(r'(?:酒店|度假酒店|温泉|双早|早餐|入住|离店|房型|大床房|双床房|连住|不加价|亲子活动|可取消)')
RULES_RE = re.compile(r'(?:适用范围|有效期|使用说明|使用方式|退赔说明|注意事项|报名须知|评分标准|流程|评审)')

IMAGE_TYPE_RULES = {
    'pricing': [
        '团购', '抢购', '秒杀', '特价', '原价', '现价', '到手价', '套餐', '票价', '门票', '成人票', '儿童票',
        '双人', '单人', '立减', '优惠', '券后', '拼团', '限时', '预售', '库存', '使用时间', '有效期', '退改', '包含', '权益'
    ],
    'rules': [
        '规则', '须知', '报名须知', '评分', '评分标准', '细则', '流程', '步骤', '办法', '要求', '条件', '说明', '注意事项', '评审', '资格', '审核'
    ],
    'poster': [
        '活动', '讲座', '论坛', '沙龙', '公开课', '直播', '分享会', '报名', '时间', '地点', '主讲', '嘉宾', '扫码', '立即报名', '活动时间', '参与方式'
    ],
    'course': [
        '课程', '大纲', '目录', '章节', '模块', '课时', '训练营', '专题', '学习', '第一讲', '第二讲', 'lesson', 'module', 'chapter'
    ],
    'scenery': [
        '景点', '景区', '风景', '人文', '历史', '古镇', '博物馆', '推荐', '亮点', '打卡', '介绍', '文化', '特色', '游玩', '攻略'
    ],
    'table_like': [
        '分值', '项目', '指标', '序号', '名称', '内容', '备注', '标准', '得分', '单位', '类别', '数量', '明细'
    ],
}

TYPE_LABELS = {
    'pricing': '价格/商品页',
    'rules': '规则/评分页',
    'poster': '海报/活动页',
    'course': '课程/目录页',
    'scenery': '景色/人文页',
    'table_like': '表格/明细页',
    'mixed': '混合信息页',
    'unknown': '未确定类型',
}


def normalize_line(line: str) -> str:
    s = (line or '').replace('\u3000', ' ').strip()
    s = s.replace('Al', 'AI').replace('A上', 'AI')
    s = re.sub(r'\s+', ' ', s).strip()
    if len(CJK_RE.findall(s)) >= 4:
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', s)
        s = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[，。！？：；、）》】])', '', s)
        s = re.sub(r'(?<=[（《【])\s+(?=[\u4e00-\u9fff])', '', s)
    s = re.sub(r'[|｜]{2,}', '|', s)
    s = re.sub(r'[·•]{2,}', '•', s)
    s = re.sub(r'[“”]{2,}', '“', s)
    s = re.sub(r'^[_\-~+=*#@]+$', '', s).strip()
    return s.strip()


def compact_for_check(line: str) -> str:
    return re.sub(r'[\s\-—_.,，。:：;；|｜\[\]()（）<>《》]+', '', line).lower()


def has_meaningful_cjk(line: str) -> bool:
    return len(CJK_RE.findall(line)) >= 3


def is_noise_line(line: str) -> bool:
    if not line:
        return True
    compact = compact_for_check(line)
    if compact in {'', 'ye', 'oo', 'rn'}:
        return True
    if line in {'//', '/', '|', '||', '|||', '-', '--', '---'}:
        return True
    if len(compact) <= 2 and not has_meaningful_cjk(line):
        return True
    punct_ratio = sum(1 for ch in line if not ch.isalnum() and not CJK_RE.match(ch)) / max(len(line), 1)
    if len(line) <= 6 and punct_ratio > 0.6:
        return True
    alpha_ratio = sum(1 for ch in line if ch.isalpha()) / max(len(line), 1)
    if alpha_ratio > 0.7 and len(line) <= 12 and not any(x in line.lower() for x in ['vip', 'ai']):
        return True
    return False


def quality_score(line: str) -> int:
    score = 0
    if has_meaningful_cjk(line):
        score += 2
    if PRICE_RE.search(line):
        score += 3
    if DATE_RE.search(line) or TIME_RE.search(line):
        score += 2
    if CONTACT_RE.search(line):
        score += 2
    if AIRLINE_RE.search(line) or HOTEL_RE.search(line) or RULES_RE.search(line):
        score += 2
    if any(ch.isdigit() for ch in line):
        score += 1
    compact = compact_for_check(line)
    if compact and len(compact) >= 6:
        score += 1
    return score


def clean_lines(text: str):
    lines = [normalize_line(x) for x in (text or '').replace('\r', '\n').splitlines()]
    out = []
    prev_blank = False
    seen = set()
    for line in lines:
        if is_noise_line(line):
            if out and not prev_blank:
                out.append('')
            prev_blank = True
            continue
        dedupe_key = compact_for_check(line)
        if len(dedupe_key) >= 6 and dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        out.append(line)
        prev_blank = False
    cleaned = []
    last_blank = False
    for line in out:
        if not line:
            if cleaned and not last_blank:
                cleaned.append('')
            last_blank = True
        else:
            cleaned.append(line)
            last_blank = False
    return cleaned


def filter_full_lines(image_type: str, lines):
    filtered = []
    for line in lines:
        if not line:
            if filtered and filtered[-1] != '':
                filtered.append('')
            continue
        compact = compact_for_check(line)
        cjk = len(CJK_RE.findall(line))
        digit = sum(ch.isdigit() for ch in line)
        if image_type in {'poster', 'rules', 'pricing', 'course'}:
            if len(compact) <= 2 and cjk == 0 and digit == 0:
                continue
        if image_type == 'poster':
            if len(compact) <= 4 and cjk <= 1 and digit == 0:
                continue
        if image_type == 'pricing':
            if len(compact) <= 3 and not (PRICE_RE.search(line) or DATE_RE.search(line) or TIME_RE.search(line)):
                continue
        filtered.append(line)
    while filtered and not filtered[-1]:
        filtered.pop()
    return filtered


def guess_image_type(text: str):
    t = (text or '').lower()
    scores = Counter()
    for key, keywords in IMAGE_TYPE_RULES.items():
        for kw in keywords:
            if kw.lower() in t:
                scores[key] += 1
    if RULES_RE.search(text):
        scores['rules'] += 3
    if AIRLINE_RE.search(text) or HOTEL_RE.search(text):
        scores['pricing'] += 2
    if scores:
        top_type, top_score = scores.most_common(1)[0]
        if top_score >= 2:
            return top_type
        if top_score == 1 and len(scores) == 1:
            return top_type
        return 'mixed'
    return 'unknown'


def extract_candidate_lines(lines, min_score=3):
    candidates = []
    for line in lines:
        if not line:
            continue
        score = quality_score(line)
        if score >= min_score:
            candidates.append((score, line))
    candidates.sort(key=lambda x: (-x[0], len(x[1])))
    ordered = []
    used = set()
    for score, line in candidates:
        key = compact_for_check(line)
        if key in used:
            continue
        used.add(key)
        ordered.append(line)
    return ordered


def extract_fields(lines):
    fields = {
        'prices': [],
        'dates': [],
        'times': [],
        'contacts': [],
        'routes': [],
        'hotels': [],
        'rules': [],
        'highlights': [],
    }
    seen = {k: set() for k in fields}
    for line in lines:
        compact = compact_for_check(line)
        if not compact:
            continue
        if PRICE_RE.search(line) and compact not in seen['prices']:
            fields['prices'].append(line)
            seen['prices'].add(compact)
        if DATE_RE.search(line) and compact not in seen['dates']:
            fields['dates'].append(line)
            seen['dates'].add(compact)
        if TIME_RE.search(line) and compact not in seen['times']:
            fields['times'].append(line)
            seen['times'].add(compact)
        if CONTACT_RE.search(line) and compact not in seen['contacts']:
            fields['contacts'].append(line)
            seen['contacts'].add(compact)
        if AIRLINE_RE.search(line) and compact not in seen['routes']:
            fields['routes'].append(line)
            seen['routes'].add(compact)
        if HOTEL_RE.search(line) and compact not in seen['hotels']:
            fields['hotels'].append(line)
            seen['hotels'].add(compact)
        if RULES_RE.search(line) and compact not in seen['rules']:
            fields['rules'].append(line)
            seen['rules'].add(compact)
        if quality_score(line) >= 5 and compact not in seen['highlights']:
            fields['highlights'].append(line)
            seen['highlights'].add(compact)
    return fields


def build_summary_for_type(image_type: str, lines):
    fields = extract_fields(lines)
    summary = []
    if image_type == 'pricing':
        for line in fields['routes'][:3]:
            summary.append(f'行程/商品：{line}')
        for line in fields['hotels'][:3]:
            summary.append(f'酒店/房型：{line}')
        for line in fields['prices'][:5]:
            summary.append(f'价格/费用：{line}')
        for line in (fields['dates'] + fields['times'])[:5]:
            summary.append(f'时间/有效期：{line}')
        for line in fields['contacts'][:4]:
            summary.append(f'权益/限制：{line}')
    elif image_type == 'rules':
        for line in fields['rules'][:8]:
            summary.append(f'规则：{line}')
        for line in fields['dates'][:3]:
            summary.append(f'时间：{line}')
    elif image_type == 'poster':
        for line in fields['highlights'][:4]:
            summary.append(f'主题：{line}')
        for line in (fields['dates'] + fields['times'])[:4]:
            summary.append(f'时间：{line}')
        for line in fields['contacts'][:4]:
            summary.append(f'活动信息：{line}')
    elif image_type == 'course':
        for line in fields['highlights'][:8]:
            summary.append(f'课程结构：{line}')
    elif image_type == 'scenery':
        for line in fields['highlights'][:8]:
            summary.append(f'景点/亮点：{line}')
    else:
        for line in extract_candidate_lines(lines, min_score=4)[:8]:
            summary.append(f'关键信息：{line}')

    if not summary:
        for line in extract_candidate_lines(lines, min_score=3)[:8]:
            summary.append(f'关键信息：{line}')
    return summary[:12]


def build_fulltext_for_type(image_type: str, lines):
    return filter_full_lines(image_type, lines)


def group_image_blocks(raw_data):
    blocks = []
    for img in raw_data.get('images', []) or []:
        text = (img.get('ocr_text') or '').strip()
        if not text:
            continue
        lines = clean_lines(text)
        if not lines:
            continue
        image_type = guess_image_type('\n'.join(lines))
        summary_lines = build_summary_for_type(image_type, lines)
        full_lines = build_fulltext_for_type(image_type, lines)
        blocks.append({
            'kind': 'image',
            'index': img.get('index'),
            'source': img.get('url') or '',
            'image_type': image_type,
            'type_label': TYPE_LABELS.get(image_type, TYPE_LABELS['unknown']),
            'lines': lines,
            'full_lines': full_lines,
            'summary_lines': summary_lines,
            'uncertain': img.get('uncertain') or [],
            'segment_mode': bool(img.get('segment_mode')),
            'segments': img.get('segments') or [],
            'size': img.get('size'),
        })
    for gif in raw_data.get('gifs', []) or []:
        text = (gif.get('deduped_text') or '').strip()
        if not text:
            continue
        lines = clean_lines(text)
        if not lines:
            continue
        image_type = guess_image_type('\n'.join(lines))
        summary_lines = build_summary_for_type(image_type, lines)
        full_lines = build_fulltext_for_type(image_type, lines)
        blocks.append({
            'kind': 'gif',
            'index': gif.get('index'),
            'source': gif.get('url') or '',
            'image_type': image_type,
            'type_label': TYPE_LABELS.get(image_type, TYPE_LABELS['unknown']),
            'lines': lines,
            'full_lines': full_lines,
            'summary_lines': summary_lines,
            'uncertain': gif.get('uncertain') or [],
            'segment_mode': False,
            'segments': gif.get('frames') or [],
            'size': None,
        })
    return blocks


def summarize_text(lines, limit=4):
    candidates = extract_candidate_lines(lines, min_score=4)
    if not candidates:
        candidates = extract_candidate_lines(lines, min_score=3)
    return candidates[:limit]


def build_overview(raw_data, image_blocks):
    overview = []
    title = raw_data.get('page', {}).get('title', '').strip()
    if title:
        overview.append(f'标题：{title}')
    body_text = (raw_data.get('body_text') or '').strip()
    if body_text:
        body_lines = clean_lines(body_text)
        top = summarize_text(body_lines, limit=3)
        if top:
            overview.append('正文要点：' + '；'.join(top))
    if image_blocks:
        type_counter = Counter(block['type_label'] for block in image_blocks)
        overview.append('图片信息类型：' + '、'.join([f"{k}×{v}" for k, v in type_counter.items()]))
    return overview


def build_markdown(title: str, body_text: str, image_blocks, uncertain_notes):
    parts = []
    if title:
        parts.append(f'# {title}')
        parts.append('')

    parts.append('## 概览')
    overview = build_overview({'page': {'title': title}, 'body_text': body_text}, image_blocks)
    if overview:
        for item in overview:
            parts.append(f'- {item}')
    else:
        parts.append('- 已完成可见文本提取与整理。')
    parts.append('')

    if body_text:
        parts.append('## 正文主线')
        parts.append(body_text)
        parts.append('')

    if image_blocks:
        parts.append('## 图片补充信息（摘要层）')
        for block in image_blocks:
            parts.append(f"### 图片 {block['index']}｜{block['type_label']}")
            if block['source']:
                parts.append(f"- 来源：{block['source']}")
            if block.get('size'):
                parts.append(f"- 尺寸：{block['size'].get('width', 0)}x{block['size'].get('height', 0)}")
            if block.get('segment_mode'):
                parts.append('- 处理方式：分段 OCR')
            if block['summary_lines']:
                for line in block['summary_lines']:
                    parts.append(f'- {line}')
            elif block['full_lines']:
                for line in block['full_lines'][:6]:
                    parts.append(f'- 全文摘录：{line}')
            else:
                parts.append('- 未提取到足够清晰的有效文字。')
            parts.append('')

        parts.append('## 图片逐张完整提取（全文层）')
        for block in image_blocks:
            parts.append(f"### 图片 {block['index']}｜{block['type_label']}")
            if block['source']:
                parts.append(f"- 来源：{block['source']}")
            if block.get('size'):
                parts.append(f"- 尺寸：{block['size'].get('width', 0)}x{block['size'].get('height', 0)}")
            if block.get('segment_mode'):
                parts.append('- 处理方式：分段 OCR')
            if block['full_lines']:
                parts.extend(block['full_lines'])
            else:
                parts.append('(未提取到足够清晰的有效文字)')
            parts.append('')

    if uncertain_notes:
        parts.append('## 不确定信息')
        for note in uncertain_notes:
            parts.append(f'- {note}')
        parts.append('')

    parts.append('## 小结')
    if image_blocks:
        parts.append('这份结果同时保留了摘要层与全文层；当图片信息密集时，优先保留逐图完整提取，再在摘要层归纳高价值信息。')
    else:
        parts.append('这份结果以正文提取为主，已尽量清理噪声并保留主要信息。')
    parts.append('')
    return '\n'.join(parts).strip() + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-json', required=True)
    ap.add_argument('--title', default='')
    ap.add_argument('--body-text', default='')
    ap.add_argument('--output-json')
    ap.add_argument('--output-markdown')
    args = ap.parse_args()

    data = json.loads(Path(args.input_json).read_text(encoding='utf-8'))
    title = args.title or data.get('page', {}).get('title', '')
    body_lines = clean_lines(args.body_text or data.get('body_text', ''))
    body_text = '\n'.join(body_lines).strip()

    image_blocks = group_image_blocks(data)
    uncertain_notes = []
    uncertain_notes.extend(data.get('uncertain') or [])
    for block in image_blocks:
        for note in block.get('uncertain') or []:
            if note not in uncertain_notes:
                uncertain_notes.append(note)

    clean_markdown = build_markdown(title, body_text, image_blocks, uncertain_notes)
    out = {
        'clean_markdown': clean_markdown,
        'structured_blocks': {
            'title': title,
            'body_text': body_text,
            'image_blocks': image_blocks,
        },
        'raw_ocr_candidates': data,
    }
    if args.output_json:
        Path(args.output_json).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    if args.output_markdown:
        Path(args.output_markdown).write_text(out['clean_markdown'], encoding='utf-8')
    if not args.output_json and not args.output_markdown:
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
