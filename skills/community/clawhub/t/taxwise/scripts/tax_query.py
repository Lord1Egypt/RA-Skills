#!/usr/bin/env python3
"""税率查询工具 - 免费版
用法: python3 tax_query.py <税种> [--纳税人类型 <小规模|一般>] [--地区 <省份>]
"""

import argparse
import json
import sys

# 中国主要税种税率数据（基于2024年政策）
TAX_RATES = {
    "增值税": {
        "一般纳税人": {
            "基本税率": {"rate": "13%", "scope": "销售货物、加工修理修配、有形动产租赁"},
            "低税率1": {"rate": "9%", "scope": "交通运输、邮政、建筑、不动产租赁、农产品"},
            "低税率2": {"rate": "6%", "scope": "金融服务、生活服务、现代服务"},
            "零税率": {"rate": "0%", "scope": "出口货物、跨境应税行为"},
        },
        "小规模纳税人": {
            "一般征收率": {"rate": "3%", "scope": "一般情况"},
            "不动产征收率": {"rate": "5%", "scope": "不动产销售/租赁"},
            "优惠政策": {"rate": "1%", "scope": "2023-2027:月销售额≤10万免征，超过部分减按1%"},
        },
    },
    "企业所得税": {
        "基本税率": {"rate": "25%", "scope": "大多数企业"},
        "小微企业": {"rate": "5%", "scope": "年应纳税所得额≤300万，从业≤300人，资产≤5000万"},
        "高新技术企业": {"rate": "15%", "scope": "经认定的高新技术企业"},
        "西部大开发": {"rate": "15%", "scope": "西部地区鼓励类产业"},
    },
    "个人所得税": {
        "综合所得": {
            "description": "工资薪金、劳务报酬、稿酬、特许权使用费",
            "brackets": [
                {"range": "≤36,000", "rate": "3%", "deduction": 0},
                {"range": "36,001-144,000", "rate": "10%", "deduction": 2520},
                {"range": "144,001-300,000", "rate": "20%", "deduction": 16920},
                {"range": "300,001-420,000", "rate": "25%", "deduction": 31920},
                {"range": "420,001-660,000", "rate": "30%", "deduction": 52920},
                {"range": "660,001-960,000", "rate": "35%", "deduction": 85920},
                {"range": ">960,000", "rate": "45%", "deduction": 181920},
            ],
        },
        "经营所得": {
            "description": "个体工商户、个人独资企业、合伙企业",
            "brackets": [
                {"range": "≤30,000", "rate": "5%", "deduction": 0},
                {"range": "30,001-90,000", "rate": "10%", "deduction": 1500},
                {"range": "90,001-300,000", "rate": "20%", "deduction": 10500},
                {"range": "300,001-500,000", "rate": "30%", "deduction": 40500},
                {"range": ">500,000", "rate": "35%", "deduction": 65500},
            ],
        },
        "其他": {
            "利息股息红利": "20%",
            "财产租赁": "20%",
            "财产转让": "20%",
            "偶然所得": "20%",
        },
    },
    "附加税": {
        "城市维护建设税": {"rates": {"市区": "7%", "县镇": "5%", "其他": "1%"}, "base": "实缴增值税+消费税"},
        "教育费附加": {"rate": "3%", "base": "实缴增值税+消费税"},
        "地方教育附加": {"rate": "2%", "base": "实缴增值税+消费税"},
    },
    "印花税": {
        "购销合同": "0.03%",
        "加工承揽合同": "0.03%",
        "建设工程合同": "0.03%",
        "租赁合同": "0.1%",
        "借款合同": "0.005%",
        "产权转移书据": "0.05%",
        "营业账簿": "0.025%",
        "权利许可证照": "5元/件",
    },
    "房产税": {
        "从价计征": {"rate": "1.2%", "base": "房产原值×(1-扣除比例)"},
        "从租计征": {"rate": "12%", "base": "租金收入"},
        "个人住房出租优惠": {"rate": "4%", "base": "租金收入"},
    },
    "消费税": {
        "卷烟": "56%+从量（生产环节）",
        "白酒": "20%+从量（生产环节）",
        "化妆品": "15%",
        "贵重首饰": "5%",
        "小汽车": "1%-40%（按排量）",
        "成品油": "定额（按升）",
    },
}

