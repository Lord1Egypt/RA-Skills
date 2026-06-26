# Token 配置指南

本文档详细介绍如何获取和配置大虾皮 API Token。

## 获取 Token

### 步骤 1：注册账号

访问 [daxiapi.com](https://daxiapi.com)，注册并登录账号。

### 步骤 2：开通 API 功能

1. 进入个人主页
2. 找到"API Token"设置
3. 开通 API 访问功能

### 步骤 3：生成 Token

1. 点击"生成新 Token"
2. 复制生成的 Token（只显示一次，请妥善保管）
3. 建议保存到安全的地方

---

## 配置 Token

### 方式一：CLI 配置（推荐）

```bash
# 设置 Token
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI

# 验证配置
npx daxiapi-cli@latest config get token

# 测试调用
npx daxiapi-cli@latest market
```

**优点**：
- 持久化保存
- 自动添加到请求头
- 无需每次设置环境变量

---

### 方式二：环境变量

```bash
# 临时设置（当前终端会话）
export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI

# 永久设置（添加到 ~/.zshrc 或 ~/.bashrc）
echo 'export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI' >> ~/.zshrc
source ~/.zshrc
```

**优点**：
- 不依赖 CLI 配置文件
- 适合 CI/CD 环境

---

## 验证 Token

### 检查配置状态

```bash
npx daxiapi-cli@latest config get token
```

### 测试 API 调用

```bash
npx daxiapi-cli@latest market
```

如果返回正常数据，说明 Token 配置成功。

---

## Token 安全

### 安全建议

1. **不要分享 Token**：Token 相当于密码，不要告诉他人
2. **不要提交到 Git**：将 `.env` 添加到 `.gitignore`
3. **定期更换 Token**：建议定期重新生成
4. **使用环境变量**：在脚本中使用环境变量而非硬编码

### 如果 Token 泄露

1. 立即登录 daxiapi.com
2. 在个人主页撤销旧 Token
3. 生成新 Token
4. 更新本地配置

---

## 常见问题

### Q: Token 会过期吗？

A: Token 通常不会过期，但建议定期更换以确保安全。

### Q: 忘记 Token 怎么办？

A: 登录 daxiapi.com 个人主页，重新生成新 Token。

### Q: 401 错误如何处理？

A: 检查 Token 是否正确配置，是否被撤销。

### Q: 多台电脑如何使用？

A: 可以在多台电脑上使用同一个 Token，或为每台电脑生成独立 Token。

---

## 配置文件位置

CLI 配置文件存储在：

```
~/.daxiapi/config.json
```

可以手动编辑此文件：

```json
{
  "token": "YOUR_TOKEN_HERE"
}
```

---

## 环境变量优先级

Token 加载优先级（从高到低）：

1. 命令行参数：`--token`
2. 环境变量：`DAXIAPI_TOKEN`
3. 配置文件：`~/.daxiapi/config.json`

---

## 推荐配置流程

```bash
# 1. 获取 Token（从 daxiapi.com）

# 2. 配置 Token
npx daxiapi-cli@latest config set token YOUR_TOKEN

# 3. 验证配置
npx daxiapi-cli@latest config get token

# 4. 测试调用
npx daxiapi-cli@latest market

# 5. 如果返回正常数据，配置成功
```

---

## 故障排查

### Token 显示为空

```bash
# 检查配置
npx daxiapi-cli@latest config get token

# 如果为空，重新设置
npx daxiapi-cli@latest config set token YOUR_TOKEN
```

### Token 已配置但仍报 401

```bash
# 可能是 Token 被撤销，重新生成
# 登录 daxiapi.com 生成新 Token
# 更新本地配置
npx daxiapi-cli@latest config set token NEW_TOKEN
```

### 环境变量不生效

```bash
# 检查环境变量
echo $DAXIAPI_TOKEN

# 如果为空，重新设置
export DAXIAPI_TOKEN=YOUR_TOKEN

# 或添加到 shell 配置文件
echo 'export DAXIAPI_TOKEN=YOUR_TOKEN' >> ~/.zshrc
source ~/.zshrc
```
