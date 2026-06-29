#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_link_validator.py - Step Link Validator v1.29.0
步骤衔接校验器：分析两个步骤之间的输入/输出匹配情况，
自动检测缺口并生成粘连点建议。

核心算法：
  1. 读取 step_A 的 produces 和 step_B 的 consumes
  2. 逐条匹配（类型匹配 + 语义关键词匹配）
  3. 计算匹配置信度
  4. 不匹配 → 生成 adhesion 构建建议

零外部依赖，仅使用 Python 标准库。
跨平台支持 Windows/Linux/macOS。
"""

import argparse
import json
import re
import sys
from pathlib import Path

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-sub/data/"
SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR.parent / ".standardization" / "skill-sub" / "data"


# ============================================================
# 类型匹配权重表
# ============================================================

# 兼容的类型对（A.produces.type → B.consumes.type 可匹配）
_TYPE_COMPATIBILITY = {
    "report":     ["report", "result", "data", "text"],
    "result":     ["result", "report", "data"],
    "data":       ["data", "result", "list", "param"],
    "file":       ["file", "path", "dir"],
    "path":       ["path", "dir", "file"],
    "dir":        ["dir", "path"],
    "config":     ["config", "param", "data"],
    "list":       ["list", "data", "text"],
    "json":       ["json", "data", "text", "config"],
    "markdown":   ["markdown", "text", "report"],
    "text":       ["text", "data"],
    "name":       ["name", "param"],
    "param":      ["param", "config", "data"],
    "url":        ["url", "text", "param"],
    "other":      ["other", "data", "text", "param"],
}

# 明确的缺口匹配词 — 产生词与消费词之间的语义关系
_PRODUCE_TO_CONSUME_SYNONYMS = [
    # 同义词对
    ("生成", "分析"), ("生成", "读取"), ("生成", "输入"),
    ("输出", "输入"), ("输出", "分析"), ("输出", "读取"),
    ("保存", "读取"), ("写入", "读取"), ("写入", "加载"),
    ("创建", "处理"), ("创建", "分析"),
    ("产生", "消费"), ("产生", "需要"),
    ("审查", "分析"), ("审查", "检测"),
    ("报告", "分析"), ("报告", "审查"),
    ("扫描", "分析"), ("扫描", "检测"),
    ("结果", "输入"), ("结果", "处理"),
    ("配置", "配置"), ("数据", "数据"),
    ("文件", "文件"), ("目录", "目录"),
    ("路径", "路径"), ("参数", "参数"),
]

# 明确的缺口触词 — 这些词出现在 produces/consumes 中时大概率需要粘连点
_GAP_TRIGGER_PRODUCES = ["报告", "结果", "文件"]
_GAP_TRIGGER_CONSUMES = ["配置", "参数", "格式"]


def validate_link(step_a_interface, step_b_interface, step_a_name="A", step_b_name="B"):
    """校验步骤 A 到步骤 B 的衔接

    参数：
        step_a_interface: dict — step_A 的 interface 字段（含 consumes/produces）
        step_b_interface: dict — step_B 的 interface 字段
        step_a_name: str — 步骤 A 的名称（用于输出）
        step_b_name: str — 步骤 B 的名称

    返回：
        dict — {
            "passed": bool,          # 是否通过
            "score": float,          # 总体匹配置信度 0.0~1.0
            "matched": list,         # 匹配项
            "mismatched": list,      # 不匹配项
            "gap_type": str,         # 缺口类型: "none" | "semantic" | "process" | "decision"
            "adhesion_suggestion": dict | None,  # 如果 mismatch，自动生成粘连点建议
        }
    """
    produces = step_a_interface.get("produces", [])
    consumes = step_b_interface.get("consumes", [])

    # 如果双方都没有 I/O 声明，无法分析
    if not produces and not consumes:
        return {
            "passed": True,
            "score": 0.5,
            "matched": [],
            "mismatched": [],
            "gap_type": "none",
            "note": "双方均未声明 I/O 接口，无法进行衔接分析",
            "adhesion_suggestion": None,
        }

    # 如果 B 没有 consumes，但 A 有 produces → trace 级匹配（视为 mild match）
    if not consumes and produces:
        return {
            "passed": True,
            "score": 0.6,
            "matched": [{"from": p.get("desc", "?"), "to": "(B 未声明输入)", "confidence": "trace"} for p in produces],
            "mismatched": [],
            "gap_type": "none",
            "note": "步骤 B 未声明输入，假设可接受步骤 A 的输出",
            "adhesion_suggestion": None,
        }

    # 如果 A 没有 produces → 无法确定 B 能消费什么
    if not produces and consumes:
        return {
            "passed": True,
            "score": 0.4,
            "matched": [],
            "mismatched": [{"from": "(A 未声明输出)", "to": c.get("desc", "?"), "confidence": "missing"} for c in consumes],
            "gap_type": "semantic",
            "note": "步骤 A 未声明输出，无法确认其是否能满足 B 的输入需求",
            "adhesion_suggestion": _build_adhesion_suggestion(
                gap_type="semantic",
                from_desc="(未知)",
                to_desc=consumes[0].get("desc", "?"),
                from_name=step_a_name,
                to_name=step_b_name,
            ),
        }

    # ---- 主匹配逻辑 ----
    matched = []
    mismatched = []

    # 遍历 A 的每个输出 vs B 的每个输入
    for prod in produces:
        p_type = prod.get("type", "other")
        p_desc = prod.get("desc", "")

        best_match = None
        best_score = 0.0

        for cons in consumes:
            c_type = cons.get("type", "other")
            c_desc = cons.get("desc", "")

            # 类型兼容性
            compatible_types = _TYPE_COMPATIBILITY.get(p_type, ["other"])
            type_match = c_type in compatible_types

            # 语义相似度（关键词重叠）
            semantic_score = _calc_semantic_similarity(p_desc, c_desc)

            # 综合得分
            score = 0.0
            if type_match:
                score = 0.4 + 0.6 * semantic_score
            else:
                score = 0.3 * semantic_score

            if score > best_score:
                best_score = score
                best_match = {
                    "from": p_desc,
                    "to": c_desc,
                    "from_type": p_type,
                    "to_type": c_type,
                    "type_match": type_match,
                    "semantic_score": round(semantic_score, 2),
                    "score": round(score, 2),
                    "confidence": _score_to_confidence(score),
                }

        if best_match and best_score >= 0.4:
            matched.append(best_match)
        elif best_match:
            best_match["gap_reason"] = _explain_gap(p_desc, c_desc if best_match else "", p_type, c_type if best_match else "")
            mismatched.append(best_match)
        else:
            mismatched.append({
                "from": p_desc,
                "to": "(B 未匹配到此输出)",
                "from_type": p_type,
                "to_type": "?",
                "score": 0.0,
                "confidence": "mismatch",
                "gap_reason": f"步骤 B 没有 consumes 能匹配此输出（{p_desc}）",
            })

    # 检查未被任何 produces 覆盖的 consumes
    matched_to = set(m["to"] for m in matched)
    for cons in consumes:
        c_desc = cons.get("desc", "")
        if c_desc and c_desc not in matched_to:
            # 检查是否已被任何 mismatched 覆盖
            already_listed = any(m.get("to") == c_desc for m in mismatched)
            if not already_listed:
                mismatched.append({
                    "from": "(A 无对应输出)",
                    "to": c_desc,
                    "from_type": "?",
                    "to_type": cons.get("type", "other"),
                    "score": 0.0,
                    "confidence": "missing",
                    "gap_reason": f"步骤 B 需要「{c_desc}」，但步骤 A 未产生此输出",
                })

    # 计算总体分数
    total_pairs = max(len(matched) + len(mismatched), 1)
    match_score = len(matched) / total_pairs if total_pairs else 0.0

    # 判断缺口类型
    gap_type = _determine_gap_type(matched, mismatched, produces, consumes)

    # 生成粘连点建议
    adhesion = None
    if mismatched:
        adhesion = _build_adhesion_suggestion(
            gap_type=gap_type,
            from_desc=mismatched[0].get("from", "?"),
            to_desc=mismatched[0].get("to", "?"),
            from_name=step_a_name,
            to_name=step_b_name,
        )

    return {
        "passed": len(mismatched) == 0,
        "score": round(match_score, 2),
        "matched": matched,
        "mismatched": mismatched,
        "gap_type": gap_type,
        "note": _generate_note(match_score, gap_type, len(mismatched)),
        "adhesion_suggestion": adhesion,
    }


def _calc_semantic_similarity(text_a, text_b):
    """计算两个文本间的语义相似度（基于关键词重叠）"""
    if not text_a or not text_b:
        return 0.0

    # 中文分词（按字/词简单分割）
    chars_a = set(text_a.lower())
    chars_b = set(text_b.lower())

    # 共通字符比例
    if not chars_a or not chars_b:
        return 0.0
    char_overlap = len(chars_a & chars_b) / max(len(chars_a | chars_b), 1)

    # 语义同义词匹配
    synonym_hits = 0
    for pa, pb in _PRODUCE_TO_CONSUME_SYNONYMS:
        if pa in text_a and pb in text_b:
            synonym_hits += 1

    # 综合得分
    score = char_overlap * 0.5 + min(synonym_hits * 0.2, 0.3)
    return min(score, 1.0)


def _score_to_confidence(score):
    """将数值分数转为置信度标签"""
    if score >= 0.8:
        return "high"
    elif score >= 0.6:
        return "medium"
    elif score >= 0.4:
        return "low"
    elif score >= 0.1:
        return "trace"
    else:
        return "mismatch"


def _explain_gap(p_desc, c_desc, p_type, c_type):
    """生成缺口原因说明"""
    reasons = []
    if p_type != c_type and c_type:
        reasons.append(f"类型不匹配（{p_type} → {c_type}）")
    if p_desc and c_desc and p_desc not in c_desc and c_desc not in p_desc:
        reasons.append(f"语义不匹配（{p_desc[:20]} → {c_desc[:20]}）")
    if not c_desc and not p_desc:
        reasons.append("双方描述均不明确")
    if not reasons:
        reasons.append("I/O 接口不兼容")
    return "; ".join(reasons)


def _determine_gap_type(matched, mismatched, produces, consumes):
    """判断缺口类型"""
    if not mismatched:
        return "none"

    # 检查是否涉及关键输出/输入缺失
    for m in mismatched:
        p_desc = m.get("from", "")
        c_desc = m.get("to", "")
        for trigger in _GAP_TRIGGER_PRODUCES:
            if trigger in p_desc:
                return "semantic"
        for trigger in _GAP_TRIGGER_CONSUMES:
            if trigger in c_desc:
                return "process"

    return "semantic"


def _build_adhesion_suggestion(gap_type, from_desc, to_desc, from_name, to_name):
    """构建粘连点建议"""
    if gap_type == "none":
        return None

    reason_template = {
        "semantic": (
            f"输出「{from_desc}」与所需输入「{to_desc}」之间存在语义鸿沟。"
            f"A 步骤产出的内容格式/结构无法被 B 步骤直接消费，"
            f"需要中间转换处理"
        ),
        "process": (
            f"A 步骤完成后缺少一个中间处理步骤，"
            f"无法将「{from_desc}」转为 B 步骤所需的「{to_desc}」。"
            f"可能需要数据格式转换或内容提取"
        ),
        "decision": (
            f"从「{from_desc}」到「{to_desc}」之间需要人工决策，"
            f"无法自动完成，需要判断"""
        ),
    }

    reason = reason_template.get(gap_type, f"输出「{from_desc}」与输入「{to_desc}」不匹配")

    return {
        "reason": reason,
        "solutions": [
            {
                "mode": "manual",
                "description": f"人工将 {from_name} 的输出转换为 {to_name} 可接受的输入格式",
            },
            {
                "mode": "hybrid",
                "description": f"LLM 读取 {from_name} 的输出，提取关键信息，重构为 {to_name} 需要的格式",
                "llm_steps": f"1) 读取 {from_name} 的输出\n2) 提取关键数据\n3) 按 {to_name} 的输入规范重排\n4) 传给 {to_name}",
                "tool_steps": "",
            },
        ],
    }


