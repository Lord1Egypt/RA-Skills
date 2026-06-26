#!/usr/bin/env python3
"""Shopping list management."""

import argparse, json, os, sys
from datetime import datetime

LIST_FILE = os.path.expanduser("~/.openclaw/workspace/smart-shopper/data/shopping_list.json")


def load():
    os.makedirs(os.path.dirname(LIST_FILE), exist_ok=True)
    if os.path.exists(LIST_FILE):
        return json.load(open(LIST_FILE))
    return {"items": [], "created": datetime.now().isoformat()}


def save(data):
    os.makedirs(os.path.dirname(LIST_FILE), exist_ok=True)
    json.dump(data, open(LIST_FILE, "w"), indent=2, ensure_ascii=False)


def add_item(item, price=None, url=None, platform=None, notes=None):
    sl = load()
    entry = {
        "id": len(sl["items"]) + 1,
        "item": item,
        "price": price,
        "url": url,
        "platform": platform,
        "notes": notes,
        "added": datetime.now().isoformat(),
        "bought": False,
    }
    sl["items"].append(entry)
    save(sl)
    return entry


def remove_item(item_id):
    sl = load()
    sl["items"] = [i for i in sl["items"] if i["id"] != item_id]
    save(sl)


def mark_bought(item_id):
    sl = load()
    for i in sl["items"]:
        if i["id"] == item_id:
            i["bought"] = True
    save(sl)


def show():
    return load()


def clear():
    save({"items": [], "created": datetime.now().isoformat()})


def export_list():
    sl = load()
    lines = ["# 🛒 购物清单", f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    total = 0
    for i in sl["items"]:
        status = "✅" if i["bought"] else "⬜"
        price_str = f"${i['price']}" if i.get("price") else "价格待定"
        lines.append(f"{status} {i['item']} — {price_str}")
        if i.get("platform"):
            lines.append(f"   平台: {i['platform']}")
        if i.get("url"):
            lines.append(f"   链接: {i['url']}")
        if i.get("notes"):
            lines.append(f"   备注: {i['notes']}")
        lines.append("")
        if i.get("price"):
            total += i["price"]
    lines.append(f"💰 总计: ${total:.2f}")
    return "\n".join(lines)


def format_output(data):
    lines = ["🛒 购物清单", ""]
    total = 0
    for i in data["items"]:
        status = "✅" if i["bought"] else "⬜"
        price_str = f"${i['price']}" if i.get("price") else ""
        lines.append(f"  {status} [{i['id']}] {i['item']} {price_str}")
        if i.get("url"):
            lines.append(f"      🔗 {i['url']}")
        if i.get("price"):
            total += i["price"]
    if not data["items"]:
        lines.append("  (空列表)")
    lines.append(f"\n💰 预估总计: ${total:.2f}")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--action", choices=["show", "add", "remove", "bought", "clear", "export"], default="show")
    p.add_argument("--item", default=None)
    p.add_argument("--price", type=float, default=None)
    p.add_argument("--url", default=None)
    p.add_argument("--platform", default=None)
    p.add_argument("--notes", default=None)
    p.add_argument("--id", type=int, default=None)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.action == "add":
        r = add_item(a.item, a.price, a.url, a.platform, a.notes)
        print(f"✅ 已添加: [{r['id']}] {r['item']}")
    elif a.action == "remove":
        remove_item(a.id)
        print(f"✅ 已删除 #{a.id}")
    elif a.action == "bought":
        mark_bought(a.id)
        print(f"✅ 已标记 #{a.id} 为已购买")
    elif a.action == "clear":
        clear()
        print("✅ 购物清单已清空")
    elif a.action == "export":
        print(export_list())
    else:
        data = show()
        print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
