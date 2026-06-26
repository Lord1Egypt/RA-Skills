# -*- coding: utf-8 -*-
"""
综合清洗脚本 v2：修复所有已知质量问题
1. 过滤符号表（2.2.x 类编号）
2. 修复中英文粘连 → 插入空格
3. 切除末尾章节标题
4. 切分过长条文（>300字）
5. 标记过短/无中文条文为skip
"""
import json, re, sys, os, copy
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
from extract_regulation import has_ocr_errors, validate

SKIP_KEYWORDS_IN_CHAPTER = ["符号", "符号和", "术语和符号"]

# ===== 修复函数 =====

def fix_en_glue(text):
    """中英文之间插入空格"""
    # 中文后紧跟英文
    text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z])', r'\1 \2', text)
    # 英文后紧跟中文
    text = re.sub(r'([a-zA-Z])([\u4e00-\u9fff])', r'\1 \2', text)
    # 中文后紧跟数字（但不是条文编号开头的情况）
    # text = re.sub(r'([\u4e00-\u9fff])(\d)', r'\1 \2', text)  # 这个太激进，暂不用
    return text


def fix_chapter_tail(text):
    """切除末尾混入的章节标题"""
    # 匹配末尾的 "数字+中文" 章节标题模式
    # 如 "3基本规定3.1一般规定" "11.1一般规定" "5.2 地基承载力计算"
    patterns = [
        # 多级章节拼接：...规定3.1一般规定 或 ...5.2材料要求
        re.compile(r'[\u4e00-\u9fff。，；](\d{1,2}[\.\s]*\d{0,2}[\.\s]*\d{0,2}[\u4e00-\u9fff][\u4e00-\u9fff\w\s]{2,25})$'),
        # 单级：...后接 "3基本规定"
        re.compile(r'[\u4e00-\u9fff。，；](\d{1,2}[\u4e00-\u9fff][\u4e00-\u9fff\w\s]{2,20})$'),
    ]
    for pat in patterns:
        m = pat.search(text)
        if m:
            text = text[:m.start()+1]
    return text.strip()


def split_long_text(text, max_len=300):
    """将过长条文按句号/分号切分为多段"""
    if len(text) <= max_len:
        return [text]
    
    # 按句号切分
    sentences = re.split(r'(。)', text)
    # 重新组合：保留句号
    parts = []
    current = ""
    for i in range(0, len(sentences)-1, 2):
        s = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else "")
        if len(current) + len(s) > max_len and current:
            parts.append(current)
            current = s
        else:
            current += s
    if sentences and len(sentences) % 2 == 1:
        current += sentences[-1]
    if current:
        parts.append(current)
    
    # 如果单句就超长，按分号再切
    final = []
    for part in parts:
        if len(part) <= max_len:
            final.append(part)
        else:
            subs = re.split(r'[；;]', part)
            cur = ""
            for sub in subs:
                if not sub:
                    continue
                sep = "；" if sub else ""
                if len(cur) + len(sub) + 1 > max_len and cur:
                    final.append(cur)
                    cur = sub
                else:
                    cur = cur + ("；" if cur else "") + sub
            if cur:
                final.append(cur)
    
    return final if final else [text]


def is_symbol_table(aid, info):
    """判断是否是符号表条目"""
    chapter = info.get('chapter', '')
    text = info['text']
    
    # chapter 包含"符号"
    if any(kw in chapter for kw in SKIP_KEYWORDS_IN_CHAPTER):
        # 但术语(2.1.x)保留，只有符号(2.2.x)过滤
        parts = aid.split('.')
        if len(parts) >= 2 and parts[1] == '2':
            return True
    
    # 文本本身是密集符号（很多大写字母+等号/分号的组合）
    symbol_matches = re.findall(r'[A-Z][a-z]?[a-z]?\s*[=，,、；;]', text)
    if len(symbol_matches) >= 5 and len(text) > 200:
        return True
    
    return False


