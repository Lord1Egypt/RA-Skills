"""字段抽取：OCR规则优先，本地 VLM 仅作辅助兜底（补缺失字段的定位）。"""
import os
import re
import json
import base64

import config
import utils
# ocr_engine / requests 均为懒加载（见 extract / call_vlm），避免重型依赖污染导入期

# 关键词定位：在 OCR 文本行里找 "标签:值"
def _find_after(text_lines, label_re):
    for ln in text_lines:
        t = ln["text"]
        m = re.search(label_re + r"\s*[:：]?\s*(.+)", t)
        if m:
            return m.group(1).strip(), ln["conf"]
    return None, None


def extract_by_rules(lines):
    blob = "\n".join(l["text"] for l in lines)
    fields = {}
    conf = {}

    # 发票类型（从整段文本判断）
    if "增值税专用发票" in blob:
        fields["发票类型"], conf["发票类型"] = "增值税专用发票", 1.0
    elif "增值税电子普通发票" in blob or "电子普通发票" in blob:
        fields["发票类型"], conf["发票类型"] = "电子普通发票", 1.0
    elif "定额发票" in blob:
        fields["发票类型"], conf["发票类型"] = "定额发票", 1.0
    elif "增值税普通发票" in blob or "普通发票" in blob:
        fields["发票类型"], conf["发票类型"] = "纸质普通发票", 1.0

    code, c1 = _find_after(lines, r"发票代码")
    if code:
        fields["发票代码"], conf["发票代码"] = code, c1
    num, c2 = _find_after(lines, r"发票号码")
    if num:
        fields["发票号码"], conf["发票号码"] = re.sub(r"\D", "", num), c2

    date_raw, c3 = _find_after(lines, r"开票日期")
    if date_raw:
        fields["开票日期"], conf["开票日期"] = utils.parse_date(date_raw), c3

    for label, key in [("价税合计", "价税合计"), ("不含税金额", "不含税金额"),
                       ("税额", "税额"), ("税率", "税率")]:
        val, c = _find_after(lines, label)
        if val is not None:
            fields[key] = utils.parse_amount(val) if key != "税率" else val
            conf[key] = c

    seller, c4 = _find_after(lines, r"销售方|销货单位|收款人|名称")
    if seller:
        fields["销售方名称"], conf["销售方名称"] = seller, c4

    return fields, conf


VLM_PROMPT = (
    "你是发票字段抽取助手。下面这张发票图，请逐字抄录，不要推断或补全。"
    "仅输出 JSON，字段：发票代码,发票号码,开票日期,发票类型,销售方名称,"
    "不含税金额,税额,价税合计,税率。数字保留原文，日期格式 YYYY-MM-DD。"
)

VLM_SCHEMA = {
    "type": "object",
    "properties": {
        "发票代码": {"type": "string"},
        "发票号码": {"type": "string"},
        "开票日期": {"type": "string"},
        "发票类型": {"type": "string"},
        "销售方名称": {"type": "string"},
        "不含税金额": {"type": "number"},
        "税额": {"type": "number"},
        "价税合计": {"type": "number"},
        "税率": {"type": "string"},
    },
}


def call_vlm(image_path):
    """调用本地 Ollama 多模态模型，仅用于补缺失字段。"""
    import requests
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {
        "model": config.VLM_MODEL,
        "messages": [{"role": "user", "content": VLM_PROMPT, "images": [b64]}],
        "format": VLM_SCHEMA,
        "stream": False,
    }
    r = requests.post(config.OLLAMA_API, json=payload, timeout=180)
    r.raise_for_status()
    return json.loads(r.json()["message"]["content"])


def extract(image_path):
    """返回 (fields, method)。OCR规则优先；关键数字缺失时本地 VLM 辅助。"""
    from ocr_engine import ocr_file
    lines = ocr_file(image_path)
    fields, conf = extract_by_rules(lines)
    method = "ocr+rules"

    missing = [k for k in ("发票号码", "价税合计", "税额", "不含税金额") if not fields.get(k)]
    if missing:
        try:
            vlm = call_vlm(image_path)
            for k, v in vlm.items():
                # VLM 仅补缺失字段；已用 OCR 得到的数字不覆盖
                if not fields.get(k) and v not in (None, ""):
                    fields[k] = v
            method = "ocr+vlm(辅助兜底)"
        except Exception as e:
            method = f"ocr-only(VLM不可用:{e})"
    return fields, method
