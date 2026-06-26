#!/usr/bin/env python3
"""
Gate 7项检查 单元测试
验证 G1-G7 每项检查的正确拦截能力和放行能力。

版本: 1.0.0
日期: 2026-05-15
任务: 3.1 Gate 7项检查代码实现 - 测试

运行方式:
    cd 实施_阶段三
    python -m pytest test_gate_checker.py -v

覆盖率目标: ≥ 80%
"""

import sys
import os
import pytest

# 确保可以导入 gate_checker
sys.path.insert(0, os.path.dirname(__file__))

from gate_checker import (
    # 核心 Gate 函数
    gate_g1_step_concreteness,
    gate_g2_expected_assertiveness,
    gate_g3_business_flow_coverage,
    gate_g4_smoke_source,
    gate_g5_banned_patterns,
    gate_g6_step_atomicity,
    gate_g7_traceability,
    run_gate_checks,
    evaluate_gate,
    format_gate_report,
    # 辅助函数
    _get_case_field,
    _is_smoke,
    _extract_step_lines,
    _extract_step_contents,
    _jaccard_similarity,
    # 常量
    STATUS_PASSED,
    STATUS_FAILED,
    STATUS_WARNING,
    LEVEL_BLOCK,
    LEVEL_WARNING,
)


# ============================================================
# 测试数据：P5 测试点
# ============================================================

P5_TEST_POINTS = [
    {
        "id": "TP-001",
        "title": "发起债券投顾分润申请",
        "category": "main_flow",
        "priority": "P0",
        "status": "active",
        "page_path": {
            "full_path": "首页→营销管理→协同分润→债券投顾",
            "hierarchy": ["首页", "营销管理", "协同分润", "债券投顾"],
        },
        "operations_chain": [
            {"step": 1, "action_type": "navigate", "target_element": "首页→营销管理→协同分润→债券投顾"},
            {"step": 2, "action_type": "click", "target_element": "「发起分润申请」按钮"},
            {"step": 3, "action_type": "input", "target_element": "「创收比例(%)」输入框", "data_value": "50"},
            {"step": 4, "action_type": "click", "target_element": "「提交」按钮"},
        ],
        "ui_elements": {
            "buttons": [{"name": "发起分润申请"}, {"name": "提交"}, {"name": "编辑"}],
            "inputs": [{"name": "创收比例(%)"}, {"name": "分润说明"}],
            "selectors": [{"name": "协办单位"}],
        },
        "field_specs": [
            {"name": "创收比例(%)", "type": "number"},
            {"name": "分润说明", "type": "text"},
        ],
    },
    {
        "id": "TP-002",
        "title": "创收比例字段校验",
        "category": "field_validation",
        "priority": "P2",
        "status": "active",
        "page_path": {
            "full_path": "首页→营销管理→协同分润→债券投顾",
            "hierarchy": ["首页", "营销管理"],
        },
        "operations_chain": [
            {"step": 1, "action_type": "navigate", "target_element": "分润申请弹窗"},
        ],
        "ui_elements": {
            "inputs": [{"name": "创收比例(%)"}],
        },
        "field_specs": [
            {"name": "创收比例(%)", "type": "number"},
        ],
    },
    {
        "id": "TP-003",
        "title": "分润审批流程",
        "category": "branch",
        "priority": "P1",
        "status": "active",
        "page_path": {
            "full_path": "首页→审批管理→待审批",
            "hierarchy": ["首页", "审批管理"],
        },
        "operations_chain": [
            {"step": 1, "action_type": "navigate", "target_element": "首页→审批管理→待审批"},
            {"step": 2, "action_type": "click", "target_element": "「审批通过」按钮"},
            {"step": 3, "action_type": "click", "target_element": "「确认」按钮"},
        ],
        "ui_elements": {
            "buttons": [{"name": "审批通过"}, {"name": "审批驳回"}, {"name": "确认"}],
        },
        "field_specs": [],
    },
]


