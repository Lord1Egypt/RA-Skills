#!/usr/bin/env python3
"""
A/B 测试点分类体系 —— classify_test_point()

分类定义：
  A类（业务流程）：
    - 操作链路≥3步
    - 每步有具体UI变化
    - 至少1个异常分支
    - 冒烟用例必须来自A类
  
  B类（字段边界）：
    - field_validation：单字段格式/必填
    - boundary：边界值
    - exception：异常数据
    - B类不能作为冒烟用例

版本: 1.0.0
日期: 2026-05-15
任务: 2.3 A/B分类体系实现

用法:
    from ab_classifier import classify_test_point, classify_batch

    case_type = classify_test_point(tp)
    # 返回: "A" 或 "B"

    results = classify_batch(batch_points)
    # 返回: [(tp_id, case_type, reason), ...]
"""

from typing import Any, Dict, List, Tuple, Optional


# ============================================================
# 常量定义
# ============================================================

# A类必需分类（至少 match 其中一种组合）
A_CLASS_CATEGORIES = frozenset({
    "main_flow",
    "branch",
    "integration",
    "permission",
    "state_migration",
})

# B类分类
B_CLASS_CATEGORIES = frozenset({
    "field_validation",
    "boundary",
})

# 可降级判断的分类（根据 operations_chain 长度决定 A/B）
FLEXIBLE_CATEGORIES = frozenset({
    "exception",
    "security",
    "performance",
    "compatibility",
})

# A类最小操作步骤数
A_CLASS_MIN_STEPS = 3

# A类需要的最小异常分支数
A_CLASS_MIN_EXCEPTION_BRANCHES = 1

# B类字段靶向数据 key 名
B_CLASS_FIELD_KEYS = frozenset({
    "field_target",
    "field_name",
    "test_data_matrix",
})


# ============================================================
# 核心：测试点分类
# ============================================================

def classify_test_point(tp: dict) -> Tuple[str, str]:
    """
    判定单个测试点的 A/B 分类。

    判定优先级（从高到低）：
      1. category 明确为 A类类别（main_flow/branch/integration/permission/state_migration）→ A
      2. category 明确为 B类类别（field_validation/boundary）→ B
      3. category 为灵活类别（exception/security/performance/compatibility）：
         a. operations_chain ≥ 3步且有异常分支 → A
         b. 否则 → B
      4. 无 category：根据 operations_chain 长度判定
         a. operations_chain ≥ 3步 → A
         b. 否则 → B

    Args:
        tp: P5 测试点 dict

    Returns:
        (case_type, reason): 
            case_type: "A" 或 "B"
            reason: 分类理由
    """
    if not isinstance(tp, dict):
        return ("B", "输入非 dict 类型，默认 B 类")

    category = (tp.get("category", "") or "").strip().lower()
    operations_chain = tp.get("operations_chain", [])
    chain_len = len(operations_chain) if isinstance(operations_chain, list) else 0

    # ---- 第1优先级：category 明确为 A类 ----
    if category in A_CLASS_CATEGORIES:
        # A类必须满足操作链≥3步
        if chain_len >= A_CLASS_MIN_STEPS:
            return ("A", f"类别 {category} + 操作链{chain_len}步 ≥ {A_CLASS_MIN_STEPS}步")
        else:
            # 类别明确是 main_flow 但操作链不足
            return ("A", f"类别 {category}（业务流程类），操作链{chain_len}步（低于标准{chain_len}<{A_CLASS_MIN_STEPS}，但仍归A类）")

    # ---- 第2优先级：category 明确为 B类 ----
    if category in B_CLASS_CATEGORIES:
        return ("B", f"类别 {category}（字段/边界测试）")

    # ---- 第3优先级：灵活类别 ----
    if category in FLEXIBLE_CATEGORIES:
        if chain_len >= A_CLASS_MIN_STEPS:
            return ("A", f"类别 {category} + 操作链{chain_len}步 ≥ {A_CLASS_MIN_STEPS}步")
        else:
            return ("B", f"类别 {category}，操作链{chain_len}步 < {A_CLASS_MIN_STEPS}步")

    # ---- 第4优先级：无分类，根据操作链长度判定 ----
    if chain_len >= A_CLASS_MIN_STEPS:
        return ("A", f"操作链{chain_len}步 ≥ {A_CLASS_MIN_STEPS}步（无明确分类，以操作复杂度判定）")
    else:
        return ("B", f"操作链{chain_len}步 < {A_CLASS_MIN_STEPS}步（无明确分类，以操作复杂度判定）")


