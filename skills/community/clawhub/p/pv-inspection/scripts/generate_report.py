#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光伏电站巡检报告生成脚本
支持日报、周报、月报生成
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# 输出目录
OUTPUT_DIR = Path("/home/admin/.openclaw/workspace/pv-inspection/reports")

def generate_daily_report(station_name: str, date_str: str):
    """生成日报"""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    
    # 模拟数据（实际应从监控系统获取）
    report_data = {
        "station": station_name,
        "date": date_str,
        "inspector": "巡检人员",
        "weather": "晴",
        "generation": {
            "daily": 1250.5,  # kWh
            "cumulative": 45678.9,  # kWh
            "peak_power": 850.2  # kW
        },
        "equipment": {
            "inverter": {"total": 10, "normal": 9, "abnormal": 1},
            "combiner": {"total": 20, "normal": 20, "abnormal": 0},
            "modules": {"total": 500, "normal": 498, "abnormal": 2}
        },
        "defects": [
            {
                "id": 1,
                "location": "3 号逆变器",
                "description": "通讯故障",
                "severity": "重要",
                "suggestion": "联系厂家维修"
            }
        ]
    }
    
    # 生成报告内容
    content = f"""# 光伏电站巡检日报

**电站名称：** {report_data['station']}
**巡检日期：** {report_data['date']}
**巡检人员：** {report_data['inspector']}
**天气情况：** {report_data['weather']}

## 一、发电数据
- 今日发电量：{report_data['generation']['daily']:.1f} kWh
- 累计发电量：{report_data['generation']['cumulative']:.1f} kWh
- 峰值功率：{report_data['generation']['peak_power']:.1f} kW

## 二、设备状态
- 逆变器：正常 {report_data['equipment']['inverter']['normal']}/{report_data['equipment']['inverter']['total']}
- 汇流箱：正常 {report_data['equipment']['combiner']['normal']}/{report_data['equipment']['combiner']['total']}
- 光伏组件：正常 {report_data['equipment']['modules']['normal']}/{report_data['equipment']['modules']['total']}

## 三、缺陷记录
"""
    
    if report_data['defects']:
        content += "| 序号 | 位置 | 缺陷描述 | 严重程度 | 整改建议 |\n"
        content += "|------|------|----------|----------|----------|\n"
        for defect in report_data['defects']:
            content += f"| {defect['id']} | {defect['location']} | {defect['description']} | {defect['severity']} | {defect['suggestion']} |\n"
    else:
        content += "今日无缺陷记录\n"
    
    content += f"""
## 四、明日计划
- [ ] 待整改项目跟踪
- [ ] 重点设备检查

---
*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 保存报告
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"daily_{station_name}_{date_str}.md"
    output_file.write_text(content, encoding='utf-8')
    
    print(f"✅ 日报已生成：{output_file}")
    return str(output_file)


def generate_weekly_report(station_name: str, week_str: str):
    """生成周报"""
    # 解析周数（格式：2026-W12）
    year, week = week_str.split("-W")
    
    content = f"""# 光伏电站巡检周报

**电站名称：** {station_name}
**统计周期：** {year}年第{week}周

## 一、发电统计
- 周发电量：XXXX kWh
- 日均发电量：XXXX kWh
- 环比上周：+X.X%

## 二、设备运行
- 逆变器可用率：XX.X%
- 汇流箱可用率：XX.X%
- 组件完好率：XX.X%

## 三、缺陷统计
- 新增缺陷：X 个
- 完成整改：X 个
- 待整改：X 个

## 四、下周计划
- [ ] 重点检查项目
- [ ] 计划性维护

---
*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"weekly_{station_name}_{week_str}.md"
    output_file.write_text(content, encoding='utf-8')
    
    print(f"✅ 周报已生成：{output_file}")
    return str(output_file)


def generate_monthly_report(station_name: str, month_str: str):
    """生成月报"""
    content = f"""# 光伏电站巡检月报

**电站名称：** {station_name}
**统计月份：** {month_str}

## 一、发电统计
- 月发电量：XXXX kWh
- 日均发电量：XXXX kWh
- 环比上月：+X.X%
- 同比去年：+X.X%

## 二、设备运行
- 逆变器可用率：XX.X%
- 汇流箱可用率：XX.X%
- 组件完好率：XX.X%
- PR 值：XX.X%

## 三、缺陷统计
- 新增缺陷：X 个
- 完成整改：X 个
- 待整改：X 个
- 整改完成率：XX.X%

## 四、发电量趋势
（此处插入趋势图）

## 五、缺陷分析
（此处插入缺陷分类饼图）

## 六、下月计划
- [ ] 计划性维护
- [ ] 设备更换
- [ ] 专项检查

---
*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"monthly_{station_name}_{month_str}.md"
    output_file.write_text(content, encoding='utf-8')
    
    print(f"✅ 月报已生成：{output_file}")
    return str(output_file)


def main():
    parser = argparse.ArgumentParser(description="光伏电站巡检报告生成")
    parser.add_argument("--type", choices=["daily", "weekly", "monthly"], required=True, help="报告类型")
    parser.add_argument("--station", required=True, help="电站名称")
    parser.add_argument("--date", help="日期（日报用 YYYY-MM-DD）")
    parser.add_argument("--week", help="周数（周报用 2026-W12）")
    parser.add_argument("--month", help="月份（月报用 2026-03）")
    
    args = parser.parse_args()
    
    if args.type == "daily":
        if not args.date:
            args.date = datetime.now().strftime("%Y-%m-%d")
        generate_daily_report(args.station, args.date)
    elif args.type == "weekly":
        if not args.week:
            # 当前周
            args.week = datetime.now().strftime("%G-W%V")
        generate_weekly_report(args.station, args.week)
    elif args.type == "monthly":
        if not args.month:
            args.month = datetime.now().strftime("%Y-%m")
        generate_monthly_report(args.station, args.month)


if __name__ == "__main__":
    main()
