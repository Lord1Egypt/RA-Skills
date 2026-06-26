#!/usr/bin/env python3
"""
测试用例导出工具
支持格式：CSV, Markdown, JSON, XMind, TestLink XML
"""

import sys
import json
import csv
from io import StringIO

def export_to_csv(test_cases, output_path):
    """导出为 CSV"""
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        headers = ["模块名称", "用例 ID", "用例标题", "前置条件", "步骤", "预期", "测试类型", "优先级", "测试所属阶段"]
        writer.writerow(headers)
        for tc in test_cases:
            writer.writerow(tc)
    return f"✅ CSV 文件已导出：{output_path}"

def export_to_markdown(test_cases, output_path):
    """导出为 Markdown"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 测试用例\n\n")
        
        # 按优先级分组统计
        p0 = sum(1 for tc in test_cases if tc[7] == "P0")
        p1 = sum(1 for tc in test_cases if tc[7] == "P1")
        p2 = sum(1 for tc in test_cases if tc[7] == "P2")
        
        f.write(f"**总用例数**: {len(test_cases)}  \n")
        f.write(f"- P0: {p0} 个\n")
        f.write(f"- P1: {p1} 个\n")
        f.write(f"- P2: {p2} 个\n\n")
        
        f.write("## 测试用例详情\n\n")
        f.write("| 用例 ID | 用例标题 | 前置条件 | 测试步骤 | 预期结果 | 测试类型 | 优先级 |\n")
        f.write("|---------|----------|----------|----------|----------|----------|--------|\n")
        
        for tc in test_cases:
            module, tc_id, title, precondition, steps, expected, test_type, priority, stage = tc
            # 替换换行符为 HTML 换行
            steps_md = steps.replace('\n', '<br>')
            f.write(f"| {tc_id} | {title} | {precondition} | {steps_md} | {expected} | {test_type} | {priority} |\n")
        
        f.write("\n---\n*由 test-case-generator 自动生成*\n")
    
    return f"✅ Markdown 文件已导出：{output_path}"

def export_to_json(test_cases, output_path):
    """导出为 JSON"""
    data = []
    for tc in test_cases:
        data.append({
            "module": tc[0],
            "id": tc[1],
            "title": tc[2],
            "precondition": tc[3],
            "steps": tc[4].split('\n'),
            "expected": tc[5],
            "type": tc[6],
            "priority": tc[7],
            "stage": tc[8]
        })
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return f"✅ JSON 文件已导出：{output_path}"

def export_to_xmind(test_cases, output_path):
    """导出为 XMind 兼容的 JSON 格式"""
    xmind_data = {
        "rootTopic": {
            "title": "测试用例",
            "children": {
                "attached": [
                    {
                        "title": f"P0 高优先级 ({sum(1 for tc in test_cases if tc[7] == 'P0')}个)",
                        "children": {
                            "attached": [
                                {
                                    "title": f"{tc[1]} {tc[2]}",
                                    "notes": {
                                        "plain": f"前置条件：{tc[3]}\n\n步骤：{tc[4]}\n\n预期：{tc[5]}\n\n类型：{tc[6]}"
                                    }
                                }
                                for tc in test_cases if tc[7] == "P0"
                            ]
                        }
                    },
                    {
                        "title": f"P1 中优先级 ({sum(1 for tc in test_cases if tc[7] == 'P1')}个)",
                        "children": {
                            "attached": [
                                {
                                    "title": f"{tc[1]} {tc[2]}",
                                    "notes": {
                                        "plain": f"前置条件：{tc[3]}\n\n步骤：{tc[4]}\n\n预期：{tc[5]}\n\n类型：{tc[6]}"
                                    }
                                }
                                for tc in test_cases if tc[7] == "P1"
                            ]
                        }
                    },
                    {
                        "title": f"P2 低优先级 ({sum(1 for tc in test_cases if tc[7] == 'P2')}个)",
                        "children": {
                            "attached": [
                                {
                                    "title": f"{tc[1]} {tc[2]}",
                                    "notes": {
                                        "plain": f"前置条件：{tc[3]}\n\n步骤：{tc[4]}\n\n预期：{tc[5]}\n\n类型：{tc[6]}"
                                    }
                                }
                                for tc in test_cases if tc[7] == "P2"
                            ]
                        }
                    }
                ]
            }
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(xmind_data, f, ensure_ascii=False, indent=2)
    
    return f"✅ XMind 文件已导出：{output_path}（可用 XMind 导入）"

def export_to_testlink(test_cases, output_path):
    """导出为 TestLink XML 格式"""
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<testsuite>')
    
    for tc in test_cases:
        module, tc_id, title, precondition, steps, expected, test_type, priority, stage = tc
        priority_map = {"P0": "1", "P1": "2", "P2": "3"}
        
        xml_lines.append(f'  <testcase name="{tc_id} {title}" importance="{priority_map.get(priority, "3")}" exec_order="1">')
        xml_lines.append(f'    <preconditions><![CDATA[{precondition}]]></preconditions>')
        xml_lines.append(f'    <steps>')
        for i, step in enumerate(steps.split('\n'), 1):
            xml_lines.append(f'      <step><step_number><![CDATA[{i}]]></step_number><actions><![CDATA[{step}]]></actions><expectedresults><![CDATA[{expected}]]></expectedresults><active>1</active></step>')
        xml_lines.append(f'    </steps>')
        xml_lines.append(f'  </testcase>')
    
    xml_lines.append('</testsuite>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    return f"✅ TestLink XML 已导出：{output_path}"

def main():
    if len(sys.argv) < 3:
        print("用法：python export_testcases.py <格式> <输出路径>")
        print("格式：csv, markdown, md, json, xmind, testlink, xml")
        sys.exit(1)
    
    format_type = sys.argv[1].lower()
    output_path = sys.argv[2]
    
    # 从 stdin 读取测试用例 JSON
    input_data = sys.stdin.read()
    test_cases = json.loads(input_data)
    
    if format_type in ['csv']:
        result = export_to_csv(test_cases, output_path)
    elif format_type in ['markdown', 'md']:
        result = export_to_markdown(test_cases, output_path)
    elif format_type == 'json':
        result = export_to_json(test_cases, output_path)
    elif format_type == 'xmind':
        result = export_to_xmind(test_cases, output_path)
    elif format_type in ['testlink', 'xml']:
        result = export_to_testlink(test_cases, output_path)
    else:
        print(f"❌ 不支持的格式：{format_type}")
        sys.exit(1)
    
    print(result)

if __name__ == '__main__':
    main()
