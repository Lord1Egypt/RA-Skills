#!/usr/bin/env python3
"""
Skill Usage Analyzer - 分析任意 OpenClaw 技能并生成使用指南
"""
import os
import sys
import re
import json
import argparse

def parse_skill_md(filepath):
    """解析 SKILL.md 文件，提取关键信息."""
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'name': '',
        'description': '',
        'metadata': {},
        'features': [],
        'examples': [],
        'config': [],
        'warnings': [],
        'best_practices': [],
        'file_structure': []
    }
    
    # 提取 YAML frontmatter
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        # 提取 name
        name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
        if name_match:
            result['name'] = name_match.group(1).strip()
        
        # 提取 description
        desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
        if desc_match:
            result['description'] = desc_match.group(1).strip()
    
    # 如果没有从 frontmatter 获取到，尝试从内容中提取
    if not result['name']:
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            result['name'] = title_match.group(1).strip()
    
    # 提取功能列表（## Features, ## 功能, ## 核心功能 等）
    features_section = re.search(r'##\s*(?:Features|功能|核心功能|Features).*?\n(.*?)(?=##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if features_section:
        features_text = features_section.group(1)
        # 提取列表项
        feature_items = re.findall(r'[-*]\s*(.+?)(?=\n|$)', features_text)
        result['features'] = [f.strip() for f in feature_items if f.strip()]
    
    # 提取使用示例（## Usage, ## 使用, ## 示例, ## Examples 等）
    examples_section = re.search(r'##\s*(?:Usage|使用|示例|Examples|Quick Start|快速开始).*?\n(.*?)(?=##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if examples_section:
        examples_text = examples_section.group(1)
        # 提取代码块
        code_blocks = re.findall(r'```(?:\w+)?\s*\n(.*?)```', examples_text, re.DOTALL)
        result['examples'] = [cb.strip() for cb in code_blocks if cb.strip()]
        
        # 如果没有代码块，提取列表项作为示例
        if not result['examples']:
            example_items = re.findall(r'[-*]\s*(.+?)(?=\n|$)', examples_text)
            result['examples'] = [e.strip() for e in example_items if e.strip()]
    
    # 提取配置选项（## Config, ## 配置, ## Configuration 等）
    config_section = re.search(r'##\s*(?:Config|配置|Configuration|Options|选项).*?\n(.*?)(?=##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if config_section:
        config_text = config_section.group(1)
        config_items = re.findall(r'[-*]\s*(.+?)(?=\n|$)', config_text)
        result['config'] = [c.strip() for c in config_items if c.strip()]
    
    # 提取注意事项（## Notes, ## 注意, ## Warnings, ## 警告 等）
    warnings_section = re.search(r'##\s*(?:Notes|注意|Warnings|警告|Caution|注意事项|Requirements|要求).*?\n(.*?)(?=##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if warnings_section:
        warnings_text = warnings_section.group(1)
        warning_items = re.findall(r'[-*•]\s*(.+?)(?=\n|$)', warnings_text)
        result['warnings'] = [w.strip() for w in warning_items if w.strip()]
    
    # 提取最佳实践（## Tips, ## 提示, ## Best Practices, ## 最佳实践 等）
    tips_section = re.search(r'##\s*(?:Tips|提示|Best Practices|最佳实践|Recommendations|建议).*?\n(.*?)(?=##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if tips_section:
        tips_text = tips_section.group(1)
        tip_items = re.findall(r'[-*\d+\.]\s*(.+?)(?=\n|$)', tips_text)
        result['best_practices'] = [t.strip() for t in tip_items if t.strip()]
    
    # 分析文件结构
    skill_dir = os.path.dirname(filepath)
    if os.path.exists(skill_dir):
        for item in os.listdir(skill_dir):
            item_path = os.path.join(skill_dir, item)
            if os.path.isfile(item_path):
                result['file_structure'].append(f"📄 {item}")
            elif os.path.isdir(item_path):
                sub_items = os.listdir(item_path)
                result['file_structure'].append(f"📁 {item}/ ({len(sub_items)} 项)")
    
    return result

def generate_report(data, format='text'):
    """生成分析报告."""
    if format == 'json':
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    if format == 'markdown':
        return generate_markdown_report(data)
    
    return generate_text_report(data)

def generate_text_report(data):
    """生成文本格式报告."""
    lines = []
    name = data.get('name', 'Unknown Skill')
    
    # 标题
    lines.append(f"\n🔍 技能分析报告: {name}")
    lines.append("═" * 60)
    
    # 基本信息
    lines.append("\n📋 基本信息")
    lines.append("─" * 60)
    lines.append(f"名称: {name}")
    if data.get('description'):
        lines.append(f"描述: {data['description']}")
    
    # 核心功能
    if data.get('features'):
        lines.append(f"\n🎯 核心功能 ({len(data['features'])}个)")
        lines.append("─" * 60)
        for i, feature in enumerate(data['features'], 1):
            lines.append(f"{i}. {feature}")
    
    # 使用示例
    if data.get('examples'):
        lines.append(f"\n💻 使用示例")
        lines.append("─" * 60)
        for i, example in enumerate(data['examples'][:5], 1):  # 最多显示5个
            if '\n' in example:
                lines.append(f"\n示例 {i}:")
                lines.append(example)
            else:
                lines.append(f"{i}. {example}")
    
    # 配置选项
    if data.get('config'):
        lines.append(f"\n⚙️ 配置选项")
        lines.append("─" * 60)
        for config in data['config']:
            lines.append(f"• {config}")
    
    # 文件结构
    if data.get('file_structure'):
        lines.append(f"\n📁 文件结构 ({len(data['file_structure'])}项)")
        lines.append("─" * 60)
        for item in data['file_structure']:
            lines.append(f"  {item}")
    
    # 注意事项
    if data.get('warnings'):
        lines.append(f"\n⚠️ 注意事项")
        lines.append("─" * 60)
        for warning in data['warnings']:
            lines.append(f"• {warning}")
    
    # 最佳实践
    if data.get('best_practices'):
        lines.append(f"\n💡 最佳实践")
        lines.append("─" * 60)
        for i, tip in enumerate(data['best_practices'][:5], 1):
            lines.append(f"{i}. {tip}")
    
    lines.append("\n" + "═" * 60)
    return '\n'.join(lines)

def generate_markdown_report(data):
    """生成 Markdown 格式报告."""
    lines = []
    name = data.get('name', 'Unknown Skill')
    
    lines.append(f"# 🔍 {name} 使用指南")
    lines.append("")
    
    # 基本信息
    lines.append("## 📋 基本信息")
    lines.append("")
    lines.append(f"**名称**: {name}")
    if data.get('description'):
        lines.append(f"**描述**: {data['description']}")
    lines.append("")
    
    # 核心功能
    if data.get('features'):
        lines.append(f"## 🎯 核心功能")
        lines.append("")
        for feature in data['features']:
            lines.append(f"- {feature}")
        lines.append("")
    
    # 使用示例
    if data.get('examples'):
        lines.append(f"## 💻 使用示例")
        lines.append("")
        for i, example in enumerate(data['examples'], 1):
            lines.append(f"### 示例 {i}")
            lines.append("```")
            lines.append(example)
            lines.append("```")
            lines.append("")
    
    # 配置选项
    if data.get('config'):
        lines.append(f"## ⚙️ 配置选项")
        lines.append("")
        for config in data['config']:
            lines.append(f"- {config}")
        lines.append("")
    
    # 文件结构
    if data.get('file_structure'):
        lines.append(f"## 📁 文件结构")
        lines.append("")
        for item in data['file_structure']:
            lines.append(f"- {item}")
        lines.append("")
    
    # 注意事项
    if data.get('warnings'):
        lines.append(f"## ⚠️ 注意事项")
        lines.append("")
        for warning in data['warnings']:
            lines.append(f"- {warning}")
        lines.append("")
    
    # 最佳实践
    if data.get('best_practices'):
        lines.append(f"## 💡 最佳实践")
        lines.append("")
        for tip in data['best_practices']:
            lines.append(f"- {tip}")
        lines.append("")
    
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='分析 OpenClaw 技能并生成使用指南')
    parser.add_argument('skill_path', help='SKILL.md 文件路径或技能目录')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'markdown'], default='text',
                        help='输出格式 (默认: text)')
    parser.add_argument('--examples-only', '-e', action='store_true',
                        help='只显示使用示例')
    parser.add_argument('--output', '-o', help='输出到文件')
    
    args = parser.parse_args()
    
    # 确定 SKILL.md 路径
    skill_path = args.skill_path
    if os.path.isdir(skill_path):
        skill_path = os.path.join(skill_path, 'SKILL.md')
    
    if not os.path.exists(skill_path):
        print(f"❌ 错误: 找不到文件 {skill_path}")
        sys.exit(1)
    
    # 解析技能
    data = parse_skill_md(skill_path)
    if not data:
        print(f"❌ 错误: 无法解析 {skill_path}")
        sys.exit(1)
    
    # 如果只显示示例
    if args.examples_only:
        print(f"\n💻 {data['name']} 使用示例:\n")
        for i, example in enumerate(data['examples'], 1):
            print(f"示例 {i}:")
            print("─" * 40)
            print(example)
            print()
        return
    
    # 生成报告
    report = generate_report(data, args.format)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到: {args.output}")
    else:
        print(report)

if __name__ == '__main__':
    main()
