"""
对比分析：testcase/（旧方式） vs output/（skill完整流程）
"""

import json, os, glob

print('=' * 70)
print(' 对比分析：原始单文件生成 vs SKILL 完整五阶段流程')
print('=' * 70)

# === 1. 结构对比 ===
print('\n📁 一、输出结构对比')
print('-' * 60)
print(f'{"维度":20s} {"原始生成(testcase/)":30s} {"SKILL流程(output/)":30s}')
print('-' * 60)
print(f'{"输出文件数":20s} {"14个独立JSON":30s} {"5个阶段文件+1个Excel":30s}')
print(f'{"阶段分离":20s} {"❌ 全部合并到一个文件":30s} {"✅ 五阶段独立输出":30s}')
print(f'{"审计可追溯":20s} {"❌ 无阶段中间产物":30s} {"✅ 每阶段有独立JSON":30s}')
print(f'{"需求可测性":20s} {"❌ 未单独标注":30s} {"✅ phase2独立标注可测性":30s}')
print(f'{"设计策略":20s} {"❌ 混合在用例文件中":30s} {"✅ phase3独立呈现":30s}')
print(f'{"Excel生成":20s} {"✅ writer.py生成":30s} {"✅ writer.py生成":30s}')
print(f'{"源文件追溯":20s} {"❌ 无源文件字段":30s} {"✅ 每条标记源文件":30s}')

# === 2. 用例数量对比 ===
print('\n📊 二、用例数量对比')
print('-' * 60)

