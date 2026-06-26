#!/usr/bin/env python3
"""
V4.8.0 P6 引导卡生成器

为 LOW 档位模型生成「设计引导卡」，将测试方法论规则由代码消化后
嵌入到每个测试点的 prompt 中，使弱模型只需执行「设计」而非「理解规则 + 设计」。

用法:
    from tools.p6_guide import generate_guide_cards
    guides = generate_guide_cards(test_points, p0_data, p1_data, skill_dir)
    # → [{test_point_id, test_intent, step_pattern, key_ui, ...}, ...]
"""

import re

__version__ = "1.0.0"


# ============================================================
# Category → 引导模板映射（V4.8.0 完整版）
# ============================================================

CATEGORY_GUIDE_MAP = {
    # 正向验证
    "main_flow": {
        "test_intent": "正向验证：按主流程操作，验证预期结果正确出现",
        "step_pattern": ["进入页面", "触发操作", "填写数据", "提交/确认", "查看结果"],
        "expected_pattern": ["提示文案", "数据变化（N→N+1）", "字段值核对"],
    },
    # 异常验证
    "exception": {
        "test_intent": "异常验证：输入非法值/执行非法操作，验证系统拦截+错误提示",
        "step_pattern": ["进入页面", "输入异常值", "触发校验", "观察错误提示"],
        "expected_pattern": ["具体错误提示文案", "输入框红色边框", "提交按钮置灰/不可用"],
    },
    # 边界验证
    "boundary": {
        "test_intent": "边界验证：输入边界值（最小值/最大值/临界值），验证边界条件处理正确",
        "step_pattern": ["进入页面", "输入边界值", "触发校验/提交", "观察处理结果"],
        "expected_pattern": ["边界值接受/拒绝的提示", "边界值处理后的数据状态"],
    },
    # 风险验证
    "risk_verification": {
        "test_intent": "风险验证：验证特定风险点的防护措施是否生效",
        "step_pattern": ["构造风险场景", "执行触发操作", "观察防护响应"],
        "expected_pattern": ["防护措施的具体表现", "风险被阻断/降级的证据"],
    },
    # 接口测试
    "api": {
        "test_intent": "接口测试：验证API的请求/响应格式、状态码、数据正确性",
        "step_pattern": ["构造请求参数", "发送HTTP请求", "检查响应状态码", "校验响应体字段"],
        "expected_pattern": ["HTTP状态码的具体值", "响应体中关键字段的值/类型", "错误码和错误信息"],
    },
    # 集成测试
    "integration": {
        "test_intent": "集成测试：验证跨系统/跨模块的数据流转和状态同步",
        "step_pattern": ["在A系统执行操作", "等待数据同步", "在B系统验证结果"],
        "expected_pattern": ["B系统中的数据与A系统一致", "同步延迟/失败的提示"],
    },
    # 兜底（覆盖所有未知 category）
    "default": {
        "test_intent": "通用验证：按测试点描述执行操作，观察并记录系统响应",
        "step_pattern": ["按测试点描述执行操作", "观察系统响应"],
        "expected_pattern": ["操作后的可观测现象（具体值/状态/文案）"],
    },
}


# ============================================================
# 引导卡生成
# ============================================================

def generate_guide_cards(
    test_points: list,
    p0_data: dict = None,
    p1_data: dict = None,
    skill_dir: str = None,
) -> list:
    """为一批测试点生成引导卡数组。

    Args:
        test_points: P5 test_points 列表（已过滤为当前批次）
        p0_data: P0 output.json 内容
        p1_data: P1 output.json 内容（可选）
        skill_dir: skill 根目录（用于读取 forbidden_words.py）

    Returns:
        引导卡 dict 列表，顺序与输入一致
    """
    if not test_points:
        return []

    guides = []
    for tp in test_points:
        guide = _generate_single_guide(tp, p0_data, p1_data, skill_dir)
        guides.append(guide)

    return guides


