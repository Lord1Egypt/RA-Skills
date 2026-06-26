# symx_payment - 支付宝支付集成指南

## 问题说明

用户反馈"看不到支付宝调取"，这是因为之前的测试脚本使用模拟数据，没有真正输出支付宝收银台链接。

---

## 解决方案

### 方式 1：使用 index.py 脚本（推荐）

**完整充值流程（包含支付宝支付）：**

```bash
cd /home/admin/.openclaw/skills/symx-payment/scripts

# 运行充值流程
python3 index.py recharge 13800138000
```

**输出示例：**

```
============================================================
  步骤 5: 调起支付宝支付
============================================================

🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴
请处理以下支付请求：
订单 ID: ORD20260428134900
金额：¥ 100
收银台链接：https://excashier.alipay.com/pc.htm?outTradeNo=13800138000_100
🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

[ALIPAY_PAYMENT_REQUEST]
{
  "type": "alipay_payment",
  "orderId": "ORD20260428134900",
  "amount": 100,
  "cashierUrl": "https://excashier.alipay.com/pc.htm?outTradeNo=13800138000_100",
  "detail": "增值账户续费 - 标准套餐 - 账号：13800138000 - 金额：100 元",
  "phoneNumber": "13800138000"
}
[/ALIPAY_PAYMENT_REQUEST]
```

**关键点：** 输出中包含 `excashier.alipay.com` 链接，这会触发 OpenClaw 的 `alipay-pay-for-service` 技能。

---

### 方式 2：使用 alipay_integration.py 模块

```python
from alipay_integration import create_recharge_order, trigger_alipay_payment

# 创建订单
order_result = create_recharge_order(
    phone="13800138000",
    amount=100,
    package_type="标准套餐",
    detail="增值账户续费 - 标准套餐"
)

if order_result["success"]:
    order = order_result["data"]
    # 触发支付宝支付
    payment_output = trigger_alipay_payment(
        cashier_url=order["cashierUrl"],
        amount=order["amount"],
        detail=order["detail"]
    )
    print(payment_output)
```

---

### 方式 3：在 OpenClaw 中自动调用支付宝技能

修改 `SKILL.md` 添加自动调用逻辑：

```markdown
## 支付宝支付自动调用

当创建充值订单后，自动调用 `alipay-pay-for-service` 技能：

1. 获取收银台链接（cashierUrl）
2. 使用 sessions_spawn 调用支付宝支付技能
3. 等待支付完成
4. 根据结果调用回调接口
```

**实际调用代码（Python）：**

```python
import subprocess


def call_alipay_skill(cashier_url):
    """调用支付宝支付技能"""
    # 在 OpenClaw 环境中，这会触发 alipay-pay-for-service 技能
    cmd = f'openclaw message send --message "请使用支付宝支付：{cashier_url}"'
    subprocess.run(cmd, shell=True)
```

---

## 测试支付宝支付流程

### 测试命令

```bash
# 1. 运行充值流程（会输出支付宝链接）
python3 index.py recharge 13800138000

# 2. 测试支付宝集成模块
python3 alipay_integration.py

# 3. 测试支付回调（模拟成功）
python3 index.py callback ORD123 ALIPAY_PROOF_123 13800138000 true
```

---

## 支付宝技能触发机制

`alipay-pay-for-service` 技能的触发条件：

1. **URL 触发**：消息中包含 `cashier*.alipay.com` 或 `excashier*.alipay.com`
2. **关键词触发**：消息中包含"请使用支付宝支付"等文字
3. **技能调用**：直接使用 `sessions_spawn` 调用

**我们的实现：**

- `index.py` 输出的链接格式：`https://excashier.alipay.com/pc.htm?...`
- 符合触发条件 ✅

---

## 完整流程演示

```
用户：帮我充值 100 元

↓ 执行 python3 index.py recharge 13800138000

1. ✅ 查询账户 → 余额不足
2. ✅ 选择充值金额 → 100 元
3. ✅ 生成充值明细
4. ✅ 创建订单 → 获取 cashierUrl
5. 🔴 输出支付宝支付请求（包含 excashier.alipay.com 链接）
   ↓
   OpenClaw 检测到支付宝链接
   ↓
   自动调用 alipay-pay-for-service 技能
   ↓
   用户完成支付
   ↓
6. ✅ 支付回调 → 更新账户数据
```

---

## 注意事项

1. **真实 API 环境**：需要配置 Token 和可访问的云端 API
2. **支付宝钱包**：首次使用需要调用 `alipay-authenticate-wallet` 开通
3. **支付凭证**：支付成功后保存 paymentProof 用于回调
4. **测试模式**：API 不可用时会自动使用模拟数据

---

## 文件清单

| 文件                              | 用途       |
|---------------------------------|----------|
| `scripts/index.py`              | 主入口，完整流程 |
| `scripts/alipay_integration.py` | 支付宝集成模块  |
| `scripts/query.py`              | 账户查询     |
| `scripts/recharge.py`           | 充值流程     |
| `scripts/callback.py`           | 支付回调     |

---

## 快速测试

```bash
cd /home/admin/.openclaw/skills/symx-payment/scripts

# 运行完整充值流程（会看到支付宝链接）
python3 index.py recharge 13800138000
```