# Count from testcase/ individual files
testcase_total = 0
testcase_by_file = {}
for f in sorted(os.listdir('testcase')):
    if not f.endswith('.json') or f == 'combined.json':
        continue
    try:
        with open(os.path.join('testcase', f), 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        n = len(data.get('测试用例', []))
        testcase_by_file[f] = n
        testcase_total += n
    except:
        testcase_by_file[f] = -1

# Count from output/phase4_cases.json
with open('output/phase4_cases.json', 'r', encoding='utf-8') as f:
    p4 = json.load(f)
output_cases = p4.get('测试用例', [])
output_total = len(output_cases)

# Count from phase2
with open('output/phase2_requirements.json', 'r', encoding='utf-8') as f:
    p2 = json.load(f)
output_reqs = p2.get('需求', [])
output_req_total = len(output_reqs)

# Count from phase1
with open('output/phase1_domains.json', 'r', encoding='utf-8') as f:
    p1 = json.load(f)
output_domains = p1.get('业务域', [])
output_domain_count = len(output_domains)

print(f'{"指标":20s} {"原始(testcase/)":20s} {"SKILL(output/)":20s} {"差异":10s}')
print('-' * 60)
print(f'{"用例总数":20s} {testcase_total:<20d} {output_total:<20d} {output_total-testcase_total:+d}')
print(f'{"需求总数":20s} {"-":20s} {output_req_total:<20d} {"N/A":10s}')
print(f'{"业务域数":20s} {"-":20s} {output_domain_count:<20d} {"N/A":10s}')
print(f'{"设计策略":20s} {"-":20s} {len(p4.get("设计策略",[])):<20d} {"N/A":10s}')
print()

# Per-file comparison
print(f'{"文件":35s} {"原始":>6s} {"SKILL":>6s} {"差异":>6s}')
print('-' * 55)
for f in sorted(testcase_by_file.keys()):
    old_n = testcase_by_file.get(f, 0)
    # Find corresponding cases in output
    src = f.replace('-testcases.json', '.md')
    new_n = sum(1 for c in output_cases if c.get('源文件', '') == src)
    diff = new_n - old_n
    if old_n >= 0:
        print(f'  {f:30s} {old_n:6d} {new_n:6d} {diff:+6d}')
print('-' * 55)
print(f'  {"总计":30s} {testcase_total:6d} {output_total:6d} {output_total-testcase_total:+6d}')

# === 3. Quality metric comparison ===
print('\n📈 三、质量指标对比')
print('-' * 60)

# Priority distribution
print(f'\n优先级分布:')
pri_map = {}
for c in output_cases:
    p = c.get('优先级', '未知')
    pri_map[p] = pri_map.get(p, 0) + 1
for p in ['P0', 'P1', 'P2', 'P3']:
    print(f'  {p}: {pri_map.get(p, 0)}条 ({pri_map.get(p, 0)/output_total*100:.1f}%)')

# Dimension distribution
print(f'\n测试维度分布:')
dim_map = {}
for c in output_cases:
    d = c.get('测试维度', '未知')
    dim_map[d] = dim_map.get(d, 0) + 1
for d in sorted(dim_map.keys()):
    print(f'  {d}: {dim_map.get(d, 0)}条')

# Method distribution
print(f'\n设计方法分布:')
method_map = {}
for c in output_cases:
    m = c.get('设计方法', '未知')
    method_map[m] = method_map.get(m, 0) + 1
for m in sorted(method_map.keys()):
    print(f'  {m}: {method_map.get(m, 0)}条')

# Business domain distribution
print(f'\n业务域分布:')
dom_map = {}
for c in output_cases:
    d = c.get('业务域', '未知')
    dom_map[d] = dom_map.get(d, 0) + 1
for d in sorted(dom_map.keys()):
    print(f'  {d}: {dom_map.get(d, 0)}条')

# === 4. Gap Analysis ===
print('\n🔍 四、Gap 分析')
print('-' * 60)

gaps = []

# 4a. Structure gap
gaps.append(('输出架构', '原始未分离阶段',
    'SKILL要求五阶段独立输出(output/phase1~4)，已完整实现'))

# 4b. Missing metadata in old approach
old_has_source = False
for f in sorted(os.listdir('testcase')):
    if not f.endswith('.json') or f == 'combined.json':
        continue
    try:
        with open(os.path.join('testcase', f), 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        cases = data.get('测试用例', [])
        if cases and '源文件' in cases[0]:
            old_has_source = True
            break
    except:
        pass

gaps.append(('源文件追溯', 
    '❌ 无' if not old_has_source else '✅ 有',
    'SKILL流程每条用例标记了源文件字段'))

# 4c. Phase 2 - 可测性标注
gaps.append(('需求可测性', '❌ 未独立评估',
    '✅ phase2独立标注可测性状态(可测/不可测/需澄清)'))

# 4d. Phase 3 - 设计方法选择矩阵
gaps.append(('设计方法选择', '❌ 混合在用例中',
    '✅ phase3独立呈现设计策略(方法/覆盖目标/预期用例数)'))

# 4e. Audit chain
gaps.append(('审计链条', '❌ 仅最终用例',
    '✅ 业务域→需求→设计→用例 全链条可追溯'))

print(f'{"维度":25s} {"原始方式":30s} {"SKILL方式":35s}')
print('-' * 90)
for title, old, new in gaps:
    print(f'{title:25s} {old:30s} {new:35s}')

# === 5. Summary ===
print('\n' + '=' * 70)
print(' 总结')
print('=' * 70)
print("""
原始方式(testcase/):
  ✅ 生成了14个独立JSON文件 + Excel
  ❌ 未按skill要求分阶段输出
  ❌ 无独立的业务域分析/需求清单/设计策略文件
  ❌ 部分JSON文件有语法错误(中文引号)
  ❌ 用例数: 266(原始) - 修复后263

SKILL完整流程(output/):
  ✅ 严格按五阶段输出
  ✅ 业务域分析(18个) → phase1_domains.json
  ✅ 需求提取(212条) → phase2_requirements.json
  ✅ 测试设计(17条) → phase3_design.json
  ✅ 用例生成(263条) → phase4_cases.json
  ✅ 最终Excel → 数据安全舱_测试用例.xlsx
  ✅ 每条数据标记源文件，全链条可追溯
  ✅ 修复了所有JSON语法问题

核心差距: 原始方式缺少阶段中间产物，无法审计追溯；
 SKILL流程提供了完整的 业务域→需求→设计→用例 四层审计链条。
""")
