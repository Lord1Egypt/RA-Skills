#!/usr/bin/env python3
"""
P5 自检验证模块 — _validate_prepared_point()
对 P5 输出的每条测试点执行13项完整性自检，确保必备字段有内容。

版本: 1.0.0
日期: 2026-05-15
任务: 1.3 P5自检验证实现

用法:
    from p5_validate import validate_prepared_point, validate_batch

    issues = validate_prepared_point(tp)
    report = validate_batch(batch_points)

无外部依赖，仅使用 Python 标准库。
"""

from typing import Any


# ============================================================
# 常量定义
# ============================================================

# 有效的 category 枚举值
VALID_CATEGORIES = frozenset({
    "main_flow",
    "branch",
    "integration",
    "permission",
    "exception",
    "boundary",
    "field_validation",
    "security",
    "state_migration",
    "performance",
    "compatibility",
})

# 有效的 priority 枚举值
VALID_PRIORITIES = frozenset({"P0", "P1", "P2", "P3", "P4"})

# 检查级别
LEVEL_FORCE = "FORCE"   # 强制项，不通过则视为严重缺陷
LEVEL_WARN = "WARN"     # 建议项，不通过则预警但不阻断


# ============================================================
# 辅助函数
# ============================================================

def _str_len(value: Any) -> int:
    """安全获取字符串长度，非字符串类型返回0"""
    if isinstance(value, str):
        return len(value.strip())
    return 0


def _list_len(value: Any) -> int:
    """安全获取列表长度，非列表类型返回0"""
    if isinstance(value, list):
        return len(value)
    return 0


def _is_non_empty_str(value: Any) -> bool:
    """判断是否为非空字符串"""
    return isinstance(value, str) and bool(value.strip())


def _is_valid_enum(value: Any, valid_set: frozenset) -> bool:
    """判断值是否在有效枚举集合中"""
    if not isinstance(value, str):
        return False
    return value.strip() in valid_set


# ============================================================
# 核心：13项完整性自检
# ============================================================

def validate_prepared_point(tp: dict) -> list:
    """
    对单条测试点执行13项完整性检查。

    检查项清单（与任务1.3严格对应）：

    | # | 检查项              | 检查逻辑                     |
    |---|---------------------|------------------------------|
    | 1 | page_path 非空      | 长度 > 0                     |
    | 2 | operations_chain 至少1步 | 列表长度 ≥ 1             |
    | 3 | field_specs 至少1个 | 列表长度 ≥ 1                  |
    | 4 | business_rules 至少1条 | 列表长度 ≥ 1               |
    | 5 | description 长度 ≥20 | 字符数 ≥ 20                 |
    | 6 | category 有效值     | 在有效枚举中                  |
    | 7 | priority 有效值     | P0/P1/P2/P3/P4               |
    | 8 | 前置条件完整性       | 环境+账号+数据三要素           |
    | 9 | 操作链路步骤连贯性   | step 序号连续                 |
    | 10 | 字段规格完整性       | 字段名+类型+约束              |
    | 11 | 无矛盾信息          | 路径与操作不冲突               |
    | 12 | 风险点已识别         | 有 risk_flag 但无 risk_description 时预警 |
    | 13 | PCI 已识别          | 有 pci_flag 但无 pci_description 时预警 |

    Args:
        tp: P5 输出的测试点 dict

    Returns:
        list[dict]: 问题列表，每项包含：
            - code: 检查项编号 (V01~V13)
            - level: FORCE | WARN
            - message: 问题描述
            - field: 涉及字段名
        空列表表示全部通过。
    """
    if not isinstance(tp, dict):
        return [_make_issue("V00", LEVEL_FORCE, "测试点数据类型错误，期望 dict", "root")]

    issues = []

    # ---- V01: page_path 非空 ----
    issues.extend(_check_page_path(tp))

    # ---- V02: operations_chain 至少1步 ----
    issues.extend(_check_operations_chain_count(tp))

    # ---- V03: field_specs 至少1个 ----
    issues.extend(_check_field_specs_count(tp))

    # ---- V04: business_rules 至少1条 ----
    issues.extend(_check_business_rules_count(tp))

    # ---- V05: description 长度 ≥ 20 ----
    issues.extend(_check_description_length(tp))

    # ---- V06: category 有效值 ----
    issues.extend(_check_category(tp))

    # ---- V07: priority 有效值 ----
    issues.extend(_check_priority(tp))

    # ---- V08: 前置条件完整性（环境+账号+数据三要素） ----
    issues.extend(_check_precondition(tp))

    # ---- V09: 操作链路步骤连贯性（step序号连续） ----
    issues.extend(_check_operations_chain_continuity(tp))

    # ---- V10: 字段规格完整性（字段名+类型+约束） ----
    issues.extend(_check_field_specs_completeness(tp))

    # ---- V11: 无矛盾信息（路径与操作不冲突） ----
    issues.extend(_check_no_contradiction(tp))

    # ---- V12: 风险点已识别 ----
    issues.extend(_check_risk_identification(tp))

    # ---- V13: PCI 已识别 ----
    issues.extend(_check_pci_identification(tp))

    return issues