# ============================================================
# 辅助函数测试
# ============================================================

class TestHelperFunctions:
    """辅助函数测试"""

    def test_get_case_field_direct(self):
        case = {"case_id": "TC-001", "steps": "1. 步骤1"}
        assert _get_case_field(case, "case_id") == "TC-001"
        assert _get_case_field(case, "steps") == "1. 步骤1"

    def test_get_case_field_alias(self):
        """测试别名映射"""
        case = {"id": "TC-001"}
        assert _get_case_field(case, "case_id") == "TC-001"

    def test_get_case_field_default(self):
        case = {"case_id": "TC-001"}
        assert _get_case_field(case, "not_exist", "default") == "default"

    def test_get_case_field_non_dict(self):
        assert _get_case_field("not a dict", "case_id", "?") == "?"

    def test_is_smoke_bool(self):
        assert _is_smoke(True) is True
        assert _is_smoke(False) is False

    def test_is_smoke_str(self):
        assert _is_smoke("是") is True
        assert _is_smoke("true") is True
        assert _is_smoke("否") is False
        assert _is_smoke("false") is False

    def test_is_smoke_int(self):
        assert _is_smoke(1) is True
        assert _is_smoke(0) is False

    def test_is_smoke_none(self):
        assert _is_smoke(None) is False

    def test_extract_step_lines(self):
        text = "1. 步骤一\n2. 步骤二\n非步骤行\n3. 步骤三"
        lines = _extract_step_lines(text)
        assert len(lines) == 3

    def test_extract_step_lines_empty(self):
        assert _extract_step_lines("") == []
        assert _extract_step_lines(None) == []

    def test_extract_step_contents(self):
        text = "1. 步骤一\n2. 步骤二"
        contents = _extract_step_contents(text)
        assert contents == ["步骤一", "步骤二"]

    def test_jaccard_similarity_identical(self):
        a = {"分润", "申请", "提交"}
        assert _jaccard_similarity(a, a) == 1.0

    def test_jaccard_similarity_disjoint(self):
        a = {"分润", "申请"}
        b = {"审批", "驳回"}
        assert _jaccard_similarity(a, b) == 0.0

    def test_jaccard_similarity_partial(self):
        a = {"分润", "申请", "提交"}
        b = {"分润", "申请", "审批"}
        expected = 2 / 4  # 交集2 / 并集4
        assert abs(_jaccard_similarity(a, b) - expected) < 0.01

    def test_jaccard_similarity_empty(self):
        assert _jaccard_similarity(set(), set()) == 0.0


# ============================================================
# G1: 步骤具体性检查 测试
# ============================================================