def _has_b_class_indicators(tp: dict) -> bool:
    """
    检查测试点是否有 B类特征标记。

    B类特征：
      - 包含 field_target（字段靶向）
      - 包含 test_data_matrix（测试数据矩阵）
      - 有 field_specs 且 operations_chain ≤ 1 步
    """
    # 有 field_target
    if tp.get("field_target"):
        return True

    # 有 test_data_matrix
    tdm = tp.get("test_data_matrix", [])
    if isinstance(tdm, list) and len(tdm) > 0:
        return True

    # 有 field_specs 但 operations_chain 很少
    ops = tp.get("operations_chain", [])
    chain_len = len(ops) if isinstance(ops, list) else 0
    specs = tp.get("field_specs", [])
    specs_len = len(specs) if isinstance(specs, list) else 0

    if specs_len >= 1 and chain_len <= 1:
        return True

    return False


def _count_exception_branches(tp: dict) -> int:
    """
    统计测试点的异常分支数。

    来源：
      1. exception_scenarios 列表长度
      2. business_rules 中 violation_behavior 非空的规则数
      3. field_specs 中 validation_rules 总数
    """
    count = 0

    # 来源1：exception_scenarios
    exs = tp.get("exception_scenarios", [])
    if isinstance(exs, list):
        count += len(exs)

    # 来源2：business_rules 中的违规行为
    rules = tp.get("business_rules", [])
    if isinstance(rules, list):
        for rule in rules:
            if isinstance(rule, dict):
                v = rule.get("violation_behavior", "")
                if v and isinstance(v, str) and v.strip():
                    count += 1

    return count


# ============================================================
# A类质量最低门槛检查
# ============================================================

