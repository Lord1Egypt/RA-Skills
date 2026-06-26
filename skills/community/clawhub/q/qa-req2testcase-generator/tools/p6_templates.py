#!/usr/bin/env python3
"""
V3.4.1 P6模板引擎 — 基于P5测试点自动生成完整用例
用于hybrid模式的p6_code_generate action

每种category一套模板，通过关键词提取+变体词组实现差异化。
集成A/B分类体系：A类生成3步以上操作链+UI断言，B类生成单字段校验。

版本: 3.4.1
日期: 2026-05-16
任务: 集成ab_classifier到p6_templates
"""

import re
import json
import os
from collections import Counter

# A/B分类体系集成
try:
    from ab_classifier import classify_test_point
    # is_type_a 可能不存在于所有版本，安全导入
    try:
        from ab_classifier import is_type_a as _is_type_a_func
        is_type_a = _is_type_a_func
    except ImportError:
        is_type_a = None  # type: ignore
except ImportError:
    classify_test_point = None  # type: ignore
    is_type_a = None  # type: ignore


# ============================================================
# 关键词提取
# ============================================================

def extract_keywords(description, precondition=""):
    """从description中提取关键操作词和对象"""
    # 提取动词+宾语
    action_patterns = [
        r'(查看|导入|导出|上传|下载|点击|切换|输入|删除|新增|修改|编辑|搜索|筛选|排序|推送|同步|验证|提交|审核|登录|退出)',
        r'(展示|显示|隐藏|加载|刷新|跳转|返回|保存|取消|确认|关闭|打开)',
    ]
    actions = []
    for pat in action_patterns:
        actions.extend(re.findall(pat, description))

    # 提取操作对象（名词短语）
    object_patterns = [
        r'([\u4e00-\u9fa5]{2,8}(?:Tab|页面|列表|表格|按钮|字段|弹窗|菜单|模块|榜单|数据|文件|报表))',
        r'([\u4e00-\u9fa5]{2,6}(?:功能|入口|权限|角色|状态))',
    ]
    objects = []
    for pat in object_patterns:
        objects.extend(re.findall(pat, description))

    # 提取角色
    role_patterns = [
        r'(管理员|运营人员|业务人员|普通用户|机构用户|员工|客户)',
    ]
    roles = []
    for pat in role_patterns:
        roles.extend(re.findall(pat, description + " " + precondition))

    return {
        "actions": actions[:3] if actions else ["操作"],
        "objects": objects[:3] if objects else ["相关功能"],
        "roles": roles[:2] if roles else ["用户"],
        "desc_short": description[:30],
    }


# ============================================================
# 页面路径提取（优先使用page_path字段）
# ============================================================

def _extract_page_path_display(tp):
    """从测试点中提取page_path的显示文本。
    
    优先级：
    1. page_path.full_path（dict格式的完整路径）
    2. page_path.hierarchy 拼接（dict格式无full_path时）
    3. page_path 字符串（str格式）
    4. 回退到空串（由调用方决定是否使用description）
    
    Args:
        tp: 测试点dict
    Returns:
        str: 页面路径显示文本（如 "首页→营销管理→协同分润"）
    """
    page_path = tp.get("page_path", "")
    if not page_path:
        return ""
    
    if isinstance(page_path, dict):
        # dict格式：优先用full_path，其次用hierarchy拼接
        full_path = page_path.get("full_path", "")
        if full_path:
            return full_path
        hierarchy = page_path.get("hierarchy", [])
        if hierarchy:
            return "→".join(hierarchy)
        return ""
    
    if isinstance(page_path, str):
        return page_path.strip()
    
    return ""


def _get_navigation_text(tp, fallback_obj="相关功能"):
    """获取导航步骤中的页面描述文本。
    
    优先使用page_path，回退到description关键词提取的对象。
    
    Args:
        tp: 测试点dict
        fallback_obj: 关键词提取的对象名（回退用）
    Returns:
        str: 导航目标文本
    """
    page_display = _extract_page_path_display(tp)
    if page_display:
        return page_display
    return fallback_obj


# ============================================================
# 步骤动词变体（避免重复）
# ============================================================

VERB_VARIANTS = {
    "查看": ["查看", "浏览", "检查"],
    "点击": ["点击", "单击", "选择"],
    "输入": ["输入", "填写", "录入"],
    "验证": ["验证", "确认", "检查"],
    "进入": ["进入", "打开", "访问"],
}

_variant_counter = Counter()

def get_variant(verb):
    """获取动词变体，轮换使用避免重复"""
    variants = VERB_VARIANTS.get(verb, [verb])
    idx = _variant_counter[verb] % len(variants)
    _variant_counter[verb] += 1
    return variants[idx]


# ============================================================
# 模板定义（11套）
# ============================================================

# ============================================================
# A/B分类辅助：判断是否为A类（兼容ab_classifier无is_type_a函数的情况）
# ============================================================

def _is_type_a_safe(tp):
    """安全判断测试点是否为A类，兼容不同版本的ab_classifier"""
    # 优先使用ab_classifier的is_type_a函数（如果存在）
    if callable(is_type_a):
        try:
            return is_type_a(tp)
        except Exception:
            pass
    # 回退：使用classify_test_point
    try:
        case_type, _ = classify_test_point(tp)
        return case_type == "A"
    except Exception:
        # 最终回退：根据category和operations_chain判断
        category = (tp.get("category", "") or "").lower()
        chain_len = len(tp.get("operations_chain", []) or [])
        a_cats = {"main_flow", "branch", "integration", "permission", "state_migration"}
        if category in a_cats:
            return True
        if chain_len >= 3:
            return True
        return False