ALIASES = {
    "vat": "增值税", "增值税": "增值税", "增值": "增值税",
    "cit": "企业所得税", "企业所得税": "企业所得税", "所得税": "企业所得税", "企税": "企业所得税",
    "iit": "个人所得税", "个人所得税": "个人所得税", "个税": "个人所得税",
    "附加": "附加税", "附加税": "附加税", "城建税": "附加税", "教育费附加": "附加税",
    "印花税": "印花税", "stamp": "印花税",
    "房产税": "房产税", "房产税": "房产税",
    "消费税": "消费税", "消费": "消费税",
    "关税": "关税",
}


def format_tax(tax_name, data):
    """格式化税率输出"""
    lines = [f"\n📊 {tax_name}"]
    lines.append("=" * 50)

    def _format_val(val, indent="   "):
        """递归格式化值"""
        result = []
        if isinstance(val, dict):
            if "description" in val:
                result.append(f"{indent}范围: {val['description']}")
            if "brackets" in val:
                for b in val["brackets"]:
                    result.append(f"{indent}{b['range']:20s} 税率: {b['rate']}  速算扣除数: {b['deduction']}")
            if "rate" in val:
                result.append(f"{indent}税率: {val['rate']}")
                if "scope" in val:
                    result.append(f"{indent}范围: {val['scope']}")
                if "base" in val:
                    result.append(f"{indent}计税依据: {val['base']}")
            if "rates" in val:
                for k, v in val["rates"].items():
                    result.append(f"{indent}{k}: {v}")
            # recurse into sub-dicts that aren't special keys
            covered = {"description", "brackets", "rate", "scope", "base", "rates"}
            for k, v in val.items():
                if k not in covered:
                    if isinstance(v, dict) and "rate" in v:
                        # leaf rate dict
                        result.append(f"{indent}{k}:")
                        result.append(f"{indent}  税率: {v['rate']}")
                        if "scope" in v:
                            result.append(f"{indent}  范围: {v['scope']}")
                        if "base" in v:
                            result.append(f"{indent}  计税依据: {v['base']}")
                    elif isinstance(v, dict):
                        result.append(f"{indent}【{k}】")
                        result.extend(_format_val(v, indent + "  "))
                    elif isinstance(v, str):
                        result.append(f"{indent}{k}: {v}")
                    elif isinstance(v, list):
                        for item in v:
                            result.extend(_format_val(item, indent))
        else:
            result.append(f"{indent}{val}")
        return result

    if isinstance(data, dict):
        for key, val in data.items():
            lines.append(f"\n  【{key}】")
            lines.extend(_format_val(val))
    else:
        lines.extend(_format_val(data))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="中国税率查询工具")
    parser.add_argument("税种", help="税种名称（增值税/企业所得税/个人所得税/附加税/印花税/房产税/消费税/关税）")
    parser.add_argument("--纳税人类型", choices=["小规模", "一般"], default=None,
                        help="增值税纳税人类型")
    parser.add_argument("--地区", default=None, help="地区（影响城建税税率）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    tax_input = args.__dict__["税种"]
    tax_name = ALIASES.get(tax_input)

    if not tax_name:
        available = ", ".join(TAX_RATES.keys())
        print(f"❌ 未知税种: {tax_input}")
        print(f"支持的税种: {available}")
        sys.exit(1)

    data = TAX_RATES.get(tax_name)
    if not data:
        print(f"⚠️  {tax_name} 暂无数据")
        sys.exit(1)

    # 增值税特殊处理：按纳税人类型筛选
    if tax_name == "增值税" and args.纳税人类型:
        key = "小规模纳税人" if args.纳税人类型 == "小规模" else "一般纳税人"
        data = {key: data[key]}
    elif tax_name == "增值税":
        pass  # 显示全部

    # 附加税：地区影响城建税
    if tax_name == "附加税" and args.地区:
        pass  # 已在数据中

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_tax(tax_name, data))
        print(f"\n💡 提示: 以上数据基于2024年政策，实际以税务机关最新公告为准。")
        print(f"   详细政策参考: references/china_tax_rates.md")


if __name__ == "__main__":
    main()
