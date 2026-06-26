#!/usr/bin/env python3
from __future__ import annotations

import re
from typing import Any, Optional


def _format_value(value, field: str = '') -> str:
    if value in (None, ''):
        return '-'
    if field in {'fans', 'avgViews'}:
        try:
            return f"{int(float(value)):,}"
        except Exception:
            return str(value)
    if field in {'avgEngagementRate'}:
        try:
            num = float(value)
            if num <= 1:
                num *= 100
            return f"{num:.2f}%"
        except Exception:
            return str(value)
    if field in {'wotohubScore', 'gmv30d', 'matchScore'}:
        try:
            num = float(value)
            return f"{num:,.2f}" if not num.is_integer() else f"{int(num):,}"
        except Exception:
            return str(value)
    if field in {'tags'} and isinstance(value, list):
        return ' / '.join(str(v).strip() for v in value if str(v).strip()) or '-'
    return str(value)


def render_markdown_table(rows: list[dict], columns: Optional[list[str]]= None) -> str:
    if not rows:
        return '暂无结果'
    columns = columns or [
        'channelName', 'fans', 'avgViews', 'avgEngagementRate', 'platform',
        'gmv30d', 'originalLink', 'tags', 'wotohubLink', 'advantages'
    ]
    headers = {
        'rank': '排名',
        'channelName': '频道名',
        'fans': '粉丝数',
        'avgViews': '平均观看量',
        'avgEngagementRate': '平均互动率',
        'platform': '平台',
        'wotohubCategory': 'WotoHub分类',
        'wotohubScore': 'WotoHub评分',
        'country': '国家',
        'gmv30d': '近30天GMV',
        'originalLink': '博主主页',
        'wotohubLink': 'WotoHub分析',
        'tags': '标签',
        'advantages': '优势',
        'besId': 'besId',
        'matchScore': '匹配分',
        'matchTier': '匹配等级',
    }
    lines = [
        '| ' + ' | '.join(headers.get(col, col) for col in columns) + ' |',
        '| ' + ' | '.join('---' for _ in columns) + ' |',
    ]
    for row in rows:
        values = []
        for col in columns:
            cell = _format_value(row.get(col), col).replace('\n', ' ').replace('|', '\\|')
            values.append(cell)
        lines.append('| ' + ' | '.join(values) + ' |')
    return '\n'.join(lines)


def render_plaintext_table(rows: list[dict], columns: Optional[list[str]]= None) -> str:
    if not rows:
        return '暂无结果'
    columns = columns or [
        'channelName', 'fans', 'avgViews', 'avgEngagementRate', 'platform',
        'gmv30d', 'originalLink', 'tags', 'wotohubLink', 'advantages'
    ]
    headers = {
        'rank': '排名',
        'channelName': '频道名',
        'fans': '粉丝数',
        'avgViews': '平均观看量',
        'avgEngagementRate': '平均互动率',
        'platform': '平台',
        'wotohubCategory': 'WotoHub分类',
        'wotohubScore': 'WotoHub评分',
        'country': '国家',
        'gmv30d': '近30天GMV',
        'originalLink': '博主主页',
        'wotohubLink': 'WotoHub分析',
        'tags': '标签',
        'advantages': '优势',
        'besId': 'besId',
        'matchScore': '匹配分',
        'matchTier': '匹配等级',
    }
    widths = {col: len(headers.get(col, col)) for col in columns}
    formatted_rows = []
    for row in rows:
        formatted = {col: _format_value(row.get(col), col).replace('\n', ' ') for col in columns}
        formatted_rows.append(formatted)
        for col in columns:
            widths[col] = min(max(widths[col], len(formatted[col])), 80)
    header_line = ' | '.join(headers.get(col, col).ljust(widths[col]) for col in columns)
    sep_line = '-+-'.join('-' * widths[col] for col in columns)
    body_lines = []
    for row in formatted_rows:
        body_lines.append(' | '.join(row[col][:widths[col]].ljust(widths[col]) for col in columns))
    return '\n'.join([header_line, sep_line, *body_lines])


def build_relaxation_suggestions(payload: dict) -> list[str]:
    suggestions = []
    if payload.get('hasEmail'):
        suggestions.append('可先取消“必须有邮箱”筛选，扩大召回后再二次筛选')
    if payload.get('minFansNum'):
        suggestions.append('可适当降低最低粉丝门槛，例如从当前值下调 30%-50%')
    if payload.get('advancedKeywordList'):
        suggestions.append('可减少关键词数量，只保留 1-2 个核心关键词')
    if payload.get('blogCateIds'):
        suggestions.append('可放宽 WotoHub 分类，先保留一级/二级类目')
    if payload.get('regionList'):
        suggestions.append('可放宽国家范围，先测试相近市场或去掉地区限制')
    if payload.get('blogLangs'):
        suggestions.append('可放宽语言限制，优先保留英语或目标市场主语言')
    if not suggestions:
        suggestions.append('可放宽平台、地区、粉丝量或关键词条件后重试')
    return suggestions[:4]


