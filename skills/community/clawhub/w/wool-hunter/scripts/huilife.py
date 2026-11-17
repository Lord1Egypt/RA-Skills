#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
惠生活外卖红包查询 (移植自 YKred/waimaiquan-skill, Node -> Python 标准库)
覆盖美团/饿了么/京东外卖/淘宝闪购隐藏红包与优惠活动。

用法:
    python huilife.py                       # 查优惠活动 (projects)
    python huilife.py --coupons             # 查优惠券列表 (coupons)
    python huilife.py --section 外卖         # 按板块筛选 (如 外卖/美团)
    python huilife.py --format text         # 纯文本输出
    python huilife.py --json                # JSON 原始输出

签名规则 (HMAC-SHA256):
    1. 除 signature 外所有参数按参数名 ASCII 升序排列
    2. 拼接成 key=value 用 & 连接, 末尾追加 &secret=SECRET_KEY
    3. 用 SECRET_KEY 对该串做 HMAC-SHA256, 结果转 16 进制小写即签名
"""

import os
import sys
import json
import time
import hmac
import hashlib
import urllib.request
import urllib.error
import urllib.parse

# ---- 配置（必须通过环境变量注入，禁止硬编码密钥）----
API_BASE_URL = os.environ.get(
    "HL_API_BASE_URL",
    "https://backend.appmiaoda.com/projects/supabase300636050605256704/functions/v1/open-api")
ACCESS_KEY = os.environ.get("HL_ACCESS_KEY")
SECRET_KEY = os.environ.get("HL_SECRET_KEY")
SITE_URL = os.environ.get("HL_SITE_URL", "https://app-aujs40uyrf9d.appmiaoda.com")
TIMEOUT = int(os.environ.get("HL_TIMEOUT", "15"))

if not ACCESS_KEY:
    raise RuntimeError("缺少 HL_ACCESS_KEY 环境变量，请设置惠生活 API Access Key")
if not SECRET_KEY:
    raise RuntimeError("缺少 HL_SECRET_KEY 环境变量，请设置惠生活 API Secret Key")

TRIGGER_KEYWORDS = [
    "外卖红包", "外卖优惠", "外卖券", "外卖优惠券",
    "优惠券", "领券", "领红包", "省钱",
    "点外卖", "叫外卖", "外卖", "外卖神券",
    "满减", "满减红包", "折扣", "首单优惠",
    "美团红包", "饿了么红包", "京东外卖",
    "美团外卖", "饿了么外卖",
    "惠生活", "吃什么", "今天吃什么",
]


def generate_signature(params):
    """按 ASCII 升序拼接参数 + secret, HMAC-SHA256 -> hex 小写。"""
    sign_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    sign_str += "&secret=" + SECRET_KEY
    return hmac.new(
        SECRET_KEY.encode("utf-8"),
        sign_str.encode("utf-8"),
        hashlib.sha256).hexdigest()


def _http_get(url):
    """先直连, 失败且环境有代理再试代理 (Windows 沙箱网络适配)。"""
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (huilife-skill)"})
    try:
        with urllib.request.build_opener(
                urllib.request.ProxyHandler({})).open(req, timeout=TIMEOUT) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        if not (os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")):
            raise
        with urllib.request.build_opener().open(req, timeout=TIMEOUT) as r:
            return r.read().decode("utf-8", "replace")


def _request(endpoint, section_name=None):
    """构造签名请求并调用 API, 返回 {success, list, message}。"""
    params = {
        "access_key": ACCESS_KEY,
        "timestamp": str(int(time.time())),
        "page": "1",
        "page_size": "20",
    }
    if section_name:
        params["section_name"] = section_name

    # 签名用原始值(不编码), URL 查询串用百分号编码值
    signature = generate_signature(params)
    qs = "&".join(
        "%s=%s" % (urllib.parse.quote(str(k), safe=""),
                   urllib.parse.quote(str(params[k]), safe=""))
        for k in sorted(params))
    qs += "&signature=" + signature
    url = API_BASE_URL + "/" + endpoint + "?" + qs

    try:
        raw = _http_get(url)
    except Exception as e:
        return {"success": False, "list": [], "message": "网络请求失败: %s" % e}

    try:
        data = json.loads(raw)
    except Exception:
        return {"success": False, "list": [], "message": "响应解析失败"}

    if data.get("code") == 200 and data.get("data"):
        lst = data["data"].get("list")
        return {"success": True, "list": lst if isinstance(lst, list) else [],
                "message": ""}
    return {"success": False, "list": [],
            "message": data.get("message") or ("code=%s" % data.get("code"))}


def _sale_count(n):
    try:
        n = int(n)
    except (TypeError, ValueError):
        return ""
    if n >= 10000:
        return "%.1fw" % (n / 10000)
    if n >= 1000:
        return "%.1fk" % (n / 1000)
    return str(n)


def _date_str():
    t = time.localtime()
    return "%d月%d日" % (t.tm_mon, t.tm_mday)


def render_projects(data):
    """渲染优惠活动列表 (对应上游 renderProjects wechat)。"""
    if not data["success"]:
        return "查询失败: %s" % data["message"]
    lst = data["list"]
    if not lst:
        return "暂无进行中的优惠活动, 换个板块或稍后再试"

    out = "今日羊毛活动已挖出！（%s）\n\n" % _date_str()
    out += "一键领全部红包：\n   %s\n\n" % SITE_URL
    out += "今日必领：\n"
    for i, item in enumerate(lst, 1):
        title = item.get("title") or item.get("name") or "优惠活动"
        section = item.get("section_name") or ""
        desc = item.get("description") or item.get("desc") or ""
        out += "   %d. %s\n" % (i, title)
        if section:
            out += "      板块: %s\n" % section
        if desc:
            out += "      %s\n" % desc
    out += "\n复制到微信打开 -> 一个个领 -> 再点餐"
    return out


def render_coupons(data):
    """渲染优惠券列表 (对应上游 renderCoupons wechat)。"""
    if not data["success"]:
        return "查询失败: %s" % data["message"]
    lst = data["list"]
    if not lst:
        return "暂无可用优惠券, 换个板块或稍后再试"

    out = "今日外卖优惠券已更新！（%s）\n\n" % _date_str()
    out += "一键领全部优惠：\n   %s\n\n" % SITE_URL
    out += "今日优惠券推荐：\n"
    for i, item in enumerate(lst, 1):
        title = item.get("title") or "优惠券"
        final_price = item.get("final_price") or item.get("price") or ""
        coupon_amount = item.get("coupon_amount") or ""
        sale_count = _sale_count(item.get("sale_count", 0))
        out += "   %d. %s\n" % (i, title)
        if coupon_amount:
            line = "      优惠 %s 元" % coupon_amount
            if final_price:
                line += "，到手价 %s 元" % final_price
            out += line + "\n"
        elif final_price:
            out += "      到手价 %s 元\n" % final_price
        if sale_count:
            out += "      已售 %s 件\n" % sale_count
    out += "\n复制到微信打开 -> 领券 -> 再点餐"
    return out


def render_text(data, kind):
    """纯文本/终端友好输出 (对应上游 renderXxxText)。"""
    if not data["success"]:
        return "FAIL: %s" % data["message"]
    lst = data["list"]
    if not lst:
        return "EMPTY: 暂无数据"
    lines = ["[%s] %d 条 (%s)" % (kind, len(lst), _date_str())]
    for i, item in enumerate(lst, 1):
        title = item.get("title") or item.get("name") or item.get("subject") or "-"
        extra = item.get("final_price") or item.get("coupon_amount") or ""
        row = "%d. %s" % (i, title)
        if extra:
            row += "  |  %s" % extra
        lines.append(row)
    lines.append("领券入口: %s" % SITE_URL)
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="惠生活外卖红包查询")
    parser.add_argument("--coupons", action="store_true", help="查优惠券列表 (默认查活动)")
    parser.add_argument("--section", default=None, help="板块名筛选, 如 外卖/美团")
    parser.add_argument("--format", default="wechat", choices=["wechat", "text"],
                        help="输出格式 (默认 wechat)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 原始数据")
    parser.add_argument("text", nargs="?", default="", help="自然语言输入 (仅做触发判断)")
    args = parser.parse_args()

    if args.text:
        low = args.text.lower()
        if not any(kw in low for kw in TRIGGER_KEYWORDS):
            print("未命中外卖/优惠触发词, 该查询可能应路由到其他通道。")
            print("本通道覆盖: 外卖红包/优惠券/领券/点外卖/美团/饿了么/京东外卖")
            sys.exit(0)

    kind = "coupons" if args.coupons else "projects"
    result = _request(kind, args.section)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.format == "text":
        print(render_text(result, kind))
    else:
        print(render_coupons(result) if args.coupons else render_projects(result))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()


# ── 引流信息（固定输出，prepare_release.py 自动补齐）─────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _print_leadgen()
