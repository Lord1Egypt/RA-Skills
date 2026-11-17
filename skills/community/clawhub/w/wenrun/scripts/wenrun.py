#!/usr/bin/env python3
"""
文润 (wenrun) — 中文AI文本自然度检测工具

用法:
    python3 scripts/wenrun.py analyze --text "要检测的文本"
    python3 scripts/wenrun.py analyze --file article.txt
    python3 scripts/wenrun.py analyze --file article.txt --verbose
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FEATURES_PATH = BASE_DIR / "features" / "ai-patterns.json"

# Severity → deduction mapping
SEVERITY_PENALTY = {"high": 6, "medium": 3, "low": 1}


def load_patterns():
    """加载特征库"""
    if not FEATURES_PATH.exists():
        print(f"❌ 特征库未找到: {FEATURES_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(FEATURES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def scan_text(text: str, patterns: list) -> list:
    """对文本运行 keyword 和 regex 类型的模式匹配"""
    findings = []
    text_len = len(text)
    
    for p in patterns:
        ptype = p.get("type", "keyword")
        pid = p["id"]
        pat_str = p["pattern"]
        severity = p.get("severity", "medium")
        note = p.get("note", "")
        
        if ptype == "keyword":
            # Simple substring search
            pat = re.escape(pat_str)
            matches = list(re.finditer(pat, text, re.IGNORECASE))
            for m in matches:
                findings.append({
                    "pattern_id": pid,
                    "pattern": pat_str,
                    "severity": severity,
                    "note": note,
                    "position": m.start(),
                    "context": _get_context(text, m.start(), m.end()),
                })
                
        elif ptype == "keyword_context":
            # Only flag if pattern density exceeds threshold
            pat = re.escape(pat_str)
            matches = list(re.finditer(pat, text, re.IGNORECASE))
            density = len(matches) / max(1, text_len / 500)  # per 500 chars
            if density > 2:
                for m in matches:
                    findings.append({
                        "pattern_id": pid,
                        "pattern": pat_str,
                        "severity": severity,
                        "note": f"{note} (密度: {density:.1f}x/500字)",
                        "position": m.start(),
                        "context": _get_context(text, m.start(), m.end()),
                    })
                    
        elif ptype == "regex":
            try:
                matches = list(re.finditer(pat_str, text, re.IGNORECASE))
                for m in matches:
                    findings.append({
                        "pattern_id": pid,
                        "pattern": pat_str,
                        "severity": severity,
                        "note": note,
                        "position": m.start(),
                        "context": _get_context(text, m.start(), m.end()),
                    })
            except re.error:
                pass  # Skip invalid regex
        
    return findings


def analyze_statistical(text: str) -> list:
    """统计分析：段落结构、词汇密度、语气特征"""
    findings = []
    lines = text.strip().split('\n')
    paragraphs = [l.strip() for l in text.split('\n\n') if l.strip()]
    sentences = [s.strip() for s in re.split(r'[。！？\n]', text) if s.strip()]
    
    if not paragraphs or not sentences:
        return findings
    
    # PS-01: Paragraph length uniformity
    if len(paragraphs) >= 3:
        plens = [len(p) for p in paragraphs]
        avg = sum(plens) / len(plens)
        std_dev = (sum((l - avg) ** 2 for l in plens) / len(plens)) ** 0.5
        cv = std_dev / avg if avg > 0 else 0
        if cv < 0.3:
            findings.append({
                "pattern_id": "PS-01",
                "pattern": "[统计]段落长度趋同",
                "severity": "medium",
                "note": f"各段落长度的变异系数={cv:.2f} (<0.3表示过于规整)",
                "position": 0,
                "context": f"段落长度: {plens}"
            })
    
    # PS-04: No short paragraphs
    if len(paragraphs) >= 4:
        short_count = sum(1 for p in paragraphs if len(p) < 50)
        if short_count == 0:
            findings.append({
                "pattern_id": "PS-04",
                "name": "缺少短段落",
                "severity": "low",
                "note": "全文没有短段落（<50字），缺少节奏变化",
                "position": 0,
                "context": f"最长段={max(len(p) for p in paragraphs)}, 最短段={min(len(p) for p in paragraphs)}"
            })
    
    # M-02: No rhetorical questions (反问句)
    rhetorical = len(re.findall(r'难道|怎么不|怎能|哪能|何尝', text))
    if rhetorical == 0 and len(sentences) > 15:
        findings.append({
            "pattern_id": "M-02",
            "pattern": "[统计]缺少反问句",
            "severity": "medium",
            "note": f"全文{sentences}句，没有反问句。AI文本极少使用反问",
            "position": 0,
            "context": f"反问句数=0"
        })
    
    # M-04: No colloquial expressions
    colloquial = len(re.findall(r'嘛|呗|啦|哟|哈|嗯|哦|咦|噗', text))
    if colloquial == 0 and len(text) > 300:
        findings.append({
            "pattern_id": "M-04",
            "pattern": "[统计]缺少口语化表达",
            "severity": "medium",
            "note": "全文没有语气词（嘛呗啦等），AI文本倾向全篇正式",
            "position": 0,
            "context": f"口语词数=0"
        })
    elif colloquial < 3 and len(text) > 300:
        findings.append({
            "pattern_id": "M-04",
            "pattern": "[统计]口语化表达偏少",
            "severity": "low",
            "note": f"全文仅{colloquial}个口语词，AI文本倾向于过度正式",
            "position": 0,
            "context": f"口语词数={colloquial}"
        })
    
    # S-04: 的 density
    de_count = len(re.findall(r'的', text))
    de_ratio = de_count / max(1, len(text)) * 100
    if de_ratio > 8:
        findings.append({
            "pattern_id": "S-04",
            "pattern": "[统计]的密度偏高",
            "severity": "low",
            "note": f"的占比={de_ratio:.1f}% (>8%可能偏AI)",
            "position": 0,
            "context": f"的/{len(text)}字={de_count}/{len(text)}"
        })
    
    # M-05: Perfect formality (感叹号使用异常)
    excl = len(re.findall(r'！', text))
    excl_ratio = excl / max(1, len(sentences)) * 100
    if excl_ratio < 2 and len(text) > 500:
        findings.append({
            "pattern_id": "M-05",
            "pattern": "[统计]感叹号使用过少",
            "severity": "low",
            "note": f"感叹号仅{excl}个（{excl_ratio:.0f}%句子），情感表达缺失",
            "position": 0,
            "context": f"!数={excl} / 句数={len(sentences)}"
        })
    
    # S-06: 这 density
    zhe_count = len(re.findall(r'这是一种|这是一个|这意味着', text))
    zhe_ratio = zhe_count / max(1, len(text)) * 1000
    if zhe_ratio > 3:
        findings.append({
            "pattern_id": "S-06",
            "pattern": "[统计]这字密度过高",
            "severity": "low",
            "note": f"'这是一种/这是一个/这意味着' 出现{zhe_count}次",
            "position": 0,
            "context": f"这式句={zhe_count}"
        })
    
    # Sentence length variance
    if len(sentences) >= 5:
        slens = [len(s) for s in sentences if len(s) > 5]
        if slens:
            s_avg = sum(slens) / len(slens)
            s_std = (sum((l - s_avg) ** 2 for l in slens) / len(slens)) ** 0.5
            s_cv = s_std / s_avg if s_avg > 0 else 0
            if s_cv < 0.4:
                findings.append({
                    "pattern_id": "PS-03",
                    "pattern": "[统计]句子长度趋同",
                    "severity": "medium",
                    "note": f"句子长度变异系数={s_cv:.2f} (<0.4说明句式单一)",
                    "position": 0,
                    "context": f"句长变异系数={s_cv:.2f}"
                })
    
    return findings


def _get_context(text: str, start: int, end: int, width: int = 25) -> str:
    """提取匹配位置的上下文"""
    ctx_start = max(0, start - width)
    ctx_end = min(len(text), end + width)
    prefix = "..." if ctx_start > 0 else ""
    suffix = "..." if ctx_end < len(text) else ""
    return prefix + text[ctx_start:ctx_end].replace('\n', ' ') + suffix


def compute_scores(findings_text, findings_stat, categories, style_mode='auto'):
    """计算各维度和综合评分，支持文体上下文的权重调整"""
    data = load_patterns()
    style_config = data.get('style_config', {})
    modes = style_config.get('modes', {})
    
    # Determine effective style mode
    if style_mode == 'auto':
        # Auto-detect: check text characteristics
        # Simple heuristic: if 第一/第二/第三 density is high → academic
        counted = sum(1 for f in findings_text if f.get('pattern_id') in ('T-01','T-02','T-04','T-05','T-06'))
        if counted > 5:
            effective_mode = 'academic'
        elif any(f.get('severity') == 'high' and f.get('category', '') == 'EXCESSIVE_POLITE' for f in findings_text):
            effective_mode = 'marketing'
        else:
            effective_mode = 'casual'
    else:
        effective_mode = style_mode if style_mode in modes else 'casual'
    
    mode_config = modes.get(effective_mode, {'adjustments': {'default': 1.0}})
    adjustments = mode_config.get('adjustments', {})
    default_adj = adjustments.get('default', 1.0)
    
    # Build mappings
    cat_weights = {c['id']: c['weight'] for c in categories}
    cat_names = {c['id']: c['name'] for c in categories}
    pat_to_cat = {}
    pat_style = {}
    for c in categories:
        for p in c['patterns']:
            pat_to_cat[p['id']] = c['id']
            pat_style[p['id']] = p.get('style_mode', 'casual')
    
    # Score per category
    cat_scores = {}
    cat_details = {}
    
    for c in categories:
        cid = c['id']
        triggered = [f for f in findings_text if f.get('pattern_id') in pat_to_cat and pat_to_cat[f['pattern_id']] == cid]
        triggered += [f for f in findings_stat if f.get('pattern_id') in pat_to_cat and pat_to_cat[f['pattern_id']] == cid]
        
        penalty = 0
        for f in triggered:
            pid = f.get('pattern_id', '')
            sev = f.get('severity', 'low')
            base = SEVERITY_PENALTY.get(sev, 1)
            # Apply style adjustment based on pattern's style_mode
            p_style = pat_style.get(pid, 'casual')
            adj = adjustments.get(cid, default_adj)
            # Academic patterns get bigger reduction in academic mode
            if effective_mode == 'academic' and p_style == 'academic':
                adj = min(adj, 0.4)  # Academic patterns in academic mode: max 40% penalty
            penalty += base * adj
        
        score = max(0, 100 - int(penalty))
        cat_scores[cid] = score
        cat_details[cid] = {
            "name": cat_names.get(cid, cid),
            "score": score,
            "issues": len(triggered),
            "penalty": round(penalty, 1),
        }
    
    # Compute base weighted overall
    total_weight = sum(cat_weights.get(cid, 10) for cid in cat_scores)
    if total_weight == 0:
        overall = 100
    else:
        weighted = sum(cat_scores.get(cid, 100) * cat_weights.get(cid, 10) for cid in cat_scores)
        overall = weighted / total_weight
    
    # Synergy penalty: if multiple core categories are simultaneously flagged
    synergy = 0
    core_cats = ['TEMPLATE_STRUCTURE', 'BUZZWORD', 'TRANSITION']
    flagged_core = sum(1 for cid in core_cats if cat_scores.get(cid, 100) < 85)
    if flagged_core >= 2:
        synergy = flagged_core * 5  # -5 per flagged core category
        overall -= synergy
    
    # Red flag: if BUZZWORD score < 60 AND TEMPLATE_STRUCTURE score < 80 → clear AI signal
    buzz = cat_scores.get('BUZZWORD', 100)
    templ = cat_scores.get('TEMPLATE_STRUCTURE', 100)
    if buzz < 70 and templ < 85:
        overall -= 10
    if buzz < 50 and templ < 70:
        overall -= 15
    
    overall = max(0, min(100, overall))
    
    # Verdict (thresholds adjusted for academic mode)
    if effective_mode == 'academic':
        thresholds = [(85, '非常自然', '学术写作中无明显模板痕迹'), (70, '基本自然', '学术写作规范范围内'),
                      (55, '疑似AI', '部分表达有AI嫌疑'), (35, '明显AI', '大量AI特征')]
    else:
        thresholds = [(90, '非常自然', '文本无明显AI痕迹'), (75, '基本自然', '少数地方略带AI痕迹'),
                      (60, '疑似AI', '有多处AI文本特征'), (40, '明显AI', '大量AI文本特征')]
    
    verdict = '极可能AI'
    detail = '完全符合AI文本特征模式，建议重写'
    for threshold, v, d in thresholds:
        if overall >= threshold:
            verdict = v
            detail = d
            break
    
    return {
        "overall": round(overall, 1),
        "verdict": verdict,
        "detail": detail,
        "style_mode": effective_mode,
        "categories": cat_details,
    }


def analyze(text: str, verbose: bool = False, style_mode: str = 'auto') -> dict:
    """完整分析流程，支持文体上下文"""
    data = load_patterns()
    
    all_patterns = []
    for c in data['categories']:
        all_patterns.extend(c['patterns'])
    
    findings_text = scan_text(text, all_patterns)
    findings_stat = analyze_statistical(text)
    scores = compute_scores(findings_text, findings_stat, data['categories'], style_mode)
    
    return {
        "version": data['version'],
        "input_length": len(text),
        "scores": scores,
        "style_config": data.get('style_config', {}),
        "findings": {
            "text_patterns": findings_text,
            "statistical": findings_stat,
        },
        "total_findings": len(findings_text) + len(findings_stat),
    }


def format_report(result: dict, verbose: bool = False):
    """输出分析报告"""
    s = result['scores']
    findings_text = result['findings']['text_patterns']
    findings_stat = result['findings']['statistical']
    
    # Header
    print("=" * 55)
    print(f"  文润 (WenRun) v1.1.0 — AI文本自然度检测")
    print(f"  输入长度: {result['input_length']} 字")
    print("=" * 55)
    print()
    
    # Overall score
    if s.get('style_mode'):
        print(f"  文体模式: {s['style_mode']}")
    print(f"  结论: {s['verdict']} — {s['detail']}")
    print()
    
    # Category breakdown
    print(f"  ── 维度评分 ──")
    for cid, cd in sorted(s['categories'].items(), key=lambda x: x[1]['score']):
        bar = '█' * (cd['score'] // 10) + '░' * (10 - cd['score'] // 10)
        marker = '⚠' if cd['score'] < 80 else '✓'
        print(f"  {marker} {cd['name']:12s} {cd['score']:3d}/100 {bar} ({cd['issues']}项)")
    print()
    
    # Findings detail
    all_findings = sorted(findings_text + findings_stat, key=lambda x: -SEVERITY_PENALTY.get(x.get('severity', 'low'), 1))
    
    if all_findings:
        print(f"  ── 发现问题 ({len(all_findings)} 处) ──")
        for f in all_findings[:30]:  # Show top 30
            sev = f.get('severity', 'low')
            sev_label = {'high': '高', 'medium': '中', 'low': '低'}.get(sev, '低')
            ctx = f.get('context', '')
            note = f.get('note', '')
            print(f"  [{sev_label}] {ctx}")
            if note:
                print(f"       → {note}")
            print()
        
        if len(all_findings) > 30:
            print(f"  ... 还有 {len(all_findings) - 30} 处发现 (使用 --verbose 查看全部)")
            print()
    
    if not all_findings:
        print("  ✓ 未发现明显AI文本特征")
        print()
    
    # Footer
    print("=" * 55)
    print(f"  免责声明: 本工具分析仅供参考，不构成对AI检测结果的保证。")
    print()


def main():
    parser = argparse.ArgumentParser(description="文润 — 中文AI文本自然度检测")
    sub = parser.add_subparsers(dest="command", help="子命令")
    
    p_analyze = sub.add_parser("analyze", help="分析文本")
    p_analyze.add_argument("--text", "-t", help="直接输入文本")
    p_analyze.add_argument("--file", "-f", help="从文件读取文本")
    p_analyze.add_argument("--verbose", "-v", action="store_true", help="显示详细结果")
    p_analyze.add_argument("--style", "-s", choices=["auto", "academic", "casual", "marketing"],
                          default="auto", help="写作文体模式 (默认自动检测)")
    p_analyze.add_argument("--json", "-j", action="store_true", help="输出JSON格式")
    
    p_check = sub.add_parser("check", help="检查特征库状态")
    
    args = parser.parse_args()
    
    if args.command == "check":
        data = load_patterns()
        total = sum(len(c['patterns']) for c in data['categories'])
        sc = data.get('style_config', {})
        print(f"文润 v{data['version']}")
        print(f"特征库: {len(data['categories'])} 类, {total} 条规则")
        for c in data['categories']:
            academic_count = sum(1 for p in c['patterns'] if p.get('style_mode') == 'academic')
            universal_count = sum(1 for p in c['patterns'] if p.get('style_mode') == 'universal')
            mode_tag = f" (学术×{academic_count} 通用×{universal_count})" if academic_count or universal_count else ""
            print(f"  {c['name']:12s} {len(c['patterns']):3d} 条  (权重={c['weight']}){mode_tag}")
        if sc.get('modes'):
            print(f"文体模式: {', '.join(sc['modes'].keys())}")
            for mk, mv in sc['modes'].items():
                print(f"    {mk:12s} {mv['label']}")
        return
    
    if args.command == "analyze":
        text = None
        if args.text:
            text = args.text
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            # Read from stdin
            text = sys.stdin.read().strip()
        
        if not text:
            print("❌ 请提供要分析的文本 (--text 或 --file)")
            sys.exit(1)
        
        result = analyze(text, verbose=args.verbose, style_mode=args.style)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            format_report(result, verbose=args.verbose)
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