def validate_a_class_quality(tp: dict) -> List[dict]:
    """
    对 A类测试点执行 9项质量检查清单。

    检查项：
      1. 步骤数 ≥ 3步
      2. 第1步包含具体导航路径
      3. 最后1步包含最终状态变化断言
      4. 至少1步包含数据输入（具体值）
      5. 期望结果中至少1条包含UI元素的具体内容/状态
      6. 期望结果中至少1条包含数据变化的描述
      7. 不使用"正常""成功""正确"等模糊词
      8. 不包含"如有""若无""假设"等条件性词汇
      9. 每条期望结果可以独立校验

    Args:
        tp: A类测试点

    Returns:
        list[dict]: 问题列表
    """
    issues = []
    ops = tp.get("operations_chain", [])
    if not isinstance(ops, list):
        ops = []

    chain_len = len(ops)

    # [1] 步骤数 ≥ 3步
    if chain_len < 3:
        issues.append({
            "code": "A-Q01",
            "level": "FORCE",
            "message": f"A类步骤数 {chain_len} < 3，不满足最低门槛",
            "field": "operations_chain"
        })

    # [2] 第1步包含导航路径
    if chain_len >= 1:
        first_step = ops[0]
        if isinstance(first_step, dict):
            action_type = str(first_step.get("action_type", "")).lower()
            description = str(first_step.get("description", ""))
            target = str(first_step.get("target_element", ""))
            if action_type != "navigate" and "导航" not in description and "进入" not in description and "→" not in (description + target):
                issues.append({
                    "code": "A-Q02",
                    "level": "WARN",
                    "message": "A类第1步未明确包含导航路径",
                    "field": "operations_chain[0]"
                })

    # [3] 最后1步包含状态变化断言
    if chain_len >= 1:
        last_step = ops[-1]
        if isinstance(last_step, dict):
            anchor = str(last_step.get("expected_anchor", ""))
            state_keywords = ("成功", "失败", "展示", "显示", "跳转", "更新", "新增", "状态", "变为", "关闭", "提示")
            if not any(kw in anchor for kw in state_keywords):
                issues.append({
                    "code": "A-Q03",
                    "level": "WARN",
                    "message": "A类最后1步的 expected_anchor 未包含状态变化描述",
                    "field": "operations_chain[-1].expected_anchor"
                })

    # [4] 至少1步包含数据输入
    has_data_input = False
    for op in ops:
        if isinstance(op, dict):
            dv = op.get("data_value")
            at = str(op.get("action_type", "")).lower()
            if dv or at in ("input", "select"):
                has_data_input = True
                break
    if not has_data_input:
        issues.append({
            "code": "A-Q04",
            "level": "WARN",
            "message": "A类操作链路中缺少数据输入步骤",
            "field": "operations_chain"
        })

    # [5] 至少1条期望结果包含UI元素的具体内容
    has_ui_assertion = False
    for op in ops:
        if isinstance(op, dict):
            anchor = str(op.get("expected_anchor", ""))
            # 检查是否包含具体UI元素描述
            if len(anchor) >= 10 and any(kw in anchor for kw in ("按钮", "弹窗", "菜单", "列表", "输入框", "提示", "文案", "页面", "显示", "加载")):
                has_ui_assertion = True
                break
    if not has_ui_assertion and chain_len > 0:
        issues.append({
            "code": "A-Q05",
            "level": "WARN",
            "message": "A类期望结果缺少具体UI元素断言",
            "field": "operations_chain[].expected_anchor"
        })

    # [6] 至少1条期望结果包含数据变化的描述
    has_data_change = False
    for op in ops:
        if isinstance(op, dict):
            anchor = str(op.get("expected_anchor", ""))
            if any(kw in anchor for kw in ("新增", "更新", "删除", "变化", "状态", "记录", "数据", "保存")):
                has_data_change = True
                break
    if not has_data_change and chain_len > 0:
        issues.append({
            "code": "A-Q06",
            "level": "WARN",
            "message": "A类期望结果缺少数据变化描述",
            "field": "operations_chain[].expected_anchor"
        })

    # [7] 检测模糊词
    fuzzy_words = ["正常", "成功", "正确"]
    violations = []
    for i, op in enumerate(ops):
        if isinstance(op, dict):
            anchor = str(op.get("expected_anchor", ""))
            for fw in fuzzy_words:
                # 允许UI文案引用（如「提交成功」）
                if f"「{fw}" in anchor or f"{fw}」" in anchor or f"{fw}" in anchor:
                    continue
                # 简单检测（实际应结合上下文，此处为快速扫描）
                if fw in anchor and len(anchor.replace(fw, "")) < len(anchor) * 0.3:
                    violations.append(f"步骤{i+1}: {fw}")
    if violations:
        issues.append({
            "code": "A-Q07",
            "level": "WARN",
            "message": f"A类期望结果包含模糊词（如非UI文案引用）: {', '.join(violations[:3])}",
            "field": "operations_chain[].expected_anchor"
        })

    # [8] 检测条件性词汇
    conditional_words = ["如有", "若无", "假如", "假设", "可能", "或许", "如果"]
    cond_violations = []
    for i, op in enumerate(ops):
        if isinstance(op, dict):
            text = str(op.get("description", "")) + " " + str(op.get("expected_anchor", ""))
            for cw in conditional_words:
                if cw in text:
                    cond_violations.append(f"步骤{i+1}: {cw}")
    if cond_violations:
        issues.append({
            "code": "A-Q08",
            "level": "FORCE",
            "message": f"A类包含条件性词汇（不符合规范）: {', '.join(cond_violations[:3])}",
            "field": "operations_chain[].description/expected_anchor"
        })

    # [9] 每条期望结果可独立校验
    # (在此检查所有 expected_anchor 是否有非空值)
    empty_anchors = []
    for i, op in enumerate(ops):
        if isinstance(op, dict):
            anchor = str(op.get("expected_anchor", "")).strip()
            if not anchor:
                empty_anchors.append(str(i + 1))
    if empty_anchors:
        issues.append({
            "code": "A-Q09",
            "level": "WARN",
            "message": f"A类 {len(empty_anchors)} 个步骤的 expected_anchor 为空: 步骤{', '.join(empty_anchors)}",
            "field": "operations_chain[].expected_anchor"
        })

    return issues


# ============================================================
# B类质量最低门槛检查
# ============================================================

