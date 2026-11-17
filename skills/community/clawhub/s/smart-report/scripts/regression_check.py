#!/usr/bin/env python3
"""smart-report 开发者回归自测脚本。

端到端验证技能全链路（真实 CLI 子进程，非 mock）：
- 校验层：黑名单/AST 单元测试、transform 错误码契约、超时机制
- 解析层：CSV/TSV/TXT/JSON/GBK/Excel、脏表头 flags、多文件合并
- 渲染层：26 种图表（契约键 + HTML 落盘）
- 多图模式、flags/主题/语言/dry-run/annotation
- transform 黄金模式 + 沙箱逃逸 PoC 拦截
- 错误路径：结构化 JSON + suggestion
- 报告层：report_spec + 图表 HTML + ledger → 单文件 HTML 报告（report_assembler.py）
- 论点台账：claims.json 形式校验（论点必有论据 / 论据可解析 / 数字可溯源 / coverage 每图挂论点）

用法：python scripts/regression_check.py [技能根目录]（默认为脚本上级目录）
测试数据与输出写入 tempfile 临时目录，不污染技能目录；退出码 0=全过，1=有失败。
"""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path


BASE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
CLI = BASE / 'scripts' / 'cli.py'
DP = BASE / 'scripts' / 'data_parser.py'
ROOT = Path(tempfile.mkdtemp(prefix='sc_regression_'))
DATA = ROOT / 'data'
OUT = ROOT / 'out'
DATA.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BASE))
import pandas as pd
from scripts.data_transformer import DataTransformer, validate_code_blacklist, validate_code_ast
from scripts.exceptions import SmartChartsError, ErrorCode
from scripts.data_parser import DataParser

PASS, FAIL = 0, 0
FAILURES = []

def rec(name, ok, detail=''):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"[PASS] {name}")
    else:
        FAIL += 1
        FAILURES.append((name, detail))
        print(f"[FAIL] {name}  -- {detail}")

def run_cli(args, timeout=90):
    t0 = time.time()
    proc = subprocess.run([sys.executable, str(CLI)] + [str(a) for a in args],
                          capture_output=True, text=True, timeout=timeout)
    dt = time.time() - t0
    out = None
    if proc.stdout.strip():
        try:
            out = json.loads(proc.stdout)
        except json.JSONDecodeError:
            out = None
    return proc.returncode, out, proc.stderr, dt

