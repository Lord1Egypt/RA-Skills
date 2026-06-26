#!/usr/bin/env python3
"""
需求变更对比与增量更新工具
对比新旧需求，识别变更点，建议更新用例
"""

import sys
import json
import difflib

def extract_requirements_points(text):
    """从需求文本中提取功能点（简单实现）"""
    # 按行分割，提取包含功能描述的行
    points = []
    for line in text.split('\n'):
        line = line.strip()
        if line and len(line) > 5:
            # 跳过纯标题
            if not line.startswith('#') and not line.startswith('-'):
                points.append(line)
    return points

def compare_requirements(old_text, new_text):
    """对比需求变更"""
    old_points = set(extract_requirements_points(old_text))
    new_points = set(extract_requirements_points(new_text))
    
    added = new_points - old_points
    removed = old_points - new_points
    unchanged = old_points & new_points
    
    return {
        "新增": list(added),
        "删除": list(removed),
        "未变": list(unchanged),
        "新增数量": len(added),
        "删除数量": len(removed)
    }

def analyze_impact(change_info, testcases):
    """分析变更对用例的影响"""
    impact = {
        "需新增用例": [],
        "需修改用例": [],
        "需删除用例": []
    }
    
    # 新增需求 -> 需要新增用例
    for req in change_info["新增"]:
        impact["需新增用例"].append({
            "需求点": req,
            "建议": f"为'{req[:30]}...'生成至少 3 个测试用例（正常 + 异常 + 边界）"
        })
    
    # 删除需求 -> 标记相关用例待删除
    for req in change_info["删除"]:
        for tc in testcases:
            if req[:10] in tc.get('title', '') or req[:10] in tc.get('expected', ''):
                impact["需删除用例"].append({
                    "需求点": req,
                    "相关用例": tc['id'],
                    "建议": "检查是否还需要保留"
                })
    
    # 未变需求 -> 检查用例是否需要更新
    for req in change_info["未变"][:5]:  # 只检查前 5 个
        for tc in testcases:
            if req[:10] in tc.get('title', ''):
                impact["需修改用例"].append({
                    "需求点": req,
                    "相关用例": tc['id'],
                    "建议": "确认用例是否仍然适用"
                })
    
    return impact

def generate_incremental_plan(change_info, impact):
    """生成增量更新计划"""
    plan = []
    
    plan.append("# 测试用例增量更新计划\n")
    plan.append(f"## 变更概览\n")
    plan.append(f"- 新增需求点：{change_info['新增数量']} 个")
    plan.append(f"- 删除需求点：{change_info['删除数量']} 个\n")
    
    if change_info["新增"]:
        plan.append("## 新增需求\n")
        for req in change_info["新增"][:10]:
            plan.append(f"- {req[:80]}")
        plan.append("")
    
    if change_info["删除"]:
        plan.append("## 删除需求\n")
        for req in change_info["删除"][:10]:
            plan.append(f"- {req[:80]}")
        plan.append("")
    
    plan.append("## 用例更新建议\n")
    plan.append(f"### 需新增用例 ({len(impact['需新增用例'])}个需求点)\n")
    for item in impact["需新增用例"][:5]:
        plan.append(f"- **{item['需求点'][:50]}...**")
        plan.append(f"  - {item['建议']}")
    
    plan.append(f"\n### 需检查用例 ({len(impact['需修改用例'])}个)\n")
    for item in impact["需修改用例"][:5]:
        plan.append(f"- {item['相关用例']}: {item['建议']}")
    
    plan.append(f"\n### 可能需删除 ({len(impact['需删除用例'])}个)\n")
    for item in impact["需删除用例"][:5]:
        plan.append(f"- {item['相关用例']}: {item['建议']}")
    
    return '\n'.join(plan)

def main():
    if len(sys.argv) < 3:
        print("用法：python diff_requirements.py <旧需求文件> <新需求文件> [用例 JSON]")
        sys.exit(1)
    
    old_file = sys.argv[1]
    new_file = sys.argv[2]
    testcase_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 读取需求文件
    with open(old_file, 'r', encoding='utf-8') as f:
        old_text = f.read()
    with open(new_file, 'r', encoding='utf-8') as f:
        new_text = f.read()
    
    # 对比需求
    change_info = compare_requirements(old_text, new_text)
    
    print("=" * 70)
    print("需求变更分析报告")
    print("=" * 70)
    print(f"新增需求点：{change_info['新增数量']} 个")
    print(f"删除需求点：{change_info['删除数量']} 个")
    print(f"未变需求点：{len(change_info['未变'])} 个")
    print()
    
    if change_info["新增"]:
        print("📝 新增需求:")
        for req in change_info["新增"][:5]:
            print(f"  + {req[:60]}...")
        if len(change_info["新增"]) > 5:
            print(f"  ... 还有 {len(change_info['新增']) - 5} 个")
        print()
    
    if change_info["删除"]:
        print("❌ 删除需求:")
        for req in change_info["删除"][:5]:
            print(f"  - {req[:60]}...")
        if len(change_info["删除"]) > 5:
            print(f"  ... 还有 {len(change_info['删除']) - 5} 个")
        print()
    
    # 如果有用例文件，分析影响
    if testcase_file:
        with open(testcase_file, 'r', encoding='utf-8') as f:
            testcases = json.load(f)
        
        impact = analyze_impact(change_info, testcases)
        
        print("-" * 70)
        print("用例影响分析:")
        print(f"  🆕 建议新增用例：{len(impact['需新增用例'])} 个需求点")
        print(f"  ✏️  建议检查用例：{len(impact['需修改用例'])} 个")
        print(f"  🗑️  可能需删除：{len(impact['需删除用例'])} 个")
        print()
        
        # 生成更新计划
        plan = generate_incremental_plan(change_info, impact)
        
        # 保存到文件
        output_file = 'incremental_update_plan.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plan)
        print(f"✅ 增量更新计划已保存到：{output_file}")
    else:
        print("💡 提示：提供用例 JSON 文件可生成详细的增量更新计划")
    
    print("=" * 70)

if __name__ == '__main__':
    main()
