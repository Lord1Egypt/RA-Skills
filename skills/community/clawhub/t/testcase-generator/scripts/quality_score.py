#!/usr/bin/env python3
"""
测试用例质量评分工具
评估维度：覆盖率、可执行性、独立性、可维护性、完备性
"""

import sys
import json
import re

def calculate_coverage_score(test_cases, requirements):
    """覆盖率评分 - 检查需求点是否有对应用例"""
    if not requirements:
        return 100, "未提供需求点，跳过覆盖率检查"
    
    # 简单实现：检查用例数量是否足够
    min_cases = len(requirements) * 3  # 每个需求至少 3 个用例
    actual_cases = len(test_cases)
    
    if actual_cases >= min_cases:
        score = 100
    else:
        score = min(100, (actual_cases / min_cases) * 100)
    
    return score, f"用例数{actual_cases}，建议{min_cases}个"

def calculate_executability_score(test_cases):
    """可执行性评分 - 步骤清晰度"""
    scores = []
    issues = []
    
    for i, tc in enumerate(test_cases):
        steps = tc[4]
        expected = tc[5]
        
        # 检查步骤是否有编号
        has_numbering = bool(re.search(r'\d+\.', steps))
        
        # 检查步骤是否具体（长度）
        step_detail = len(steps) > 10
        
        # 检查预期结果是否具体
        expected_detail = len(expected) > 5
        
        # 检查是否有模糊词汇
        vague_words = ['可能', '也许', '大概', '应该', '等']
        has_vague = any(word in expected for word in vague_words)
        
        case_score = 100
        if not has_numbering:
            case_score -= 20
            issues.append(f"{tc[1]}: 步骤缺少编号")
        if not step_detail:
            case_score -= 20
            issues.append(f"{tc[1]}: 步骤描述过于简单")
        if not expected_detail:
            case_score -= 20
            issues.append(f"{tc[1]}: 预期结果不具体")
        if has_vague:
            case_score -= 20
            issues.append(f"{tc[1]}: 预期结果包含模糊词汇")
        
        scores.append(max(0, case_score))
    
    avg_score = sum(scores) / len(scores) if scores else 0
    return avg_score, f"{len(issues)} 个问题"

def calculate_independence_score(test_cases):
    """独立性评分 - 用例间依赖程度"""
    # 检查前置条件中是否依赖其他用例执行
    dependency_keywords = ['用例', '执行后', '完成后', '之后']
    dependent_count = 0
    
    for tc in test_cases:
        precondition = tc[3].lower()
        if any(keyword in precondition for keyword in dependency_keywords):
            dependent_count += 1
    
    total = len(test_cases)
    independent_count = total - dependent_count
    score = (independent_count / total) * 100 if total > 0 else 100
    
    return score, f"{dependent_count}个用例存在依赖"

def calculate_maintainability_score(test_cases):
    """可维护性评分 - 命名规范、结构清晰"""
    scores = []
    
    for tc in test_cases:
        tc_id = tc[1]
        title = tc[2]
        
        case_score = 100
        
        # 检查 ID 格式
        if not re.match(r'TC-[A-Z]+-\d+', tc_id):
            case_score -= 20
        
        # 检查标题长度
        if len(title) < 5 or len(title) > 50:
            case_score -= 10
        
        # 检查标题是否包含功能点
        if len(title.split()) < 2:
            case_score -= 10
        
        scores.append(max(0, case_score))
    
    avg_score = sum(scores) / len(scores) if scores else 0
    return avg_score, "命名规范检查完成"

def calculate_completeness_score(test_cases):
    """完备性评分 - 测试类型分布"""
    type_count = {}
    for tc in test_cases:
        test_type = tc[6]
        type_count[test_type] = type_count.get(test_type, 0) + 1
    
    # 期望的测试类型
    expected_types = ['功能测试', '异常测试', '边界测试', '安全测试', '性能测试']
    covered_types = len([t for t in expected_types if type_count.get(t, 0) > 0])
    
    score = (covered_types / len(expected_types)) * 100
    
    types_info = ', '.join([f"{t}:{c}" for t, c in type_count.items()])
    return score, f"覆盖{covered_types}/{len(expected_types)}种类型 ({types_info})"

def main():
    if len(sys.argv) < 2:
        print("用法：python quality_score.py <测试用例 JSON 文件> [需求 JSON 文件]")
        sys.exit(1)
    
    # 读取测试用例
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        test_cases_data = json.load(f)
    
    # 转换为列表格式
    test_cases = []
    for tc in test_cases_data:
        test_cases.append([
            tc.get('module', '模块'),
            tc.get('id', 'TC-001'),
            tc.get('title', '标题'),
            tc.get('precondition', ''),
            tc.get('steps', ''),
            tc.get('expected', ''),
            tc.get('type', '功能测试'),
            tc.get('priority', 'P2'),
            tc.get('stage', '系统测试')
        ])
    
    # 读取需求（可选）
    requirements = []
    if len(sys.argv) > 3:
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            requirements = json.load(f)
    
    print("=" * 70)
    print("测试用例质量评估报告")
    print("=" * 70)
    print(f"用例总数：{len(test_cases)}")
    print()
    
    # 各维度评分
    coverage_score, coverage_info = calculate_coverage_score(test_cases, requirements)
    exec_score, exec_info = calculate_executability_score(test_cases)
    indep_score, indep_info = calculate_independence_score(test_cases)
    maint_score, maint_info = calculate_maintainability_score(test_cases)
    comp_score, comp_info = calculate_completeness_score(test_cases)
    
    print("各维度评分：")
    print(f"  📊 覆盖率：   {coverage_score:6.1f}/100  ({coverage_info})")
    print(f"  ✅ 可执行性： {exec_score:6.1f}/100  ({exec_info})")
    print(f"  🔗 独立性：   {indep_score:6.1f}/100  ({indep_info})")
    print(f"  📝 可维护性： {maint_score:6.1f}/100  ({maint_info})")
    print(f"  📋 完备性：   {comp_score:6.1f}/100  ({comp_info})")
    print()
    
    # 综合评分
    total_score = (coverage_score + exec_score + indep_score + maint_score + comp_score) / 5
    print("-" * 70)
    print(f"🎯 综合评分：{total_score:.1f}/100")
    print()
    
    # 评级
    if total_score >= 90:
        grade = "A+ (优秀)"
    elif total_score >= 80:
        grade = "A (良好)"
    elif total_score >= 70:
        grade = "B (中等)"
    elif total_score >= 60:
        grade = "C (合格)"
    else:
        grade = "D (需改进)"
    
    print(f"📈 评级：{grade}")
    print("=" * 70)
    
    # 改进建议
    print("\n💡 改进建议：")
    if coverage_score < 80:
        print("  - 增加测试用例数量，确保每个需求点有至少 3 个用例覆盖")
    if exec_score < 80:
        print("  - 优化测试步骤描述，添加编号，避免模糊词汇")
    if indep_score < 80:
        print("  - 减少用例间依赖，确保用例可独立执行")
    if maint_score < 80:
        print("  - 规范用例 ID 格式（TC-模块 - 序号），优化标题命名")
    if comp_score < 80:
        print("  - 补充测试类型，覆盖异常/边界/安全/性能测试")
    
    if total_score >= 80:
        print("  ✅ 用例质量良好，可以投入使用")
    
    print()
    
    # 返回综合评分
    return 0 if total_score >= 60 else 1

if __name__ == '__main__':
    sys.exit(main())
