"""生成月度财税台账.xlsx + 异常票据清单。"""
import os

import openpyxl

import config


def build(records, out_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "月度财税台账"
    ws.append(config.LEDGER_HEADER)

    abnormal_ws = wb.create_sheet("异常票据清单")
    abnormal_ws.append(["源文件", "票据状态", "风险备注", "发票号码", "销售方"])

    for r in records:
        if r.get("票据状态") in ("异常", "待确认"):
            abnormal_ws.append([
                r.get("_src", ""),
                r.get("票据状态", ""),
                r.get("风险备注", ""),
                r.get("发票号码", ""),
                r.get("销售方名称", ""),
            ])
            continue
        ws.append([
            r.get("开票日期", ""),
            r.get("发票类型", ""),
            r.get("销售方名称", ""),
            r.get("不含税金额", ""),
            r.get("税额", ""),
            r.get("价税合计", ""),
            r.get("发票号码", ""),
            r.get("票据状态", ""),
            r.get("所属月份", ""),
            r.get("风险备注", ""),
        ])

    # 合计行
    total_amount = sum(float(r.get("价税合计") or 0) for r in records
                       if r.get("票据状态") not in ("异常", "待确认"))
    total_tax = sum(float(r.get("税额") or 0) for r in records
                    if r.get("票据状态") not in ("异常", "待确认"))
    ws.append(["合计", "", "", "", round(total_tax, 2), round(total_amount, 2), "", "", "", ""])

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    wb.save(out_path)
    return out_path