def _generate_a_class_steps(tp, case_idx, kw):
    """A类用例：生成3步以上操作链+UI断言
    
    A类特征：
    - 操作链路≥3步
    - 每步有具体UI变化
    - 至少1个异常分支
    """
    role = kw["roles"][0]
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "相关功能")
    action = kw["actions"][0] if kw["actions"] else "操作"
    operations_chain = tp.get("operations_chain", []) or []
    ui_elements = tp.get("ui_elements", []) or []

    if operations_chain and len(operations_chain) >= 3:
        # 有完整operations_chain，直接展开
        steps = []
        expected = []
        for i, op in enumerate(operations_chain):
            if isinstance(op, dict):
                step_desc = op.get("description", f"执行第{i+1}步操作")
                target = op.get("target_element", "")
                data_val = op.get("data_value", "")
                anchor = op.get("expected_anchor", "")
                
                step_text = f"{i+1}. {step_desc}"
                if target:
                    step_text += f"（{target}）"
                if data_val:
                    step_text += f"，输入值：{data_val}"
                steps.append(step_text)
                
                exp_text = f"{i+1}. {anchor}" if anchor else f"{i+1}. 操作完成，页面响应正常"
                expected.append(exp_text)
            else:
                steps.append(f"{i+1}. {op}")
                expected.append(f"{i+1}. 操作完成，结果符合预期")
    else:
        # 无完整operations_chain，从上下文生成3步以上操作链
        if case_idx == 1:  # 正向验证
            steps = [
                f"1. 使用{role}账号登录CRM系统",
                f"2. 导航至{obj}页面（通过菜单或快捷入口）",
                f"3. {get_variant(action)}{kw['desc_short'][:20]}",
                f"4. 验证操作结果（检查列表/详情/状态变化）",
            ]
            expected = [
                "1. 登录成功，进入系统首页",
                f"2. {obj}页面正常加载，数据展示完整，UI元素渲染正确",
                f"3. {action}成功，系统给出明确反馈提示",
                f"4. 操作结果与预期一致，数据状态正确更新",
            ]
            # 如果有ui_elements，追加UI断言步骤
            if ui_elements:
                ui_desc = "、".join(str(e.get("name", e)) if isinstance(e, dict) else str(e) for e in ui_elements[:3])
                steps.append(f"5. 确认UI元素（{ui_desc}）展示正确")
                expected.append(f"5. UI元素位置、样式、文案均符合设计稿，交互响应正常")
        else:  # 异常/边界变体
            exception_scenarios = tp.get("exception_scenarios", []) or []
            ex_desc = exception_scenarios[0].get("description", "异常条件") if exception_scenarios and isinstance(exception_scenarios[0], dict) else "异常条件"
            steps = [
                f"1. 使用{role}账号登录CRM系统",
                f"2. 导航至{obj}页面",
                f"3. 构造异常条件：{ex_desc}",
                f"4. 观察系统响应与错误处理",
            ]
            expected = [
                "1. 登录成功",
                f"2. {obj}页面正常加载",
                "3. 系统检测到异常输入/条件",
                "4. 给出明确错误提示（非技术堆栈），数据不受影响，支持重试",
            ]

    return steps, expected


def _generate_b_class_steps(tp, case_idx, kw):
    """B类用例：生成单字段校验
    
    B类特征：
    - 聚焦1个字段或1个边界条件
    - 期望结果中明确写出错误提示的具体文案
    """
    obj = kw["objects"][0] if kw["objects"] else "输入字段"
    field_target = tp.get("field_target", {}) or {}
    field_specs = tp.get("field_specs", []) or []
    test_data_matrix = tp.get("test_data_matrix", []) or []

    field_name = ""
    if isinstance(field_target, dict):
        field_name = field_target.get("field_name", "")
    if not field_name and field_specs:
        first_spec = field_specs[0] if isinstance(field_specs[0], dict) else {}
        field_name = first_spec.get("name", "目标字段")
    if not field_name:
        field_name = obj

    if test_data_matrix and case_idx <= len(test_data_matrix):
        # 有test_data_matrix，直接使用
        td = test_data_matrix[case_idx - 1]
        if isinstance(td, dict):
            value = td.get("value", "")
            data_type = td.get("type", "测试数据")
            exp_behavior = td.get("expected_behavior", "系统给出校验提示")

            steps = [
                f"1. 登录CRM系统，进入相关页面",
                f"2. 定位{field_name}字段",
                f"3. 输入测试值：{value}（类型：{data_type}）",
                f"4. 触发校验（失焦/提交）",
            ]
            expected = [
                "1. 页面正常加载",
                f"2. {field_name}字段可见且可编辑",
                f"3. 输入值被接受或前端即时校验拦截",
                f"4. {exp_behavior}",
            ]
        else:
            steps = [
                f"1. 登录CRM系统，进入相关页面",
                f"2. 在{field_name}字段执行校验测试",
            ]
            expected = [
                "1. 页面正常加载",
                f"2. {field_name}校验结果符合预期",
            ]
    else:
        # 无test_data_matrix，根据case_idx生成边界用例
        if case_idx == 1:  # 有效值
            steps = [
                f"1. 登录CRM系统，进入相关页面",
                f"2. 在{field_name}中输入合法值",
                f"3. 提交并验证结果",
            ]
            expected = [
                "1. 页面正常加载",
                f"2. {field_name}接受合法输入，无校验错误",
                "3. 数据正确保存，结果符合业务规则",
            ]
        elif case_idx == 2:  # 无效值
            steps = [
                f"1. 登录CRM系统，进入相关页面",
                f"2. 在{field_name}中输入无效值（空值/非法格式/特殊字符）",
                f"3. 触发校验并观察提示",
            ]
            expected = [
                "1. 页面正常加载",
                f"2. 前端校验拦截或输入框标红",
                f"3. 显示明确错误提示（如「{field_name}格式不正确」），数据不被提交",
            ]
        else:  # 边界值
            steps = [
                f"1. 登录CRM系统，进入相关页面",
                f"2. 在{field_name}中输入边界值（最大值/最小值/临界值）",
                f"3. 提交并验证处理结果",
            ]
            expected = [
                "1. 页面正常加载",
                f"2. 系统接受边界值或给出范围提示",
                f"3. 边界值处理正确，不产生异常数据",
            ]

    return steps, expected


