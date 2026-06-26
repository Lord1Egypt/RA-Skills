"""
calculate_cost.py - 成本核算脚本
复刻 wood_quotation_template.xlsx 的完整计算逻辑
"""

import json
from pathlib import Path


# ============================================================
# 模式切换：INTERNAL（内部版）/ EXTERNAL（公开版）
# ============================================================
RUN_MODE = "EXTERNAL"  # 切换为 "INTERNAL" 可启用真实采购数据


# ============================================================
# 采购配置（根据实际情况修改）
# ============================================================
if RUN_MODE == "INTERNAL":
    MATERIAL_PRICES = {
        "桦木板材(18mm)": {"1-49张": 220, "50-99张": 205, "100张以上": 190},
        "E1级颗粒板(18mm)": {"1-99张": 85, "100-199张": 80, "200张以上": 75},
        "水性清漆(5L)": {"1-19桶": 180, "20-49桶": 170, "50桶以上": 160},
        "冷轧钢铰链": {"1-499个": 8.5, "500-999个": 8, "1000个以上": 7.5}
    }

    LOSS_RATES = {
        "桦木板材": 0.06,
        "E1级颗粒板": 0.03,
        "水性清漆": 0.01,
        "冷轧钢铰链": 0.01
    }

else:
    # 公开版：示例配置，请根据实际情况修改
    MATERIAL_PRICES = {
        "板材(18mm)": {"1-49张": 200, "50-99张": 180, "100张以上": 160},
        "颗粒板(18mm)": {"1-99张": 80, "100-199张": 75, "200张以上": 70},
        "清漆(5L)": {"1-19桶": 180, "20-49桶": 160, "50桶以上": 150},
        "铰链": {"1-499个": 8, "500-999个": 7, "1000个以上": 6}
    }
    LOSS_RATES = {
        "板材": 0.05,
        "颗粒板": 0.03,
        "清漆": 0.01,
        "铰链": 0.01
    }

# 工艺单价（元/项）
PROCESS_PRICES = {
    "切割": 5,
    "封边": 3,
    "喷漆": 25,
    "烤漆": 40,
    "贴皮": 15,
    "CNC": 30,
    "雕刻": 35,
    "打磨": 8,
    "组装": 20,
}

# 报价利润率（可调整）
PROFIT_MARGIN = 1.30  # 1.30 = 30% 利润率


def calc_board_qty(width_mm, depth_mm, height_mm, board_type="多层板") -> dict:
    """
    计算板材用量（基于展开面积估算）
    返回：板材张数 + 利用率
    """
    # 每张标准板可用面积（mm²）
    BOARD_AREA = 1220 * 2440  # 约 2.98 m²

    # 估算展开系数（根据柜体类型调整）
    展开系数 = 4.5  # 柜体类平均展开系数
    展开面积_mm2 = (width_mm * depth_mm + depth_mm * height_mm + width_mm * height_mm) * 2 * 展开系数
    展开面积_m2 = 展开面积_mm2 / 1_000_000

    # 单张板材面积（m²）
    board_area_m2 = (1220 * 2440) / 1_000_000  # ≈ 2.98 m²

    # 理论张数
    raw_qty = 展开面积_m2 / board_area_m2
    # 含损耗张数（取整+损耗余量）
    qty_with_loss = round(raw_qty * 1.08, 1)

    return {
        "展开面积_m2": round(展开面积_m2, 3),
        "理论张数": round(raw_qty, 2),
        "含损耗张数": qty_with_loss,
        "利用率": f"{round(raw_qty / qty_with_loss * 100, 1)}%"
    }


def calc_process_cost(processes: list) -> dict:
    """计算工艺成本（分项）"""
    items = []
    total = 0
    for p in processes:
        if p in PROCESS_PRICES:
            price = PROCESS_PRICES[p]
            total += price
            items.append({"工艺": p, "单价(元)": price, "备注": "含损耗"})
    return {"分项": items, "工艺成本合计": total}


def calc_material_cost(materials: list, qty: float) -> dict:
    """计算材料成本（支持阶梯价格精确匹配）"""
    items = []
    total = 0
    for m in materials:
        if m in MATERIAL_PRICES:
            price_tiers = MATERIAL_PRICES[m]
            # 根据用量精确匹配阶梯价格
            price = None
            matched_tier = None
            
            # 解析阶梯价格区间
            for tier, p in price_tiers.items():
                # 匹配格式：如 "1-49张"、"100张以上"、"1-99张"
                if "以上" in tier or "+" in tier:
                    # 无上限档位
                    min_qty = int(tier.replace("张以上", "").replace("个以上", "").replace("桶以上", "").replace("+", "").replace("以上", ""))
                    if qty >= min_qty:
                        price = p
                        matched_tier = tier
                elif "-" in tier:
                    # 区间档位
                    parts = tier.replace("张", "").replace("个", "").replace("桶", "").split("-")
                    min_qty = int(parts[0])
                    max_qty = int(parts[1])
                    if min_qty <= qty <= max_qty:
                        price = p
                        matched_tier = tier
            
            # 默认取第一档
            if price is None:
                first_tier = list(price_tiers.keys())[0]
                price = price_tiers[first_tier]
                matched_tier = first_tier
            
            cost = price * qty
            total += cost
            items.append({
                "材料": m,
                "价格档位": matched_tier,
                "单价": price,
                "用量": qty,
                "金额(元)": round(cost, 2)
            })
    return {"分项": items, "材料成本合计": round(total, 2)}


