# 请求示例（Node.js 版本）

---

## 命令格式

所有 API 调用使用以下命令格式：

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=<INTERFACE_CODE> \
  -method=<METHOD> \
  -endpoint=<ENDPOINT> \
  [--<key>=<value> ...]
```

### 参数说明

| 参数 | 说明 |
| -------- | -------- |
| `-interfaceId` | 接口代码（如 C00003、C00009、L00001 等），必填 |
| `-method` | HTTP 方法 (POST) 或 local |
| `-endpoint` | API 端点路径（local 接口不需要） |
| `--<key>=<value>` | 接口参数，按需传入 |

> **凭据说明**：
> - C00003 绑定子钱包时，需传入 `--apiKey`、`--subWalletName`、`--subWalletId`
> - 其他接口的 apiKey 和 subWalletId 自动从本地 `~/.zl-claw-pay/state.json` 读取，无需在命令行传入
> - C00011 需要传入 `--subWalletName`（AI 从 user.md 自动获取）
>
> 🔒 **传输安全**：所有 API 请求必须使用 HTTPS 协议，严禁使用 HTTP。

---

## 本地接口

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

## 1. 绑定子钱包 (C00003)

> **首次使用必须先执行此接口**，绑定成功后凭据加密保存到本地 `~/.zl-claw-pay/state.json`。

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00003 \
  -method=POST \
  -endpoint=/post/claw/bind-sub-wallet \
  --apiKey=your_64hex_sm2_private_key \
  --subWalletName=your_wallet_name \
  --subWalletId=your_sub_wallet_id
```

**预期响应**：
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

## 2. 查询子钱包 (L00001)

查询当前绑定的子钱包信息。

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

## 3. 发起支付 (C00009)

发起免密支付。当用户意图清晰时直接执行支付。

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

## 4. 查询支付状态 (C00005)

查询支付交易状态。

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

## 5. 查询交易记录 (C00007)

查询交易流水记录。

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

## 6. 撤销绑定 (C00011)

撤销子钱包绑定（不可逆操作）。成功后本地凭据也会被清除。

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

## 7. 解绑子钱包 (L00002)

本地解绑子钱包，清除本地凭据（不通知服务端）。

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

## 8. 卸载技能 (L99999)

清除本地凭据数据。此操作不可逆。

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=L99999 \
  -method=local
```

**预期响应**：
```json
{
  "resCode": "S010000",
  "resMsg": "卸载成功",
  "details": {
    "wasBound": true,
    "hadApiKey": true,
    "stateCleared": true,
    "skillDir": "/path/to/skill",
    "nodeModulesDir": "/path/to/skill/node_modules"
  }
}
```