def run_dp(args, timeout=60):
    proc = subprocess.run([sys.executable, str(DP)] + [str(a) for a in args],
                          capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr

# ══════════════════ 数据准备 ══════════════════
(DATA / 'cities.csv').write_text(
    "城市,销售额,利润,人口万\n北京,1200,300,2189\n上海,1500,400,2487\n广州,900,180,1874\n深圳,1100,260,1768\n", encoding='utf-8')
(DATA / 'trend.csv').write_text(
    "月份,销售额,利润\n1月,1000,250\n2月,1150,280\n3月,1300,320\n4月,1280,310\n5月,1420,360\n6月,1550,390\n", encoding='utf-8')
(DATA / 'freq.csv').write_text(
    "类别\nA\nB\nA\nC\nA\nB\nC\nD\nA\nB\n\nC\n", encoding='utf-8')
(DATA / 'students.csv').write_text(
    "姓名,数学,语文,英语\n张三,85,78,92\n李四,92,88,95\n王五,60,72,68\n赵六,75,80,77\n钱七,88,85,90\n孙八,45,60,55\n周九,95,93,97\n吴十,70,68,74\n", encoding='utf-8')
(DATA / 'radar.csv').write_text(
    "指标,产品A,产品B\n性能,90,75\n易用性,85,80\n功能,70,92\n价格,60,85\n服务,80,70\n", encoding='utf-8')
(DATA / 'heat.csv').write_text(
    "星期,早高峰,午高峰,晚高峰\n周一,320,280,410\n周二,340,275,420\n周三,335,290,435\n周四,350,285,425\n周五,380,300,470\n", encoding='utf-8')
(DATA / 'graph.csv').write_text(
    "source,target,value\nA,B,5\nA,C,3\nB,D,2\nC,D,4\nD,E,1\n", encoding='utf-8')
(DATA / 'relation.csv').write_text(
    "来源,去向,金额\n总部,华北分部,500\n总部,华南分部,400\n华北分部,北京办,200\n", encoding='utf-8')
(DATA / 'funnel.csv').write_text(
    "阶段,人数\n浏览,10000\n加购,3000\n下单,1200\n支付,900\n复购,300\n", encoding='utf-8')
(DATA / 'words.csv').write_text(
    "关键词,频次\n数据,120\n分析,95\n可视化,88\n模型,76\n图表,70\n统计,60\n", encoding='utf-8')
(DATA / 'venn.csv').write_text(
    "name,value\n仅A,40\n仅B,25\nA∩B,15\n", encoding='utf-8')
(DATA / 'org.csv').write_text(
    "parent,child\n根,分支A\n根,分支B\n分支A,叶子1\n分支A,叶子2\n分支B,叶子3\n", encoding='utf-8')
(DATA / 'gauge.csv').write_text(
    "完成率\n78.5\n82.3\n75.0\n79.9\n", encoding='utf-8')
(DATA / 'scatter_xy.csv').write_text(
    "x_val,y_val\n10,20\n15,30\n20,40\n25,50\n", encoding='utf-8')
(DATA / 'waterfall.csv').write_text(
    "month,profit\n1月,100\n2月,120\n3月,90\n4月,110\n5月,130\n", encoding='utf-8')
(DATA / 'pareto.csv').write_text(
    "类别,数量\nA,45\nB,30\nC,15\nD,6\nE,4\n", encoding='utf-8')
(DATA / 'special.csv').write_text(
    "销售额(元),A/B\n100,5\n200,8\n150,6\n", encoding='utf-8')
(DATA / 'messy.csv').write_text(
    "这是一份导出说明\n导出时间:2026-01-01\n城市,销售额\n北京,120\n上海,180\n广州,150\n", encoding='utf-8')
(DATA / 'ffill.csv').write_text(
    "部门,经理,工资\n技术部,张三,12000\n,,11500\n市场部,李四,10000\n,,9800\n", encoding='utf-8')
(DATA / 'en.csv').write_text(
    "city,revenue,profit\nNYC,1000,250\nLA,850,180\nChicago,720,150\n", encoding='utf-8')
(DATA / 'nested.json').write_text(
    json.dumps([{"城市": "北京", "销售额": 100, "详情": {"区域": "华北"}},
                {"城市": "上海", "销售额": 150, "详情": {"区域": "华东"}}], ensure_ascii=False), encoding='utf-8')
(DATA / 'students.tsv').write_text(
    "姓名\t数学\t语文\n张三\t85\t78\n李四\t92\t88\n", encoding='utf-8')
(DATA / 'scores.txt').write_text(
    "姓名;数学\n张三;85\n李四;92\n", encoding='utf-8')
(DATA / 'm1.csv').write_text("城市,销售额\n北京,100\n上海,200\n", encoding='utf-8')
(DATA / 'sales_long.csv').write_text("month,region,revenue\n1月,east,200\n1月,north,150\n2月,east,220\n2月,north,160\n3月,east,250\n3月,north,170\n", encoding='utf-8')
(DATA / 'm2.csv').write_text("城市,销售额\n广州,150\n深圳,180\n", encoding='utf-8')
(DATA / 'm3.csv').write_text("A,B\n1,2\n3,4\n", encoding='utf-8')
# GBK 编码
(DATA / 'gbk.csv').write_bytes("城市,销售额\n北京,1200\n上海,1500\n".encode('gbk'))
# Excel（openpyxl 可用时）
HAS_XLSX = False
try:
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active; ws.title = '数据'
    ws.append(['城市', '销售额', '利润'])
    for r in [('北京', 1200, 300), ('上海', 1500, 400), ('广州', 900, 180)]: ws.append(list(r))
    ws2 = wb.create_sheet('脏表')
    ws2.append(['学生信息表（导出）'])
    ws2.append(['编号', '姓名', '数学', '语文'])
    for r in [('001', '张三', 85, 78), ('002', '李四', 92, 88)]: ws2.append(list(r))
    wb.save(DATA / 'book.xlsx')
    HAS_XLSX = True
except ImportError:
    print("!! openpyxl 不可用，Excel 用例跳过")

# ══════════════════ U: 校验层单元测试 ══════════════════
print("\n─── U1: 逃逸 PoC（黑名单层）───")
POCS = {
    'pd.__builtins__ 直达': "result = pd.__builtins__",
    '__getattribute__ 取 eval': "result = pd.__getattribute__('eval')",
    '__getattr__ 变体': "result = pd.__getattr__('open')",
    '__loader__ 导入机': "x = np.__loader__; result = df",
    '__spec__': "x = pd.__spec__; result = df",
    '__self__': "x = (df.sum).__self__; result = df",
    '__func__': "x = (df.sum).__func__; result = df",
    '__reduce__ 反序列化': "x = df.__reduce__; result = df",
    '旧黑名单项仍拦截(eval)': "result = eval('1')",
    '旧黑名单项仍拦截(import)': "import os",
    '旧黑名单项仍拦截(open)': "result = open('/tmp/sc_poctest')",
}
df_u = pd.DataFrame({'类别': ['A', 'B', 'A'], '数值': [1, 2, 3]})
for name, code in POCS.items():
    v = validate_code_blacklist(code)
    rec(f"U1-黑名单拦截: {name}", bool(v), f"未被拦截: {code!r}")

print("\n─── U2: 逃逸 PoC（transform() 全路径）───")
for name, code in POCS.items():
    try:
        DataTransformer().transform(df_u, code)
        rec(f"U2-transform拒绝: {name}", False, "未被拒绝，代码被执行")
    except SmartChartsError as e:
        rec(f"U2-transform拒绝: {name}", e.code == ErrorCode.TRANSFORM_EXEC_ERROR,
            f"错误码不符: {e.code}")

print("\n─── U3: 黄金模式零误报（黑名单 + AST）───")
GOLDEN = {
    '频次聚合': "result = df['类别'].fillna('未标注').value_counts().rename_axis('name').reset_index(name='value')",
    '分组聚合': "result = df.groupby('类别')['数值'].sum().rename_axis('name').reset_index(name='value')",
    '透视': "result = df.pivot_table(index='类别', columns='类别', values='数值', aggfunc='sum').reset_index()",
    'melt': "result = df.melt(id_vars=['类别'], var_name='name', value_name='value')",
    'rename': "result = df.rename(columns={'类别': 'name', '数值': 'value'})",
    'ffill': "result = df.ffill()",
    'waterfall-diff': "tmp = df.copy(); tmp['d'] = tmp['数值'].diff().fillna(tmp['数值'].iloc[0]); result = tmp[['类别', 'd']]",
    'np.select': "result = df.assign(等级=np.select([df['数值'] > 2, df['数值'] > 1], ['高', '中'], default='低'))",
    '布尔向量位运算': "result = df[(df['数值'] > 1) & (df['类别'] == 'A')]",
    '推导式+lambda': "result = df.assign(k=[x * 2 for x in df['数值']]).assign(f=lambda t: t['数值'].map(lambda v: v + 1))",
}
for name, code in GOLDEN.items():
    v = validate_code_blacklist(code) + validate_code_ast(code)
    rec(f"U3-黄金零误报: {name}", not v, f"误报: {v}")

print("\n─── U4: transform() 正常执行返回 DataFrame ───")
for name, code in GOLDEN.items():
    try:
        r = DataTransformer().transform(df_u, code)
        rec(f"U4-transform执行: {name}", isinstance(r, pd.DataFrame) and not r.empty,
            f"返回异常: {type(r)}")
    except Exception as e:
        rec(f"U4-transform执行: {name}", False, f"异常: {e}")

print("\n─── U5: transform 错误码契约 ───")
ERR_CASES = {
    '无 result 变量(3002)': ("x = 1", ErrorCode.TRANSFORM_NO_RESULT),
    'result 非 DataFrame(3003)': ("result = 42", ErrorCode.TRANSFORM_INVALID_RESULT),
    'result 为空(3004)': ("result = df.iloc[0:0]", ErrorCode.TRANSFORM_EMPTY_RESULT),
    'AST违规-类定义(3001)': ("class Foo:\n    pass", ErrorCode.TRANSFORM_EXEC_ERROR),
    'AST违规-try(3001)': ("try:\n    x = 1\nexcept:\n    pass", ErrorCode.TRANSFORM_EXEC_ERROR),
    '语法错误(3001)': ("def broken(", ErrorCode.TRANSFORM_EXEC_ERROR),
}
for name, (code, expect) in ERR_CASES.items():
    try:
        DataTransformer().transform(df_u, code)
        rec(f"U5-错误码: {name}", False, "未抛错")
    except SmartChartsError as e:
        rec(f"U5-错误码: {name}", e.code == expect, f"期望 {expect.name} 实得 {e.code.name}")

print("\n─── U6: 超时机制（while True，10s）───")
t0 = time.time()
try:
    DataTransformer().transform(df_u, "while True:\n    x = 1")
    rec("U6-超时拦截", False, "未超时")
except SmartChartsError as e:
    rec("U6-超时拦截", e.code == ErrorCode.TRANSFORM_EXEC_ERROR and '超时' in e.message,
        f"{e.code.name}: {e.message}")

# ══════════════════ P: 数据解析层 ══════════════════
print("\n─── P1: 各格式解析 ───")
PARSE_CASES = {
    'CSV': 'cities.csv', 'TSV': 'students.tsv', 'TXT(分号)': 'scores.txt',
    'JSON(嵌套1层)': 'nested.json', 'GBK编码': 'gbk.csv',
}
for name, f in PARSE_CASES.items():
    try:
        df = DataParser().parse_file(DATA / f)
        rec(f"P1-解析: {name}", not df.empty, "空 DataFrame")
    except Exception as e:
        rec(f"P1-解析: {name}", False, str(e)[:120])

try:
    df = DataParser().parse_file(DATA / 'nested.json')
    rec("P1-JSON嵌套列名规范化", '详情_区域' in df.columns, f"列: {list(df.columns)}")
except Exception as e:
    rec("P1-JSON嵌套列名规范化", False, str(e)[:120])

df_sp = DataParser().parse_file(DATA / 'special.csv')
rec("P1-特殊字符列规范化(销售额(元)→销售额_元)", '销售额_元' in df_sp.columns, f"列: {list(df_sp.columns)}")
rec("P1-特殊字符列规范化(A/B→a_b)", 'a_b' in df_sp.columns, f"列: {list(df_sp.columns)}")

try:
    df_m = DataParser().parse_file(DATA / 'messy.csv', skiprows=2)
    rec("P1-skiprows脏表头", list(df_m.columns) == ['城市', '销售额'] and len(df_m) == 3,
        f"列: {list(df_m.columns)}, 行数: {len(df_m)}")
except Exception as e:
    rec("P1-skiprows脏表头", False, str(e)[:120])

if HAS_XLSX:
    try:
        df_s1 = DataParser().parse_file(DATA / 'book.xlsx', sheet_name='数据')
        rec("P1-Excel按名称选sheet", len(df_s1) == 3, f"行数: {len(df_s1)}")
    except Exception as e:
        rec("P1-Excel按名称选sheet", False, str(e)[:120])
    try:
        df_s2 = DataParser().parse_file(DATA / 'book.xlsx', sheet_name='脏表', header_row=1)
        rec("P1-Excel脏表header-row", list(df_s2.columns) == ['编号', '姓名', '数学', '语文'],
            f"列: {list(df_s2.columns)}")
    except Exception as e:
        rec("P1-Excel脏表header-row", False, str(e)[:120])
    try:
        DataParser().parse_file(DATA / 'book.xlsx', sheet_name='不存在的表')
        rec("P1-Excel错误sheet结构化报错", False, "未报错")
    except SmartChartsError as e:
        rec("P1-Excel错误sheet结构化报错", e.code == ErrorCode.DATA_PARSE_ERROR, f"{e.code.name}")

rc, so, se = run_dp([DATA / 'm1.csv', DATA / 'm2.csv', '--merge', '--summary'])
rec("P2-多文件纵向合并", rc == 0 and 'source_file' in so, f"rc={rc}, out={so[:150]}")
rc, so, se = run_dp([DATA / 'm1.csv', DATA / 'm3.csv', '--merge', '--summary'])
rec("P2-无重叠合并报错", rc != 0 and 'DATA_MERGE_ERROR' in (so + se), f"rc={rc}")

# ══════════════════ C: 26 种图表端到端 ══════════════════
print("\n─── C: 26 种图表（成功 + 契约键 + HTML 落盘）───")
CHARTS = [
    ('line', 'trend.csv', ['--x-axis', '月份', '--y-axis', '销售额', '利润']),
    ('bar', 'cities.csv', ['--x-axis', '城市', '--y-axis', '销售额']),
    ('area', 'trend.csv', ['--x-axis', '月份', '--y-axis', '销售额']),
    ('pie', 'freq.csv', ['--x-axis', 'name', '--y-axis', 'value',
     '--transform-code', "result = df['类别'].fillna('未标注').value_counts().rename_axis('name').reset_index(name='value')"]),
    ('scatter', 'students.csv', ['--x-axis', '数学', '--y-axis', '语文', '--label-col', '姓名']),
    ('radar', 'radar.csv', ['--x-axis', '指标', '--y-axis', '产品a', '产品b']),
    ('heatmap', 'heat.csv', ['--x-axis', '星期', '--y-axis', '早高峰', '午高峰', '晚高峰']),
    ('treemap', 'words.csv', ['--x-axis', '关键词', '--y-axis', '频次']),
    ('graph', 'graph.csv', []),
    ('boxplot', 'students.csv', ['--y-axis', '数学', '语文', '英语']),
    ('waterfall', 'waterfall.csv', ['--x-axis', 'month', '--y-axis', 'profit']),
    ('gauge', 'gauge.csv', ['--y-axis', '完成率']),
    ('sankey', 'relation.csv',
     ['--transform-code', "result = df.rename(columns={'来源': 'source', '去向': 'target', '金额': 'value'})"]),
    ('funnel', 'funnel.csv', ['--x-axis', '阶段', '--y-axis', '人数']),
    ('sunburst', 'words.csv', ['--x-axis', '关键词', '--y-axis', '频次']),
    ('wordcloud', 'words.csv', ['--x-axis', '关键词', '--y-axis', '频次']),
    ('histogram', 'students.csv', ['--x-axis', '数学']),
    ('stacked_bar', 'cities.csv', ['--x-axis', '城市', '--y-axis', '销售额', '利润']),
    ('bubble', 'cities.csv', ['--x-axis', '销售额', '--y-axis', '利润', '人口万']),
    ('pareto', 'pareto.csv', ['--x-axis', '类别', '--y-axis', '数量']),
    ('combo', 'cities.csv', ['--x-axis', '城市', '--y-axis', '销售额', '利润']),
    ('venn', 'venn.csv', ['--x-axis', 'name', '--y-axis', 'value']),
    ('mindmap', 'org.csv', ['--x-axis', 'parent', '--y-axis', 'child']),
    ('orgchart', 'org.csv', ['--x-axis', 'parent', '--y-axis', 'child']),
    ('liquid', 'gauge.csv', ['--y-axis', '完成率']),
    ('spreadsheet', 'students.csv', []),
]
CONTRACT_KEYS = {'success', 'html_path', 'chart_type', 'title', 'data_rows', 'data_preview', 'plot_stats'}
for ctype, fname, extra in CHARTS:
    rc, out, se, dt = run_cli([DATA / fname, ctype, '--title', f'{ctype}回归测试', *extra])
    name = f"C-{ctype:12s} ({fname})"
    if rc != 0 or not out or not out.get('chart', {}).get('success'):
        rec(name, False, f"rc={rc} stdout={(json.dumps(out, ensure_ascii=False)[:200] if out else 'None')} stderr={se[:200]}")
        continue
    c = out['chart']
    missing = CONTRACT_KEYS - set(c.keys())
    html_ok = c['html_path'] and Path(c['html_path']).exists() and Path(c['html_path']).stat().st_size > 1024
    rec(name, not missing and html_ok,
        f"缺契约键: {missing or '无'}, html: {c['html_path']}")

# ══════════════════ T: transform 黄金模式端到端 ══════════════════
print("\n─── T: transform 黄金模式（CLI 端到端）───")
# groupby
rc, out, se, _ = run_cli([DATA / 'm1.csv', 'bar', '--title', 'T1',
    '--transform-code', "result = df.groupby('城市')['销售额'].sum().rename_axis('name').reset_index(name='value')",
    '--x-axis', 'name', '--y-axis', 'value'])
rec("T1-groupby聚合→bar", rc == 0 and out and out['chart']['success'],
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")
# pivot_table 多系列
rc, out, se, _ = run_cli([DATA / 'sales_long.csv', 'line', '--title', 'T2',
    '--transform-code', "result = df.pivot_table(index='month', columns='region', values='revenue', aggfunc='sum').reset_index()",
    '--x-axis', 'month', '--y-axis', 'east', 'north'])
rec("T2-pivot_table多系列→line", rc == 0 and out and out['chart']['success'],
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")
# ffill 多语句
rc, out, se, _ = run_cli([DATA / 'ffill.csv', 'pie', '--title', 'T3',
    '--transform-code', "tmp = df.ffill(); result = tmp['部门'].value_counts().rename_axis('name').reset_index(name='value')",
    '--x-axis', 'name', '--y-axis', 'value'])
rec("T3-ffill多语句→pie", rc == 0 and out and out['chart']['success'],
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")
# waterfall diff 模式
rc, out, se, _ = run_cli([DATA / 'waterfall.csv', 'waterfall', '--title', 'T4',
    '--transform-code', "tmp = df.copy(); tmp['delta'] = tmp['profit'].diff().fillna(tmp['profit'].iloc[0]); result = tmp[['month', 'delta']]",
    '--x-axis', 'month', '--y-axis', 'delta'])
rec("T4-waterfall-diff模式", rc == 0 and out and out['chart']['success'],
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")
# np.select
rc, out, se, _ = run_cli([DATA / 'students.csv', 'bar', '--title', 'T5',
    '--transform-code', "result = df.assign(等级=np.select([df['数学'] > 90, df['数学'] > 60], ['优', '中'], default='及格边缘'))",
    '--x-axis', '等级', '--y-axis', '数学'])
rec("T5-np.select→bar", rc == 0 and out and out['chart']['success'],
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")
# rename + graph 自动检测
rc, out, se, _ = run_cli([DATA / 'relation.csv', 'graph', '--title', 'T6',
    '--transform-code', "result = df.rename(columns={'来源': 'source', '去向': 'target', '金额': 'value'})"])
rec("T6-rename→graph自动检测", rc == 0 and out and out['chart']['success'],
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")
# 特殊字符列（规范化后引用）
rc, out, se, _ = run_cli([DATA / 'special.csv', 'bar', '--title', 'T7',
    '--x-axis', '销售额_元', '--y-axis', 'a_b'])
rec("T7-特殊字符列规范化引用", rc == 0 and out and out['chart']['success'],
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")
# skiprows + transform
rc, out, se, _ = run_cli([DATA / 'messy.csv', 'bar', '--title', 'T8', '--skiprows', '2',
    '--transform-code', "result = df.assign(销售额=df['销售额'].map(lambda v: v * 2))",
    '--x-axis', '城市', '--y-axis', '销售额'])
rec("T8-skiprows+transform", rc == 0 and out and out['chart']['success'],
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")

# CLI 层逃逸拦截（结构化错误 + suggestion）
rc, out, se, _ = run_cli([DATA / 'm1.csv', 'bar', '--title', 'T9',
    '--transform-code', "result = pd.__builtins__ and df", '--x-axis', '城市', '--y-axis', '销售额'])
ok = rc == 1 and out and not out['chart']['success'] \
     and out['chart']['error']['code_name'] == 'TRANSFORM_EXEC_ERROR' \
     and '__builtins__' in out['chart']['error']['details'].get('violations', []) \
     and 'suggestion' in out['chart']['error']['details']
rec("T9-CLI逃逸拦截(__builtins__)", ok, f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:300] if out else se[:300]}")

# ══════════════════ M: 多图模式 ══════════════════
print("\n─── M: 多图模式 ───")
charts_cfg = [
    {"type": "bar", "title": "M1柱状", "x_axis": "城市", "y_axis": ["销售额"]},
    {"type": "line", "title": "M1折线", "x_axis": "月份", "y_axis": ["销售额", "利润"]},
    {"type": "pie", "title": "M1饼图", "transform_code": "result = df['类别'].fillna('未标注').value_counts().rename_axis('name').reset_index(name='value')", "x_axis": "name", "y_axis": ["value"]},
]
cfg_path = ROOT / 'charts.json'
cfg_path.write_text(json.dumps(charts_cfg, ensure_ascii=False), encoding='utf-8')
# freq.csv 无 月份 列 → line 会失败？用 cities+专用文件不行（单文件）。改用 trend.csv？
# pie 需要 频次列。折衷：用 freq.csv 时 line 失败属预期 → 换 cities.csv，pie 用利润分箱。
charts_cfg = [
    {"type": "bar", "title": "M柱状", "x_axis": "城市", "y_axis": ["销售额"]},
    {"type": "combo", "title": "M组合", "x_axis": "城市", "y_axis": ["销售额", "利润"]},
    {"type": "scatter", "title": "M散点", "x_axis": "销售额", "y_axis": ["利润"]},
]
cfg_path.write_text(json.dumps(charts_cfg, ensure_ascii=False), encoding='utf-8')
rc, out, se, _ = run_cli([DATA / 'cities.csv', '--charts-file', cfg_path])
ok = rc == 0 and out and out.get('summary', {}).get('total') == 3 and out['summary']['succeeded'] == 3 \
     and all(c.get('success') and Path(c['html_path']).exists() for c in out['charts'])
rec("M1-charts-file多图(3张全成功)", ok,
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:300] if out else se[:300]}")

# 全局 transform + 单图级 transform
rc, out, se, _ = run_cli([DATA / 'students.csv', '--charts-file', cfg_path, '--transform-code', 'result = df.copy()'])
# students.csv 无 城市 列 → 全失败。改用 cities.csv
rc, out, se, _ = run_cli([DATA / 'cities.csv', '--charts-file', cfg_path,
    '--transform-code', "result = df.assign(销售额=df['销售额'].map(lambda v: v / 10))"])
ok = rc == 0 and out and out['summary']['succeeded'] == 3
rec("M2-全局transform多图", ok, f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")

# 部分失败（exit 0 + summary 正确）
cfg_part = [
    {"type": "bar", "title": "好图", "x_axis": "城市", "y_axis": ["销售额"]},
    {"type": "bar", "title": "坏图", "x_axis": "不存在的列", "y_axis": ["销售额"]},
]
(ROOT / 'part.json').write_text(json.dumps(cfg_part, ensure_ascii=False), encoding='utf-8')
rc, out, se, _ = run_cli([DATA / 'cities.csv', '--charts-file', ROOT / 'part.json'])
ok = rc == 0 and out and out['summary'] == {'total': 2, 'succeeded': 1, 'failed': 1} \
     and out['charts'][0]['success'] and not out['charts'][1]['success'] \
     and 'suggestion' in out['charts'][1]['error']['details']
rec("M3-部分失败(exit 0 + per-chart错误)", ok, f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:300] if out else se[:300]}")

# 内联 --charts
rc, out, se, _ = run_cli([DATA / 'cities.csv', '--charts', '[{"type":"bar","x_axis":"城市","y_axis":["销售额"]}]'])
rec("M4-内联--charts", rc == 0 and out and out['summary']['succeeded'] == 1,
    f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")

# 非法 --charts
rc, out, se, _ = run_cli([DATA / 'cities.csv', '--charts', '[{"x_axis":"城市"}]'])
rec("M5-非法charts(缺type)结构化报错", rc == 1 and 'CHART_CONFIG_ERROR' in se, f"rc={rc}, se={se[:150]}")

# 多图 dry-run
rc, out, se, _ = run_cli([DATA / 'cities.csv', '--charts-file', cfg_path, '--dry-run'])
ok = rc == 0 and out and all(c['success'] and c.get('dry_run') and c['html_path'] is None
                             for c in out['charts'])
rec("M6-多图dry-run(不落盘)", ok, f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:250] if out else se[:250]}")

# ══════════════════ F: flags / 主题 / 语言 ══════════════════
print("\n─── F: flags / 主题 / 语言 / dry-run / annotation ───")
for theme in ('default', 'classic', 'dark'):
    rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', f'主题{theme}',
                              '--x-axis', '城市', '--y-axis', '销售额', '--theme', theme])
    rec(f"F1-主题: {theme}", rc == 0 and out and out['chart']['success'], f"rc={rc}")

rc, out, se, _ = run_cli([DATA / 'en.csv', 'bar', '--title', 'Revenue by City',
                          '--x-axis', 'city', '--y-axis', 'revenue', '--lang', 'en'])
rec("F2-lang=en(英文数据)", rc == 0 and out and out['chart']['success'], f"rc={rc}")
rc, out, se, _ = run_cli([DATA / 'en.csv', 'bar', '--title', '城市营收', '--lang', 'zh',
                          '--x-axis', 'city', '--y-axis', 'revenue'])
rec("F3-lang=zh(覆盖自动检测)", rc == 0 and out and out['chart']['success'], f"rc={rc}")

rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'F4', '--dry-run',
                          '--x-axis', '城市', '--y-axis', '销售额'])
c = out.get('chart', {}) if out else {}
ok = rc == 0 and c.get('dry_run') is True and c.get('html_path') is None and 'plot_stats' in c
rec("F4-dry-run(html_path=null+plot_stats)", ok, json.dumps(out, ensure_ascii=False)[:200] if out else se[:200])

ANNOT = '回归测试注解：上海以 1500 领先四城。'
SUB = '2026年Q1 · 数据来源：测试套件'
rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'F5注解',
                          '--x-axis', '城市', '--y-axis', '销售额',
                          '--annotation', ANNOT, '--subtitle', SUB])
ok = rc == 0 and out and out['chart']['success']
if ok:
    html = Path(out['chart']['html_path']).read_text(encoding='utf-8')
    ok = ANNOT in html and SUB in html
rec("F5-annotation+subtitle注入HTML", ok, f"rc={rc}")

import re as _re
rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'F6', '--sort', 'value',
                          '--x-axis', '城市', '--y-axis', '销售额'])
