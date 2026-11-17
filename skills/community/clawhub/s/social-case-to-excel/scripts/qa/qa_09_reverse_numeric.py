# -*- coding: utf-8 -*-
"""QA：反向数字核对 —— 中文列里出现、但原帖里找不到的数字。

为什么需要反向：正向（原帖每个数字都要在中文里出现）只能抓「漏写」；写错量级、
写错来源（把 A 帖的数字写到 B 帖）、凭印象加数字，都只有反向能抓。真实收益：
上一轮靠它抓出 1 处笔误（$1.1m/mo 被写成「11,000 美元/月」而不是 110 万美元/月）
和 2 处该补的原帖细节。

单位归一化：把 万/十万/百万/千万/亿/万亿 与 k/M/B/billion 换算成同一个数再比，
容差 1%。已知假报（看到了不必改数据）：
  - 帖内序号：「7. Most…」会被当成 7M、「9. Buy」被当成 9B、「3. KD<10」被当成 3000；
  - 换行/空格后的单词首字母被当单位："$3,800\nMonth" → 3.8e9（Month 的 M）、
    "500 keywords" → 500k。脚本现在要求英文字母单位**紧贴数字**（中间不能有空格/换行），
    且后面不能紧跟字母，这两类已消除；
  - 小写单位：$1.1m / $7.5mm / 3bn 这类（已支持小写 m/mm/b/bn）；
  - 组合单位：已有 —— "12.2 trillion" 写成中文「12.2 万亿」以前会被切成「12.2 万」，
    现在 `万亿` 排在 `万`/`亿` 前面，已修；
  - @handle 里的数字：@qanon416、@jwcollins1955；
  - **URL 参数与推广链接**：`?s=21&t=0xKh7c0T…`、`…industry-at-a-glance-2025-46c7`、
    `beehiiv.com/p/…` 里的数字；
  - **电话 / WhatsApp 号**：`+82 10-2688-3795` 会被拆成 10 / 2688 / 3795 三个数；
  - **作者笔误照抄**：原文写 `$1000k+` 时中文照抄并标注（原文如此），反向会报 1000 找不到；
  - **派生数字**：由原帖两个数算出来的差值/比率（如 $40K−$25K 的「差价 $15K」），
    中文侧必须标注「（$40K−$25K，自算）」，否则会被判成凭空写数；
  - **中文惯用写法**：`1.5k` 写成「1,500」、「9 out of 10」写成「10 次里有 9 次」——
    数值等价，脚本按字面比对会报找不到；
  - 自己补的日期戳 / 表头编号。

**来源分类**：数字查不到，可能是「写错」，也可能是「来源不是原帖正文」——最典型的是
从配图 OCR 读出来的后台截图数字（GSC 点击量、Shopify 后台金额、订单号）。这类不是错误，
不该让人手工复核。脚本会自动读工作目录下的 `*ocr*.json`，把 OCR 文本并入比对池；
仍查不到、但能在 OCR 里找到的，单独归到「OCR 来源（正常）」一类打印，不计入可疑。

结果三类分开打印，判读顺序是：**可疑** 逐条确认 → OCR 来源 扫一眼是否合理 → 计数。
"""
import glob, json, os, re, sys
from openpyxl import load_workbook

XLSX = '/tmp/social-case-to-excel-example/跨境电商案例拆解库_X_选品-黑五-关键词-Listing-站外-Reddit_20260916.xlsx'
SEL = '/tmp/cb_sel.json'
sel = json.load(open(SEL, encoding='utf-8'))
rows = sel if isinstance(sel, list) else sel.get('rows', sel)
bytid = {str(r['tid']): r for r in rows}
wb = load_workbook(XLSX)
ws = wb[wb.sheetnames[0]]
hdr = [c.value for c in ws[1]]
# 检查哪些列：中文写作列（按表头找，表头改过也不怕）
COLS = [i + 1 for i, h in enumerate(hdr) if h and re.search(
    r'案例主体|结果|方法拆解|可迁移|正文翻译|案例研究推文', str(h))]
def key(v):
    """编号规范化：'01' / '1' / 1 视为同一条（否则 rowmap 查不到，脚本会静默全绿）。"""
    return re.sub(r'^0+(?=\d)', '', str(v).strip())


# 用「推文ID」列对齐 xlsx 行与入选池记录（编号列是构建时才生成的序号，入选池里没有）；
# 没有 ID 列就退回按行序对齐。表头对不上、或一条都没匹配上时直接报错而不是静默通过。
tid_col = next((i + 1 for i, h in enumerate(hdr) if h and ('推文ID' in str(h) or 'tweet' in str(h).lower())), None)
rowmap = {}
if tid_col:
    for r in range(2, ws.max_row + 1):
        v = ws.cell(r, tid_col).value
        if v:
            rowmap[str(v).strip()] = r
