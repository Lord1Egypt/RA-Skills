#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SGCFX 工程造价汇总计算表(表3010) → Excel
=============================================================
造价链条（与《建设工程工程量清单计价规范》一致）：
  A  分部分项合价
  A.1 甲供材料费
  B  措施项目        B.1 安全生产措施费
  C  其他项目        C.1 暂列金额 / C.2 专业工程暂估价 / C.3 计日工
                    C.4 总承包服务费 / C.5 合同约定的其他项目
  D  税前建安工程造价 = A+B+C
  E  增值税 = (D-A.1) × 9%
  总价合计 = D-A.1+E

字段定位：数据区内按标题名精确匹配，取其后第一个非零 double。
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



SRC  = sys.argv[1] if len(sys.argv) > 1 else 'tmp_sgcfx'
DISC = sys.argv[2] if len(sys.argv) > 2 else '4'
OUT  = sys.argv[3] if len(sys.argv) > 3 else '输出'

# 分册 → 单位工程 映射。**不同项目必须重新核对**：
#   做法：读 {DISC}/Tree 得到「单项工程 → 单位工程」层级顺序，
#   再用清单编码前缀判断专业（01=建筑 / 03=安装 / 04=市政总平 / 05=其他），
#   最后按金额量级配对（清单合价 < 单位工程金额，同专业内按大小排序匹配）。
# 下面为空时自动降级为「分册N」，不臆造名称。
MAP = {}
KEYS = ['分部分项合价', '甲供材料费', '通用措施项目合价+专业措施项目合价',
        '安全生产措施费', '其他项目合价', '暂列金额', '专业工程暂估价',
        '计日工', '总承包服务费', '合同约定的其他项目', 'A+B+C',
        '(D-A.1)*费率', 'D-A.1+E']

