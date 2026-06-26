# -*- coding: utf-8 -*-
"""
清洗JSON条文文本：去除换行符、页眉页尾垃圾、多余空白。
输出干净的纯文本，适合向量化检索。
"""
import json, re, sys, os
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# 常见页眉页脚/水印垃圾
JUNK_PATTERNS = [
    r'www\.\w+\.com',
    r'浏览专用',
    r'息公',
    r'住房城乡建设部公告',
    r'中华人民共和国.*?(标准|行业|规范|规程)',
    r'JGJ\s*\d+[-—]\d+',
    r'JTG\s*\w+[-—]\d+',
    r'JT\s*/?\s*T\s*\d+[-—]\d+',
    r'GB\s*\d+[-—~]\d+',
    r'GB/T\s*\d+[-—]\d+',
    r'TSG\s*\d+[-—]\d+',
    r'公路工程施工安全技术规范\(JTG\s*\w+[-——]\d+\)',
    r'公路隧道施工技术规范',
    r'建筑施工.*?安全技术',
    r'\d{4}[-—]\d{2}[-—]\d{2}',
]

JUNK_RE = [re.compile(p) for p in JUNK_PATTERNS]


def clean_text(text):
    """清洗单条条文文本"""
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 跳过匹配垃圾模式的行
        is_junk = False
        for pat in JUNK_RE:
            if pat.fullmatch(line) or (len(line) < 40 and pat.search(line) and len(pat.search(line).group()) > len(line) * 0.5):
                is_junk = True
                break
        if is_junk:
            continue
        cleaned.append(line)
    
    result = ''.join(cleaned)
    # 多余空白合并
    result = re.sub(r'\s+', ' ', result).strip()
    return result


def process_file(json_path):
    d = json.load(open(json_path, encoding='utf-8'))
    arts = d['articles']
    changed = 0
    
    for aid, info in arts.items():
        old = info['text']
        new = clean_text(old)
        if new != old:
            info['text'] = new
            changed += 1
            # 重新评估quality
            from extract_regulation import has_ocr_errors
            info['quality'] = 'clean' if not has_ocr_errors(new) else 'ocr_error'
    
    # 重新生成report
    from extract_regulation import validate
    d['report'] = validate(arts)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    
    return changed, len(arts), d['report']


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='JSON file or directory')
    args = parser.parse_args()
    
    p = Path(args.input)
    files = sorted(p.glob('*.json')) if p.is_dir() else [p]
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    
    total_changed = 0
    total_articles = 0
    for jf in files:
        changed, total, report = process_file(str(jf))
        total_changed += changed
        total_articles += total
        print(f"  {jf.name}: {changed}/{total} cleaned, {report['total']} articles")
    
    print(f"\nDone: {len(files)} files, {total_changed}/{total_articles} articles cleaned")


if __name__ == '__main__':
    main()