def _make_issue(code: str, level: str, message: str, field: str) -> dict:
    """构造标准检查结果项"""
    return {
        "code": code,
        "level": level,
        "message": message,
        "field": field,
    }


# ============================================================
# 13项检查实现
# ============================================================

def _check_page_path(tp: dict) -> list:
    """
    V01: page_path 非空
    检查逻辑：长度 > 0
    """
    page_path = tp.get("page_path")

    # 情况1：dict 类型，检查 full_path 或 hierarchy
    if isinstance(page_path, dict):
        full_path = page_path.get("full_path", "")
        hierarchy = page_path.get("hierarchy", [])
        if _is_non_empty_str(full_path):
            return []
        if isinstance(hierarchy, list) and len(hierarchy) > 0:
            return []
        return [_make_issue("V01", LEVEL_FORCE,
                            "page_path 为空 dict，缺少 full_path 或 hierarchy",
                            "page_path")]

    # 情况2：str 类型，检查非空
    if isinstance(page_path, str):
        if _str_len(page_path) > 0:
            return []
        return [_make_issue("V01", LEVEL_FORCE,
                            "page_path 为空字符串", "page_path")]

    # 情况3：None 或其他类型
    return [_make_issue("V01", LEVEL_FORCE,
                        f"page_path 缺失或类型无效（当前: {type(page_path).__name__}）",
                        "page_path")]


def _check_operations_chain_count(tp: dict) -> list:
    """
    V02: operations_chain 至少1步
    检查逻辑：列表长度 ≥ 1
    """
    ops = tp.get("operations_chain")
    if isinstance(ops, list) and len(ops) >= 1:
        return []
    actual = _list_len(ops)
    return [_make_issue("V02", LEVEL_FORCE,
                        f"operations_chain 为空或不是列表，当前 {actual} 步，要求 ≥ 1",
                        "operations_chain")]


def _check_field_specs_count(tp: dict) -> list:
    """
    V03: field_specs 至少1个
    检查逻辑：列表长度 ≥ 1
    """
    specs = tp.get("field_specs")
    if isinstance(specs, list) and len(specs) >= 1:
        return []
    actual = _list_len(specs)
    return [_make_issue("V03", LEVEL_FORCE,
                        f"field_specs 为空或不是列表，当前 {actual} 个，要求 ≥ 1",
                        "field_specs")]


def _check_business_rules_count(tp: dict) -> list:
    """
    V04: business_rules 至少1条
    检查逻辑：列表长度 ≥ 1
    """
    rules = tp.get("business_rules")
    if isinstance(rules, list) and len(rules) >= 1:
        return []
    actual = _list_len(rules)
    return [_make_issue("V04", LEVEL_WARN,
                        f"business_rules 为空或不是列表，当前 {actual} 条，建议 ≥ 1",
                        "business_rules")]


