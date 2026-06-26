#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""闻其声耳轻松可视采耳 Skill 自动化测试脚本"""

import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
REF_DIR = os.path.join(SKILL_DIR, 'references')

results = {'pass': 0, 'fail': 0, 'checks': []}
P = '✅'
F = '❌'

def check(name, condition, detail=''):
    if condition:
        results['pass'] += 1
        results['checks'].append(f'  {P} {name}')
    else:
        results['fail'] += 1
        results['checks'].append(f'  {F} {name}: {detail}')
    return condition

def read_ref(filename):
    path = os.path.join(REF_DIR, filename)
    with open(path, encoding='utf-8') as f:
        return f.read()

# ========== 1. 文件结构完整性 ==========
print('=== 1. 文件结构完整性 ===')
expected_files = [
    'SKILL.md', '.gitignore', 'README.md', 'README_EN.md', 'version.json',
    'references/business-info.md', 'references/services.md',
    'references/promotions.md', 'references/faq.md', 'references/brand.md',
]
for f in expected_files:
    check(f'文件: {f}', os.path.exists(os.path.join(SKILL_DIR, f)))

# ========== 2. 参考文件内容覆盖 ==========
print('\n=== 2. 参考文件内容覆盖 ===')
ref_checks = {
    'business-info.md': ['10:00', '22:00', '南昌', '青山湖区', '北京东路',
                         '京东小区', 'eqs', 'eqs88888888', '高新'],
    'services.md': ['服务时长', '适用人群', '禁忌说明',
                    '健康耳道', '炎症', '鼓膜穿孔', '五步消毒法', '一客一换', '明码标价'],
    'promotions.md': ['300', '500', '1000', '送', '无需预约'],
    'faq.md': ['中耳炎', '孕期', '哺乳期', '消毒', '五步消毒', '一客一换',
               '持证上岗', '鼓膜穿孔', '禁忌'],
    'brand.md': ['2023', '直营', '南昌', '五步消毒法', '一客一换'],
}

for fname, keywords in ref_checks.items():
    fpath = os.path.join(REF_DIR, fname)
    if not os.path.exists(fpath):
        check(f'{fname} 文件存在', False, '文件不存在')
        continue
    content = read_ref(fname)
    missing = [kw for kw in keywords if kw not in content]
    check(f'{fname} 全部关键词覆盖', len(missing) == 0,
          f'缺失: {missing}' if missing else '')

# ========== 3. SKILL.md 结构完整性 ==========
print('\n=== 3. SKILL.md 结构完整性 ===')
sk_path = os.path.join(SKILL_DIR, 'SKILL.md')
with open(sk_path, encoding='utf-8') as f:
    sk = f.read()

structure_checks = {
    'YAML frontmatter name': 'name: wenqisheng-ear-care' in sk,
    'YAML frontmatter description': 'description:' in sk,
    '触发关键词覆盖': '闻其声' in sk and '可视采耳' in sk and '采耳' in sk,
    '数据读取规则': '数据读取规则' in sk,
    '引用business-info.md': 'business-info.md' in sk,
    '引用services.md': 'services.md' in sk,
    '引用promotions.md': 'promotions.md' in sk,
    '引用faq.md': 'faq.md' in sk,
    '引用brand.md': 'brand.md' in sk,
    '语气规范': '专业严谨' in sk,
    '症状处理分级机制': '症状处理分级' in sk or '三步流程' in sk,
    '鼓膜穿孔禁忌': '鼓膜穿孔' in sk,
    '首次对话判断': '首次对话' in sk,
    '紧急症状转诊': '紧急症状' in sk,
    '竞品对比应对': '竞品对比' in sk,
    '短关键词触发': '短关键词触发' in sk,
    '用户情绪处理': '用户情绪处理' in sk,
    '引导式追问': '引导式追问' in sk,
    '严禁AI诊断': '不得给出诊断结论' in sk,
}

for label, condition in structure_checks.items():
    check(label, condition, '' if condition else '缺失')

# ========== 4. 检查 SKILL.md 无硬编码业务数据 ==========
print('\n=== 4. 检查 SKILL.md 无硬编码业务数据 ===')
# 这些数据应该只在 references/ 中出现，不应硬编码在 SKILL.md 中
hardcoded_checks = [
    ('无硬编码具体地址路名', '北京东路' not in sk),
    ('无硬编码具体门牌', '京东小区北门' not in sk),
    ('无硬编码地铁站名', '高新地铁站' not in sk),
    ('无硬编码Wi-Fi密码', 'eqs88888888' not in sk),
    ('无硬编码座机号', '(0791) 3361632122' not in sk and '0791-3361632122' not in sk),
    ('无硬编码手机号', '13361632122' not in sk),
]
for label, condition in hardcoded_checks:
    check(label, condition)