def _generate_single_guide(
    tp: dict,
    p0_data: dict = None,
    p1_data: dict = None,
    skill_dir: str = None,
) -> dict:
    """为单个测试点生成引导卡。"""
    cat = (tp.get("category") or "").strip()
    desc = (tp.get("description") or "").strip()

    # 1. 从 category 获取基础模板
    template = CATEGORY_GUIDE_MAP.get(cat, CATEGORY_GUIDE_MAP["default"])

    # 2. test_intent
    test_intent = template["test_intent"]

    # 3. step_pattern：动态提取 + 模板 fallback
    step_pattern = _extract_step_pattern(desc, cat, template)

    # 4. expected_pattern
    expected_pattern = list(template["expected_pattern"])

    # 5. key_ui：多源提取
    key_ui = _extract_key_ui(tp, desc, p0_data, p1_data)

    # 6. key_data
    key_data = _extract_key_data(desc)

    # 7. must_avoid：拆分步骤/期望禁止词
    step_avoid, expected_avoid = _load_forbidden_words(skill_dir)

    # 8. special_rules（V4.8.3: 传入 p0_data 用于业务规则提取）
    special_rules = _detect_special_rules(desc, tp, p0_data)

    return {
        "test_point_id": tp.get("id", ""),
        "category": cat,
        "p5_description": desc,
        "p5_precondition": tp.get("precondition", ""),
        "test_intent": test_intent,
        "step_pattern": step_pattern,
        "expected_pattern": expected_pattern,
        "key_ui": key_ui,
        "key_data": key_data if key_data else None,
        "step_must_avoid": step_avoid,
        "expected_must_avoid": expected_avoid,
        "special_rules": special_rules,
        # V4.8.7: 预算控制字段，告诉LOW模型每个TP至少生成几条用例
        "expected_case_count": tp.get("expected_case_count", 2),
        "complexity": tp.get("complexity", "L2"),
    }


# ============================================================
# 提取函数
# ============================================================

def _extract_step_pattern(desc: str, category: str, template: dict) -> list:
    """从 P5 description 动态提取操作动词序列，而非套用固定模板。

    核心思路：用正则提取 description 中的操作动词+对象，组装为步骤骨架。
    提取不到时 fallback 到 category 通用模板。
    """
    steps = []

    # 提取路径信息：「XX」中的页面/模块名
    path = re.findall(r'进入[「「]?([^」」]+)[」」]?', desc)
    if path:
        steps.append(f'进入{"→".join(path[:2])}页面')
    elif "进入" in desc:
        # 宽松匹配
        nav = re.findall(r'进入([\u4e00-\u9fa5]{2,10}(?:页面|模块|菜单)?)', desc)
        if nav:
            steps.append(f'进入{nav[0]}')

    # 提取操作动词+引号内容
    ops = re.findall(
        r'(点击|输入|选择|删除|勾选|上传|下载|拖拽|切换|打开|关闭|填写|修改|清空)'
        r'[「「]?([^」」，,，。.\s]{1,20})[」」]?',
        desc
    )
    for verb, target in ops[:5]:
        steps.append(f'{verb}「{target}」')

    # 补充观察/验证步骤
    if category in ("exception", "boundary"):
        steps.append("观察系统错误/拦截提示信息")
    elif category == "risk_verification":
        steps.append("观察防护措施的响应表现")
    elif category == "api":
        steps.append("检查响应数据与预期一致")
    else:
        steps.append("查看操作结果（弹窗提示/列表变化/状态更新）")

    # 过滤掉异常步骤：含嵌套引号（正则匹配到脏数据）、过长或过短
    def _is_valid_step(s: str) -> bool:
        if s.count('「') > 1 or s.count('」') > 1:  # 嵌套引号 → 脏数据
            return False
        if len(s) > 60 or len(s) < 3:
            return False
        return True
    steps = [s for s in steps if _is_valid_step(s)]

    # Fallback：提取不到有效操作动词时使用模板
    if len(steps) < 2:
        steps = list(template["step_pattern"])

    return steps


def _extract_key_ui(
    tp: dict,
    desc: str,
    p0_data: dict = None,
    p1_data: dict = None,
) -> list:
    """多源提取 UI 元素，4 层 fallback。

    L1: P0.ui_elements（最可靠）
    L2: P0.field_specs 字段标签
    L3: P5 description 引号内容
    L4: 正则提取 UI 模式词
    """
    ui = set()

    blocks = p0_data.get("blocks", {}) if p0_data else {}

    # L1：P0.ui_elements
    for elem in blocks.get("ui_elements", [])[:10]:
        name = elem.get("name", "") if isinstance(elem, dict) else str(elem)
        if name and len(name) >= 2:
            ui.add(name)

    # L2：P0.field_specs 字段→输入框/下拉框
    for spec in blocks.get("field_specs", [])[:10]:
        label = (spec.get("label") or spec.get("field_name") or "").strip()
        if not label:
            continue
        ftype = spec.get("field_type", "")
        if ftype in ("dropdown", "select"):
            ui.add(f"{label}下拉框")
        elif ftype in ("date", "datetime"):
            ui.add(f"{label}日期选择器")
        else:
            ui.add(f"{label}输入框")

    # L3：P5 description 中引号包裹的 UI 名称
    quoted = re.findall(r'[「「]([^」」]+)[」」]', desc)
    for q in quoted:
        if 2 <= len(q) <= 20:
            ui.add(q)

    # L4：正则提取「XX按钮」「XX框」等 UI 模式
    pattern_ui = re.findall(
        r'([\u4e00-\u9fa5]{2,6}(?:按钮|输入框|下拉框|列表|页面|弹窗|Toast|图标|菜单|标签页|复选框))',
        desc
    )
    ui.update(pattern_ui)

    result = sorted(ui)[:8]
    return result if result else ["页面操作区"]