def _check_description_length(tp: dict) -> list:
    """
    V05: description 长度 ≥ 20
    检查逻辑：字符数 ≥ 20
    """
    desc = tp.get("description", "")
    length = _str_len(desc)
    if length >= 20:
        return []
    return [_make_issue("V05", LEVEL_FORCE,
                        f"description 长度 {length}，要求 ≥ 20 字符",
                        "description")]


def _check_category(tp: dict) -> list:
    """
    V06: category 有效值
    检查逻辑：在有效枚举中
    """
    cat = tp.get("category", "")
    if _is_valid_enum(cat, VALID_CATEGORIES):
        return []
    return [_make_issue("V06", LEVEL_FORCE,
                        f"category 值「{cat}」不在有效枚举中，"
                        f"有效值: {', '.join(sorted(VALID_CATEGORIES))}",
                        "category")]


def _check_priority(tp: dict) -> list:
    """
    V07: priority 有效值
    检查逻辑：P0/P1/P2/P3/P4
    """
    pri = tp.get("priority", "")
    if _is_valid_enum(pri, VALID_PRIORITIES):
        return []
    return [_make_issue("V07", LEVEL_FORCE,
                        f"priority 值「{pri}」不在有效枚举中，有效值: P0, P1, P2, P3, P4",
                        "priority")]


def _check_precondition(tp: dict) -> list:
    """
    V08: 前置条件完整性
    检查逻辑：环境 + 账号 + 数据三要素
    """
    precond = tp.get("precondition")

    if precond is None:
        return [_make_issue("V08", LEVEL_FORCE,
                            "precondition 缺失，要求包含环境(environment)+账号(account)+数据(data_preparation)三要素",
                            "precondition")]

    # dict 类型：逐项检查三要素
    if isinstance(precond, dict):
        missing = []
        if not precond.get("environment"):
            missing.append("environment")
        if not precond.get("account"):
            missing.append("account")
        if not precond.get("data_preparation"):
            missing.append("data_preparation")

        if missing:
            return [_make_issue("V08", LEVEL_FORCE,
                                f"precondition 缺少三要素: {', '.join(missing)}",
                                "precondition")]
        return []

    # str 类型：检查非空
    if isinstance(precond, str):
        if _str_len(precond) > 0:
            # 字符串形式无法精确验证三要素，标记为建议
            return [_make_issue("V08", LEVEL_WARN,
                                "precondition 为字符串格式，建议使用结构化 dict（含 environment/account/data_preparation 三要素）",
                                "precondition")]
        return [_make_issue("V08", LEVEL_FORCE,
                            "precondition 为空字符串",
                            "precondition")]

    # 其他类型
    return [_make_issue("V08", LEVEL_FORCE,
                        f"precondition 类型无效（当前: {type(precond).__name__}），要求 dict 或 str",
                        "precondition")]


