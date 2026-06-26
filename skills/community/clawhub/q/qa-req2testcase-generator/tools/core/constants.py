#!/usr/bin/env python3
"""
core/constants.py — 全局常量
"""

import os

# ============================================================
# 版本与步骤
# ============================================================

SKILL_VERSION = "4.6.14"
STEPS = ["onboarding", "step0", "step0_8", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "step7"]
GATE_STEPS = ["onboarding", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"]

# HMAC固定密钥（V4.0.1: 避免文件内容变化导致密钥断裂）
HMAC_SECRET = "xy-req2testcase-v4-hmac-2026"

# P6分批大小（V4.0.1: 提取为全局常量，便于灰度调整）
P6_BATCH_SIZE = 8

# ============================================================
# 各步骤必需字段（以云端实际JSON为真源，2026-04-29统一）
# ============================================================

P0_REQUIRED_FIELDS = ["quality_score", "blocks", "objective"]
P1_REQUIRED_FIELDS = ["feature_tree"]
P3_REQUIRED_FIELDS = ["risk_points"]
P4_REQUIRED_FIELDS = ["pci_list"]
P5_REQUIRED_FIELDS = ["test_points", "merge_log"]
P6_REQUIRED_FIELDS = ["testcases"]
P7_REQUIRED_FIELDS = ["gate_result"]

# ============================================================
# 域识别关键词
# ============================================================

DOMAIN_KEYWORDS = {
    "trade": ["交易", "委托", "撤单", "成交", "清算", "结算", "资金冻结", "T+1"],
    "asset_mgmt": ["资管", "净值", "申赎", "申购", "赎回", "衍生品", "期货", "期权", "保证金"],
    "risk_ctrl": ["风控", "预警", "限额", "合规检查", "风险控制"],
    "crm": ["客户", "跟进", "开户", "KYC", "客户经理", "客户关系"],
    "etrading": ["网上营业厅", "APP", "适当性", "产品推荐", "在线交易", "移动端", "H5"],
    "ops_mgmt": ["运营", "活动", "营销", "后台管理", "数据报表", "统计", "导出"],
    "compliance": ["合规", "证书", "从业", "监管", "报送", "资质", "执照"],
    "it_infra": ["部署", "监控", "服务器", "权限配置", "变更", "IT", "基础设施", "投行", "承销", "IPO"],
}

# ============================================================
# 域名→文件名映射
# ============================================================

DOMAIN_FILENAME_MAP = {
    "客户域": "客户", "交易域": "交易", "资管域": "资管", "自营域": "自营",
    "投顾域": "投顾", "投研域": "投研", "投行业务域": "投行", "机构业务域": "机构",
    "清算托管域": "清算托管", "风控合规域": "风控合规", "行情资讯域": "行情资讯", "互联网终端域": "互联网终端"
}

# ============================================================
# P6模式推荐映射表 (V3.4.0)
# ============================================================

MODEL_RECOMMENDATIONS = {
    "deepseek-v4": "turbo",
    "deepseek-v4-pro": "turbo",
    "DeepSeek-V4-Pro": "turbo",
    "claude-sonnet-4": "turbo",
    "claude-opus-4": "turbo",
    "gpt-4o": "turbo",
    "gpt-5": "turbo",
    "minimax-m2": "hybrid",
    "minimax-m2.7": "hybrid",
    "qwen-max": "hybrid",
    "qwen3": "hybrid",
    "glm-4": "hybrid",
    "doubao": "hybrid",
    "doubao-seed-2.0-pro": "hybrid",
}
DEFAULT_P6_MODE_RECOMMENDATION = "hybrid"

VALID_P6_MODES = {"turbo", "hybrid", "strict"}

# ============================================================
# Prompt文件映射
# ============================================================

PROMPT_FILES = {
    "P0": "prompts/P0_requirement_structuring.md",
    "P1": "prompts/P1_feature_tree_generation.md",
    "P2": "prompts/P2_test_point_draft.md",
    "P3": "prompts/P3_risk_identification.md",
    "P4": "prompts/P4_pci_identification.md",
    "P5": "prompts/P5_test_point_merge.md",
    "P6": "prompts/P6_testcase_generation.md",
    "P7": "prompts/archive/P7_quality_gate.md",
}

# 每步需要的上游产物
UPSTREAM_FILES = {
    "P0": ["task_meta.json"],
    "P1": ["p0_output.json"],
    "P2": ["p1_output.json"],
    "P3": ["p1_output.json"],
    "P4": ["p1_output.json"],
    "P5": ["p2_output.json", "p3_output.json", "p4_output.json"],
    "P6": [],
    "P7": ["p6_output.json"],
}

# 知识注入映射
KNOWLEDGE_INJECT = {
    "P0": ["knowledge/industry/{domain}.md", "knowledge/methodology/design_methods.md"],
    "P1": ["knowledge/methodology/design_methods.md"],
    "P2": ["knowledge/methodology/boundary_rules.md", "knowledge/methodology/api_test_standard.md"],
    "P3": ["knowledge/industry/{domain}.md"],
    "P4": ["knowledge/industry/{domain}.md"],
    "P5": [],
    "P6": ["knowledge/company_standards/testcase_design_spec.md"],
    "P7": [],
}

# ============================================================
# 每步最小产出数量
# ============================================================

MIN_OUTPUT_COUNTS = {
    "P0": {"blocks.operations|blocks.pages|blocks.business_rules": 1},
    "P1": {"feature_tree.modules|modules": 2},
    "P2": {"test_points": 8},
    "P3": {"risk_points": 1},
    "P4": {"pci_list": 1},
    "P5": {"test_points": 10},
    "P6": {"testcases": 15},
}

# P6用例质量规则
P6_QUALITY_RULES = {
    "smoke_ratio_min": 0.05,
    "smoke_ratio_max": 0.20,
    "p0_ratio_max": 0.20,
    "all_same_priority": False,
    "per_requirement_smoke": True,
}

# ============================================================
# SKILL_DIR自动发现
# ============================================================

DEFAULT_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================
# V3.5.2: gate合法来源映射表
# ============================================================

_VALID_GATE_SOURCES = {
    "onboarding": ["onboarding"],
    "step0": ["step0"],
    "step0_8": ["step0_8_save"],
    "P0": ["step_run", "quality_check"],
    "P1": ["step_run", "quality_check"],
    "P2": ["p2_code_generate", "quality_check"],
    "P3": ["step_run", "quality_check"],
    "P4": ["step_run", "quality_check"],
    "P5": ["p5_code_merge", "quality_check"],
    "P6": ["p6_merge", "quality_check"],
    "P7": ["p7_code_check", "quality_check"],
}
