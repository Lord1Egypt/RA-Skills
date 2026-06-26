#!/usr/bin/env python3
"""
分析所有已安装的技能并生成索引
"""
import os
import sys
import json
import argparse
from analyze_skill import parse_skill_md, generate_markdown_report

def find_all_skills(skills_dir):
    """查找所有已安装的技能."""
    skills = []
    if not os.path.exists(skills_dir):
        return skills
    
    for item in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, item)
        if os.path.isdir(skill_path):
            skill_md = os.path.join(skill_path, 'SKILL.md')
            if os.path.exists(skill_md):
                skills.append({
                    'name': item,
                    'path': skill_path,
                    'md_path': skill_md
                })
    
    return skills

def generate_index(skills, output_file=None):
    """生成技能索引."""
    lines = []
    lines.append("# 🔍 OpenClaw 技能索引")
    lines.append("")
    lines.append(f"共发现 **{len(skills)}** 个技能")
    lines.append("")
    lines.append("| 技能名称 | 描述 | 核心功能 | 状态 |")
    lines.append("|----------|------|----------|------|")
    
    for skill in sorted(skills, key=lambda x: x['name']):
        data = parse_skill_md(skill['md_path'])
        if data:
            name = data.get('name', skill['name'])
            desc = data.get('description', '')[:50] + '...' if len(data.get('description', '')) > 50 else data.get('description', '-')
            features = len(data.get('features', []))
            status = "✅" if features > 0 else "⚠️"
            
            # 创建链接
            rel_path = os.path.relpath(skill['path'], os.path.expanduser('~/.openclaw/workspace/skills'))
            lines.append(f"| [{name}](./{rel_path}/SKILL.md) | {desc} | {features}项 | {status} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 快速分类")
    lines.append("")
    
    # 按类别分组
    categories = {
        '开发工具': [],
        '数据处理': [],
        '内容创作': [],
        '系统管理': [],
        '其他': []
    }
    
    for skill in skills:
        data = parse_skill_md(skill['md_path'])
        if data:
            desc = data.get('description', '').lower()
            name = data.get('name', skill['name']).lower()
            
            if any(k in desc or k in name for k in ['code', 'git', 'dev', 'program', '开发', '代码']):
                categories['开发工具'].append(data.get('name', skill['name']))
            elif any(k in desc or k in name for k in ['data', 'file', 'parse', '数据', '文件', '分析']):
                categories['数据处理'].append(data.get('name', skill['name']))
            elif any(k in desc or k in name for k in ['write', 'content', 'create', '创作', '写作', '生成']):
                categories['内容创作'].append(data.get('name', skill['name']))
            elif any(k in desc or k in name for k in ['system', 'manage', 'monitor', '系统', '管理', '监控']):
                categories['系统管理'].append(data.get('name', skill['name']))
            else:
                categories['其他'].append(data.get('name', skill['name']))
    
    for category, items in categories.items():
        if items:
            lines.append(f"### {category}")
            lines.append("")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")
    
    content = '\n'.join(lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 技能索引已保存到: {output_file}")
    
    return content

def main():
    parser = argparse.ArgumentParser(description='分析所有已安装的技能')
    parser.add_argument('--skills-dir', '-d', default='~/.openclaw/workspace/skills',
                        help='技能目录路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['markdown', 'json'], default='markdown',
                        help='输出格式')
    
    args = parser.parse_args()
    
    skills_dir = os.path.expanduser(args.skills_dir)
    
    print(f"🔍 正在扫描技能目录: {skills_dir}")
    skills = find_all_skills(skills_dir)
    print(f"✅ 发现 {len(skills)} 个技能")
    
    if args.format == 'json':
        # 输出 JSON 格式
        all_data = []
        for skill in skills:
            data = parse_skill_md(skill['md_path'])
            if data:
                data['path'] = skill['path']
                all_data.append(data)
        
        output = json.dumps(all_data, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✅ 报告已保存到: {args.output}")
        else:
            print(output)
    else:
        # 输出 Markdown 格式
        generate_index(skills, args.output)

if __name__ == '__main__':
    main()