def _check_operations_chain_continuity(tp: dict) -> list:
    """
    V09: 操作链路步骤连贯性
    检查逻辑：step 序号连续（1, 2, 3, ...），无跳跃或重复
    """
    ops = tp.get("operations_chain", [])
    if not isinstance(ops, list) or len(ops) == 0:
        # V02 已覆盖空列表检查，此处跳过
        return []

    issues = []

    # 收集所有 step 序号
    step_numbers = []
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            issues.append(_make_issue("V09", LEVEL_WARN,
                                      f"operations_chain[{i}] 不是 dict 类型",
                                      f"operations_chain[{i}]"))
            continue
        step = op.get("step")
        if step is None:
            # 没有 step 字段时，使用索引+1作为隐式序号
            step_numbers.append(i + 1)
        else:
            try:
                step_numbers.append(int(step))
            except (TypeError, ValueError):
                issues.append(_make_issue("V09", LEVEL_FORCE,
                                          f"operations_chain[{i}].step 值「{step}」不是有效整数",
                                          f"operations_chain[{i}].step"))

    if not step_numbers:
        return issues

    # 检查连续性：期望从1开始，每次+1
    expected = list(range(1, len(step_numbers) + 1))
    if step_numbers != expected:
        # 详细分析问题
        problems = []
        if step_numbers[0] != 1:
            problems.append(f"起始序号 {step_numbers[0]} ≠ 1")

        gaps = []
        for i in range(1, len(step_numbers)):
            diff = step_numbers[i] - step_numbers[i - 1]
            if diff != 1:
                if diff > 1:
                    gaps.append(f"步骤 {step_numbers[i-1]}→{step_numbers[i]} 之间跳跃了 {diff-1} 步")
                elif diff <= 0:
                    gaps.append(f"步骤 {step_numbers[i-1]}→{step_numbers[i]} 存在重复或倒序")
        if gaps:
            problems.extend(gaps)

        # 检查重复
        seen = set()
        duplicates = []
        for s in step_numbers:
            if s in seen:
                duplicates.append(s)
            seen.add(s)
        if duplicates:
            problems.append(f"重复序号: {sorted(set(duplicates))}")

        issues.append(_make_issue("V09", LEVEL_FORCE,
                                  f"操作链路 step 序号不连续: {'; '.join(problems)}",
                                  "operations_chain"))

    return issues


def _check_field_specs_completeness(tp: dict) -> list:
    """
    V10: 字段规格完整性
    检查逻辑：每个 field_spec 应包含字段名(name) + 类型(type) + 约束(constraints)
    """
    specs = tp.get("field_specs", [])
    if not isinstance(specs, list) or len(specs) == 0:
        # V03 已覆盖空列表检查，此处跳过
        return []

    issues = []
    for i, spec in enumerate(specs):
        if not isinstance(spec, dict):
            issues.append(_make_issue("V10", LEVEL_FORCE,
                                      f"field_specs[{i}] 不是 dict 类型",
                                      f"field_specs[{i}]"))
            continue

        missing_parts = []
        if not _is_non_empty_str(spec.get("name")):
            missing_parts.append("name(字段名)")
        if not _is_non_empty_str(spec.get("type")) and spec.get("type") is not None:
            # type 可以为 None 但建议有值
            missing_parts.append("type(类型)")
        elif spec.get("type") is None:
            missing_parts.append("type(类型)")

        if not spec.get("constraints") and not spec.get("validation_rules"):
            missing_parts.append("constraints(约束)")

        if missing_parts:
            field_name = spec.get("name", f"#{i}")
            issues.append(_make_issue("V10", LEVEL_WARN,
                                      f"字段规格「{field_name}」不完整，缺少: {', '.join(missing_parts)}",
                                      f"field_specs[{i}]"))

    return issues