def process_file(json_path, max_len=300):
    d = json.load(open(json_path, encoding='utf-8'))
    arts = d.get('articles', {})
    
    stats = {
        'total': len(arts),
        'skipped_symbol': 0,
        'skipped_short': 0,
        'skipped_no_chinese': 0,
        'fixed_glue': 0,
        'fixed_tail': 0,
        'split_long': 0,
        'final_count': 0,
    }
    
    new_arts = {}
    
    for aid, info in sorted(arts.items()):
        text = info['text']
        
        # 1. 过滤符号表
        if is_symbol_table(aid, info):
            stats['skipped_symbol'] += 1
            continue
        
        # 2. 过滤过短且无实质内容
        if len(text) < 5:
            stats['skipped_short'] += 1
            continue
        
        # 3. 过滤无中文
        if not re.search(r'[\u4e00-\u9fff]', text):
            stats['skipped_no_chinese'] += 1
            continue
        
        # 4. 修复中英文粘连
        new_text = fix_en_glue(text)
        if new_text != text:
            stats['fixed_glue'] += 1
            text = new_text
        
        # 5. 切除末尾章节标题
        new_text = fix_chapter_tail(text)
        if new_text != text:
            stats['fixed_tail'] += 1
            text = new_text
        
        # 6. 切分过长条文
        if len(text) > max_len:
            parts = split_long_text(text, max_len)
            if len(parts) > 1:
                stats['split_long'] += 1
                for pi, part in enumerate(parts):
                    new_id = f"{aid}.{chr(97+pi)}"  # 3.1.2.a, 3.1.2.b, ...
                    new_info = copy.deepcopy(info)
                    new_info['id'] = new_id
                    new_info['text'] = part
                    new_info['quality'] = 'clean' if not has_ocr_errors(part) else 'ocr_error'
                    new_arts[new_id] = new_info
                continue
        
        # 更新文本和质量
        info['text'] = text
        info['quality'] = 'clean' if not has_ocr_errors(text) else 'ocr_error'
        new_arts[aid] = info
    
    stats['final_count'] = len(new_arts)
    
    # 重新生成report
    report = validate(new_arts)
    d['articles'] = new_arts
    d['report'] = report
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    
    return stats


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='JSON file or directory')
    parser.add_argument('--maxlen', type=int, default=300, help='Max article length (default 300)')
    args = parser.parse_args()
    
    p = Path(args.input)
    files = sorted(p.glob('*.json')) if p.is_dir() else [p]
    
    total_stats = {
        'files': 0, 'total_in': 0, 'total_out': 0,
        'skipped_symbol': 0, 'skipped_short': 0, 'skipped_no_chinese': 0,
        'fixed_glue': 0, 'fixed_tail': 0, 'split_long': 0,
    }
    
    for jf in files:
        d = json.load(open(str(jf), encoding='utf-8'))
        if d.get('report', {}).get('total', 0) == 0:
            print(f"  SKIP {jf.name} (0 articles)")
            continue
        
        stats = process_file(str(jf), args.maxlen)
        
        for k in total_stats:
            if k in ('files', 'total_in', 'total_out'):
                continue
            total_stats[k] += stats.get(k, 0)
        total_stats['files'] += 1
        total_stats['total_in'] += stats['total']
        total_stats['total_out'] += stats['final_count']
        
        print(f"  {jf.name}: {stats['total']} → {stats['final_count']} "
              f"(skip: {stats['skipped_symbol']}符号+{stats['skipped_short']}短+{stats['skipped_no_chinese']}无中文, "
              f"fix: {stats['fixed_glue']}粘连+{stats['fixed_tail']}标题, "
              f"split: {stats['split_long']}长)")
    
    print(f"\n{'='*60}")
    print(f"总: {total_stats['files']}个文件, "
          f"{total_stats['total_in']} → {total_stats['total_out']}条 "
          f"(净{'+' if total_stats['total_out']>total_stats['total_in'] else ''}{total_stats['total_out']-total_stats['total_in']})")
    print(f"  跳过: {total_stats['skipped_symbol']}符号表 + {total_stats['skipped_short']}过短 + {total_stats['skipped_no_chinese']}无中文")
    print(f"  修复: {total_stats['fixed_glue']}粘连 + {total_stats['fixed_tail']}标题混入")
    print(f"  切分: {total_stats['split_long']}条过长条文")


if __name__ == '__main__':
    main()