def _gen_main_flow(tp, case_idx, kw):
    """main_flow: 主流程正向验证"""
    role = kw["roles"][0]
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "相关功能")
    action = kw["actions"][0] if kw["actions"] else "操作"

    if case_idx == 1:  # 正向验证
        steps = [
            f"1. 使用{role}账号登录CRM系统",
            f"2. {get_variant('进入')}{obj}页面",
            f"3. {get_variant(action)}{kw['desc_short'][:15]}",
        ]
        expected = [
            "1. 登录成功，进入系统首页",
            f"2. {obj}页面正常加载，数据展示完整",
            f"3. {action}成功，结果符合业务规则",
        ]
    else:  # 异常/边界变体
        steps = [
            f"1. 使用{role}账号登录CRM系统",
            f"2. {get_variant('进入')}{obj}页面",
            f"3. 构造异常条件（如数据为空/网络超时/并发操作）",
        ]
        expected = [
            "1. 登录成功",
            f"2. {obj}页面正常加载",
            "3. 系统给出明确错误提示，数据不受影响",
        ]
    return steps, expected


def _gen_branch(tp, case_idx, kw):
    """branch: 分支逻辑验证"""
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "目标元素")

    if case_idx == 1:
        steps = [
            f"1. 登录CRM系统，进入相关页面",
            f"2. 定位{obj}，确认当前状态",
            f"3. 执行分支操作（{kw['desc_short'][:15]}）",
        ]
        expected = [
            "1. 登录成功，页面正常展示",
            f"2. {obj}状态正确显示",
            "3. 分支逻辑正确执行，结果符合预期",
        ]
    else:
        steps = [
            f"1. 登录CRM系统，进入相关页面",
            f"2. 构造非预期分支条件",
            f"3. 观察系统处理逻辑",
        ]
        expected = [
            "1. 登录成功",
            "2. 系统正确识别非预期条件",
            "3. 走入正确的异常分支，给出合理提示",
        ]
    return steps, expected


def _gen_integration(tp, case_idx, kw):
    """integration: 功能间联动验证"""
    if case_idx == 1:
        steps = [
            f"1. 登录CRM系统，完成前置操作（{kw['desc_short'][:12]}的前置条件）",
            f"2. 执行当前操作（依赖前置结果）",
            f"3. 验证上下游数据一致性",
        ]
        expected = [
            "1. 前置操作成功，产生预期数据",
            "2. 当前操作成功，正确引用前置数据",
            "3. 关联数据同步更新，无数据不一致",
        ]
    else:
        steps = [
            f"1. 登录CRM系统，前置操作产生异常数据",
            f"2. 执行当前操作（依赖异常前置数据）",
            f"3. 观察系统处理",
        ]
        expected = [
            "1. 前置操作完成（含异常数据）",
            "2. 系统检测到数据异常，给出提示",
            "3. 不产生脏数据，事务回滚或拒绝操作",
        ]
    return steps, expected


def _gen_permission(tp, case_idx, kw):
    """permission: 权限控制验证"""
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "受限功能")

    if case_idx == 1:  # 无权限访问
        steps = [
            f"1. 使用无{obj}权限的普通账号登录CRM系统",
            f"2. 尝试访问{obj}页面（直接输入URL或点击菜单）",
            f"3. 观察系统响应",
        ]
        expected = [
            "1. 登录成功（普通账号）",
            f"2. 系统拒绝访问或隐藏{obj}入口",
            "3. 显示权限不足提示，不泄露受限数据",
        ]
    else:  # 越权操作
        steps = [
            f"1. 使用低权限账号登录CRM系统",
            f"2. 通过接口/URL直接请求{obj}的操作接口",
            f"3. 观察系统响应",
        ]
        expected = [
            "1. 登录成功",
            "2. 接口返回403或权限校验失败",
            "3. 操作被拒绝，数据未被修改",
        ]
    return steps, expected


def _gen_exception(tp, case_idx, kw):
    """exception: 异常场景验证"""
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "相关功能")

    if case_idx == 1:
        steps = [
            f"1. 登录CRM系统，进入{obj}页面",
            f"2. 构造异常输入（空值/超长/特殊字符/非法格式）",
            f"3. 提交操作并观察系统响应",
        ]
        expected = [
            f"1. {obj}页面正常加载",
            "2. 系统接受输入或前端校验拦截",
            "3. 给出明确错误提示（如「输入格式不正确」），数据不受影响",
        ]
    else:
        steps = [
            f"1. 登录CRM系统，进入{obj}页面",
            f"2. 模拟系统异常（如后端超时/数据库连接失败）",
            f"3. 观察前端表现",
        ]
        expected = [
            f"1. {obj}页面正常加载",
            "2. 触发异常条件",
            "3. 前端显示友好错误提示（非技术堆栈），支持重试",
        ]
    return steps, expected


def _gen_boundary(tp, case_idx, kw):
    """boundary: 边界值验证"""
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "输入字段")

    if case_idx == 1:  # 边界内
        steps = [
            f"1. 登录CRM系统，进入相关页面",
            f"2. 在{obj}中输入边界值（最大值/最小值/临界值）",
            f"3. 提交并验证处理结果",
        ]
        expected = [
            "1. 页面正常加载",
            "2. 系统接受边界值输入",
            "3. 数据正确处理，结果符合业务规则",
        ]
    else:  # 超出边界
        steps = [
            f"1. 登录CRM系统，进入相关页面",
            f"2. 在{obj}中输入超出边界的值（超大/超小/溢出）",
            f"3. 提交并观察系统响应",
        ]
        expected = [
            "1. 页面正常加载",
            "2. 前端校验拦截或后端返回错误",
            "3. 给出明确提示（如「数值超出范围」），不产生异常数据",
        ]
    return steps, expected


