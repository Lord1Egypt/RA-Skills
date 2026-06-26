#!/usr/bin/env python3
"""Track product prices over time."""

import argparse, json, os, sys
from datetime import datetime

TRACK_FILE = os.path.expanduser("~/.openclaw/workspace/smart-shopper/data/price_tracker.json")


def load():
    os.makedirs(os.path.dirname(TRACK_FILE), exist_ok=True)
    if os.path.exists(TRACK_FILE):
        return json.load(open(TRACK_FILE))
    return {"items": []}


def save(data):
    os.makedirs(os.path.dirname(TRACK_FILE), exist_ok=True)
    json.dump(data, open(TRACK_FILE, "w"), indent=2, ensure_ascii=False)


def add_item(name, price, url, platform=None):
    data = load()
    entry = {
        "id": len(data["items"]) + 1,
        "name": name,
        "url": url,
        "platform": platform,
        "history": [{
            "price": price,
            "date": datetime.now().isoformat(),
        }],
        "target_price": None,
        "alert": False,
    }
    data["items"].append(entry)
    save(data)
    return entry


def update_price(item_id, price):
    data = load()
    for item in data["items"]:
        if item["id"] == item_id:
            item["history"].append({
                "price": price,
                "date": datetime.now().isoformat(),
            })
            # Check if target reached
            if item["target_price"] and price <= item["target_price"]:
                item["alert"] = True
            save(data)
            return item
    return None


def set_target(item_id, target):
    data = load()
    for item in data["items"]:
        if item["id"] == item_id:
            item["target_price"] = target
            save(data)
            return item
    return None


def show():
    return load()


def alerts():
    data = load()
    return [i for i in data["items"] if i.get("alert")]


def format_output(data):
    lines = ["📊 价格追踪", ""]
    for item in data["items"]:
        lines.append(f"🔖 [{item['id']}] {item['name']}")
        if item.get("platform"):
            lines.append(f"   平台：{item['platform']}")
        
        # Price history
        prices = [h["price"] for h in item["history"]]
        if len(prices) > 1:
            change = prices[-1] - prices[0]
            arrow = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            lines.append(f"   {arrow} 价格：${prices[0]:.2f} → ${prices[-1]:.2f} ({change:+.2f})")
        else:
            lines.append(f"   💰 当前：${prices[0]:.2f}")
        
        if item.get("target_price"):
            status = "✅" if item.get("alert") else "⏳"
            lines.append(f"   {status} 目标：${item['target_price']:.2f}")
        
        lines.append(f"   🔗 {item['url']}")
        lines.append("")
    
    if not data["items"]:
        lines.append("  (空列表)")
    
    # Show alerts
    alert_items = alerts()
    if alert_items:
        lines.append("\n🚨 价格警报:")
        for a in alert_items:
            lines.append(f"  • {a['name']} 已降至目标价格!")
    
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--action", choices=["show", "add", "update", "target", "alerts"], default="show")
    p.add_argument("--id", type=int, default=None)
    p.add_argument("--name", default=None)
    p.add_argument("--price", type=float, default=None)
    p.add_argument("--url", default=None)
    p.add_argument("--platform", default=None)
    p.add_argument("--target", type=float, default=None)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    
    if a.action == "add":
        r = add_item(a.name, a.price, a.url, a.platform)
        print(f"✅ 已添加追踪：[{r['id']}] {r['name']} @ ${r['price']:.2f}")
    elif a.action == "update":
        r = update_price(a.id, a.price)
        if r:
            print(f"✅ 已更新价格：[{a.id}] {r['name']} @ ${a.price:.2f}")
        else:
            print(f"❌ 未找到 #{a.id}")
    elif a.action == "target":
        r = set_target(a.id, a.target)
        if r:
            print(f"✅ 已设置目标价：[{a.id}] {r['name']} 目标 ${a.target:.2f}")
        else:
            print(f"❌ 未找到 #{a.id}")
    elif a.action == "alerts":
        data = {"items": alerts()}
        print(json.dumps(data, indent=2) if a.json else format_output(data))
    else:
        data = show()
        print(json.dumps(data, indent=2) if a.json else format_output(data))
