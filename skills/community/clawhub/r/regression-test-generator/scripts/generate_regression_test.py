#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回归测试用例生成器
根据变更描述自动推荐需要执行的回归测试用例
"""

import re
import sys
import json
from datetime import datetime

# 模块关键词映射
MODULE_KEYWORDS = {
    'algorithm': ['算法', '计算', '逻辑', 'algorithm', 'calculate'],
    'sensor': ['传感器', 'sensor', '检测', '读取'],
    'reagent': ['试剂', 'reagent', '缓冲液', '系统液', '耗材'],
    'ui': ['界面', 'UI', '显示', '按钮', '布局', '颜色'],
    'database': ['数据库', 'database', '存储', '数据'],
    'api': ['接口', 'API', '通信', 'LIS', '传输'],
    'security': ['安全', 'security', '权限', '登录', '认证'],
    'report': ['报告', 'report', '结果', '打印', '导出'],
}

# 测试用例模板库
TEST_CASE_LIBRARY = {
    'algorithm': [
        {'id': 'TC-032', 'name': '缓冲液不足时提示并停止实验', 'type': '功能测试', 'priority_base': 'high', 'time': 15},
        {'id': 'TC-045', 'name': '连续多个实验的缓冲液累计消耗', 'type': '功能测试', 'priority_base': 'high', 'time': 20},
        {'id': 'TC-078', 'name': '不同人份数的缓冲液计算', 'type': '功能测试', 'priority_base': 'medium', 'time': 15},
        {'id': 'TC-089', 'name': '界面显示消耗量格式', 'type': 'UI 测试', 'priority_base': 'low', 'time': 5},
        {'id': 'TC-091', 'name': '缓冲液余量显示准确性', 'type': '功能测试', 'priority_base': 'medium', 'time': 10},
    ],
    'sensor': [
        {'id': 'TC-101', 'name': '试剂仓传感器数据准确性验证', 'type': '功能测试', 'priority_base': 'high', 'time': 20},
        {'id': 'TC-102', 'name': '传感器故障时的错误处理', 'type': '异常测试', 'priority_base': 'high', 'time': 15},
        {'id': 'TC-105', 'name': '重试机制功能验证（最多 3 次）', 'type': '功能测试', 'priority_base': 'medium', 'time': 20},
        {'id': 'TC-108', 'name': '试剂余量计算准确性', 'type': '功能测试', 'priority_base': 'medium', 'time': 15},
    ],
    'reagent': [
        {'id': 'TC-032', 'name': '缓冲液不足时提示并停止实验', 'type': '功能测试', 'priority_base': 'high', 'time': 15},
        {'id': 'TC-045', 'name': '连续多个实验的缓冲液累计消耗', 'type': '功能测试', 'priority_base': 'high', 'time': 20},
        {'id': 'TC-078', 'name': '不同人份数的缓冲液计算', 'type': '功能测试', 'priority_base': 'medium', 'time': 15},
        {'id': 'TC-110', 'name': '试剂更换流程验证', 'type': '功能测试', 'priority_base': 'high', 'time': 25},
        {'id': 'TC-115', 'name': '试剂有效期检查', 'type': '功能测试', 'priority_base': 'medium', 'time': 10},
    ],
    'ui': [
        {'id': 'TC-201', 'name': '主界面按钮可点击性验证', 'type': 'UI 测试', 'priority_base': 'medium', 'time': 10},
        {'id': 'TC-202', 'name': '界面在不同分辨率下的显示', 'type': '兼容性测试', 'priority_base': 'medium', 'time': 15},
        {'id': 'TC-205', 'name': '按钮颜色和样式一致性', 'type': 'UI 测试', 'priority_base': 'low', 'time': 10},
        {'id': 'TC-208', 'name': '界面文字清晰可读', 'type': 'UI 测试', 'priority_base': 'low', 'time': 5},
        {'id': 'TC-210', 'name': '界面操作流程顺畅性', 'type': '用户体验测试', 'priority_base': 'medium', 'time': 15},
    ],
    'database': [
        {'id': 'TC-301', 'name': '数据存储完整性验证', 'type': '功能测试', 'priority_base': 'high', 'time': 20},
        {'id': 'TC-302', 'name': '数据库异常恢复测试', 'type': '异常测试', 'priority_base': 'high', 'time': 25},
        {'id': 'TC-305', 'name': '历史数据查询准确性', 'type': '功能测试', 'priority_base': 'medium', 'time': 15},
    ],
    'api': [
        {'id': 'TC-401', 'name': 'LIS 通信数据准确性', 'type': '接口测试', 'priority_base': 'high', 'time': 20},
        {'id': 'TC-402', 'name': '网络中断后数据重传', 'type': '异常测试', 'priority_base': 'high', 'time': 20},
        {'id': 'TC-405', 'name': '数据导出格式验证', 'type': '功能测试', 'priority_base': 'medium', 'time': 15},
    ],
    'security': [
        {'id': 'TC-501', 'name': '用户权限验证', 'type': '安全测试', 'priority_base': 'high', 'time': 15},
        {'id': 'TC-502', 'name': '登录失败锁定机制', 'type': '安全测试', 'priority_base': 'high', 'time': 15},
        {'id': 'TC-505', 'name': '审计追踪记录完整性', 'type': '安全测试', 'priority_base': 'high', 'time': 20},
    ],
    'report': [
        {'id': 'TC-601', 'name': '检测结果报告格式验证', 'type': '功能测试', 'priority_base': 'high', 'time': 15},
        {'id': 'TC-602', 'name': '报告数据准确性核对', 'type': '功能测试', 'priority_base': 'high', 'time': 20},
        {'id': 'TC-605', 'name': '报告打印功能验证', 'type': '功能测试', 'priority_base': 'medium', 'time': 10},
    ],
}

# 变更类型关键词
CHANGE_TYPE_KEYWORDS = {
    'fix': ['修复', 'fix', 'bug', '问题', '错误'],
    'feat': ['新增', '添加', 'feat', '功能', '支持'],
    'refactor': ['重构', 'refactor', '优化', '整理'],
    'ui': ['界面', 'UI', '样式', '颜色', '布局'],
}

def detect_modules(change_desc: str) -> list:
    """检测受影响的模块"""
    detected = []
    desc_lower = change_desc.lower()
    
    for module, keywords in MODULE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in desc_lower:
                detected.append(module)
                break
    
    return detected if detected else ['core']

def detect_change_type(change_desc: str) -> str:
    """检测变更类型"""
    desc_lower = change_desc.lower()
    
    for change_type, keywords in CHANGE_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in desc_lower:
                return change_type
    
    return 'other'

def adjust_priority(test_case: dict, change_type: str, is_patient_safety: bool) -> str:
    """根据变更类型调整优先级"""
    base_priority = test_case['priority_base']
    
    # 患者安全相关，直接提升为高
    if is_patient_safety:
        return 'high'
    
    # Bug 修复，高优先级用例保持高
    if change_type == 'fix' and base_priority == 'high':
        return 'high'
    
    # 界面变更，降低非 UI 测试优先级
    if change_type == 'ui' and 'UI' not in test_case['type']:
        if base_priority == 'high':
            return 'medium'
    
    return base_priority

def is_patient_safety_related(change_desc: str) -> bool:
    """判断是否涉及患者安全"""
    safety_keywords = ['安全', '患者', '结果', '检测', '计算', '剂量', '浓度', '阳性', '阴性']
    return any(kw in change_desc for kw in safety_keywords)

def generate_test_recommendations(change_desc: str) -> dict:
    """生成测试建议"""
    modules = detect_modules(change_desc)
    change_type = detect_change_type(change_desc)
    is_safety = is_patient_safety_related(change_desc)
    
    recommendations = {'high': [], 'medium': [], 'low': []}
    total_time = 0
    
    # 收集相关测试用例
    seen_ids = set()
    for module in modules:
        test_cases = TEST_CASE_LIBRARY.get(module, [])
        for tc in test_cases:
            if tc['id'] in seen_ids:
                continue
            seen_ids.add(tc['id'])
            
            priority = adjust_priority(tc, change_type, is_safety)
            tc_with_priority = {**tc, 'priority': priority}
            recommendations[priority].append(tc_with_priority)
            total_time += tc['time']
    
    # 如果没有匹配到用例，返回通用建议
    if not any(recommendations.values()):
        recommendations['medium'] = [{
            'id': 'TC-999',
            'name': '核心功能冒烟测试',
            'type': '功能测试',
            'priority': 'medium',
            'time': 30
        }]
        total_time = 30
    
    return {
        'recommendations': recommendations,
        'total_time': total_time,
        'modules': modules,
        'change_type': change_type
    }

def format_output(recommendations: dict, change_desc: str) -> str:
    """格式化输出"""
    rec = recommendations['recommendations']
    total_time = recommendations['total_time']
    modules = recommendations['modules']
    
    output = f"""# 🧪 回归测试建议

