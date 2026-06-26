# -*- coding: utf-8 -*-
"""
HTML 导出模块
生成可交互的 Web 界面，支持筛选、搜索、排序
"""
import os
import json
from typing import List, Dict, Any
from utils.config import OUTPUT_DIR, CATEGORY_ORDER, STATUS_ICONS
from classifier.category_map import get_category
from utils.translator import translate_description


def generate_html(skills: List[Dict[str, Any]], title: str,
                  is_activated: bool = True) -> str:
    """
    生成交互式 HTML 页面

    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能

    Returns:
        HTML 字符串
    """
    # 构建分类选项
    category_options = ['<option value="">全部分类</option>']
    for cat in CATEGORY_ORDER:
        category_options.append(f'<option value="{cat}">{cat}</option>')

    # 构建技能数据 JSON - 确保每个技能都有分类字段
    skills_data = []
    for skill in skills:
        cat = get_category(skill['name'])
        skills_data.append({
            'name': skill['name'],
            'status': skill.get('status', 'unknown'),
            'version': skill.get('version', ''),
            'description': translate_description(skill.get('description', '')),
            'big_category': cat[0],
            'sub_category': cat[1]
        })

    skills_json = json.dumps(skills_data, ensure_ascii=False)
    status_icons_json = json.dumps(STATUS_ICONS, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - OpenClaw 技能列表</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .toolbar {{ padding: 20px; background: #f8f9fa; border-bottom: 1px solid #eee; display: flex; gap: 15px; flex-wrap: wrap; }}
        .toolbar input, .toolbar select {{ padding: 10px 15px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; min-width: 200px; }}
        .toolbar input:focus, .toolbar select:focus {{ outline: none; border-color: #667eea; }}
        .stats {{ display: flex; gap: 20px; padding: 20px; background: #f8f9fa; flex-wrap: wrap; }}
        .stat-card {{ background: white; padding: 15px 25px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .stat-card .value {{ font-size: 28px; font-weight: bold; color: #333; }}
        .stat-card .label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #f8f9fa; padding: 15px; text-align: left; font-weight: 600; color: #333; border-bottom: 2px solid #eee; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9fa; }}
        .status-icon {{ font-size: 18px; }}
        .skill-name {{ font-weight: 600; color: #333; }}
        .skill-version {{ color: #666; font-size: 12px; background: #e9ecef; padding: 2px 8px; border-radius: 4px; }}
        .category-tag {{ font-size: 12px; background: #e7f3ff; color: #0066cc; padding: 3px 8px; border-radius: 4px; }}
        .skill-desc {{ max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .hidden {{ display: none; }}
        .empty {{ text-align: center; padding: 50px; color: #999; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; }}
        .badge-ready {{ background: #d4edda; color: #155724; }}
        .badge-needsetup {{ background: #fff3cd; color: #856404; }}
        .badge-disabled {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📦 {title}</h1>
            <p>共 {len(skills)} 个{'已' if is_activated else '未'}激活技能 | OpenClaw Skill Manager</p>
        </div>

        <div class="toolbar">
            <input type="text" id="searchInput" placeholder="🔍 搜索技能名称或描述...">
            <select id="categoryFilter">
                {''.join(category_options)}
            </select>
            <select id="statusFilter">
                <option value="">全部状态</option>
                <option value="ready">✅ 已就绪</option>
                <option value="needsetup">⚠️ 需配置</option>
                <option value="disabled">❌ 已禁用</option>
            </select>
        </div>

        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="value" id="totalCount">{len(skills)}</div>
                <div class="label">总计</div>
            </div>
            <div class="stat-card">
                <div class="value" id="readyCount">{sum(1 for s in skills if s.get('status') == 'ready')}</div>
                <div class="label">已就绪</div>
            </div>
            <div class="stat-card">
                <div class="value" id="filterCount">0</div>
                <div class="label">筛选结果</div>
            </div>
        </div>

        <table id="skillTable">
            <thead>
                <tr>
                    <th style="width: 60px;">状态</th>
                    <th>技能名称</th>
                    <th style="width: 120px;">版本</th>
                    <th>分类</th>
                    <th>描述</th>
                </tr>
            </thead>
            <tbody id="skillTableBody">
            </tbody>
        </table>

        <div id="emptyState" class="empty hidden">
            😔 没有找到匹配的技能
        </div>
    </div>

    <script>
        const STATUS_ICONS = {status_icons_json};
        const skills = {skills_json};

        function renderSkills(filtered = null) {{
            const tbody = document.getElementById('skillTableBody');
            const emptyState = document.getElementById('emptyState');
            const table = document.getElementById('skillTable');
            const data = filtered || skills;

            tbody.innerHTML = '';

            if (data.length === 0) {{
                emptyState.classList.remove('hidden');
                table.classList.add('hidden');
            }} else {{
                emptyState.classList.add('hidden');
                table.classList.remove('hidden');

                data.forEach(skill => {{
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><span class="status-icon">${{STATUS_ICONS[skill.status] || '❓'}}</span></td>
                        <td><span class="skill-name">${{skill.name}}</span></td>
                        <td>${{skill.version ? `<span class="skill-version">v${{skill.version}}</span>` : '-'}}</td>
                        <td><span class="category-tag">${{skill.big_category}}</span></td>
                        <td class="skill-desc">${{skill.description || '-'}}</td>
                    `;
                    tbody.appendChild(row);
                }});
            }}

            document.getElementById('filterCount').textContent = data.length;
        }}

        function filterSkills() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const categoryFilter = document.getElementById('categoryFilter').value;
            const statusFilter = document.getElementById('statusFilter').value;

            const filtered = skills.filter(skill => {{
                const matchSearch = !searchTerm ||
                    skill.name.toLowerCase().includes(searchTerm) ||
                    (skill.description && skill.description.toLowerCase().includes(searchTerm));
                const matchCategory = !categoryFilter || skill.big_category === categoryFilter;
                const matchStatus = !statusFilter || skill.status === statusFilter;

                return matchSearch && matchCategory && matchStatus;
            }});

            renderSkills(filtered);
        }}

        document.getElementById('searchInput').addEventListener('input', filterSkills);
        document.getElementById('categoryFilter').addEventListener('change', filterSkills);
        document.getElementById('statusFilter').addEventListener('change', filterSkills);

        // 初始渲染
        renderSkills();
    </script>
</body>
</html>'''

    return html


def export_html(skills: List[Dict[str, Any]], title: str,
                is_activated: bool = True, output_path: str = None) -> str:
    """
    导出 HTML 文件

    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能
        output_path: 输出路径（默认自动生成）

    Returns:
        输出文件路径
    """
    content = generate_html(skills, title, is_activated)

    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"{title}.html")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path