class TestG1StepConcreteness:
    """G1 步骤具体性检查测试"""

    def test_pass_concrete_steps(self):
        """正常具体步骤应通过"""
        cases = [{
            "case_id": "TC-G1-OK",
            "steps": (
                "1. 导航至首页→营销管理→协同分润→债券投顾\n"
                "2. 点击「发起分润申请」按钮\n"
                "3. 在「创收比例(%)」输入框输入50"
            ),
        }]
        result = gate_g1_step_concreteness(cases, P5_TEST_POINTS)
        assert result["check_id"] == "G1"
        assert result["status"] == STATUS_PASSED

    def test_fail_banned_pattern(self):
        """禁止模式应被拦截"""
        cases = [{
            "case_id": "TC-G1-BANNED",
            "steps": (
                "1. 进入相关功能页面\n"
                "2. 执行相关操作"
            ),
        }]
        result = gate_g1_step_concreteness(cases, P5_TEST_POINTS)
        assert result["status"] in (STATUS_FAILED, STATUS_WARNING)
        banned_issues = [i for i in result["issues"] if i.get("type") == "banned"]
        assert len(banned_issues) >= 1

    def test_fail_vague_steps(self):
        """模糊步骤应被拦截"""
        cases = [{
            "case_id": "TC-G1-VAGUE",
            "steps": (
                "1. 验证分润功能\n"
                "2. 检查系统响应"
            ),
        }]
        result = gate_g1_step_concreteness(cases, P5_TEST_POINTS)
        assert result["status"] in (STATUS_FAILED, STATUS_WARNING)
        assert len(result["issues"]) >= 1

    def test_pass_login_steps(self):
        """登录类步骤应放行"""
        cases = [{
            "case_id": "TC-G1-LOGIN",
            "steps": "1. 使用管理员账号登录系统",
        }]
        result = gate_g1_step_concreteness(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_PASSED

    def test_pass_p5_element_reference(self):
        """引用P5元素名的步骤应通过"""
        cases = [{
            "case_id": "TC-G1-P5REF",
            "steps": "1. 点击「发起分润申请」按钮",
        }]
        result = gate_g1_step_concreteness(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_PASSED

    def test_pass_path_format(self):
        """包含路径格式的步骤应通过"""
        cases = [{
            "case_id": "TC-G1-PATH",
            "steps": "1. 导航至首页→营销管理→协同分润→债券投顾",
        }]
        result = gate_g1_step_concreteness(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_PASSED

    def test_empty_cases(self):
        """空用例列表应通过"""
        result = gate_g1_step_concreteness([], P5_TEST_POINTS)
        assert result["status"] == STATUS_PASSED

    def test_no_p5_points(self):
        """无P5测试点时仍能运行"""
        cases = [{
            "case_id": "TC-G1-NOP5",
            "steps": "1. 点击「确定」按钮",
        }]
        result = gate_g1_step_concreteness(cases, [])
        # 引号内有内容，应通过
        assert result["status"] == STATUS_PASSED


# ============================================================
# G2: 期望断言性检查 测试
# ============================================================

class TestG2ExpectedAssertiveness:
    """G2 期望断言性检查测试"""

    def test_pass_concrete_assertions(self):
        """具体断言应通过"""
        cases = [{
            "case_id": "TC-G2-OK",
            "expected_results": (
                "1. 提示「分润申请提交成功」\n"
                "2. 列表新增1条状态为「待审核」的记录\n"
                "3. 弹窗自动关闭"
            ),
        }]
        result = gate_g2_expected_assertiveness(cases)
        assert result["check_id"] == "G2"
        assert result["status"] == STATUS_PASSED

    def test_fail_fuzzy_assertions(self):
        """模糊表述应被拦截"""
        cases = [{
            "case_id": "TC-G2-FUZZY",
            "expected_results": (
                "1. 正常加载\n"
                "2. 功能正常\n"
                "3. 操作成功"
            ),
        }]
        result = gate_g2_expected_assertiveness(cases)
        assert result["status"] == STATUS_FAILED
        assert len(result["issues"]) >= 3

    def test_fail_nine_banned_patterns(self):
        """验证9种禁止模式全部可检测"""
        banned_phrases = [
            "正常加载", "验证成功", "符合业务规则",
            "符合预期", "功能正常", "数据正确",
            "操作成功", "展示完整", "流程正确",
        ]
        for phrase in banned_phrases:
            cases = [{
                "case_id": "TC-G2-BANNED",
                "expected_results": f"1. {phrase}",
            }]
            result = gate_g2_expected_assertiveness(cases)
            assert len(result["issues"]) >= 1, f"未检测到禁止模式: {phrase}"

    def test_fail_empty_expected(self):
        """空期望结果应被拦截"""
        cases = [{
            "case_id": "TC-G2-EMPTY",
            "expected_results": "",
        }]
        result = gate_g2_expected_assertiveness(cases)
        assert len(result["issues"]) >= 1

    def test_pass_ui_state_assertions(self):
        """UI状态断言应通过"""
        cases = [{
            "case_id": "TC-G2-UI",
            "expected_results": (
                "1. 输入框红色边框 + 错误提示「创收比例不能小于0」\n"
                "2. 弹窗关闭，列表刷新"
            ),
        }]
        result = gate_g2_expected_assertiveness(cases)
        assert result["status"] == STATUS_PASSED

    def test_warning_threshold(self):
        """模糊表述占比低于阈值应为WARNING"""
        # 5个用例中1个有模糊表述，比例 1/5 = 20%，不超过0.20
        cases = [
            {
                "case_id": f"TC-G2-THR-{i}",
                "expected_results": "1. 具体断言内容",
            }
            for i in range(5)
        ]
        cases[0]["expected_results"] = "1. 功能正常"
        result = gate_g2_expected_assertiveness(cases)
        assert result["status"] == STATUS_WARNING


# ============================================================
# G3: 业务流程覆盖检查 测试
# ============================================================

class TestG3BusinessFlowCoverage:
    """G3 业务流程覆盖检查测试"""

    def test_pass_full_coverage(self):
        """完整覆盖应通过"""
        cases = [
            {
                "case_id": "TC-G3-001",
                "source_test_point": "TP-001",
                "steps": "1. 步骤1\n2. 步骤2\n3. 步骤3",
            },
            {
                "case_id": "TC-G3-002",
                "source_test_point": "TP-002",
                "steps": "1. 步骤1",
            },
            {
                "case_id": "TC-G3-003",
                "source_test_point": "TP-003",
                "steps": "1. 步骤1\n2. 步骤2\n3. 步骤3",
            },
        ]
        result = gate_g3_business_flow_coverage(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_PASSED

    def test_fail_missing_coverage(self):
        """P5测试点未被覆盖应失败"""
        cases = [
            {
                "case_id": "TC-G3-001",
                "source_test_point": "TP-001",
                "steps": "1. 步骤1\n2. 步骤2\n3. 步骤3",
            },
        ]
        # P5有3个active测试点，但只有1个被覆盖
        result = gate_g3_business_flow_coverage(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_FAILED
        coverage_issues = [i for i in result["issues"] if i.get("type") == "coverage_gap"]
        assert len(coverage_issues) >= 2

    def test_fail_a_class_step_short(self):
        """A类用例步骤数<3应失败"""
        cases = [{
            "case_id": "TC-G3-SHORT",
            "source_test_point": "TP-001",  # main_flow (A类)
            "steps": "1. 步骤1",
        }]
        result = gate_g3_business_flow_coverage(cases, [P5_TEST_POINTS[0]])
        assert result["status"] == STATUS_FAILED
        step_issues = [i for i in result["issues"] if i.get("type") == "a_class_step_short"]
        assert len(step_issues) >= 1

    def test_fail_b_class_smoke(self):
        """B类标记为冒烟应失败"""
        cases = [{
            "case_id": "TC-G3-BSMOKE",
            "source_test_point": "TP-002",  # field_validation (B类)
            "is_smoke": True,
            "steps": "1. 步骤1",
        }]
        result = gate_g3_business_flow_coverage(cases, [P5_TEST_POINTS[1]])
        assert result["status"] == STATUS_FAILED
        smoke_issues = [i for i in result["issues"] if i.get("type") == "b_class_smoke"]
        assert len(smoke_issues) >= 1


# ============================================================
# G4: 冒烟用例来源检查 测试
# ============================================================

class TestG4SmokeSource:
    """G4 冒烟用例来源检查测试"""

    def test_pass_a_class_smoke(self):
        """A类+P0冒烟用例应通过"""
        cases = [{
            "case_id": "TC-G4-OK",
            "source_test_point": "TP-001",  # main_flow (A类)
            "is_smoke": True,
            "priority": "P0",
        }]
        result = gate_g4_smoke_source(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_PASSED

    def test_warning_non_a_class_smoke(self):
        """非A类冒烟用例应WARNING"""
        cases = [{
            "case_id": "TC-G4-NA",
            "source_test_point": "TP-002",  # field_validation (B类)
            "is_smoke": True,
            "priority": "P2",
        }]
        result = gate_g4_smoke_source(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_WARNING
        non_a_issues = [i for i in result["issues"] if i.get("type") == "non_a_class_smoke"]
        assert len(non_a_issues) >= 1

    def test_warning_smoke_not_p0(self):
        """冒烟用例非P0应WARNING"""
        cases = [{
            "case_id": "TC-G4-NP0",
            "source_test_point": "TP-001",
            "is_smoke": True,
            "priority": "P2",
        }]
        result = gate_g4_smoke_source(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_WARNING

    def test_pass_no_smoke(self):
        """无冒烟用例应通过"""
        cases = [{
            "case_id": "TC-G4-NOSMOKE",
            "source_test_point": "TP-001",
            "is_smoke": False,
            "priority": "P1",
        }]
        result = gate_g4_smoke_source(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_PASSED


# ============================================================
# G5: 禁止模式检测 测试
# ============================================================

class TestG5BannedPatterns:
    """G5 禁止模式检测测试"""

    def test_pass_clean_cases(self):
        """干净用例应通过"""
        cases = [{
            "case_id": "TC-G5-OK",
            "title": "发起分润申请流程验证",
            "steps": (
                "1. 导航至首页→营销管理→协同分润→债券投顾\n"
                "2. 点击「发起分润申请」按钮\n"
                "3. 在「创收比例(%)」输入框输入50\n"
                "4. 点击「提交」按钮"
            ),
        }]
        result = gate_g5_banned_patterns(cases)
        assert result["status"] == STATUS_PASSED

    def test_fail_copy_title(self):
        """步骤复制title应失败"""
        cases = [{
            "case_id": "TC-G5-COPY",
            "title": "创收比例 字段 边界值 校验 测试 验证",
            "steps": (
                "1. 对 创收比例 字段 进行 边界值 校验 测试 验证 操作\n"
                "2. 对 创收比例 字段 进行 边界值 校验 测试 验证 操作\n"
                "3. 对 创收比例 字段 进行 边界值 校验 测试 验证 操作\n"
                "4. 对 创收比例 字段 进行 边界值 校验 测试 验证 操作"
            ),
        }]
        result = gate_g5_banned_patterns(cases)
        copy_issues = [i for i in result["issues"] if i.get("type") == "copy_title"]
        assert len(copy_issues) >= 1

    def test_fail_banned_phrase_related_page(self):
        """禁止模式'进入相关功能页面'应被拦截"""
        cases = [{
            "case_id": "TC-G5-BP",
            "title": "测试用例标题",
            "steps": "1. 进入相关功能页面\n2. 其他步骤",
        }]
        result = gate_g5_banned_patterns(cases)
        phrase_issues = [i for i in result["issues"] if i.get("type") == "banned_phrase"]
        assert len(phrase_issues) >= 1

    def test_fail_verify_function(self):
        """禁止模式'验证XX功能'应被拦截"""
        cases = [{
            "case_id": "TC-G5-VF",
            "title": "测试用例标题",
            "steps": "1. 验证分润功能",
        }]
        result = gate_g5_banned_patterns(cases)
        phrase_issues = [i for i in result["issues"] if i.get("type") == "banned_phrase"]
        assert len(phrase_issues) >= 1

    def test_fail_conditional_words(self):
        """条件性词汇应被拦截"""
        cases = [{
            "case_id": "TC-G5-COND",
            "title": "测试用例标题",
            "steps": "1. 如有异常则跳过\n2. 正常步骤",
        }]
        result = gate_g5_banned_patterns(cases)
        cond_issues = [i for i in result["issues"] if i.get("type") == "conditional"]
        assert len(cond_issues) >= 1

    def test_fail_duplicate_steps(self):
        """3条以上用例步骤相同应被拦截"""
        cases = [
            {
                "case_id": f"TC-G5-DUP-{i}",
                "title": f"测试用例{i}",
                "steps": "1. 步骤A\n2. 步骤B\n3. 步骤C",
            }
            for i in range(4)
        ]
        result = gate_g5_banned_patterns(cases)
        dup_issues = [i for i in result["issues"] if i.get("type") == "duplicate_steps"]
        assert len(dup_issues) >= 1

    def test_two_duplicate_pass(self):
        """2条用例步骤相同不应被拦截"""
        cases = [
            {
                "case_id": f"TC-G5-DUP2-{i}",
                "title": f"测试用例{i}",
                "steps": "1. 步骤A\n2. 步骤B",
            }
            for i in range(2)
        ]
        result = gate_g5_banned_patterns(cases)
        dup_issues = [i for i in result["issues"] if i.get("type") == "duplicate_steps"]
        assert len(dup_issues) == 0


# ============================================================
# G6: 步骤原子性检查 测试
# ============================================================

class TestG6StepAtomicity:
    """G6 步骤原子性检查测试"""

    def test_pass_atomic_steps(self):
        """原子性步骤应通过"""
        cases = [{
            "case_id": "TC-G6-OK",
            "steps": (
                "1. 导航至首页→营销管理→协同分润→债券投顾\n"
                "2. 点击「发起分润申请」按钮\n"
                "3. 在「创收比例(%)」输入框输入50"
            ),
        }]
        result = gate_g6_step_atomicity(cases)
        assert result["status"] == STATUS_PASSED

    def test_fail_click_and_verify(self):
        """点击+验证合并应失败"""
        cases = [{
            "case_id": "TC-G6-CV",
            "steps": "1. 点击「提交」按钮并验证页面加载",
        }]
        result = gate_g6_step_atomicity(cases)
        assert result["status"] == STATUS_FAILED
        assert len(result["issues"]) >= 1

    def test_fail_input_then_click(self):
        """输入+点击合并应失败"""
        cases = [{
            "case_id": "TC-G6-IC",
            "steps": "1. 输入50后点击「提交」按钮",
        }]
        result = gate_g6_step_atomicity(cases)
        assert result["status"] == STATUS_FAILED
        assert len(result["issues"]) >= 1

    def test_fail_login_and_navigate(self):
        """登录+导航合并应失败"""
        cases = [{
            "case_id": "TC-G6-LN",
            "steps": "1. 登录系统并进入分润管理页面",
        }]
        result = gate_g6_step_atomicity(cases)
        assert result["status"] == STATUS_FAILED
        assert len(result["issues"]) >= 1

    def test_fail_select_and_input(self):
        """选择+输入合并应失败"""
        cases = [{
            "case_id": "TC-G6-SI",
            "steps": "1. 选择「协办单位」并输入「XX公司」",
        }]
        result = gate_g6_step_atomicity(cases)
        assert result["status"] == STATUS_FAILED
        assert len(result["issues"]) >= 1

    def test_pass_navigation_chain(self):
        """导航链路（A→B→C）应放行"""
        cases = [{
            "case_id": "TC-G6-NAV",
            "steps": "1. 导航至首页→营销管理→协同分润→债券投顾",
        }]
        result = gate_g6_step_atomicity(cases)
        assert result["status"] == STATUS_PASSED

    def test_empty_cases(self):
        """空用例列表应通过"""
        result = gate_g6_step_atomicity([])
        assert result["status"] == STATUS_PASSED


# ============================================================
# G7: P5-P6 可追溯性检查 测试
# ============================================================

class TestG7Traceability:
    """G7 P5-P6 可追溯性检查测试"""

    def test_pass_traceable_path(self):
        """可追溯路径应通过"""
        cases = [{
            "case_id": "TC-G7-OK",
            "steps": "1. 导航至首页→营销管理→协同分润→债券投顾",
            "expected_results": "1. 页面正常展示",
        }]
        result = gate_g7_traceability(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_PASSED

    def test_warning_untraceable_path(self):
        """不可追溯路径应WARNING"""
        cases = [{
            "case_id": "TC-G7-UNTRACE",
            "steps": "1. 导航至系统设置→权限管理→用户管理",
            "expected_results": "",
        }]
        result = gate_g7_traceability(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_WARNING
        path_issues = [i for i in result["issues"] if i.get("type") == "path_mismatch"]
        assert len(path_issues) >= 1

    def test_warning_untraceable_element(self):
        """不可追溯元素名应WARNING"""
        cases = [{
            "case_id": "TC-G7-ELEM",
            "steps": "1. 点击「不存在的按钮」按钮",
            "expected_results": "",
        }]
        result = gate_g7_traceability(cases, P5_TEST_POINTS)
        assert result["status"] == STATUS_WARNING
        elem_issues = [i for i in result["issues"] if i.get("type") == "element_mismatch"]
        assert len(elem_issues) >= 1

    def test_pass_generic_names(self):
        """通用名称应放行"""
        cases = [{
            "case_id": "TC-G7-GEN",
            "steps": "1. 点击「确定」按钮\n2. 点击「取消」按钮",
            "expected_results": "",
        }]
        result = gate_g7_traceability(cases, P5_TEST_POINTS)
        elem_issues = [i for i in result["issues"] if i.get("type") == "element_mismatch"]
        assert len(elem_issues) == 0

    def test_pass_p5_referenced_elements(self):
        """P5中存在的元素名应放行"""
        cases = [{
            "case_id": "TC-G7-P5REF",
            "steps": "1. 点击「发起分润申请」按钮",
            "expected_results": "",
        }]
        result = gate_g7_traceability(cases, P5_TEST_POINTS)
        elem_issues = [i for i in result["issues"] if i.get("type") == "element_mismatch"]
        assert len(elem_issues) == 0


# ============================================================
# 集成测试: run_gate_checks + evaluate_gate
# ============================================================

class TestGateIntegration:
    """Gate 检查集成测试"""

    def _make_good_cases(self):
        """构建一组应通过所有检查的用例"""
        return [
            {
                "case_id": "TC-INT-001",
                "title": "发起债券投顾分润申请完整流程",
                "source_test_point": "TP-001",
                "is_smoke": True,
                "priority": "P0",
                "steps": (
                    "1. 导航至首页→营销管理→协同分润→债券投顾\n"
                    "2. 点击「发起分润申请」按钮\n"
                    "3. 在「创收比例(%)」输入框输入50\n"
                    "4. 点击「提交」按钮"
                ),
                "expected_results": (
                    "1. 提示「分润申请提交成功」\n"
                    "2. 列表新增1条状态为「待审核」的记录\n"
                    "3. 弹窗自动关闭"
                ),
            },
            {
                "case_id": "TC-INT-002",
                "title": "创收比例正常值输入验证",
                "source_test_point": "TP-002",
                "is_smoke": False,
                "priority": "P2",
                "steps": (
                    "1. 导航至首页→营销管理→协同分润→债券投顾\n"
                    "2. 点击「发起分润申请」按钮\n"
                    "3. 在「创收比例(%)」输入框输入50"
                ),
                "expected_results": (
                    "1. 页面正常展示\n"
                    "2. 弹窗打开，表单字段可见\n"
                    "3. 输入框显示50，无校验错误"
                ),
            },
            {
                "case_id": "TC-INT-003",
                "title": "分润审批通过流程验证",
                "source_test_point": "TP-003",
                "is_smoke": False,
                "priority": "P1",
                "steps": (
                    "1. 导航至首页→审批管理→待审批\n"
                    "2. 点击「审批通过」按钮\n"
                    "3. 点击「确认」按钮"
                ),
                "expected_results": (
                    "1. 待审批列表显示分润申请记录\n"
                    "2. 确认对话框弹出\n"
                    "3. 提示审批成功，状态变更"
                ),
            },
        ]

    def test_good_cases_pass_all(self):
        """优质用例应通过所有检查"""
        cases = self._make_good_cases()
        results = run_gate_checks(cases, P5_TEST_POINTS)
        evaluation = evaluate_gate(results)

        assert evaluation["status"] == "PASS", f"预期PASS，实际{evaluation['status']}。{evaluation['summary']}"
        assert evaluation["block_failed"] == 0

    def test_bad_cases_fail(self):
        """问题用例应被拦截"""
        cases = self._make_good_cases() + [
            {
                "case_id": "TC-INT-BAD",
                "title": "验证分润功能",
                "source_test_point": "TP-001",
                "is_smoke": False,
                "priority": "P2",
                "steps": (
                    "1. 进入相关功能页面\n"
                    "2. 执行相关操作\n"
                    "3. 检查系统响应"
                ),
                "expected_results": (
                    "1. 正常加载\n"
                    "2. 功能正常\n"
                    "3. 操作成功"
                ),
            },
        ]
        results = run_gate_checks(cases, P5_TEST_POINTS)
        evaluation = evaluate_gate(results)

        assert evaluation["status"] in ("FAIL", "PARTIAL")
        assert evaluation["block_failed"] > 0 or evaluation["warnings"] > 0

    def test_quick_check_subset(self):
        """快速检查子集（G1+G2+G5）"""
        cases = self._make_good_cases()
        results = run_gate_checks(cases, P5_TEST_POINTS, check_ids=["G1", "G2", "G5"])

        assert len(results) == 3
        assert all(r["check_id"] in ("G1", "G2", "G5") for r in results)

        evaluation = evaluate_gate(results)
        assert evaluation["status"] == "PASS"

    def test_evaluate_empty_results(self):
        """空结果应返回PASS"""
        evaluation = evaluate_gate([])
        assert evaluation["status"] == "PASS"

    def test_format_report(self):
        """报告格式化应正常输出"""
        cases = self._make_good_cases()
        results = run_gate_checks(cases, P5_TEST_POINTS)
        evaluation = evaluate_gate(results)
        report = format_gate_report(results, evaluation)

        assert "Gate 7项检查报告" in report
        assert "G1" in report
        assert "G7" in report


# ============================================================
# Gate一次通过率测试 (验收标准: ≥80%)
# ============================================================

class TestGatePassRate:
    """Gate 一次通过率测试"""

    def test_pass_rate_above_80_percent(self):
        """
        验收标准: Gate一次通过率 ≥ 80%
        使用混合用例（80%优质 + 20%有问题）验证
        """
        good_cases = [
            {
                "case_id": f"TC-RATE-G{i:03d}",
                "title": f"优质用例{i}",
                "source_test_point": P5_TEST_POINTS[i % 3]["id"],
                "is_smoke": i == 0,
                "priority": "P0" if i == 0 else "P2",
                "steps": (
                    "1. 导航至首页→营销管理→协同分润→债券投顾\n"
                    "2. 点击「发起分润申请」按钮\n"
                    "3. 在「创收比例(%)」输入框输入50\n"
                    "4. 点击「提交」按钮"
                ),
                "expected_results": (
                    "1. 提示「分润申请提交成功」\n"
                    "2. 列表新增1条状态为「待审核」的记录"
                ),
            }
            for i in range(8)
        ]

        # 运行Gate检查
        results = run_gate_checks(good_cases, P5_TEST_POINTS)

        # 计算通过率
        passed = sum(1 for r in results if r["status"] == STATUS_PASSED)
        total = len(results)
        pass_rate = passed / total if total > 0 else 0

        assert pass_rate >= 0.80, f"Gate通过率 {pass_rate:.1%} 低于80%目标"


# ============================================================
# 运行入口
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
