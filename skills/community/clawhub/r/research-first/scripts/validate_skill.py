#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agent Skills 规范校验器（本地等价实现，替代 `uvx skills-ref validate`）

用法: python validate_skill.py <skill目录>

实现依据（2026-10-18 research，非凭印象）:
  https://agentskills.io            —— 格式开放标准（Anthropic 起源）
  https://github.com/agentskills/agentskills  —— spec
  agentskills.io/specification     —— 字段与阈值
校验项:
  1. SKILL.md 存在且文件名精确
  2. frontmatter 存在且为合法 key: value
  3. name 合法（^[a-z0-9]+(-[a-z0-9]+)*$，1-64）
  4. 目录名 == frontmatter name
  5. description 1-1024 字符且含 "Use when"
  6. SKILL.md < 500 行
  7. 顶层只允许 scripts/ references/ assets/
  8. ⛔ 不得含 context: fork（Claude Code 专属，含它会让其他 ~54 个 agent 静默降级）
  9. license 字段（推荐但非强制）

退出码: 0 = 通过 / 1 = 有 FAIL / 2 = 解析失败（vacuous guard）

⛔ VACUOUS_GUARD: 读不到 name/description 时必须 exit 2 ——
「没读到」绝不等于「通过」，否则改个格式就静默变橡皮章。
"""
import os
import re
import sys

NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
ALLOWED_DIRS = {'scripts', 'references', 'assets', '.claude-plugin', '.git'}
REQUIRED_HINT = 'Use when'


def die(msg, code=2):
    print(f'⛔ {msg}')
    sys.exit(code)


def parse_frontmatter(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return None, text, '文件未以 --- 开头（缺少 frontmatter）'
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end = i
            break
    if end is None:
        return None, text, 'frontmatter 没有闭合的 ---'
    fm = {}
    for ln in lines[1:end]:
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', ln)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in '"\'':
                val = val[1:-1]
            fm[key] = val
    return fm, text, None


def main(skill_dir):
    skill_dir = skill_dir.rstrip('/\\')
    dir_name = os.path.basename(skill_dir.replace('\\', '/').rstrip('/'))
    if not os.path.isdir(skill_dir):
        die(f'目录不存在: {skill_dir}')
    skill_md = os.path.join(skill_dir, 'SKILL.md')

    results = []
    if not os.path.isfile(skill_md):
        results.append(('FAIL', 'SKILL.md', '文件不存在（文件名必须是精确的 SKILL.md）'))
        report(dir_name, results)
    fm, text, err = parse_frontmatter(skill_md)

    if err:
        results.append(('FAIL', 'frontmatter', err))
        report(dir_name, results)

    # ⛔ VACUOUS_GUARD
    if not fm:
        die('frontmatter 解析出 0 个字段 —— 校验器空过。'
            ' 「读不到」不等于「通过」，请检查 YAML 格式。')
    if 'name' not in fm or 'description' not in fm:
        die(f'缺少必需字段（解析到: {list(fm)}）—— name 与 description 都必须有。')

    name = fm.get('name', '')
    desc = fm.get('description', '')

    # 1 name
    if not NAME_RE.match(name):
        results.append(('FAIL', 'name', f'不合法: "{name}"（只允许小写字母/数字/连字符）'))
    elif len(name) > 64:
        results.append(('FAIL', 'name', f'超长 {len(name)} > 64'))
    else:
        results.append(('PASS', 'name', f'{name}'))

    # 2 目录名一致
    if dir_name != name:
        results.append(('FAIL', '目录名', f'目录 "{dir_name}" ≠ name "{name}"（规范要求一致）'))
    else:
        results.append(('PASS', '目录名', f'{dir_name} == name'))

    # 3 description
    if len(desc) > 1024:
        results.append(('FAIL', 'description', f'超长 {len(desc)} > 1024 字符'))
    elif len(desc) < 10:
        results.append(('FAIL', 'description', f'过短 {len(desc)} 字符'))
    elif REQUIRED_HINT.lower() not in desc.lower():
        results.append(('WARN', 'description',
                        f'未含 "{REQUIRED_HINT}" —— 规范建议写成触发条件，'
                        f'否则 agent 可能不会激活本 skill'))
    else:
        results.append(('PASS', 'description', f'{len(desc)} 字符，含 "{REQUIRED_HINT}"'))

    # 4 行数
    n = len(text.splitlines())
    if n >= 500:
        results.append(('FAIL', 'SKILL.md 行数', f'{n} 行 ≥ 500，规范要求 < 500（深度内容应放 references/）'))
    else:
        results.append(('PASS', 'SKILL.md 行数', f'{n} 行 < 500'))

    # 5 子目录
    extras = [d for d in os.listdir(skill_dir)
              if os.path.isdir(os.path.join(skill_dir, d)) and d not in ALLOWED_DIRS]
    if extras:
        results.append(('WARN', '子目录', f'非标准目录: {extras}（规范只定义 scripts/ references/ assets/）'))
    else:
        results.append(('PASS', '子目录', '仅 scripts/ references/ assets/'))

    # 6 context: fork
    if re.search(r'^context\s*:', fm.get('__raw__', '') or '', re.M) or 'context: fork' in text[:text.find('---', 3)]:
        results.append(('FAIL', 'context: fork',
                        '⛔ 这是 Claude Code 专属字段，含它会让其他 agent 静默降级'))
    else:
        results.append(('PASS', 'context: fork', '未使用（可移植）'))

    # 7 license
    if 'license' in fm:
        results.append(('PASS', 'license', fm['license']))
    else:
        results.append(('WARN', 'license', '未声明（推荐 MIT / Apache-2.0）'))

    report(dir_name, results)


def report(dir_name, results):
    print(f'\nAgent Skills 规范校验 —— {dir_name}\n' + '-' * 58)
    fails = 0
    for level, item, msg in results:
        icon = {'PASS': '✅', 'WARN': '⚠️ ', 'FAIL': '⛔'}[level]
        print(f'{icon} {item:<18}: {msg}')
        if level == 'FAIL':
            fails += 1
    print('-' * 58)
    print(('✅ 符合规范' if not fails else f'❌ {fails} 项不合规 —— ⛔ 别发布')
          + ('（⚠️ 项建议一并处理）' if any(l == 'WARN' for l, _, _ in results) else ''))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('用法: python validate_skill.py <skill目录>')
        sys.exit(2)
    main(sys.argv[1])
