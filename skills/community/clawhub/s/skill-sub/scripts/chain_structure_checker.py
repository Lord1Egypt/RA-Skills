"""
chain_structure_checker.py - 调用链结构校验器 v1.25.0
纯算法，零外部依赖。保存前最后一道关，不合格直接拒绝保存。

检查项:
  - JSON 结构合法性
  - step 类型枚举 (skill/loop/branch/adhesion)
  - 必填字段完整性
  - 依赖闭环检测

用法:
    python scripts/chain_structure_checker.py <chain.json>
    python scripts/chain_structure_checker.py <chain.json> --fix
"""

import json
import sys
from pathlib import Path
from copy import deepcopy


# ============================================================
# 类型定义
# ============================================================

VALID_TYPES = {"skill", "loop", "branch", "adhesion"}

SKILL_REQUIRED = {"index", "type", "step_name", "skill_name"}
LOOP_REQUIRED = {"index", "type", "step_name", "loop"}
BRANCH_REQUIRED = {"index", "type", "step_name", "branch"}
ADHESION_REQUIRED = {"index", "type", "step_name", "adhesion"}

LOOP_SUB_REQUIRED = {"mode", "steps"}
BRANCH_SUB_REQUIRED = {"condition", "if_steps", "else_steps"}
ADHESION_SUB_REQUIRED = {"reason", "solutions"}


# ============================================================
# 校验核心
# ============================================================

def check(chain_data):
    """
    校验完整调用链 JSON。
    chain_data: dict — 调用链数据（含 name, steps 等）
    返回: dict — { "passed": bool, "errors": list, "fixable": bool }
    """
    errors = []

    # 1. 顶层结构
    if not isinstance(chain_data, dict):
        errors.append({"field": "root", "message": "调用链数据必须是 JSON 对象", "fixable": False})
        return {"passed": False, "errors": errors, "fixable": False}

    if "name" not in chain_data or not chain_data["name"]:
        errors.append({"field": "name", "message": "缺少 name 字段", "fixable": True})

    steps = chain_data.get("steps", [])
    if not steps:
        errors.append({"field": "steps", "message": "steps 为空或缺失", "fixable": True})
        return {"passed": len(errors) == 0, "errors": errors, "fixable": any(e["fixable"] for e in errors)}

    # 2. 逐步骤校验
    seen_indices = set()
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append({"field": f"steps[{i}]", "message": f"步骤 {i} 不是 JSON 对象", "fixable": False})
            continue

        step_type = step.get("type", "skill")
        idx = step.get("index", i + 1)

        # 类型枚举校验
        if step_type not in VALID_TYPES:
            errors.append({"field": f"steps[{i}].type", "message": f"步骤 {idx}: 无效类型 '{step_type}'，有效值: {sorted(VALID_TYPES)}",
                          "fixable": True})

        # 索引唯一性
        if idx in seen_indices:
            errors.append({"field": f"steps[{i}].index", "message": f"索引 {idx} 重复", "fixable": True})
        seen_indices.add(idx)

        # 通用必填字段
        if not step.get("step_name"):
            errors.append({"field": f"steps[{i}].step_name", "message": f"步骤 {idx}: 缺少 step_name", "fixable": True})

        # 类型专用校验
        if step_type == "skill":
            for f in SKILL_REQUIRED:
                if f not in step or (isinstance(step.get(f), str) and not step[f]):
                    errors.append({"field": f"steps[{i}].{f}", "message": f"步骤 {idx}: 缺少必填字段 {f}",
                                  "fixable": True})

        elif step_type == "loop":
            for f in LOOP_REQUIRED:
                if f not in step:
                    errors.append({"field": f"steps[{i}].{f}", "message": f"步骤 {idx}: 缺少必填字段 {f}",
                                  "fixable": True})
            loop = step.get("loop", {})
            if isinstance(loop, dict):
                for f in LOOP_SUB_REQUIRED:
                    if f not in loop:
                        errors.append({"field": f"steps[{i}].loop.{f}", "message": f"步骤 {idx}: loop 缺少 {f}",
                                      "fixable": True})
                # 递归校验子步骤
                sub_steps = loop.get("steps", [])
                sub_result = _check_sub_steps(sub_steps, f"steps[{i}].loop.steps")
                errors.extend(sub_result)

        elif step_type == "branch":
            for f in BRANCH_REQUIRED:
                if f not in step:
                    errors.append({"field": f"steps[{i}].{f}", "message": f"步骤 {idx}: 缺少必填字段 {f}",
                                  "fixable": True})
            branch = step.get("branch", {})
            if isinstance(branch, dict):
                for f in BRANCH_SUB_REQUIRED:
                    if f not in branch:
                        errors.append({"field": f"steps[{i}].branch.{f}", "message": f"步骤 {idx}: branch 缺少 {f}",
                                      "fixable": True})
                for key in ["if_steps", "else_steps"]:
                    sub_result = _check_sub_steps(branch.get(key, []), f"steps[{i}].branch.{key}")
                    errors.extend(sub_result)

        elif step_type == "adhesion":
            for f in ADHESION_REQUIRED:
                if f not in step:
                    errors.append({"field": f"steps[{i}].{f}", "message": f"步骤 {idx}: 缺少必填字段 {f}",
                                  "fixable": True})
            adhesion = step.get("adhesion", {})
            if isinstance(adhesion, dict):
                for f in ADHESION_SUB_REQUIRED:
                    if f not in adhesion:
                        errors.append({"field": f"steps[{i}].adhesion.{f}", "message": f"步骤 {idx}: adhesion 缺少 {f}",
                                      "fixable": True})
                solutions = adhesion.get("solutions", [])
                if isinstance(solutions, list) and len(solutions) == 0:
                    errors.append({"field": f"steps[{i}].adhesion.solutions",
                                   "message": f"步骤 {idx}: adhesion.solutions 至少需要 1 个方案",
                                   "fixable": True})
                for si, sol in enumerate(solutions if isinstance(solutions, list) else []):
                    if not isinstance(sol, dict):
                        continue
                    mode = sol.get("mode", "")
                    if mode not in ("manual", "auto", "hybrid"):
                        errors.append({"field": f"steps[{i}].adhesion.solutions[{si}].mode",
                                       "message": f"步骤 {idx}: 无效方案模式 '{mode}'",
                                       "fixable": True})

    # 3. 依赖闭环检测
    dep_errors = _check_dependency_cycles(steps)
    errors.extend(dep_errors)

    passed = len([e for e in errors if not e.get("fixable", True) or True]) > 0
    passed = len([e for e in errors if e.get("fixable", True)]) == 0

    return {
        "passed": len(errors) == 0,
        "errors": errors,
        "fixable": any(e.get("fixable", True) for e in errors),
    }


