# symx_payment API 配置参考

## 云端 API 配置

### 基础配置

```json
{
  "baseUrl": "https://lifeemergence.com/jeecg-boot-xzgz",
  "authType": "bearer",
  "token": "YOUR_BEARER_TOKEN_HERE"
}
```

### 接口路径

| 接口     | 路径                      | 方法   | 说明               |
|--------|-------------------------|------|------------------|
| 账户查询   | `/api/account/query`    | POST | 查询账户余额、使用次数等     |
| 创建充值订单 | `/api/account/recharge` | POST | 创建充值订单，返回支付宝支付参数 |
| 支付成功回调 | `/api/payment/success`  | POST | 支付成功后回写数据        |
| 支付失败回调 | `/api/payment/fail`     | POST | 支付失败后记录          |

---

## 接口详情

### 1. 账户查询接口

**请求：**

```json
POST /api/account/query
Authorization: Bearer <token>
Content-Type: application/json

{
"phoneNumber": "13800138000"
}
```

**响应：**

```json
{
  "totalRecharged": 1000.00,
  "balance": 50.00,
  "remainingUses": 10,
  "usedCount": 90,
  "isInsufficient": false
}
```

---

### 2. 创建充值订单接口

**请求：**

```json
POST /api/account/recharge
Authorization: Bearer <token>
Content-Type: application/json

{
"phoneNumber": "13800138000",
"amount": 100,
"detail": "增值账户续费 - 标准套餐 - 账号：13800138000 - 金额：100 元",
"packageType": "标准套餐"
}
```

**响应：**

```json
{
  "orderId": "ORD20260428001",
  "amount": 100,
  "alipayParams": {
    // 支付宝支付参数
  },
  "cashierUrl": "https://cashier.alipay.com/..."
}
```

---

### 3. 支付成功回调接口

**请求：**

```json
POST /api/payment/success
Authorization: Bearer <token>
Content-Type: application/json

{
"orderId": "ORD20260428001",
"paymentProof": "支付宝支付凭证",
"amount": 100,
"phoneNumber": "13800138000",
"status": "SUCCESS"
}
```

**响应：**

```json
{
  "rechargedAmount": 100,
  "rechargedCount": 1,
  "newBalance": 150
}
```

---

### 4. 支付失败回调接口

**请求：**

```json
POST /api/payment/fail
Authorization: Bearer <token>
Content-Type: application/json

{
"orderId": "ORD20260428001",
"errorReason": "用户取消支付",
"phoneNumber": "13800138000",
"status": "FAILED"
}
```

**响应：**

```json
{
  "orderId": "ORD20260428001",
  "message": "已记录失败"
}
```

---

## 配置方式

### 方式 1：修改脚本中的 API_CONFIG

直接编辑 `scripts/query.py`、`scripts/recharge.py`、`scripts/callback.py` 中的 `API_CONFIG` 字典。

### 方式 2：使用环境变量（推荐）

```bash
export SYMX_API_BASE_URL="https://lifeemergence.com/jeecg-boot-xzgz"
export SYMX_API_TOKEN="your-bearer-token"
export SYMX_API_AUTH_TYPE="bearer"
```

### 方式 3：创建配置文件

在 `references/` 目录下创建 `config.json`：

```json
{
  "baseUrl": "https://lifeemergence.com/jeecg-boot-xzgz",
  "authType": "bearer",
  "token": "your-bearer-token",
  "queryPath": "/api/account/query",
  "rechargePath": "/api/account/recharge",
  "callbackSuccessPath": "/api/payment/success",
  "callbackFailPath": "/api/payment/fail"
}
```

---

## 充值金额档位

默认档位：`[10, 50, 100, 500]` 元

可在 `scripts/recharge.py` 中修改 `RECHARGE_AMOUNTS` 列表自定义档位。

---

## 充值明细格式

默认格式：

```
增值账户续费 - {套餐类型} - 账号：{手机号} - 金额：{金额}元 - 备注：{备注}
```

套餐类型可选：

- 体验套餐
- 标准套餐
- 专业套餐

---

## 测试命令

```bash
# 测试账户查询
python3 scripts/query.py 13800138000 <token>

# 测试充值明细生成
python3 scripts/recharge.py

# 测试回调（需要真实订单 ID）
python3 scripts/callback.py
```
