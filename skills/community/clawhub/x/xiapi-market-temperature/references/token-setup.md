# Token 配置指南

本文档详细介绍如何获取和配置大虾皮 API Token。

## Token 获取

### 步骤1：访问大虾皮网站

访问 [daxiapi.com](https://daxiapi.com) 并登录账号。

### 步骤2：进入会员中心

登录后，进入个人中心或会员中心页面。

### 步骤3：开通 API Token 功能

1. 找到 "API 管理" 或 "Token 管理" 入口
2. 点击 "开通 API Token" 或类似按钮
3. 系统会生成一个唯一的 Token 字符串

### 步骤4：保存 Token

**重要**：Token 只显示一次，请务必保存好。建议复制到安全的地方存储。

## Token 配置

提供两种配置方式，推荐使用方式一（CLI 配置）。

### 方式一：CLI 配置（推荐）

使用 CLI 命令配置 Token，配置后持久化存储在本地。

```bash
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI
```

**优点**：

- 配置后永久有效，无需每次设置
- 自动存储在本地配置文件中
- 跨终端会话保持

**验证配置**：

```bash
npx daxiapi-cli@latest config get token
```

如返回你配置的 Token，则配置成功。

### 方式二：环境变量配置

通过设置环境变量配置 Token，适合临时使用或 CI/CD 环境。

**Linux/macOS**：

```bash
# 临时设置（当前终端会话有效）
export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI

# 永久设置（添加到 shell 配置文件）
echo 'export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI' >> ~/.zshrc
source ~/.zshrc
```

**Windows**：

```cmd
# 临时设置（当前终端会话有效）
set DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI

# 永久设置（用户环境变量）
setx DAXIAPI_TOKEN "YOUR_TOKEN_FROM_DAXIAPI"
```

**优点**：

- 不存储在本地文件，相对安全
- 适合临时使用或自动化脚本

**缺点**：

- 每次新终端会话需要重新设置（除非添加到配置文件）
- 不如 CLI 配置方便

## 验证配置

配置完成后，建议执行以下命令验证：

```bash
npx daxiapi-cli@latest market temp
```

**成功标志**：

- 返回 JSON 格式的市场温度数据
- 无认证错误提示

**失败标志**：

- 返回 `401 Unauthorized` 错误
- 提示 "未配置 API Token"

## Token 安全建议

1. **不要分享 Token**：Token 是个人专属，不要分享给他人
2. **不要提交到代码仓库**：避免将 Token 提交到 Git 仓库
3. **定期更换**：建议定期在大虾皮网站重新生成 Token
4. **使用环境变量**：在公共或共享环境中，优先使用环境变量方式

## 常见问题

### Q1: Token 在哪里查看？

**A**: Token 只在生成时显示一次。如果忘记了 Token，需要在大虾皮网站重新生成。

### Q2: Token 有效期是多久？

**A**: 具体有效期请参考大虾皮网站的说明。一般情况下，Token 长期有效，但建议定期更换。

### Q3: 如何更换 Token？

**A**:

1. 在大虾皮网站重新生成 Token
2. 使用 CLI 命令更新：`npx daxiapi-cli@latest config set token NEW_TOKEN`

### Q4: 配置后仍然报 401 错误？

**A**: 可能原因：

1. Token 已过期或被禁用 → 重新生成 Token
2. Token 格式错误 → 检查是否完整复制，没有多余空格
3. 使用环境变量但未生效 → 检查环境变量是否正确设置

### Q5: 多个终端如何共享配置？

**A**: CLI 配置存储在本地文件，同一台机器的多个终端会共享配置。如果在不同机器上使用，需要分别配置。

## 故障排除

### 问题1：命令找不到

```
command not found: npx
```

**解决方案**：确保已安装 Node.js 和 npm。

### 问题2：权限错误

```
Permission denied
```

**解决方案**：

- 检查是否有写入配置文件的权限
- 尝试使用管理员权限运行

### 问题3：网络错误

```
Network Error / ECONNREFUSED
```

**解决方案**：

- 检查网络连接
- 检查是否需要代理
- 确认能访问 daxiapi.com

## 相关文档

- [CLI 命令参考](cli-commands.md)
- [字段说明](field-descriptions.md)