def _check_no_contradiction(tp: dict) -> list:
    """
    V11: 无矛盾信息
    检查逻辑：page_path 与 operations_chain 不冲突

    矛盾场景：
      - page_path 指向模块A，但 operations_chain 中的 navigate 步骤指向模块B
      - operations_chain 中的 navigate 步骤路径与 page_path 不一致
    """
    page_path = tp.get("page_path")
    ops = tp.get("operations_chain", [])

    if not isinstance(ops, list) or len(ops) == 0:
        return []

    # 提取 page_path 中的关键路径信息
    page_path_str = ""
    if isinstance(page_path, dict):
        page_path_str = page_path.get("full_path", "")
        if not page_path_str and isinstance(page_path.get("hierarchy"), list):
            page_path_str = "→".join(page_path["hierarchy"])
    elif isinstance(page_path, str):
        page_path_str = page_path

    if not page_path_str:
        return []

    # 检查 operations_chain 中 navigate 步骤的目标是否与 page_path 一致
    issues = []
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            continue
        action_type = str(op.get("action_type", "")).lower()
        if action_type != "navigate":
            continue

        target = str(op.get("target", op.get("description", "")))

        if not target:
            continue

        # 提取 page_path 的最后一级作为核心模块名
        path_parts = [p.strip() for p in page_path_str.replace("→", ">").split(">") if p.strip()]
        core_module = path_parts[-1] if path_parts else ""

        # 检查 navigate 目标是否包含核心模块名
        # 或者 navigate 目标是否是 page_path 的子集
        if core_module and core_module not in target:
            # 可能是矛盾，但需要宽松匹配（目标可能是简写或包含额外描述）
            # 仅当目标中完全不包含 page_path 的任何一级时才报错
            all_parts_found = any(part in target for part in path_parts if len(part) >= 2)
            if not all_parts_found and len(target) >= 2:
                issues.append(_make_issue(
                    "V11", LEVEL_WARN,
                    f"操作链路 navigate 步骤[{i}] 目标「{target}」"
                    f"与 page_path「{page_path_str}」可能不一致",
                    f"operations_chain[{i}]"
                ))

    return issues


def _check_risk_identification(tp: dict) -> list:
    """
    V12: 风险点已识别
    检查逻辑：有 risk_flag 但无 risk_description 时应预警
    """
    issues = []

    # 检查测试点级别的 risk 标记
    risk_flag = tp.get("risk_flag", tp.get("has_risk", False))
    risk_desc = tp.get("risk_description", "")

    # 布尔标记
    if risk_flag is True:
        if not _is_non_empty_str(risk_desc):
            issues.append(_make_issue("V12", LEVEL_WARN,
                                      "risk_flag 为 True 但 risk_description 为空，风险描述未识别",
                                      "risk_description"))

    # 字符串标记（非空字符串视为有 flag）
    if isinstance(risk_flag, str) and _is_non_empty_str(risk_flag):
        if not _is_non_empty_str(risk_desc):
            issues.append(_make_issue("V12", LEVEL_WARN,
                                      f"risk_flag「{risk_flag}」已设置但 risk_description 为空",
                                      "risk_description"))

    # 检查 risk 列表中的条目
    risks = tp.get("related_risks", tp.get("risks", []))
    if isinstance(risks, list):
        for i, risk in enumerate(risks):
            if not isinstance(risk, dict):
                continue
            r_flag = risk.get("risk_flag", risk.get("severity", ""))
            r_desc = risk.get("description", risk.get("risk_description", ""))
            if r_flag and not _is_non_empty_str(r_desc):
                issues.append(_make_issue("V12", LEVEL_WARN,
                                          f"related_risks[{i}] 有标记但缺少描述",
                                          f"related_risks[{i}].description"))

    return issues


def _check_pci_identification(tp: dict) -> list:
    """
    V13: PCI 已识别
    检查逻辑：有 pci_flag 但无 pci_description 时应预警
    """
    issues = []

    # 检查测试点级别的 PCI 标记
    pci_flag = tp.get("pci_flag", tp.get("has_pci", tp.get("is_pci_blocked", False)))
    pci_desc = tp.get("pci_description", "")

    # 布尔标记
    if pci_flag is True:
        if not _is_non_empty_str(pci_desc):
            issues.append(_make_issue("V13", LEVEL_WARN,
                                      "pci_flag 为 True 但 pci_description 为空，PCI 描述未识别",
                                      "pci_description"))

    # 字符串标记
    if isinstance(pci_flag, str) and _is_non_empty_str(pci_flag):
        if not _is_non_empty_str(pci_desc):
            issues.append(_make_issue("V13", LEVEL_WARN,
                                      f"pci_flag「{pci_flag}」已设置但 pci_description 为空",
                                      "pci_description"))

    # 检查 pci 列表中的条目
    pcis = tp.get("related_pcis", tp.get("pcis", []))
    if isinstance(pcis, list):
        for i, pci in enumerate(pcis):
            if not isinstance(pci, dict):
                continue
            p_flag = pci.get("pci_flag", pci.get("blocking", pci.get("pci_status", "")))
            p_desc = pci.get("description", pci.get("question", pci.get("pci_description", "")))
            if p_flag and not _is_non_empty_str(p_desc):
                issues.append(_make_issue("V13", LEVEL_WARN,
                                          f"related_pcis[{i}] 有标记但缺少描述",
                                          f"related_pcis[{i}].description"))

    return issues