def _check_sub_steps(sub_steps, prefix):
    """递归校验子步骤结构"""
    errors = []
    if not isinstance(sub_steps, list):
        return [{"field": prefix, "message": f"{prefix} 必须是数组", "fixable": True}]
    for i, sub in enumerate(sub_steps):
        if not isinstance(sub, dict):
            errors.append({"field": f"{prefix}[{i}]", "message": f"{prefix}[{i}] 不是 JSON 对象", "fixable": False})
            continue
        st = sub.get("type", "skill")
        if st not in VALID_TYPES:
            errors.append({"field": f"{prefix}[{i}].type", "message": f"{prefix}[{i}]: 无效类型 '{st}'",
                          "fixable": True})
        if st == "skill" and not sub.get("skill_name"):
            errors.append({"field": f"{prefix}[{i}].skill_name", "message": f"{prefix}[{i}]: skill 步骤缺少 skill_name",
                          "fixable": True})
    return errors


def _check_dependency_cycles(steps):
    """检测依赖闭环"""
    errors = []
    step_map = {}
    for step in steps:
        idx = step.get("index", 0)
        if idx:
            step_map[idx] = step

    for step in steps:
        idx = step.get("index", 0)
        if not idx:
            continue
        visited = set()
        current = idx
        while current in step_map:
            if current in visited:
                errors.append({"field": "depends_on", "message": f"检测到依赖闭环，涉及步骤 {current}",
                              "fixable": True})
                break
            visited.add(current)
            deps = step_map[current].get("depends_on", [])
            if not deps:
                break
            current = deps[0]
    return errors


# ============================================================
# 自动修复（简单修复）
# ============================================================

def auto_fix(chain_data):
    """尝试自动修复可修复的错误"""
    fixed = False
    steps = chain_data.get("steps", [])

    # 重新编号
    for i, step in enumerate(steps):
        expected = i + 1
        if step.get("index") != expected:
            step["index"] = expected
            fixed = True

    chain_data["steps"] = steps
    return chain_data, fixed


# ============================================================
# CLI
# ============================================================

def main():
    import argparse

    # 修复 Windows 控制台编码问题
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(
        description="Chain Structure Checker v1.25.0 — 调用链结构校验器（保存前最后一道关）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("chain_file", nargs="?", help="调用链 JSON 文件路径")
    parser.add_argument("--fix", action="store_true", help="尝试自动修复可修复问题")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()

    if not args.chain_file:
        print("❌ 请指定调用链 JSON 文件路径")
        return 1

    try:
        with open(args.chain_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ 文件读取失败: {e}")
        return 1

    if args.fix:
        data, fixed = auto_fix(data)
        if fixed:
            with open(args.chain_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ 自动修复完成（索引重新编号）")

    result = check(data)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["passed"]:
            print(f"✅ 结构校验通过（{len(data.get('steps', []))} 步骤）")
        else:
            print(f"❌ 结构校验未通过（{len(result['errors'])} 个错误）")
            for e in result["errors"]:
                fixable = "[可修复]" if e.get("fixable", True) else "[不可修复]"
                print(f"  {fixable} {e['message']}")
            if result["fixable"]:
                print("\n💡 部分错误可自动修复，试试 --fix")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
