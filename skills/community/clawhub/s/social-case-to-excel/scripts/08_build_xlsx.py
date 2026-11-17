# -*- coding: utf-8 -*-
"""渲染《跨境电商案例拆解库》xlsx（多 sheet + 内嵌缩略图）+ 独立 markdown 交付"""
import json, os, re, glob
from PIL import Image
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorMarker
from openpyxl.drawing.xdr import XDRPositiveSize2D
from openpyxl.utils.units import pixels_to_EMU

# ---- 每跑一批新案例，改这一段（其余都是通用逻辑）----
# WS 输出目录 / OUT xlsx 路径 / MD markdown 路径 / PLATFORM 平台名 / THEMES 本次的主题列表。
WS = '/tmp/social-case-to-excel-example'
OUT = WS + '/<本次主题>案例拆解库_<平台>_<线1>-<线2>_<日期>.xlsx'
MD = WS + '/<本次主题>案例研究_<条数>条_<日期>.md'
PLATFORM = 'Reddit'          # 展示名：sheet 标题、链接回退、口径说明里都用它（默认数据源是 Reddit）
# 账号前缀按平台来：Reddit 是 u/xxx，X 是 @xxx。表头「原帖账号」保持不变（QA 的契约列之一）。
def ACC(s):
    return ('u/%s' if PLATFORM.lower() == 'reddit' else '@%s') % s
PRIO = {'S': 0, 'A': 1, 'B': 2, 'C': 3}
# 生成时间：落进 sheet3 与 markdown 文件头，别手写日期（会忘改）
import datetime as _dt
GENERATED_AT = '%s（周%s）' % (_dt.date.today().isoformat(), '一二三四五六日'[_dt.date.today().weekday()])
THEMES = ['选品', '黑五营销', '关键词', 'Listing运营', '站外运营', 'Reddit营销']

# ---- 原帖数据 ----
# 用**通配**读本轮抓取文件，不要写死 4 个文件名：轮次数会变，写死了文件少一个就
# FileNotFoundError、多一个就静默漏数据。
RAW_POOL = sorted(glob.glob('/tmp/cbx*_all.json'))
if not RAW_POOL:
    raise SystemExit('没找到原始抓取文件 /tmp/cbx*_all.json —— 先跑 01~04_fetch*.py')
recs = {}
for p in RAW_POOL:
    d = json.load(open(p))
    for lb, blk in d.items():
        # 形状容错：标准形状是 {label: {tweets: [...]}}，但别假设一定是（见 references/pipeline.md 6.0.3）
        tl = blk.get('tweets') if isinstance(blk, dict) else blk
        for t in (tl if isinstance(tl, list) else []):
            if not isinstance(t, dict):
                continue
            tid = str(t.get('tweet_id') or t.get('id') or '')
            if tid and tid not in recs:
                recs[tid] = t
print('RAW_POOL:', len(RAW_POOL), 'files |', len(recs), 'records')
sel = json.load(open('/tmp/cb_sel.json'))
SEL_TID = [r['tid'] for r in (sel if isinstance(sel, list) else sel.get('rows', sel))]

# ---- 案例行（写作文件，glob 通配；不要写 range(1,9)，文件少一个就直接 FileNotFoundError）----
CASES = []
for f in sorted(glob.glob('/tmp/cb_rows*.py')):
    ns = {}
    exec(open(f, encoding='utf-8').read(), ns)
    CASES += ns.get('CASES', [])
print('CASES:', len(CASES), '| 唯一 tid:', len({c['tid'] for c in CASES}))

MAN = {}
POST = {}
for f in sorted(glob.glob('/tmp/tcb*.py')):
    ns = {}
    exec(open(f, encoding='utf-8').read(), ns)
    MAN.update(ns.get('MAN', {}))
    POST.update(ns.get('POST', {}))
print('译文:', len(MAN), '| 推文:', len(POST))

MEDIA = json.load(open('/tmp/cbx_media.json'))