def _gen_compatibility(tp, case_idx, kw):
    """compatibility: 兼容性验证"""
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "相关功能")

    if case_idx == 1:
        steps = [
            f"1. 使用Chrome浏览器登录CRM系统",
            f"2. 进入{obj}页面，执行核心操作",
            f"3. 切换到Firefox/Edge浏览器重复操作",
        ]
        expected = [
            "1. Chrome下功能正常",
            f"2. {obj}操作成功，数据正确",
            "3. 其他浏览器下功能表现一致，无兼容性问题",
        ]
    else:
        steps = [
            f"1. 使用移动端浏览器访问CRM系统",
            f"2. 进入{obj}页面",
            f"3. 验证页面自适应和功能可用性",
        ]
        expected = [
            "1. 移动端可正常访问",
            "2. 页面自适应展示，无错位",
            "3. 核心功能可用，交互正常",
        ]
    return steps, expected


def _gen_performance(tp, case_idx, kw):
    """performance: 性能验证"""
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "相关功能")

    if case_idx == 1:
        steps = [
            f"1. 登录CRM系统，准备大量测试数据（1000+条）",
            f"2. 进入{obj}页面，触发数据加载",
            f"3. 记录页面加载时间和响应速度",
        ]
        expected = [
            "1. 测试数据准备完成",
            f"2. {obj}页面在3秒内完成加载",
            "3. 列表滚动流畅，无卡顿，分页正常",
        ]
    else:
        steps = [
            f"1. 模拟10个用户并发访问{obj}",
            f"2. 每个用户执行相同操作",
            f"3. 观察系统响应和数据一致性",
        ]
        expected = [
            "1. 并发请求全部到达服务器",
            "2. 所有请求在5秒内返回",
            "3. 数据一致，无脏读/幻读",
        ]
    return steps, expected


def _gen_security(tp, case_idx, kw):
    """security: 安全验证"""
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "输入字段")

    if case_idx == 1:
        steps = [
            f"1. 登录CRM系统，进入含{obj}的页面",
            f"2. 在输入框中注入特殊字符（<script>alert(1)</script>）",
            f"3. 提交并观察页面渲染",
        ]
        expected = [
            "1. 页面正常加载",
            "2. 系统对输入进行转义或拦截",
            "3. 页面不执行注入脚本，显示转义后的文本",
        ]
    else:
        steps = [
            f"1. 使用已过期的Token访问API接口",
            f"2. 尝试执行敏感操作",
            f"3. 观察系统响应",
        ]
        expected = [
            "1. 请求携带过期Token",
            "2. 系统返回401未授权",
            "3. 敏感操作被拒绝，引导重新登录",
        ]
    return steps, expected


def _gen_state_migration(tp, case_idx, kw):
    """state_migration: 状态迁移验证"""
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "业务对象")

    if case_idx == 1:
        steps = [
            f"1. 登录CRM系统，创建{obj}（初始状态）",
            f"2. 执行状态变更操作（如提交/审核/完成）",
            f"3. 验证状态流转是否正确",
        ]
        expected = [
            f"1. {obj}创建成功，状态为初始态",
            "2. 状态变更成功，记录变更时间和操作人",
            "3. 状态流转符合业务规则，不可逆操作不可回退",
        ]
    else:
        steps = [
            f"1. 登录CRM系统，将{obj}置于特定状态",
            f"2. 尝试执行非法状态跳转（如从完成态回到初始态）",
            f"3. 观察系统响应",
        ]
        expected = [
            f"1. {obj}处于指定状态",
            "2. 系统拒绝非法状态跳转",
            "3. 给出明确提示，状态不变",
        ]
    return steps, expected


def _gen_api(tp, case_idx, kw):
    """api: 接口验证"""
    obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "业务接口")

    if case_idx == 1:  # 正向
        steps = [
            f"1. 获取有效Token（通过登录接口）",
            f"2. 调用{obj}接口，传入合法参数",
            f"3. 验证响应状态码和返回数据",
        ]
        expected = [
            "1. Token获取成功",
            "2. 接口返回HTTP 200",
            "3. 响应体包含预期字段，数据正确",
        ]
    else:  # 异常参数
        steps = [
            f"1. 获取有效Token",
            f"2. 调用{obj}接口，传入非法参数（缺失必填/类型错误/超长）",
            f"3. 验证错误响应",
        ]
        expected = [
            "1. Token获取成功",
            "2. 接口返回HTTP 400/422",
            "3. 响应体包含明确错误码和错误描述",
        ]
    return steps, expected


# ============================================================
# 模板分发器
# ============================================================

TEMPLATE_GENERATORS = {
    "main_flow": _gen_main_flow,
    "branch": _gen_branch,
    "integration": _gen_integration,
    "permission": _gen_permission,
    "exception": _gen_exception,
    "boundary": _gen_boundary,
    "compatibility": _gen_compatibility,
    "performance": _gen_performance,
    "security": _gen_security,
    "state_migration": _gen_state_migration,
    "state": _gen_state_migration,  # 别名
    "api": _gen_api,
    "interface": _gen_api,  # 别名
}


# ============================================================
# V4.1.9: 动态模块名提取（配置文件 + 数据驱动，无硬编码）
# ============================================================

# 模块级缓存，避免重复IO和计算
_module_map_cache = None
_module_map_cache_mtime = None


def _load_module_map_config():
    """从 config/module_map.json 加载模块映射配置（带文件缓存）。
    
    配置文件格式：
    {
      "module_map": {
        "M01": "模块A",
        "M02": "模块B"
      },
      "keyword_fallback": [
        {"keywords": ["查询", "搜索"], "module": "查询模块"}
      ]
    }
    
    Returns:
        dict: {"module_map": {...}, "keyword_fallback": [...]}
    """
    global _module_map_cache, _module_map_cache_mtime
    
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config", "module_map.json"
    )
    
    if not os.path.exists(config_path):
        return {"module_map": {}, "keyword_fallback": []}
    
    # 文件修改时间检查（缓存失效）
    try:
        mtime = os.path.getmtime(config_path)
        if _module_map_cache is not None and _module_map_cache_mtime == mtime:
            return _module_map_cache
    except OSError:
        pass
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        _module_map_cache = config
        _module_map_cache_mtime = mtime
        return config
    except Exception:
        return {"module_map": {}, "keyword_fallback": []}