def _generate_note(score, gap_type, mismatch_count):
    """生成人类可读的总结"""
    if gap_type == "none" and score >= 0.8:
        return "✅ 步骤衔接良好，无缺口"
    elif gap_type == "none" and score >= 0.5:
        return "✅ 基本可衔接，建议确认"
    elif gap_type == "none":
        return "⚠️ 部分匹配，I/O 声明可能不完整"
    else:
        n = mismatch_count
        return f"❌ 检测到 {n} 个{mismatch_count}缺口（类型: {gap_type}），需要粘连点"


# ============================================================
# CLI 入口
# ============================================================

def main():
    # 修复 Windows 控制台编码问题
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(
        description="Step Link Validator v1.29.0 - 步骤衔接校验器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从 JSON 文件读两个步骤的 interface 并校验
  python step_link_validator.py check --from-json file_a.json --to-json file_b.json

  # 从 JSON 字符串直接传
  python step_link_validator.py check --from '{"produces":[{"type":"report","desc":"审查报告"}]}' --to '{"consumes":[{"type":"config","desc":"配置参数"}]}'

  # 从步骤索引读
  python step_link_validator.py check --from-step "skill-a.step-1" --to-step "skill-b.step-2"
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # check
    p_check = subparsers.add_parser("check", help="校验两个步骤的衔接")
    from_group = p_check.add_mutually_exclusive_group(required=True)
    from_group.add_argument("--from-json", help="步骤A interface JSON 文件路径")
    from_group.add_argument("--from", dest="from_str", help="步骤A interface JSON 字符串")
    from_group.add_argument("--from-step", help="步骤A 步骤ID（从 step_index 读取）")
    to_group = p_check.add_mutually_exclusive_group(required=True)
    to_group.add_argument("--to-json", help="步骤B interface JSON 文件路径")
    to_group.add_argument("--to", dest="to_str", help="步骤B interface JSON 字符串")
    to_group.add_argument("--to-step", help="步骤B 步骤ID（从 step_index 读取）")
    p_check.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "check":
        return _cmd_check(args)

    parser.print_help()
    return 1


def _cmd_check(args):
    """处理 check 命令"""
    # 读取步骤 A 的 interface
    iface_a = _load_interface(args.from_json, args.from_str, args.from_step, "A")
    if iface_a is None:
        return 1

    # 读取步骤 B 的 interface
    iface_b = _load_interface(args.to_json, args.to_str, args.to_step, "B")
    if iface_b is None:
        return 1

    # 执行校验
    result = validate_link(iface_a, iface_b)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_result(result)

    return 0 if result["passed"] else 1


def _load_interface(json_path, json_str, step_id, label):
    """从不同来源加载 interface"""
    if json_path:
        path = Path(json_path)
        if not path.exists():
            print(f"❌ 文件不存在: {json_path}")
            return None
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 解析 {json_path} 失败: {e}")
            return None

    if json_str:
        try:
            return json.loads(json_str)
        except Exception as e:
            print(f"❌ 解析 JSON 失败: {e}")
            return None

    if step_id:
        if "." not in step_id:
            print(f"❌ 步骤ID格式应为 skill_name.step_name")
            return None
        skill_name = step_id.split(".")[0]
        bp_dir = Path.home() / ".workbuddy" / "skills" / ".standardization" / "skill-sub" / "step_index"
        bp_file = bp_dir / f"{skill_name}.json"
        if not bp_file.exists():
            print(f"❌ 步骤索引 '{skill_name}' 不存在，请先运行 step_indexer.py scan")
            return None
        try:
            with open(bp_file, "r") as f:
                blueprint = json.load(f)
            for step in blueprint.get("steps", []):
                if step.get("step_id") == step_id:
                    return step.get("interface", {})
            print(f"❌ 步骤 '{step_id}' 未在 '{skill_name}' 中找到")
            return None
        except Exception as e:
            print(f"❌ 读取步骤索引失败: {e}")
            return None

    return None


def _print_result(result):
    """打印校验结果"""
    print(f"📋 步骤衔接校验结果")
    print(f"{'='*50}")
    print(f"  状态: {'✅ 通过' if result['passed'] else '❌ 需处理'}")
    print(f"  匹配分数: {result['score']}")
    print(f"  缺口类型: {result['gap_type']}")
    print(f"  说明: {result.get('note', '')}")
    print()

    if result.get("matched"):
        print(f"✅ 已匹配 ({len(result['matched'])} 项):")
        for m in result["matched"]:
            conf_icon = {"high": "🟢", "medium": "🟡", "low": "🟠"}.get(m["confidence"], "⚪")
            print(f"  {conf_icon} {m['from'][:35]} → {m['to'][:35]} ({m['confidence']})")

    if result.get("mismatched"):
        print(f"\n❌ 未匹配 ({len(result['mismatched'])} 项):")
        for m in result["mismatched"]:
            conf_icon = {"missing": "🔴", "mismatch": "🔴", "trace": "🟡"}.get(m["confidence"], "🟠")
            print(f"  {conf_icon} {m['from'][:35]} → {m['to'][:35]}")
            if m.get("gap_reason"):
                print(f"    原因: {m['gap_reason']}")

    if result.get("adhesion_suggestion"):
        print(f"\n🔗 粘连点建议:")
        sug = result["adhesion_suggestion"]
        print(f"  原因: {sug['reason'][:100]}...")
        print(f"  方案 {len(sug['solutions'])} 个:")
        for i, sol in enumerate(sug["solutions"], 1):
            print(f"    {i}. [{sol['mode']}] {sol['description'][:80]}")

    print()


if __name__ == "__main__":
    sys.exit(main())
