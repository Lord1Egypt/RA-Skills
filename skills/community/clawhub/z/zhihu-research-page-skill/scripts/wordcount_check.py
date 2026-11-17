# -*- coding: utf-8 -*-
"""字数核验 + <code> 标签完整性自检脚本
用法: python scripts/wordcount_check.py <文件路径>  # 给定文件
      python scripts/wordcount_check.py               # 自动扫 ./other/_draft_*.html
在 Phase 5.2 每个写作 agent 写完草稿后运行，两种检查全部通过才算完成。
"""
import re, sys, glob, os

BLOCK_TAGS = {'p','table','div','h3','h4','h5','blockquote','ul','ol'}

def valid_chars(text):
    t = re.sub(r'<script.*?</script>', '', text, flags=re.S)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t)
    cn = len(re.findall(r'[\u4e00-\u9fff]', t))
    pn = len(re.findall(r'[\u3000-\u303f\uff00-\uffef]', t))
    return cn + pn

def check_code_tags(html, filepath):
    """检查 <code> 标签完整性，失败返回错误消息列表"""
    errors = []
    opens = len(re.findall(r'<\s*code[^>]*>', html, re.I))
    closes = len(re.findall(r'</\s*code\s*>', html, re.I))
    if opens != closes:
        errors.append(f"<code> 开 {opens} != 闭 {closes}，差额 {opens-closes}")
    for m in re.finditer(r'<\s*code[^>]*>(.*?)</\s*code\s*>', html, re.S|re.I):
        inner = m.group(1)
        for tag in BLOCK_TAGS:
            if re.search(rf'<\s*{tag}[\s>]', inner, re.I):
                errors.append(f"<code> 内嵌套块级 <{tag}> —— 会导致等宽字体泄漏")
                break
    return errors

def main():
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        targets = glob.glob('./other/_draft_*.html') + glob.glob('./other/_draft_ch_*.html')
        if not targets:
            targets = glob.glob('_draft_*.html') + glob.glob('_draft_ch_*.html')

    if not targets:
        print("[跳过] 未找到草稿文件"); return 0

    all_ok = True
    for fp in targets:
        if not os.path.exists(fp): continue
        html = open(fp, encoding='utf-8', errors='ignore').read()
        vc = valid_chars(html)
        print(f"[{fp}] 有效中文字数: {vc}")
        if vc < 11000:
            print(f"  ❌ 不足 11,000 字 (差 {11000-vc})")
            all_ok = False

        errors = check_code_tags(html, fp)
        if errors:
            for e in errors: print(f"  ❌ {e}")
            all_ok = False
        else:
            print(f"  ✅ <code> 标签检查通过")

    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
