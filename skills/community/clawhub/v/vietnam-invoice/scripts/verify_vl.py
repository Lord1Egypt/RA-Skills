"""越南发票验真 - VL 模型自动提取字段 + API 验真

用法:
    # 完整模式: VL 提取 + 验真
    python verify_vl.py invoice.jpg

    # 直接模式: 跳过 VL 提取，直接验真 (Claude 已提取字段时使用)
    python verify_vl.py --direct --nbmst X --khhdon Y --shdon Z --khmshdon 1 --hdon 01

    # 仅提取字段
    python verify_vl.py --extract-only invoice.jpg

环境变量:
    VL_API_KEY   - 百炼平台 API Key (必填，完整模式需要)
    CJY_USER     - 超级鹰用户名 (必填)
    CJY_PASS     - 超级鹰密码 (必填)
    VL_BASE_URL  - VL API 地址 (默认: https://dashscope.aliyuncs.com/compatible-mode/v1)
    VL_MODEL     - 模型名称 (默认: qwen3-vl-30b-a3b-instruct)
    CJY_SOFTID   - 超级鹰软件ID (默认: 96001)
    CJY_CODETYPE - 验证码类型 (默认: 1902)
"""

import argparse
import base64
import io
import json
import os
import re
import sys

import requests
import urllib3
from openai import OpenAI
from playwright.sync_api import sync_playwright

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== 配置 ====================

# 越南税务 API
TAX_API = "https://hoadondientu.gdt.gov.vn:30000"
CAPTCHA_URL = f"{TAX_API}/captcha"
QUERY_URL = f"{TAX_API}/query/guest-invoices"
MAX_RETRIES = 5

# 超级鹰
CJY_USER = os.environ.get("CJY_USER", "")
CJY_PASS = os.environ.get("CJY_PASS", "")
CJY_SOFTID = int(os.environ.get("CJY_SOFTID", "96001"))
CJY_CODETYPE = int(os.environ.get("CJY_CODETYPE", "1902"))

