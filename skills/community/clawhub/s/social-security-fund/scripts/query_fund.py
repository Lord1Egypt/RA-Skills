#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公积金查询工具
支持查询公积金余额、缴存记录、贷款额度估算等

注意：实际查询需要登录各地公积金系统
本脚本提供模拟查询和官方查询入口指引
"""

import argparse
import json
import hashlib
from datetime import datetime

# 各城市公积金查询入口
CITY_FUND_PORTALS = {
    "北京": {
        "name": "北京住房公积金管理中心",
        "url": "http://gjj.beijing.gov.cn/",
        "query_url": "https://gjj.beijing.gov.cn/web/zwfw5/159113/index.html",
        "loan_hotline": "010-12329",
    },
    "上海": {
        "name": "上海住房公积金网",
        "url": "http://www.shgjj.com/",
        "query_url": "https://www.shgjj.com/",
        "loan_hotline": "021-12329",
    },
    "广州": {
        "name": "广州住房公积金管理中心",
        "url": "http://gjj.gz.gov.cn/",
        "query_url": "https://gjj.gz.gov.cn/gjjfwpt/",
        "loan_hotline": "020-12329",
    },
    "深圳": {
        "name": "深圳市住房公积金管理中心",
        "url": "http://zjj.sz.gov.cn/",
        "query_url": "https://zjj.sz.gov.cn/ztzl/zwfw/gjjzhfw/",
        "loan_hotline": "0755-12329",
    },
    "杭州": {
        "name": "杭州住房公积金管理中心",
        "url": "http://gjj.hangzhou.gov.cn/",
        "query_url": "https://gjj.hangzhou.gov.cn/",
        "loan_hotline": "0571-12329",
    },
    "成都": {
        "name": "成都住房公积金管理中心",
        "url": "http://gjj.chengdu.gov.cn/",
        "query_url": "https://gjj.chengdu.gov.cn/",
        "loan_hotline": "028-12329",
    },
}

# 公积金贷款额度计算参数
LOAN_PARAMS = {
    "北京": {"max_individual": 120, "max_family": 120, "balance_multiplier": 15},
    "上海": {"max_individual": 50, "max_family": 100, "balance_multiplier": 40},
    "广州": {"max_individual": 60, "max_family": 100, "balance_multiplier": 20},
    "深圳": {"max_individual": 50, "max_family": 90, "balance_multiplier": 14},
    "杭州": {"max_individual": 60, "max_family": 120, "balance_multiplier": 15},
    "成都": {"max_individual": 40, "max_family": 70, "balance_multiplier": 20},
}

def simulate_query(city: str, account: str = None) -> dict:
    """
    模拟公积金查询（演示用）
    """
    now = datetime.now()
    
    # 根据账号生成模拟数据
    if account:
        hash_val = int(hashlib.md5(account.encode()).hexdigest()[:8], 16)
        balance = 20000 + (hash_val % 100000)
        monthly_deposit = 1000 + (hash_val % 3000)
    else:
        balance = 50000
        monthly_deposit = 2400
    
    # 获取贷款参数
    loan_param = LOAN_PARAMS.get(city, LOAN_PARAMS["北京"])
    estimated_loan = min(
        balance * loan_param["balance_multiplier"] / 10000,
        loan_param["max_individual"]
    )
    
    return {
        "city": city,
        "query_time": now.isoformat(),
        "account": account[:6] + "****" if account else "****",
        "fund": {
            "balance": balance,
            "status": "正常缴存",
            "monthly_deposit": monthly_deposit,
            "personal_ratio": 0.12,
            "company_ratio": 0.12,
            "last_deposit": now.strftime("%Y-%m"),
        },
        "loan_estimate": {
            "max_amount": estimated_loan,
            "unit": "万元",
            "note": "实际额度以公积金中心审批为准",
        },
    }

def get_query_guide(city: str) -> dict:
    """获取官方查询指引"""
    if city not in CITY_FUND_PORTALS:
        city = "北京"
    
    portal = CITY_FUND_PORTALS[city]
    return {
        "city": city,
        "portal_name": portal["name"],
        "portal_url": portal["url"],
        "query_url": portal["query_url"],
        "hotline": portal["loan_hotline"],
        "methods": [
            "官方网站查询",
            "12329 热线查询",
            "公积金 APP 查询",
            "支付宝市民中心",
            "微信城市服务",
            "公积金柜台查询",
        ],
        "required": [
            "身份证号",
            "公积金账号（可选）",
            "手机号（接收验证码）",
        ],
        "withdrawal_conditions": [
            "购买、建造、翻建、大修自住住房",
            "偿还购房贷款本息",
            "租房自住",
            "离休、退休",
            "完全丧失劳动能力并与单位终止劳动关系",
            "出境定居",
        ],
    }

def format_result(result: dict) -> str:
    """格式化输出结果"""
    if "portal_name" in result:
        # 查询指引
        lines = [
            f"🏦 {result['city']}公积金查询指引",
            f"━━━━━━━━━━━━━━━━",
            f"🏛️ 机构：{result['portal_name']}",
            f"🌐 官网：{result['portal_url']}",
            f"🔗 查询入口：{result['query_url']}",
            f"📞 热线：{result['hotline']}",
            f"",
            f"📱 查询方式：",
        ]
        for i, method in enumerate(result["methods"], 1):
            lines.append(f"   {i}. {method}")
        lines.append(f"")
        lines.append(f"📝 需要准备：")
        for item in result["required"]:
            lines.append(f"   • {item}")
        lines.append(f"")
        lines.append(f"💡 提取条件：")
        for cond in result["withdrawal_conditions"]:
            lines.append(f"   • {cond}")
        return "\n".join(lines)
    else:
        # 查询结果
        fund = result["fund"]
        loan = result["loan_estimate"]
        lines = [
            f"🏦 公积金查询结果",
            f"━━━━━━━━━━━━━━━━",
            f"📍 城市：{result['city']}",
            f"⏰ 查询时间：{result['query_time']}",
            f"🔢 账号：{result['account']}",
            f"📊 缴存状态：{fund['status']}",
            f"",
            f"💰 账户信息：",
            f"   • 账户余额：¥{fund['balance']:,.2f}",
            f"   • 月缴存额：¥{fund['monthly_deposit']:,.2f}",
            f"   • 个人比例：{fund['personal_ratio']*100:.0f}%",
            f"   • 单位比例：{fund['company_ratio']*100:.0f}%",
            f"   • 最后缴存：{fund['last_deposit']}",
            f"",
            f"🏠 贷款额度估算：",
            f"   • 最高可贷：约{loan['max_amount']:.1f}万元",
            f"   • 说明：{loan['note']}",
            f"",
            f"⚠️ 说明：以上为模拟数据，实际数据请通过官方渠道查询",
        ]
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="公积金查询工具")
    parser.add_argument("--city", type=str, default="北京", help="城市名称")
    parser.add_argument("--account", type=str, default=None, help="公积金账号（模拟查询用）")
    parser.add_argument("--guide", action="store_true", help="仅显示查询指引")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    if args.guide:
        result = get_query_guide(args.city)
    else:
        result = simulate_query(args.city, args.account)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_result(result))

if __name__ == "__main__":
    main()
