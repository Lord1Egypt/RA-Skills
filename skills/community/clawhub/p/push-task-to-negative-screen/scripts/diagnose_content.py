#!/usr/bin/env python3
"""
内容字段诊断工具
用于诊断 content 字段显示 \n\n 的问题
"""

import json
import sys
import os

def diagnose_content(content):
    """诊断内容字段"""
    print("=" * 60)
    print("内容字段诊断报告")
    print("=" * 60)
    
    if not content:
        print("[ERROR] 内容为空")
        return
    
    print(f"内容类型: {type(content)}")
    print(f"内容长度: {len(content)}")
    
    # 显示原始内容（使用 repr 显示转义字符）
    print(f"\n原始内容 (repr):")
    print(repr(content[:200]) + ("..." if len(content) > 200 else ""))
    
    # 显示实际内容
    print(f"\n实际内容:")
    print(content[:200] + ("..." if len(content) > 200 else ""))
    
    # 检查换行符
    print(f"\n换行符分析:")
    single_newline_count = content.count('\n')
    escaped_newline_count = content.count('\\n')
    double_escaped_count = content.count('\\\\n')
    
    print(f"  实际换行符 (\\n): {single_newline_count}")
    print(f"  转义换行符 (\\\\n): {escaped_newline_count}")
    print(f"  双重转义换行符 (\\\\\\\\n): {double_escaped_count}")
    
    # 检查其他转义字符
    print(f"\n其他转义字符:")
    escape_chars = ['\\t', '\\r', '\\\\', '\\"', "\\'"]
    for char in escape_chars:
        count = content.count(char)
        if count > 0:
            print(f"  {repr(char)}: {count}")
    
    # 诊断结果
    print(f"\n诊断结果:")
    if escaped_newline_count > 0 and single_newline_count == 0:
        print("[ERROR] 问题：内容包含转义的换行符 (\\\\n)，但没有实际换行符")
        print("   可能原因：JSON 双重序列化或字符串转义错误")
        print("   解决方案：使用 content.replace('\\\\n', '\\n')")
    elif double_escaped_count > 0:
        print("[ERROR] 问题：内容包含双重转义的换行符 (\\\\\\\\n)")
        print("   可能原因：多次 JSON 序列化")
        print("   解决方案：检查数据生成流程，避免多重序列化")
    elif single_newline_count > 0:
        print("[OK] 正常：内容包含实际换行符")
    else:
        print("[INFO] 信息：内容没有换行符")
    
    # 修复建议
    print(f"\n修复建议:")
    if escaped_newline_count > 0:
        print("1. 在数据生成时避免转义换行符")
        print("2. 使用以下代码修复:")
        print("   fixed_content = content.replace('\\\\n', '\\n')")
        print("3. 检查 JSON 序列化次数")

def diagnose_json_file(filepath):
    """诊断 JSON 文件"""
    print(f"\n诊断文件: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'task_content' in data:
            diagnose_content(data['task_content'])
        else:
            print("[ERROR] 文件中没有 task_content 字段")
            print("可用字段:", list(data.keys()))
    
    except Exception as e:
        print(f"[ERROR] 文件读取失败: {e}")

def diagnose_json_string(json_str):
    """诊断 JSON 字符串"""
    print(f"\n诊断 JSON 字符串")
    
    try:
        data = json.loads(json_str)
        
        if 'task_content' in data:
            diagnose_content(data['task_content'])
        else:
            print("[ERROR] JSON 中没有 task_content 字段")
            print("可用字段:", list(data.keys()))
    
    except Exception as e:
        print(f"❌ JSON 解析失败: {e}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python diagnose_content.py <JSON文件路径>")
        print("  python diagnose_content.py --json '{\"task_content\": \"...\"}'")
        print("  python diagnose_content.py --test  # 运行测试用例")
        return
    
    if sys.argv[1] == '--json':
        if len(sys.argv) < 3:
            print("请提供 JSON 字符串")
            return
        diagnose_json_string(sys.argv[2])
    
    elif sys.argv[1] == '--test':
        print("运行测试用例...")
        
        # 测试用例1：正常内容
        print("\n测试用例1：正常内容（实际换行符）")
        normal_content = "第一行\n\n第二行\n第三行"
        diagnose_content(normal_content)
        
        # 测试用例2：转义的内容
        print("\n测试用例2：转义的内容（\\\\n）")
        escaped_content = "第一行\\n\\n第二行\\n第三行"
        diagnose_content(escaped_content)
        
        # 测试用例3：双重转义
        print("\n测试用例3：双重转义的内容（\\\\\\\\n）")
        double_escaped = "第一行\\\\n\\\\n第二行\\\\n第三行"
        diagnose_content(double_escaped)
    
    else:
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            diagnose_json_file(filepath)
        else:
            print(f"❌ 文件不存在: {filepath}")

if __name__ == "__main__":
    main()