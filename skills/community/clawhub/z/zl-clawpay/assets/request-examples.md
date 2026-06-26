# 请求示例（Node.js 版本）

本文档提供 ZL-ClawPay 技能所有接口的完整请求示例和预期响应。

> 📚 **详细接口定义**请参考 [api-spec.md](../references/api-spec.md)
> 
> 📚 **使用场景指南**请参考 [SKILL.md](../SKILL.md)

---

## 命令格式说明

### 基本格式

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=<INTERFACE_CODE> \
  -method=<METHOD> \
  -endpoint=<ENDPOINT> \
  [--<key>=<value> ...]
```

### 参数说明

| 参数 | 必填 | 说明 |
| -------- | -------- | -------- |
| `-interfaceId` | 是 | 接口代码（如 C00003、C00009、L00001 等） |
| `-method` | 是 | 请求方法：`POST` 或 `local` |
| `-endpoint` | 否 | API 端点路径（local 接口不需要） |
| `--<key>=<value>` | 否 | 接口参数，按需传入 |

### 凭据传递规则

| 接口 | 凭据传递方式 |
|------|-------------|
| C00003 | 需传入 `--apiKey`、`--subWalletName`、`--subWalletId` |
| C00011 | 需传入 `--subWalletName`（AI 从 user.md 自动获取） |
| 其他接口 | apiKey 和 subWalletId 自动从本地 `~/.zl-claw-pay/state.json` 读取 |

> 🔒 **传输安全**：所有 API 请求必须使用 HTTPS 协议，严禁使用 HTTP。

---

## 本地接口说明

本地接口使用 `method=local`，无需 `-endpoint` 参数：

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=<INTERFACE_CODE> \
  -method=local
```

**特点**：
- 直接本地 Node.js 方法调用
- 无 HTTP 网络请求
- 不涉及第三方（ZLPay）
- 接口代码以 `L` 开头

---

## 接口示例

### 1. 绑定子钱包 (C00003)

**场景**：用户首次使用，需要绑定子钱包

**说明**：绑定成功后，凭据将加密保存到本地 `~/.zl-claw-pay/state.json`

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00003 \
  -method=POST \
  -endpoint=/post/claw/bind-sub-wallet \
  --apiKey=your_64hex_sm2_private_key \
  --subWalletName=your_wallet_name \
  --subWalletId=your_sub_wallet_id
```

**预期响应（成功）**：
```json
{
  "resCode": "S010000",
  "resMsg": "Success",
  "resData": {
    "subWalletId": "a1b2c3d4e5f6..."
  }
}
```

---

### 2. 查询支付状态 (C00005)

**场景**：发起支付后，查询订单支付结果

**说明**：使用发起支付时返回的 `seqId` 作为 `orgSeqId` 查询

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00005 \
  -method=POST \
  -endpoint=/post/claw/query-pay-status \
  --orgSeqId=MERCH123456789
```

**商户收款场景**（需要传入 merApiKey）：

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00005 \
  -method=POST \
  -endpoint=/post/claw/query-pay-status \
  --orgSeqId=MERCH123456789 \
  --merApiKey=ak_xxxxxxxxxxxxxxxxx
```

**预期响应**：
```json
{
  "resCode": "S010000",
  "resMsg": "Success",
  "resData": {
    "orderStatus": "success"
  }
}
```

---

### 3. 查询交易记录 (C00007)

**场景**：用户查看历史交易流水或对账

**说明**：日期参数可选，不传则默认查询当天

**默认查询（当天）**：
```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00007 \
  -method=POST \
  -endpoint=/post/claw/query-receipt-list
```

**自定义日期范围**：
```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00007 \
  -method=POST \
  -endpoint=/post/claw/query-receipt-list \
  --startDate=20260301 \
  --endDate=20260331
```

**预期响应**：
```json
{
  "resCode": "S010000",
  "resMsg": "Success",
  "resData": {
    "receiptList": []
  }
}
```

---

### 4. 发起支付 (C00009)

**场景**：用户确认支付后发起免密支付

> ⚠️ **风险提示**：此命令会发起真实金融交易，产生实际扣款。执行前请确认商户、金额和订单信息正确。

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00009 \
  -method=POST \
  -endpoint=/post/pay-claw/payment \
  --amount=100 \
  --merApiKey=ak_xxxxxxxxxxxxxxxxx \
  --orderDetail=商品购买 \
  --seqId=MERCH202601010001
```

**预期响应**：
```json
{
  "resCode": "S010000",
  "resMsg": "成功",
  "resData": {
    "seqId": "17772584730259962885995302852576",
    "orderStatus": "成功"
  }
}
```

---

### 5. 撤销绑定 (C00011)

**场景**：用户需要彻底撤销子钱包绑定（不可逆操作）

**说明**：成功后本地凭据也会被清除，API key 永久禁用

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00011 \
  -method=POST \
  -endpoint=/post/pay-claw/unbind-sub-wallet \
  --subWalletName=我的子钱包
```

> **注意**：`apiKey` 和 `subWalletId` 自动从本地 state.json 读取，无需传入。`subWalletName` 由 AI 从 user.md 自动获取。

**预期响应**：
```json
{
  "resCode": "S010000",
  "resMsg": "Success",
  "resData": {
    "unbindStatus": "已解绑"
  }
}
```

---

### 6. 查询子钱包 (L00001)

**场景**：查询当前子钱包绑定状态

**说明**：本地接口，不涉及网络请求

```bash
node {baseDir}/scripts/skill.js call -interfaceId=L00001 -method=local
```

**预期响应（已绑定）**：
```json
{
  "resCode": "S010000",
  "resMsg": "已绑定",
  "subWalletId": "a1b2***c3d4",
  "bindStatus": "已绑定"
}
```

**预期响应（未绑定）**：
```json
{
  "resCode": "S010000",
  "resMsg": "未绑定",
  "subWalletId": null,
  "bindStatus": "未绑定"
}
```

---

### 7. 解绑子钱包 (L00002)

**场景**：本地清除凭据，但不通知服务端

**说明**：如需彻底撤销绑定，请使用 C00011

```bash
node {baseDir}/scripts/skill.js call -interfaceId=L00002 -method=local
```

**预期响应（成功）**：
```json
{
  "resCode": "S010000",
  "resMsg": "解绑成功",
  "subWalletId": "a1b2***c3d4",
  "unbindStatus": "已解绑"
}
```

**预期响应（未绑定）**：
```json
{
  "resCode": "F010001",
  "resMsg": "未绑定子钱包",
  "unbindStatus": "解绑失败"
}
```

---

## 接口速查表

| 序号 | 接口 | 功能 | 方法 | 场景 |
|------|------|------|------|------|
| 1 | C00003 | 绑定子钱包 | POST | 首次使用 |
| 2 | C00005 | 查询支付状态 | POST | 支付后查询 |
| 3 | C00007 | 查询交易记录 | POST | 查看流水 |
| 4 | C00009 | 发起支付 | POST | 确认支付 |
| 5 | C00011 | 撤销绑定 | POST | 彻底解绑 |
| 6 | L00001 | 查询子钱包 | local | 查询状态 |
| 7 | L00002 | 解绑子钱包 | local | 本地解绑 |

---

## 相关文档

- [SKILL.md](../SKILL.md) - 技能说明、使用场景、执行规则
- [api-spec.md](../references/api-spec.md) - 详细接口定义、参数说明、错误码
