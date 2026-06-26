# -*- coding: utf-8 -*-
"""检查所有JSON文件的质量问题"""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

output_dir = Path(r"D:\有斐家\小一\常用规范处理成果")

# 检测英文粘连 (中文后直接跟英文单词，无空格)
EN_GLUE_RE = re.compile(r'[\u4e00-\u9fff][a-zA-Z]')

# 检测章节标题混入末尾
# 如 "3基本规定3.1一般规定" 或 "5.2材料要求"
CHAPTER_TAIL_RE = re.compile(r'[\u4e00-\u9fff]\d{1,2}[\.\s]*\d{0,2}[\.\s]*\d{0,2}[\u4e00-\u9fff].{0,20}$')

# 检测符号表特征 (大量符号=, 如 "Fwk", "NGk", "Nad"等)
SYMBOL_DENSE_RE = re.compile(r'(?:[A-Z][a-z]?[a-z]?\s*[=，,、；;]|(?:[A-Z][\w]*[a-z][\w]*[，,、；;])){3,}')

# 检测纯符号罗列 (没有中文的行)
MOSTLY_SYMBOL_RE = re.compile(r'^[A-Za-z\d\.\s\+\-\=\/\(\)，,、；;：:＞≥＜≤∑μγφψλβπαεδ]+')

# 超长条文
TOO_LONG = 300

# 超短条文
TOO_SHORT = 5

for jf in sorted(output_dir.glob("*.json")):
    d = json.load(open(str(jf), encoding='utf-8'))
    arts = d.get('articles', {})
    report = d.get('report', {})
    
    if report.get('total', 0) == 0:
        print(f"\n{'='*60}")
        print(f"❌ {jf.stem} — 0条 (无法提取)")
        continue
    
    print(f"\n{'='*60}")
    print(f"📄 {jf.stem} — {report['total']}条")
    
    issues = {
        'en_glue': [],       # 中英文粘连
        'symbol_dense': [],  # 符号表/密集符号
        'chapter_tail': [],  # 末尾混入章节标题
        'too_long': [],      # 过长
        'too_short': [],     # 过短
        'ocr_error': [],     # OCR错误
        'no_chinese': [],    # 无中文
    }
    
    for aid, info in sorted(arts.items()):
        text = info['text']
        tlen = len(text)
        
        # 中英文粘连
        if EN_GLUE_RE.search(text):
            issues['en_glue'].append((aid, tlen))
        
        # 符号密集
        if SYMBOL_DENSE_RE.search(text):
            issues['symbol_dense'].append((aid, tlen))
        
        # 末尾混入章节标题
        if CHAPTER_TAIL_RE.search(text) and tlen > 50:
            tail = CHAPTER_TAIL_RE.search(text).group()
            issues['chapter_tail'].append((aid, tail))
        
        # 过长
        if tlen > TOO_LONG:
            issues['too_long'].append((aid, tlen))
        
        # 过短
        if tlen < TOO_SHORT:
            issues['too_short'].append((aid, tlen))
        
        # OCR错误
        if info.get('quality') == 'ocr_error':
            issues['ocr_error'].append((aid, tlen))
        
        # 无中文
        if not re.search(r'[\u4e00-\u9fff]', text):
            issues['no_chinese'].append((aid, text[:50]))
    
    has_issue = False
    labels = {
        'en_glue': '🔤 中英文粘连',
        'symbol_dense': '📐 符号表/密集符号',
        'chapter_tail': '📑 末尾混入章节标题',
        'too_long': '📏 过长(>300字)',
        'too_short': '⚠️ 过短(<5字)',
        'ocr_error': '🔍 OCR错误',
        'no_chinese': '🚫 无中文',
    }
    for key, label in labels.items():
        items = issues[key]
        if items:
            has_issue = True
            print(f"  {label}: {len(items)}条")
            if key == 'chapter_tail':
                for aid, tail in items[:5]:
                    print(f"    {aid}: ...{tail}")
                if len(items) > 5:
                    print(f"    ... 还有{len(items)-5}条")
            elif key == 'too_long':
                items.sort(key=lambda x: -x[1])
                for aid, tlen in items[:5]:
                    print(f"    {aid}: {tlen}字")
                if len(items) > 5:
                    print(f"    ... 还有{len(items)-5}条")
            elif key == 'too_short':
                for aid, tlen in items[:5]:
                    print(f"    {aid}: {tlen}字")
            elif key == 'no_chinese':
                for aid, txt in items[:3]:
                    print(f"    {aid}: {txt}")
            elif key in ('en_glue', 'symbol_dense', 'ocr_error'):
                ids = [x[0] for x in items[:10]]
                print(f"    {', '.join(ids)}")
                if len(items) > 10:
                    print(f"    ... 还有{len(items)-10}条")
    
    if not has_issue:
        print(f"  ✅ 无问题")
