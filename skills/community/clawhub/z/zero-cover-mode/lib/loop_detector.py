"""零稀泥模式 — 循环检测 loop_detector.py

检查最近 N 个修复中是否有重复模式。
使用 Jaccard 相似度（token 化）替代 SequenceMatcher，性能 O(n+m) 而非 O(n*m)。

Usage:
    python loop_detector.py check <ndjson_path> <bug_type> <root_cause>
    python loop_detector.py scan <ndjson_path>
"""

import json, sys, os, re, logging

from .config import LOOP_WINDOW_SIZE, LOOP_THRESHOLD, LOOP_SIM_THRESHOLD

log = logging.getLogger("loop")

# P2-5: 扩展高频词列表，降低 Jaccard 误判
# P1-6: 精简 _TEMPLATE_WORDS — 只保留真正无意义的通用词
# 注意：不要删除 "缺少""缺失""未" 等有语义的词，它们对差异度检测很重要
_TEMPLATE_WORDS = {
    "fix", "repair", "cause", "caused", "due", "because",
    "issue", "problem", "error", "bug", "result", "leads",
    "leading", "导致", "引起",
    # 以下高频词仅保留真正无意义的模板词
    "would", "could", "should", "always", "never",
    "default", "need",
    # 中文对等模板词 — 降低中文根因分析的 Jaccard 误判
    "会", "能", "应该", "总是", "从不",
    "可能", "需要", "必须",
    # P2: 补充缺失的高频中文无意义词
    "由于", "因为", "因此", "其中",
    "之后", "同时", "方式", "方法",
}


def _normalize(text):
    """清洗根因文本：降维去噪"""
    t = text.lower()
    for word in _TEMPLATE_WORDS:
        t = re.sub(r'\b' + word + r'\b', '', t)
    t = re.sub(r'\b\d+[\.:]?\d*\b', '', t)
    t = re.sub(r'[\s]+', ' ', t).strip()
    return t


def _tokenize(text):
    """分词为 token 集合

    _normalize() 已移除 _TEMPLATE_WORDS 和数字，
    此处不再重复过滤（P3-v11.2-1: 移除冗余检查）。
    """
    t = _normalize(text)
    tokens = set()
    for word in re.findall(r'[a-z]{2,}|[\u4e00-\u9fff]', t.lower()):
        tokens.add(word)
    # P1-6: 如果清洗后 token < 3，回退到原始文本重新分词
    if len(tokens) < 3:
        t2 = text.lower()
        for word in _TEMPLATE_WORDS:
            t2 = re.sub(r'\b' + word + r'\b', '', t2)
        t2 = re.sub(r'\b\d+[\.:]?\d*\b', '', t2)
        tokens = set(re.findall(r'[a-z]{2,}|[\u4e00-\u9fff]', t2))
        # P2-F: 回退后仍然空集，返回空集（Jaccard 默认防御为 0.0）
        if not tokens:
            return set()
    return tokens


def text_similarity(a, b):
    """Jaccard 相似度（基于 token 集合）

    P2-4: 从 O(n*m) SequenceMatcher 替换为 O(|A|+|B|) Jaccard，
    对中文和英文都有效。

    如果任意一方 token 集为空，返回 0.0 表示不相似
    （而非返回 1.0 误判为完全相同）—— P1-6 修正。
    """
    tokens_a = _tokenize(a)
    tokens_b = _tokenize(b)
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def detect_loop(ndjson_path, bug_type, root_cause,
                window=LOOP_WINDOW_SIZE, threshold=LOOP_THRESHOLD,
                sim_threshold=LOOP_SIM_THRESHOLD):
    """
    检查最近 window 条记录中同 bug_type 的出现次数和根因相似度。
    """
    if not os.path.exists(ndjson_path):
        result = {"loop_detected": False, "triggered": False,
                  "error": "ndjson not found"}
        from .contracts import LoopDetectionResult
        try:
            LoopDetectionResult(**result)
        except Exception as e:
            log.warning("LoopDetectionResult 契约校验失败: %s", e)
        return result

    with open(ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = [l.strip() for l in f if l.strip()]

    recent = []
    for line in lines[-window:]:
        try:
            recent.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    same_type = [r for r in recent if r.get("bug_type") == bug_type]

    if len(same_type) >= threshold:
        scores = [text_similarity(r.get("root_cause", ""), root_cause)
                  for r in same_type]
        max_sim = max(scores) if scores else 0
        if max_sim >= sim_threshold:
            result = {
                "loop_detected": True,
                "same_type_count": len(same_type),
                "max_similarity": round(max_sim, 3),
                "triggered": True,
            }
            from .contracts import LoopDetectionResult
            try:
                LoopDetectionResult(**result)
            except Exception as e:
                log.warning("LoopDetectionResult 契约校验失败: %s", e)
            return result

    result = {"loop_detected": False, "triggered": False,
              "same_type_count": len(same_type)}
    # 返回值通过 Pydantic 契约校验
    from .contracts import LoopDetectionResult
    try:
        LoopDetectionResult(**result)
    except Exception as e:
        log.warning("LoopDetectionResult 契约校验失败: %s", e)
    return result


def scan_all(ndjson_path, window=LOOP_WINDOW_SIZE, threshold=LOOP_THRESHOLD,
             sim_threshold=LOOP_SIM_THRESHOLD):
    """扫描整个 ndjson，找出所有循环模式"""
    if not os.path.exists(ndjson_path):
        return []

    with open(ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = [l.strip() for l in f if l.strip()]

    records = []
    for line in lines:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    alerts = []
    for i in range(len(records)):
        start = max(0, i - window)
        batch = records[start:i]
        bug_type = records[i].get("bug_type", "")
        root_cause = records[i].get("root_cause", "")
        same_type = [r for r in batch if r.get("bug_type") == bug_type]
        if len(same_type) >= threshold - 1:
            scores = [text_similarity(r.get("root_cause", ""), root_cause)
                      for r in same_type]
            if scores and max(scores) >= sim_threshold:
                alerts.append({
                    "index": i,
                    "bug_id": records[i].get("bug_id", ""),
                    "bug_type": bug_type,
                    "same_type_count": len(same_type) + 1,
                    "max_similarity": round(max(scores), 3),
                })
    return alerts


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="循环检测器")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check", help="检查特定记录是否循环")
    p.add_argument("ndjson_path", nargs="?", default="FIX_CLOSURE_LOG.ndjson")
    p.add_argument("bug_type")
    p.add_argument("root_cause")

    p = sub.add_parser("scan", help="全量扫描循环模式")
    p.add_argument("ndjson_path", nargs="?", default="FIX_CLOSURE_LOG.ndjson")

    args = parser.parse_args()

    try:
        if args.command == "check":
            result = detect_loop(args.ndjson_path, args.bug_type, args.root_cause)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == "scan":
            alerts = scan_all(args.ndjson_path)
            if alerts:
                print(f"发现 {len(alerts)} 个循环模式:")
                for a in alerts:
                    print(f"  #{a['index']} {a['bug_id']}: "
                          f"{a['bug_type']} x{a['same_type_count']} "
                          f"(sim={a['max_similarity']})")
            else:
                print("OK: 未发现循环模式")
    except Exception as e:
        log.error("执行失败: %s", e)
        sys.exit(1)