ok = rc == 0 and out and out['chart']['success']
if ok:
    html_v = Path(out['chart']['html_path']).read_text(encoding='utf-8')
    # sort 在渲染层生效（data_preview 是渲染前数据，原序属预期）；
    # 断言 xAxis data 数组首元素为最大值城市「上海」
    m = _re.search(r'"data":\s*\[\s*"[^"]+"', html_v)
    ok = m is not None and m.group(0).rstrip().endswith('"上海"')
    # 对照组：sort=none 时首元素应为原序首城市「北京」且两份 HTML 不同
    rc2, out2, _, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'F6', '--sort', 'none',
                               '--x-axis', '城市', '--y-axis', '销售额'])
    if ok and rc2 == 0 and out2:
        html_n = Path(out2['chart']['html_path']).read_text(encoding='utf-8')
        m2 = _re.search(r'"data":\s*\[\s*"[^"]+"', html_n)
        ok = m2 is not None and m2.group(0).rstrip().endswith('"北京"') and html_v != html_n
rec("F6-sort=value渲染层降序", ok, f"rc={rc}")

rc, out, se, _ = run_cli([DATA / 'trend.csv', 'line', '--title', 'F7', '--y-scale',
                          '--x-axis', '月份', '--y-axis', '销售额'])
rec("F7-y-scale(line)", rc == 0 and out and out['chart']['success'], f"rc={rc}")
for lab in ('all', 'key'):
    rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', f'F8-{lab}', '--label', lab,
                              '--x-axis', '城市', '--y-axis', '销售额'])
    rec(f"F8-label={lab}", rc == 0 and out and out['chart']['success'], f"rc={rc}")