def _extract_key_data(desc: str) -> dict:
    """从 P5 description 提取测试数据（数值+单位、引号内容）。"""
    data = {}

    # 数值+可选单位
    for val, unit in re.findall(r'(\d+\.?\d*)\s*([%％个条次秒元]?)', desc)[:3]:
        key = unit if unit else "数值"
        data[key] = val

    # 引号内容
    quoted = re.findall(r'[「「]([^」」]+)[」」]', desc)
    for i, q in enumerate(quoted[:3]):
        if len(q) >= 2 and not q.rstrip("0123456789.%％"):  # 跳过纯数字
            data[f"值{i+1}"] = q

    # 去重值
    seen = set()
    deduped = {}
    for k, v in data.items():
        if v not in seen:
            deduped[k] = v
            seen.add(v)

    return deduped


def _load_forbidden_words(skill_dir: str = None) -> tuple:
    """从 forbidden_words.py 加载禁止词汇，拆分为步骤/期望两类。

    Returns:
        (step_avoid, expected_avoid) 两个列表
    """
    step_avoid = ["验证", "检查", "确认", "构造", "执行操作", "观察", "确保"]
    expected_avoid = ["正常", "成功", "操作成功", "数据正确", "符合预期", "功能正常",
                      "流程正确", "展示完整", "处理正常", "结果正确", "结果符合"]

    if not skill_dir:
        return step_avoid, expected_avoid

    try:
        import sys, os
        config_dir = os.path.join(skill_dir, "tools", "config")
        if config_dir not in sys.path:
            sys.path.insert(0, config_dir)
        from forbidden_words import L1_ABSOLUTE, L1_PATTERNS
        step_avoid = list(L1_ABSOLUTE[:10])
        expected_avoid = [p.replace(r'\s*[，。；]?', '') for p in L1_PATTERNS[:10]]
    except Exception:
        pass

    return step_avoid, expected_avoid


def _detect_special_rules(desc: str, tp: dict, p0_data: dict = None) -> list:
    """检测券商/安全场景规则触发条件。

    当 P5 description 包含特定关键词时，引导卡注入对应的业务规则提示。
    V4.8.3: 新增从 P0 blocks_markdown 提取业务约束。
    """
    rules = []

    # 交易时段
    if any(kw in desc for kw in ["交易时段", "非交易", "集合竞价", "9:30", "15:00"]):
        rules.append("交易时段限制：非交易时段操作需验证拦截或提示")

    # T+1 清算
    if any(kw in desc for kw in ["清算", "T+1", "T+0", "交割"]):
        rules.append("T+1清算：验证清算前后数据状态变化，关注数据口径（自然日/交易日）")

    # 安全测试（文件上传场景）
    if any(kw in desc for kw in ["文件上传", "导入", "附件", "上传", "导入文件"]):
        rules.append("安全测试：需设计恶意文件/SQL注入/XSS/路径遍历/超大文件用例")

    # 特殊证券
    if any(kw in desc for kw in ["停牌", "ST", "退市", "零股"]):
        rules.append("特殊证券：停牌/ST/退市的拦截或标注，零股的最小交易单位限制")

    # 数据时效
    if any(kw in desc for kw in ["实时", "查询时间", "数据截止", "刷新"]):
        rules.append("数据时效性：验证数据更新时间标注，实时vs延迟数据的展示差异")

    # 双人复核/审批流
    if any(kw in desc for kw in ["审批", "复核", "双人", "审核", "会签"]):
        rules.append("审批流程：验证审批状态流转（待审批→审批中→已通过/已驳回），需设计驳回后重新提交场景")

    # 权限分级
    if any(kw in desc for kw in ["权限", "角色", "部门", "白名单", "可见"]):
        rules.append("权限控制：验证不同角色/部门的数据可见性和操作权限差异")

    # 数据导出
    if any(kw in desc for kw in ["导出", "下载", "报表", "打印"]):
        rules.append("导出功能：验证导出格式、数据量限制、文件名规范、敏感数据脱敏")

    # V4.8.3: 从 P0 blocks_markdown 提取业务约束
    p0_rules = _extract_business_rules_from_p0(p0_data)
    # 去重合并，P0规则优先追加到末尾
    for r in p0_rules:
        if r not in rules:
            rules.append(r)

    return rules[:5]  # 最多5条，避免引导卡过长


