#!/usr/bin/env python3
"""
p5_validate.py 单元测试
覆盖 _validate_prepared_point() 的13项检查 + 边界场景 + validate_batch()

运行方式:
    python -m pytest test_p5_validate.py -v
    或
    python test_p5_validate.py
"""

import sys
import os
import unittest

# 将当前目录加入 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from p5_validate import (
    validate_prepared_point,
    validate_batch,
    validate_and_report,
    LEVEL_FORCE,
    LEVEL_WARN,
    _make_issue,
)


# ============================================================
# 辅助函数：构造标准测试数据
# ============================================================

def _make_valid_test_point(**overrides) -> dict:
    """
    构造一个通过所有13项检查的标准测试点。
    可通过 **overrides 覆盖任意字段以触发特定检查。
    """
    base = {
        "id": "TP-001",
        "title": "债券投顾分润申请完整流程",
        "description": "用户在债券投顾页面发起新的分润申请，填写协办单位、创收比例、分润说明等完整信息后提交",
        "category": "main_flow",
        "priority": "P0",
        "page_path": {
            "full_path": "首页 → 营销管理 → 协同分润 → 债券投顾",
            "hierarchy": ["首页", "营销管理", "协同分润", "债券投顾"],
        },
        "operations_chain": [
            {"step": 1, "action_type": "navigate", "description": "导航到债券投顾页面",
             "target": "首页→营销管理→协同分润→债券投顾"},
            {"step": 2, "action_type": "click", "description": "点击发起分润申请按钮",
             "target_element": "「发起分润申请」按钮"},
            {"step": 3, "action_type": "input", "description": "填写分润信息并提交",
             "target_element": "分润信息表单"},
        ],
        "field_specs": [
            {"name": "协办单位", "type": "select", "constraints": {"required": True}},
        ],
        "business_rules": [
            {"rule_id": "BR-001", "description": "分润比例总和必须为100%"},
        ],
        "precondition": {
            "environment": {"system": "CRM", "module": "营销管理"},
            "account": {"role": "营销管理员", "account_id": "admin001"},
            "data_preparation": ["预置至少1条债券投顾产品数据"],
        },
        "risk_flag": False,
        "pci_flag": False,
    }
    base.update(overrides)
    return base


def _get_issue_codes(issues: list) -> list:
    """从 issues 列表中提取所有 code"""
    return [i["code"] for i in issues]


def _has_code(issues: list, code: str) -> bool:
    """检查 issues 中是否包含指定 code"""
    return any(i["code"] == code for i in issues)


def _get_by_code(issues: list, code: str) -> list:
    """获取指定 code 的所有 issues"""
    return [i for i in issues if i["code"] == code]


# ============================================================
# 测试类
# ============================================================

