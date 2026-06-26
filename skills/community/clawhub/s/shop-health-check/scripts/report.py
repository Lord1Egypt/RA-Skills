#!/usr/bin/env python3
"""
report.py - 店铺健康巡检汇总报告 + 飞书推送
整合 check_sites、check_ssl、check_404 的结果，判定告警，推送到飞书
"""
import sys
import os
import json
import configparser
import datetime

# 添加 scripts 目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import check_sites
import check_ssl
import check_404


def load_config():
    config_path = os.path.join(SKILL_DIR, "config/shops.conf")
    cfg = configparser.ConfigParser()
    cfg.read(config_path)
    return cfg


def format_feishu_message(report_data):
    """将报告格式化为飞书消息卡片（Card）"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    shops = report_data["shops"]

    has_alert = any(s["has_alert"] for s in shops)
    icon = "🚨" if has_alert else "✅"
    title = f"{icon} 店铺健康巡检报告 | {now}"

    # 构建卡片内容
    elements = [{"tag": "markdown", "content": f"**{title}**\n"}]

    for shop in shops:
        shop_icon = "📦" if not shop["has_alert"] else "⚠️"
        elements.append({"tag": "markdown", "content": f"\n{shop_icon} **{shop['name']}** (`{shop['domain']}`)\n"})

        # 站点可用性
        site_issues = [r for r in shop["sites"] if not r["ok"]]
        if not site_issues:
            elements.append({"tag": "markdown", "content": "  ✅ 站点可用性：全部正常\n"})
        else:
            for r in site_issues:
                err = r.get("error", f"状态码 {r.get('status')}")
                elements.append({"tag": "markdown", "content": f"  ❌ {r['path']}：{err}（{r['response_time']}s）\n"})

        # SSL
        ssl = shop["ssl"]
        if ssl["status"] == "valid":
            elements.append({"tag": "markdown", "content": f"  ✅ SSL证书：正常（剩余 {ssl['days_remaining']} 天）\n"})
        elif ssl["status"] == "warning":
            elements.append({"tag": "markdown", "content": f"  ⚠️ SSL证书：剩余 {ssl['days_remaining']} 天，请尽快续期！\n"})
        elif ssl["status"] == "expired":
            elements.append({"tag": "markdown", "content": "  ❌ SSL证书：已过期！\n"})
        else:
            elements.append({"tag": "markdown", "content": f"  ❌ SSL证书：{ssl.get('error', '检查失败')}\n"})

        # 商品页抽检
        products = shop["products"]
        if not products:
            elements.append({"tag": "markdown", "content": "  ⚠️ 未检测到商品页\n"})
        else:
            ok_count = sum(1 for p in products if p["ok"])
            problem_products = [p for p in products if not p["ok"]]
            if not problem_products:
                elements.append({"tag": "markdown", "content": f"  🔍 商品页抽检：全部正常（{ok_count}/{len(products)}）\n"})
            else:
                elements.append({"tag": "markdown", "content": f"  🔍 商品页抽检：{ok_count}/{len(products)} 正常\n"})
                for p in problem_products:
                    if p["is_404"]:
                        elements.append({"tag": "markdown", "content": f"    ❌ 404: `{p['url']}`\n"})
                    elif p["has_error_text"]:
                        elements.append({"tag": "markdown", "content": f"    ❌ 内容错误: `{p['url']}` — {p['content_check']}\n"})

    # 底部总结
    total_issues = sum(s["total_issues"] for s in shops)
    if has_alert:
        elements.append({"tag": "markdown", "content": f"\n---  \n⚡ 共 **{total_issues}** 个问题需要处理"})
    else:
        elements.append({"tag": "markdown", "content": f"\n---  \n🎉 所有店铺健康，无异常。"})

    card = {
        "config": {"wide_screen_mode": True},
        "elements": elements
    }
    return card


def send_feishu(card, webhook=None):
    """发送消息到飞书"""
    if not webhook:
        webhook = os.environ.get("FEISHU_WEBHOOK")
    if not webhook:
        print("⚠️ 未配置飞书 Webhook，跳过推送。")
        return False

    try:
        import requests
        payload = {"msg_type": "interactive", "card": card}
        resp = requests.post(webhook, json=payload, timeout=10)
        result = resp.json()
        if result.get("code") == 0:
            print("📨 飞书推送成功")
            return True
        else:
            print(f"❌ 飞书推送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 飞书推送异常: {e}")
        return False


def generate_text_report(report_data):
    """生成纯文本报告（用于控制台输出）"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    has_alert = any(s["has_alert"] for s in report_data["shops"])
    icon = "🚨" if has_alert else "✅"
    lines = [f"{icon} 店铺健康巡检报告 | {now}", "=" * 40]

    for shop in report_data["shops"]:
        shop_icon = "📦" if not shop["has_alert"] else "⚠️"
        lines.append(f"\n{shop_icon} {shop['name']} ({shop['domain']})")

        # 站点可用性
        site_issues = [r for r in shop["sites"] if not r["ok"]]
        if not site_issues:
            lines.append(f"  ✅ 站点可用性：全部正常")
        else:
            lines.append(f"  ❌ 站点可用性：{len(site_issues)} 个问题")
            for r in site_issues:
                err = r.get("error", f"状态码 {r.get('status')}")
                lines.append(f"    - {r['path']}: {err} ({r['response_time']}s)")

        # SSL
        ssl = shop["ssl"]
        if ssl["status"] == "valid":
            lines.append(f"  ✅ SSL证书：正常（剩余 {ssl['days_remaining']} 天）")
        elif ssl["status"] == "warning":
            lines.append(f"  ⚠️ SSL证书：剩余 {ssl['days_remaining']} 天，请尽快续期！")
        elif ssl["status"] == "expired":
            lines.append(f"  ❌ SSL证书：已过期！")
        else:
            lines.append(f"  ❌ SSL证书：{ssl.get('error', '检查失败')}")

        # 商品页
        products = shop["products"]
        if not products:
            lines.append("  ⚠️ 未检测到商品页")
        else:
            ok_count = sum(1 for p in products if p["ok"])
            problem_products = [p for p in products if not p["ok"]]
            if not problem_products:
                lines.append(f"  🔍 商品页抽检：全部正常（{ok_count}/{len(products)}）")
            else:
                lines.append(f"  🔍 商品页抽检：{ok_count}/{len(products)} 正常")
                for p in problem_products:
                    if p["is_404"]:
                        lines.append(f"    ❌ 404: {p['url']}")
                    elif p["has_error_text"]:
                        lines.append(f"    ❌ 内容错误: {p['url']} — {p['content_check']}")

    total_issues = sum(s["total_issues"] for s in report_data["shops"])
    lines.append("")
    if has_alert:
        lines.append(f"⚡ 共 {total_issues} 个问题需要处理")
    else:
        lines.append("🎉 所有店铺健康，无异常。")

    return "\n".join(lines)


