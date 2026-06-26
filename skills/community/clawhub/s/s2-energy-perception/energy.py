#!/usr/bin/env python3
import sys
import os
import json
import argparse
import re
from datetime import datetime

# =====================================================================
# ⚡ S2-SP-OS: Energy Perception Radar (V1.1.0)
# Passive Inventory + Advanced Local Visual Dashboard / 本地数据可视化看板
# =====================================================================

class S2EnergyManager:
    def __init__(self, zone: str, grid: str):
        self.zone = zone.lower()
        self.grid = grid
        self.carbon_factor = 0.5810 
        # ... [此处保留之前的 device_db 和 room_templates 代码，为节省篇幅略] ...
        self.room_templates = {"living_room": [{"name": "Main_AC", "type": "HVAC", "power_w": 2000, "smart": True}]}

    # ... [此处保留之前的 run_inventory 和 read_smart_breaker 代码，为节省篇幅略] ...
    
    def generate_dashboard(self) -> dict:
        """
        [高级视觉特性]: 延迟加载重型分析库，生成 30 天动态能耗与物理设备静态画像。
        生成本地图表文件，供 Agent 提取并展示给用户。
        """
        try:
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt
            plt.style.use('seaborn-v0_8-whitegrid')
        except ImportError:
            return {"error": "Dashboard generation requires: pip install pandas numpy matplotlib"}

        output_dir = os.getcwd()
        chart_paths = []

        # 1. 构建模拟的 20 个设备全屋盘点底座
        data = [
            {"Room": "Living Room", "Device": "Main AC", "Power_W": 2000},
            {"Room": "Living Room", "Device": "Smart TV", "Power_W": 150},
            {"Room": "Master Bed", "Device": "Bedroom AC", "Power_W": 1000},
            {"Room": "Kitchen", "Device": "Refrigerator", "Power_W": 150},
            {"Room": "Kitchen", "Device": "Microwave", "Power_W": 1000},
            {"Room": "Bathroom", "Device": "Water Heater", "Power_W": 2000},
            # ... 模拟 20 个设备缩略
            {"Room": "Study", "Device": "Desktop PC", "Power_W": 300}
        ]
        df = pd.DataFrame(data)

        # 图表 1: 功率横向对比条形图 (Bar Chart)
        df_sorted = df.sort_values(by="Power_W", ascending=True)
        plt.figure(figsize=(10, 6))
        plt.barh(df_sorted["Device"], df_sorted["Power_W"], color='#3498db')
        plt.title('Power Rating of Household Appliances (Watts)', fontweight='bold')
        bar_path = os.path.join(output_dir, 's2_appliance_bar.png')
        plt.tight_layout()
        plt.savefig(bar_path, dpi=100)
        plt.close()
        chart_paths.append(f"file://{bar_path}")

        # 图表 2: 30天动态能耗波动与 7日滑动平均 (Line Chart)
        np.random.seed(42)
        days = np.arange(1, 31)
        daily_matrix = np.zeros((30, len(df)))
        
        for i, row in df.iterrows():
            base_h = 4.0 # 模拟基准小时
            noise = np.random.normal(loc=base_h, scale=base_h * 0.2, size=30)
            weekend_multiplier = np.where((days % 7 == 6) | (days % 7 == 0), 1.3, 1.0)
            hours = np.clip(noise * weekend_multiplier, 0, 24)
            daily_matrix[:, i] = (hours * row["Power_W"]) / 1000.0

        total_daily_kwh = np.sum(daily_matrix, axis=1)
        ma_7 = pd.Series(total_daily_kwh).rolling(window=7, min_periods=1).mean()

        plt.figure(figsize=(12, 5))
        plt.plot(days, total_daily_kwh, marker='o', color='#2c3e50', label='Daily Consumption')
        plt.plot(days, ma_7, linestyle='--', color='#e74c3c', label='7-Day Moving Avg')
        plt.fill_between(days, total_daily_kwh, color='#3498db', alpha=0.2)
        plt.title('30-Day Household Electricity Fluctuation (kWh)', fontweight='bold')
        plt.legend()
        line_path = os.path.join(output_dir, 's2_daily_trend.png')
        plt.tight_layout()
        plt.savefig(line_path, dpi=100)
        plt.close()
        chart_paths.append(f"file://{line_path}")

        return {
            "action": "generate_dashboard",
            "status": "success",
            "total_devices_analyzed": len(df),
            "peak_daily_kwh": round(float(np.max(total_daily_kwh)), 2),
            "generated_charts_uris": chart_paths,
            "vendor_nl": "Advanced data visualization generated locally. No cloud analytics used. / 高级可视化图表已在本地生成，零云端分析介入。"
        }


def main():
    if os.environ.get("S2_PRIVACY_CONSENT") != "1":
        print(json.dumps({"error": "SECURITY BLOCK: Environment variable S2_PRIVACY_CONSENT=1 is missing."}, ensure_ascii=False))
        sys.exit(1)

    parser = argparse.ArgumentParser()
    # 新增 generate_dashboard 动作
    parser.add_argument("--action", choices=["inventory", "read_breaker", "generate_dashboard"], required=True)
    parser.add_argument("--method", choices=["text", "vision", "default"])
    parser.add_argument("--payload", default="")
    parser.add_argument("--zone", required=True)
    parser.add_argument("--grid", required=True)
    args = parser.parse_args()

    manager = S2EnergyManager(args.zone, args.grid)
    core_tensors = {}

    if args.action == "inventory":
        core_tensors = manager.run_inventory(args.method, args.payload)
    elif args.action == "read_breaker":
        core_tensors = manager.read_smart_breaker()
    elif args.action == "generate_dashboard":
        core_tensors = manager.generate_dashboard()

    print(json.dumps({
        "status": "AUTHORIZED_ENERGY_DATA",
        "architecture_compliance": "PASSIVE_MONITOR_ONLY",
        "s2_chronos_memzero": {
            "spatial_signature": {"zone_room": args.zone, "grid_voxel": args.grid},
            "chronos_timestamp": datetime.now().isoformat(),
            "core_tensors": core_tensors
        }
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()