"""零稀泥模式 — 根因深度验证器 root_cause_validator.py

自动检查 BUG_ROOT_CAUSE.md 的 5-Whys 深度。

Usage:
    python root_cause_validator.py check <file_path>
    python root_cause_validator.py audit <directory>
"""

import re, sys, os, logging

from .config import SKILL_VERSION, ROOT_CAUSE_MIN_LEVEL

log = logging.getLogger("root_cause")

# P1-6: 共享中英文标签常量，LEVEL_PATTERNS 和 _has_content_after 共用
_LEVEL_LABELS = r'(?:L[1-4]|现象层|直接原因|深层原因|根本原因|Phenomenon|Direct\s+cause|Deep\s+cause|Root\s+cause|Level\s+[1-4]|第[1-4]层|第一[二三四]层|表层现象|直接症状|观察结果|直接诱因|代码路径|设计缺失|架构原因|系统性原因|流程原因)'

# P3-4: 增强正则，支持更多 Markdown 格式和中英文标签
LEVEL_PATTERNS = {
    "L1": re.compile(
        r'(?:^|(?<=\n))(?:#{1,3}\s+|>\s+|\-\s+|\*\s+|\+\s+)'
        r'(?:L1|现象层|Phenomenon|Level\s+1|'
        r'第1层|第一层|表层现象|直接症状|观察结果)'
        r'(?:\s*[：:\|\-–\—]+\s*)',
        re.IGNORECASE,
    ),
    "L2": re.compile(
        r'(?:^|(?<=\n))(?:#{1,3}\s+|>\s+|\-\s+|\*\s+|\+\s+)'
        r'(?:L2|直接原因|Direct\s+cause|Level\s+2|'
        r'第2层|第二层|直接诱因|代码路径)'
        r'(?:\s*[：:\|\-–\—]+\s*)',
        re.IGNORECASE,
    ),
    "L3": re.compile(
        r'(?:^|(?<=\n))(?:#{1,3}\s+|>\s+|\-\s+|\*\s+|\+\s+)'
        r'(?:L3|深层原因|Deep\s+cause|Level\s+3|'
        r'第3层|第三层|设计缺失|架构原因)'
        r'(?:\s*[：:\|\-–\—]+\s*)',
        re.IGNORECASE,
    ),
    "L4": re.compile(
        r'(?:^|(?<=\n))(?:#{1,3}\s+|>\s+|\-\s+|\*\s+|\+\s+)'
        r'(?:L4|根本原因|Root\s+cause|Level\s+4|'
        r'第4层|第四层|系统性原因|流程原因)'
        r'(?:\s*[：:\|\-–\—]+\s*)',
        re.IGNORECASE,
    ),
}

# P5: 模块级预编译循环论证检测（热路径，避免每次调用 _has_content_after 重新编译 6 个正则）
_CIRCULAR_PATTERNS = [re.compile(p) for p in [
    r'同上', r'同上所[述示]', r'见上文',
    r'refer to above', r'same as above', r'as above',
]]


def _has_content_after(lines, found_pos):
    """检查标题后是否有非空内容

    P0-F: 增加最小内容长度检查（≥5 中文字符或 ≥10 英文字符）
    和循环论证检测（"同上"、"同上所述"、"见上文" 等）。
    """
    _MIN_CONTENT_LEN = 5

    # 优先检查匹配行本身
    current = lines[found_pos].strip()
    # 去掉标题前缀标记（##, -, *, > 等）
    content_part = re.sub(r'^[#\s>\-\*\+\|]+', '', current).strip()
    # 去掉标签部分（L1:, 现象层: 等），检查后面是否有正文
    # P1-6: 使用共享 _LEVEL_LABELS 常量，避免重复定义
    label_removed = re.sub(r'^' + _LEVEL_LABELS + r'[\s—:\|\-–]*',
                           '', content_part, flags=re.IGNORECASE).strip()
    if label_removed:
        # P0-F: 检查最小长度
        if len(label_removed) < _MIN_CONTENT_LEN:
            pass  # fall through to subsequent line check
        # P0-F: 检查循环论证
        if any(p.search(label_removed) for p in _CIRCULAR_PATTERNS):
            return False
        # P5: 删除冗余条件 — 上一个 if 已确保 len >= _MIN_CONTENT_LEN
        return True

    # 检查后续非标题行
    for j in range(found_pos + 1, min(found_pos + 15, len(lines))):
        stripped = lines[j].strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|") if c.strip()]
            if any(len(c) > 1 for c in cells
                    if not c.startswith("-") and not c.startswith(":")):
                return True
        else:
            # P0-F: 检查后续行内容
            if len(stripped) < _MIN_CONTENT_LEN:
                continue
            if any(p.search(stripped) for p in _CIRCULAR_PATTERNS):
                continue
            return True
    return False


