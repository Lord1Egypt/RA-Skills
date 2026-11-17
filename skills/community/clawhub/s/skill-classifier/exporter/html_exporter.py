# -*- coding: utf-8 -*-
"""
HTML 导出模块
生成可交互的 Web 界面：搜索、筛选、表头排序、缺失依赖关系图
"""
import html as html_lib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from utils.config import OUTPUT_DIR, CATEGORY_ORDER, STATUS_ICONS
from classifier.category_map import get_category


def _source_short(skill: Dict[str, Any]) -> str:
    return str(skill.get('source') or '').replace('openclaw-', '')


def build_cols(usage: Optional[Dict]) -> List[Dict[str, str]]:
    """输出列定义（label 用于表头，key 对应数据字段；sort 为空表示不可排序）"""
    cols = [
        {'key': 'status', 'label': '状态', 'sort': ''},
        {'key': 'name', 'label': '技能名称', 'sort': 'name'},
        {'key': 'version', 'label': '版本', 'sort': 'version'},
        {'key': 'source', 'label': '来源', 'sort': 'source'},
    ]
    if usage is not None:
        cols.append({'key': 'calls', 'label': '调用量', 'sort': 'calls'})
    cols.append({'key': 'category', 'label': '分类', 'sort': 'big_category'})
    cols.append({'key': 'description', 'label': '描述', 'sort': ''})
    return cols


def _deps_svg(edges: List[Dict[str, str]]) -> str:
    """缺失依赖二部图：左列技能，右列缺失项（kind:dep），连线为边"""
    if not edges:
        return ''
    left, right, pairs = [], [], []
    for e in edges:
        if e['skill'] not in left:
            left.append(e['skill'])
        dkey = f"{e['kind']}:{e['dep']}"
        if dkey not in right:
            right.append(dkey)
        pairs.append((e['skill'], dkey, e['kind']))
    row_h, margin, name_w = 26, 16, 300
    width = name_w + 240 + 260
    height = max(len(left), len(right)) * row_h + margin * 2 + 10
    left_y = {n: margin + i * row_h + 16 for i, n in enumerate(left)}
    right_y = {n: margin + i * row_h + 16 for i, n in enumerate(right)}
    parts = [f'<svg viewBox="0 0 {width} {height}" style="width:100%;max-width:860px;'
             f'background:#fff;border:1px solid #eee;border-radius:8px;margin:10px 0;'
             f'font-size:12px">']
    esc = html_lib.escape
    for skill, dkey, kind in pairs:
        x1, y1 = margin + name_w - 10, left_y[skill] - 4
        x2, y2 = margin + name_w + 220, right_y[dkey] - 4
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                     f'stroke="#c3cad9" stroke-width="1"/>')
    for n, y in left_y.items():
        parts.append(f'<text x="{margin}" y="{y}" fill="#333">{esc(n)}</text>')
    for n, y in right_y.items():
        parts.append(f'<text x="{margin + name_w + 230}" y="{y}" fill="#555">{esc(n)}</text>')
    parts.append('</svg>')
    return ''.join(parts)


