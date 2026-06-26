#!/usr/bin/env python3
"""
calc_tile.py — 瓦匠工程量与成本估算脚本

计算内容：
  1. 瓷砖用量（片数 + 损耗）
  2. 辅料用量（水泥/砂/瓷砖胶）
  3. 人工费估算
  4. 总成本汇总
  5. 材料建议

用法：
  python3 calc_tile.py --space bathroom --length 3 --width 2.5 --tile-len 300 --tile-wid 600 --tile-price 12 --city-tier 1

各参数含义：
  --space        空间类型：bathroom|kitchen|livingroom|balcony
  --length       房间长度 (m)
  --width        房间宽度 (m)
  --tile-len     瓷砖长度 (mm)
  --tile-wid     瓷砖宽度 (mm)
  --tile-price   瓷砖单价（元/片）
  --wall-height  墙面铺贴高度 (m)，仅厨卫需要。默认卫生间 2.4m，厨房 2.4m
  --city-tier    城市等级：1（一线）/2（二线）/3（其他），默认 2
  --identity     用户身份：owner（业主）/worker（从业者），默认 owner
  --json         输出 JSON（供 AI 解析），默认输出可读文本
"""

import argparse
import json
import sys

# ─── 损耗率表 ───
LOSS_RATES = {
    "bathroom": {"small": 0.12, "normal": 0.08, "large": 0.10},
    "kitchen": {"small": 0.10, "normal": 0.06, "large": 0.10},
    "livingroom": {"normal": 0.04, "large": 0.10},
    "balcony": {"normal": 0.06, "large": 0.10},
}

# ─── 人工费（元/㎡，二线基准）───
LABOR_FLOOR = {"normal": 45, "large": 80, "extra": 120}   # 地砖
LABOR_WALL = {"normal": 50, "large": 90, "extra": 140}    # 墙砖

# ─── 城市系数 ───
CITY_MULTIPLIER = {1: 1.4, 2: 1.0, 3: 0.85}

# ─── 辅料用量 ───
ADHESIVE_RATES = {
    "small": {"name": "水泥砂浆", "cement_kg_per_m2": 10, "sand_kg_per_m2": 30},
    "normal": {"name": "瓷砖胶C1", "tile_glue_kg_per_m2": 5},
    "large": {"name": "瓷砖胶C2", "tile_glue_kg_per_m2": 8},
    "extra": {"name": "瓷砖胶C2S1", "tile_glue_kg_per_m2": 10},
}

# ─── 瓷砖规格分类 ───
def classify_tile(len_mm, wid_mm):
    """根据瓷砖尺寸分类：small / normal / large / extra"""
    area_m2 = len_mm * wid_mm / 1_000_000
    long_edge = max(len_mm, wid_mm)
    if long_edge < 300 or area_m2 < 0.09:
        return "extra"  # 马赛克/异形
    elif long_edge < 600:
        return "small"
    elif long_edge < 900:
        return "normal"
    elif long_edge < 1200:
        return "large"
    else:
        return "extra"  # 岩板/超大板


def get_loss_rate(space, tile_class):
    losses = LOSS_RATES.get(space, LOSS_RATES["livingroom"])
    return losses.get(tile_class, max(losses.values()))


def calc_tile_count(area_m2, tile_len_mm, tile_wid_mm, loss_rate):
    tile_area = tile_len_mm * tile_wid_mm / 1_000_000
    base_count = area_m2 / tile_area
    return int(base_count * (1 + loss_rate)) + 1  # 向上取整


def calc_wall_area(length, width, wall_height, door_area=1.6, window_area=1.0):
    """墙面面积 = 周长 × 高度 - 门窗"""
    perimeter = 2 * (length + width)
    gross = perimeter * wall_height
    return gross - door_area - window_area


def calc_floor_area(length, width):
    return length * width


def estimate_materials(area_m2, tile_class):
    info = ADHESIVE_RATES[tile_class]
    result = {"method": info["name"]}
    if "cement_kg_per_m2" in info:
        result["cement_kg"] = round(area_m2 * info["cement_kg_per_m2"])
        result["sand_kg"] = round(area_m2 * info["sand_kg_per_m2"])
        # 水泥包装：50kg/包
        result["cement_bags"] = max(1, round(result["cement_kg"] / 50))
        result["sand_bags"] = max(1, round(result["sand_kg"] / 25))  # 25kg/袋砂
    if "tile_glue_kg_per_m2" in info:
        glue_kg = area_m2 * info["tile_glue_kg_per_m2"]
        result["tile_glue_kg"] = round(glue_kg, 1)
        result["tile_glue_bags"] = max(1, round(glue_kg / 20))  # 20kg/包
    return result


