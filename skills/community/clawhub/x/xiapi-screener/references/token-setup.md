# Token 配置指南

## 获取 Token

### 步骤 1：注册并登录大虾皮

访问 [daxiapi.com](https://daxiapi.com) 注册并登录账号。

### 步骤 2：开通 API Token 功能

1. 进入个人主页
2. 找到「API 管理」或「会员中心」
3. 开通 API Token 功能（可能需要 VIP 会员）

### 步骤 3：生成 Token

在 API 管理页面生成你的专属 Token。

> ⚠️ **注意**：Token 是敏感信息，请妥善保管，不要泄露给他人。

## 配置 Token

### 方式一：通过 CLI 配置（推荐）

```bash
# 设置 Token
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI

# 验证配置
npx daxiapi-cli@latest config get token
```

**配置文件位置**：

- macOS/Linux: `~/.daxiapi/config.json`
- Windows: `%USERPROFILE%\.daxiapi\config.json`

### 方式二：环境变量

```bash
# Linux/macOS
export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI

# Windows (CMD)
set DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI

# Windows (PowerShell)
$env:DAXIAPI_TOKEN="YOUR_TOKEN_FROM_DAXIAPI"
```

### 方式三：在代码中直接使用

```javascript
const api = require('daxiapi-cli/lib/api');

// 直接传入 Token
const data = await api.getPatternStocks('YOUR_TOKEN', 'vcp');
```

## 验证 Token

```bash
# 测试命令 - 获取 VCP 形态股票
npx daxiapi-cli@latest stock pattern vcp

# 如果返回正常数据，则 Token 配置成功
# 如果返回 401 错误，则 Token 无效或未配置
```

## 常见问题

### Q1: Token 配置后仍然提示未配置？

**可能原因**：

1. Token 配置在错误的 shell 会话中
2. 环境变量未生效
3. 配置文件权限问题

**解决方案**：

```bash
# 检查配置文件
cat ~/.daxiapi/config.json

# 重新配置
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI

# 验证
npx daxiapi-cli@latest config get token
```

### Q2: 提示 401 Unauthorized？

**可能原因**：

1. Token 无效或已过期
2. 非 VIP 用户无法使用 API
3. Token 格式错误

**解决方案**：

1. 重新登录大虾皮网站检查 Token 状态
2. 确认是否开通 VIP 会员
3. 复制完整的 Token（注意不要有多余空格）

### Q3: 提示请求频率超限？

**API 限制**：

- 每分钟限制 10 次请求
- 每日限制 1000 次请求

**解决方案**：

等待 30-60 秒后重试。

## 安全建议

1. **不要将 Token 提交到代码仓库**
2. **不要在公开场合分享 Token**
3. **定期更换 Token**
4. **如果 Token 泄露，立即在大虾皮网站重新生成**

## Token 权限说明

| 功能         | 免费用户 | VIP 用户 |
| ------------ | -------- | -------- |
| 市场指数数据 | ✅       | ✅       |
| 行业板块数据 | ✅       | ✅       |
| 股票形态筛选 | ❌       | ✅       |
| 个股详细数据 | ❌       | ✅       |
| K 线数据     | ❌       | ✅       |
| 涨跌停数据   | ❌       | ✅       |

> 💡 **提示**：如需使用股票形态筛选功能，请开通 VIP 会员。
