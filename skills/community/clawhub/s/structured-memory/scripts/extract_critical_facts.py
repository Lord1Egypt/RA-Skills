#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CRITICAL_FACTS_DIR = ROOT / 'critical-facts'

EXAMPLE_ONLY_PATTERNS = [
    r'举个例子',
    r'只是为了说明',
    r'只是举例',
    r'都只是举例',
    r'讨论 critical-facts',
    r'设计边界',
    r'分类讨论',
    r'不代表真的',
    r'不是在记录真实',
    r'example only',
]

REAL_SIGNAL_PATTERNS = [
    r'服务器',
    r'主机',
    r'IP 是',
    r'地址是',
    r'路径是',
    r'endpoint 是',
    r'服务地址',
    r'用于',
    r'登录',
    r'部署',
    r'连接',
    r'修复',
    r'执行',
    r'这台',
    r'那台',
]

IPV4_RE = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
URL_RE = re.compile(r'https?://[^\s)`\]>]+')
PATH_RE = re.compile(r'(?<![\w.-])/(?:[\w.-]+/)*[\w.-]+')
OPEN_ID_RE = re.compile(r'\bou_[A-Za-z0-9_]+\b')
CHAT_ID_RE = re.compile(r'\bchat:[A-Za-z0-9_:-]+\b')
UUID_RE = re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', re.I)
JOB_ID_RE = re.compile(r'\b(?:job[_ -]?id|run[_ -]?id)[:= ]+([A-Za-z0-9_-]+)\b', re.I)
SERVICE_RE = re.compile(r'\b[a-z0-9][a-z0-9-]*(?:\.[a-z0-9-]+)?\.service\b', re.I)
REPO_RE = re.compile(r'(?:git@[^\s:]+:[^\s]+|https?://(?:github\.com|gitlab\.com|gitee\.com)/[^\s)]+)')
ACCOUNT_RE = re.compile(r'\b(?:user|username|账号|账户)[:： ]+([A-Za-z0-9._-]+)\b', re.I)
SERVICE_CONTEXT_RE = re.compile(r'服务名|service|systemd|unit|daemon|gateway|网关|服务地址|endpoint', re.I)
PARSE_SCRIPT = ROOT / 'skills/structured-memory/scripts/parse_daily_memory.py'
EXCLUDED_PROJECT_ENTITIES = {'UserA', 'OpenClaw', 'Feishu', 'GPT-5.4'}
GENERIC_ENTITIES = {'UserA', 'GPT-5.4'}


def uniq_dicts(items):
    seen = set()
    out = []
    for item in items:
        key = (item.get('fact_type'), item.get('value'))
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def sensitivity_for(fact_type: str, value: str) -> str:
    if fact_type in {'host', 'account'}:
        return 'high'
    if fact_type in {'endpoint', 'path', 'repo', 'service', 'identifier', 'cron'}:
        return 'medium'
    return 'low'


def target_file_for(fact_type: str) -> Path:
    mapping = {
        'host': CRITICAL_FACTS_DIR / 'hosts.md',
        'account': CRITICAL_FACTS_DIR / 'credentials.md',
        'path': CRITICAL_FACTS_DIR / 'locations.md',
        'repo': CRITICAL_FACTS_DIR / 'locations.md',
        'service': CRITICAL_FACTS_DIR / 'services.md',
        'endpoint': CRITICAL_FACTS_DIR / 'services.md',
        'cron': CRITICAL_FACTS_DIR / 'automation.md',
        'identifier': CRITICAL_FACTS_DIR / 'ids.md',
        'document-ref': CRITICAL_FACTS_DIR / 'ids.md',
        'address': CRITICAL_FACTS_DIR / 'locations.md',
        'device': CRITICAL_FACTS_DIR / 'ids.md',
    }
    return mapping.get(fact_type, CRITICAL_FACTS_DIR / 'ids.md')


def line_is_example_only(line: str) -> bool:
    has_example = any(re.search(p, line, flags=re.I) for p in EXAMPLE_ONLY_PATTERNS)
    has_real_signal = any(re.search(p, line, flags=re.I) for p in REAL_SIGNAL_PATTERNS)
    return has_example and not has_real_signal