matched = [r for r in rows if str(r.get('tid', '')).strip() in rowmap]
if not matched:
    print('!! 没有任何一条入选记录能对上 xlsx 行（检查推文ID列与 sel 的 tid 是否同一批数据）')
    sys.exit(1)


def xrow(idx, rec):
    r = rowmap.get(str(rec.get('tid', '')).strip())
    return r if r else (idx + 2 if idx + 2 <= ws.max_row else None)

UNIT = {'兆': 1e12, '万亿': 1e12, '亿': 1e8, '千万': 1e7, '百万': 1e6, '十万': 1e5,
        '万': 1e4, '千': 1e3,
        'k': 1e3, 'K': 1e3, 'M': 1e6, 'MM': 1e6, 'mm': 1e6, 'm': 1e6,
        'B': 1e9, 'b': 1e9, 'billion': 1e9, 'million': 1e6, 'bn': 1e9}

# 中文单位可以带空格（「1.5 万」），英文字母单位必须紧贴数字且后面不接字母
# （否则 "Month"/"KD"/"keywords" 的首字母会被当成 百万/千）。
# 「万亿」要排在「万」「亿」前面，否则 "12.2 万亿" 会被切成「12.2 万」。
NUM_RE = re.compile(
    r'(\d[\d,]*(?:\.\d+)?)'
    r'(?:[ \t]*(万亿|兆|千万|百万|十万|亿|万|千))?'
    r'(?:(billion|million|MM|mm|bn|[kKMBmb])(?![A-Za-z]))?'
    r'(?![\d])')


def nums(txt):
    """抽出所有数字 token 并归一化成绝对值集合（忽略单位缺失）。"""
    out = set()
    for m in NUM_RE.finditer(txt):
        core = m.group(1).replace(',', '').rstrip('.')
        if not re.fullmatch(r'\d+(\.\d+)?', core):
            continue
        out.add(round(float(core) * UNIT.get(m.group(2) or m.group(3) or '', 1), 4))
    return out


def ocr_texts():
    """工作目录下的 OCR 结果（*ocr*.json）——配图里的数字是合法来源。
    结构兼容 {path: text} / {path: [..]} / 裸字符串；找不到就返回空集合。"""
    cands = []
    for pat in ('*ocr*.json', '*OCR*.json'):
        cands += glob.glob(os.path.join(os.path.dirname(os.path.abspath(SEL)), pat))
    blob, files = [], sorted(set(cands))
    for p in files:
        try:
            data = json.load(open(p, encoding='utf-8'))
        except Exception:
            continue
        stack = [data]
        while stack:
            v = stack.pop()
            if isinstance(v, str):
                blob.append(v)
            elif isinstance(v, dict):
                stack.extend(v.values())
            elif isinstance(v, list):
                stack.extend(v)
    return set().union(*[nums(t) for t in blob]) if blob else set(), files


def close(a, b):
    return abs(a - b) <= max(1e-9, 0.01 * max(abs(a), abs(b)))


THRESH = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0
OCR_SRC, ocr_files = ocr_texts()
bad = 0
from_ocr = []
for idx, r in enumerate(rows):
    xr = xrow(idx, r)
    if not xr:
        continue
    src = nums(r.get('text', '') or '')
    for col in COLS:
        v = ws.cell(xr, col).value
        if not isinstance(v, str):
            continue
        for x in sorted(nums(v)):
            if x < THRESH or any(close(x, s) for s in src):
                continue
            i = v.find(('%g' % x).rstrip('0').rstrip('.'))
            frag = v[max(0, i - 40):i + 30].replace('\n', ' ') if i >= 0 else v[:60]
            label = '%s @%-17s 列%d(%s) 数字 %g' % (
                key(ws.cell(xr, 1).value), r.get('sn', '?'), col, hdr[col - 1], x)
            if any(close(x, s) for s in OCR_SRC):
                # 来源是配图（后台截图 / GSC 面板），不是笔误，单独列出免得人工复核
                from_ocr.append('%s | %s' % (label, frag))
                continue
            print(' %s 原帖找不到 | %s' % (label, frag))
            bad += 1
print('反向核对：可疑数字 %d 个（对照脚本头部注释里的假报清单逐条确认）' % bad)
if ocr_files:
    print('来源=配图 OCR 的数字 %d 个（共读 %d 个 OCR 文件，正常来源，扫一眼即可）' % (
        len(from_ocr), len(ocr_files)))
    for line in from_ocr[:40]:
        print('  ', line)
    if len(from_ocr) > 40:
        print('   … 其余 %d 个省略' % (len(from_ocr) - 40))
else:
    print('提示：工作目录下没找到 *ocr*.json，配图里的数字会全部被算作「可疑」——'
          '把 OCR 结果落盘成 %s/*ocr*.json 可以让这部分自动归类' % os.path.dirname(os.path.abspath(SEL)))
