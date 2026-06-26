#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""深度审计：穷尽式检查医疗安全红线、结构完整性和数据一致性"""

import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
REF_DIR = os.path.join(SKILL_DIR, 'references')

def read(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

def ref(name):
    return os.path.join(REF_DIR, name)

sk = read(os.path.join(SKILL_DIR, 'SKILL.md'))
faq = read(ref('faq.md'))
svc = read(ref('services.md'))
promo = read(ref('promotions.md'))
biz = read(ref('business-info.md'))
brand = read(ref('brand.md'))

PASS = '✅'
FAIL = '❌'

results = []

def check(category, label, condition, detail=''):
    results.append((category, label, condition, detail))
    icon = PASS if condition else FAIL
    print(f'  {icon} [{"PASS" if condition else "FAIL"}] {label}')
    if detail and not condition:
        print(f'         → {detail}')

# ============================================================
# P0: 医疗安全红线
# ============================================================
print('\n=== P0: 医疗安全红线 ===')

check('P0', 'AI不得诊断(三步流程)', '三步流程' in sk)
check('P0', 'AI不得诊断(明确禁止)', '不得给出诊断结论' in sk)
check('P0', '鼓膜穿孔→就医', '就医' in sk)
check('P0', '紧急症状转诊(流脓)', '流脓' in sk)
check('P0', '紧急症状转诊(出血)', '出血' in sk)
check('P0', '紧急症状转诊(剧痛)', '剧痛' in sk)
check('P0', 'FAQ Q2引导到店检测', '到店' in faq and '检测' in faq)
check('P0', 'FAQ Q2含紧急就医提示', '就医' in faq)
check('P0', 'FAQ Q3有限定词', '一般情况下' in faq or '一般情况' in faq)
check('P0', 'FAQ Q7不引导自诊断', '如果' not in faq.split('### Q7:')[1].split('###')[0] if '### Q7:' in faq else True,
      'Q7 不应要求用户自我判断耳道健康状况')
check('P0', '禁忌表改为内部参考', '内部参考' in faq)
check('P0', '禁忌表标注AI不得直接使用', 'AI客服不得据此' in faq or 'AI处理规则' in faq)

# ============================================================
# P1: 数据结构完整性
# ============================================================
print('\n=== P1: 数据结构完整性 ===')

check('P1', 'business-info.md 含营业时间', '10:00' in biz and '22:00' in biz)
check('P1', 'business-info.md 含完整地址', '南昌' in biz and '青山湖区' in biz)
check('P1', 'business-info.md 含联系电话', '13361632122' in biz)
check('P1', 'business-info.md 含区号', '0791' in biz)
check('P1', 'business-info.md 含Wi-Fi', 'eqs' in biz)
check('P1', 'business-info.md 含地铁交通', '地铁' in biz)
check('P1', 'services.md 含4个项目', svc.count('### ') >= 4, f'当前{svc.count("### ")}个')
check('P1', 'services.md 含价格(58元)', '58 元' in svc)
check('P1', 'services.md 含价格(98元)', '98 元' in svc)
check('P1', 'services.md 含价格(128元)', '128 元' in svc)
check('P1', 'services.md 含禁忌说明', '禁忌' in svc)
check('P1', 'services.md 含消毒说明', '五步消毒法' in svc)
check('P1', 'promotions.md 含充值优惠', '充值' in promo)
check('P1', 'promotions.md 含预约规则', '预约' in promo)
check('P1', 'promotions.md 含取消规则', '取消' in promo)
check('P1', 'faq.md 含10个FAQ', len([l for l in faq.split('\n') if l.startswith('### Q')]) >= 10)
check('P1', 'faq.md 含安全须知', '禁忌与安全须知' in faq)
check('P1', 'brand.md 含成立时间', '2023' in brand)
check('P1', 'brand.md 含门店数量', '4家' in brand)

# ============================================================
# P2: 数据一致性
# ============================================================
print('\n=== P2: 数据一致性 ===')

check('P2', '价格58在services和faq一致', '58' in svc and '58' in faq)
check('P2', '价格98在services和faq一致', '98' in svc and '98' in faq)
check('P2', '价格128在services和faq一致', '128' in svc and '128' in faq)
check('P2', '鼓膜穿孔禁止一致', '鼓膜穿孔' in svc and '鼓膜穿孔' in faq)
check('P2', '五步消毒法一致', '五步消毒法' in svc and '五步消毒' in faq)
check('P2', '一客一换一致', '一客一换' in svc and '一客一换' in faq and '一客一换' in brand)
check('P2', '充值金额一致(300)', '300' in promo)
check('P2', '充值金额一致(500)', '500' in promo)
check('P2', '充值金额一致(1000)', '1000' in promo)

# ============================================================
# P3: 更新机制
# ============================================================
print('\n=== P3: 更新机制 ===')

check('P3', 'version.json 存在', os.path.exists(os.path.join(SKILL_DIR, 'version.json')))
check('P3', 'update_skill.py 存在', os.path.exists(os.path.join(SCRIPT_DIR, 'update_skill.py')))
check('P3', 'SKILL.md 无硬编码数据', '北京东路' not in sk)
check('P3', '数据文件独立可编辑', all(f.endswith('.md') for f in os.listdir(REF_DIR)))
check('P3', 'Git 仓库已初始化', os.path.exists(os.path.join(SKILL_DIR, '.git', 'HEAD')))
check('P3', 'auto_update.sh 存在', os.path.exists(os.path.join(SCRIPT_DIR, 'auto_update.sh')))
check('P3', 'GitHub Actions 工作流存在', os.path.exists(os.path.join(SKILL_DIR, '.github', 'workflows', 'release.yml')))

# ============================================================
# 汇总
# ============================================================
total = len(results)
passed = sum(1 for _, _, ok, _ in results if ok)
failed = total - passed
p0_failed = sum(1 for cat, _, ok, _ in results if cat == 'P0' and not ok)

print(f'\n{"="*55}')
print(f'  深度审计总结')
print(f'{"="*55}')
print(f'  总检查项: {total}')
print(f'  通过: {passed}')
print(f'  失败: {failed}')
if p0_failed > 0:
    print(f'  ⚠️  P0 医疗安全红线仍有 {p0_failed} 项未通过！')
print(f'  通过率: {passed/total*100:.0f}%' if total > 0 else '  无结果')
print(f'{"="*55}')

# 列出所有失败项
if failed > 0:
    print('\n失败项列表:')
    for cat, label, ok, detail in results:
        if not ok:
            print(f'  {FAIL} [{cat}] {label}')
            if detail:
                print(f'         {detail}')

exit(0 if failed == 0 else 1)