# VL 模型 (阿里云百炼 Qwen-VL)
VL_BASE_URL = os.environ.get("VL_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
VL_API_KEY = os.environ.get("VL_API_KEY", "")
VL_MODEL = os.environ.get("VL_MODEL", "qwen3-vl-30b-a3b-instruct")

# ==================== 状态映射 (来自前端 JS 源码) ====================

TTHAI_MAP = {
    1: "新发票", 2: "替换发票", 3: "调整发票",
    4: "已被替换", 5: "已被调整", 6: "已作废",
}

TTXLY_MAP = {
    1: "等待处理", 2: "已拒绝", 3: "处理中",
    4: "已处理", 5: "已签发（已赋码）",
    6: None, 7: None, 8: "已发送审核通知", 9: "已发送审核通知",
}

# ==================== VL 字段提取 ====================

EXTRACT_PROMPT = """\
你是一个越南发票字段提取专家。请仔细分析这张越南发票图片，提取以下字段并以 JSON 格式返回：
{
    "nbmst": "卖家税号 (Mã số thuế)，10位数字",
    "khhdon": "发票符号 (Ký hiệu hóa đơn)，如 1C25TTT",
    "shdon": "发票号码 (Số hóa đơn)，纯数字",
    "khmshdon": "模板号，整数",
    "hdon": "发票类型代码，如 01 或 02",
    "tgtthue": "总税额 (Tổng tiền thuế)，纯数字不带分隔符",
    "tgtttbso": "总金额 (Tổng tiền thanh toán)，纯数字不带分隔符",
    "invoice_type": "发票类型名称（越南语原文）"
}
判断发票类型的方法：
- "HÓA ĐƠN GIÁ TRỊ GIA TĂNG" → khmshdon=1, hdon=01
- "HÓA ĐƠN BÁN HÀNG" → khmshdon=2, hdon=02
- "HÓA ĐƠN BÁN TÀI SẢN CÔNG" → khmshdon=3, hdon=03
- "HÓA ĐƠN BÁN HÀNG DỰ TRỮ QUỐC GIA" → khmshdon=4, hdon=04
- "HÓA ĐƠN KHÁC" → khmshdon=5, hdon=05
- "PHIẾU XUẤT KHO KIÊM VẬN CHUYỂN NỘI BỘ" → khmshdon=6, hdon=06_01
- "PHIẾU XUẤT KHO GỬI BÁN HÀNG ĐẠI LÝ" → khmshdon=6, hdon=06_02
- "HOÁ ĐƠN THƯƠNG MẠI" → khmshdon=7, hdon=07
- "HÓA ĐƠN GTGT TÍCH HỢP BIÊN LAI" → khmshdon=8, hdon=08
- "HÓA ĐƠN BÁN HÀNG TÍCH HỢP BIÊN LAI" → khmshdon=9, hdon=09
注意：只返回 JSON，不要返回其他内容。如果某个字段无法识别，设为空字符串。\
"""


def _get_mime_type(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    return {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
            ".gif": "image/gif", ".webp": "image/webp"}.get(ext, "image/jpeg")


def _pdf_to_images(pdf_path: str) -> list[bytes]:
    """将 PDF 每页转为 PNG bytes（委托给 pdf_to_images 子模块）"""
    from pdf_to_images import pdf_to_images as _convert
    result = _convert(pdf_path, dpi=192)
    print(f"[提取] PDF 共 {len(result)} 页，已转为图片", file=sys.stderr)
    return result


def _extract_fields(file_path: str) -> dict:
    """调用 VL 模型提取发票字段，支持图片和 PDF"""
    if not VL_API_KEY:
        _error_exit("VL_API_KEY 环境变量未设置，请在百炼平台获取 API Key")

    ext = os.path.splitext(file_path)[1].lower()
    print(f"[提取] 读取文件: {file_path}", file=sys.stderr)

    image_parts = []
    if ext == ".pdf":
        for png_bytes in _pdf_to_images(file_path):
            b64 = base64.b64encode(png_bytes).decode()
            image_parts.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}"},
            })
    else:
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        image_parts.append({
            "type": "image_url",
            "image_url": {"url": f"data:{_get_mime_type(file_path)};base64,{b64}"},
        })

    print(f"[提取] 调用模型: {VL_MODEL}，共 {len(image_parts)} 张图片", file=sys.stderr)
    client = OpenAI(base_url=VL_BASE_URL, api_key=VL_API_KEY)
    resp = client.chat.completions.create(
        model=VL_MODEL,
        messages=[{
            "role": "user",
            "content": [{"type": "text", "text": EXTRACT_PROMPT}] + image_parts,
        }],
        max_tokens=1024,
        temperature=0.0,
    )

    text = resp.choices[0].message.content.strip()
    if text.startswith("```"):
        text = "\n".join(l for l in text.split("\n") if not l.strip().startswith("```"))

    try:
        fields = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[^{}]+\}", text, re.DOTALL)
        if m:
            fields = json.loads(m.group())
        else:
            raise ValueError(f"VL 模型返回无法解析:\n{text}")

    print("[提取] 完成:", file=sys.stderr)
    for k, v in fields.items():
        print(f"  {k}: {v}", file=sys.stderr)
    return fields


# ==================== 请求重试 ====================

REQUEST_RETRIES = 3


def _request(method, url, retries=REQUEST_RETRIES, **kwargs):
    """带重试的 requests 调用，最多重试 retries 次"""
    kwargs.setdefault("timeout", 30)
    for i in range(1, retries + 1):
        try:
            resp = method(url, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            print(f"  [请求] {url} 第 {i}/{retries} 次失败: {e}", file=sys.stderr)
            if i == retries:
                raise
    return None  # unreachable


# ==================== 验证码 & 验真 ====================

def _get_captcha() -> dict:
    resp = _request(requests.get, CAPTCHA_URL, retries=REQUEST_RETRIES, verify=False, timeout=15)
    return resp.json()


def _svg_to_png(svg: str) -> bytes:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 250, "height": 60})
        page.set_content(
            f'<html><body style="margin:0;padding:4px;background:white;">{svg}</body></html>'
        )
        el = page.query_selector("svg")
        png = el.screenshot() if el else page.screenshot(full_page=True)
        browser.close()
    return png


def _recognize_captcha(png: bytes) -> str:
    if not CJY_USER or not CJY_PASS:
        _error_exit("超级鹰账号未配置，请设置 CJY_USER 和 CJY_PASS 环境变量")
    b64 = base64.b64encode(png).decode()
    resp = _request(requests.post,
        "https://upload.chaojiying.net/Upload/Processing.php",
        retries=REQUEST_RETRIES,
        json={"user": CJY_USER, "pass": CJY_PASS, "softid": CJY_SOFTID,
              "codetype": CJY_CODETYPE, "file_base64": b64},
        timeout=30,
    )
    data = resp.json()
    if data.get("err_no") != 0:
        raise RuntimeError(f"超级鹰识别失败: {data}")
    return data["pic_str"]


