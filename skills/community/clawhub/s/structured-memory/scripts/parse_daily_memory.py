#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DOMAIN_BITS = {
    'strategy': 0,
    'business': 1,
    'organization': 2,
    'finance': 3,
    'legal': 4,
    'project': 5,
    'operations': 6,
    'tech': 7,
    'routines': 8,
    'personal': 9,
    'meta': 10,
    'misc': 11,
}

LINE_RULES = [
    (r'目标|路线图|roadmap|planning|优先级|资源分配', 'strategy', 'priority'),
    (r'晨报|ai-tech-daily-brief', 'routines', 'morning-brief'),
    (r'cron|定时', 'routines', 'cron'),
    (r'提醒我|设置提醒|提醒事项|提醒时间', 'routines', 'reminder'),
    (r'日报', 'routines', 'daily-report'),
    (r'周报', 'routines', 'weekly-report'),
    (r'openclaw', 'tech', 'openclaw'),
    (r'context-engine|插件|plugin|架构', 'tech', 'architecture'),
    (r'agent|模型|gpt|人工智能|legacy', 'tech', 'ai'),
    (r'代码|脚本', 'tech', 'coding'),
    (r'安全|权限边界|敏感配置', 'tech', 'security'),
    (r'记忆系统|memory system|taxonomy|module|entity|tag|critical-facts|structured-memory', 'meta', 'memory-system'),
    (r'规则|workflow|回复|先查 memory|先主动查|查不到记录|检索上限|事件核心|daily memory|summary', 'meta', 'workflow-rule'),
    (r'项目|phase|里程碑|风险|阻塞|实现|spec|blocker|owner|依赖|milestone|progress|延期|change request|change-request|变更', 'project', 'risk'),
    (r'客户|交付|需求|产品|演示版本|增长|定价|销售', 'business', 'product'),
    (r'公司|组织|团队|流程|汇报|reporting|会议|headcount|人力', 'organization', 'process'),
    (r'招聘|绩效|人事|入职|离职|onboarding', 'organization', 'recruiting'),
    (r'财务|报销|预算|发票|税|付款|revenue|报表', 'finance', 'budget'),
    (r'合同|合规|法务|nda|授权|条款|知识产权|approval', 'legal', 'contract'),
    (r'运维|执行|支持|跟进|交接|故障|support|follow-up|incident|值守|工单', 'operations', 'workflow'),
    (r'个人|习惯|偏好|健康|情绪|生活|状态|休息|睡眠|作息', 'personal', 'preference'),
    (r'学习|读完|读书|方法论|课程|研究|周末', 'personal', 'learning'),
]

TAXONOMY_CONTEXT_PATTERN = r'taxonomy|domain|module|entity|tag|structured-memory|分类|职场通用|按需创建|精简|关键事实|分类策略|只是为了说明|举个例子|分类示例|讨论.*算.*(operations|meta)|讨论.*workflow'

ENTITY_RULES = [
    (r'\bOpenClaw\b', 'OpenClaw'),
    (r'\bFeishu\b|飞书', 'Feishu'),
    (r'\bUserA\b', 'UserA'),
    (r'\bai-tech-daily-brief\b', 'ai-tech-daily-brief'),
    (r'\bstructured-memory\b', 'structured-memory'),
    (r'\bGPT-5\.4\b', 'GPT-5.4'),
]

SYSTEM_TAG_RULES = [
    (r'失败|error|故障', 'failure'),
    (r'修复|解决|resolved|补发', 'resolved'),
    (r'纠正|要求|规则|必须|确认', 'rule'),
    (r'项目|spec', 'project'),
    (r'提醒|任务|cron|晨报', 'task'),
    (r'纠正|指出', 'correction'),
    (r'故障|失败|投递', 'incident'),
]

FREE_TAG_PATTERNS = [
    'context-engine',
    'delivery',
    'retrieval',
    'critical-facts',
    'taxonomy',
    'module',
    'entity',
    'tag',
    'cron',
    'memory',
]


def uniq(seq):
    seen = set()
    out = []
    for x in seq:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def parse_structured_entries(text: str):
    entries = []
    if '## Entries' not in text:
        return entries
    block = text.split('## Entries', 1)[1]
    parts = re.split(r'\n-\s+', '\n' + block)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        item = {
            'domains': [], 'modules': [], 'entities': [], 'system_tags': [], 'free_tags': []
        }
        for key in item.keys():
            m = re.search(rf'{key}:\s*\[(.*?)\]', part)
            if m:
                vals = [x.strip().strip('"\'') for x in m.group(1).split(',') if x.strip()]
                item[key] = vals
        m = re.search(r'importance:\s*(\w+)', part)
        if m:
            item['importance'] = m.group(1)
        m = re.search(r'summary:\s*(.+)', part)
        if m:
            item['summary'] = m.group(1).strip()
        entries.append(item)
    return entries


