#!/usr/bin/env python3
"""Create a conservative Markdown pick-and-pack list from a sanitized JSON order batch."""
import json
import sys
from collections import Counter
from pathlib import Path


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(2)


def is_positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def main(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    orders = data.get("orders")
    kits = data.get("kits", {})
    gifts = data.get("gifts", [])
    packaging = data.get("packaging_rules", [])
    if not isinstance(orders, list) or not orders:
        fail("输入必须包含非空 orders 数组。")
    if len(orders) > 20:
        fail("最多支持 20 个订单。")
    item_component_lines = 0

    def reserve_pick_rows(count):
        """Reserve every rendered product/component row before it is emitted."""
        nonlocal item_component_lines
        item_component_lines += count
        if item_component_lines > 100:
            fail("最多支持 100 条商品或组件行。")
    component_totals = Counter()
    unresolved = []
    rendered = ["# 发货拣货装箱单", "", "仅供人工拣货与装箱核对；不读取后台、不扣库存、不创建运单，也不表示已发货。", ""]
    for order in orders:
        oid = order.get("id", "未编号订单")
        rendered += [f"## 订单 {oid}", "", "### 拣货与装箱勾选", ""]
        items = order.get("items", [])
        if not items:
            unresolved.append(f"{oid}：缺少商品行")
        for item in items:
            sku, qty, unit = item.get("sku"), item.get("quantity"), item.get("unit")
            unit = unit.strip() if isinstance(unit, str) else unit
            if sku and is_positive_number(qty) and not unit:
                unresolved.append(f"{oid}：商品 {sku} 缺少单位")
                rendered.append(f"- {sku} × {qty:g}（待确认单位；不能确认拣货数量）")
                reserve_pick_rows(1)
                continue
            if not sku or not is_positive_number(qty) or not unit:
                unresolved.append(f"{oid}：商品行缺 SKU、正数数量或单位")
                continue
            if sku in kits:
                parts = kits[sku]
                if not isinstance(parts, list) or not parts:
                    unresolved.append(f"{oid}：套装 {sku} 缺少已确认组成，停止拆套计算")
                    rendered.append(f"- {sku} × {qty:g} {unit}（待确认套装组成；不能确认拣货数量）")
                    reserve_pick_rows(1)
                    continue
                valid_parts = all(
                    isinstance(part, dict)
                    and part.get("sku")
                    and is_positive_number(part.get("quantity"))
                    and isinstance(part.get("unit"), str)
                    and part.get("unit").strip()
                    for part in parts
                )
                if not valid_parts:
                    unresolved.append(f"{oid}：套装 {sku} 的组件资料不完整，停止拆套计算")
                    rendered.append(f"- {sku} × {qty:g} {unit}（待确认套装组件；不能确认拣货数量）")
                    reserve_pick_rows(1)
                    continue
                # A confirmed kit consumes one parent row plus one row for every part.
                reserve_pick_rows(1 + len(parts))
                rendered.append(f"- [ ] {sku} × {qty} {unit}（按已确认套装拆拣）")
                for part in parts:
                    psku, pqty, punit = part.get("sku"), part.get("quantity"), part.get("unit")
                    punit = punit.strip()
                    component_totals[(psku, punit)] += qty * pqty
                    rendered.append(f"  - [ ] {psku} × {qty * pqty:g} {punit}")
            else:
                reserve_pick_rows(1)
                rendered.append(f"- [ ] {sku} × {qty:g} {unit}")
        for gift in gifts:
            if not isinstance(gift, dict) or (
                not gift.get("qualifying_sku")
                or not is_positive_number(gift.get("min_order_quantity"))
                or not str(gift.get("min_order_unit", "")).strip()
                or not gift.get("sku")
                or not is_positive_number(gift.get("quantity"))
                or not isinstance(gift.get("unit"), str)
                or not gift["unit"].strip()
            ):
                unresolved.append(f"{oid}：赠品条件资料不完整")
                continue
            matching_items = [x for x in items if isinstance(x, dict) and x.get("sku") == gift["qualifying_sku"]]
            if any(not is_positive_number(x.get("quantity")) or not str(x.get("unit", "")).strip() for x in matching_items):
                unresolved.append(f"{oid}：赠品门槛商品 {gift['qualifying_sku']} 的数量或单位待确认，不能计算赠品")
                continue
            units = {str(x["unit"]).strip().casefold() for x in matching_items}
            required_unit = str(gift["min_order_unit"]).strip().casefold()
            if matching_items and (len(units) != 1 or required_unit not in units):
                unresolved.append(f"{oid}：赠品门槛商品 {gift['qualifying_sku']} 存在不同计量单位或不匹配门槛单位，需提供同单位数量或明确换算规则")
                continue
            matching = sum(x.get("quantity", 0) for x in matching_items)
            if matching >= gift["min_order_quantity"]:
                rendered.append(f"- [ ] 赠品 {gift['sku']} × {gift['quantity']:g} {gift['unit'].strip()}（条件已满足）")
        rendered.append("")
    rendered += ["## 拆套后组件汇总", ""]
    rendered += [f"- [ ] {sku} × {qty:g} {unit}" for (sku, unit), qty in sorted(component_totals.items())] or ["- 暂无已确认套装组件"]
    rendered += ["", "## 待确认项", ""]
    rendered += [f"- {x}" for x in unresolved] or ["- 无"]
    rendered += ["", "## 包装规则", ""]
    if packaging:
        rendered += [f"- [ ] {rule}" for rule in packaging]
    else:
        rendered.append("- 待确认：未提供包装规则；不猜测附件、赠品或包裹数量。")
    print("\n".join(rendered))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("用法：generate_picklist.py INPUT.json")
    main(sys.argv[1])