**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**变更内容：** {change_desc}  
**影响模块：** {', '.join(modules)}

---

## 回归测试清单

"""
    
    # 高优先级
    if rec['high']:
        output += "### 🔴 高优先级（必须执行）\n\n"
        for i, tc in enumerate(rec['high'], 1):
            output += f"{i}. **{tc['id']}**: {tc['name']}\n"
            output += f"   类型：{tc['type']} | 预计：{tc['time']} 分钟\n\n"
    
    # 中优先级
    if rec['medium']:
        output += "### 🟡 中优先级（建议执行）\n\n"
        for i, tc in enumerate(rec['medium'], 1):
            output += f"{i}. **{tc['id']}**: {tc['name']}\n"
            output += f"   类型：{tc['type']} | 预计：{tc['time']} 分钟\n\n"
    
    # 低优先级
    if rec['low']:
        output += "### 🟢 低优先级（可选执行）\n\n"
        for i, tc in enumerate(rec['low'], 1):
            output += f"{i}. **{tc['id']}**: {tc['name']}\n"
            output += f"   类型：{tc['type']} | 预计：{tc['time']} 分钟\n\n"
    
    # 汇总
    output += f"""---

## 汇总信息

| 优先级 | 用例数量 | 说明 |
|--------|----------|------|
| 高 | {len(rec['high'])} | 必须执行，涉及核心功能/患者安全 |
| 中 | {len(rec['medium'])} | 建议执行，涉及重要功能 |
| 低 | {len(rec['low'])} | 可选执行，涉及边缘功能 |

**预计总耗时：** {total_time} 分钟（约 {total_time/60:.1f} 小时）

---

## 执行建议

1. **时间紧张时** - 优先执行高优先级用例
2. **Bug 修复** - 高 + 中优先级用例全部执行
3. **版本发布** - 所有用例建议执行
4. **界面变更** - 可适当降低非 UI 测试优先级

---

**提示：** 实际执行时间可能因环境和个人操作习惯有所不同
"""
    
    return output

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供变更描述'}, ensure_ascii=False))
        sys.exit(1)
    
    change_desc = ' '.join(sys.argv[1:])
    recommendations = generate_test_recommendations(change_desc)
    output = format_output(recommendations, change_desc)
    
    print(output)

if __name__ == '__main__':
    main()
