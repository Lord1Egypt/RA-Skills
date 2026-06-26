#!/usr/bin/env python3
"""
测试订单信息绑定流程
展示业务订单与支付宝订单的绑定关系
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recharge import get_recharge_packages, generate_recharge_detail

# 测试数据
phone = "13800138000"
package = get_recharge_packages()[1]  # 基础套餐

print("\n")
print("╔" + "═" * 80 + "╗")
print("║" + " " * 25 + "订单信息绑定流程测试" + " " * 25 + "║")
print("╚" + "═" * 80 + "╝")

# 1. 用户选择套餐
print("\n【步骤 1】用户选择套餐")
print(f"  套餐名称：{package['name']}")
print(f"  充值金额：¥{package['amount']}元")
print(f"  可用次数：{package['uses']}次")

# 2. 创建业务订单（云端）
print("\n【步骤 2】创建业务订单（调用云端接口）")
cloud_order_id = f"CLOUD_{phone}_20260428170001"
print(f"  云端订单 ID: {cloud_order_id}")

# 3. 创建支付宝订单
print("\n【步骤 3】创建支付宝订单")
alipay_out_trade_no = f"ORDER_{phone}_20260428170001"
print(f"  商户订单号：{alipay_out_trade_no}")

# 4. 传递参数给云端订单接口
print("\n【步骤 4】传递订单信息给云端接口")
print(f"""
  请求参数：
  {{
    "phoneNumber": "{phone}",
    "amount": {package['amount']},
    "packageType": "{package['name']}",
    "package": {{
      "amount": {package['amount']},
      "uses": {package['uses']},
      "name": "{package['name']}"
    }},
    "cloudOrderId": "{cloud_order_id}",
    "alipayOutTradeNo": "{alipay_out_trade_no}"
  }}
""")

# 5. 云端返回
print("\n【步骤 5】云端接口返回")
print(f"""
  响应数据：
  {{
    "success": true,
    "data": {{
      "orderId": "{cloud_order_id}",
      "status": "PENDING_PAYMENT",
      "amount": {package['amount']},
      "uses": {package['uses']}
    }}
  }}
""")

# 6. 调起支付宝支付
print("\n【步骤 6】调起支付宝支付")
print(f"""
  支付宝请求参数：
  {{
    "app_id": "2021006150611467",
    "method": "alipay.trade.page.pay",
    "biz_content": {{
      "out_trade_no": "{alipay_out_trade_no}",
      "total_amount": "{package['amount']}",
      "subject": "增值账户续费 - {package['name']}",
      "body": "增值账户续费 - {phone}|套餐:{package['name']}|{package['amount']}元|{package['uses']}次",
      "extend_params": {{
        "cloud_order_id": "{cloud_order_id}"
      }}
    }}
  }}
""")

# 7. 支付成功回调
print("\n【步骤 7】支付宝支付成功回调")
alipay_trade_no = "2026042822001234567890123456"
print(f"""
  支付宝回调参数：
  {{
    "trade_no": "{alipay_trade_no}",  // 支付宝交易号
    "out_trade_no": "{alipay_out_trade_no}",  // 商户订单号
    "cloud_order_id": "{cloud_order_id}",  // 云端订单 ID（通过 extend_params 回传）
    "total_amount": "{package['amount']}",
    "trade_status": "TRADE_SUCCESS"
  }}
""")

# 8. 更新业务订单
print("\n【步骤 8】更新业务订单（调用云端接口）")
print(f"""
  请求参数：
  {{
    "cloudOrderId": "{cloud_order_id}",
    "alipayTradeNo": "{alipay_trade_no}",
    "alipayOutTradeNo": "{alipay_out_trade_no}",
    "amount": {package['amount']},
    "uses": {package['uses']},
    "status": "PAID"
  }}
""")

# 9. 最终结果
print("\n【步骤 9】订单绑定完成")
print(f"""
  订单绑定关系：
  ┌─────────────────────────────────────────────────┐
  │  业务订单 ID:    {cloud_order_id}
  │  支付宝订单号：  {alipay_out_trade_no}
  │  支付宝交易号：  {alipay_trade_no}
  │  充值金额：      ¥{package['amount']}元
  │  可用次数：      {package['uses']}次
  │  订单状态：      ✅ 已支付
  └─────────────────────────────────────────────────┘
""")

print("\n✅ 订单信息绑定流程测试完成！")
print("\n关键要点：")
print("  1. 云端订单 ID 通过 extend_params.cloud_order_id 传递给支付宝")
print("  2. 支付宝回调时会回传 cloud_order_id")
print("  3. 通过 cloud_order_id 可以关联业务订单和支付宝订单")
print("  4. 套餐信息通过 body 参数传递给支付宝（用于显示）")
print("  5. 套餐详细信息通过 package 参数传递给云端接口")