def run_full_check(target_shop=None, config=None):
    """执行完整巡检"""
    if config is None:
        config = load_config()

    report_data = {
        "time": datetime.datetime.now().isoformat(),
        "shops": []
    }

    shops_to_check = [target_shop] if target_shop else [
        s for s in config.sections() if s != "DEFAULT"
    ]

    for shop_name in shops_to_check:
        shop_data = {
            "name": config.get(shop_name, "name", fallback=shop_name),
            "domain": config.get(shop_name, "domain"),
            "sites": [],
            "ssl": {},
            "products": [],
            "has_alert": False,
            "total_issues": 0
        }

        # 1. 站点可用性
        sites = check_sites.check_shop(config, shop_name)
        shop_data["sites"] = sites
        site_issues = [r for r in sites if not r["ok"]]
        if site_issues:
            shop_data["has_alert"] = True
            shop_data["total_issues"] += len(site_issues)

        # 2. SSL
        domain = config.get(shop_name, "domain")
        warning_days = int(config.get(shop_name, "ssl_warning_days", fallback=14))
        ssl_result = check_ssl.check_ssl(domain, 443, warning_days)
        shop_data["ssl"] = ssl_result
        if ssl_result["status"] in ("warning", "expired", "error"):
            shop_data["has_alert"] = True
            shop_data["total_issues"] += 1

        # 3. 商品页抽检
        products = check_404.check_shop_products(config, shop_name)
        shop_data["products"] = products
        product_issues = [p for p in products if not p["ok"]]
        if product_issues:
            shop_data["has_alert"] = True
            shop_data["total_issues"] += len(product_issues)

        report_data["shops"].append(shop_data)

    return report_data


def main():
    import argparse
    parser = argparse.ArgumentParser(description="店铺健康巡检报告")
    parser.add_argument("--shop", help="指定巡检的店铺名称（如 shop1）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--no-feishu", action="store_true", help="跳过飞书推送")
    args = parser.parse_args()

    print("🔍 开始店铺健康巡检...")
    config = load_config()
    report_data = run_full_check(target_shop=args.shop, config=config)

    if args.json:
        print(json.dumps(report_data, indent=2, ensure_ascii=False))
        return 0

    text_report = generate_text_report(report_data)
    print("\n" + text_report)

    # 飞书推送（有告警时发送，正常时可选）
    if not args.no_feishu:
        webhook = None
        if args.shop:
            try:
                webhook = config.get(args.shop, "feishu_webhook")
            except Exception:
                pass
        if not webhook:
            try:
                webhook = config.get("DEFAULT", "feishu_webhook")
            except Exception:
                pass

        has_alert = any(s["has_alert"] for s in report_data["shops"])
        # 有告警时发飞书，正常时也发（方便确认巡检正常）
        card = format_feishu_message(report_data)
        send_feishu(card, webhook)

    return 0


if __name__ == "__main__":
    sys.exit(main())