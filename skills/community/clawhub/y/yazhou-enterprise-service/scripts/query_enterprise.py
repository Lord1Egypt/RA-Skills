#!/usr/bin/env python3
"""
企业信息查询辅助脚本
通过Web搜索和抓取，辅助查询企业基本信息
"""

import sys
import json
import subprocess

def search_enterprise(enterprise_name):
    """
    查询企业基本信息
    使用WebSearch工具搜索企业信息
    """
    print(f"正在查询企业: {enterprise_name}")
    print("请使用 WorkBuddy 的 WebSearch 工具搜索以下内容：")
    print(f"1. {enterprise_name} 企业信用信息")
    print(f"2. {enterprise_name} 天眼查")
    print(f"3. {enterprise_name} 企查查")
    print(f"4. {enterprise_name} 国家统一社会信用代码")

    # 返回搜索建议
    search_suggestions = [
        f"{enterprise_name} 企业信用信息公示系统",
        f"{enterprise_name} 天眼查企业信息",
        f"{enterprise_name} 经营范围 注册资本",
        f"{enterprise_name} 法定代表人",
        f"{enterprise_name} 行政处罚",
        f"{enterprise_name} 经营异常"
    ]

    return {
        "enterprise_name": enterprise_name,
        "search_suggestions": search_suggestions,
        "query_channels": [
            "国家企业信用信息公示系统: http://www.gsxt.gov.cn/",
            "天眼查: https://www.tianyancha.com/",
            "企查查: https://www.qcc.com/",
            "爱企查: https://aiqicha.baidu.com/"
        ]
    }

def generate_enterprise_report(enterprise_info):
    """
    生成企业信息查询报告
    """
    report = f"""# 企业基本信息查询结果

## 企业基本信息
- 企业名称：{enterprise_info.get('enterprise_name', '未获取')}
- 统一社会信用代码：{enterprise_info.get('credit_code', '未获取')}
- 法定代表人：{enterprise_info.get('legal_representative', '未获取')}
- 注册资本：{enterprise_info.get('registered_capital', '未获取')}
- 成立日期：{enterprise_info.get('establishment_date', '未获取')}
- 企业类型：{enterprise_info.get('enterprise_type', '未获取')}
- 经营范围：{enterprise_info.get('business_scope', '未获取')}
- 注册地址：{enterprise_info.get('registered_address', '未获取')}
- 经营状态：{enterprise_info.get('operating_status', '未获取')}

## 资质与认定
- 高新技术企业：{enterprise_info.get('high_tech_enterprise', '未获取')}
- 科技型中小企业：{enterprise_info.get('tech_sme', '未获取')}
- 其他资质：{enterprise_info.get('other_qualifications', '未获取')}

## 经营状况
- 行政处罚记录：{enterprise_info.get('admin_penalty', '未获取')}
- 经营异常记录：{enterprise_info.get('business_abnormalities', '未获取')}
- 严重违法失信记录：{enterprise_info.get('serious_violations', '未获取')}

## 政策匹配建议
根据企业特征，建议重点关注以下政策：
1. {enterprise_info.get('policy_suggestion_1', '请根据企业类型和行业匹配政策')}
2. {enterprise_info.get('policy_suggestion_2', '')}
3. {enterprise_info.get('policy_suggestion_3', '')}
"""

    return report

def match_policies(enterprise_info):
    """
    根据企业信息匹配优惠政策
    """
    suggestions = []

    enterprise_type = enterprise_info.get('enterprise_type', '')
    industry = enterprise_info.get('industry', '')
    qualifications = enterprise_info.get('qualifications', [])

    # 高新技术企业
    if '高新技术' in qualifications or enterprise_info.get('high_tech_enterprise') == '是':
        suggestions.append("高新技术企业税收优惠（企业所得税减按15%征收）")

    # 科技型中小企业
    if '科技型中小' in qualifications or enterprise_info.get('tech_sme') == '是':
        suggestions.append("科技型中小企业研发费用加计扣除")

    # 小型微利企业
    if '小型微利' in enterprise_type or enterprise_info.get('enterprise_size') == '小型':
        suggestions.append("小型微利企业所得税优惠")

    # 按行业匹配
    if '电子信息' in industry or '生物医药' in industry or '新材料' in industry:
        suggestions.append("产业发展专项资金")

    if '制造' in industry:
        suggestions.append("企业技改补贴")

    if '旅游' in industry:
        suggestions.append("旅游业发展专项资金")

    # 通用政策
    suggestions.append("融资支持政策（政银企对接平台）")
    suggestions.append("人才引进政策（人才住房保障）")

    return suggestions

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python query_enterprise.py <企业名称>")
        print("示例: python query_enterprise.py 海南迈思科技有限公司")
        sys.exit(1)

    enterprise_name = sys.argv[1]

    # 查询企业信息
    result = search_enterprise(enterprise_name)

    # 输出结果
    print("\n查询建议:")
    for suggestion in result["search_suggestions"]:
        print(f"  - {suggestion}")

    print("\n查询渠道:")
    for channel in result["query_channels"]:
        print(f"  - {channel}")

    print("\n请使用 WorkBuddy 的 WebSearch 和 WebFetch 工具获取详细信息。")