def _extract_module_from_feature_tree(tp):
    """方案A：从P1 feature_tree动态提取module名称。
    
    P1 feature_tree 结构：
    feature_tree.modules = [
      {"id": "M01", "name": "模块名", "children": [...]},
      ...
    ]
    
    P5 source_scenario 格式如 REQ-XXX-M01-F01-S01，
    通过匹配M##编码找到对应module的name。
    
    Args:
        tp: 测试点dict
    Returns:
        str: 模块名（空字符串表示无法提取）
    """
    src = tp.get("source_scenario", "")
    if not src:
        return ""
    
    # 从source_scenario解析模块编码（如 M01）
    m_match = re.search(r'-M(\d+)-', src)
    if not m_match:
        return ""
    
    m_code = m_match.group(1)  # 如 "01"
    m_id = f"M{m_code}"  # 如 "M01"
    
    # 从P5测试点的source字段获取P1模块名
    # source数组可能包含 "M01-F01" 或 "M01-F01-S01" 格式的引用
    sources = tp.get("source", [])
    if isinstance(sources, list):
        for src_ref in sources:
            src_str = str(src_ref)
            # 匹配 M##-F## 模式
            if src_str.startswith(m_id):
                # source引用确认匹配，但名称需从外部数据获取
                # 此处仅返回编码作为fallback
                pass
    
    return ""  # feature_tree数据不在此函数作用域内


def _extract_module_from_sources(tp):
    """方案B：从P5测试点的source_scenario/source字段解析模块信息。
    
    解析逻辑：
    1. source_scenario (如 REQ-JTCRM-75672-M01-F01-S01) → 提取M##编码
    2. source数组 (如 ["M01-F01", "M01-F02"]) → 交叉验证
    3. 如果P5数据中包含 module_name 字段（由上游P5注入），直接使用
    
    Args:
        tp: 测试点dict
    Returns:
        str: 模块名（空字符串表示无法提取）
    """
    # 优先：P5可能直接携带module_name（由上游注入）
    module_name = tp.get("module_name", "")
    if module_name:
        return module_name
    
    # 尝试从source_scenario的编码通过配置文件映射
    src = tp.get("source_scenario", "")
    m_match = re.search(r'-M(\d+)-', src) if src else None
    if m_match:
        m_code = m_match.group(1)
        m_id = f"M{m_code}"
        
        # 查询配置文件中的映射
        config = _load_module_map_config()
        module_map = config.get("module_map", {})
        if isinstance(module_map, dict) and m_id in module_map:
            return module_map[m_id]
        # 兼容数字key
        if isinstance(module_map, dict) and int(m_code) in module_map:
            return module_map[int(m_code)]
    
    return ""


def _extract_module(tp):
    """从测试点提取业务模块名（动态化，无硬编码）。
    
    提取优先级：
    1. tp.module_name（上游直接注入）
    2. config/module_map.json 配置文件映射（M## → 模块名）
    3. 配置文件中的keyword_fallback（关键词 → 模块名）
    4. 从tp.source数组或description动态提取通用模块名
    
    Args:
        tp: 测试点dict
    Returns:
        str: 模块名
    """
    desc = tp.get("description", "")
    
    # 1. 上游注入的module_name
    result = _extract_module_from_sources(tp)
    if result:
        return result
    
    # 2. 配置文件的keyword_fallback
    config = _load_module_map_config()
    kw_fallbacks = config.get("keyword_fallback", [])
    if isinstance(kw_fallbacks, list):
        for fb in kw_fallbacks:
            if isinstance(fb, dict):
                keywords = fb.get("keywords", [])
                module = fb.get("module", "")
                if keywords and module and any(kw in desc for kw in keywords):
                    return module
    
    # 3. 从source_scenario提取M##编码作为通用模块标识
    src = tp.get("source_scenario", "")
    m_match = re.search(r'-M(\d+)-', src) if src else None
    if m_match:
        m_code = m_match.group(1)
        return f"模块{m_code}"
    
    # 4. 从source数组提取
    sources = tp.get("source", [])
    if isinstance(sources, list) and sources:
        first_src = str(sources[0])
        # 提取 M## 部分
        src_m = re.match(r'(M\d+)', first_src)
        if src_m:
            return f"模块{src_m.group(1)}"
    
    # 5. 最终fallback：无模块名
    return "未分类模块"

