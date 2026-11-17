"""校验：勾稽关系 + 格式 + 分类 + 风险备注。"""
import re

import config
import utils


def classify_type(fields):
    t = fields.get("发票类型", "") or ""
    if "专用" in t:
        return "增值税专用发票"
    if "电子" in t or "增值税电子" in t:
        return "电子普通发票"
    if "定额" in t:
        return "定额发票"
    if "普通" in t:
        return "纸质普通发票"
    return "待确认"


def validate(fields):
    remarks = []
    status = "正常"

    ht = utils.parse_amount(fields.get("不含税金额"))
    tax = utils.parse_amount(fields.get("税额"))
    total = utils.parse_amount(fields.get("价税合计"))
    if None not in (ht, tax, total):
        if abs((ht + tax) - total) > 0.01:
            remarks.append("价税合计≠不含税金额+税额")
            status = "异常"
    elif total is None:
        remarks.append("缺少价税合计")
        status = "异常"

    num = (fields.get("发票号码") or "").strip()
    if num and not re.fullmatch(r"\d{8,20}", num):
        remarks.append("发票号码格式异常")
        status = "异常"

    # 仅校验台账必需字段（发票代码不在表头，不强制）
    for k in ("发票号码", "开票日期", "价税合计", "销售方名称"):
        if not fields.get(k):
            remarks.append(f"缺{k}")
            if status != "异常":
                status = "异常"

    itype = classify_type(fields)
    if itype == "待确认":
        remarks.append("发票类型未能识别")
        if status != "异常":
            status = "待确认"

    return status, remarks, itype


def month_of(fields):
    return utils.month_of(fields.get("开票日期"))
