#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""淘宝联盟关键词选品和推广链接生成（官方 TOP API，标准库实现）。

凭据文件：~/.workbuddy/secrets/taobao_affiliate.json
字段：app_key、app_secret、adzone_id；可选 site_id。
"""
import argparse
import hashlib
import hmac
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

API_URL = "https://eco.taobao.com/router/rest"
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".workbuddy", "secrets", "taobao_affiliate.json")


class AffiliateError(RuntimeError):
    pass


def load_config():
    if not os.path.isfile(CONFIG_PATH):
        raise AffiliateError(
            "缺少淘宝联盟 API 配置文件：{}。需要 app_key、app_secret、adzone_id；"
            "请先在淘宝开放平台创建应用，并从淘宝联盟推广位管理取得推广位 ID。".format(CONFIG_PATH)
        )
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise AffiliateError("淘宝联盟配置文件无法读取：{}".format(exc))
    missing = [key for key in ("app_key", "app_secret", "adzone_id") if not str(config.get(key, "")).strip()]
    if missing:
        raise AffiliateError("淘宝联盟配置缺少字段：{}。密钥只保存在本机配置文件中。".format(", ".join(missing)))
    return config


def _sign(params, app_secret):
    source = "".join("{}{}".format(key, params[key]) for key in sorted(params) if key != "sign")
    digest = hmac.new(app_secret.encode("utf-8"), source.encode("utf-8"), hashlib.sha256).hexdigest()
    return digest.upper()


def _http_post(url, form, timeout=20):
    data = urllib.parse.urlencode(form).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) WorkBuddyCoupon/1.0",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        },
        method="POST",
    )
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=timeout) as response:
            return response.read().decode("utf-8", "replace")
    except Exception:
        if not (os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")):
            raise
        with urllib.request.build_opener().open(req, timeout=timeout) as response:
            return response.read().decode("utf-8", "replace")


def _api_call(method, params, config, timeout=20):
    request_params = {
        "app_key": str(config["app_key"]),
        "format": "json",
        "method": method,
        "simplify": "true",
        "sign_method": "hmac-sha256",
        "timestamp": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S"),
        "v": "2.0",
    }
    request_params.update({key: str(value) for key, value in params.items() if value is not None})
    request_params["sign"] = _sign(request_params, str(config["app_secret"]))
    try:
        payload = json.loads(_http_post(API_URL, request_params, timeout))
    except Exception as exc:
        raise AffiliateError("淘宝开放平台请求失败：{}".format(exc))
    if not isinstance(payload, dict):
        raise AffiliateError("淘宝开放平台返回了无法识别的数据")
    error = payload.get("error_response") or payload.get("errorResponse")
    if error:
        code = error.get("code", "")
        message = error.get("msg") or error.get("sub_msg") or "接口调用失败"
        raise AffiliateError("淘宝开放平台错误{}：{}".format(" (code {})".format(code) if code else "", message))
    return payload


def _first(mapping, *names):
    for name in names:
        value = mapping.get(name)
        if value not in (None, ""):
            return value
    return ""


def _extract_items(payload):
    root = payload
    for key in ("tbk_dg_material_optional_response", "tbk_dg_material_optional_up_grade_response"):
        if key in root:
            root = root[key]
            break
    result = root.get("result_list") or root.get("resultList") or {}
    if isinstance(result, list):
        return result
    if not isinstance(result, dict):
        return []
    items = result.get("map_data") or result.get("mapData") or result.get("data") or []
    if isinstance(items, dict):
        return [items]
    return items if isinstance(items, list) else []


def search(keyword, limit=5, has_coupon=False, config=None, timeout=20):
    if not keyword.strip():
        raise AffiliateError("请提供商品关键词")
    config = config or load_config()
    params = {
        "adzone_id": config["adzone_id"],
        "q": keyword.strip(),
        "page_no": 1,
        "page_size": max(1, min(int(limit), 20)),
        "platform": 2,
        "material_id": config.get("material_id", 2836),
        "has_coupon": "true" if has_coupon else None,
        "sort": "tk_rate_des",
    }
    payload = _api_call("taobao.tbk.dg.material.optional", params, config, timeout)
    items = []
    for item in _extract_items(payload):
        if not isinstance(item, dict):
            continue
        items.append({
            "title": _first(item, "title", "short_title", "shortTitle"),
            "shop": _first(item, "shop_title", "shopTitle", "nick"),
            "price": _first(item, "zk_final_price", "zkFinalPrice", "price"),
            "coupon": _first(item, "coupon_info", "couponInfo"),
            "coupon_amount": _first(item, "coupon_amount", "couponAmount"),
            "commission_rate": _first(item, "commission_rate", "commissionRate"),
            "commission_type": _first(item, "commission_type", "commissionType"),
            "sales_30d": _first(item, "volume"),
            "url": _first(item, "coupon_share_url", "couponShareUrl", "url", "click_url", "clickUrl"),
            "item_url": _first(item, "item_url", "itemUrl"),
        })
    return {"keyword": keyword.strip(), "source": "淘宝联盟官方物料搜索 API", "items": items}


def convert(link, config=None, timeout=20):
    """Convert a Taobao/Tmall product or promotion URL to an attributed link."""
    link = link.strip()
    parsed = urllib.parse.urlparse(link)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise AffiliateError("请粘贴完整的淘宝/天猫商品链接（需以 http:// 或 https:// 开头）")
    config = config or load_config()
    payload = _api_call("taobao.tbk.dg.general.link.convert", {
        "adzone_id": config["adzone_id"],
        "biz_scene_id": config.get("biz_scene_id", "1"),
        "promotion_type": config.get("promotion_type", "2"),
        "material_list": link,
        "required_link_type": "cps_short_tpwd,coupon_short_url",
    }, config, timeout)
    return {"input": link, "source": "淘宝联盟官方万能转链 API", "response": payload}


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="用淘宝联盟官方 API 搜商品或将商品链接转为推广链接")
    parser.add_argument("keyword", nargs="?", help="商品关键词，例如 无线鼠标")
    parser.add_argument("--keyword", "-k", dest="keyword_opt", help="商品关键词")
    parser.add_argument("--convert", metavar="URL", help="将淘宝/天猫商品链接转为联盟推广链接")
    parser.add_argument("--limit", type=int, default=5, help="最多返回商品数（1-20，默认 5）")
    parser.add_argument("--coupon", action="store_true", help="只查有优惠券的商品")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--timeout", type=int, default=20, help="网络超时秒数")
    args = parser.parse_args(argv)
    try:
        if args.convert:
            result = convert(args.convert, timeout=max(3, args.timeout))
        else:
            keyword = args.keyword_opt or args.keyword or ""
            result = search(keyword, args.limit, args.coupon, timeout=max(3, args.timeout))
    except AffiliateError as exc:
        print("淘宝联盟：{}".format(exc), file=sys.stderr)
        return 2
    except Exception as exc:
        print("淘宝联盟查询失败：{}".format(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if args.convert:
        print("淘宝联盟转链｜来源：{}".format(result["source"]))
        print(json.dumps(result["response"], ensure_ascii=False, indent=2))
        print("\n提示：链接归因与佣金以淘宝联盟规则和最终有效订单为准。")
        return 0
    print("淘宝联盟选品｜关键词：{}｜数据：{}".format(result["keyword"], result["source"]))
    if not result["items"]:
        print("没有查到匹配商品；可缩短关键词，或在联盟后台确认推广位和 API 权限。")
        return 0
    for index, item in enumerate(result["items"], 1):
        commission = item["commission_rate"]
        try:
            commission = "{:.2f}%".format(float(commission) / 100)
        except (TypeError, ValueError):
            pass
        print("\n{}. {}".format(index, item["title"] or "（无标题）"))
        print("   店铺：{}｜价格：{} 元｜佣金率：{}".format(item["shop"] or "未知", item["price"] or "未知", commission or "未知"))
        if item["coupon"]:
            print("   优惠券：{}".format(item["coupon"]))
        if item["url"]:
            print("   推广链接：{}".format(item["url"]))
        elif item["item_url"]:
            print("   商品链接（尚未返回推广链接）：{}".format(item["item_url"]))
    print("\n提示：佣金以淘宝联盟归因和最终有效订单为准；商品价格、优惠和佣金可能变化。")
    return 0


# ── 引流信息（固定输出）────────────────────────────────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _code = main()
    _print_leadgen()
    raise SystemExit(_code)