rc, out, se, _ = run_cli([DATA / 'students.csv', 'scatter', '--title', 'F9',
                          '--x-axis', '数学', '--y-axis', '语文', '--label-col', '姓名', '--color-by', '英语'])
rec("F9-scatter label-col+color-by(数值)", rc == 0 and out and out['chart']['success'], f"rc={rc}")
rc, out, se, _ = run_cli([DATA / 'cities.csv', 'scatter', '--title', 'F10',
                          '--x-axis', '销售额', '--y-axis', '利润', '--color-by', '城市'])
rec("F10-scatter color-by(类别)", rc == 0 and out and out['chart']['success'], f"rc={rc}")

rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'F11',
                          '--x-axis', '城市', '--y-axis', '销售额', '--width', '1200', '--height', '800'])
rec("F11-width/height", rc == 0 and out and out['chart']['success'], f"rc={rc}")

# 离线性：HTML 不引用外部 CDN
rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'F12', '--x-axis', '城市', '--y-axis', '销售额'])
ok = rc == 0 and out and out['chart']['success']
if ok:
    html = Path(out['chart']['html_path']).read_text(encoding='utf-8')
    ok = 'echarts' in html.lower() and 'src="http' not in html and 'href="http' not in html
    sz = len(html)
rec("F12-离线HTML(echarts内联无CDN)", ok, f"size={sz if ok else 'N/A'}")

# stdout 纯 JSON 契约（单行可解析已在 run_cli 验证；这里显式确认 stderr 无泄漏）
rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'F13', '--x-axis', '城市', '--y-axis', '销售额'])
rec("F13-stdout纯JSON契约", rc == 0 and out is not None and out.get('chart', {}).get('success'),
    f"stdout解析失败或 stderr 泄漏: {se[:150]}")

# ══════════════════ E: 错误路径 ══════════════════
print("\n─── E: 错误路径（结构化 JSON + suggestion）───")
rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar3d', '--title', 'E1', '--x-axis', '城市', '--y-axis', '销售额'])
ok = rc == 1 and out and not out['chart']['success'] and out['chart']['error']['code_name'] == 'CHART_TYPE_UNSUPPORTED'
rec("E1-不支持的图表类型(4002)", ok, f"rc={rc}")

rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'E2', '--x-axis', '不存在的列', '--y-axis', '销售额'])
ok = rc == 1 and out and not out['chart']['success'] and out['chart']['error']['code_name'] == 'CHART_CONFIG_ERROR'
rec("E2-轴字段缺失(4003)", ok, f"rc={rc}")

rc, out, se, _ = run_cli(['/tmp/不存在.csv', 'bar'])
ok = rc == 1 and 'FILE_NOT_FOUND' in se
rec("E3-文件不存在(1001,stderr)", ok, f"rc={rc}, se={se[:120]}")

(DATA / 'scores.xyz').write_text('姓名,数学\n张三,85\n', encoding='utf-8')
rc, out, se, _ = run_cli([DATA / 'scores.xyz', 'bar'])
ok = rc == 1 and 'FILE_FORMAT_INVALID' in se
rec("E4-不支持扩展名(1003)", ok, f"rc={rc}, se={se[:120]}")

rc, out, se, _ = run_cli([DATA / 'cities.csv'])
ok = rc == 1 and 'CHART_CONFIG_ERROR' in se
rec("E5-缺图表类型(4003)", ok, f"rc={rc}, se={se[:120]}")

rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--nope'])
ok = rc == 1 and 'CHART_CONFIG_ERROR' in se and 'suggestion' in se
rec("E6-未知flag(argparse→结构化JSON)", ok, f"rc={rc}, se={se[:150]}")

rc, out, se, _ = run_cli([DATA / 'cities.csv', '--charts-file', '/tmp/不存在.json'])
ok = rc == 1 and 'FILE_NOT_FOUND' in se
rec("E7-charts-file缺失(1001)", ok, f"rc={rc}, se={se[:120]}")

# E8: 5 个逃逸 PoC 经 CLI（覆盖 dunder 新增项）
for kw, code in [('__builtins__', "result = pd.__builtins__"),
                 ('__getattribute__', "x = pd.__getattribute__; result = df"),
                 ('__loader__', "x = np.__loader__; result = df"),
                 ('__reduce__', "x = df.__reduce__; result = df"),
                 ('__spec__', "x = pd.__spec__; result = df")]:
    rc, out, se, _ = run_cli([DATA / 'm1.csv', 'bar', '--title', 'E8', '--transform-code', code,
                              '--x-axis', '城市', '--y-axis', '销售额'])
    ok = rc == 1 and out and not out['chart']['success'] \
         and out['chart']['error']['code_name'] == 'TRANSFORM_EXEC_ERROR' \
         and kw in out['chart']['error']['details'].get('violations', [])
    rec(f"E8-CLI逃逸拦截: {kw}", ok, f"rc={rc}")

# E9: P1-1 嵌套模块路径逃逸（此前 133 项全绿但真实可落盘/可出网）
for kw, code in [('open_memmap', "x = np.lib.format.open_memmap('/tmp/sc_probe_e9.npy', mode='w+', dtype='float64', shape=(2,)); result = df"),
                 ('get_handle', "h = pd.io.common.get_handle('/tmp/sc_probe_e9.txt', mode='w'); result = df"),
                 ('pd.io(网络)', "h = pd.io.common.get_handle('http://127.0.0.1:9/x.csv', mode='r'); result = df")]:
    v = validate_code_blacklist(code) + validate_code_ast(code)
    rec(f"E9-嵌套路径逃逸拦截: {kw}", bool(v), f"未被拦截: {code[:60]}")
    try:
        DataTransformer().transform(df_u, code)
        rec(f"E9-transform拒绝: {kw}", False, "代码被执行")
    except SmartChartsError as e:
        rec(f"E9-transform拒绝: {kw}", e.code == ErrorCode.TRANSFORM_EXEC_ERROR, f"{e.code.name}")
# 落盘取证：确认探针文件确实没有被创建
rec("E9-探针文件未落盘",
    not os.path.exists('/tmp/sc_probe_e9.npy') and not os.path.exists('/tmp/sc_probe_e9.txt'),
    "逃逸代码真实创建了文件")