def generate_testcase(tp, case_idx, skeleton_entry):
    """为单条用例生成完整的fields内容

    V3.4.1: 集成A/B分类体系
    - A类（业务流程）：生成3步以上操作链+UI断言
    - B类（字段边界）：生成单字段校验

    Args:
        tp: P5测试点dict（含id/description/category/precondition等）
        case_idx: 用例序号（1=正向，2+=异常/边界）
        skeleton_entry: 骨架条目（含case_id/priority/is_smoke）

    Returns:
        dict: 完整的用例fields（含ab_class字段）
    """
    category = (tp.get("category", "") or "main_flow").lower()
    description = tp.get("description", "")
    precondition = tp.get("precondition", "")
    related_rules = tp.get("related_rules", [])

    # 提取关键词
    kw = extract_keywords(description, precondition)

    # ===== V3.4.1: A/B分类判断 =====
    ab_class = "A"  # 默认A类
    ab_reason = ""
    try:
        ab_class, ab_reason = classify_test_point(tp)
    except Exception:
        # classify_test_point异常时回退到基于category的判断
        b_class_cats = {"field_validation", "boundary"}
        if category in b_class_cats:
            ab_class = "B"
            ab_reason = f"类别 {category}（字段/边界测试）"
        else:
            ab_class = "A"
            ab_reason = f"类别 {category}（业务流程类）"

    # ===== V3.4.1: 根据A/B分类选择生成策略 =====
    if ab_class == "A":
        # A类：优先使用A类专用生成器（3步以上操作链+UI断言）
        operations_chain = tp.get("operations_chain", []) or []
        if operations_chain and len(operations_chain) >= 3:
            # 有完整operations_chain，直接展开
            steps, expected = _generate_a_class_steps(tp, case_idx, kw)
        else:
            # 无完整operations_chain，使用category模板但至少3步
            generator = TEMPLATE_GENERATORS.get(category, _gen_main_flow)
            steps, expected = generator(tp, case_idx, kw)
            # 确保A类至少3步
            if len(steps) < 3:
                role = kw["roles"][0]
                obj = _get_navigation_text(tp, kw["objects"][0] if kw["objects"] else "相关功能")
                steps.insert(1, f"2. 导航至{obj}页面")
                expected.insert(1, f"2. {obj}页面正常加载，UI元素渲染正确")
                # 重新编号
                _step_pattern = r'^\d+\.\s*'
                steps = [f"{i+1}. {re.sub(_step_pattern, '', s)}" for i, s in enumerate(steps)]
                expected = [f"{i+1}. {re.sub(_step_pattern, '', e)}" for i, e in enumerate(expected)]
    else:
        # B类：使用B类专用生成器（单字段校验）
        steps, expected = _generate_b_class_steps(tp, case_idx, kw)

    # 构建前置条件（三要素）
    role = kw["roles"][0]
    precond_parts = [
        f"1. {role}已登录CRM系统，账户状态正常",
    ]
    if precondition:
        precond_parts.append(f"2. {precondition}")
    else:
        precond_parts.append("2. 预置相关测试数据，通过后台接口创建")
    precond_parts.append("3. 系统处于正常工作状态，相关服务可用")
    preconditions_text = "；".join(precond_parts)

    # 构建title
    case_type_map = {1: "正向验证", 2: "异常验证", 3: "边界验证"}
    case_type_label = case_type_map.get(case_idx, "补充验证")
    title = f"{description[:30]}-{case_type_label}"

    # 构建test_case_type
    type_map = {
        "main_flow": "正向验证",
        "branch": "分支验证",
        "integration": "集成异常",
        "permission": "权限验证",
        "exception": "异常处理",
        "boundary": "边界验证",
        "compatibility": "兼容回归",
        "performance": "性能验证",
        "security": "安全验证",
        "state_migration": "状态迁移",
        "state": "状态迁移",
        "api": "接口验证",
        "interface": "接口验证",
    }
    test_case_type = type_map.get(category, "正向验证")
    if case_idx > 1 and category in ("main_flow", "branch"):
        test_case_type = "异常处理"

    # 构建test_category
    cat_map = {
        "performance": "性能",
        "security": "安全",
        "compatibility": "兼容性",
    }
    test_category = cat_map.get(category, "功能")

    # 构建remarks
    remarks_prefix_map = {
        "main_flow": "[前台功能/正向流程]",
        "branch": "[前台功能/正向流程]",
        "exception": "[前台功能/异常处理]",
        "boundary": "[前台功能/边界值]",
        "permission": "[权限控制]",
        "performance": "[性能]",
        "security": "[安全]",
        "compatibility": "[兼容性]",
        "integration": "[后台功能/正向流程]",
        "state_migration": "[前台功能/正向流程]",
        "state": "[前台功能/正向流程]",
        "api": "[后台功能/正向流程]",
        "interface": "[后台功能/正向流程]",
    }
    remarks_prefix = remarks_prefix_map.get(category, "[前台功能/正向流程]")
    rules_text = f" 关联规则:{'、'.join(related_rules)}" if related_rules else ""
    remarks = f"{remarks_prefix}{rules_text}"


    # V4.1.8: 从测试点提取业务模块名用于test_suite和评审工具分类
    module_name = _extract_module(tp)

    # V3.4.1: A/B分类标签加入remarks
    ab_tag = "[A类-业务流程]" if ab_class == "A" else "[B类-字段边界]"

    # 组装fields（含test_suite用于评审工具模块分类 + ab_class标记）
    fields = {
        "title": title,
        "preconditions": preconditions_text,
        "steps": "\n".join(steps),
        "expected_results": "\n".join(expected),
        "test_case_type": test_case_type,
        "test_category": test_category,
        "test_suite": module_name,  # V4.1.8: 业务模块名（评审工具据此分类）
        "remarks": f"{ab_tag}[{module_name}]{rules_text}",
        "ab_class": ab_class,  # V3.4.1: A/B分类标记
        "ab_reason": ab_reason,  # V3.4.1: 分类理由
    }

    return fields


