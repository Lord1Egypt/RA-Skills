#!/usr/bin/env python3
"""
测试用例评审工具
支持逐条评审、批量修改、去重检测
"""

import sys
import json
import difflib

def load_testcases(path):
    """加载测试用例"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_testcases(testcases, path):
    """保存测试用例"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(testcases, f, ensure_ascii=False, indent=2)

def detect_duplicates(testcases):
    """检测相似用例"""
    duplicates = []
    n = len(testcases)
    
    for i in range(n):
        for j in range(i + 1, n):
            tc1 = testcases[i]
            tc2 = testcases[j]
            
            # 比较标题相似度
            similarity = difflib.SequenceMatcher(None, tc1['title'], tc2['title']).ratio()
            
            if similarity > 0.8:  # 相似度超过 80%
                duplicates.append({
                    "用例 1": {"id": tc1['id'], "标题": tc1['title']},
                    "用例 2": {"id": tc2['id'], "标题": tc2['title']},
                    "相似度": f"{similarity * 100:.1f}%"
                })
    
    return duplicates

def batch_update_priority(testcases, filter_type, new_priority):
    """批量修改优先级"""
    count = 0
    for tc in testcases:
        if filter_type == 'all' or tc.get('type') == filter_type:
            tc['priority'] = new_priority
            count += 1
    return count

def batch_update_stage(testcases, filter_type, new_stage):
    """批量修改测试阶段"""
    count = 0
    for tc in testcases:
        if filter_type == 'all' or tc.get('type') == filter_type:
            tc['stage'] = new_stage
            count += 1
    return count

def filter_by_priority(testcases, priority):
    """按优先级筛选"""
    return [tc for tc in testcases if tc.get('priority') == priority]

def filter_by_type(testcases, test_type):
    """按测试类型筛选"""
    return [tc for tc in testcases if tc.get('type') == test_type]

def statistics(testcases):
    """统计信息"""
    stats = {
        "总数": len(testcases),
        "按优先级": {},
        "按类型": {},
        "按阶段": {}
    }
    
    for tc in testcases:
        # 优先级统计
        p = tc.get('priority', 'P2')
        stats["按优先级"][p] = stats["按优先级"].get(p, 0) + 1
        
        # 类型统计
        t = tc.get('type', '功能测试')
        stats["按类型"][t] = stats["按类型"].get(t, 0) + 1
        
        # 阶段统计
        s = tc.get('stage', '系统测试')
        stats["按阶段"][s] = stats["按阶段"].get(s, 0) + 1
    
    return stats

def print_statistics(stats):
    """打印统计信息"""
    print("\n" + "=" * 60)
    print("测试用例统计")
    print("=" * 60)
    print(f"总数：{stats['总数']}")
    print("\n按优先级:")
    for p, count in sorted(stats['按优先级'].items()):
        print(f"  {p}: {count}个")
    print("\n按类型:")
    for t, count in sorted(stats['按类型'].items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}个")
    print("\n按阶段:")
    for s, count in sorted(stats['按阶段'].items()):
        print(f"  {s}: {count}个")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("测试用例评审工具")
        print("\n用法:")
        print("  python review_testcases.py <用例 JSON 文件> <命令> [参数]")
        print("\n命令:")
        print("  stats              - 显示统计信息")
        print("  duplicates         - 检测相似用例")
        print("  update-priority <类型> <新优先级> - 批量修改优先级")
        print("  update-stage <类型> <新阶段>    - 批量修改测试阶段")
        print("  filter-priority <优先级>        - 按优先级筛选")
        print("  filter-type <类型>              - 按类型筛选")
        print("  save <输出路径>                 - 保存修改")
        sys.exit(1)
    
    input_path = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'stats'
    
    testcases = load_testcases(input_path)
    
    if command == 'stats':
        stats_data = statistics(testcases)
        print_statistics(stats_data)
    
    elif command == 'duplicates':
        duplicates = detect_duplicates(testcases)
        if duplicates:
            print(f"\n⚠️  发现 {len(duplicates)} 对相似用例:\n")
            for dup in duplicates:
                print(f"  {dup['用例 1']['id']} {dup['用例 1']['标题']}")
                print(f"  ↔️ 相似度 {dup['相似度']}")
                print(f"  {dup['用例 2']['id']} {dup['用例 2']['标题']}")
                print()
        else:
            print("\n✅ 未发现相似用例")
    
    elif command == 'update-priority':
        if len(sys.argv) < 5:
            print("用法：python review_testcases.py <文件> update-priority <类型> <新优先级>")
            sys.exit(1)
        filter_type = sys.argv[3]
        new_priority = sys.argv[4]
        count = batch_update_priority(testcases, filter_type, new_priority)
        print(f"✅ 已更新 {count} 个用例的优先级为 {new_priority}")
        save_testcases(testcases, input_path)
    
    elif command == 'update-stage':
        if len(sys.argv) < 5:
            print("用法：python review_testcases.py <文件> update-stage <类型> <新阶段>")
            sys.exit(1)
        filter_type = sys.argv[3]
        new_stage = sys.argv[4]
        count = batch_update_stage(testcases, filter_type, new_stage)
        print(f"✅ 已更新 {count} 个用例的测试阶段为 {new_stage}")
        save_testcases(testcases, input_path)
    
    elif command == 'filter-priority':
        if len(sys.argv) < 4:
            print("用法：python review_testcases.py <文件> filter-priority <优先级>")
            sys.exit(1)
        priority = sys.argv[3]
        filtered = filter_by_priority(testcases, priority)
        print(f"\n找到 {len(filtered)} 个 {priority} 优先级的用例:")
        for tc in filtered[:10]:
            print(f"  {tc['id']} {tc['title']}")
        if len(filtered) > 10:
            print(f"  ... 还有 {len(filtered) - 10} 个")
    
    elif command == 'filter-type':
        if len(sys.argv) < 4:
            print("用法：python review_testcases.py <文件> filter-type <类型>")
            sys.exit(1)
        test_type = sys.argv[3]
        filtered = filter_by_type(testcases, test_type)
        print(f"\n找到 {len(filtered)} 个 {test_type} 类型的用例:")
        for tc in filtered[:10]:
            print(f"  {tc['id']} {tc['title']}")
        if len(filtered) > 10:
            print(f"  ... 还有 {len(filtered) - 10} 个")
    
    elif command == 'save':
        if len(sys.argv) < 4:
            print("用法：python review_testcases.py <文件> save <输出路径>")
            sys.exit(1)
        output_path = sys.argv[3]
        save_testcases(testcases, output_path)
        print(f"✅ 已保存到：{output_path}")
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
