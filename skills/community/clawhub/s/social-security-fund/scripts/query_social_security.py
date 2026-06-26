#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社保查询工具
支持查询社保缴纳记录、缴费基数、账户余额等

注意：实际查询需要登录各地社保系统
本脚本提供模拟查询和官方查询入口指引
"""

import argparse
import json
import hashlib
from datetime import datetime

# 各城市社保查询入口
CITY_PORTALS = {
    "北京": {
        "name": "北京市人力资源和社会保障局",
        "url": "http://rsj.beijing.gov.cn/",
        "query_url": "http://fuwu.rsj.beijing.gov.cn/bishopsite/login/login.html",
    },
    "上海": {
        "name": "上海市人力资源和社会保障局",
        "url": "http://rsj.sh.gov.cn/",
        "query_url": "https://zzfz.rsj.sh.gov.cn/zzfz/",
    },
    "广州": {
        "name": "广州市人力资源和社会保障局",
        "url": "http://rsj.gz.gov.cn/",
        "query_url": "http://ggfw.gdhrss.gov.cn/gdggfw/",
    },
    "深圳": {
        "name": "深圳市社会保险基金管理局",
        "url": "http://hrss.sz.gov.cn/szsi/",
        "query_url": "https://sipub.sz.gov.cn/homsWeb/",
    },
    "杭州": {
        "name": "杭州市人力资源和社会保障局",
        "url": "http://hrss.hangzhou.gov.cn/",
        "query_url": "https://gzlz.hrss.hangzhou.gov.cn/",
    },
    "成都": {
        "name": "成都市人力资源和社会保障局",
        "url": "http://cdhrss.chengdu.gov.cn/",
        "query_url": "http://www.cd12333.com/",
    },
}

def simulate_query(city: str, idcard: str = None) -> dict:
    """
    模拟社保查询（演示用）
    实际使用需要对接官方 API
    """
    # 生成模拟数据
    now = datetime.now()
    months = 120  # 模拟 10 年
    
    # 根据身份证计算模拟数据（仅演示）
    if idcard:
        hash_val = int(hashlib.md5(idcard.encode()).hexdigest()[:8], 16)
        base_salary = 5000 + (hash_val % 10000)
        medical_balance = 1000 + (hash_val % 5000)
        pension_months = 60 + (hash_val % 120)
    else:
        base_salary = 8000
        medical_balance = 3500
        pension_months = months
    
    return {
        "city": city,
        "query_time": now.isoformat(),
        "social_security": {
            "pension": {
                "months": pension_months,
                "base": base_salary,
                "personal_account": base_salary * 0.08 * pension_months,
            },
            "medical": {
                "balance": medical_balance,
                "status": "正常参保",
            },
            "unemployment": {
                "months": pension_months,
            },
            "work_injury": {
                "status": "正常参保",
            },
            "maternity": {
                "status": "正常参保",
            },
        },
        "status": "正常",
        "last_payment": now.strftime("%Y-%m"),
    }

def get_query_guide(city: str) -> dict:
    """获取官方查询指引"""
    if city not in CITY_PORTALS:
        city = "北京"  # 默认
    
    portal = CITY_PORTALS[city]
    return {
        "city": city,
        "portal_name": portal["name"],
        "portal_url": portal["url"],
        "query_url": portal["query_url"],
        "methods": [
            "官方网站查询",
            "12333 热线查询",
            "社保 APP 查询",
            "支付宝/微信城市服务",
            "社保局窗口查询",
        ],
        "required": [
            "身份证号",
            "社保卡号（可选）",
            "手机号（接收验证码）",
        ],
    }

def format_result(result: dict) -> str:
    """格式化输出结果"""
    if "portal_name" in result:
        # 查询指引
        lines = [
            f"📋 {result['city']}社保查询指引",
            f"━━━━━━━━━━━━━━━━",
            f"🏛️ 机构：{result['portal_name']}",
            f"🌐 官网：{result['portal_url']}",
            f"🔗 查询入口：{result['query_url']}",
            f"",
            f"📱 查询方式：",
        ]
        for i, method in enumerate(result["methods"], 1):
            lines.append(f"   {i}. {method}")
        lines.append(f"")
        lines.append(f"📝 需要准备：")
        for item in result["required"]:
            lines.append(f"   • {item}")
        return "\n".join(lines)
    else:
        # 查询结果
        ss = result["social_security"]
        lines = [
            f"📋 社保查询结果",
            f"━━━━━━━━━━━━━━━━",
            f"📍 城市：{result['city']}",
            f"⏰ 查询时间：{result['query_time']}",
            f"📊 参保状态：{result['status']}",
            f"💳 最后缴费：{result['last_payment']}",
            f"",
            f"👴 养老保险：",
            f"   • 累计缴费：{ss['pension']['months']} 个月",
            f"   • 缴费基数：¥{ss['pension']['base']:,.2f}",
            f"   • 个人账户：¥{ss['pension']['personal_account']:,.2f}",
            f"",
            f"🏥 医疗保险：",
            f"   • 账户余额：¥{ss['medical']['balance']:,.2f}",
            f"   • 参保状态：{ss['medical']['status']}",
            f"",
            f"⚠️ 说明：以上为模拟数据，实际数据请通过官方渠道查询",
        ]
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="社保查询工具")
    parser.add_argument("--city", type=str, default="北京", help="城市名称")
    parser.add_argument("--idcard", type=str, default=None, help="身份证号（模拟查询用）")
    parser.add_argument("--guide", action="store_true", help="仅显示查询指引")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    if args.guide:
        result = get_query_guide(args.city)
    else:
        result = simulate_query(args.city, args.idcard)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_result(result))

if __name__ == "__main__":
    main()