def _extract_business_rules_from_p0(p0_data: dict) -> list:
    """V4.8.3: 从 P0 blocks_markdown 提取业务约束规则。

    解析 blocks_markdown 中的「业务规则」「约束条件」「校验规则」段落，
    提取为简短的可执行规则提示，注入引导卡。
    """
    if not p0_data:
        return []

    blocks_md = p0_data.get("blocks_markdown", "")
    if not blocks_md or len(blocks_md) < 50:
        return []

    rules = []

    # 1. 按段落拆分
    sections = re.split(r'\n(?=#{1,3}\s)', blocks_md)

    # 2. 只处理包含业务规则关键词的段落
    rule_keywords = [
        "业务规则", "约束条件", "校验规则", "计算规则", "状态流转",
        "权限", "角色", "审批", "复核", "限制", "禁止", "必须",
        "规则", "条件", "门槛", "阈值", "比例", "上限", "下限"
    ]

    for section in sections:
        # 检查段落是否包含规则关键词
        section_lower = section.lower()
        if not any(kw in section for kw in rule_keywords):
            continue

        # 提取列表项（- 或 数字. 开头）
        items = re.findall(
            r'(?:^|\n)\s*(?:[-•*]|\d+[.、])\s*(.+?)(?=\n|$)',
            section, re.MULTILINE
        )
        for item in items:
            item = item.strip()
            if not item or len(item) < 8:
                continue
            # 过滤掉纯标题/标签行
            if re.match(r'^(#{1,3}\s|\*\*|业务规则|约束条件)', item):
                continue
            # 截断过长规则（≤60字）
            if len(item) > 60:
                item = item[:57] + "..."
            rules.append(f"P0规则: {item}")

    # 3. 也提取正文中的规则性语句（以必须/禁止/不得开头）
    must_patterns = re.findall(
        r'(?:必须|禁止|不得|需|应)[\u4e00-\u9fa5，,。.；;：:、\d%]{10,50}',
        blocks_md
    )
    for mp in must_patterns[:3]:  # 最多3条
        mp = mp.strip()
        if len(mp) > 55:
            mp = mp[:52] + "..."
        if mp not in rules:
            rules.append(f"P0规则: {mp}")

    # 去重（按内容相似度）
    unique_rules = []
    for r in rules:
        is_dup = False
        for ur in unique_rules:
            # 简单去重：80%以上字符重叠
            if len(set(r) & set(ur)) / max(len(set(r)), 1) > 0.7:
                is_dup = True
                break
        if not is_dup:
            unique_rules.append(r)

    return unique_rules[:5]  # 最多5条


def generate_draft_case(tp: dict, skeleton: dict, p0_data: dict = None) -> dict:
    """生成兜底草稿用例（单条）。

    当单批连续 3 次 Gate 拒绝时，用此函数生成草稿作为保底输出。
    草稿标记 [草稿] 前缀，需人工审查。

    Args:
        tp: P5 test_point
        skeleton: 骨架元数据 {case_id, priority, is_smoke, source_test_point}
        p0_data: P0 output（用于提取 UI 元素）

    Returns:
        19 列完整草稿 dict
    """
    desc = tp.get("description", "")
    precondition = tp.get("precondition", "")

    # 生成步骤草稿
    template = CATEGORY_GUIDE_MAP.get(
        tp.get("category", ""), CATEGORY_GUIDE_MAP["default"]
    )
    steps_list = _extract_step_pattern(desc, tp.get("category", ""), template)

    # 步骤格式化
    formatted_steps = "\n".join(
        f"{i}. {s}" for i, s in enumerate(steps_list, 1)
    )

    # 期望结果草稿
    exp_pattern = template["expected_pattern"]
    formatted_expected = "\n".join(
        f"{i}. [草稿] {e}" for i, e in enumerate(exp_pattern, 1)
    )

    return {
        "project": skeleton.get("project", ""),
        "case_type": "测试用例",
        "case_id": skeleton.get("case_id", ""),
        "requirement": skeleton.get("requirement", ""),
        "priority": skeleton.get("priority", "P2"),
        "title": f"[草稿] {desc[:50]}",
        "menu_path": tp.get("source_scenario", ""),
        "preconditions": f"[草稿] {precondition}" if precondition else "[草稿] 待补充前置条件",
        "steps": f"[草稿-需人工审查]\n{formatted_steps}",
        "expected_results": formatted_expected,
        "is_smoke": skeleton.get("is_smoke", False),
        "creator": "AI生成(草稿兜底)",
        "assignee": "",
        "test_case_type": template["test_intent"][:20],
        "test_category": tp.get("category", "功能"),
        "status": "",
        "screenshot": "",
        "test_suite": tp.get("source_scenario", ""),
        "remarks": "⚠️ 自动生成草稿，需人工审查 | 来源:V4.8.0草稿兜底机制",
        "source_test_point": skeleton.get("source_test_point", tp.get("id", "")),
    }


# V4.8.0: 显式导出
__all__ = [
    "generate_guide_cards",
    "generate_draft_case",
    "CATEGORY_GUIDE_MAP",
]
