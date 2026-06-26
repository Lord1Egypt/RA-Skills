#!/usr/bin/env python3
"""
飞书数据收集器 - 从飞书文档/Bitable/聊天收集报告数据
此脚本生成一个JSON数据文件，供 generate_report.py 使用

注意：实际的飞书API调用由OpenClaw的feishu工具完成，
此脚本负责解析和结构化收集到的数据。
"""

import json
import argparse
from datetime import datetime

def _classify_line(line):
    """对单行文本进行分类，返回类别名或 None。
    
    优先级（高到低）：风险 > 完成 > 进行中 > 计划
    一行只归入一个类别，避免重复匹配。
    """
    if not line.strip():
        return None

    # 用行首 emoji 前缀做最高优先级判断
    prefix_map = {
        "✅": "completed",
        "✔️": "completed",
        "🔄": "in_progress",
        "⏳": "in_progress",
        "📅": "planned",
        "📌": "planned",
        "⚠️": "risks",
        "🚨": "risks",
        "❌": "risks",
    }
    for emoji, category in prefix_map.items():
        if line.lstrip().startswith(emoji):
            return category

    # 无 emoji 前缀时，按优先级关键词匹配（互斥）
    # 优先级：风险 > 完成 > 进行中 > 计划
    risk_markers = ["风险", "阻塞", "延期", "问题", "bug", "失败", "异常"]
    complete_markers = ["完成", "已完成", "done", "上线", "发布", "搞定", "解决"]
    progress_markers = ["进行中", "开发中", "wip", "待完成", "待审核"]
    plan_markers = ["计划", "预计", "明天", "下周", "待办", "TODO"]

    line_lower = line.lower()
    for marker in risk_markers:
        if marker in line_lower:
            return "risks"
    for marker in complete_markers:
        if marker in line_lower:
            return "completed"
    for marker in progress_markers:
        if marker in line_lower:
            return "in_progress"
    for marker in plan_markers:
        if marker in line_lower:
            return "planned"

    return None


def parse_doc_content(raw_content, keywords=None):
    """从飞书文档内容中提取关键信息"""
    items = {
        "completed": [],
        "in_progress": [],
        "planned": [],
        "risks": [],
        "metrics": []
    }
    
    if not raw_content:
        return items
    
    lines = raw_content.split("\n") if isinstance(raw_content, str) else []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        category = _classify_line(line)
        if category and category in items:
            items[category].append(line)
    
    return items

def merge_data_sources(sources):
    """合并多个数据源的提取结果"""
    merged = {
        "completed": [],
        "in_progress": [],
        "planned": [],
        "risks": [],
        "metrics": []
    }
    
    for source in sources:
        for key in merged:
            if key in source:
                merged[key].extend(source[key])
    
    # 去重
    for key in merged:
        merged[key] = list(dict.fromkeys(merged[key]))
    
    return merged

def main():
    parser = argparse.ArgumentParser(description="飞书数据收集器")
    parser.add_argument("--input", help="输入JSON文件（飞书工具的原始输出）")
    parser.add_argument("--output", help="输出JSON文件路径")
    parser.add_argument("--source-type", choices=["doc", "bitable", "chat"], default="doc", help="数据源类型")
    args = parser.parse_args()
    
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    else:
        raw_data = {}
    
    # 解析数据
    if args.source_type == "doc":
        items = parse_doc_content(raw_data.get("content", ""))
    else:
        items = parse_doc_content(str(raw_data))
    
    # 输出
    result = {
        "generated_at": datetime.now().isoformat(),
        "source_type": args.source_type,
        "data": items
    }
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"数据已写入: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