# ========== 5. 顾客问答场景覆盖测试 ==========
print('\n=== 5. 顾客问答场景覆盖测试 ===')

qa_scenarios = [
    ('你们几点开门？', ['10:00', '22:00'], '营业时间'),
    ('周末营业吗？', ['10:00', '22:00'], '营业时间'),
    ('发个定位给我', ['南昌', '青山湖区', '北京东路'], '地址导航'),
    ('坐地铁怎么过去？', ['高新', '地铁'], '地址导航'),
    ('WiFi密码多少？', ['eqs88888888'], 'WiFi'),
    ('需要预约吗？', ['无需预约'], '预约'),
    ('有哪些项目？多少钱？', ['服务时长', '适用人群', '明码标价'], '服务项目'),
    ('采耳会疼吗？', ['不', '可视', '专业'], 'FAQ'),
    ('有中耳炎能做吗？', ['到店', '检测'], 'FAQ'),
    ('孕期能做吗？', ['可以', '一般'], 'FAQ'),
    ('工具怎么消毒？', ['五步消毒', '一客一换', '独立包装'], 'FAQ'),
    ('老师有资质吗？', ['持证', '3年'], 'FAQ'),
    ('最近有什么活动？', ['送', '充值'], '优惠'),
    ('耳朵发炎了能做吗？', ['炎症', '检测'], 'FAQ'),
    ('做完需要注意什么？', ['24', '进水', '辛辣'], 'FAQ'),
    ('你们店开了多久了？', ['2023'], '品牌'),
    ('鼓膜穿孔能做吗？', ['评估', '技师'], '禁忌'),
    ('不舒服怎么办？', ['调整', '手法'], 'FAQ'),
    ('服务过程包括头部按摩吗？', ['专业采耳', '不包含', '头部'], 'FAQ'),
]

for q, must_contain, category in qa_scenarios:
    found = False
    for fname in os.listdir(REF_DIR):
        content = read_ref(fname)
        if all(kw in content for kw in must_contain):
            found = True
            break
    if not found and all(kw in sk for kw in must_contain):
        found = True
    check(f'[{category}] {q[:20]}...', found, f'需含: {must_contain}')

# ========== 6. 数据一致性交叉检查 ==========
print('\n=== 6. 数据一致性交叉检查 ===')
services = read_ref('services.md')
faq = read_ref('faq.md')
promo = read_ref('promotions.md')

# v1.1.0: 价格已改为到店了解，不再硬编码在 references 中
check('服务项目不含硬编码价格', '58' not in services and '98' not in services and '128' not in services)

for kw in ['鼓膜穿孔', '禁忌']:
    check(f'禁忌"{kw}"在services和faq中一致', kw in services and kw in faq)

check('faq安全评估逻辑', ('到店' in faq and '评估' in faq) or '未经检测' in faq)

# ========== 7. 版本管理检查 ==========
print('\n=== 7. 版本管理检查 ===')
version_path = os.path.join(SKILL_DIR, 'version.json')
check('version.json 存在', os.path.exists(version_path))
if os.path.exists(version_path):
    with open(version_path, encoding='utf-8') as f:
        ver = json.load(f)
    check('version.json 含 version 字段', 'version' in ver)
    check('version.json 含 skill 字段', 'skill' in ver)

check('Git 仓库已初始化', os.path.exists(os.path.join(SKILL_DIR, '.git', 'HEAD')))
check('CHANGELOG.md 存在', os.path.exists(os.path.join(SKILL_DIR, 'CHANGELOG.md')))

# ========== 结果汇总 ==========
total = results['pass'] + results['fail']
print(f'\n{"="*50}')
print(f'    测试结果汇总')
print(f'{"="*50}')
print(f'  通过: {results["pass"]}/{total}')
print(f'  失败: {results["fail"]}/{total}')
print(f'  通过率: {results["pass"]/total*100:.1f}%' if total > 0 else '  无结果')
print(f'{"="*50}')

print('\n'.join(results['checks']))

json_path = os.path.join(SKILL_DIR, 'dist', 'test-report.json')
os.makedirs(os.path.dirname(json_path), exist_ok=True)
with open(json_path, 'w', encoding='utf-8') as jf:
    json.dump({
        'passed': results['pass'],
        'failed': results['fail'],
        'total': total,
        'pass_rate': f'{results["pass"]/total*100:.1f}%' if total > 0 else 'N/A',
    }, jf, ensure_ascii=False, indent=2)
print(f'\nJSON report saved: {json_path}')

exit(0 if results['fail'] == 0 else 1)
