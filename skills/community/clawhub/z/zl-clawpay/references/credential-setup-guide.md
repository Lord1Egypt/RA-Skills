# 凭据配置引导

ZL-ClawPay 技能使用**本地加密存储**模式管理凭据，无需配置环境变量。首次使用时通过 **C00003 绑定子钱包** 接口将凭据加密保存到本地。

## 凭据存储方式

| 配置项 | 存储方式 | 说明 |
|--------|----------|------|
| `apiKey`（SM2 私钥） | 本地加密存储 `~/.zl-claw-pay/state.json` | 证联 APP 获取，仅用于客户端 SM2 签名，不传给服务器 |
| `subWalletId`（子钱包ID） | 本地加密存储 `~/.zl-claw-pay/state.json` | 证联 APP 获取，用作请求头 appId |

> 🔐 **加密方式**：`apiKey` 和 `subWalletId` 使用 AES-256-GCM 加密存储，密钥由机器特征派生。

## 首次使用流程

### 1. 获取凭据信息

在证联 APP 中获取以下信息：

| 参数 | 说明 | 获取位置 |
|------|------|----------|
| `apiKey` | SM2 私钥（64位 hex） | 证联 APP → 我的 → API 密钥 |
| `subWalletId` | 子钱包 ID（32位 hex） | 证联 APP → 我的 → 子钱包管理 |
| `subWalletName` | 子钱包名称 | AI 从 OpenClaw user.md 自动获取 |

> ⚠️ **安全提醒**：`apiKey` 是 SM2 私钥，等同于你的支付密码，**切勿通过对话框传递**，仅在绑定命令中使用一次。

### 2. 执行绑定命令

使用 C00003 接口绑定子钱包，凭据将自动加密保存到本地：

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00003 \
  -method=POST \
  -endpoint=/post/claw/bind-sub-wallet \
  --apiKey=<64位hex密钥> \
  --subWalletName=<子钱包名称> \
  --subWalletId=<32位hex子钱包ID>
```

绑定成功后：
- `apiKey` 和 `subWalletId` 已加密保存到 `~/.zl-claw-pay/state.json`
- 后续所有接口自动从本地读取凭据，无需再次传入

## 校验绑定状态

查询当前绑定状态：

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

## 配置失败处理

### apiKey 验证失败

**错误信息**：
```
apiKey 验证失败：无效的 SM2 私钥格式
```

**解决方法**：
1. 确认 apiKey 为 64 位 hex 字符串
2. 核对 apiKey 是否与证联 APP 中显示的一致
3. 确认该密钥未过期或被撤销

### subWalletId 验证失败

**错误信息**：
```
subWalletId 验证失败：子钱包不存在
```

**解决方法**：
1. 确认 subWalletId 为 32 位 hex 字符串
2. 查看证联 APP → 我的 → 子钱包管理，确认子钱包 ID
3. 如果尚未创建子钱包，请先在证联 APP 中创建

### 子钱包名称不匹配

**错误信息**：
```
子钱包名称不匹配：申报名称与实际名称不一致
```

**解决方法**：
1. 确认 `subWalletName` 与证联 APP 中申报时上送的名称一致
2. AI 会自动从 OpenClaw user.md 获取智能体名称，请确保配置正确

## 更换/删除凭据

| 操作 | 方法 | 说明 |
|------|------|------|
| **本地解绑** | 调用 `L00002` 接口 | 仅清除本地凭据，服务端绑定关系保留 |
| **服务端撤销** | 调用 `C00011` 接口 | 不可逆操作，API key 将被永久禁用 |

### 本地解绑示例

```bash
node {baseDir}/scripts/skill.js call -interfaceId=L00002 -method=local
```

### 服务端撤销示例

```bash
node {baseDir}/scripts/skill.js call \
  -interfaceId=C00011 \
  -method=POST \
  -endpoint=/post/pay-claw/unbind-sub-wallet \
  --subWalletName=<子钱包名称>
```

> ⚠️ **注意**：C00011 撤销绑定是**不可逆操作**，撤销后该 API key 将被永久禁用，无法再次使用。
