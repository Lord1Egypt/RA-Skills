# Token 配置指南

本文档详细说明如何获取和配置大虾皮 API Token。

## 什么是 Token？

Token 是访问大虾皮 API 的认证凭证，用于验证用户身份和权限。

## 获取 Token

### 步骤 1：注册账号

1. 访问 [daxiapi.com](https://daxiapi.com)
2. 点击"注册"按钮
3. 填写注册信息并完成验证

### 步骤 2：开通 API 功能

1. 登录后进入"个人中心"
2. 找到"API 管理"或"会员中心"
3. 开通 API Token 功能

### 步骤 3：获取 Token

1. 在 API 管理页面
2. 点击"生成 Token"或"获取 Token"
3. 复制生成的 Token（格式通常为长字符串）

**⚠️ 重要提示**：
- Token 只显示一次，请妥善保存
- 不要将 Token 分享给他人
- Token 泄露可能导致账号风险

## 配置 Token

### 方式一：环境变量（推荐）

**优点**：临时有效，安全性较高

**Linux/macOS**：

```bash
# 临时设置（当前终端会话有效）
export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI' >> ~/.bashrc
source ~/.bashrc
```

**Windows**：

```cmd
# 临时设置（当前命令行会话有效）
set DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI

# 永久设置（系统环境变量）
setx DAXIAPI_TOKEN "YOUR_TOKEN_FROM_DAXIAPI"
```

### 方式二：CLI 配置

**优点**：持久保存，无需每次设置

```bash
# 设置 Token
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI

# 验证配置
npx daxiapi-cli@latest config get token
```

**配置文件位置**：

- Linux/macOS: `~/.daxiapirc`
- Windows: `%USERPROFILE%\.daxiapirc`

## 验证配置

### 快速测试

```bash
npx daxiapi-cli@latest market style
```

**成功表现**：返回正常数据，无错误信息

**失败表现**：
- `401 Unauthorized`
- `Authentication failed`
- `Invalid token`

## 常见问题

### Q: Token 配置后仍然报 401 错误？

A: 可能原因：
1. Token 已过期：重新生成 Token
2. Token 格式错误：检查是否完整复制
3. 配置未生效：重启终端或重新登录

### Q: 如何更新 Token？

A: 重新执行配置命令即可覆盖旧 Token：

```bash
npx daxiapi-cli@latest config set token NEW_TOKEN
```

### Q: Token 会过期吗？

A: Token 有效期取决于会员类型：
- 普通会员：通常 30 天
- 高级会员：通常 90 天
- 永久会员：长期有效

### Q: 如何保护 Token 安全？

A: 建议：
1. 不要将 Token 提交到代码仓库
2. 不要在公共场合分享 Token
3. 定期更换 Token
4. 使用环境变量而非配置文件（可选）

## 删除 Token

如需删除 Token 配置：

```bash
# 删除配置文件中的 Token
npx daxiapi-cli@latest config delete token

# 或手动删除配置文件
rm ~/.daxiapirc  # Linux/macOS
del %USERPROFILE%\.daxiapirc  # Windows
```

## 多环境配置

如需在不同环境使用不同 Token：

```bash
# 开发环境
export DAXIAPI_TOKEN=DEV_TOKEN

# 生产环境
export DAXIAPI_TOKEN=PROD_TOKEN
```

环境变量优先级高于配置文件。
