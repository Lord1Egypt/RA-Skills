#!/usr/bin/env python3
"""发票识别工具 - 免费版（Mock OCR）
用法: python3 invoice_ocr.py <发票图片路径> [--json]

生产环境替换 _ocr_mock() 为真实OCR API调用。
推荐: 百度AI发票识别API 或 阿里云发票识别API
"""

import argparse
import json
import os
import sys
from datetime import datetime


def _ocr_mock(image_path):
    """Mock发票识别结果 - 替换为真实OCR API

    百度AI示例:
    ```python
    from aip import AipOcr
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    with open(image_path, 'rb') as f:
        result = client.vatInvoice(f.read())
    ```

    阿里云示例:
    ```python
    from alibabacloud_ocr_api20210707.client import Client
    # ... 调用 RecognizeVatInvoice
    ```
    """
    if not os.path.exists(image_path):
        return None

    # 根据文件名模拟不同发票类型
    basename = os.path.basename(image_path).lower()

    if "专票" in basename or "special" in basename:
        return {
            "发票类型": "增值税专用发票",
            "发票代码": "1100214130",
            "发票号码": "08492315",
            "开票日期": "2024-03-15",
            "校验码": "12345678901234567890",
            "购买方": {
                "名称": "北京某某科技有限公司",
                "纳税人识别号": "91110108MA01XXXXX1",
                "地址电话": "北京市海淀区中关村大街1号 010-12345678",
                "开户行及账号": "工商银行北京中关村支行 1234567890123456789",
            },
            "销售方": {
                "名称": "上海某某商贸有限公司",
                "纳税人识别号": "91310115MA02XXXXX2",
                "地址电话": "上海市浦东新区陆家嘴路100号 021-87654321",
                "开户行及账号": "建设银行上海浦东支行 9876543210987654321",
            },
            "货物或服务": [
                {"名称": "办公用品", "规格": "A4复印纸", "单位": "箱", "数量": 10,
                 "单价": 150.00, "金额": 1500.00, "税率": "13%", "税额": 195.00},
                {"名称": "打印耗材", "规格": "墨盒", "单位": "个", "数量": 5,
                 "单价": 200.00, "金额": 1000.00, "税率": "13%", "税额": 130.00},
            ],
            "金额合计": 2500.00,
            "税额合计": 325.00,
            "价税合计": 2825.00,
            "价税合计大写": "贰仟捌佰贰拾伍元整",
        }
    else:
        return {
            "发票类型": "增值税普通发票",
            "发票代码": "011002100211",
            "发票号码": "49238156",
            "开票日期": "2024-03-20",
            "校验码": "98765432109876543210",
            "购买方": {
                "名称": "北京某某科技有限公司",
                "纳税人识别号": "91110108MA01XXXXX1",
            },
            "销售方": {
                "名称": "京东集团",
                "纳税人识别号": "91110302MA00XXXXX3",
            },
            "货物或服务": [
                {"名称": "笔记本电脑", "规格": "ThinkPad X1", "单位": "台", "数量": 1,
                 "单价": 8999.00, "金额": 8999.00, "税率": "13%", "税额": 1169.87},
            ],
            "金额合计": 8999.00,
            "税额合计": 1169.87,
            "价税合计": 10168.87,
            "价税合计大写": "壹万零壹佰陆拾捌元捌角柒分",
        }


def format_invoice(data):
    """格式化发票信息输出"""
    lines = [
        "\n🧾 发票识别结果",
        "=" * 50,
        f"  发票类型: {data.get('发票类型', 'N/A')}",
        f"  发票代码: {data.get('发票代码', 'N/A')}",
        f"  发票号码: {data.get('发票号码', 'N/A')}",
        f"  开票日期: {data.get('开票日期', 'N/A')}",
        f"  校验码:   {data.get('校验码', 'N/A')}",
    ]

    # 购买方
    buyer = data.get("购买方", {})
    if isinstance(buyer, dict):
        lines.append("\n  📥 购买方:")
        for k, v in buyer.items():
            lines.append(f"    {k}: {v}")

    # 销售方
    seller = data.get("销售方", {})
    if isinstance(seller, dict):
        lines.append("\n  📤 销售方:")
        for k, v in seller.items():
            lines.append(f"    {k}: {v}")

    # 货物或服务
    items = data.get("货物或服务", [])
    if items:
        lines.append("\n  📦 货物/服务明细:")
        lines.append(f"    {'名称':<12s} {'数量':>4s} {'单价':>10s} {'金额':>10s} {'税率':>5s} {'税额':>10s}")
        lines.append(f"    {'-'*62}")
        for item in items:
            lines.append(
                f"    {item.get('名称',''):<12s} {item.get('数量',0):>4} "
                f"{item.get('单价',0):>10.2f} {item.get('金额',0):>10.2f} "
                f"{item.get('税率',''):<5s} {item.get('税额',0):>10.2f}"
            )

    # 合计
    lines.append(f"\n  💰 金额合计: ¥{data.get('金额合计', 0):,.2f}")
    lines.append(f"  💰 税额合计: ¥{data.get('税额合计', 0):,.2f}")
    lines.append(f"  💰 价税合计: ¥{data.get('价税合计', 0):,.2f}")
    lines.append(f"  大写: {data.get('价税合计大写', 'N/A')}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="发票识别工具")
    parser.add_argument("发票图片", help="发票图片路径")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--use-api", action="store_true",
                        help="使用真实OCR API（需配置API密钥）")
    args = parser.parse_args()

    image_path = args.__dict__["发票图片"]

    if not os.path.exists(image_path):
        print(f"❌ 文件不存在: {image_path}")
        sys.exit(1)

    # 检查是否使用真实API
    if args.use_api:
        # TODO: 接入真实OCR API
        print("⚠️  真实OCR API尚未接入，使用Mock模式。")
        print("   请在脚本中配置百度AI或阿里云OCR API密钥。")

    result = _ocr_mock(image_path)
    if not result:
        print("❌ 无法识别发票，请确保图片清晰")
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_invoice(result))
        print(f"\n💡 提示: 当前为Mock模式，识别结果为模拟数据。")
        print(f"   接入真实OCR后，将使用百度AI/阿里云API进行识别。")


if __name__ == "__main__":
    main()