def _load_reviewed_cases_for_knowledge(test_points):
    """V4.1.9: 从knowledge/reviewed_cases/读取相关业务域的评审经验。
    
    读取逻辑：
    1. 从测试点中提取source_scenario，确定业务域
    2. 匹配knowledge/reviewed_cases/下对应域的规则文件
    3. 蒸馏为简洁经验提示（避免prompt膨胀）
    
    容错处理：
    - knowledge/reviewed_cases/目录不存在 → 返回空字符串
    - 目录为空 → 返回空字符串
    - 文件格式异常 → 跳过该文件
    
    Args:
        test_points: 测试点列表
    Returns:
        str: 评审经验摘要文本（用于注入模板生成），空字符串表示无可用知识
    """
    # 确定skill根目录
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reviewed_cases_dir = os.path.join(skill_dir, "knowledge", "reviewed_cases")
    
    # 容错：目录不存在或为空
    if not os.path.isdir(reviewed_cases_dir):
        return ""
    
    try:
        case_files = [f for f in os.listdir(reviewed_cases_dir)
                       if f.endswith("_rules.json")]
    except OSError:
        return ""
    
    if not case_files:
        return ""
    
    # 收集测试点文本用于匹配
    tp_text = " ".join(
        tp.get("description", "") + " " + tp.get("source_scenario", "")
        for tp in test_points[:20]  # 限制采样量
    )
    
    # 尝试匹配域特定规则
    matched_rules = []
    
    # 域名→文件名映射（与knowledge/domain_match.py保持一致）
    domain_filename_map = {
        "客户域": "客户", "交易域": "交易", "资管域": "资管", "自营域": "自营",
        "投顾域": "投顾", "投研域": "投研", "投行业务域": "投行", "机构业务域": "机构",
        "清算托管域": "清算托管", "风控合规域": "风控合规", "行情资讯域": "行情资讯", "互联网终端域": "互联网终端",
    }
    
    # 域关键词检测（轻量版，避免import循环）
    domain_keywords = {
        "客户": ["客户", "用户", "开户", "账户"],
        "交易": ["交易", "买入", "卖出", "委托", "订单"],
        "资管": ["资管", "基金", "理财", "产品"],
        "投顾": ["投顾", "顾问", "分润", "投建议"],
        "风控合规": ["风控", "合规", "审核", "权限", "角色"],
        "清算托管": ["清算", "托管", "结算"],
        "机构": ["机构", "营业部", "渠道"],
    }
    
    # 检测匹配的域
    matched_domain_files = set()
    for domain_key, keywords in domain_keywords.items():
        if any(kw in tp_text for kw in keywords):
            matched_domain_files.add(domain_key)
    
    # 如果没匹配到特定域，加载通用规则
    if not matched_domain_files:
        matched_domain_files.add("通用")
    
    # 加载并蒸馏规则
    for domain_key in matched_domain_files:
        rule_file = f"{domain_key}_rules.json"
        rule_path = os.path.join(reviewed_cases_dir, rule_file)
        if not os.path.exists(rule_path):
            continue
        try:
            with open(rule_path, "r", encoding="utf-8") as f:
                rules_data = json.load(f)
            
            # 蒸馏：每层最多3条，只取高权重/高频规则
            for layer_name, label in [
                ("tag_rules", "质量规则"),
                ("operation_rules", "操作规范"),
                ("positive_rules", "优秀模式"),
            ]:
                rules = rules_data.get(layer_name, [])
                if not rules or not isinstance(rules, list):
                    continue
                # 按权重/频率排序
                sorted_rules = sorted(
                    rules,
                    key=lambda r: (r.get("weight", 1.0), r.get("frequency", 0)),
                    reverse=True
                )
                for r in sorted_rules[:3]:
                    freq = r.get("frequency", 1)
                    weight = r.get("weight", 1.0)
                    rule_text = r.get("rule", "")
                    if rule_text:
                        prefix = "[强规则]" if freq >= 5 else "[规则]" if freq >= 2 else "[参考]"
                        matched_rules.append(f"{prefix} {rule_text}")
        except Exception:
            continue  # 跳过异常文件
    
    if not matched_rules:
        return ""
    
    # 限制总条数，避免注入过大
    matched_rules = matched_rules[:15]
    
    return (
        "[历史评审经验] 以下规则来自历史评审，生成用例时请参考：\n"
        + "\n".join(f"- {r}" for r in matched_rules)
    )


def generate_batch(test_points, skeleton_entries, batch_meta=None):
    """为一个批次生成全部用例

    Args:
        test_points: 本批次的P5测试点列表
        skeleton_entries: 本批次的骨架列表
        batch_meta: 批次元信息（可选）

    Returns:
        dict: 完整的batch JSON（含testcases和statistics）
    """
    # 构建测试点索引
    tp_map = {tp.get("id", ""): tp for tp in test_points}

    # 按source_test_point分组骨架
    from collections import defaultdict
    tp_cases = defaultdict(list)
    for sk in skeleton_entries:
        src = sk.get("source_test_point", "")
        tp_cases[src].append(sk)

    testcases = []
    
    # V4.1.9: 加载knowledge评审经验（代码模板模式的知识注入）
    knowledge_hints = _load_reviewed_cases_for_knowledge(test_points)
    
    for src_tp_id, skeletons in tp_cases.items():
        tp = tp_map.get(src_tp_id, {"description": src_tp_id, "category": "main_flow"})
        for idx, sk in enumerate(skeletons, 1):
            fields = generate_testcase(tp, idx, sk)
            # V4.1.9: 将knowledge经验注入remarks（如果有的话）
            if knowledge_hints and "fields" in fields:
                existing_remarks = fields.get("remarks", "")
                fields["remarks"] = f"{existing_remarks}\n{knowledge_hints}"
                fields["knowledge_injected"] = True  # 标记已注入knowledge
            testcases.append({
                "id": sk["case_id"],
                "source_test_point": src_tp_id,
                "priority": sk.get("priority", "P1"),
                "is_smoke": sk.get("is_smoke", False),
                "fields": fields,
            })

    # 统计
    pri_dist = Counter(tc.get("priority", "?") for tc in testcases)
    smoke_count = sum(1 for tc in testcases if tc.get("is_smoke"))

    # V3.4.1: A/B分类统计
    ab_a_count = sum(1 for tc in testcases if tc.get("fields", {}).get("ab_class") == "A")
    ab_b_count = sum(1 for tc in testcases if tc.get("fields", {}).get("ab_class") == "B")

    return {
        "testcases": testcases,
        "statistics": {
            "total_cases": len(testcases),
            "smoke_count": smoke_count,
            "by_priority": dict(pri_dist),
            "ab_class_stats": {
                "a_class_count": ab_a_count,
                "b_class_count": ab_b_count,
                "a_class_ratio": round(ab_a_count / len(testcases), 4) if testcases else 0.0,
            },
            "generation_method": "code_template_ab",
            "knowledge_injected": bool(knowledge_hints),  # V4.1.9: 标记是否注入了knowledge
        }
    }


# ============================================================
# V3.4.1: 基于上下文的用例生成（直接展开operations_chain/ui_elements/field_specs）
# ============================================================