data = []
miss = []
for c in CASES:
    t = recs.get(c['tid'])
    if not t:
        miss.append(c['tid'])
        continue

    def mi(*keys):
        """按序取第一个有值的数值字段；**没有就返回 None**（不是 0）。

        Reddit 没有转发/浏览字段（只有 score 与 num_comments），总表那两列要显示「—」；
        填 0 会让读者以为"这条帖真的 0 转发"，是口径错误。空值由后面的统一填充逻辑写成「—」。
        """
        for k in keys:
            v = t.get(k)
            if v is None or v == '' or v == '—':
                continue
            try:
                return int(float(str(v).replace(',', '')))
            except Exception:
                return None
        return None

    # 链接优先用记录里的 permalink（Reddit 是 /r/…/comments/<id>/，X 是状态页）；
    # 都没有才退回 X 状态页兜底，免得表里出现空链接。
    url = t.get('post_url') or ''
    if not str(url).startswith('http'):
        u = t.get('url') or ''
        url = u if str(u).startswith('http') else ''
    if not url:
        url = 'https://x.com/i/status/' + c['tid']
    d = dict(c)
    d.update({'sn': t.get('screen_name') or t.get('author') or '', 'url': url,
              'created': t.get('created_at') or '', 'lang': t.get('lang') or '',
              'fav': mi('favorites', 'score') or 0,
              'rt': mi('retweets'), 'rp': mi('replies', 'num_comments'), 'views': mi('views'),
              'text': t.get('text') or '',
              'imgs': MEDIA.get(c['tid'], [])})
    d['zh'] = MAN.get(c['tid'], '')
    if not d['zh']:
        cjk = sum(1 for ch in d['text'] if '\u4e00' <= ch <= '\u9fff')
        if cjk > len(d['text']) * 0.15:
            # 中文原帖的「免译占位」：前缀字符串与 references/schema.md、qa_07 的识别口径
            # 保持一致（qa_07 用 startswith('（原帖即中文') 数中文帖；前缀 10 字 + '\n\n' = 12，
            # 所以译文长度恒等于原文长度 + 12）。改了这里要同步改文档，否则下一轮会怀疑是漏译。
            d['zh'] = '（原帖即中文，免译）\n\n' + d['text']
    d['post'] = POST.get(c['tid'], '')
    data.append(d)
print('未匹配:', miss)
if any(not d['zh'] for d in data):
    print('缺译文:', [d['sn'] for d in data if not d['zh']])
if any(not d['post'] for d in data):
    print('缺推文:', [d['sn'] for d in data if not d['post']])

data.sort(key=lambda d: (THEMES.index(d['line']), PRIO[d['pri']], -d['fav']))
for i, d in enumerate(data, 1):
    d['no'] = i
json.dump(data, open('/tmp/cb_cases_final.json', 'w'), ensure_ascii=False, indent=1)

FILL_H = PatternFill('solid', fgColor='EEF3FB')
FILLS = {k: PatternFill('solid', fgColor=v) for k, v in
         {'S': 'FDE7D3', 'A': 'EAF6EC', 'B': 'F5F5F5', 'C': 'FAFAFA'}.items()}
THIN = Side(style='thin', color='D9D9D9')
BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
LINK = Font(color='0B5FA5', underline='single', size=10)

COLS = ['编号', '优先级', '所属线', '案例类型', '案例主体（谁 + 做了什么）', '起点 → 结果（关键数字）',
        '方法拆解（可复制步骤）', '可迁移到我们', '证据强度 / 风险', '原帖账号', '原帖链接', '推文ID',
        '发布时间(UTC)', '语种', '点赞', '转发', '评论', '浏览', '原帖配图', '配图缩略图',
        '正文原文', '正文翻译(中文)', '案例研究推文（Markdown）']
W = [6, 7, 12, 16, 40, 46, 84, 48, 40, 16, 30, 20, 13, 7, 9, 7, 7, 9, 10, 32, 90, 90, 100]

wb = Workbook()
ws = wb.active
ws.title = '1-案例总表'
ws.append(COLS)
for c in range(1, len(COLS) + 1):
    cell = ws.cell(row=1, column=c)
    cell.fill = FILL_H
    cell.font = Font(bold=True, size=10)
    cell.alignment = Alignment(vertical='center', horizontal='center', wrap_text=True)
    cell.border = BD
    ws.column_dimensions[get_column_letter(c)].width = W[c - 1]
ws.row_dimensions[1].height = 34

