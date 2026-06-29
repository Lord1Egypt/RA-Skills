"""
chain_flow_validator.py - 调用链流程校验器 v1.25.0
纯算法，零外部依赖。校验调用链的步骤连续性、依赖完整性、粘连点比例、skill 存在性。

输出结构化校验报告，供 AI 修正参考。

用法:
    python scripts/chain_flow_validator.py <chain.json>
    python scripts/chain_flow_validator.py <chain.json> --skills-dir <路径>
"""

import json
import os
import sys
from pathlib import Path


# ============================================================
# 校验规则
# ============================================================

def validate(steps, skills_dir=None):
    """
    校验调用链步骤列表。
    steps: list[dict] — 步骤列表
    skills_dir: str|None — 技能目录路径（用于校验 skill 存在性）
    返回: dict — { "passed": bool, "issues": list[dict] }
    """
    issues = []
    total = len(steps)

    if total == 0:
        return {"passed": True, "issues": [], "summary": "空调用链，无需校验"}

    # 1. 索引连续性检查
    indices = [s.get("index", i + 1) for i, s in enumerate(steps)]
    expected = list(range(1, total + 1))
    if indices != expected:
        # 找出跳跃或重复
        seen = set()
        for i, idx in enumerate(indices):
            if idx < 1:
                issues.append({"type": "index_invalid", "severity": "ERROR",
                               "step": idx, "message": f"步骤 {i+1} 索引无效: {idx}"})
            elif idx in seen:
                issues.append({"type": "index_duplicate", "severity": "ERROR",
                               "step": idx, "message": f"索引 {idx} 重复"})
            else:
                seen.add(idx)
        missing = sorted(set(expected) - seen)
        if missing:
            issues.append({"type": "index_gap", "severity": "WARN",
                           "step": missing[0], "message": f"索引缺失: {missing}"})

    # 2. 依赖链完整性检查
    all_indices = set(indices)
    for step in steps:
        idx = step.get("index", "?")
        deps = step.get("depends_on", [])
        for d in deps:
            if d not in all_indices and d != 0:
                issues.append({"type": "dep_missing", "severity": "ERROR",
                               "step": idx, "message": f"步骤 {idx} 依赖不存在的步骤 {d}"})

    # 3. 孤立步骤检查（无入链/出链，且不是第一步）
    if total > 1:
        has_incoming = set()
        has_outgoing = set()
        for step in steps:
            idx = step.get("index", "?")
            deps = step.get("depends_on", [])
            for d in deps:
                if d in all_indices:
                    has_outgoing.add(d)
                    has_incoming.add(idx)
        # 第一步可以无 incoming
        first_idx = indices[0]
        for step in steps:
            idx = step.get("index", "?")
            if idx == first_idx:
                continue
            if idx not in has_incoming and idx not in has_outgoing:
                issues.append({"type": "orphan_step", "severity": "WARN",
                               "step": idx, "message": f"步骤 {idx} 是孤立步骤（无依赖链连接）"})

    # 3b. 连续粘连点检查：粘连点是两个 skill 步骤之间的连接器，不允许连续出现
    for i in range(len(steps) - 1):
        curr = steps[i]
        next_s = steps[i + 1]
        if curr.get("type", "skill") == "adhesion" and next_s.get("type", "skill") == "adhesion":
            curr_idx = curr.get("index", "?")
            next_idx = next_s.get("index", "?")
            issues.append({"type": "adhesion_consecutive", "severity": "ERROR",
                           "step": curr_idx, "message": f"粘连点步骤 {curr_idx} 后紧跟粘连点 {next_idx}，连续缺口应合并为一个粘连点"})

    # 4. 粘连点比例检查
    adhesion_count = sum(1 for s in steps if s.get("type", "skill") == "adhesion")
    if total > 0:
        ratio = adhesion_count / total
        if ratio > 0.3:
            issues.append({"type": "adhesion_overage", "severity": "WARN",
                           "step": 0, "message": f"粘连点占比 {ratio:.0%}（{adhesion_count}/{total}），超过 30% 上限"})
        elif adhesion_count > 0 and ratio > 0.1:
            issues.append({"type": "adhesion_notable", "severity": "INFO",
                           "step": 0, "message": f"粘连点占比 {ratio:.0%}（{adhesion_count}/{total}），建议检查是否必要"})

    # 5. 粘连点方案完整性检查
    for step in steps:
        if step.get("type", "skill") != "adhesion":
            continue
        idx = step.get("index", "?")
        adhesion = step.get("adhesion", {})
        if not adhesion.get("solutions"):
            issues.append({"type": "adhesion_no_solution", "severity": "ERROR",
                           "step": idx, "message": f"粘连点步骤 {idx} 缺少解决方案"})
        if not adhesion.get("reason"):
            issues.append({"type": "adhesion_no_reason", "severity": "WARN",
                           "step": idx, "message": f"粘连点步骤 {idx} 缺少原因说明"})

    # 6. Skill 存在性检查（仅当提供 skills_dir 时）
    if skills_dir:
        skills_path = Path(skills_dir)
        for step in steps:
            if step.get("type", "skill") != "skill":
                continue
            idx = step.get("index", "?")
            skill_name = step.get("skill_name", "")
            if not skill_name:
                issues.append({"type": "skill_missing_name", "severity": "ERROR",
                               "step": idx, "message": f"步骤 {idx} 缺少 skill_name"})
                continue
            # 检查 SKILL.md 是否存在
            skill_path = skills_path / skill_name
            if not (skill_path / "SKILL.md").exists():
                issues.append({"type": "skill_not_found", "severity": "ERROR",
                               "step": idx, "message": f"步骤 {idx} 引用的 skill '{skill_name}' 不存在"})

    # 汇总
    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]
    passed = len(errors) == 0

    # 计算 auto_safe：链中无 manual 粘连点且无 ask 模式时 true
    auto_safe = True
    for step in steps:
        if step.get("type", "skill") == "adhesion":
            adhesion = step.get("adhesion", {})
            for sol in adhesion.get("solutions", []):
                if sol.get("mode") == "manual":
                    auto_safe = False
                    break
            if not auto_safe:
                break
            # 无 solutions 时也不安全
            if not adhesion.get("solutions"):
                auto_safe = False
                break
        # failure_mode.on_exhaust = "ask" 也需要人介入
        fm = step.get("failure_mode", {})
        if isinstance(fm, dict) and fm.get("on_exhaust") == "ask":
            auto_safe = False
            break
        if isinstance(fm, str) and fm == "ask":
            auto_safe = False
            break

    return {
        "passed": passed,
        "auto_safe": auto_safe,
        "issues": issues,
        "summary": {
            "total": total,
            "errors": len(errors),
            "warnings": len(warnings),
            "infos": len([i for i in issues if i["severity"] == "INFO"]),
            "adhesion_count": adhesion_count,
            "adhesion_ratio": round(adhesion_count / total, 2) if total > 0 else 0,
        }
    }