def infer_from_text(text: str):
    domains, modules, entities, system_tags, free_tags = [], [], [], [], []

    lines = [ln.strip('- ').strip() for ln in text.splitlines() if ln.strip().startswith('- ')]
    if not lines:
        lines = [text]

    document_taxonomy_context = re.search(TAXONOMY_CONTEXT_PATTERN, text, flags=re.I) is not None
    has_real_world_signal = re.search(r'真正发生|真问题|真实业务推进|客户要求|必须交付|可演示版本|已查明|根因|OpenClaw 脚本|报销单|发票附件|付款时间|incident 已|support 工单|follow-up', text, flags=re.I) is not None

    line_hits = []
    for line in lines:
        taxonomy_context = re.search(TAXONOMY_CONTEXT_PATTERN, line, flags=re.I) or (document_taxonomy_context and not has_real_world_signal)
        local_domains, local_modules = [], []
        for pattern, domain, module in LINE_RULES:
            if not re.search(pattern, line, flags=re.I):
                continue
            if taxonomy_context and domain in {'business', 'finance', 'legal', 'organization', 'personal', 'operations'}:
                continue
            local_domains.append(domain)
            local_modules.append(module)
        for pattern, entity_name in ENTITY_RULES:
            if re.search(pattern, line, flags=re.I):
                entities.append(entity_name)
        for pattern, tag in SYSTEM_TAG_RULES:
            if re.search(pattern, line, flags=re.I):
                system_tags.append(tag)
        low = line.lower()
        for tag in FREE_TAG_PATTERNS:
            if tag.lower() in low:
                free_tags.append(tag)
        line_hits.append({
            'line': line,
            'domains': uniq(local_domains),
            'modules': uniq(local_modules),
        })

    # 句子级权重：优先采用“高信号行”上的命中，避免整篇被弱示例词带偏。
    prioritized = []
    for item in line_hits:
        line = item['line']
        score = 0
        if re.search(r'根因|已查明|失败|error|故障|修复|补发', line, flags=re.I):
            score += 3
        if re.search(r'明确纠正|确认|要求|规则|方案|设计|实现', line, flags=re.I):
            score += 2
        if re.search(r'例如|比如|覆盖|包括|举例', line, flags=re.I):
            score -= 2
        prioritized.append((score, item))

    prioritized.sort(key=lambda x: x[0], reverse=True)

    for score, item in prioritized:
        domains.extend(item['domains'])
        modules.extend(item['modules'])

    signal_lines = ' '.join(lines)

    if re.search(r'讨论.*workflow|workflow 这个词|不是在说真实交接|不是在说真实故障', signal_lines, flags=re.I):
        domains = [d for d in domains if d != 'operations']
        modules = [m for m in modules if m != 'workflow']

    if 'ai-tech-daily-brief' in entities and 'ai' in modules:
        # 任务名中的 ai 不应自动推导为通用 AI 主题。
        if not re.search(r'人工智能|AI 能力|AI 模型|聊 AI|讨论 AI', signal_lines, flags=re.I):
            modules = [m for m in modules if m != 'ai']

    # 更严格的 module 约束，避免过宽命中。
    if 'context-engine' not in signal_lines.lower() and '插件' not in signal_lines and 'plugin' not in signal_lines.lower():
        modules = [m for m in modules if m != 'architecture']
    if not re.search(r'风险|阻塞|phase|里程碑|项目|实现|spec|blocker|owner|依赖|milestone|变更', signal_lines, flags=re.I):
        modules = [m for m in modules if m != 'risk']

    if 'project' in domains and re.search(r'里程碑|owner|依赖|变更|blocker|风险|milestone|change request|change-request', signal_lines, flags=re.I):
        modules.append('risk')
    if 'business' in domains and re.search(r'客户|交付|需求|产品|销售|定价|增长', signal_lines, flags=re.I):
        modules.append('product')

    if not domains:
        domains = ['misc']
        modules = ['uncategorized']

    domains = uniq(domains)
    modules = uniq(modules)
    entities = uniq(entities)
    system_tags = uniq(system_tags)
    free_tags = uniq(free_tags)

    priority = 'high' if ('failure' in system_tags or 'incident' in system_tags or len(domains) >= 3) else 'medium'
    return {
        'domains': domains,
        'modules': modules,
        'entities': entities,
        'system_tags': system_tags,
        'free_tags': free_tags,
        'priority': priority,
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: parse_daily_memory.py <memory_markdown>')
    path = Path(sys.argv[1])
    text = path.read_text(encoding='utf-8')
    date = path.stem

    structured = parse_structured_entries(text)
    if structured:
        domains, modules, entities, system_tags, free_tags = [], [], [], [], []
        priority = 'medium'
        for item in structured:
            domains.extend(item.get('domains', []))
            modules.extend(item.get('modules', []))
            entities.extend(item.get('entities', []))
            system_tags.extend(item.get('system_tags', []))
            free_tags.extend(item.get('free_tags', []))
            if item.get('importance') in ('high', 'critical'):
                priority = 'high'
        result = {
            'date': date,
            'domains': uniq(domains),
            'modules': uniq(modules),
            'entities': uniq(entities),
            'system_tags': uniq(system_tags),
            'free_tags': uniq(free_tags),
            'priority': priority,
            'source_format': 'structured',
        }
    else:
        inferred = infer_from_text(text)
        result = {'date': date, **inferred, 'source_format': 'legacy'}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