def generate_html(skills: List[Dict[str, Any]], title: str,
                  is_activated: bool = True, usage: Optional[Dict] = None,
                  deps_edges: Optional[List[Dict[str, str]]] = None) -> str:
    """
    生成交互式 HTML 页面

    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能
        usage: 使用统计（None 则不含调用量列）
        deps_edges: 缺失依赖边（None 则不含依赖关系图）

    Returns:
        HTML 字符串
    """
    cols = build_cols(usage)

    # 构建分类选项
    category_options = ['<option value="">全部分类</option>']
    for cat in CATEGORY_ORDER:
        category_options.append(f'<option value="{cat}">{cat}</option>')

    skills_data = []
    for skill in skills:
        cat = get_category(skill['name'])
        # 仅放行 http(s) 主页链接，阻断 javascript: 等危险 scheme（SkillSpector 整改）
        homepage = skill.get('homepage') or ''
        if not homepage.startswith(('http://', 'https://')):
            homepage = ''
        item = {
            'name': skill['name'],
            'status': skill.get('status', 'unknown'),
            'version': skill.get('version', ''),
            'source': _source_short(skill),
            'emoji': skill.get('emoji') or '',
            'homepage': homepage,
            'description': skill.get('description', ''),
            'big_category': cat[0],
            'sub_category': cat[1],
        }
        if usage is not None:
            calls = (usage.get(skill['name']) or {}).get('calls')
            item['calls'] = calls if calls is not None else ''
        skills_data.append(item)

    status_icons_json = json.dumps(STATUS_ICONS, ensure_ascii=False).replace('</', '<\\/')
    skills_json = json.dumps(skills_data, ensure_ascii=False).replace('</', '<\\/')
    cols_json = json.dumps(cols, ensure_ascii=False)

    deps_section = ''
    if deps_edges:
        deps_section = ('<div style="padding: 20px;">'
                        '<h2 style="font-size:18px;margin-bottom:6px">🔗 缺失依赖关系</h2>'
                        f'<p style="color:#666;font-size:13px">共 {len(deps_edges)} 条缺失依赖边</p>'
                        + _deps_svg(deps_edges) + '</div>')

    th_html = ''.join(
        f'<th data-sort="{c["sort"]}">{c["label"]}</th>' if c['sort']
        else f'<th>{c["label"]}</th>' for c in cols)

    page = f'''<!DOCTYPE html>
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
        th {{ background: #f8f9fa; padding: 15px; text-align: left; font-weight: 600; color: #333; border-bottom: 2px solid #eee; user-select: none; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9fa; }}
        .status-icon {{ font-size: 18px; }}
        .skill-name {{ font-weight: 600; color: #333; }}
        .skill-version {{ color: #666; font-size: 12px; background: #e9ecef; padding: 2px 8px; border-radius: 4px; }}
        .category-tag {{ font-size: 12px; background: #e7f3ff; color: #0066cc; padding: 3px 8px; border-radius: 4px; }}
        .skill-desc {{ max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .hidden {{ display: none; }}
        .empty {{ text-align: center; padding: 50px; color: #999; }}
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
        {deps_section}
        <table id="skillTable">
            <thead>
                <tr>{th_html}</tr>
            </thead>
            <tbody id="skillTableBody">
            </tbody>
        </table>

        <div id="emptyState" class="empty hidden">
            😔 没有找到匹配的技能
        </div>
    </div>
'''

    script = '''    <script>
        const STATUS_ICONS = __STATUS__;
        const skills = __SKILLS__;
        const COLS = __COLS__;
        let currentData = skills.slice();

        function esc(s) {
            return String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
        }

        function cellHtml(c, skill) {
            if (c.key === 'status') {
                return '<td><span class="status-icon">' + esc(STATUS_ICONS[skill.status] || '❓') + '</span></td>';
            }
            if (c.key === 'name') {
                const label = esc((skill.emoji ? skill.emoji + ' ' : '') + skill.name);
                const inner = skill.homepage
                    ? '<a href="' + esc(skill.homepage) + '" target="_blank" rel="noopener noreferrer" style="color:#0066cc;text-decoration:none">' + label + '</a>'
                    : label;
                return '<td><span class="skill-name">' + inner + '</span></td>';
            }
            if (c.key === 'version') {
                return '<td>' + (skill.version ? '<span class="skill-version">v' + esc(skill.version) + '</span>' : '-') + '</td>';
            }
            if (c.key === 'category') {
                return '<td><span class="category-tag">' + esc(skill.big_category) + '</span></td>';
            }
            const v = skill[c.key];
            return '<td>' + ((v === null || v === undefined || v === '') ? '-' : esc(v)) + '</td>';
        }

        function renderSkills(data) {
            const tbody = document.getElementById('skillTableBody');
            const emptyState = document.getElementById('emptyState');
            const table = document.getElementById('skillTable');
            tbody.innerHTML = '';
            if (data.length === 0) {
                emptyState.classList.remove('hidden');
                table.classList.add('hidden');
            } else {
                emptyState.classList.add('hidden');
                table.classList.remove('hidden');
                data.forEach(skill => {
                    const row = document.createElement('tr');
                    row.innerHTML = COLS.map(c => cellHtml(c, skill)).join('');
                    tbody.appendChild(row);
                });
            }
            document.getElementById('filterCount').textContent = data.length;
        }

        function filterSkills() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const categoryFilter = document.getElementById('categoryFilter').value;
            const statusFilter = document.getElementById('statusFilter').value;
            currentData = skills.filter(skill => {
                const matchSearch = !searchTerm ||
                    skill.name.toLowerCase().includes(searchTerm) ||
                    (skill.description && skill.description.toLowerCase().includes(searchTerm));
                const matchCategory = !categoryFilter || skill.big_category === categoryFilter;
                const matchStatus = !statusFilter || skill.status === statusFilter;
                return matchSearch && matchCategory && matchStatus;
            });
            renderSkills(currentData);
        }

        let sortKey = null, sortAsc = true;
        function sortBy(key) {
            if (sortKey === key) { sortAsc = !sortAsc; } else { sortKey = key; sortAsc = true; }
            document.querySelectorAll('th[data-sort]').forEach(th => {
                const dir = th.dataset.sort === key ? (sortAsc ? ' ▲' : ' ▼') : '';
                th.textContent = th.dataset.label + dir;
            });
            const sorted = currentData.slice().sort((a, b) => {
                let va = a[key], vb = b[key];
                if (typeof va === 'number' || typeof vb === 'number') {
                    va = Number(va) || 0; vb = Number(vb) || 0;
                    return sortAsc ? va - vb : vb - va;
                }
                va = String(va == null ? '' : va).toLowerCase();
                vb = String(vb == null ? '' : vb).toLowerCase();
                return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
            });
            renderSkills(sorted);
        }

        document.getElementById('searchInput').addEventListener('input', filterSkills);
        document.getElementById('categoryFilter').addEventListener('change', filterSkills);
        document.getElementById('statusFilter').addEventListener('change', filterSkills);
        document.querySelectorAll('th[data-sort]').forEach(th => {
            th.dataset.label = th.textContent;
            th.addEventListener('click', () => sortBy(th.dataset.sort));
            th.style.cursor = 'pointer';
        });

        renderSkills(currentData);
    </script>
</body>
</html>'''

    page = page + script
    return (page
            .replace('__STATUS__', status_icons_json)
            .replace('__SKILLS__', skills_json)
            .replace('__COLS__', cols_json))


def export_html(skills: List[Dict[str, Any]], title: str,
                is_activated: bool = True, output_path: str = None,
                usage: Optional[Dict] = None,
                deps_edges: Optional[List[Dict[str, str]]] = None) -> str:
    """
    导出 HTML 文件

    Args:
        skills: 技能列表
        title: 标题
        is_activated: 是否为已激活技能
        output_path: 输出路径（默认自动生成）
        usage: 使用统计（None 则不含调用量列）
        deps_edges: 缺失依赖边（None 则不含依赖关系图）

    Returns:
        输出文件路径
    """
    content = generate_html(skills, title, is_activated, usage=usage, deps_edges=deps_edges)

    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"{title}.html")

    Path(output_path).write_text(content, encoding='utf-8')

    return output_path