def _parse_result(data: dict) -> dict:
    """解析 API 响应，返回验真结果"""
    tthai = data.get("tthai")
    ttxly = data.get("ttxly")
    invoice_exists = tthai is not None or ttxly is not None

    if not invoice_exists:
        return {
            "is_authentic": False, "invoice_exists": False,
            "invoice_status": None, "processing_status": None,
            "detail": "发票不存在", "raw_data": data,
        }

    invoice_status = TTHAI_MAP.get(tthai, f"未知状态({tthai})")
    processing_status = TTXLY_MAP.get(ttxly, f"未知状态({ttxly})") or ""

    is_illegal = data.get("bhphap") == 1
    is_cancelled = tthai == 6
    is_issued = ttxly == 5
    is_replaced = tthai == 4
    is_adjusted = tthai == 5
    is_authentic = invoice_exists and not is_cancelled and not is_illegal

    detail = f"发票存在 - 处理状态: {processing_status}"
    if is_illegal:
        detail = "非法发票"
    elif is_cancelled:
        detail = "发票已作废"
    elif is_replaced:
        detail = "发票已被替换"
    elif is_adjusted:
        detail = "发票已被调整"
    elif not is_issued:
        detail = f"发票尚未签发: {processing_status}"

    result = {
        "is_authentic": is_authentic,
        "invoice_exists": invoice_exists,
        "invoice_status": invoice_status,
        "processing_status": processing_status,
        "tthai": tthai,
        "ttxly": ttxly,
        "detail": detail,
        "raw_data": data,
    }
    for key in ("kqcht", "pdndungs", "hdonLquans"):
        val = data.get(key)
        if val:
            result[{"kqcht": "error_info", "pdndungs": "reasons",
                    "hdonLquans": "related_invoices"}[key]] = val
    return result


def _query_invoice(nbmst, khhdon, shdon, khmshdon, hdon, tgtttbso="", tgtthue=""):
    """查询发票，自动处理验证码重试"""
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"[验真] 尝试 {attempt}/{MAX_RETRIES}...", file=sys.stderr)

        captcha_data = _get_captcha()
        captcha_text = _recognize_captcha(_svg_to_png(captcha_data["content"]))
        print(f"  验证码: {captcha_text}", file=sys.stderr)

        params = {
            "khmshdon": khmshdon, "hdon": hdon, "nbmst": nbmst,
            "khhdon": khhdon, "shdon": shdon, "tgtttbso": tgtttbso,
            "tgtthue": tgtthue,
            "cvalue": captcha_text, "ckey": captcha_data["key"],
        }
        print(f"  请求参数: {json.dumps(params, ensure_ascii=False)}", file=sys.stderr)

        resp = _request(requests.get, QUERY_URL, retries=REQUEST_RETRIES,
                        params=params, verify=False, timeout=60)
        print(f"  响应状态: {resp.status_code}", file=sys.stderr)

        if not resp.text.strip():
            return _parse_result({})

        data = resp.json()
        msg = data.get("message", "")
        if "captcha" in msg.lower() or "mã captcha" in msg.lower():
            print("  验证码错误，重试...", file=sys.stderr)
            continue

        return _parse_result(data)

    return {"is_authentic": False, "invoice_exists": False,
            "detail": f"验证码识别失败，已重试 {MAX_RETRIES} 次"}


# ==================== 公开接口 ====================

def verify_direct(nbmst, khhdon, shdon, khmshdon, hdon, tgtttbso="", tgtthue=""):
    """直接验真模式：跳过 VL 提取，使用已提取的字段直接查询"""
    # khhdon 去掉首位数字 (发票上的 Ký hiệu 包含模板号前缀，API 只需要符号部分)
    if khhdon:
        print(f"  khhdon 去除前缀: {khhdon} -> {khhdon[1:]}", file=sys.stderr)
        khhdon = khhdon[1:]

    return _query_invoice(
        nbmst=str(nbmst), khhdon=str(khhdon), shdon=str(shdon),
        khmshdon=str(khmshdon), hdon=str(hdon), tgtttbso=str(tgtttbso),
        tgtthue=str(tgtthue),
    )


