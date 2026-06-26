# build_excel.py — 招聘进度 Excel 生成脚本

## 使用方法

将下方脚本写入 `/tmp/build_excel.py`，然后执行：

```bash
python3 /tmp/build_excel.py --workspace "$(pwd)" --payload /tmp/hiring_payload.json
```

参数：
- `--workspace` — 工作目录（输出 Excel 和读取人工更正文件的位置）
- `--payload` — JSON payload 文件路径（如省略，自动使用 workspace 中最新的 `feishu_payload*.json`）

## 前置依赖

```bash
pip install openpyxl
```

## 输出

- `西湖数智-招聘进度.xlsx` — 3-sheet 工作簿
- stdout 输出 JSON 摘要：行数、已应用更正、未映射职位、各类统计

## 脚本源码

```python
#!/usr/bin/env python3
"""
Build/refresh the 西湖数智-招聘进度.xlsx report.

Usage:
    python build_excel.py --payload <path-to-rows.json> --workspace <workspace-dir>
"""
import argparse, json, re, sys, os, glob
from collections import defaultdict
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUTPUT_FILENAME = "西湖数智-招聘进度.xlsx"
OVERRIDES_FILENAME = "招聘进度_人工更正.json"

# ============================================================
# Position normalization
# ============================================================

def normalize_position(p: str) -> str:
    if not p: return "(未填写)"
    s = p.strip()
    s = re.sub(r"[（(].*?[)）]", "", s).strip()
    s = re.sub(r"\s+", " ", s)
    for sep in (" & ", "&", " - ", "-", "、", " or ", "or"):
        s = s.replace(sep, "/")
    s = re.sub(r"/+", "/", s).strip("/").strip()
    return s

CANONICAL = {
    "视觉设计": "视觉设计 & 视频制作专员",
    "视觉设计/视频制作专员": "视觉设计 & 视频制作专员",
    "数据科学家": "数据科学家",
    "数据专家": "数据科学家",
    "数据专家/科学家": "数据科学家",
    "数据分析师/数据科学家": "数据科学家",
    "数据工程师": "数据科学家",
    "数据算法工程师": "数据科学家",
    "模型训练专家": "模型训练专家",
    "模型训练工程师": "模型训练专家",
    "模型训练专家/模型训练工程师": "模型训练专家",
    "模型训练工程师/模型训练专家": "模型训练专家",
    "数据专家/模型训练专家": "模型训练专家",
    "AI 工程师": "模型训练专家",
    "Infra专家/训练加速工程师": "Infra 专家",
    "模型训练工程师 infra训练专家": "Infra 专家",
    "具身算法专家": "具身算法专家",
    "具身智能仿真算法工程师": "具身算法专家",
    "未表明。机器人学习方向": "具身算法专家",
    "运动控制算法工程师": "运动控制算法工程师",
    "运动控制算法工程师/具身算法专家": "运动控制算法工程师",
    "硬件控制算法实习生": "运动控制算法工程师",
    "硬件测试工程师": "硬件测试工程师",
    "硬件全栈专家": "硬件全栈专家",
    "全栈工程师": "硬件全栈专家",
    "移动开发工程师": "硬件全栈专家",
    "算法工程师/数据科学家": "算法工程师",
    "算法工程师/数据分析师": "算法工程师",
    "公关": "公关",
    "商务拓展": "商务拓展",
    "(未填写)": "(未填写)",
}

CANONICAL_ORDER = [
    "视觉设计 & 视频制作专员", "数据科学家", "模型训练专家",
    "具身算法专家", "运动控制算法工程师", "硬件全栈专家",
    "硬件测试工程师", "Infra 专家", "算法工程师",
    "公关", "商务拓展", "(未填写)",
]

def canonicalize(raw_position: str):
    norm = normalize_position(raw_position)
    if norm in CANONICAL:
        return CANONICAL[norm], None
    return norm, norm

# ============================================================
# Manual overrides
# ============================================================
def apply_overrides(rows_by_serial: dict, overrides: dict):
    def get_list(key):
        node = overrides.get(key, {})
        return set(node.get("审批编号", []) if isinstance(node, dict) else node)

    r1 = get_list("rejected_after_round_1")
    r2 = get_list("rejected_after_round_2")
    r3 = get_list("rejected_after_round_3")
    rscreen = get_list("rejected_after_screening")
    withdrawn = get_list("withdrawn")

    applied = []
    for serial, row in rows_by_serial.items():
        if serial in r1:
            row["status"] = "拒绝"; row["node_r1"] = "拒绝"
            row["node_r2"] = ""; row["node_r3"] = ""; row["node_handle"] = ""
            applied.append(("R1拒", serial, row.get("name","")))
        elif serial in r2:
            row["status"] = "拒绝"; row["node_r2"] = "拒绝"
            row["node_r3"] = ""; row["node_handle"] = ""
            applied.append(("R2拒", serial, row.get("name","")))
        elif serial in r3:
            row["status"] = "拒绝"; row["node_r3"] = "拒绝"; row["node_handle"] = ""
            applied.append(("R3拒", serial, row.get("name","")))
        elif serial in rscreen:
            row["status"] = "拒绝"; row["node_resume_screen"] = "拒绝"
            row["node_r1"] = ""; row["node_r2"] = ""; row["node_r3"] = ""; row["node_handle"] = ""
            applied.append(("简筛拒", serial, row.get("name","")))
        elif serial in withdrawn:
            row["status"] = "撤回"
            applied.append(("撤回", serial, row.get("name","")))
    return applied

# ============================================================
# Excel build
# ============================================================
HEADER_FONT = Font(name='Arial', bold=True, color='FFFFFF', size=11)
HEADER_FILL = PatternFill('solid', fgColor='4472C4')
TOTALS_FONT = Font(name='Arial', bold=True)
TOTALS_FILL = PatternFill('solid', fgColor='D9E1F2')
BORDER = Border(left=Side(style='thin', color='B0B0B0'), right=Side(style='thin', color='B0B0B0'),
                top=Side(style='thin', color='B0B0B0'), bottom=Side(style='thin', color='B0B0B0'))
CENTER = Alignment(horizontal='center', vertical='center')
LEFT = Alignment(horizontal='left', vertical='center')

SHEET1_HEADERS = ['#','审批编号','当前状态','提交时间','完结时间','姓名','申请职位',
                  '手机号','邮箱','毕业院校','曾经任职','CV',
                  '简历筛查-状态','一面-状态','二面-状态','三面-状态','办理-状态']
SHEET1_WIDTHS = [4,14,10,16,16,10,22,16,24,20,35,28,12,10,10,10,10]

SHEET2_HEADERS = ['候选人','申请职位','审批编号','节点','类型','状态','开始','结束','审批人(末8位oid)']
SHEET2_WIDTHS = [10,22,14,10,8,10,16,16,14]

SHEET3_HEADERS = ['职位类别','投递人数','面试进行中','通过简历筛选','通过一面','通过二面','通过三面','发放Offer']
SHEET3_WIDTHS = [22,11,13,14,11,11,11,11]


def build(payload: dict, workspace_dir: str):
    rows = payload["rows"]
    rows_by_serial = {r["serial"]: r for r in rows if r.get("serial")}

    overrides_path = os.path.join(workspace_dir, OVERRIDES_FILENAME)
    overrides = {}
    if os.path.exists(overrides_path):
        with open(overrides_path, "r", encoding="utf-8") as f:
            overrides = json.load(f)
    applied = apply_overrides(rows_by_serial, overrides)

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # Sheet 1
    ws1 = wb.create_sheet("审批总览")
    ws1.append(SHEET1_HEADERS)
    for idx, r in enumerate(rows, 1):
        ws1.append([
            idx, r.get("serial",""), r.get("status",""), r.get("submit_time",""), r.get("end_time",""),
            r.get("name",""), r.get("position",""), r.get("phone",""), r.get("email",""),
            r.get("school",""), r.get("prior_jobs",""), r.get("cv",""),
            r.get("node_resume_screen",""), r.get("node_r1",""), r.get("node_r2",""),
            r.get("node_r3",""), r.get("node_handle","")
        ])
    _style_header(ws1, SHEET1_HEADERS, SHEET1_WIDTHS)
    ws1.freeze_panes = "A2"

    # Sheet 2
    ws2 = wb.create_sheet("节点流转明细")
    ws2.append(SHEET2_HEADERS)
    for r in rows:
        for t in r.get("tasks", []):
            ws2.append([
                r.get("name",""), r.get("position",""), r.get("serial",""),
                t.get("node_name",""), t.get("type",""), t.get("status",""),
                t.get("start",""), t.get("end",""), t.get("approver_oid8","")
            ])
    _style_header(ws2, SHEET2_HEADERS, SHEET2_WIDTHS)
    ws2.freeze_panes = "A2"

    # Sheet 3
    ws3 = wb.create_sheet("职位投递汇总")
    ws3.append(SHEET3_HEADERS)

    groups = defaultdict(lambda: {'total':0,'in_progress':0,'screen':0,'r1':0,'r2':0,'r3':0,'offer':0})
    unmapped = set()
    for r in rows:
        canon, unmapped_form = canonicalize(r.get("position",""))
        if unmapped_form:
            unmapped.add(unmapped_form)
        g = groups[canon]
        g['total'] += 1
        if r.get("status") == "待审批": g['in_progress'] += 1
        if r.get("node_resume_screen") == "通过": g['screen'] += 1
        if r.get("node_r1") == "通过": g['r1'] += 1
        if r.get("node_r2") == "通过": g['r2'] += 1
        if r.get("node_r3") == "通过": g['r3'] += 1
        if r.get("status") == "通过": g['offer'] += 1

    order = list(CANONICAL_ORDER) + sorted(c for c in groups if c not in CANONICAL_ORDER)
    for canon in order:
        if canon not in groups: continue
        g = groups[canon]
        ws3.append([canon, g['total'], g['in_progress'], g['screen'], g['r1'], g['r2'], g['r3'], g['offer']])

    last_data_row = ws3.max_row
    totals_row = last_data_row + 1
    ws3.cell(totals_row, 1, '合计')
    n_cols = len(SHEET3_HEADERS)
    for col in range(2, n_cols + 1):
        L = get_column_letter(col)
        ws3.cell(totals_row, col, f'=SUM({L}2:{L}{last_data_row})')

    _style_header(ws3, SHEET3_HEADERS, SHEET3_WIDTHS)
    for col in range(1, n_cols + 1):
        c = ws3.cell(totals_row, col); c.font = TOTALS_FONT; c.fill = TOTALS_FILL
        c.alignment = LEFT if col==1 else CENTER; c.border = BORDER
    ws3.freeze_panes = "A2"

    out_path = os.path.join(workspace_dir, OUTPUT_FILENAME)
    wb.save(out_path)

    print(json.dumps({
        "ok": True,
        "output_path": out_path,
        "n_rows": len(rows),
        "n_overrides_applied": len(applied),
        "overrides_applied": [{"kind":k, "serial":s, "name":n} for k,s,n in applied],
        "unmapped_positions": sorted(unmapped),
        "summary": {
            canon: {k: groups[canon][k] for k in ['total','in_progress','screen','r1','r2','r3','offer']}
            for canon in order if canon in groups
        }
    }, ensure_ascii=False, indent=2))


def _style_header(ws, headers, widths):
    for col_idx, h in enumerate(headers, 1):
        c = ws.cell(1, col_idx)
        c.font = HEADER_FONT; c.fill = HEADER_FILL; c.alignment = CENTER; c.border = BORDER
    for col_idx, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = w
    for r in range(2, ws.max_row+1):
        for col_idx in range(1, len(headers)+1):
            c = ws.cell(r, col_idx); c.font = Font(name='Arial', size=11)
            c.alignment = LEFT if col_idx==1 else CENTER
            c.border = BORDER


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--payload", help="JSON payload file")
    ap.add_argument("--workspace", required=True, help="Workspace directory")
    args = ap.parse_args()

    payload_path = args.payload
    if not payload_path:
        candidates = glob.glob(os.path.join(args.workspace, "feishu_payload*.json"))
        if not candidates:
            sys.exit(f"No feishu_payload*.json found in {args.workspace}")
        payload_path = max(candidates, key=os.path.getmtime)
        print(f"# Using newest payload: {os.path.basename(payload_path)}", file=sys.stderr)

    with open(payload_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    build(payload, args.workspace)
```