def generate_testcase_from_context(tp, case_idx, skeleton_entry):
    """从测试点上下文直接生成用例（展开operations_chain/ui_elements/field_specs）

    与generate_testcase不同，此函数优先直接展开P5结构化数据，
    而非依赖category模板。

    Args:
        tp: P5测试点dict（含operations_chain/ui_elements/field_specs等）
        case_idx: 用例序号
        skeleton_entry: 骨架条目

    Returns:
        dict: 完整的用例fields
    """
    description = tp.get("description", "")
    precondition = tp.get("precondition", "")
    operations_chain = tp.get("operations_chain", []) or []
    ui_elements = tp.get("ui_elements", []) or []
    field_specs = tp.get("field_specs", []) or []
    test_data_matrix = tp.get("test_data_matrix", []) or []
    exception_scenarios = tp.get("exception_scenarios", []) or []

    # A/B分类判断
    ab_class = "A"
    ab_reason = ""
    try:
        ab_class, ab_reason = classify_test_point(tp)
    except Exception:
        ab_reason = "分类异常，默认A类"

    # 提取关键词
    kw = extract_keywords(description, precondition)
    role = kw["roles"][0]

    # ---- 生成步骤和期望 ----
    if ab_class == "A" and operations_chain and len(operations_chain) >= 3:
        # A类有完整操作链：直接展开
        steps, expected = _generate_a_class_steps(tp, case_idx, kw)
    elif ab_class == "B":
        # B类：字段校验
        steps, expected = _generate_b_class_steps(tp, case_idx, kw)
    else:
        # 回退到标准生成
        steps, expected = _gen_main_flow(tp, case_idx, kw)

    # ---- 构建前置条件 ----
    precond_parts = [f"1. {role}已登录CRM系统，账户状态正常"]
    if precondition:
        precond_parts.append(f"2. {precondition}")
    else:
        precond_parts.append("2. 预置相关测试数据，通过后台接口创建")
    precond_parts.append("3. 系统处于正常工作状态，相关服务可用")

    # ---- 构建标题 ----
    case_type_map = {1: "正向验证", 2: "异常验证", 3: "边界验证"}
    case_type_label = case_type_map.get(case_idx, "补充验证")
    title = f"{description[:30]}-{case_type_label}"

    # ---- 模块名 ----
    module_name = _extract_module(tp)

    # ---- A/B标签 ----
    ab_tag = "[A类-业务流程]" if ab_class == "A" else "[B类-字段边界]"

    return {
        "title": title,
        "preconditions": "；".join(precond_parts),
        "steps": "\n".join(steps),
        "expected_results": "\n".join(expected),
        "test_case_type": case_type_label,
        "test_category": "功能",
        "test_suite": module_name,
        "remarks": f"{ab_tag}[{module_name}]",
        "ab_class": ab_class,
        "ab_reason": ab_reason,
    }


# ============================================================
# V3.4.1: AI生成后的格式标准化
# ============================================================

def format_testcase(raw_fields, tp=None):
    """AI生成后的格式标准化

    对AI生成的用例fields进行格式标准化，确保字段完整性和规范性。
    同时添加A/B分类标记。

    Args:
        raw_fields: AI生成的原始fields dict
        tp: 可选的测试点dict，用于A/B分类和模块提取

    Returns:
        dict: 标准化后的用例fields
    """
    if not isinstance(raw_fields, dict):
        return raw_fields

    # ---- 1. 标题标准化 ----
    title = str(raw_fields.get("title", "")).strip()
    if not title:
        title = "未命名用例"
    # 去除多余空格
    title = re.sub(r'\s+', ' ', title)

    # ---- 2. 步骤编号标准化 ----
    steps_text = str(raw_fields.get("steps", ""))
    steps_lines = [line.strip() for line in steps_text.split("\n") if line.strip()]
    _num_pattern = re.compile(r'^\d+[.、)）]\s*')
    steps_lines = [f"{i+1}. {_num_pattern.sub('', line)}" for i, line in enumerate(steps_lines)]

    # ---- 3. 期望结果编号标准化 ----
    expected_text = str(raw_fields.get("expected_results", ""))
    expected_lines = [line.strip() for line in expected_text.split("\n") if line.strip()]
    expected_lines = [f"{i+1}. {_num_pattern.sub('', line)}" for i, line in enumerate(expected_lines)]

    # ---- 4. 前置条件标准化 ----
    precond_text = str(raw_fields.get("preconditions", "")).strip()
    if not precond_text:
        precond_text = "1. 用户已登录系统，账户状态正常；2. 预置相关测试数据；3. 系统处于正常工作状态"

    # ---- 5. A/B分类 ----
    ab_class = raw_fields.get("ab_class", "")
    ab_reason = raw_fields.get("ab_reason", "")
    if not ab_class and tp:
        try:
            ab_class, ab_reason = classify_test_point(tp)
        except Exception:
            ab_class = "A"
            ab_reason = "分类异常，默认A类"
    if not ab_class:
        ab_class = "A"
        ab_reason = "无测试点数据，默认A类"

    # ---- 6. 模块名 ----
    module_name = raw_fields.get("test_suite", "")
    if not module_name and tp:
        module_name = _extract_module(tp)
    if not module_name:
        module_name = "未分类模块"

    # ---- 7. A/B标签 ----
    ab_tag = "[A类-业务流程]" if ab_class == "A" else "[B类-字段边界]"

    # ---- 8. remarks标准化 ----
    remarks = str(raw_fields.get("remarks", "")).strip()
    if ab_tag not in remarks:
        remarks = f"{ab_tag}{remarks}"

    return {
        "title": title,
        "preconditions": precond_text,
        "steps": "\n".join(steps_lines),
        "expected_results": "\n".join(expected_lines),
        "test_case_type": raw_fields.get("test_case_type", "正向验证"),
        "test_category": raw_fields.get("test_category", "功能"),
        "test_suite": module_name,
        "remarks": remarks,
        "ab_class": ab_class,
        "ab_reason": ab_reason,
    }