rows_meta = []
for d in data:
    n = len(d['imgs'])
    mtag = ('%d 张（见 sheet 4）' % n) if n else '无'
    ws.append([d['no'], d['pri'], d['line'], d['ctype'], d['subject'], d['result'],
               d['steps'], d['transfer'], d['risk'], ACC(d['sn']), d['url'], d['tid'],
               d['created'], d['lang'], d['fav'], d['rt'], d['rp'], d['views'],
               mtag, '', d['text'], d['zh'], d['post']])
    r = ws.max_row
    rows_meta.append((r, d))
    for c in range(1, len(COLS) + 1):
        cell = ws.cell(row=r, column=c)
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        cell.font = Font(size=10)
        cell.border = BD
    ws.cell(row=r, column=2).fill = FILLS[d['pri']]
    ws.cell(row=r, column=10).font = Font(size=10, bold=True)
    for c in (1, 2, 15, 16, 17, 18):
        ws.cell(row=r, column=c).alignment = Alignment(vertical='top', horizontal='center')
    ws.cell(row=r, column=11).hyperlink = d['url']
    ws.cell(row=r, column=11).font = LINK
    if n:
        ws.cell(row=r, column=19).hyperlink = d['imgs'][0]['url']
        ws.cell(row=r, column=19).font = LINK
    ws.row_dimensions[r].height = 120