def calc_loss(materials: list, material_cost: float, process_cost: float) -> dict:
    """计算综合损耗（材料损耗）"""
    # 材料损耗率
    combined_rate = sum(LOSS_RATES.get(m.split("(")[0], 0) for m in materials)
    # 含材料损耗
    total_base = material_cost + process_cost
    loss = round(total_base * combined_rate, 2)
    return {
        "综合损耗率": f"{round(combined_rate * 100, 1)}%",
        "损耗金额(元)": loss
    }


def generate_quotation(parsing_result: dict) -> dict:
    """
    主入口：根据图纸解析结果生成完整报价
    Args:
        parsing_result: parse_drawing.py 的输出
    Returns:
        dict: 完整报价明细
    """
    dimensions = parsing_result.get("dimensions", {})
    materials = parsing_result.get("materials", [])
    processes = parsing_result.get("processes", [])

    if not dimensions:
        return {
            "status": "error",
            "message": "未能从图纸中提取尺寸数据，请补充尺寸信息（格式：W*D*H，如1200*600*800）"
        }

    # 取第一个识别的尺寸
    dim_key = list(dimensions.keys())[0]
    dim = dimensions[dim_key]
    w, d, h = dim["width"], dim["depth"], dim["height"]

    # 1. 板材用量
    board_calc = calc_board_qty(w, d, h)
    qty = board_calc["含损耗张数"]

    # 2. 材料成本
    default_materials = ["桦木板材(18mm)"]
    mat_cost_result = calc_material_cost(materials if materials else default_materials, qty)
    material_cost = mat_cost_result["材料成本合计"]

    # 3. 工艺成本
    proc_cost_result = calc_process_cost(processes if processes else ["切割", "封边", "打磨", "组装"])

    # 4. 损耗
    loss_result = calc_loss(materials if materials else default_materials, material_cost, proc_cost_result["工艺成本合计"])

    # 5. 总成本
    工艺成本 = proc_cost_result["工艺成本合计"]
    损耗金额 = loss_result["损耗金额(元)"]
    总成本 = round(material_cost + 工艺成本 + 损耗金额, 2)

    # 6. 报价金额
    报价金额 = round(总成本 * PROFIT_MARGIN, 2)

    # 汇总
    return {
        "status": "success",
        "图纸尺寸": dim_key,
        "宽_w": w,
        "深_d": d,
        "高_h": h,
        "材料明细": mat_cost_result["分项"],
        "工艺明细": proc_cost_result["分项"],
        "板材用量": board_calc,
        "损耗": loss_result,
        "工艺成本": 工艺成本,
        "材料成本": material_cost,
        "总成本": 总成本,
        "报价金额": 报价金额,
        "利润率": f"{(PROFIT_MARGIN - 1) * 100:.0f}%"
    }


def format_quotation_table(quotation: dict) -> str:
    """生成 Markdown 报价表格（对话展示用）"""
    if quotation.get("status") == "error":
        return f"❌ 报价失败：{quotation.get('message')}"

    lines = [
        "## 📋 木作报价明细",
        "",
        f"**图纸尺寸**：{quotation.get('图纸尺寸')}（W{quotation['宽_w']} × D{quotation['深_d']} × H{quotation['高_h']}mm）",
        "",
        "### 一、材料成本",
        "| 材料 | 价格档位 | 单价 | 用量 | 金额 |",
        "|------|----------|------|------|------|",
    ]

    for m in quotation.get("材料明细", []):
        lines.append(f"| {m['材料']} | {m['价格档位']} | {m['单价']}元 | {m['用量']} | {m['金额(元)']}元 |")
    lines.append(f"| **材料合计** | | | | **{quotation['材料成本']}元** |")
    lines.append("")

    lines.append("### 二、工艺成本")
    lines.append("| 工艺 | 单价 |")
    lines.append("|------|------|")
    for p in quotation.get("工艺明细", []):
        lines.append(f"| {p['工艺']} | {p['单价(元)']}元 |")
    lines.append(f"| **工艺合计** | **{quotation['工艺成本']}元** |")
    lines.append("")

    lines.append("### 三、损耗核算")
    lines.append(f"- 综合损耗率：{quotation['损耗']['综合损耗率']}")
    lines.append(f"- 损耗金额：{quotation['损耗']['损耗金额(元)']}元")
    lines.append("")

    lines.append("### 四、报价汇总")
    lines.append(f"- **板材用量**：{quotation['板材用量']['含损耗张数']}张（利用率 {quotation['板材用量']['利用率']}）")
    lines.append(f"- **总成本**：{quotation['总成本']}元")
    lines.append(f"- **报价金额**：💰 **{quotation['报价金额']}元**")
    lines.append(f"- **利润率**：{quotation['利润率']}")
    lines.append("")

    lines.append("*本报价仅供内部参考，不对外泄露采购数据。*")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # 接收 parse_drawing.py 的输出
        parsing_result = json.loads(sys.argv[1])
    else:
        # 默认测试数据
        parsing_result = {
            "dimensions": {"W1200_D600_H800": {"width": 1200, "depth": 600, "height": 800}},
            "materials": ["桦木板材(18mm)"],
            "processes": ["切割", "封边", "喷漆", "打磨", "组装"]
        }

    quotation = generate_quotation(parsing_result)
    print(format_quotation_table(quotation))