HDR_FILL = PatternFill('solid', fgColor='305496')
HDR_FONT = Font(name='等线', size=11, bold=True, color='FFFFFF')
BODY = Font(name='等线', size=10)
TOT_FILL = PatternFill('solid', fgColor='FFF2CC')
TOT_FONT = Font(name='等线', size=10, bold=True, color='C00000')
SUB_FILL = PatternFill('solid', fgColor='DDEBF7')
SUB_FONT = Font(name='等线', size=10, bold=True)
THIN = Side(style='thin', color='BFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
MONEY = '#,##0.00'


def parse_3010(path):
    d = open(path, 'rb').read(); n = len(d)
    S = 96 + struct.unpack_from('<I', d, 4)[0]
    p = S; out = []
    while p + 4 <= n:
        L = struct.unpack_from('<I', d, p)[0]
        if 1 <= L <= 200 and p + 4 + 2 * L <= n:
            b = d[p + 4:p + 4 + 2 * L]
            try:
                s = b.decode('utf-16-le')
            except Exception:
                p += 1; continue
            if sum(1 for c in s if c.isprintable() or c in '\r\n\t') / len(s) >= 0.9:
                out.append((p, L, s)); p += 4 + 2 * L; continue
        p += 1
    end = {o: o + 4 + 2 * L for o, L, s in out}
    val = {}
    for o, L, s in out:
        if s in KEYS and s not in val:
            for j in range(6):
                oo = end[o] + j * 4
                if oo + 8 > n: break
                v = struct.unpack_from('<d', d, oo)[0]
                if v == v and 0.005 < abs(v) < 1e12:
                    val[s] = round(v, 2); break
            val.setdefault(s, 0.0)
    return val


def main():
    os.makedirs(OUT, exist_ok=True)
    base = os.path.join(SRC, DISC)
    subs = sorted([x for x in os.listdir(base) if x.isdigit()], key=int)
    rows = []
    for sid in subs:
        p = os.path.join(base, sid, '3010')
        if not os.path.exists(p) or os.path.getsize(p) < 1000:
            continue
        v = parse_3010(p)
        single, prof = MAP.get(sid, (f'单项工程({sid})', '单位工程'))
        A = v.get('分部分项合价', 0); A1 = v.get('甲供材料费', 0)
        B = v.get('通用措施项目合价+专业措施项目合价', 0)
        B1 = v.get('安全生产措施费', 0); C = v.get('其他项目合价', 0)
        C1 = v.get('暂列金额', 0); C2 = v.get('专业工程暂估价', 0)
        D = v.get('A+B+C', 0); E = v.get('(D-A.1)*费率', 0)
        T = v.get('D-A.1+E', 0)
        # 自校验
        chk1 = round(A + B + C - D, 2)
        chk2 = round((D - A1) * 0.09 - E, 2)
        chk3 = round(D - A1 + E - T, 2)
        rows.append({'分册': f'{DISC}/{sid}', '单项工程': single, '单位工程': prof,
                     'A分部分项合价': A, 'A.1甲供材料费': A1, 'B措施项目': B,
                     'B.1安全生产措施费': B1, 'C其他项目': C, 'C.1暂列金额': C1,
                     'C.2专业工程暂估价': C2, 'D税前造价': D, 'E增值税9%': E,
                     '总价合计': T, '验①A+B+C=D': chk1,
                     '验②(D-A1)×9%=E': chk2, '验③D-A1+E=总价': chk3})
    wb = Workbook(); ws = wb.active; ws.title = '造价汇总计算表'
    h = list(rows[0].keys())
    ws.append(h)
    for c in range(1, len(h) + 1):
        cell = ws.cell(1, c)
        cell.fill = HDR_FILL; cell.font = HDR_FONT
        cell.alignment = Alignment('center', 'center', wrap_text=True)
        cell.border = BORDER
    for r in rows:
        ws.append([r[k] for k in h])
    ws.append(['', '总计', '', *[round(sum(x[k] for x in rows), 2)
                                 for k in h[3:]]])
    lr = ws.max_row
    for r in range(2, lr + 1):
        is_t = ws.cell(r, 2).value == '总计'
        for c in range(1, len(h) + 1):
            cell = ws.cell(r, c)
            cell.border = BORDER
            cell.font = TOT_FONT if is_t else BODY
            if is_t: cell.fill = TOT_FILL
            if h[c - 1].startswith('验') or h[c - 1] in (
                    'A分部分项合价', 'A.1甲供材料费', 'B措施项目', 'B.1安全生产措施费',
                    'C其他项目', 'C.1暂列金额', 'C.2专业工程暂估价',
                    'D税前造价', 'E增值税9%', '总价合计'):
                cell.number_format = MONEY
                cell.alignment = Alignment('right', 'center')
    for i, k in enumerate(h, 1):
        ws.column_dimensions[get_column_letter(i)].width = \
            9 if k == '分册' else 16 if k == '单项工程' else \
            17 if k == '单位工程' else 15
    _defuse_formulas(ws)
    ws.freeze_panes = 'B2'
    tag = '审核值' if DISC == '4' else '送审值'
    out = os.path.join(OUT, f'07-工程造价汇总计算表({tag}).xlsx')
    wb.save(out)
    print('生成:', out)
    print(f"\n{'分册':<6}{'单位工程':<20}{'分部分项':>13}{'措施':>10}{'其他':>12}{'税前':>13}{'增值税':>11}{'总价':>13}  验①②③")
    for r in rows:
        ok = '通过' if abs(r['验①A+B+C=D']) < 0.05 and abs(r['验②(D-A1)×9%=E']) < 0.05 \
                and abs(r['验③D-A1+E=总价']) < 0.05 else '不通过'
        print(f"{r['分册']:<6}{r['单项工程'][:4]+'-'+r['单位工程']:<20}"
              f"{r['A分部分项合价']:>13,.2f}{r['B措施项目']:>10,.0f}{r['C其他项目']:>12,.0f}"
              f"{r['D税前造价']:>13,.2f}{r['E增值税9%']:>11,.2f}{r['总价合计']:>13,.2f}  {ok}")
    T = sum(r['总价合计'] for r in rows)
    ref = os.environ.get("REF_TOTAL")
    if ref:
        print(f"\n12 个单位工程总价合计 = {T:,.2f}")
        print(f"汇总表工程总额       = {float(ref):,.2f}   差 = {T-float(ref):+,.2f}")
    else:
        print(f"\n12 个单位工程总价合计 = {T:,.2f}"
              "  （可用环境变量 REF_TOTAL 传入汇总表总额做交叉验证）")


if __name__ == '__main__':
    main()