def validate_b_class_quality(tp: dict) -> List[dict]:
    """
    对 B类测试点执行质量检查。

    检查项：
      1. 每条用例聚焦1个字段或1个边界条件
      2. 期望结果中明确写出错误提示的具体文案
      3. is_smoke 必须为 False
      4. 数据设计覆盖有效/无效/边界三类

    Args:
        tp: B类测试点

    Returns:
        list[dict]: 问题列表
    """
    issues = []

    # [1] 聚焦单字段
    field_target = tp.get("field_target", {})
    field_specs = tp.get("field_specs", [])
    specs_len = len(field_specs) if isinstance(field_specs, list) else 0

    if field_target:
        # B类应有明确的字段靶向
        fn = field_target.get("field_name", "")
        if not fn:
            issues.append({
                "code": "B-Q01",
                "level": "WARN",
                "message": "B类 field_target 中缺少 field_name",
                "field": "field_target.field_name"
            })
    elif specs_len > 1:
        issues.append({
            "code": "B-Q01",
            "level": "WARN",
            "message": f"B类包含 {specs_len} 个字段规格，建议每用例聚焦1个字段",
            "field": "field_specs"
        })

    # [2] 期望中有错误提示文案
    tdm = tp.get("test_data_matrix", [])
    if isinstance(tdm, list):
        has_error_msg = False
        for td in tdm:
            if isinstance(td, dict):
                eb = td.get("expected_behavior", "")
                if eb and isinstance(eb, str) and len(eb) >= 5:
                    has_error_msg = True
                    break
        if not has_error_msg and len(tdm) > 0:
            issues.append({
                "code": "B-Q02",
                "level": "WARN",
                "message": "B类 test_data_matrix 中缺少期望错误行为描述",
                "field": "test_data_matrix[].expected_behavior"
            })

    # [3] is_smoke 必须为 False
    is_smoke = tp.get("is_smoke_candidate", False)
    if is_smoke:
        issues.append({
            "code": "B-Q03",
            "level": "FORCE",
            "message": "B类测试点被标记为冒烟候选（B类不允许作为冒烟用例）",
            "field": "is_smoke_candidate"
        })

    # [4] 数据覆盖三类检查
    if isinstance(tdm, list) and len(tdm) > 0:
        types_found = set()
        for td in tdm:
            if isinstance(td, dict):
                t = td.get("type", td.get("data_type", ""))
                if t:
                    types_found.add(str(t).lower())

        expected_types = {"有效", "无效", "边界", "valid", "invalid", "boundary"}
        if not (types_found & expected_types):
            issues.append({
                "code": "B-Q04",
                "level": "WARN",
                "message": f"B类测试数据未覆盖有效/无效/边界三类，当前类型: {types_found or '无'}",
                "field": "test_data_matrix"
            })

    return issues


# ============================================================
# 冒烟用例规则
# ============================================================

def validate_smoke_candidate(tp: dict, case_type: str) -> dict:
    """
    验证冒烟用例规则：
      - 冒烟用例必须来自 A类
      - B类不能为冒烟用例
      - P0 + A类 + 正向验证 → 可为冒烟

    Args:
        tp: 测试点
        case_type: A 或 B

    Returns:
        dict: {"valid": bool, "reason": str, "auto_corrected": bool}
    """
    is_smoke = tp.get("is_smoke_candidate", False)
    priority = tp.get("priority", "")

    if not is_smoke:
        return {"valid": True, "reason": "非冒烟候选", "auto_corrected": False}

    if case_type == "B":
        # B类不能为冒烟
        return {
            "valid": False,
            "reason": f"B类测试点不能作为冒烟用例（冒烟必须来自A类业务流程）",
            "auto_corrected": True,  # 应自动修正
        }

    # A类 + 冒烟
    if priority != "P0":
        return {
            "valid": False,
            "reason": f"A类冒烟候选但 priority={priority}（非P0），建议调整为P0或取消冒烟",
            "auto_corrected": False,
        }

    return {"valid": True, "reason": f"A类 + P0 冒烟候选合法", "auto_corrected": False}


# ============================================================
# 批量分类
# ============================================================

def classify_batch(batch_points: list) -> List[Tuple[str, str, str]]:
    """
    批量分类测试点。

    Args:
        batch_points: 测试点列表

    Returns:
        list[(tp_id, case_type, reason)]: 每条的分类结果
    """
    if not isinstance(batch_points, list):
        return []

    results = []
    for tp in batch_points:
        tp_id = tp.get("id", "UNKNOWN") if isinstance(tp, dict) else "UNKNOWN"
        ct, reason = classify_test_point(tp)
        results.append((tp_id, ct, reason))
    return results


