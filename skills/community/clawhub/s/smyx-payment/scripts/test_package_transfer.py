#!/usr/bin/env python3
"""测试套餐信息传递给云端接口"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recharge import get_recharge_packages, create_recharge_order, generate_recharge_detail

# 测试套餐信息
packages = get_recharge_packages()
print("\n充值套餐列表：")
for i, pkg in enumerate(packages, 1):
    print(f"{i}. {pkg['name']} - ¥{pkg['amount']}元 - {pkg['uses']}次")

# 选择套餐（测试用）
test_package = packages[1]  # 选择基础套餐
print(f"\n已选择：{test_package['name']}")

# 生成充值明细
phone = "13800138000"
detail = generate_recharge_detail(
    phone=phone,
    amount=test_package["amount"],
    package_type=test_package["name"],
    remark="测试套餐信息传递"
)

print(f"\n充值明细：{detail}")

# 创建订单（模拟传递给云端接口）
print("\n模拟调用云端接口...")
print(f"请求参数：")
print(f"  phoneNumber: {phone}")
print(f"  amount: {test_package['amount']}")
print(f"  packageType: {test_package['name']}")
print(f"  package: {test_package}")
print(f"  detail: {detail}")

print("\n✅ 套餐信息已准备好传递给云端接口！")
print("\n云端接口将收到：")
print(f"""
{{
  "phoneNumber": "{phone}",
  "amount": {test_package['amount']},
  "packageType": "{test_package['name']}",
  "package": {{
    "amount": {test_package['amount']},
    "uses": {test_package['uses']},
    "name": "{test_package['name']}"
  }},
  "detail": "{detail}"
}}
""")
