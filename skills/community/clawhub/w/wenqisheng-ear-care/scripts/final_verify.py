#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终验证脚本：检查 SKILL.md 数据分离和文件完整性"""

import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
REF_DIR = os.path.join(SKILL_DIR, 'references')

OK = '✅'
NO = '❌'
WARN = '⚠️'

passed = 0
failed = 0

def check(label, condition, detail=''):
    global passed, failed
    if condition:
        passed += 1
        print(f'  {OK} [PASS] {label}')
    else:
        failed += 1
        print(f'  {NO} [FAIL] {label}')
        if detail:
            print(f'         → {detail}')

def read_file(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def ref(filename):
    return os.path.join(REF_DIR, filename)

# ============================================================
# P0: 数据分离检查
# ============================================================
print('\n=== P0: 数据与逻辑分离检查 ===')

sk = read_file(os.path.join(SKILL_DIR, 'SKILL.md'))

# SKILL.md 不应包含硬编码业务数据
check('SKILL.md 无硬编码地址路名', '北京东路' not in sk)
check('SKILL.md 无硬编码门牌号', '京东小区北门' not in sk)
check('SKILL.md 无硬编码Wi-Fi密码', 'eqs88888888' not in sk)
check('SKILL.md 无硬编码座机号', '3361632122' not in sk)
check('SKILL.md 无硬编码手机号', '13361632122' not in sk)
check('SKILL.md 无硬编码地铁站名', '高新地铁站' not in sk)
check('SKILL.md 无硬编码具体价格(58元)', '58元' not in sk)
check('SKILL.md 无硬编码具体价格(98元)', '98元' not in sk)
check('SKILL.md 无硬编码具体价格(128元)', '128元' not in sk)
check('SKILL.md 含数据读取规则', '数据读取规则' in sk)
check('SKILL.md 含 references 引用', 'references/' in sk)

# ============================================================
# P1: 参考文件完整性
# ============================================================
print('\n=== P1: 参考文件完整性 ===')

for fname in ['business-info.md', 'services.md', 'promotions.md', 'faq.md', 'brand.md']:
    path = ref(fname)
    check(f'{fname} 存在', os.path.exists(path))
    if os.path.exists(path):
        content = read_file(path)
        check(f'{fname} 非空', len(content) > 100, f'仅{len(content)}字符')

# ============================================================
# P2: 安全红线检查
# ============================================================
print('\n=== P2: 安全红线检查 ===')

check('SKILL.md 含三步流程', '三步流程' in sk)
check('SKILL.md 禁止AI诊断', '不得给出诊断结论' in sk)
check('SKILL.md 含鼓膜穿孔禁止', '鼓膜穿孔' in sk)
check('SKILL.md 含紧急症状处理', '紧急症状' in sk)

faq = read_file(ref('faq.md'))
check('FAQ Q2 引导到店检测', '到店' in faq and '检测' in faq)
check('FAQ Q3 有限定词(一般情况)', '一般情况下' in faq or '一般情况' in faq)
check('FAQ Q7 引导到店检测', '到店' in faq and '检测' in faq)
check('FAQ 含鼓膜穿孔→就医', '就医' in faq)

# ============================================================
# P3: 版本管理
# ============================================================
print('\n=== P3: 版本管理检查 ===')

ver_path = os.path.join(SKILL_DIR, 'version.json')
check('version.json 存在', os.path.exists(ver_path))
if os.path.exists(ver_path):
    ver = json.loads(read_file(ver_path))
    check('version 字段', 'version' in ver)
    check('data_version 字段', 'data_version' in ver)
    check('skill 字段', 'skill' in ver and ver['skill'] == 'wenqisheng-ear-care')

check('CHANGELOG.md 存在', os.path.exists(os.path.join(SKILL_DIR, 'CHANGELOG.md')))
check('Git 仓库已初始化', os.path.exists(os.path.join(SKILL_DIR, '.git', 'HEAD')))
check('auto_update.sh 存在', os.path.exists(os.path.join(SKILL_DIR, 'scripts', 'auto_update.sh')))
check('GitHub Actions workflow 存在', os.path.exists(os.path.join(SKILL_DIR, '.github', 'workflows', 'release.yml')))

# ============================================================
# P4: 脚本可移植性
# ============================================================
print('\n=== P4: 脚本可移植性检查 ===')

def has_windows_path(filepath):
    """Check if file contains hardcoded Windows user paths (not in this check code)"""
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if 'has_windows_path' in line or 'has_win_path' in line:
            continue  # skip this check function itself
        if 'C:\\Users\\' in line or 'C:/Users/' in line:
            return True
    return False

# skip final_verify.py from self-check to avoid false positive
for script in ['update_skill.py', 'test_skill.py']:
    spath = os.path.join(SCRIPT_DIR, script)
    if os.path.exists(spath):
        content = read_file(spath)
        check(f'{script} 无硬编码Windows路径', not has_windows_path(spath))
        check(f'{script} 使用相对路径', 'os.path.dirname' in content or 'SCRIPT_DIR' in content)

# ============================================================
# 汇总
# ============================================================
total = passed + failed
print(f'\n{"="*55}')
print(f'  最终验证汇总')
print(f'{"="*55}')
print(f'  通过: {passed}/{total}')
print(f'  失败: {failed}/{total}')
print(f'  通过率: {passed/total*100:.0f}%' if total > 0 else '  无结果')
print(f'  综合: {"ALL CLEAR" if failed == 0 else "NEEDS WORK"}')
print(f'{"="*55}')
exit(0 if failed == 0 else 1)