def format_report(result):
    """格式化校验报告为可读文本"""
    lines = []
    s = result["summary"]
    lines.append(f"校验结果: {'通过' if result['passed'] else '未通过'}")
    lines.append(f"总步骤: {s['total']} | ERROR: {s['errors']} | WARN: {s['warnings']} | 可自动执行: {'是' if result.get('auto_safe', True) else '否'}")
    if s["adhesion_count"] > 0:
        lines.append(f"粘连点: {s['adhesion_count']} ({s['adhesion_ratio']:.0%})")

    if result["issues"]:
        lines.append("")
        lines.append("问题列表:")
        for issue in result["issues"]:
            lines.append(f"  [{issue['severity']}] {issue['message']}")

    return "\n".join(lines)


# ============================================================
# CLI
# ============================================================

def main():
    # 修复 Windows 控制台编码问题
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(
        description="Chain Flow Validator v1.25.0 — 调用链流程校验器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("chain_file", nargs="?", help="调用链 JSON 文件路径")
    parser.add_argument("--skills-dir", default="", help="技能目录路径（用于校验 skill 存在性）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--steps", help="直接传入 JSON 步骤数组（替代文件）")

    args = parser.parse_args()

    if args.steps:
        try:
            steps = json.loads(args.steps)
        except json.JSONDecodeError as e:
            print(f"❌ 步骤 JSON 解析失败: {e}")
            return 1
    elif args.chain_file:
        try:
            with open(args.chain_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            steps = data.get("steps", data if isinstance(data, list) else [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ 文件读取失败: {e}")
            return 1
    else:
        print("❌ 请指定调用链文件或使用 --steps 传入步骤 JSON")
        return 1

    skills_dir = args.skills_dir or os.environ.get("WORKBUDDY_SKILLS_DIR", "")
    result = validate(steps, skills_dir if skills_dir else None)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    import argparse
    sys.exit(main())