S1 = '/tmp/cbc_imgs_s1'
os.makedirs(S1, exist_ok=True)
n1 = 0
for r, d in rows_meta:
    n = len(d['imgs'])
    if not n:
        ws.cell(row=r, column=20).value = '（无配图）'
        continue
    grid_rows = (n + 1) // 2
    ws.row_dimensions[r].height = 6 + grid_rows * 114 + 6
    for i, it in enumerate(d['imgs']):
        sp = it['small']
        if not os.path.exists(sp):
            continue
        outp = os.path.join(S1, os.path.basename(sp))
        im = Image.open(sp).convert('RGB')
        im.thumbnail((104, 104), Image.LANCZOS)
        im.save(outp, 'JPEG', quality=78)
        pic = XLImage(outp)
        pic.width, pic.height = im.size
        pic.anchor = OneCellAnchor(
            _from=AnchorMarker(col=19, row=r - 1,
                               colOff=pixels_to_EMU(6 + (i % 2) * 112),
                               rowOff=pixels_to_EMU(6 + (i // 2) * 114)),
            ext=XDRPositiveSize2D(pixels_to_EMU(im.size[0]), pixels_to_EMU(im.size[1])))
        ws.add_image(pic)
        n1 += 1
print('sheet1 嵌入缩略图:', n1)

CAP = 408  # Excel 单元格行高上限 409.5pt
def _lines(txt, width):
    cap = width * 1.1  # 约可容纳的拉丁字符数
    out = 0
    for para in str(txt).split('\n'):
        units = 0
        for ch in para:
            units += 2.2 if ch > '\u2e80' else 1.0
        out += max(1, -(-int(units) // int(cap)))
    return out
for r in range(2, ws.max_row + 1):
    need = 0
    for col, width in ((7, 84), (21, 90), (22, 90), (23, 100)):
        t = ws.cell(row=r, column=col).value
        if t:
            need = max(need, _lines(t, width) * 13.5 + 8)
    need = min(int(need), CAP)
    if need > (ws.row_dimensions[r].height or 120):
        ws.row_dimensions[r].height = need
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(COLS)):
    for cell in row:
        if cell.column == 20:
            continue
        if cell.value is None or (isinstance(cell.value, str) and not cell.value.strip()):
            cell.value = '—'
ws.freeze_panes = 'C2'
ws.auto_filter.ref = 'A1:%s%d' % (get_column_letter(len(COLS)), ws.max_row)
print('sheet1', ws.max_row - 1, 'rows x', len(COLS), 'cols')

# ---------------- sheet 2: 方法拆解汇总 ----------------
LINE_SUM = {
 ln: '（待写）本线的共性方法：从本轮入选案例里提炼 2–3 条**跨案例的机制**（不是把案例罗列一遍），'
     '写清「哪些动作反复出现、为什么有效、代价是什么」。每条 200–500 字。'
     '这一整段每批必须重写，上一轮的分线与结论对本轮无效。'
 for ln in THEMES
}
ws2 = wb.create_sheet('2-方法拆解汇总')
ws2.append(['按线汇总：这六条线真正跑通的方法是什么'])
ws2['A1'].font = Font(bold=True, size=12)
ws2.append([])
ws2.append(['所属线', '这一线的共性方法（提炼）'])
hr = ws2.max_row
for c in (1, 2):
    cell = ws2.cell(row=hr, column=c)
    cell.fill = FILL_H
    cell.font = Font(bold=True, size=10)
    cell.border = BD
    cell.alignment = Alignment(horizontal='center', vertical='center')
for ln in THEMES:
    ws2.append([ln, LINE_SUM[ln]])
    r = ws2.max_row
    for c in (1, 2):
        cell = ws2.cell(row=r, column=c)
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        cell.font = Font(size=10)
        cell.border = BD
    ws2.row_dimensions[r].height = max(90, 15 * (len(LINE_SUM[ln]) // 92 + 1) + 12)
ws2.append([])
ws2.append([])
ws2.append(['逐条拆解：每个案例的方法步骤（按线归并，可直接当 checklist 用）'])
ws2.cell(row=ws2.max_row, column=1).font = Font(bold=True, size=12)
h2 = ['所属线', '案例编号', '案例主体（简）', '方法步骤（逐条）', '来源账号']
ws2.append(h2)
hr2 = ws2.max_row
for c in range(1, len(h2) + 1):
    cell = ws2.cell(row=hr2, column=c)
    cell.fill = FILL_H
    cell.font = Font(bold=True, size=10)
    cell.border = BD
    cell.alignment = Alignment(horizontal='center', vertical='center')
for d in sorted(data, key=lambda x: (THEMES.index(x['line']), x['no'])):
    parts = [p.strip() for p in re.split(r'[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬]', d['steps']) if p.strip()]
    for p in parts:
        ws2.append([d['line'], d['no'], d['subject'][:38], p, ACC(d['sn'])])
        r = ws2.max_row
        for c in range(1, 6):
            cell = ws2.cell(row=r, column=c)
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.font = Font(size=10)
            cell.border = BD
        ws2.cell(row=r, column=2).alignment = Alignment(vertical='top', horizontal='center')
for col, w in zip('ABCDE', [12, 8, 34, 92, 18]):
    ws2.column_dimensions[col].width = w
print('sheet2 rows', ws2.max_row)

# ---------------- sheet 4: 原帖配图 ----------------
ws4 = wb.create_sheet('4-原帖配图')
ws4.append(['原帖配图（点击"原图链接"看高清；图片来自 %s 原帖，仅作内部研究使用）' % PLATFORM])
ws4['A1'].font = Font(bold=True, size=12)
h4 = ['案例编号', '优先级', '所属线', '案例主体（简）', '序', '缩略图', '类型', '原图链接', '来源账号']
ws4.append(h4)
r = ws4.max_row
for c in range(1, len(h4) + 1):
    cell = ws4.cell(row=r, column=c)
    cell.fill = FILL_H
    cell.font = Font(bold=True, size=10)
    cell.border = BD
    cell.alignment = Alignment(horizontal='center', vertical='center')
for col, w in zip('ABCDEFGHI', [9, 7, 12, 34, 5, 38, 10, 46, 16]):
    ws4.column_dimensions[col].width = w
nimgs = 0
for d in data:
    for i, it in enumerate(d['imgs'], 1):
        small = '/tmp/cbc_imgs_s4/%s' % os.path.basename(it['small'])
        os.makedirs('/tmp/cbc_imgs_s4', exist_ok=True)
        try:
            im = Image.open(it['file']).convert('RGB')
            im.thumbnail((240, 190), Image.LANCZOS)
            im.save(small, 'JPEG', quality=80)
        except Exception as e:
            print('IMG FAIL', it.get('file', ''), e)
            continue
        kind = {'photo': '图片', 'video': '视频封面', 'animated_gif': 'GIF'}.get(it['kind'], it['kind'])
        link = it['url']
        tag = kind + ('（原帖为视频，这里放封面）' if it['kind'] != 'photo' else '')
        ws4.append([d['no'], d['pri'], d['line'], d['subject'][:34], i, '', tag, link, ACC(d['sn'])])
        r = ws4.max_row
        for c in range(1, len(h4) + 1):
            cell = ws4.cell(row=r, column=c)
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.font = Font(size=10)
            cell.border = BD
        for c in (1, 2, 5):
            ws4.cell(row=r, column=c).alignment = Alignment(vertical='top', horizontal='center')
        ws4.cell(row=r, column=8).hyperlink = link
        ws4.cell(row=r, column=8).font = LINK
        ws4.row_dimensions[r].height = 150
        ws4.add_image(XLImage(small), 'F%d' % r)
        nimgs += 1
print('sheet4 rows', ws4.max_row, '| 嵌入图片', nimgs)

# ---------------- sheet 5: 候选池原始数据 ----------------
ws5 = wb.create_sheet('5-候选池原始数据')
ws5.append(['候选池：%s 端检索命中的过滤后样本（%d 条，含未入选的，用于复查与二次选题）' % (PLATFORM, len(json.load(open('/tmp/cbx_short2.json'))))])
ws5['A1'].font = Font(bold=True, size=11)
h5 = ['序', '推文ID', '账号', '发布时间(UTC)', '语种', '点赞', '转发', '评论', '浏览', '命中主题',
      '命中领域词', '数字个数', '正文（截断 400 字）', '原帖链接']
ws5.append(h5)
r = ws5.max_row
for c in range(1, len(h5) + 1):
    cell = ws5.cell(row=r, column=c)
    cell.fill = FILL_H
    cell.font = Font(bold=True, size=10)
    cell.border = BD
    cell.alignment = Alignment(horizontal='center', vertical='center')
pool = json.load(open('/tmp/cbx_short2.json'))
for i, p in enumerate(pool, 1):
    plink = p.get('url') or ('https://x.com/i/status/' + p['tid'])
    ws5.append([i, p['tid'], ACC(str(p['sn'])), p['created'], p['lang'], p['fav'], p['rt'], p['rp'],
                p['views'], '/'.join(p['theme']), '/'.join(p['dom'][:4]), p['nnum'],
                p['text'][:400], plink])
    r = ws5.max_row
    for c in range(1, len(h5) + 1):
        cell = ws5.cell(row=r, column=c)
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        cell.font = Font(size=9)
        cell.border = BD
    ws5.cell(row=r, column=14).hyperlink = plink
    ws5.cell(row=r, column=14).font = LINK
for col, w in zip('ABCDEFGHIJKLMN', [5, 21, 18, 13, 7, 8, 7, 7, 9, 22, 30, 8, 70, 30]):
    ws5.column_dimensions[col].width = w
ws5.freeze_panes = 'C2'
ws5.auto_filter.ref = 'A1:N%d' % ws5.max_row
print('sheet5 rows', ws5.max_row)

# ---------------- sheet 6: 主题分布 ----------------
ws6 = wb.create_sheet('6-主题与检索口径')
ws6.append(['六大主题 × 案例数 × 检索式覆盖'])
ws6['A1'].font = Font(bold=True, size=12)
ws6.append([])
h6 = ['所属线', '入选案例数', 'S', 'A', 'B', '该线案例（编号 · 主体简）']
ws6.append(h6)
r = ws6.max_row
for c in range(1, len(h6) + 1):
    cell = ws6.cell(row=r, column=c)
    cell.fill = FILL_H
    cell.font = Font(bold=True, size=10)
    cell.border = BD
    cell.alignment = Alignment(horizontal='center', vertical='center')
for ln in THEMES:
    sub = [d for d in data if d['line'] == ln]
    ws6.append([ln, len(sub), sum(1 for d in sub if d['pri'] == 'S'), sum(1 for d in sub if d['pri'] == 'A'),
                sum(1 for d in sub if d['pri'] == 'B'),
                ' ; '.join('%d·%s' % (d['no'], d['subject'][:22]) for d in sub)])
    r = ws6.max_row
    for c in range(1, len(h6) + 1):
        cell = ws6.cell(row=r, column=c)
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        cell.font = Font(size=10)
        cell.border = BD
    ws6.row_dimensions[r].height = 60
for col, w in zip('ABCDEF', [12, 10, 5, 5, 5, 110]):
    ws6.column_dimensions[col].width = w

# ---------------- sheet 3: 口径与说明 ----------------
ws3 = wb.create_sheet('3-口径与说明')

# 行高裁切的量化：不要手数。以 408pt 为上限（Excel 单元格行高上限），这里算清楚本批
# 有几行被裁、由哪一列驱动 —— 这个数字要写进下面的「行高与长文阅读」说明里，
# 它决定读者该去开 markdown 还是直接在总表里看。
def _need(d):
    need, worst = 0, ''
    for key, width, nm in (('steps', 84, '方法拆解'), ('text', 90, '正文原文'),
                           ('zh', 90, '正文翻译'), ('post', 100, '案例研究推文')):
        v = _lines(d.get(key) or '', width) * 13.5 + 8
        if v > need:
            need, worst = v, nm
    return need, worst


from collections import Counter as _C
OVER = [(d['no'], _need(d)[1]) for d in data if _need(d)[0] > CAP]
OVER_TXT = ' / '.join('%s %d 条' % (k, v) for k, v in _C(w for _, w in OVER).most_common())

notes = [
 ('这份是什么', '继《X 成功案例拆解库》之后的一批，数据源换成 %s（Reddit 社区帖），继续做跨境电商主题：选品、黑五营销、关键词、Listing 运营、站外运营、Reddit 营销。每条都是"有人在跨境生意里真做过 + 有可量化结果 + 能拆出方法"，不是热点资讯。共 %d 条。' % (PLATFORM, len(data))),
 ('数据来源', '%s 社区公开帖（含帖内正文与配图），通过平台公开数据接口采集（社区内按关键词检索，按时间先后返回）。帖内指标（赞 / 评论）为接口返回原值的抓取当日快照。' % PLATFORM),
 ('时间窗口', '按相对天数窗抓取（种子轮 730 天、补捞轮 1095 天），**没有绝对起止日期**——接口只支持"最近 N 天"。因此本批口径是"截至抓取日的近 2–3 年"，不是某个自然年。'),
 ('检索式', '合计 4 轮 %d 组检索式，覆盖六大主题；%s 的检索是**社区内**搜索（一个社区 × 一句词 × 一个时间窗），没有全站搜索，所以覆盖面靠"社区数 × 词数"铺开。原始命中去重后 %d 条，过滤后候选池 %d 条（见 sheet 5）。' % (38, PLATFORM, len(recs), len(json.load(open('/tmp/cbx_short2.json'))))),
 ('案例入选标准', '三条同时满足：① 跨境生意相关（Amazon/独立站/TikTok Shop 等实物电商场景，或平台级电商数据）；② 有可量化结果（金额、月销件数、ROAS/ACOS/TACOS、CPA/CAC、留存、点击/订单等）；③ 能拆出可复制步骤或可引用的结构。'),
 ('排除规则', '剔除：纯资讯与官宣（无方法）、无数字的观点帖、内容农场式"19 岁月入 90 万美元"且无过程细节、与跨境电商无关的赛道（加密货币、股票、leetcode、faceless YouTube 等）、以及求助/树洞类无结果帖——%s 上这类占比明显高于 X，是本批最主要的噪音来源。' % PLATFORM),
 ('排序口径', '先按六大主题归线，线内按优先级（S → A → B），同优先级按点赞（%s 的 score）降序编号。' % PLATFORM),
 ('优先级', 'S＝方法完整、可直接抄（%d 条）；A＝方法可用但需按自己场景改写（%d 条）；B＝单一技巧或早期样本（%d 条）。' % (sum(1 for d in data if d['pri'] == 'S'), sum(1 for d in data if d['pri'] == 'A'), sum(1 for d in data if d['pri'] == 'B'))),
 ('案例类型', '案例（有过程有结果）／反例（踩坑复盘，价值在风险机制）／平台数据（平台级口径，用于对齐大盘）／方法论（清单化打法，无单一主人公）。'),
 ('方法拆解', '「方法拆解」列是按原帖内容重写的步骤化清单（不是翻译），「可迁移到我们」列是针对我们业务的判断，两列都是我整理的，可以逐条改。'),
 ('正文翻译(中文)', '英文帖为人工翻译，保留原文全部数字与结论；超长帖（%s 的复盘帖常达数千字符）采用逐段精译（内容完整，压缩修辞与重复），已在译文中标注。原帖本身是中文的沿用原文并标注"免译"。译文仅供内部研究，引用请以原文为准。' % PLATFORM),
 ('原帖配图', 'sheet1 第 19 列显示张数并链到第一张原图，第 20 列内嵌缩略图（每行最多 2 张）；sheet 4 按图逐条列出原图链接。%d 条案例带有配图，共 %d 张；%s 的讨论型帖常无配图，有图的多为后台/面板截图——这类截图里的数字是重要事实来源，已用 OCR 读取并纳入数字核对。图片版权归原作者，仅作内部研究使用。' % (sum(1 for d in data if d['imgs']), nimgs, PLATFORM)),
 ('案例研究推文（Markdown）', '第 23 列是可直接发布的成稿：3 个标题候选 + 故事 + 方法拆解 + 可直接抄的动作 + 一句话结论，全部 Markdown 语法。同一批内容导出为独立 markdown 文件（见同目录交付物）。'),
 ('行高与长文阅读', '行高按「方法拆解 / 正文原文 / 正文翻译 / 案例研究推文」四列中最长的一列自适应，上限 408pt（Excel 单元格行高上限）。本批 %d 条中有 %d 条超过该上限（驱动列：%s）。超长行的完整文本仍在单元格里（选中单元格可在编辑栏查看全文），完整成稿请打开同目录的 markdown 文件。下面的「超上限行号」列出具体是哪些编号。' % (len(data), len(OVER), OVER_TXT or '—')),
 ('超上限行号（编号）', '、'.join(str(n) for n, _ in OVER) or '无'),
 ('证据强度/风险', '绝大多数案例的收入与增长数字是当事人自述，社区帖不构成审计凭证；带推广性质（服务/课程/咨询引流）的已在该列标注。做决策前请按该列提示二次核实。'),
 ('研究视角', '所有内容按第三方案例研究整理，不代表原帖作者观点；引用时请注明来源账号与原帖链接。'),
 ('生成时间', '%s' % GENERATED_AT),
]
ws3.append(['项', '说明'])
for c in ('A1', 'B1'):
    ws3[c].fill = FILL_H
    ws3[c].font = Font(bold=True, size=10)
    ws3[c].border = BD
for k, v in notes:
    ws3.append([k, v])
    r = ws3.max_row
    for c in (1, 2):
        cell = ws3.cell(row=r, column=c)
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        cell.font = Font(size=10)
        cell.border = BD
    ws3.row_dimensions[r].height = max(30, 15 * (len(v) // 100 + 1) + 12)
ws3.column_dimensions['A'].width = 22
ws3.column_dimensions['B'].width = 110

# ---------------- 独立 markdown 交付 ----------------
L = ['# 跨境电商案例研究（%d 条 · 可直接发布）' % len(data), '',
     '> 数据源：%s 社区公开帖。六大主题：选品 / 黑五营销 / 关键词 / Listing 运营 / 站外运营 / Reddit 营销。' % PLATFORM,
     '> 每条含：爆款标题候选 · 故事 · 方法拆解 · 可直接抄的动作 · 一句话结论。',
     '> 生成时间：%s ｜ 正文与配图版权归原作者，引用请注明来源账号与原帖链接。' % GENERATED_AT, '', '---', '']
for d in data:
    L.append('## 案例 %d｜%s' % (d['no'], d['subject']))
    L.append('')
    L.append('`%s线 · 优先级 %s · 来源 @%s · %s`' % (d['line'], d['pri'], d['sn'], d['url']))
    L.append('')
    L.append(d['post'].strip())
    L.append('')
    L.append('---')
    L.append('')
open(MD, 'w', encoding='utf-8').write('\n'.join(L))
print('markdown:', MD, '%.1f KB' % (os.path.getsize(MD) / 1024))

wb._sheets = [wb['1-案例总表'], wb['2-方法拆解汇总'], wb['3-口径与说明'], wb['4-原帖配图'],
              wb['5-候选池原始数据'], wb['6-主题与检索口径']]
wb.save(OUT)
print('saved', OUT, '| sheets', wb.sheetnames, '| %.1f MB' % (os.path.getsize(OUT) / 1e6))