# ══════════════════ X: P0/P1/P2 修复项回归 ══════════════════
print("\n─── X: 问题清单修复项（P0/P1/P2）───")

# ── P0-1: frontmatter 必须只含平台允许键 ──
_fm = _re.match(r'^---\n(.*?)\n---', (BASE / 'SKILL.md').read_text(encoding='utf-8'), _re.DOTALL)
try:
    import yaml as _yaml
    _keys = set(_yaml.safe_load(_fm.group(1)).keys())
except ImportError:
    _keys = set(_re.findall(r'^([a-z-]+):', _fm.group(1), _re.M))
# smart-report 的 frontmatter 键集（与 smart-charts 不同：多 display_name/display_name_en/description_en）
_ALLOWED = {'name', 'version', 'display_name', 'display_name_en', 'description', 'description_en'}
rec("P0-1-frontmatter无非法键", not (_keys - _ALLOWED), f"非法键: {_keys - _ALLOWED}")
rec("P0-1-SKILL.md含激活触发段",
    'Activation Triggers' in (BASE / 'SKILL.md').read_text(encoding='utf-8'),
    "SKILL.md 缺 Activation Triggers 边界段")

# ── P0-2: exec 单一命名空间（中间变量 + lambda/生成器/嵌套 def）──
# df_u 的列为 类别 / 数值，引用必须用真实列名
for _n, _code in [('lambda引用中间变量', "k = 2; result = df.assign(v2=lambda d: d['数值']*k)"),
                  ('生成器引用中间变量', "thr = 2; result = df.assign(f=list(v > thr for v in df['数值']))"),
                  ('apply引用标量', "s = 10; result = df[['数值']].apply(lambda c: c*s)"),
                  ('嵌套def引用中间变量', "m = 3\ndef f(x):\n    return x*m\nresult = df.assign(v3=df['数值'].map(f))")]:
    try:
        _r = DataTransformer().transform(df_u, _code)
        rec(f"P0-2-单一命名空间: {_n}", isinstance(_r, pd.DataFrame) and not _r.empty, f"{type(_r)}")
    except Exception as _e:
        rec(f"P0-2-单一命名空间: {_n}", False, f"{type(_e).__name__}: {_e}")

# ── P0-3: 合计行排除 + summary 补 tail/warning ──
(DATA / 'total.csv').write_text(
    "月份,销量\n1月,10\n2月,20\n3月,30\n4月,40\n5月,50\n6月,60\n合计,210\n", encoding='utf-8')
_p = DataParser()
_df_t = _p.parse_file(DATA / 'total.csv')
rec("P0-3-合计行已排除", len(_df_t) == 6 and int(_df_t['销量'].sum()) == 210,
    f"rows={len(_df_t)}, sum={_df_t['销量'].sum()}")
_sum_t = _p.get_data_summary(_df_t)
rec("P0-3-summary补tail", 'tail' in _sum_t, f"keys={list(_sum_t)}")
rec("P0-3-summary补warning", bool(_sum_t.get('warnings')), f"warnings={_sum_t.get('warnings')}")
rec("P0-3-极值不再报成合计值", _sum_t['stats']['销量']['max'] == 60.0,
    f"max={_sum_t['stats']['销量']['max']}")
rc, out, se, _ = run_cli([DATA / 'total.csv', 'bar', '--title', 'X-P0-3',
                          '--x-axis', '月份', '--y-axis', '销量'])
rec("P0-3-CLI输出合计行advisory",
    rc == 0 and out and out['chart']['success']
    and any('合计' in a for a in out['chart'].get('advisories', [])),
    f"advisories={out['chart'].get('advisories') if out else se[:150]}")

# ── P0-4: 趋势按自然序 + 零基线不可计算 ──
from scripts.plot_stats import compute_plot_stats as _cps
_b = pd.DataFrame({'月份': ['1月', '2月', '3月', '4月'], '销量': [100, 120, 140, 160]})
_t_up = _cps(_b, 'line', '月份', ['销量'])['series'][0]['trend']
_t_rev = _cps(_b.iloc[::-1].reset_index(drop=True), 'line', '月份', ['销量'])['series'][0]['trend']
_t_shf = _cps(_b.iloc[[2, 0, 3, 1]].reset_index(drop=True), 'line', '月份', ['销量'])['series'][0]['trend']
rec("P0-4-三种行序结论一致",
    _t_up['delta_pct'] == _t_rev['delta_pct'] == _t_shf['delta_pct'] == 60.0,
    f"{_t_up} / {_t_rev} / {_t_shf}")
_z = _cps(pd.DataFrame({'m': ['a', 'b'], 'v': [0, 5000]}), 'line', 'm', ['v'])['series'][0]['trend']
rec("P0-4-零基线不报持平", _z['direction'] == 'undefined' and _z['delta_pct'] is None, f"{_z}")
_m = _cps(pd.DataFrame({'m': ['1月', '2月', '10月', '12月'], 'v': [10, 20, 30, 40]}),
          'line', 'm', ['v'])['series'][0]['trend']
rec("P0-4-月份按时间序非字典序", _m['first'] == 10.0 and _m['last'] == 40.0, f"{_m}")

# ── P0-5: 列名撞名消歧 + UNKNOWN_ERROR 带 suggestion ──
for _cols in (['Sales Amount', 'sales-amount'], ['营收($)', '营收'], ['Score', 'score'], ['A/B', 'A B']):
    _dd = pd.DataFrame({c: [1, 2] for c in _cols})
    try:
        _o = DataParser()._clean(_dd.copy())
        rec(f"P0-5-撞名消歧: {_cols}", len(set(_o.columns)) == len(_o.columns)
            and all(hasattr(_o[c], 'dtype') for c in _o.columns), f"列: {list(_o.columns)}")
    except Exception as _e:
        rec(f"P0-5-撞名消歧: {_cols}", False, f"{type(_e).__name__}: {_e}")
# 真正跑一遍 UNKNOWN_ERROR 兜底分支：注入一个非 SmartChartsError 异常，
# 捕获 stderr 上的结构化 JSON，断言 details 里有 suggestion
import io as _io
import contextlib as _ctx
import scripts.cli as _cli_mod

def _run_injected_failure(entry, argv):
    """把 parse_file 换成必炸的实现，跑真实入口，返回解析后的错误 JSON。"""
    _orig = DataParser.parse_file
    def _boom(*_a, **_k):
        raise RuntimeError("injected-for-regression")
    DataParser.parse_file = _boom
    _buf = _io.StringIO()
    try:
        with _ctx.redirect_stderr(_buf):
            try:
                entry(argv) if argv is not None else entry()
            except SystemExit:
                pass
    finally:
        DataParser.parse_file = _orig
    try:
        return json.loads(_buf.getvalue().strip().splitlines()[-1])
    except Exception:
        return {}

_err = _run_injected_failure(_cli_mod.main, [str(DATA / 'cities.csv'), 'bar',
                                             '--x-axis', '城市', '--y-axis', '销售额'])
rec("P0-5-cli兜底UNKNOWN_ERROR带suggestion",
    _err.get('code_name') == 'UNKNOWN_ERROR' and 'suggestion' in _err.get('details', {}),
    f"{_err}")
import scripts.data_parser as _dp_mod
_argv0 = sys.argv
sys.argv = ['data_parser.py', str(DATA / 'cities.csv'), '--summary']
try:
    _err2 = _run_injected_failure(_dp_mod._run_cli, None)
finally:
    sys.argv = _argv0
rec("P0-5-data_parser兜底UNKNOWN_ERROR带suggestion",
    _err2.get('code_name') == 'UNKNOWN_ERROR' and 'suggestion' in _err2.get('details', {}),
    f"{_err2}")

# ── P0-6: f-string 放行 ──
_f = "result = df.rename(columns={c: f'{c}_score' for c in df.columns})"
rec("P0-6-f-string通过校验", not (validate_code_blacklist(_f) + validate_code_ast(_f)),
    f"{validate_code_blacklist(_f) + validate_code_ast(_f)}")
try:
    _r = DataTransformer().transform(df_u, _f)
    rec("P0-6-f-string可执行", list(_r.columns) == ['类别_score', '数值_score'], f"{list(_r.columns)}")
except Exception as _e:
    rec("P0-6-f-string可执行", False, str(_e))

# ── P1-2: 粒度对账三元组 ──
rc, out, se, _ = run_cli([DATA / 'freq.csv', 'bar', '--title', 'X-P1-2', '--x-axis', 'name', '--y-axis', 'value',
                          '--transform-code',
                          "result = df['类别'].fillna('未标注').value_counts().rename_axis('name').reset_index(name='value')"])
_c = out['chart'] if out else {}
rec("P1-2-输出source_rows/plotted_rows/unique_entities",
    rc == 0 and {'source_rows', 'plotted_rows', 'unique_entities'} <= set(_c),
    f"keys={sorted(_c)}")
# freq.csv 共 12 个数据行，其中 1 行为空 —— 解析层 _clean 先丢空行，
# 故 source_rows=11；transform 聚合成 4 个类别，plotted_rows=unique_entities=4
rec("P1-2-对账三元组数值正确",
    _c.get('source_rows') == 11 and _c.get('plotted_rows') == 4 and _c.get('unique_entities') == 4,
    f"source={_c.get('source_rows')}, plotted={_c.get('plotted_rows')}, uniq={_c.get('unique_entities')}")
rec("P1-2-三元组可判定漏去重",
    _c.get('plotted_rows', 0) < _c.get('source_rows', 0)
    and sum(r['value'] for r in _c.get('data_preview', [])) == _c.get('source_rows')
    and _c.get('unique_entities') == _c.get('plotted_rows'),
    f"三元组无法支撑去重校验: {_c.get('source_rows')}/{_c.get('plotted_rows')}/{_c.get('unique_entities')}")