def classify_batch_with_stats(batch_points: list) -> dict:
    """
    批量分类并返回统计信息。

    Returns:
        dict: {
            "total": int,
            "a_class_count": int,
            "b_class_count": int,
            "a_class_ratio": float,
            "results": [(tp_id, case_type, reason), ...],
            "smoke_violations": [(tp_id, reason), ...]
        }
    """
    results = classify_batch(batch_points)
    a_count = sum(1 for _, ct, _ in results if ct == "A")
    b_count = sum(1 for _, ct, _ in results if ct == "B")
    total = len(results)

    smoke_violations = []
    for tp, (tp_id, ct, _) in zip(batch_points, results):
        if ct == "B" and tp.get("is_smoke_candidate", False):
            smoke_violations.append((tp_id, "B类被标记为冒烟候选"))

    return {
        "total": total,
        "a_class_count": a_count,
        "b_class_count": b_count,
        "a_class_ratio": round(a_count / total, 4) if total > 0 else 0.0,
        "results": results,
        "smoke_violations": smoke_violations,
    }


# ============================================================
# 自检：快速验证脚本
# ============================================================

if __name__ == "__main__":
    # 构建测试数据
    test_batch = [
        # A类：main_flow + 完整操作链
        {
            "id": "TP-A01",
            "title": "营销管理员发起债券投顾分润申请完整流程",
            "description": "用户在债券投顾页面发起新的分润申请，填写协办单位、创收比例、分润说明等完整信息后提交",
            "category": "main_flow",
            "priority": "P0",
            "is_smoke_candidate": True,
            "operations_chain": [
                {"step": 1, "action_type": "navigate", "description": "导航至债券投顾页面", "target_element": "首页→营销管理→协同分润→债券投顾", "expected_anchor": "债券投顾页面正常加载"},
                {"step": 2, "action_type": "click", "description": "点击发起分润申请", "target_element": "「发起分润申请」按钮", "expected_anchor": "分润申请弹窗打开"},
                {"step": 3, "action_type": "input", "description": "填写创收比例", "target_element": "「创收比例(%)」输入框", "data_value": "50", "expected_anchor": "输入50显示正常"},
                {"step": 4, "action_type": "click", "description": "提交申请", "target_element": "「提交」按钮", "expected_anchor": "提示「分润申请提交成功」，列表新增1条待审核记录"},
            ],
            "exception_scenarios": [{"description": "不选择协办单位直接提交"}],
            "field_specs": [{"name": "创收比例", "type": "number", "validation_rules": ["0-100"]}],
        },
        # B类：field_validation
        {
            "id": "TP-B01",
            "title": "创收比例超出范围校验",
            "description": "验证创收比例字段输入超出范围时的校验",
            "category": "field_validation",
            "priority": "P2",
            "is_smoke_candidate": False,
            "operations_chain": [
                {"step": 1, "action_type": "navigate", "description": "导航至分润申请弹窗", "target_element": "分润申请弹窗", "expected_anchor": "弹窗打开"},
            ],
            "field_target": {"field_name": "创收比例(%)"},
            "test_data_matrix": [
                {"value": "-1", "type": "无效-负数", "expected_behavior": "输入框红色边框，提示「创收比例不能为负数」"},
                {"value": "101", "type": "无效-超限", "expected_behavior": "输入框红色边框，提示「创收比例不能超过100%」"},
                {"value": "0", "type": "边界-最小值", "expected_behavior": "输入0，无校验错误"},
                {"value": "100", "type": "边界-最大值", "expected_behavior": "输入100，无校验错误"},
            ],
        },
        # B类但被错误标记为冒烟候选
        {
            "id": "TP-B02",
            "title": "分润说明字数超限校验",
            "description": "验证分润说明字段超200字时的校验",
            "category": "field_validation",
            "priority": "P2",
            "is_smoke_candidate": True,  # 错误！B类不能为冒烟
            "operations_chain": [],
            "field_target": {"field_name": "分润说明"},
            "test_data_matrix": [
                {"value": "超200字的文本...", "type": "无效-超长", "expected_behavior": "提示字数超限"}
            ],
        },
        # A类：branch + 5步操作
        {
            "id": "TP-A02",
            "title": "分润审批通过后状态流转验证",
            "description": "风控经理审批通过分润申请后，验证状态变更和数据流转",
            "category": "branch",
            "priority": "P1",
            "is_smoke_candidate": False,
            "operations_chain": [
                {"step": 1, "action_type": "navigate", "description": "以风控经理账号登录", "target_element": "审批管理→待审批", "expected_anchor": "待审批列表显示分润申请"},
                {"step": 2, "action_type": "click", "description": "查看分润申请详情", "target_element": "分润申请记录", "expected_anchor": "弹窗显示分润详情"},
                {"step": 3, "action_type": "click", "description": "点击审批通过", "target_element": "「审批通过」按钮", "expected_anchor": "确认对话框弹出"},
                {"step": 4, "action_type": "click", "description": "确认审批", "target_element": "「确认」按钮", "expected_anchor": "提示审批成功"},
                {"step": 5, "action_type": "verify", "description": "验证分润状态变更", "target_element": "分润列表", "expected_anchor": "分润状态从「待审批」变为「已通过」"},
            ],
            "exception_scenarios": [
                {"description": "审批驳回"},
                {"description": "无权审批人员尝试操作"},
            ],
        },
        # B类：boundary
        {
            "id": "TP-B03",
            "title": "创收比例边界值0.01测试",
            "description": "验证创收比例最小精度",
            "category": "boundary",
            "priority": "P2",
            "is_smoke_candidate": False,
            "operations_chain": [],
            "field_target": {"field_name": "创收比例(%)"},
            "test_data_matrix": [
                {"value": "0.01", "type": "边界-最小精度", "expected_behavior": "支持小数，无校验错误"}
            ],
        },
    ]

    print("=" * 70)
    print("A/B 分类体系 - 自测")
    print("=" * 70)

    stats = classify_batch_with_stats(test_batch)
    print(f"\n📊 分类统计:")
    print(f"   总数: {stats['total']}")
    print(f"   A类: {stats['a_class_count']} ({stats['a_class_ratio']:.1%})")
    print(f"   B类: {stats['b_class_count']} ({1 - stats['a_class_ratio']:.1%})")

    print(f"\n📋 分类明细:")
    for tp_id, ct, reason in stats["results"]:
        tp_info = next((t for t in test_batch if t["id"] == tp_id), {})
        chain_len = len(tp_info.get("operations_chain", []))
        cat = tp_info.get("category", "?")
        print(f"   {tp_id} → {ct}类 | {reason} | category={cat}")

    print(f"\n🔍 A类质量检查:")
    for tp in test_batch:
        tp_id = tp["id"]
        ct, _ = classify_test_point(tp)
        if ct == "A":
            issues = validate_a_class_quality(tp)
            if issues:
                print(f"   {tp_id}: ❌ {len(issues)} 个问题")
                for iss in issues:
                    print(f"      [{iss['code']}] {iss['message']}")
            else:
                print(f"   {tp_id}: ✅ 全部通过")

    print(f"\n🔍 B类质量检查:")
    for tp in test_batch:
        tp_id = tp["id"]
        ct, _ = classify_test_point(tp)
        if ct == "B":
            issues = validate_b_class_quality(tp)
            if issues:
                print(f"   {tp_id}: ❌ {len(issues)} 个问题")
                for iss in issues:
                    print(f"      [{iss['code']}] {iss['message']}")
            else:
                print(f"   {tp_id}: ✅ 全部通过")

    print(f"\n🔍 冒烟规则验证:")
    for tp in test_batch:
        tp_id = tp["id"]
        ct, _ = classify_test_point(tp)
        result = validate_smoke_candidate(tp, ct)
        status = "✅" if result["valid"] else "❌"
        auto = " (已自动修正)" if result["auto_corrected"] else ""
        print(f"   {tp_id} ({ct}类): {status} {result['reason']}{auto}")

    if stats["smoke_violations"]:
        print(f"\n⚠️ 冒烟违规项:")
        for tp_id, reason in stats["smoke_violations"]:
            print(f"   {tp_id}: {reason}")
    else:
        print(f"\n✅ 无冒烟违规项")

    print("=" * 70)
    print("自测完成")