def load_context(path: Path) -> dict:
    raw = subprocess.run(
        ['python3', str(PARSE_SCRIPT), str(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return json.loads(raw)


def infer_related_project(context: dict) -> str:
    if 'project' not in context.get('domains', []):
        return ''
    for entity in context.get('entities', []):
        if entity not in EXCLUDED_PROJECT_ENTITIES:
            return entity
    for tag in context.get('free_tags', []):
        if tag not in {'memory', 'regression', 'cleanup'}:
            return tag
    return ''


def infer_related_entity(line: str, value: str, fact_type: str, context: dict) -> str:
    m = re.search(r'([\w\u4e00-\u9fff.-]{1,20})那台服务器', line)
    if m:
        return f"{m.group(1)}服务器"
    m = re.search(r'([\w\u4e00-\u9fff.-]{1,20})服务器', line)
    if m and m.group(1) not in {'台', '那台', '这台'}:
        return f"{m.group(1)}服务器"

    for entity in context.get('entities', []):
        if entity in GENERIC_ENTITIES:
            continue
        if re.search(re.escape(entity), line, flags=re.I):
            return entity

    low_line = line.lower()
    low_value = value.lower()
    if 'openclaw' in low_line or 'openclaw' in low_value:
        return 'OpenClaw'
    if 'feishu' in low_line or '飞书' in line or value.startswith('ou_'):
        return 'Feishu'
    return ''


def make_fact(date: str, fact_type: str, value: str, line: str, context: dict) -> dict:
    value = value.strip('`"\'.,)】]')
    return {
        'entity': value,
        'fact_type': fact_type,
        'value': value,
        'status': 'active',
        'sensitivity': sensitivity_for(fact_type, value),
        'source': f'memory/{date}.md',
        'last_verified': date,
        'domains': context.get('domains', []),
        'modules': context.get('modules', []),
        'tags': context.get('system_tags', []) + context.get('free_tags', []),
        'related_project': infer_related_project(context),
        'related_entity': infer_related_entity(line, value, fact_type, context),
        'note': line.strip(),
    }


def extract_from_text(date: str, text: str, context: dict) -> list[dict]:
    facts = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line_is_example_only(line):
            continue

        for m in IPV4_RE.findall(line):
            facts.append(make_fact(date, 'host', m, line, context))
        for m in URL_RE.findall(line):
            facts.append(make_fact(date, 'endpoint', m, line, context))
        for m in REPO_RE.findall(line):
            facts.append(make_fact(date, 'repo', m, line, context))
        for m in PATH_RE.findall(line):
            if m.startswith('/home') or m.startswith('/etc') or m.startswith('/var') or m.startswith('/opt') or m.startswith('/srv'):
                facts.append(make_fact(date, 'path', m, line, context))
        for m in OPEN_ID_RE.findall(line):
            facts.append(make_fact(date, 'identifier', m, line, context))
        for m in CHAT_ID_RE.findall(line):
            facts.append(make_fact(date, 'identifier', m, line, context))
        for m in UUID_RE.findall(line):
            facts.append(make_fact(date, 'identifier', m, line, context))
        if SERVICE_CONTEXT_RE.search(line):
            for m in SERVICE_RE.findall(line):
                facts.append(make_fact(date, 'service', m, line, context))
            if re.search(r'\bOpenClaw\b', line) and re.search(r'gateway|daemon|systemd|unit|服务', line, flags=re.I):
                facts.append(make_fact(date, 'service', 'OpenClaw', line, context))
        for m in ACCOUNT_RE.findall(line):
            facts.append(make_fact(date, 'account', m, line, context))
        for m in JOB_ID_RE.findall(line):
            facts.append(make_fact(date, 'identifier', m, line, context))

    return uniq_dicts(facts)


def append_fact(path: Path, fact: dict) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = f'# {path.stem}\n\n'
    if not path.exists():
        path.write_text(header, encoding='utf-8')
    text = path.read_text(encoding='utf-8')

    marker = f"## {fact['last_verified']}"
    lines = text.splitlines()
    if marker in lines:
        start = lines.index(marker)
        end = start + 1
        while end < len(lines) and not lines[end].startswith('## '):
            end += 1
        section = lines[start:end]
    else:
        if not text.endswith('\n'):
            text += '\n'
        text += f"\n{marker}\n"
        path.write_text(text, encoding='utf-8')
        lines = text.splitlines()
        start = lines.index(marker)
        end = len(lines)
        section = lines[start:end]

    needle = f"  fact_type: {fact['fact_type']}\n  value: {fact['value']}\n"
    section_text = '\n'.join(section) + '\n'
    if needle in section_text:
        return False

    block = (
        f"- entity: {fact['entity']}\n"
        f"  fact_type: {fact['fact_type']}\n"
        f"  value: {fact['value']}\n"
        f"  status: {fact['status']}\n"
        f"  sensitivity: {fact['sensitivity']}\n"
        f"  source: {fact['source']}\n"
        f"  last_verified: {fact['last_verified']}\n"
        f"  domains: {fact['domains']}\n"
        f"  modules: {fact['modules']}\n"
        f"  tags: {fact['tags']}\n"
        f"  related_project: {fact['related_project']}\n"
        f"  related_entity: {fact['related_entity']}\n"
        f"  note: {fact['note']}\n"
    )
    path.write_text(path.read_text(encoding='utf-8').rstrip() + '\n' + block, encoding='utf-8')
    return True


def main():
    parser = argparse.ArgumentParser(description='Extract reusable execution-critical facts from a daily memory markdown file.')
    parser.add_argument('memory_markdown', help='Path to memory/YYYY-MM-DD.md')
    parser.add_argument('--write', action='store_true', help='Also append extracted facts into critical-facts/*.md')
    args = parser.parse_args()

    path = Path(args.memory_markdown)
    text = path.read_text(encoding='utf-8')
    date = path.stem
    context = load_context(path)
    facts = extract_from_text(date, text, context)

    written = []
    if args.write:
        for fact in facts:
            target = target_file_for(fact['fact_type'])
            if append_fact(target, fact):
                written.append(str(target.relative_to(ROOT)))

    print(json.dumps({'date': date, 'facts': facts, 'written': written}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