# ============================================================
# 批量校验
# ============================================================

def validate_batch(batch_points: list) -> dict:
    """
    对整批测试点执行完整性校验，返回校验报告。

    Args:
        batch_points: 测试点列表

    Returns:
        dict: 校验报告
            - total: 总数
            - passed: 通过数（无任何 issue）
            - failed: 失败数
            - force_issues: 强制项问题数
            - warn_issues: 预警项问题数
            - pass_rate: 通过率 (0.0 ~ 1.0)
            - details: {tp_id: [issues]}（仅包含有问题的）
            - summary: {code: count} 各检查项问题统计
    """
    if not isinstance(batch_points, list):
        return {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "force_issues": 0,
            "warn_issues": 0,
            "pass_rate": 0.0,
            "details": {},
            "summary": {},
            "error": "batch_points 不是列表类型",
        }

    all_details = {}
    total_force = 0
    total_warn = 0
    pass_count = 0
    summary_counter = {}

    for tp in batch_points:
        tp_id = tp.get("id", "UNKNOWN") if isinstance(tp, dict) else "UNKNOWN"
        issues = validate_prepared_point(tp)

        if not issues:
            pass_count += 1
        else:
            all_details[tp_id] = issues
            for issue in issues:
                code = issue.get("code", "?")
                summary_counter[code] = summary_counter.get(code, 0) + 1
                if issue.get("level") == LEVEL_FORCE:
                    total_force += 1
                else:
                    total_warn += 1

    total = len(batch_points)
    pass_rate = pass_count / total if total > 0 else 0.0

    return {
        "total": total,
        "passed": pass_count,
        "failed": len(all_details),
        "force_issues": total_force,
        "warn_issues": total_warn,
        "pass_rate": round(pass_rate, 4),
        "details": all_details,
        "summary": summary_counter,
    }


def validate_and_report(batch_points: list) -> str:
    """
    执行校验并返回人类可读的报告文本。

    Args:
        batch_points: 测试点列表

    Returns:
        str: 格式化的校验报告
    """
    report = validate_batch(batch_points)

    lines = [
        "=" * 60,
        "P5 自检验证报告",
        "=" * 60,
        f"总测试点数: {report['total']}",
        f"通过数: {report['passed']}",
        f"失败数: {report['failed']}",
        f"通过率: {report['pass_rate']:.1%}",
        f"强制项问题: {report['force_issues']}",
        f"预警项问题: {report['warn_issues']}",
        "-" * 60,
    ]

    # 问题分布统计
    if report["summary"]:
        lines.append("问题分布:")
        for code in sorted(report["summary"].keys()):
            count = report["summary"][code]
            lines.append(f"  {code}: {count} 条")
        lines.append("-" * 60)

    # 详细问题
    if report["details"]:
        lines.append("详细问题:")
        for tp_id, issues in report["details"].items():
            lines.append(f"\n  [{tp_id}]")
            for issue in issues:
                level_tag = "❌" if issue["level"] == LEVEL_FORCE else "⚠️"
                lines.append(f"    {level_tag} {issue['code']} | {issue['message']}")
    else:
        lines.append("✅ 所有测试点自检通过！")

    lines.append("=" * 60)
    return "\n".join(lines)