def check_depth(filepath):
    """检查 BUG_ROOT_CAUSE.md 的 5-Whys 深度"""
    if not os.path.exists(filepath):
        analysis = {
            "error": "file_not_found",
            "shallow": True,
            "blocking": True,
            "max_level": 0,
            "min_required": ROOT_CAUSE_MIN_LEVEL,
            "has_l4": False,
            "missing_levels": ["L1", "L2", "L3", "L4"],
            "details": {},
        }
        from .contracts import RootCauseAnalysis
        try:
            RootCauseAnalysis(**analysis)
        except Exception as e:
            log.warning("RootCauseAnalysis 契约校验失败: %s", e)
        return [], analysis

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    found = {}
    lines = content.split("\n")
    for level, pattern in LEVEL_PATTERNS.items():
        for i, line in enumerate(lines):
            if pattern.search(line):
                found[level] = _has_content_after(lines, i)
                break
        else:
            found[level] = False

    levels_found = sorted(found.keys(), key=lambda x: int(x[1:]))
    max_level = max((int(k[1:]) for k in found if found[k]), default=0)
    min_required = ROOT_CAUSE_MIN_LEVEL

    shallow = max_level < min_required
    missing = [f"L{l}" for l in range(1, 4)
               if f"L{l}" not in found or not found[f"L{l}"]
              ]

    analysis = {
        "max_level": max_level,
        "min_required": min_required,
        "shallow": shallow,
        "has_l4": found.get("L4", False),
        "missing_levels": missing,
        "details": {k: bool(v) for k, v in found.items()},
        "blocking": shallow,
    }
    # 返回值通过 Pydantic 契约校验
    from .contracts import RootCauseAnalysis
    try:
        RootCauseAnalysis(**analysis)
    except Exception as e:
        log.warning("RootCauseAnalysis 契约校验失败: %s", e)
    return levels_found, analysis


def audit_directory(bugs_base_dir):
    """扫描 bugs/ 下所有 {bug_id}/BUG_ROOT_CAUSE.md"""
    results = []
    if not os.path.isdir(bugs_base_dir):
        return results
    for entry in os.listdir(bugs_base_dir):
        candidate = os.path.join(bugs_base_dir, entry, "BUG_ROOT_CAUSE.md")
        if os.path.exists(candidate):
            levels, analysis = check_depth(candidate)
            results.append({
                "bug_id": entry,
                "path": candidate,
                "levels": levels,
                "analysis": analysis,
            })
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="根因深度验证器")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check", help="检查单个 BUG_ROOT_CAUSE.md")
    p.add_argument("file_path")

    p = sub.add_parser("audit", help="审计整个目录")
    p.add_argument("directory")

    args = parser.parse_args()

    try:
        if args.command == "check":
            levels, analysis = check_depth(args.file_path)
            max_l = analysis["max_level"]
            print(f"文件: {args.file_path}")
            print(f"发现层级: {', '.join(levels) if levels else '无'}")
            print(f"最大层级: L{max_l} (要求 >= L{analysis['min_required']})")
            if analysis["shallow"]:
                print(f"WARNING: 分析过浅 — 缺失 {analysis['missing_levels']}")
                print("blocking: true")
            else:
                print("OK: 深度达标")
            if analysis.get("has_l4"):
                print("INFO: 包含根本原因分析 (L4)")
            sys.exit(1 if analysis.get("blocking") else 0)

        elif args.command == "audit":
            results = audit_directory(args.directory)
            if not results:
                print(f"在 {args.directory} 中未找到 BUG_ROOT_CAUSE.md")
                sys.exit(0)
            print(f"审计 {len(results)} 个 BUG_ROOT_CAUSE.md:")
            for r in results:
                status = "OK" if not r["analysis"].get("shallow") else "SHALLOW"
                print(f"  [{status}] {r['bug_id']}: "
                      f"L{r['analysis']['max_level']} {r['levels']}")
            shallow = sum(1 for r in results if r["analysis"].get("shallow"))
            if shallow:
                print(f"\nWARNING: {shallow}/{len(results)} 个分析过浅")
            sys.exit(1 if shallow > 0 else 0)
    except Exception as e:
        log.error("执行失败: %s", e)
        sys.exit(1)