class TestValidatePreparedPoint(unittest.TestCase):
    """13项检查逐一测试"""

    # ---- 全通过测试 ----

    def test_all_pass(self):
        """标准测试点应通过所有13项检查"""
        tp = _make_valid_test_point()
        issues = validate_prepared_point(tp)
        self.assertEqual(len(issues), 0, f"期望全部通过，但有以下问题: {issues}")

    # ---- V01: page_path 非空 ----

    def test_v01_page_path_missing(self):
        """V01: page_path 缺失"""
        tp = _make_valid_test_point()
        del tp["page_path"]
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V01"))

    def test_v01_page_path_empty_string(self):
        """V01: page_path 为空字符串"""
        tp = _make_valid_test_point(page_path="")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V01"))

    def test_v01_page_path_empty_dict(self):
        """V01: page_path 为空 dict"""
        tp = _make_valid_test_point(page_path={})
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V01"))

    def test_v01_page_path_none(self):
        """V01: page_path 为 None"""
        tp = _make_valid_test_point(page_path=None)
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V01"))

    def test_v01_page_path_valid_string(self):
        """V01: page_path 为有效字符串"""
        tp = _make_valid_test_point(page_path="首页→营销管理→协同分润")
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V01"))

    def test_v01_page_path_hierarchy_only(self):
        """V01: page_path dict 只有 hierarchy（无 full_path）"""
        tp = _make_valid_test_point(page_path={"hierarchy": ["首页", "模块A"]})
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V01"))

    # ---- V02: operations_chain 至少1步 ----

    def test_v02_operations_chain_empty(self):
        """V02: operations_chain 为空列表"""
        tp = _make_valid_test_point(operations_chain=[])
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V02"))

    def test_v02_operations_chain_missing(self):
        """V02: operations_chain 缺失"""
        tp = _make_valid_test_point()
        del tp["operations_chain"]
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V02"))

    def test_v02_operations_chain_not_list(self):
        """V02: operations_chain 不是列表"""
        tp = _make_valid_test_point(operations_chain="navigate→click")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V02"))

    def test_v02_operations_chain_one_step(self):
        """V02: operations_chain 只有1步（应通过）"""
        tp = _make_valid_test_point(
            operations_chain=[{"step": 1, "action_type": "click", "description": "点击按钮"}]
        )
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V02"))

    # ---- V03: field_specs 至少1个 ----

    def test_v03_field_specs_empty(self):
        """V03: field_specs 为空列表"""
        tp = _make_valid_test_point(field_specs=[])
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V03"))

    def test_v03_field_specs_missing(self):
        """V03: field_specs 缺失"""
        tp = _make_valid_test_point()
        del tp["field_specs"]
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V03"))

    # ---- V04: business_rules 至少1条 ----

    def test_v04_business_rules_empty(self):
        """V04: business_rules 为空列表（WARN级别）"""
        tp = _make_valid_test_point(business_rules=[])
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V04"))
        v04_issues = _get_by_code(issues, "V04")
        self.assertEqual(v04_issues[0]["level"], LEVEL_WARN)

    def test_v04_business_rules_missing(self):
        """V04: business_rules 缺失"""
        tp = _make_valid_test_point()
        del tp["business_rules"]
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V04"))

    # ---- V05: description 长度 ≥ 20 ----

    def test_v05_description_too_short(self):
        """V05: description 不足20字符"""
        tp = _make_valid_test_point(description="太短了")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V05"))

    def test_v05_description_exactly_20(self):
        """V05: description 恰好20字符"""
        tp = _make_valid_test_point(description="12345678901234567890")
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V05"))

    def test_v05_description_19_chars(self):
        """V05: description 19字符"""
        tp = _make_valid_test_point(description="1234567890123456789")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V05"))

    def test_v05_description_empty(self):
        """V05: description 为空"""
        tp = _make_valid_test_point(description="")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V05"))

    # ---- V06: category 有效值 ----

    def test_v06_category_invalid(self):
        """V06: category 无效值"""
        tp = _make_valid_test_point(category="invalid_category")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V06"))

    def test_v06_category_empty(self):
        """V06: category 为空"""
        tp = _make_valid_test_point(category="")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V06"))

    def test_v06_category_valid_boundary(self):
        """V06: category 各种有效值"""
        for cat in ["main_flow", "boundary", "security", "exception", "field_validation"]:
            tp = _make_valid_test_point(category=cat)
            issues = validate_prepared_point(tp)
            self.assertFalse(_has_code(issues, "V06"), f"category={cat} 应通过")

    # ---- V07: priority 有效值 ----

    def test_v07_priority_invalid(self):
        """V07: priority 无效值"""
        tp = _make_valid_test_point(priority="P5")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V07"))

    def test_v07_priority_empty(self):
        """V07: priority 为空"""
        tp = _make_valid_test_point(priority="")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V07"))

    def test_v07_priority_all_valid(self):
        """V07: P0-P4 全部有效"""
        for pri in ["P0", "P1", "P2", "P3", "P4"]:
            tp = _make_valid_test_point(priority=pri)
            issues = validate_prepared_point(tp)
            self.assertFalse(_has_code(issues, "V07"), f"priority={pri} 应通过")

    # ---- V08: 前置条件完整性 ----

    def test_v08_precondition_missing(self):
        """V08: precondition 缺失"""
        tp = _make_valid_test_point()
        del tp["precondition"]
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V08"))
        v08 = _get_by_code(issues, "V08")
        self.assertEqual(v08[0]["level"], LEVEL_FORCE)

    def test_v08_precondition_empty_dict(self):
        """V08: precondition 为空 dict（缺三要素）"""
        tp = _make_valid_test_point(precondition={})
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V08"))

    def test_v08_precondition_missing_account(self):
        """V08: precondition 缺少 account"""
        tp = _make_valid_test_point(
            precondition={
                "environment": {"system": "CRM"},
                "data_preparation": ["预置数据"],
            }
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V08"))

    def test_v08_precondition_missing_environment(self):
        """V08: precondition 缺少 environment"""
        tp = _make_valid_test_point(
            precondition={
                "account": {"role": "admin"},
                "data_preparation": ["预置数据"],
            }
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V08"))

    def test_v08_precondition_missing_data_preparation(self):
        """V08: precondition 缺少 data_preparation"""
        tp = _make_valid_test_point(
            precondition={
                "environment": {"system": "CRM"},
                "account": {"role": "admin"},
            }
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V08"))

    def test_v08_precondition_string_format(self):
        """V08: precondition 为字符串格式（WARN级别）"""
        tp = _make_valid_test_point(precondition="用户已登录系统并具备相应权限")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V08"))
        v08 = _get_by_code(issues, "V08")
        self.assertEqual(v08[0]["level"], LEVEL_WARN)

    def test_v08_precondition_empty_string(self):
        """V08: precondition 为空字符串"""
        tp = _make_valid_test_point(precondition="")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V08"))
        v08 = _get_by_code(issues, "V08")
        self.assertEqual(v08[0]["level"], LEVEL_FORCE)

    # ---- V09: 操作链路步骤连贯性 ----

    def test_v09_step_gap(self):
        """V09: 步骤序号跳跃 (1, 3, 5)"""
        tp = _make_valid_test_point(
            operations_chain=[
                {"step": 1, "action_type": "navigate", "description": "导航"},
                {"step": 3, "action_type": "click", "description": "点击"},
                {"step": 5, "action_type": "input", "description": "输入"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V09"))

    def test_v09_step_duplicate(self):
        """V09: 步骤序号重复 (1, 2, 2)"""
        tp = _make_valid_test_point(
            operations_chain=[
                {"step": 1, "action_type": "navigate", "description": "导航"},
                {"step": 2, "action_type": "click", "description": "点击"},
                {"step": 2, "action_type": "input", "description": "输入"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V09"))

    def test_v09_step_wrong_start(self):
        """V09: 起始序号不是1"""
        tp = _make_valid_test_point(
            operations_chain=[
                {"step": 0, "action_type": "navigate", "description": "导航"},
                {"step": 1, "action_type": "click", "description": "点击"},
                {"step": 2, "action_type": "input", "description": "输入"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V09"))

    def test_v09_step_continuous(self):
        """V09: 连续序号 (1, 2, 3) 应通过"""
        tp = _make_valid_test_point()  # 默认就是 1, 2, 3
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V09"))

    def test_v09_step_implicit_numbering(self):
        """V09: 无 step 字段时使用隐式序号"""
        tp = _make_valid_test_point(
            operations_chain=[
                {"action_type": "navigate", "description": "导航"},
                {"action_type": "click", "description": "点击"},
                {"action_type": "input", "description": "输入"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V09"), "无 step 字段时按索引隐式编号应通过")

    def test_v09_step_invalid_type(self):
        """V09: step 值非整数"""
        tp = _make_valid_test_point(
            operations_chain=[
                {"step": "one", "action_type": "navigate", "description": "导航"},
                {"step": "two", "action_type": "click", "description": "点击"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V09"))

    def test_v09_step_empty_chain_skip(self):
        """V09: 空列表不报错（由V02覆盖）"""
        tp = _make_valid_test_point(operations_chain=[])
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V09"))

    # ---- V10: 字段规格完整性 ----

    def test_v10_field_spec_missing_name(self):
        """V10: field_spec 缺少 name"""
        tp = _make_valid_test_point(
            field_specs=[{"type": "input", "constraints": {"required": True}}]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V10"))

    def test_v10_field_spec_missing_type(self):
        """V10: field_spec 缺少 type"""
        tp = _make_valid_test_point(
            field_specs=[{"name": "字段A", "constraints": {"required": True}}]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V10"))

    def test_v10_field_spec_missing_constraints(self):
        """V10: field_spec 缺少 constraints"""
        tp = _make_valid_test_point(
            field_specs=[{"name": "字段A", "type": "input"}]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V10"))

    def test_v10_field_spec_with_validation_rules(self):
        """V10: field_spec 有 validation_rules 等同于 constraints"""
        tp = _make_valid_test_point(
            field_specs=[{"name": "字段A", "type": "input", "validation_rules": {"max_length": 50}}]
        )
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V10"))

    def test_v10_field_spec_complete(self):
        """V10: 完整的 field_spec"""
        tp = _make_valid_test_point(
            field_specs=[{"name": "字段A", "type": "input", "constraints": {"required": True}}]
        )
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V10"))

    def test_v10_field_spec_not_dict(self):
        """V10: field_spec 不是 dict"""
        tp = _make_valid_test_point(field_specs=["字段A", "字段B"])
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V10"))

    def test_v10_empty_specs_skip(self):
        """V10: 空 field_specs 不报错（由V03覆盖）"""
        tp = _make_valid_test_point(field_specs=[])
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V10"))

    # ---- V11: 无矛盾信息 ----

    def test_v11_no_contradiction(self):
        """V11: page_path 与 operations_chain 一致"""
        tp = _make_valid_test_point()
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V11"))

    def test_v11_contradicting_navigate(self):
        """V11: navigate 目标与 page_path 不一致"""
        tp = _make_valid_test_point(
            operations_chain=[
                {"step": 1, "action_type": "navigate",
                 "description": "导航", "target": "完全无关的页面XXX"},
                {"step": 2, "action_type": "click", "description": "点击"},
                {"step": 3, "action_type": "input", "description": "输入"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V11"))

    def test_v11_no_navigate_steps(self):
        """V11: 无 navigate 步骤时跳过检查"""
        tp = _make_valid_test_point(
            operations_chain=[
                {"step": 1, "action_type": "click", "description": "点击"},
                {"step": 2, "action_type": "input", "description": "输入"},
                {"step": 3, "action_type": "verify", "description": "验证"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V11"))

    def test_v11_no_page_path_skip(self):
        """V11: page_path 为空时跳过检查"""
        tp = _make_valid_test_point(page_path="")
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V11"))

    # ---- V12: 风险点已识别 ----

    def test_v12_risk_flag_true_no_desc(self):
        """V12: risk_flag=True 但无 risk_description"""
        tp = _make_valid_test_point(risk_flag=True, risk_description="")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V12"))

    def test_v12_risk_flag_true_with_desc(self):
        """V12: risk_flag=True 且有 risk_description（应通过）"""
        tp = _make_valid_test_point(risk_flag=True, risk_description="存在数据一致性风险")
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V12"))

    def test_v12_risk_flag_false(self):
        """V12: risk_flag=False（无需描述，应通过）"""
        tp = _make_valid_test_point(risk_flag=False, risk_description="")
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V12"))

    def test_v12_risk_string_flag_no_desc(self):
        """V12: risk_flag 为字符串但无描述"""
        tp = _make_valid_test_point(risk_flag="high", risk_description="")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V12"))

    def test_v12_related_risks_without_desc(self):
        """V12: related_risks 中有条目但缺描述"""
        tp = _make_valid_test_point(
            related_risks=[
                {"risk_flag": True, "description": ""},
                {"risk_flag": "medium", "description": "有描述"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V12"))

    # ---- V13: PCI 已识别 ----

    def test_v13_pci_flag_true_no_desc(self):
        """V13: pci_flag=True 但无 pci_description"""
        tp = _make_valid_test_point(pci_flag=True, pci_description="")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V13"))

    def test_v13_pci_flag_true_with_desc(self):
        """V13: pci_flag=True 且有 pci_description（应通过）"""
        tp = _make_valid_test_point(pci_flag=True, pci_description="需要确认分润规则细节")
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V13"))

    def test_v13_pci_flag_false(self):
        """V13: pci_flag=False（无需描述，应通过）"""
        tp = _make_valid_test_point(pci_flag=False, pci_description="")
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V13"))

    def test_v13_pci_string_flag_no_desc(self):
        """V13: pci_flag 为字符串但无描述"""
        tp = _make_valid_test_point(pci_flag="blocker", pci_description="")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V13"))

    def test_v13_related_pcis_without_desc(self):
        """V13: related_pcis 中有条目但缺描述"""
        tp = _make_valid_test_point(
            related_pcis=[
                {"pci_flag": True, "description": ""},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V13"))


class TestValidateBatch(unittest.TestCase):
    """批量校验测试"""

    def test_batch_all_pass(self):
        """所有测试点通过"""
        batch = [_make_valid_test_point(id=f"TP-{i:03d}") for i in range(5)]
        report = validate_batch(batch)
        self.assertEqual(report["total"], 5)
        self.assertEqual(report["passed"], 5)
        self.assertEqual(report["failed"], 0)
        self.assertEqual(report["pass_rate"], 1.0)
        self.assertEqual(report["details"], {})

    def test_batch_mixed(self):
        """部分通过部分失败"""
        batch = [
            _make_valid_test_point(id="TP-001"),
            _make_valid_test_point(id="TP-002", description="太短"),
            _make_valid_test_point(id="TP-003", category="invalid"),
        ]
        report = validate_batch(batch)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["passed"], 1)
        self.assertEqual(report["failed"], 2)
        self.assertIn("TP-002", report["details"])
        self.assertIn("TP-003", report["details"])

    def test_batch_empty(self):
        """空批次"""
        report = validate_batch([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["passed"], 0)
        self.assertEqual(report["pass_rate"], 0.0)

    def test_batch_invalid_input(self):
        """非列表输入"""
        report = validate_batch("not a list")
        self.assertEqual(report["total"], 0)
        self.assertIn("error", report)

    def test_batch_summary(self):
        """汇总统计"""
        batch = [
            _make_valid_test_point(id="TP-001", description="短"),
            _make_valid_test_point(id="TP-002", description="也短"),
        ]
        report = validate_batch(batch)
        self.assertIn("V05", report["summary"])
        self.assertEqual(report["summary"]["V05"], 2)


class TestValidateAndReport(unittest.TestCase):
    """报告格式测试"""

    def test_report_all_pass(self):
        """全部通过的报告"""
        batch = [_make_valid_test_point(id="TP-001")]
        report_text = validate_and_report(batch)
        self.assertIn("通过率: 100.0%", report_text)
        self.assertIn("✅", report_text)

    def test_report_with_issues(self):
        """有问题的报告"""
        batch = [_make_valid_test_point(id="TP-001", description="短")]
        report_text = validate_and_report(batch)
        self.assertIn("V05", report_text)
        self.assertIn("TP-001", report_text)


class TestEdgeCases(unittest.TestCase):
    """边界场景测试"""

    def test_none_input(self):
        """输入为 None"""
        issues = validate_prepared_point(None)
        self.assertTrue(len(issues) > 0)
        self.assertEqual(issues[0]["code"], "V00")

    def test_empty_dict(self):
        """输入为空 dict"""
        issues = validate_prepared_point({})
        codes = _get_issue_codes(issues)
        # 应触发多项检查
        self.assertIn("V01", codes)  # page_path
        self.assertIn("V02", codes)  # operations_chain
        self.assertIn("V05", codes)  # description
        self.assertIn("V06", codes)  # category
        self.assertIn("V07", codes)  # priority

    def test_whitespace_description(self):
        """description 为纯空白"""
        tp = _make_valid_test_point(description="   ")
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V05"))

    def test_operations_chain_with_non_dict_items(self):
        """operations_chain 中有非 dict 项"""
        tp = _make_valid_test_point(
            operations_chain=[
                "not a dict",
                {"step": 2, "action_type": "click", "description": "点击"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V09"))

    def test_page_path_string_with_path(self):
        """page_path 为字符串路径"""
        tp = _make_valid_test_point(page_path="首页>营销管理>债券投顾")
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V01"))

    def test_all_valid_categories(self):
        """所有有效 category"""
        for cat in ["main_flow", "branch", "integration", "permission",
                     "exception", "boundary", "field_validation", "security",
                     "state_migration", "performance", "compatibility"]:
            tp = _make_valid_test_point(category=cat)
            issues = validate_prepared_point(tp)
            self.assertFalse(_has_code(issues, "V06"), f"category={cat} should pass")

    def test_field_specs_empty_name(self):
        """field_spec name 为空字符串"""
        tp = _make_valid_test_point(
            field_specs=[{"name": "", "type": "input", "constraints": {"required": True}}]
        )
        issues = validate_prepared_point(tp)
        self.assertTrue(_has_code(issues, "V10"))

    def test_contradiction_with_matching_path(self):
        """navigate 目标包含 page_path 的最后一级（应通过）"""
        tp = _make_valid_test_point(
            operations_chain=[
                {"step": 1, "action_type": "navigate",
                 "target": "进入债券投顾页面"},
                {"step": 2, "action_type": "click", "description": "点击"},
                {"step": 3, "action_type": "input", "description": "输入"},
            ]
        )
        issues = validate_prepared_point(tp)
        self.assertFalse(_has_code(issues, "V11"))


# ============================================================
# 运行入口
# ============================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