def render_priority_recommendations(scored: list[dict], limit: int = 10) -> str:
    if not scored:
        return '暂无优先推荐结果'
    intro = f"我已经先跑出一批候选博主，下面这 {min(len(scored), limit)} 个里有几位是更值得优先看的："
    blocks = []
    for item in scored[:limit]:
        reasons = item.get('matchReasons') or []
        reason_text = '；'.join(str(x).strip() for x in reasons[:3] if str(x).strip()) or '综合匹配度较高'
        fans = _format_value(item.get('fansNum'), 'fans')
        interactive = _format_value(item.get('interactiveRate'), 'avgEngagementRate')
        gmv = _format_value(item.get('gmv30d'), 'gmv30d')
        homepage = item.get('originalLink') or item.get('link') or '-'
        wotohub_link = item.get('wotohubLink') or '-'
        bes_id = item.get('besId') or '-'
        action = item.get('matchTier') or '观察'
        lines = [
            str(item.get('nickname') or '未知博主'),
            '',
            f'建议动作：{action}',
            f'粉丝：{fans}',
            f'平均互动率：{interactive}',
        ]
        if gmv not in ('-', '0'):
            lines.append(f'近30日 GMV：{gmv}')
        lines.extend([
            f'主页：{homepage}',
            f'WotoHub 分析：{wotohub_link}',
            f'besId：{bes_id}',
            f'理由：{reason_text}',
        ])
        blocks.append('\n'.join(lines))
    return intro + "\n\n" + "\n\n".join(blocks)


def _collect_selection_hints(scored: list[dict], limit: int = 5) -> list[str]:
    hints = []
    for idx, item in enumerate(scored[:limit], 1):
        blogger_id = str(item.get('besId') or item.get('bEsId') or item.get('bloggerId') or item.get('id') or '').strip()
        nickname = str(item.get('nickname') or item.get('channelName') or '').strip() or f'候选{idx}'
        if blogger_id:
            hints.append(f"{idx}. {nickname} (besId: {blogger_id})")
        else:
            hints.append(f"{idx}. {nickname}")
    return hints


def _build_next_step_guidance(scored: list[dict]) -> str:
    selection_hints = _collect_selection_hints(scored, limit=5)
    lines = [
        "下一步建议：",
        "1. 先从当前结果里选 3-5 位最想联系的达人；可直接回复排名（如：1,3,5），也可直接给我 besId 列表。",
        "2. 如果要继续生成邀约邮件，请同时补齐最小 brief：productName、senderName、offerType（sample / paid / affiliate）。",
        "3. 邮件建议先走 prepare_only 预览，确认后再批量发送。",
    ]
    if selection_hints:
        lines.append("可直接参考前几位：")
        lines.extend(f"- {item}" for item in selection_hints)
    return "\n".join(lines)


def build_recommendation_display(table_rows: list[dict], scored: list[dict], payload: dict) -> dict[str, Any]:
    table_columns = [
        'channelName', 'fans', 'avgViews', 'avgEngagementRate', 'platform',
        'gmv30d', 'originalLink', 'tags', 'wotohubLink', 'advantages'
    ]
    if table_rows:
        display_limit = min(len(table_rows), 10)
        summary = f"共找到 {len(scored)} 位红人，先展示前 {display_limit} 位（脚本做基础执行排序，详细语义优先级建议应由模型补充）"
        markdown_table = render_markdown_table(table_rows[:display_limit], table_columns)
        plaintext_table = render_plaintext_table(table_rows[:display_limit], table_columns)
        priority_text = render_priority_recommendations(scored, display_limit)
        selection_hints = _collect_selection_hints(scored, limit=5)
        next_step_guidance = _build_next_step_guidance(scored)
        markdown_display_text = priority_text + "\n\n## 推荐博主表格\n\n" + markdown_table + "\n\n## 下一步\n\n" + next_step_guidance
        plain_text_display = priority_text + "\n\n推荐博主表格\n\n" + plaintext_table + "\n\n" + next_step_guidance
        return {
            'tableColumns': table_columns,
            'summary': summary,
            'priorityText': priority_text,
            'markdownTable': markdown_table,
            'plainTextTable': plaintext_table,
            'markdownDisplayText': markdown_display_text,
            'plainTextDisplay': plain_text_display,
            'displayText': markdown_display_text,
            'nextStepGuidance': next_step_guidance,
            'selectionHints': selection_hints,
            'emptyState': None,
        }
    suggestions = build_relaxation_suggestions(payload)
    summary = '未找到匹配红人'
    bullet_lines = '\n'.join(f"- {item}" for item in suggestions)
    display_text = summary + "\n\n建议你尝试以下放宽方式：\n" + bullet_lines
    return {
        'tableColumns': table_columns,
        'summary': summary,
        'priorityText': None,
        'markdownTable': '暂无结果',
        'plainTextTable': '暂无结果',
        'markdownDisplayText': display_text,
        'plainTextDisplay': display_text,
        'displayText': display_text,
        'nextStepGuidance': None,
        'selectionHints': [],
        'emptyState': {
            'message': summary,
            'suggestions': suggestions,
        },
    }