# ── P1-5: annotation_source ──
rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'X-P1-5',
                          '--x-axis', '城市', '--y-axis', '销售额'])
rec("P1-5-默认annotation标记default",
    rc == 0 and out['chart'].get('annotation_source') == 'default'
    and any('annotation' in a for a in out['chart'].get('advisories', [])),
    f"{out['chart'].get('annotation_source') if out else se[:150]}")
rc, out, se, _ = run_cli([DATA / 'cities.csv', 'bar', '--title', 'X-P1-5b',
                          '--x-axis', '城市', '--y-axis', '销售额', '--annotation', ANNOT])
rec("P1-5-用户annotation标记user",
    rc == 0 and out['chart'].get('annotation_source') == 'user'
    and 'annotation_source' not in ' '.join(out['chart'].get('advisories', [])),
    f"{out['chart'].get('annotation_source') if out else se[:150]}")

# ── P1-7: gauge --target ──
rc, out, se, _ = run_cli([DATA / 'gauge.csv', 'gauge', '--title', 'X-P1-7', '--y-axis', '完成率'])
_g = out['chart']['plot_stats']['extra'] if out else {}
rec("P1-7-无target时achievement为null",
    rc == 0 and _g.get('achievement') is None and 'achievement_note' in _g, f"{_g}")
rec("P1-7-无target时挂advisory",
    any('target' in a or '达成率' in a for a in out['chart'].get('advisories', [])),
    f"{out['chart'].get('advisories')}")
rc, out, se, _ = run_cli([DATA / 'gauge.csv', 'gauge', '--title', 'X-P1-7b', '--y-axis', '完成率',
                          '--target', '100'])
_g2 = out['chart']['plot_stats']['extra'] if out else {}
rec("P1-7-有target时achievement=mean/target",
    rc == 0 and _g2.get('target') == 100.0
    and abs(_g2.get('achievement', 0) - round(_g2['mean'] / 100, 4)) < 1e-9, f"{_g2}")

# ── P1-8: 依赖区间 + --doctor ──
_req = (BASE / 'requirements.txt').read_text(encoding='utf-8')
rec("P1-8-requirements改用兼容区间",
    'pandas>=' in _req and 'pandas==' not in _req and 'numpy>=' in _req,
    f"{_req[:80]}")
_proc = subprocess.run([sys.executable, str(CLI), '--doctor'], capture_output=True, text=True, timeout=60)
try:
    _doc = json.loads(_proc.stdout)
    rec("P1-8---doctor输出版本矩阵",
        _proc.returncode == 0 and 'dependencies' in _doc and 'assets' in _doc
        and len(_doc['dependencies']) == 4,
        f"rc={_proc.returncode}, out={_proc.stdout[:150]}")
except Exception as _e:
    rec("P1-8---doctor输出版本矩阵", False, f"{_e}: {_proc.stdout[:150]}{_proc.stderr[:150]}")

# ── P1-13: 文档硬约束要求显式 --output-dir ──
_skm = (BASE / 'SKILL.md').read_text(encoding='utf-8')
rec("P1-13-文档要求显式指定--output-dir",
    'MUST 显式传 `--output-dir`' in _skm, "SKILL.md 缺该硬约束")

# ── P2-2: 文档声明 skiprows 与 header-row 等价 ──
_refm = (BASE / 'references' / 'REFERENCE.md').read_text(encoding='utf-8')
rec("P2-2-文档声明两个flag等价",
    'same operation' in _refm or '同一' in _refm, "REFERENCE.md 未说明二者等价")

# ── P2-9: 'id' 词边界锚定 ──
from scripts.chart_generator import ChartGenerator as _CG
_df_lbl = pd.DataFrame({'width': [1], 'valid': [2], 'paid': [3], 'android': [4],
                        '学生_id': ['张三'], '数学': [90]})
_det = _CG._detect_label_col(_CG(output_dir=str(OUT)), _df_lbl, '数学', ['width'])
rec("P2-9-id子串不再误命中", _det == '学生_id', f"实际选中: {_det}")

# ── P2-12: data_points 语义改为 x 去重数 ──
_long = pd.DataFrame({'month': [f'{i}月' for i in range(1, 13)] * 5,
                      'series': [s for _ in range(12) for s in 'abcde'], 'v': range(60)})
_dp = _CG(output_dir=str(OUT))._estimate_data_points(_long, 'bar', 'month', ['v'])
rec("P2-12-data_points取nunique", _dp == 12, f"实得 {_dp}（期望 12，旧实现为 60）")

# ── P2-13: advisories 触发点扩容 ──
# 修复前全代码库只有 1 处触发（饼图 >8 类）。现有 5 处：
#   饼图>8 / gauge-liquid 缺 target / annotation 用默认模板 / 合计行排除 / 数值列部分降级
_trig = sum(
    (BASE / 'scripts' / f).read_text(encoding='utf-8').count('.append(')
    for f in ('chart_generator.py', 'data_parser.py')
)
_n_adv = sum(
    (BASE / 'scripts' / f).read_text(encoding='utf-8').count('advisories.append')
    + (BASE / 'scripts' / f).read_text(encoding='utf-8').count('merged.append')
    for f in ('chart_generator.py', 'data_parser.py')
)
rec("P2-13-advisories触发点扩容(1→5)", _n_adv >= 5, f"advisory 追加点仅 {_n_adv} 处")
# 端到端：一次调用同时命中 3 类 advisory（合计行 + 数值降级 + 默认 annotation）
(DATA / 'multi_adv.csv').write_text(
    "月份,销量\n1月,10\n2月,20\n3月,-\n合计,30\n", encoding='utf-8')
rc, out, se, _ = run_cli([DATA / 'multi_adv.csv', 'bar', '--title', 'X-P2-13',
                          '--x-axis', '月份', '--y-axis', '销量'])
_advs = out['chart'].get('advisories', []) if out else []
rec("P2-13-单次调用命中多类advisory",
    rc == 0 and sum(1 for a in _advs if '合计' in a)
    + sum(1 for a in _advs if '数值' in a or '单元格' in a)
    + sum(1 for a in _advs if 'annotation' in a) >= 3,
    f"advisories={_advs}")

# ══════════════════ 独立命名：--x-name/--y-name/--series-name/--series-names ══════════════════
def _chart_seg(args):
    """运行 CLI 并返回 HTML 里 `var chartOption = ` 之后的片段（失败返回 None）。"""
    rc, out, se, _ = run_cli(args)
    if rc != 0 or not out or not out.get('chart', {}).get('html_path'):
        return None, out, se
    html = Path(out['chart']['html_path']).read_text(encoding='utf-8')
    return html.split('var chartOption = ', 1)[1], out, se

# 1. A 类 line：x 轴名 / y 轴名 / 系列名三者独立覆盖
_seg, out, _ = _chart_seg([DATA / 'cities.csv', 'line', '--x-axis', '城市', '--y-axis', '销售额',
                           '--x-name', '城市名', '--y-name', '营收', '--series-name', '月营收'])
rec("命名-1-line三者独立覆盖", _seg is not None and '"text": "城市名"' in _seg
    and '"text": "营收"' in _seg and '"name": "月营收"' in _seg)

# 2. 无参数回退：系列名=列名
_seg, out, _ = _chart_seg([DATA / 'cities.csv', 'line', '--x-axis', '城市', '--y-axis', '销售额'])
rec("命名-2-无参数回退列名", _seg is not None and '"name": "销售额"' in _seg)

# 3. B 类 heatmap 硬编码「热力图」可覆盖
_seg, out, _ = _chart_seg([DATA / 'heat.csv', 'heatmap', '--x-axis', '星期', '--y-axis', '早高峰', '午高峰',
                           '--series-name', '客流热力'])
rec("命名-3-heatmap硬编码可覆盖", _seg is not None and '"name": "客流热力"' in _seg
    and '"name": "热力图"' not in _seg)

# 4. B 类 gauge 硬编码「仪表盘」可覆盖（data.name 的完成率不影响断言）
_seg, out, _ = _chart_seg([DATA / 'gauge.csv', 'gauge', '--y-axis', '完成率',
                           '--series-name', '季度达成'])
rec("命名-4-gauge硬编码可覆盖", _seg is not None and '"name": "季度达成"' in _seg
    and '"name": "仪表盘"' not in _seg)

# 5. waterfall 跳过隐藏底座，覆盖主柱
_seg, out, _ = _chart_seg([DATA / 'waterfall.csv', 'waterfall', '--x-axis', 'month', '--y-axis', 'profit',
                           '--series-name', '净利润'])
rec("命名-5-waterfall跳过底座", _seg is not None and '__waterfall_base__' in _seg
    and '"name": "净利润"' in _seg and '"name": "profit"' not in _seg)

# 6. combo 多系列 --series-names
_seg, out, _ = _chart_seg([DATA / 'cities.csv', 'combo', '--x-axis', '城市', '--y-axis', '销售额', '利润',
                           '--series-names', '营收额', '利润额'])
rec("命名-6-combo多系列", _seg is not None and '"name": "营收额"' in _seg and '"name": "利润额"' in _seg)

# 7. boxplot 双系列（箱线图+异常值）--series-names
_seg, out, _ = _chart_seg([DATA / 'students.csv', 'boxplot', '--y-axis', '数学', '语文',
                           '--series-names', '主科成绩', '离群点'])
rec("命名-7-boxplot双系列", _seg is not None and '"name": "主科成绩"' in _seg
    and '"name": "离群点"' in _seg and '"name": "箱线图"' not in _seg and '"name": "异常值"' not in _seg)

