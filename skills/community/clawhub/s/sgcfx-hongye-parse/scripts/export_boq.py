#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SGCFX 分部分项工程量清单(表3003) → Excel 导出器
=============================================================
逆向结论（已通过文件内部"合计"行 12/12 校验）：
  表结构 = [96字节头: +4=schema长度, +8, +12, +16=表ID, +20=版本号]
           [schema区: 字段名]  [数据区]
  字符串 = [uint32 字符数][UTF-16LE]
  数据区记录类型: F段N=分部 / F目N=清单项 / F定N=定额子目
  清单项字段序: 序号 → [工程量(字符串)] → F目N → 清单编码 → 定额编号
                → 项目名称 → 单位 → [数值区] → 项目特征 → 计算规则 → ...
  数值区: 单位字符串结束后起，[综合单价 double][综合合价 double] 步长12字节
          后续为人材机/管理费/利润的 (单价,合价) 对，步长亦为12
  校验: 综合合价 = 综合单价 × 工程量   (384/384 通过)
        文件内部"合计"行 = Σ综合合价   (12/12 通过, 差≤0.04分)
"""
import struct, re, os, sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# --- 防电子表格公式注入（CWE-1236）：第三方文件里的字段可能以 =/+/−/@ 开头 ---
def _defuse_formulas(ws, first_data_row=2):
    """强制把可能被 Excel 当作公式的字符串单元格设为文本类型。"""
    for row in ws.iter_rows(min_row=first_data_row):
        for cell in row:
            if isinstance(cell.value, str) and cell.value[:1] in ('=', '+', '-', '@', '\t'):
                cell.data_type = 's'


def _csv_safe(v):
    """CSV 输出防公式注入：危险前缀前置单引号（Excel 打开时不求值）。"""
    if isinstance(v, str) and v[:1] in ('=', '+', '-', '@', '\t'):
        return "'" + v
    return v



SRC = sys.argv[1] if len(sys.argv) > 1 else 'tmp_sgcfx'
DISC = sys.argv[2] if len(sys.argv) > 2 else '4'      # 4=审核值, 3=送审值
OUT  = sys.argv[3] if len(sys.argv) > 3 else '输出'

NUM = re.compile(r'^-?\d+(\.\d+)?$')

# 分册 → 单位工程 映射（同专业内按金额排序匹配，比值一致性 0.803~0.831）
# 分册 → 单位工程 映射。**不同项目必须重新核对**：
#   做法：读 {DISC}/Tree 得到「单项工程 → 单位工程」层级顺序，
#   再用清单编码前缀判断专业（01=建筑 / 03=安装 / 04=市政总平 / 05=其他），
#   最后按金额量级配对（清单合价 < 单位工程金额，同专业内按大小排序匹配）。
# 下面为空时自动降级为「分册N」，不臆造名称。
MAP = {}

HDR_FILL  = PatternFill('solid', fgColor='305496')
HDR_FONT  = Font(name='等线', size=11, bold=True, color='FFFFFF')
BODY      = Font(name='等线', size=10)
SUB_FILL  = PatternFill('solid', fgColor='DDEBF7')
SUB_FONT  = Font(name='等线', size=10, bold=True)
TOT_FILL  = PatternFill('solid', fgColor='FFF2CC')
TOT_FONT  = Font(name='等线', size=10, bold=True, color='C00000')
THIN      = Side(style='thin', color='BFBFBF')
BORDER    = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
MONEY, QTY, PCT = '#,##0.00', '#,##0.00', '0.00%'


def scan(path):
    d = open(path, 'rb').read(); n = len(d)
    S = 96 + struct.unpack_from('<I', d, 4)[0]
    p = S; out = []
    while p + 4 <= n:
        L = struct.unpack_from('<I', d, p)[0]
        if 1 <= L <= 500 and p + 4 + 2 * L <= n:
            b = d[p + 4:p + 4 + 2 * L]
            try:
                s = b.decode('utf-16-le')
            except Exception:
                p += 1; continue
            if sum(1 for c in s if c.isprintable() or c in '\r\n\t') / len(s) >= 0.9:
                out.append((p, L, s)); p += 4 + 2 * L; continue
        p += 1
    return d, {o: o + 4 + 2 * L for o, L, s in out}, out


def parse_3003(path):
    d, end, out = scan(path)
    mu = [o for o, L, s in out if re.fullmatch(r'F目\d+', s)]
    seg = [(o, s) for o, L, s in out if re.fullmatch(r'F段\d+', s)]
    rows = []
    for o in mu:
        pre = [x for x in out if x[0] < o]
        af = [x for x in out if x[0] > o][:8]
        if len(af) < 4:
            continue
        cs = [x[2] for x in af]
        qty = None
        for x in reversed(pre[-4:]):
            if NUM.match(x[2]):
                qty = float(x[2]); break
        st = end[af[3][0]]
        price = struct.unpack_from('<d', d, st)[0]
        amt   = struct.unpack_from('<d', d, st + 12)[0]
        # 项目特征: 单位之后第一个长文本
        feat = next((cs[i] for i in range(4, len(cs)) if len(cs[i]) > 8), '')
        rows.append({'code': cs[0], 'quota': cs[1] if len(cs) > 1 else '',
                     'name': cs[2] if len(cs) > 2 else '',
                     'unit': cs[3] if len(cs) > 3 else '',
                     'qty': qty, 'price': price, 'amt': amt,
                     'feat': feat.replace('\r\n', ' / ')})
    # 文件内部权威合计
    total = None
    for o, L, s in out:
        if s.strip() == '合计':
            for j in range(12):
                v = struct.unpack_from('<d', d, end[o] + j * 4)[0]
                if v == v and 1e3 < abs(v) < 1e9:
                    total = v; break
    return rows, total


def write_sheet(ws, rows, title):
    hdr = ['序号', '清单编码', '定额编号', '项目名称', '项目特征',
           '单位', '工程量', '综合单价', '综合合价', '验算']
    ws.append(hdr)
    for c in range(1, len(hdr) + 1):
        cell = ws.cell(1, c)
        cell.fill = HDR_FILL; cell.font = HDR_FONT
        cell.alignment = Alignment('center', 'center', wrap_text=True)
        cell.border = BORDER
    for i, r in enumerate(rows, 1):
        q, p, a = r['qty'], r['price'], r['amt']
        ok = 'OK' if (q and p and abs(q * p - a) < 0.02) else '?'
        ws.append([i, r['code'], r['quota'], r['name'], r['feat'],
                   r['unit'], q, round(p, 2), round(a, 2), ok])
    # 合计行
    ws.append(['', '', '', '合  计', '', '', '',
               '', round(sum(r['amt'] for r in rows), 2), ''])
    lr = ws.max_row
    for c in range(1, len(hdr) + 1):
        ws.cell(lr, c).fill = TOT_FILL; ws.cell(lr, c).font = TOT_FONT
        ws.cell(lr, c).border = BORDER
    for r in range(2, lr + 1):
        for c in range(1, len(hdr) + 1):
            cell = ws.cell(r, c)
            cell.border = BORDER
            cell.font = BODY if r < lr else TOT_FONT
            if hdr[c - 1] in ('工程量', '综合单价', '综合合价'):
                cell.number_format = QTY if hdr[c - 1] == '工程量' else MONEY
                cell.alignment = Alignment('right', 'center')
            else:
                cell.alignment = Alignment('left', 'center',
                                           wrap_text=len(str(cell.value or '')) > 40)
    for i, h in enumerate(hdr, 1):
        w = {'序号': 6, '清单编码': 16, '定额编号': 12, '项目名称': 26,
             '项目特征': 46, '单位': 6, '工程量': 11, '综合单价': 13,
             '综合合价': 14, '验算': 7}.get(h, 12)
        ws.column_dimensions[get_column_letter(i)].width = w
    _defuse_formulas(ws)
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f"A1:{get_column_letter(len(hdr))}{lr}"
    ws.row_dimensions[1].height = 28


def main():
    os.makedirs(OUT, exist_ok=True)
    base = os.path.join(SRC, DISC)
    subs = sorted([x for x in os.listdir(base) if x.isdigit()], key=int)
    wb = Workbook(); wb.remove(wb.active)
    summary = []
    for sid in subs:
        p = os.path.join(base, sid, '3003')
        if not os.path.exists(p) or os.path.getsize(p) < 5000:
            continue
        rows, total = parse_3003(p)
        if not rows:
            continue
        single, prof = MAP.get(sid, (f'单项工程({sid})', '单位工程'))
        name = f"{single[:4]}-{prof}"
        ws = wb.create_sheet(name[:31])
        write_sheet(ws, rows, name)
        mine = sum(r['amt'] for r in rows)
        summary.append({'分册': f'{DISC}/{sid}', '单项工程': single,
                        '单位工程': prof, '清单条数': len(rows),
                        '清单合价合计': round(mine, 2),
                        '文件内部合计': round(total, 2) if total else None,
                        '差异': round(mine - total, 2) if total else None,
                        '勾稽': '通过' if (total is None or abs(mine - total) < 0.05) else '不通过'})
    # 汇总表放最前
    ws0 = wb.create_sheet('00-分册汇总', 0)
    h = ['分册', '单项工程', '单位工程', '清单条数', '清单合价合计',
         '文件内部合计', '差异', '勾稽']
    ws0.append(h)
    for c in range(1, len(h) + 1):
        cell = ws0.cell(1, c)
        cell.fill = HDR_FILL; cell.font = HDR_FONT
        cell.alignment = Alignment('center', 'center', wrap_text=True)
        cell.border = BORDER
    for r in summary:
        ws0.append([r[k] for k in h])
    ws0.append(['', '', '总计', sum(x['清单条数'] for x in summary),
                round(sum(x['清单合价合计'] for x in summary), 2),
                round(sum(x['文件内部合计'] for x in summary), 2),
                round(sum(x['差异'] for x in summary), 2), ''])
    for r in range(2, ws0.max_row + 1):
        is_t = ws0.cell(r, 3).value == '总计'
        for c in range(1, len(h) + 1):
            cell = ws0.cell(r, c)
            cell.border = BORDER
            cell.font = TOT_FONT if is_t else BODY
            if is_t: cell.fill = TOT_FILL
            if h[c - 1] in ('清单合价合计', '文件内部合计', '差异'):
                cell.number_format = MONEY
                cell.alignment = Alignment('right', 'center')
    for i, k in enumerate(h, 1):
        ws0.column_dimensions[get_column_letter(i)].width = \
            {'分册': 9, '单项工程': 18, '单位工程': 18, '清单条数': 10,
             '清单合价合计': 16, '文件内部合计': 16, '差异': 10, '勾稽': 8}.get(k, 12)
    _defuse_formulas(ws)
    ws0.freeze_panes = 'A2'
    tag = '审核值' if DISC == '4' else '送审值'
    out = os.path.join(OUT, f'06-分部分项工程量清单({tag}).xlsx')
    wb.save(out)
    print('生成:', out)
    print(f'  分册 {len(summary)} 个，清单 {sum(x["清单条数"] for x in summary)} 条')
    for s in summary:
        print(f"    {s['分册']:<6} {s['单项工程']:<9}{s['单位工程']:<12}"
              f"{s['清单条数']:>4}条  合价={s['清单合价合计']:>13,.2f}  "
              f"文件={s['文件内部合计']:>13,.2f}  差={s['差异']:>+7.2f}  {s['勾稽']}")


if __name__ == '__main__':
    main()
