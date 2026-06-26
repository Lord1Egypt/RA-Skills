#!/usr/bin/env python3
"""智能报价引擎 — 根据设备清单和工时自动报价"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class QuotationEngine:
    """报价引擎"""

    # 设备租赁日单价参考（元/天）
    EQUIPMENT_RATES = {
        "lighting": {"moving_head": 800, "wash": 500, "led_par": 200, "followspot": 600, "default": 400},
        "audio": {"console": 2000, "speaker": 300, "monitor": 250, "microphone": 100, "default": 300},
        "video": {"led_panel": 500, "projector": 1500, "camera": 800, "switcher": 1200, "default": 500},
        "rigging": {"truss": 100, "hoist": 200, "default": 150},
        "power": {"distro": 300, "generator": 2000, "default": 200},
        "control": {"console": 3000, "default": 500}
    }

    def __init__(self):
        self.tax_rate = 0.06  # 增值税6%

    def generate(self, show_data: dict, rental_days: int = 3,
                 labor_count: int = 5, labor_rate: float = 500,
                 transport_km: float = 50, transport_rate: float = 2.0,
                 insurance_rate: float = 0.005, management_rate: float = 0.1) -> dict:
        """
        生成报价单

        Args:
            show_data: 演出数据（符合skill_show_data_protocol格式）
            rental_days: 租赁天数
            labor_count: 技术人员数
            labor_rate: 人工日费率
            transport_km: 运输距离(km)
            transport_rate: 运输费率(元/km)
            insurance_rate: 保险费率
            management_rate: 管理费率
        """
        # 1. 设备租赁费
        equipment_cost = 0
        equipment_items = []
        for eq in show_data.get("equipment", []):
            category = eq.get("category", "control")
            qty = eq.get("quantity", 1)
            daily_rate = self._get_daily_rate(category, eq.get("model", ""))
            subtotal = daily_rate * qty * rental_days
            equipment_items.append({
                "name": f"{eq.get('manufacturer', '')} {eq.get('model', '')}",
                "category": category,
                "quantity": qty,
                "daily_rate": daily_rate,
                "days": rental_days,
                "subtotal": subtotal
            })
            equipment_cost += subtotal

        # 2. 人工费
        labor_cost = labor_count * labor_rate * rental_days

        # 3. 运输费（往返）
        transport_cost = transport_km * transport_rate * 2

        # 4. 保险费
        insurance_cost = equipment_cost * insurance_rate

        # 5. 管理费
        subtotal = equipment_cost + labor_cost + transport_cost + insurance_cost
        management_cost = subtotal * management_rate

        # 6. 税费
        total_before_tax = subtotal + management_cost
        tax = total_before_tax * self.tax_rate

        grand_total = total_before_tax + tax

        quotation = {
            "quotation_id": f"QT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "project_name": show_data.get("project", {}).get("name", "未命名"),
            "client": show_data.get("project", {}).get("client", ""),
            "generated_at": datetime.now().isoformat(),
            "items": {
                "equipment": equipment_items,
                "equipment_cost": round(equipment_cost, 2),
                "labor": {"count": labor_count, "rate": labor_rate, "days": rental_days, "cost": round(labor_cost, 2)},
                "transport": {"distance_km": transport_km * 2, "rate": transport_rate, "cost": round(transport_cost, 2)},
                "insurance": {"rate": insurance_rate, "cost": round(insurance_cost, 2)},
                "management": {"rate": management_rate, "cost": round(management_cost, 2)},
                "tax": {"rate": self.tax_rate, "cost": round(tax, 2)}
            },
            "total_before_tax": round(total_before_tax, 2),
            "tax": round(tax, 2),
            "grand_total": round(grand_total, 2)
        }

        return quotation

    def _get_daily_rate(self, category: str, model: str) -> float:
        """获取设备日租单价"""
        rates = self.EQUIPMENT_RATES.get(category, {"default": 400})
        model_lower = model.lower()
        for key, rate in rates.items():
            if key in model_lower:
                return float(rate)
        return float(rates.get("default", 400))

    def export_json(self, quotation: dict, filepath: str):
        """导出JSON报价单"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(quotation, f, ensure_ascii=False, indent=2)

    def summary(self, quotation: dict) -> str:
        """报价摘要"""
        items = quotation["items"]
        lines = [
            f"报价单: {quotation['quotation_id']}",
            f"项目: {quotation['project_name']}",
            f"客户: {quotation['client']}",
            f"",
            f"设备租赁: ¥{items['equipment_cost']:,.2f}",
            f"人工费: ¥{items['labor']['cost']:,.2f}",
            f"运输费: ¥{items['transport']['cost']:,.2f}",
            f"保险费: ¥{items['insurance']['cost']:,.2f}",
            f"管理费: ¥{items['management']['cost']:,.2f}",
            f"",
            f"小计: ¥{quotation['total_before_tax']:,.2f}",
            f"税费: ¥{quotation['tax']:,.2f}",
            f"总计: ¥{quotation['grand_total']:,.2f}"
        ]
        return "\n".join(lines)


def main():
    import sys
    engine = QuotationEngine()
    if len(sys.argv) < 2:
        print("用法: python3 skill_quotation_engine_impl.py gen <show.json>")
        sys.exit(1)
    action = sys.argv[1]
    if action == "gen" and len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            show = json.load(f)
        q = engine.generate(show)
        print(engine.summary(q))

if __name__ == "__main__":
    main()