# 8. --series-name 单数覆盖第一个系列
_seg, out, _ = _chart_seg([DATA / 'cities.csv', 'bar', '--x-axis', '城市', '--y-axis', '销售额',
                           '--series-name', '总销售额'])
rec("命名-8-单数覆盖第一系列", _seg is not None and '"name": "总销售额"' in _seg)

# 9. 无轴名 graphic 的图（heatmap）传 --x-name 不崩、正常成功
rc, out, se, _ = run_cli([DATA / 'heat.csv', 'heatmap', '--x-axis', '星期', '--y-axis', '早高峰',
                          '--x-name', '周期'])
rec("命名-9-无轴名图传x-name不崩", rc == 0 and out and out['chart']['success'])

# 10. 多图 --charts-file 透传 series_name
_cfg = ROOT / 'names_charts.json'
_cfg.write_text(json.dumps([{"type": "gauge", "title": "A", "y_axis": ["完成率"], "series_name": "达成率"}],
                           ensure_ascii=False), encoding='utf-8')
rc, out, se, _ = run_cli([DATA / 'gauge.csv', '--charts-file', _cfg])
_html = Path(out['charts'][0]['html_path']).read_text(encoding='utf-8') if (rc == 0 and out and out.get('charts')) else ''
rec("命名-10-多图透传series_name", rc == 0 and '"name": "达成率"' in _html and '"name": "仪表盘"' not in _html)

# 11. liquid（水波图）系列名可改 + label 第二行跟随系列名（不再写死列名）
_seg, out, _ = _chart_seg([DATA / 'gauge.csv', 'liquid', '--y-axis', '完成率',
                           '--series-name', '季度达成'])
rec("命名-11-liquid系列名可覆盖", _seg is not None and '"name": "季度达成"' in _seg
    and 'chartOption.series[0].name' in _seg and '"name": "水波图"' not in _seg)

# 12. liquid max>100 时渲染百分比 = mean/target（与 achievement 同源，不再用 gauge_scale(max) 当分母）
(DATA / 'liquid_over100.csv').write_text(
    "完成率\n72\n85\n93\n88\n96\n104\n", encoding='utf-8')
_seg, out, _ = _chart_seg([DATA / 'liquid_over100.csv', 'liquid', '--y-axis', '完成率', '--target', '100'])
rec("liquid-max100渲染值=mean/target", _seg is not None and '0.8967' in _seg and '0.8211' not in _seg)

# 13. liquid 无 target 时回落到 gauge_scale（max≤100 → 100，均值/100 不变）
_seg, out, _ = _chart_seg([DATA / 'gauge.csv', 'liquid', '--y-axis', '完成率'])
rec("liquid-无target回落gauge_scale", _seg is not None and '0.789' in _seg)

# 14. gauge data[0].name 跟随系列名（不再残留英文列名，tooltip 显示友好名）
_seg, out, _ = _chart_seg([DATA / 'gauge.csv', 'gauge', '--y-axis', '完成率', '--series-name', '季度达成'])
rec("命名-14-gauge数据项名跟随系列", _seg is not None and '"name": "季度达成"' in _seg
    and '"name": "完成率"' not in _seg)

# 15. radar series.name 与 data[0].name 同源（--series-names 后 tooltip 不再残留列名）
_seg, out, _ = _chart_seg([DATA / 'radar.csv', 'radar', '--x-axis', '指标', '--y-axis', '产品a', '产品b',
                           '--series-names', '产品甲', '产品乙'])
rec("命名-15-radar数据项名跟随系列", _seg is not None and '"name": "产品甲"' in _seg
    and '"name": "产品乙"' in _seg and '"name": "产品a"' not in _seg and '"name": "产品b"' not in _seg)

# 16. scatter tooltip 维度名跟随 --x-name/--y-name（不再残留英文列名）
_seg, out, _ = _chart_seg([DATA / 'scatter_xy.csv', 'scatter', '--x-axis', 'x_val', '--y-axis', 'y_val',
                           '--x-name', '自变量', '--y-name', '因变量'])
rec("命名-16-scatter维度名跟随轴名", _seg is not None
    and '["自变量", "因变量"]' in _seg and '["x_val", "y_val"]' not in _seg)

# ══════════════════ R: 报告层（report_assembler.py 全链路）══════════════════
print("\n─── R: 报告组装（spec → charts → ledger → HTML）───")
_RA = BASE / 'scripts' / 'report_assembler.py'
# 先生成 2 张图（bar + line）到显式目录
_rchart_dir = OUT / 'rcharts'
_r_cfg = [
    {"type": "bar", "title": "R1-城市销售额", "x_axis": "城市", "y_axis": ["销售额"],
     "annotation": "本图展示 4 座城市的销售额对比，上海 1500 居首、广州 900 垫底。"},
    {"type": "line", "title": "R2-城市销售额与利润", "x_axis": "城市", "y_axis": ["销售额", "利润"],
     "annotation": "本图并列展示销售额与利润两条系列。"},
]
(ROOT / 'r_cfg.json').write_text(json.dumps(_r_cfg, ensure_ascii=False), encoding='utf-8')
rc, out, se, _ = run_cli([DATA / 'cities.csv', '--charts-file', ROOT / 'r_cfg.json',
                          '--output-dir', str(_rchart_dir)])
if rc != 0 or not out or out.get('summary', {}).get('succeeded') != 2:
    rec("R1-批量生成2图", False, f"rc={rc}, {json.dumps(out, ensure_ascii=False)[:200] if out else se[:200]}")