def verify_invoice(image, nbmst=None, khhdon=None, shdon=None,
                   khmshdon=None, hdon=None, extract_only=False):
    """完整验真模式：VL 提取字段 + API 验真"""
    if not os.path.isfile(image):
        _error_exit(f"文件不存在: {image}")

    fields = _extract_fields(image)

    for key, val in [("nbmst", nbmst), ("khhdon", khhdon), ("shdon", shdon),
                     ("khmshdon", khmshdon), ("hdon", hdon)]:
        if val:
            fields[key] = val

    khhdon_val = str(fields.get("khhdon", ""))
    if khhdon_val and khhdon_val[0].isdigit():
        fields["khhdon"] = khhdon_val[1:]
        print(f"  khhdon 去除前缀: {khhdon_val} -> {fields['khhdon']}", file=sys.stderr)

    if extract_only:
        return {"success": True, "fields": fields}

    for key in ["nbmst", "khhdon", "shdon", "khmshdon", "hdon"]:
        if not fields.get(key):
            return {"is_authentic": False, "invoice_exists": False,
                    "detail": f"缺少必填字段: {key}"}

    return _query_invoice(
        nbmst=str(fields["nbmst"]), khhdon=str(fields["khhdon"]),
        shdon=str(fields["shdon"]), khmshdon=str(fields["khmshdon"]),
        hdon=str(fields["hdon"]), tgtttbso=str(fields.get("tgtttbso", "")),
        tgtthue=str(fields.get("tgtthue", "")),
    )


def _error_exit(msg):
    print(f"错误: {msg}", file=sys.stderr)
    sys.exit(1)


def _check_env(direct_mode=False):
    """检查必要的环境变量"""
    missing = []
    if not CJY_USER:
        missing.append("CJY_USER (超级鹰用户名)")
    if not CJY_PASS:
        missing.append("CJY_PASS (超级鹰密码)")
    if not direct_mode and not VL_API_KEY:
        missing.append("VL_API_KEY (百炼平台 API Key)")
    if missing:
        _error_exit("以下环境变量未设置:\n  " + "\n  ".join(missing))


# ==================== CLI ====================

def main():
    parser = argparse.ArgumentParser(
        description="越南发票验真",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  # 完整模式\n"
               "  python verify_vl.py invoice.jpg\n"
               "  # 直接验真 (跳过 VL 提取)\n"
               "  python verify_vl.py --direct --nbmst 0101234567 --khhdon C25TTT --shdon 123 --khmshdon 1 --hdon 01\n"
               "  # 仅提取字段\n"
               "  python verify_vl.py --extract-only invoice.jpg\n",
    )

    # 直接验真模式参数
    parser.add_argument("--direct", action="store_true",
                        help="直接验真模式，需提供所有字段参数")
    parser.add_argument("--nbmst", help="卖家税号 (Mã số thuế)")
    parser.add_argument("--khhdon", help="发票符号 (Ký hiệu hóa đơn)")
    parser.add_argument("--shdon", help="发票号码 (Số hóa đơn)")
    parser.add_argument("--khmshdon", help="模板号")
    parser.add_argument("--hdon", help="发票类型代码")
    parser.add_argument("--tgtttbso", default="", help="总金额 (可选)")
    parser.add_argument("--tgtthue", default="", help="总税额 (可选)")

    # 完整模式参数
    parser.add_argument("--extract-only", action="store_true",
                        help="仅提取字段，不验真")
    parser.add_argument("image", nargs="?", help="发票文件路径 (JPG/PNG/PDF)")

    args = parser.parse_args()

    if args.direct:
        # 直接验真模式
        for key in ("nbmst", "khhdon", "shdon", "khmshdon", "hdon"):
            if not getattr(args, key):
                _error_exit(f"直接验真模式需要 --{key} 参数")
        _check_env(direct_mode=True)
        result = verify_direct(
            nbmst=args.nbmst, khhdon=args.khhdon, shdon=args.shdon,
            khmshdon=args.khmshdon, hdon=args.hdon, tgtttbso=args.tgtttbso,
            tgtthue=args.tgtthue,
        )
    elif args.image:
        # 完整模式
        _check_env(direct_mode=False)
        result = verify_invoice(
            args.image, extract_only=args.extract_only,
            nbmst=args.nbmst, khhdon=args.khhdon, shdon=args.shdon,
            khmshdon=args.khmshdon, hdon=args.hdon,
        )
    else:
        parser.print_help()
        sys.exit(1)

    # 输出 JSON 结果到 stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