def estimate_labor(area_m2, tile_class, tile_type, city_tier):
    base = (LABOR_FLOOR if tile_type == "floor" else LABOR_WALL).get(tile_class, 80)
    total = base * area_m2 * CITY_MULTIPLIER[city_tier]
    return round(base, 0), round(total, 0)


def get_tile_suggestion(space, tile_class):
    """根据空间和规格推荐材料"""
    suggestions = {
        "bathroom": "卫生间推荐全瓷砖上墙，使用瓷砖胶+背胶双保险。地面建议300×300或600×600防滑砖。",
        "kitchen": "厨房推荐400×800或300×600亮面砖，易清洁。地砖建议600×600防滑砖。",
        "livingroom": "客厅推荐800×800或600×1200抛釉砖/通体砖。大板需双人施工。",
        "balcony": "阳台推荐300×300或600×600防滑砖，注意做坡度排水。",
    }
    return suggestions.get(space, "")


def main():
    parser = argparse.ArgumentParser(description="瓦匠工程量与成本估算")
    parser.add_argument("--space", required=True, choices=["bathroom", "kitchen", "livingroom", "balcony"])
    parser.add_argument("--length", type=float, required=True, help="房间长度 (m)")
    parser.add_argument("--width", type=float, required=True, help="房间宽度 (m)")
    parser.add_argument("--tile-len", type=int, required=True, help="瓷砖长度 (mm)")
    parser.add_argument("--tile-wid", type=int, required=True, help="瓷砖宽度 (mm)")
    parser.add_argument("--tile-price", type=float, default=0, help="瓷砖单价（元/片）")
    parser.add_argument("--wall-height", type=float, default=None, help="墙面铺贴高度 (m)")
    parser.add_argument("--city-tier", type=int, choices=[1, 2, 3], default=2)
    parser.add_argument("--identity", choices=["owner", "worker"], default="owner")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()
    space = args.space
    city_tier = args.city_tier

    # ── 1. 面积计算 ──
    floor_area = calc_floor_area(args.length, args.width)
    need_wall = space in ("bathroom", "kitchen")
    wall_height = args.wall_height
    if need_wall and wall_height is None:
        wall_height = 2.4  # 默认层高

    wall_area = calc_wall_area(args.length, args.width, wall_height) if need_wall else 0

    # ── 2. 瓷砖分类与损耗 ──
    tile_class = classify_tile(args.tile_len, args.tile_wid)
    loss_rate = get_loss_rate(space, tile_class)

    # ── 3. 瓷砖数量 ──
    floor_tiles = calc_tile_count(floor_area, args.tile_len, args.tile_wid, loss_rate)
    wall_tiles = calc_tile_count(wall_area, args.tile_len, args.tile_wid, loss_rate) if need_wall else 0

    total_area = floor_area + wall_area
    total_tiles = floor_tiles + wall_tiles

    # ── 4. 瓷砖费用 ──
    tile_cost = round(total_tiles * args.tile_price, 2)

    # ── 5. 辅料估算 ──
    floor_materials = estimate_materials(floor_area, tile_class)
    wall_materials = estimate_materials(wall_area, tile_class) if need_wall else None

    # 汇总辅料
    cement_total = floor_materials.get("cement_kg", 0) + (wall_materials.get("cement_kg", 0) if wall_materials else 0)
    sand_total = floor_materials.get("sand_kg", 0) + (wall_materials.get("sand_kg", 0) if wall_materials else 0)
    glue_total = floor_materials.get("tile_glue_kg", 0) + (wall_materials.get("tile_glue_kg", 0) if wall_materials else 0)

    # ── 6. 人工费 ──
    floor_base, floor_labor = estimate_labor(floor_area, tile_class, "floor", city_tier)
    wall_base, wall_labor = estimate_labor(wall_area, tile_class, "wall", city_tier) if need_wall else (0, 0)
    total_labor = round(floor_labor + wall_labor, 2)

    # ── 7. 辅料成本 ≈ 水泥50/包, 砂8元/袋, 瓷砖胶35元/包
    mat_cost_cement = (floor_materials.get("cement_bags", 0) + (wall_materials.get("cement_bags", 0) if wall_materials else 0)) * 30
    mat_cost_sand = (floor_materials.get("sand_bags", 0) + (wall_materials.get("sand_bags", 0) if wall_materials else 0)) * 8
    mat_cost_glue = (glue_total / 20) * 35  # 粗略
    material_cost = round(mat_cost_cement + mat_cost_sand + mat_cost_glue, 2)

    total_cost = round(tile_cost + material_cost + total_labor, 2)

    # ── 材料建议 ──
    suggestion = get_tile_suggestion(space, tile_class)

    # ── 输出 ──
    result = {
        "space": {
            "type": space,
            "floor_area_m2": round(floor_area, 2),
            "wall_area_m2": round(wall_area, 2) if need_wall else 0,
            "total_area_m2": round(total_area, 2),
        },
        "tile": {
            "spec_mm": f"{args.tile_len}×{args.tile_wid}",
            "tile_class": tile_class,
            "loss_rate": loss_rate,
            "floor_tiles": floor_tiles,
            "wall_tiles": wall_tiles if need_wall else 0,
            "total_tiles": total_tiles,
            "unit_price": args.tile_price,
            "tile_cost": tile_cost,
        },
        "material": {
            "method": floor_materials["method"],
            "cement_kg": cement_total,
            "cement_bags": max(1, round(cement_total / 50)),
            "sand_kg": sand_total,
            "tile_glue_kg": round(glue_total, 1),
            "tile_glue_bags": max(1, round(glue_total / 20)),
            "material_cost_estimate": material_cost,
        },
        "labor": {
            "floor_unit_price": floor_base,
            "wall_unit_price": wall_base,
            "floor_total": round(floor_labor, 0),
            "wall_total": round(wall_labor, 0),
            "labor_total": round(total_labor, 0),
            "city_tier": city_tier,
        },
        "cost_summary": {
            "tile": tile_cost,
            "material": material_cost,
            "labor": round(total_labor, 0),
            "total": total_cost,
        },
        "suggestion": suggestion,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # ── 可读输出 ──
    print("=" * 50)
    print("  瓦匠工程量与成本估算报告")
    print("=" * 50)
    print(f"\n📐 空间信息")
    print(f"  空间类型：{space}")
    print(f"  地面面积：{floor_area:.2f} ㎡" + (f"  |  墙面面积：{wall_area:.2f} ㎡" if need_wall else ""))
    print(f"  铺贴总面积：{total_area:.2f} ㎡")

    print(f"\n🧱 瓷砖用量")
    print(f"  瓷砖规格：{args.tile_len}×{args.tile_wid}mm（{tile_class}）")
    print(f"  损耗率：{loss_rate:.0%}")
    print(f"  地砖用量：{floor_tiles} 片" + (f"  |  墙砖用量：{wall_tiles} 片" if need_wall else ""))
    print(f"  总用量：{total_tiles} 片")
    if args.tile_price > 0:
        print(f"  瓷砖总价：{tile_cost:.0f} 元（单价 {args.tile_price:.0f} 元/片）")

    print(f"\n🧪 辅料估算")
    print(f"  施工方式：{floor_materials['method']}")
    print(f"  水泥：约 {cement_total} kg（{max(1, round(cement_total/50))} 包）")
    print(f"  砂子：约 {sand_total} kg" if sand_total > 0 else "", end="")
    if glue_total > 0:
        print(f"  瓷砖胶：约 {glue_total:.0f} kg（{max(1, round(glue_total/20))} 包）")
    print(f"  辅料费用（估）：{material_cost:.0f} 元")

    city_label = {1: "一线城市", 2: "二线城市", 3: "其他城市"}
    print(f"\n💰 人工费估算（{city_label[city_tier]}）")
    print(f"  地砖铺贴：{floor_area:.2f} ㎡ × {floor_base:.0f} 元/㎡ = {floor_labor:.0f} 元" + (f"" if not need_wall else f""))

    if need_wall:
        print(f"  墙砖铺贴：{wall_area:.2f} ㎡ × {wall_base:.0f} 元/㎡ = {wall_labor:.0f} 元")
    print(f"  人工费合计：{total_labor:.0f} 元")

    print(f"\n💵 成本汇总")
    print(f"  瓷砖物料：{tile_cost:>8.0f} 元")
    print(f"  辅料费用：{material_cost:>8.0f} 元")
    print(f"  人工费用：{total_labor:>8.0f} 元")
    print(f"  ─────────────────")
    print(f"  总  计：  {total_cost:>8.0f} 元")
    print(f"  折合：{round(total_cost/total_area, 0):.0f} 元/㎡")

    if args.identity == "owner":
        print(f"\n💡 材料建议")
        print(f"  {suggestion}")

    print(f"\n{'=' * 50}")
    print(f"  ⚠️ 以上为估算参考，实际以现场测量为准")
    print(f"  {'=' * 50}")


if __name__ == "__main__":
    main()
