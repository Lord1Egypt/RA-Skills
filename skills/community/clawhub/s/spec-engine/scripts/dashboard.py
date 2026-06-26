#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spec Engine v3 - Web Dashboard Generator
生成可视化 HTML 仪表盘，展示所有 spec 的状态和评分。
纯 Python 标准库实现，零第三方依赖。
"""

import os
import re
import sys
import json
import glob
import argparse
from datetime import datetime
from pathlib import Path


def read_file_safe(filepath):
    """安全读取文件，兼容 UTF-8 BOM"""
    for enc in ['utf-8-sig', 'utf-8', 'gbk', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    return None


def is_spec_file(content):
    """判断是否为 spec 文件"""
    patterns = [r'#\s+项目名称', r'##\s+\d+\.\s+项目背景', r'##\s+目标', r'##\s+验收标准']
    return sum(1 for p in patterns if re.search(p, content)) >= 2


def extract_project_name(content):
    """提取项目名称"""
    m = re.search(r'#\s+项目名称[：:]\s*(.+)', content)
    if m:
        return m.group(1).strip()
    m = re.search(r'#\s+(.+)', content)
    if m:
        return m.group(1).strip()
    return "未命名"


def extract_sections(content):
    """提取所有 section"""
    sections = {}
    current = None
    lines = content.split('\n')
    for line in lines:
        m = re.match(r'^##\s+(\S+.*)', line)
        if m:
            current = m.group(1).strip()
            sections[current] = ''
        elif current:
            sections[current] += line + '\n'
    return sections


def score_spec(content):
    """评分 spec 完整性 (0-100, grade, issues)"""
    score = 100
    issues = []
    sections = extract_sections(content)
    
    required = {
        '项目名称': 20,
        '目标': 15,
        '验收标准': 15,
        '时间规划': 10,
        '技术方案': 10,
    }
    recommended = {
        '项目背景': 8,
        '风险评估': 7,
        '文件结构': 5,
        '依赖项': 5,
        '功能列表': 5,
    }
    
    for section, penalty in required.items():
        if section not in sections:
            score -= penalty
            issues.append(f"缺少必要 section: {section}")
        elif len(sections[section].strip()) < 20:
            score -= penalty // 2
            issues.append(f"{section} 内容过少")
    
    for section, penalty in recommended.items():
        if section not in sections:
            score -= penalty
            issues.append(f"缺少推荐 section: {section}")
        elif 'TODO' in sections.get(section, '') or '待定' in sections.get(section, ''):
            score -= penalty // 2
            issues.append(f"{section} 为占位内容")
    
    score = max(0, score)
    grade = 'A' if score >= 85 else 'B' if score >= 70 else 'C' if score >= 50 else 'D'
    return score, grade, issues


def extract_tech_stack(content):
    """提取技术栈"""
    techs = []
    tech_patterns = [
        r'Python', r'Node\.?js', r'Go', r'Java', r'Rust',
        r'React', r'Vue', r'Flask', r'Django', r'FastAPI',
        r'SQLite', r'MySQL', r'PostgreSQL', r'MongoDB',
        r'Docker', r'K8s', r'Redis', r'飞书|Feishu', r'Bitable',
    ]
    for p in tech_patterns:
        if re.search(p, content, re.IGNORECASE):
            techs.append(p.replace(r'\.', '.').replace(r'\?', '?'))
    return techs


def get_file_info(filepath):
    """获取文件信息"""
    stat = os.stat(filepath)
    modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
    return {
        'path': filepath,
        'name': os.path.basename(filepath),
        'size': stat.st_size,
        'modified': modified,
    }


def scan_specs(directory):
    """扫描目录下的所有 spec 文件"""
    specs = []
    for root, dirs, files in os.walk(directory):
        # 跳过隐藏目录和 __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for f in files:
            if not f.endswith('.md'):
                continue
            filepath = os.path.join(root, f)
            content = read_file_safe(filepath)
            if content and is_spec_file(content):
                score, grade, issues = score_spec(content)
                sections = extract_sections(content)
                techs = extract_tech_stack(content)
                info = get_file_info(filepath)
                specs.append({
                    'project_name': extract_project_name(content),
                    'score': score,
                    'grade': grade,
                    'issues': issues,
                    'sections': list(sections.keys()),
                    'section_count': len(sections),
                    'tech_stack': techs,
                    'file_info': info,
                })
    return sorted(specs, key=lambda s: s['score'], reverse=True)


def generate_html(specs, directory):
    """生成 HTML 仪表盘"""
    total = len(specs)
    avg_score = sum(s['score'] for s in specs) / total if total else 0
    grade_dist = {g: sum(1 for s in specs if s['grade'] == g) for g in ['A', 'B', 'C', 'D']}
    
    # 技术栈统计
    tech_counter = {}
    for s in specs:
        for t in s['tech_stack']:
            tech_counter[t] = tech_counter.get(t, 0) + 1
    tech_sorted = sorted(tech_counter.items(), key=lambda x: -x[1])
    
    grade_colors = {'A': '#22c55e', 'B': '#3b82f6', 'C': '#eab308', 'D': '#ef4444'}
    
    # 生成表格行
    table_rows = ''
    for i, s in enumerate(specs):
        gc = grade_colors.get(s['grade'], '#888')
        tech_badges = ' '.join(f'<span class="badge">{t}</span>' for t in s['tech_stack'][:3])
        issues_text = ', '.join(s['issues'][:3]) if s['issues'] else '<span class="ok">✓ 完整</span>'
        table_rows += f'''
        <tr>
            <td>{i+1}</td>
            <td><strong>{s['project_name']}</strong></td>
            <td><span class="grade" style="background:{gc}">{s['grade']}</span> {s['score']}分</td>
            <td>{s['section_count']}</td>
            <td>{tech_badges or '-'}</td>
            <td class="issues">{issues_text}</td>
            <td>{s['file_info']['modified']}</td>
        </tr>'''
    
    # 技术栈分布条
    tech_bars = ''
    if tech_sorted:
        max_count = tech_sorted[0][1]
        for tech, count in tech_sorted[:8]:
            pct = count / max_count * 100
            tech_bars += f'<div class="tech-bar"><span class="tech-name">{tech}</span><div class="bar" style="width:{pct}%"></div><span class="tech-count">{count}</span></div>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Spec Engine 仪表盘</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, "Segoe UI", sans-serif; background: #0f172a; color: #e2e8f0; padding: 24px; }}
.container {{ max-width: 1200px; margin: 0 auto; }}
h1 {{ font-size: 28px; margin-bottom: 8px; color: #f8fafc; }}
.subtitle {{ color: #94a3b8; margin-bottom: 24px; }}
.cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.card {{ background: #1e293b; border-radius: 12px; padding: 20px; text-align: center; }}
.card .number {{ font-size: 36px; font-weight: 700; }}
.card .label {{ color: #94a3b8; font-size: 14px; margin-top: 4px; }}
.grade-dist {{ display: flex; gap: 12px; justify-content: center; margin-top: 12px; }}
.grade-item {{ display: flex; align-items: center; gap: 4px; }}
.grade-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 12px; overflow: hidden; }}
th {{ background: #334155; padding: 12px 16px; text-align: left; font-weight: 600; font-size: 13px; color: #94a3b8; text-transform: uppercase; }}
td {{ padding: 12px 16px; border-bottom: 1px solid #334155; font-size: 14px; }}
tr:nth-child(even) {{ background: #1a2536; }}
.grade {{ display: inline-block; padding: 2px 10px; border-radius: 6px; color: white; font-weight: 700; font-size: 13px; }}
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; background: #334155; font-size: 12px; margin: 1px; }}
.ok {{ color: #22c55e; }}
.issues {{ font-size: 13px; color: #f59e0b; max-width: 250px; }}
.section {{ background: #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 24px; }}
.section h2 {{ font-size: 18px; margin-bottom: 16px; color: #f8fafc; }}
.tech-bar {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
.tech-name {{ width: 100px; font-size: 13px; text-align: right; }}
.bar {{ height: 20px; background: linear-gradient(90deg, #3b82f6, #8b5cf6); border-radius: 4px; transition: width 0.5s; }}
.tech-count {{ font-size: 12px; color: #94a3b8; }}
.footer {{ text-align: center; color: #64748b; font-size: 12px; margin-top: 24px; }}
</style>
</head>
<body>
<div class="container">
    <h1>📊 Spec Engine 仪表盘</h1>
    <p class="subtitle">扫描目录：{directory} · 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    
    <div class="cards">
        <div class="card"><div class="number">{total}</div><div class="label">Spec 总数</div></div>
        <div class="card"><div class="number">{avg_score:.0f}</div><div class="label">平均评分</div></div>
        <div class="card">
            <div class="number">{grade_dist['A']}</div><div class="label">A 级 Spec</div>
            <div class="grade-dist">
                <div class="grade-item"><div class="grade-dot" style="background:#22c55e"></div>A:{grade_dist['A']}</div>
                <div class="grade-item"><div class="grade-dot" style="background:#3b82f6"></div>B:{grade_dist['B']}</div>
                <div class="grade-item"><div class="grade-dot" style="background:#eab308"></div>C:{grade_dist['C']}</div>
                <div class="grade-item"><div class="grade-dot" style="background:#ef4444"></div>D:{grade_dist['D']}</div>
            </div>
        </div>
        <div class="card"><div class="number">{len(tech_counter)}</div><div class="label">涉及技术栈</div></div>
    </div>
    
    <div class="section">
        <h2>📋 Spec 列表</h2>
        <table>
            <thead><tr><th>#</th><th>项目名称</th><th>评分</th><th>Section</th><th>技术栈</th><th>问题</th><th>修改时间</th></tr></thead>
            <tbody>{table_rows}</tbody>
        </table>
    </div>
    
    {'<div class="section"><h2>🔧 技术栈分布</h2>' + tech_bars + '</div>' if tech_bars else ''}
    
    <div class="footer">Spec Engine v3.0 · CTO Agent · {datetime.now().year}</div>
</div>
</body>
</html>'''
    return html


def main():
    parser = argparse.ArgumentParser(description='Spec Engine - Web Dashboard Generator')
    parser.add_argument('-d', '--dir', default='.', help='扫描目录 (默认: 当前目录)')
    parser.add_argument('-o', '--output', default='dashboard.html', help='输出文件 (默认: dashboard.html)')
    parser.add_argument('--open', action='store_true', help='生成后打开浏览器')
    args = parser.parse_args()
    
    directory = os.path.abspath(args.dir)
    if not os.path.isdir(directory):
        print(f"[ERROR] 目录不存在: {directory}", file=sys.stderr)
        sys.exit(1)
    
    print(f"扫描目录: {directory}")
    specs = scan_specs(directory)
    
    if not specs:
        print("[WARN] 未找到 spec 文件")
    
    print(f"找到 {len(specs)} 个 spec 文件")
    for s in specs:
        print(f"  - {s['project_name']}: {s['score']}分/{s['grade']}级")
    
    html = generate_html(specs, directory)
    
    output_path = os.path.abspath(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] 仪表盘已生成: {output_path}")
    
    if args.open:
        import webbrowser
        webbrowser.open(f'file:///{output_path}')


if __name__ == '__main__':
    main()