else:
    rec("R1-批量生成2图", True)
    _html_paths = {c['title']: c['html_path'] for c in out['charts']}
    # 写 ledger.json（scan 模式，向后兼容）
    (ROOT / 'ledger.json').write_text(json.dumps([
        {"id": "sh", "metric": "上海销售额", "value": 1500, "unit": "万元",
         "source": "R1-城市销售额.plot_stats.series.0.max", "sections": ["s1"]},
        {"id": "gz", "metric": "广州销售额", "value": 900, "unit": "万元",
         "source": "R1-城市销售额.plot_stats.series.0.min", "sections": ["summary"]},
    ], ensure_ascii=False), encoding='utf-8')
    # 写 report_spec.json（2 节，数字全部可溯）
    _spec = {
        "title": "城市销售额对比 1500 万元居首",
        "subtitle": "2026 年 Q1 · 数据来源：回归测试套件",
        "theme": "default",
        "executive_summary": "上海以 1500 万元销售额居首，广州 900 万元垫底。",
        "sections": [
            {"id": "s1", "title": "上海销售额 1500 万元居首",
             "narrative": "四城中上海销售额最高。", "chart_path": _html_paths['R1-城市销售额'].split('/')[-1],
             "annotation": "本图展示 4 座城市的销售额对比。"},
            {"id": "s2", "title": "销售额与利润并排对比",
             "narrative": "销售额与利润走势一致。", "chart_path": _html_paths['R2-城市销售额与利润'].split('/')[-1],
             "annotation": "本图并列展示两条系列。"},
        ],
        "appendix": {"methodology": "数据来自回归测试套件 cities.csv。", "caveats": "仅 4 城样本。"},
    }
    (ROOT / 'report_spec.json').write_text(json.dumps(_spec, ensure_ascii=False), encoding='utf-8')
    # 组装（scan 模式 + 仅 html）
    _out_html = ROOT / 'report.html'
    _proc = subprocess.run([sys.executable, str(_RA), '--spec', str(ROOT / 'report_spec.json'),
                            '--charts-dir', str(_rchart_dir), '--output', str(_out_html),
                            '--ledger', str(ROOT / 'ledger.json')],
                           capture_output=True, text=True, timeout=120)
    _rok = False
    _parsed = {}
    if _proc.stdout.strip():
        try:
            _parsed = json.loads(_proc.stdout)
        except json.JSONDecodeError:
            _parsed = {}
    if _proc.returncode == 0 and _parsed.get('report', {}).get('success'):
        _rp = _parsed['report'].get('report_path')
        if _rp and Path(_rp).is_file() and Path(_rp).stat().st_size > 1024:
            _rok = True
            rec("R2-report_assembler组装HTML(scan模式)", True)
        else:
            rec("R2-report_assembler组装HTML(scan模式)", False, f"report_path 缺失或过小: {_rp}")
    else:
        rec("R2-report_assembler组装HTML(scan模式)", False,
            f"rc={_proc.returncode}, stdout={_proc.stdout[:200]}, stderr={_proc.stderr[:200]}")
    if _rok:
        _led = _parsed['report'].get('ledger') or {}
        rec("R3-台账校验通过(scan,misses=0)",
            _led.get('checked') and _led.get('misses') == 0, f"{_led}")

    # ── R4~R10：论点台账（claims.json）形式校验 ──
    def run_ra(extra_args, out_name='report_claims.html', timeout=120):
        _proc = subprocess.run([sys.executable, str(_RA),
                                '--spec', str(ROOT / 'report_spec.json'),
                                '--charts-dir', str(_rchart_dir),
                                '--output', str(ROOT / out_name)] + [str(a) for a in extra_args],
                               capture_output=True, text=True, timeout=timeout)
        _parsed_out = {}
        if _proc.stdout.strip():
            try:
                _parsed_out = json.loads(_proc.stdout)
            except json.JSONDecodeError:
                _parsed_out = {}
        return _proc.returncode, _parsed_out, _proc.stderr

    def parse_err(stderr_text):
        try:
            return json.loads(stderr_text.strip().splitlines()[-1])
        except Exception:
            return {}

    _claims_ok = [
        {"id": "c1", "claim": "上海销售额 1500 万元居首", "evidence": ["sh", "s1"],
         "section": "s1", "type": "结论"},
        {"id": "c2", "claim": "广州销售额 900 万元垫底", "evidence": ["gz", "s2"],
         "section": "s2", "type": "发现"},
    ]
    (ROOT / 'claims.json').write_text(json.dumps(_claims_ok, ensure_ascii=False), encoding='utf-8')

    # R4: basic 校验通过 + stdout claims 统计 + HTML 论点与论据附录
    rc4, out4, se4 = run_ra(['--ledger', str(ROOT / 'ledger.json'),
                             '--claims', str(ROOT / 'claims.json')])
    _c4 = out4.get('report', {}).get('claims') if rc4 == 0 else None
    _html4 = ''
    if _c4 and out4.get('report', {}).get('report_path'):
        _html4 = Path(out4['report']['report_path']).read_text(encoding='utf-8')
    rec("R4-claims basic校验通过",
        rc4 == 0 and _c4 and _c4.get('checked') and _c4.get('claims') == 2
        and _c4.get('evidence_refs') == 4 and '论点与论据' in _html4
        and 'id="claims-appendix"' in _html4,
        f"rc={rc4}, claims={_c4}, stderr={se4[:150]}")

    # R5: 论点缺 evidence → 5008
    (ROOT / 'claims_bad1.json').write_text(json.dumps(
        [{"id": "c1", "claim": "上海居首", "evidence": []}], ensure_ascii=False), encoding='utf-8')
    rc5, _, se5 = run_ra(['--ledger', str(ROOT / 'ledger.json'),
                         '--claims', str(ROOT / 'claims_bad1.json')], 'report_bad1.html')
    _e5 = parse_err(se5)
    rec("R5-论点缺论据报5008",
        rc5 == 1 and _e5.get('code') == 5008
        and _e5.get('code_name') == 'CLAIM_EVIDENCE_INVALID'
        and _e5.get('details', {}).get('violations', [{}])[0].get('problem') == 'missing_evidence',
        f"rc={rc5}, err={se5[:250]}")

    # R6: evidence 不可解析 → 5008
    (ROOT / 'claims_bad2.json').write_text(json.dumps(
        [{"id": "c1", "claim": "上海居首", "evidence": ["nope"]}], ensure_ascii=False), encoding='utf-8')
    rc6, _, se6 = run_ra(['--ledger', str(ROOT / 'ledger.json'),
                         '--claims', str(ROOT / 'claims_bad2.json')], 'report_bad2.html')
    _e6 = parse_err(se6)
    rec("R6-论据不可解析报5008",
        rc6 == 1 and _e6.get('code') == 5008
        and _e6.get('details', {}).get('violations', [{}])[0].get('problem') == 'unknown_evidence',
        f"rc={rc6}, err={se6[:250]}")

    # R7: 论点文本数字未入事实台账 → 5008
    (ROOT / 'claims_bad3.json').write_text(json.dumps(
        [{"id": "c1", "claim": "上海销售额 9999 万元居首", "evidence": ["sh", "s1"]}],
        ensure_ascii=False), encoding='utf-8')
    rc7, _, se7 = run_ra(['--ledger', str(ROOT / 'ledger.json'),
                         '--claims', str(ROOT / 'claims_bad3.json')], 'report_bad3.html')
    _e7 = parse_err(se7)
    rec("R7-论点数字未溯源报5008",
        rc7 == 1 and _e7.get('code') == 5008
        and _e7.get('details', {}).get('violations', [{}])[0].get('problem') == 'untraced_number',
        f"rc={rc7}, err={se7[:250]}")

    # R8: coverage 模式下含图章节未被论点引用 → 5008
    (ROOT / 'claims_bad4.json').write_text(json.dumps(
        [_claims_ok[0]], ensure_ascii=False), encoding='utf-8')  # 只覆盖 s1，s2 未覆盖
    rc8, _, se8 = run_ra(['--ledger', str(ROOT / 'ledger.json'),
                          '--claims', str(ROOT / 'claims_bad4.json'),
                          '--claims-check', 'coverage'], 'report_bad4.html')
    _e8 = parse_err(se8)
    rec("R8-coverage图未挂论点报5008",
        rc8 == 1 and _e8.get('code') == 5008
        and _e8.get('details', {}).get('violations', [{}])[0].get('problem') == 'uncovered_chart',
        f"rc={rc8}, err={se8[:250]}")

    # R9: coverage 全覆盖 → 通过 + 统计正确
    rc9, out9, se9 = run_ra(['--ledger', str(ROOT / 'ledger.json'),
                            '--claims', str(ROOT / 'claims.json'),
                            '--claims-check', 'coverage'], 'report_cov.html')
    _c9 = out9.get('report', {}).get('claims') if rc9 == 0 else None
    rec("R9-coverage全覆盖通过",
        rc9 == 0 and _c9 and _c9.get('mode') == 'coverage'
        and _c9.get('claims') == 2 and _c9.get('uncovered_charts') == 0,
        f"rc={rc9}, claims={_c9}, stderr={se9[:150]}")

    # R10: placeholder 模式 + claims coverage（推荐组合全链路）
    _spec_ph = dict(_spec)
    _spec_ph['title'] = "城市销售额对比 {{sh}} 万元居首"
    _spec_ph['executive_summary'] = "上海以 {{sh}} 万元销售额居首，广州 {{gz}} 万元垫底。"
    _spec_ph['sections'] = [
        {"id": "s1", "title": "上海销售额 {{sh}} 万元居首",
         "narrative": "四城中上海销售额最高。", "chart_path": _html_paths['R1-城市销售额'].split('/')[-1],
         "annotation": "本图展示 4 座城市的销售额对比。"},
        {"id": "s2", "title": "销售额与利润并排对比",
         "narrative": "销售额与利润走势一致。", "chart_path": _html_paths['R2-城市销售额与利润'].split('/')[-1],
         "annotation": "本图并列展示两条系列。"},
    ]
    (ROOT / 'report_spec_ph.json').write_text(json.dumps(_spec_ph, ensure_ascii=False), encoding='utf-8')
    _proc10 = subprocess.run([sys.executable, str(_RA),
                              '--spec', str(ROOT / 'report_spec_ph.json'),
                              '--charts-dir', str(_rchart_dir),
                              '--output', str(ROOT / 'report_ph.html'),
                              '--ledger', str(ROOT / 'ledger.json'),
                              '--claims', str(ROOT / 'claims.json'),
                              '--claims-check', 'coverage',
                              '--ledger-mode', 'placeholder'],
                             capture_output=True, text=True, timeout=120)
    _p10 = {}
    if _proc10.stdout.strip():
        try:
            _p10 = json.loads(_proc10.stdout)
        except json.JSONDecodeError:
            _p10 = {}
    _r10 = _p10.get('report', {})
    _html10 = ''
    if _r10.get('report_path') and Path(_r10['report_path']).is_file():
        _html10 = Path(_r10['report_path']).read_text(encoding='utf-8')
    rec("R10-placeholder+claims coverage全链路",
        _proc10.returncode == 0 and _r10.get('success')
        and (_r10.get('claims') or {}).get('checked')
        and (_r10.get('ledger') or {}).get('misses') == 0
        and '城市销售额对比 1500 万元居首' in _html10,
        f"rc={_proc10.returncode}, stdout={_proc10.stdout[:200]}, stderr={_proc10.stderr[:200]}")

    # R11: coverage 模式下纯文字章节叙事未被论点 section 指向 → 5008 uncovered_narrative
    _spec_narr = {
        "title": "叙事锚定校验",
        "subtitle": "回归测试套件",
        "theme": "default",
        "sections": [
            {"id": "s1", "title": "有图章节",
             "narrative": "有图章节的叙事。", "chart_path": _html_paths['R1-城市销售额'].split('/')[-1],
             "annotation": "本图展示城市销售额。"},
            {"id": "s2", "title": "纯文字章节",
             "narrative": "这段叙事没有对应的论点锚定。", "chart_path": None},
        ],
    }
    (ROOT / 'report_spec_narr.json').write_text(json.dumps(_spec_narr, ensure_ascii=False), encoding='utf-8')
    _claims_narr = [{"id": "c1", "claim": "有图章节的主张", "evidence": ["s1"], "section": "s1"}]
    (ROOT / 'claims_narr.json').write_text(json.dumps(_claims_narr, ensure_ascii=False), encoding='utf-8')
    _proc11 = subprocess.run([sys.executable, str(_RA),
                              '--spec', str(ROOT / 'report_spec_narr.json'),
                              '--charts-dir', str(_rchart_dir),
                              '--output', str(ROOT / 'report_narr.html'),
                              '--claims', str(ROOT / 'claims_narr.json'),
                              '--claims-check', 'coverage'],
                             capture_output=True, text=True, timeout=120)
    _e11 = {}
    if _proc11.stderr.strip():
        try:
            _e11 = json.loads(_proc11.stderr.strip().splitlines()[-1])
        except json.JSONDecodeError:
            _e11 = {}
    _v11 = _e11.get('details', {}).get('violations', [])
    rec("R11-coverage纯文字章节叙事未挂论点报5008",
        _proc11.returncode == 1 and _e11.get('code') == 5008
        and any(v.get('problem') == 'uncovered_narrative' and v.get('evidence') == 's2'
                for v in _v11),
        f"rc={_proc11.returncode}, err={_proc11.stderr[:250]}")

# ══════════════════ 汇总 ══════════════════
print("\n" + "═" * 60)
print(f"总计: {PASS + FAIL} | 通过: {PASS} | 失败: {FAIL}")
if FAILURES:
    print("\n失败明细:")
    for n, d in FAILURES:
        print(f"  ✗ {n}\n    {d[:250]}")
print("═" * 60)
print(f"测试数据与输出: {ROOT}（临时目录，可安全删除）")
sys.exit(1 if FAIL else 0)
