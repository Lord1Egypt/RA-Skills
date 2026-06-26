#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

INTERNAL_TUNING_PATTERNS = [
    r'^structured-memory 精度打磨继续推进',
    r'^继续收紧',
    r'^针对 summary',
    r'幂等性检查',
    r'分层选句策略',
    r'重建逻辑',
    r'误分类问题收紧',
    r'摘要选择',
]

LOW_SIGNAL_PATTERNS = [
    r'具体值',
    r'只是举例',
    r'举个例子',
    r'分类示例',
]

TOPIC_RULES = [
    ('strategy', r'目标|路线图|planning|优先级|资源分配'),
    ('business', r'客户|交付|需求|产品|市场|增长|定价|销售'),
    ('organization', r'例会|汇报|流程|招聘|绩效|团队|入职|onboarding|会议|headcount|人力|账号|reporting'),
    ('finance', r'报销|预算|发票|付款|收入|revenue|报表|税'),
    ('legal', r'合同|NDA|合规|授权|条款|知识产权|approval|法务'),
    ('project', r'里程碑|blocker|风险|owner|依赖|milestone|progress|延期|change request|变更'),
    ('operations', r'follow-up|support|incident|值守|交接|工单|步骤|故障'),
    ('tech', r'OpenClaw|context-engine|legacy|agent|代码|脚本|架构|AI 模型|安全|权限'),
    ('routines', r'晨报|周报|日报|cron|提醒事项|提醒时间|根因'),
    ('personal', r'系统设计|方法论|学习|睡眠|作息|健康|休息|状态|周末'),
    ('meta', r'先查 memory|没查到记录|workflow|summary|事件核心|检索上限|daily memory|规则|按需创建|精简|critical-facts|IP|账号|路径|endpoint'),
]

PREVIEW_PRIORITY = [
    r'^根因[:：]|^已查明[:：]|失败|error|故障',
    r'客户|交付|需求|产品|定价|销售|增长|市场',
    r'里程碑|blocker|风险|owner|依赖|milestone|progress|延期|change request|变更',
    r'报销|预算|发票|付款|收入|revenue|报表|税',
    r'OpenClaw|context-engine|legacy|代码|脚本|架构|AI 模型|安全|权限',
    r'合同|NDA|合规|授权|条款|知识产权|approval|法务',
    r'例会|汇报|流程|招聘|绩效|入职|onboarding|会议|headcount|人力|账号|reporting',
    r'follow-up|support|incident|值守|交接|工单|步骤',
    r'系统设计|方法论|学习|睡眠|作息|健康|休息|状态|周末',
    r'先查 memory|没查到记录|workflow|summary|事件核心|检索上限|daily memory|规则|按需创建|精简|critical-facts|IP|账号|路径|endpoint',
    r'晨报|周报|日报|cron|提醒事项|提醒时间',
]


def normalize_summary_line(line: str) -> str:
    line = re.sub(r'某个具体值|具体值', '', line, flags=re.I)
    line = re.sub(r'\s+', ' ', line).strip()
    line = re.sub(r'，\s*，', '，', line)
    return line.strip('，。 ') + ('。' if line and not line.endswith(('。', '！', '？')) else '')


def dedup(items: list[str]) -> list[str]:
    out = []
    seen = set()
    for item in items:
        item = normalize_summary_line(item) if item else item
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def should_skip(line: str) -> bool:
    # critical-facts 设计讨论里的“举例”句仍然是有价值的摘要材料，不能一刀切丢掉。
    if re.search(r'critical-facts|IP|账号|路径|endpoint', line, flags=re.I):
        return any(re.search(p, line, flags=re.I) for p in INTERNAL_TUNING_PATTERNS)
    return any(re.search(p, line, flags=re.I) for p in INTERNAL_TUNING_PATTERNS + LOW_SIGNAL_PATTERNS)


def topic_key_from_summary(text: str) -> str | None:
    for topic, pattern in TOPIC_RULES:
        if re.search(pattern, text, flags=re.I):
            return topic
    return None


def legacy_lines(text: str) -> list[str]:
    lines = [ln.strip('- ').strip() for ln in text.splitlines() if ln.strip().startswith('- ')]
    filtered = [ln for ln in lines if not should_skip(ln)]
    return filtered or lines


def summarize_structured(text: str) -> dict | None:
    entries = []
    current = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.lstrip().startswith('- domains:'):
            current = {'domains': [], 'summary': None}
            entries.append(current)
        if current is None:
            continue
        m = re.search(r'domains:\s*\[(.*?)\]', line)
        if m:
            current['domains'] = [x.strip().strip('"\'') for x in m.group(1).split(',') if x.strip()]
        m = re.search(r'summary:\s*(.+)', line)
        if m:
            current['summary'] = m.group(1).strip()
            current = None

    if not entries:
        return None

    preview = []
    topic_summaries: dict[str, list[str]] = {}
    for entry in entries:
        summary = entry.get('summary')
        if not summary:
            continue
        preview.append(summary)
        domains = entry.get('domains') or []
        topic = domains[0] if domains else topic_key_from_summary(summary) or 'misc'
        topic_summaries.setdefault(topic, []).append(summary)

    return {
        'preview': dedup(preview)[:5],
        'topic_summaries': {k: dedup(v)[:3] for k, v in topic_summaries.items()},
    }


def summarize_legacy(text: str) -> dict:
    lines = legacy_lines(text)
    preview = []
    for pattern in PREVIEW_PRIORITY:
        for line in lines:
            if line in preview:
                continue
            if re.search(pattern, line, flags=re.I):
                preview.append(line)
                break
        if len(preview) >= 5:
            break
    if not preview:
        preview = lines[:5]

    topic_summaries: dict[str, list[str]] = {}
    for topic, pattern in TOPIC_RULES:
        matched = [ln for ln in lines if re.search(pattern, ln, flags=re.I)]
        if matched:
            topic_summaries[topic] = dedup(matched)[:3]

    # 若没有命中任何主题，给 misc 兜底
    if not topic_summaries and lines:
        topic_summaries['misc'] = lines[:3]

    return {
        'preview': dedup(preview)[:5],
        'topic_summaries': topic_summaries,
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: summarize_daily_memory.py <memory_markdown>')

    text = Path(sys.argv[1]).read_text(encoding='utf-8')
    structured = summarize_structured(text)
    result = structured if structured is not None else summarize_legacy(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
