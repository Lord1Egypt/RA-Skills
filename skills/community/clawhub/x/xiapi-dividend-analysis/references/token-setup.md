# Token 配置指南

## 获取 Token

1. 登录大虾皮网站：[daxiapi.com](https://daxiapi.com)
2. 进入会员中心
3. 点击 API 管理
4. 获取 API Token

## 配置方法

### 方式一：环境变量（推荐）

**Linux/macOS**：
```bash
export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI
```

**Windows**：
```bash
set DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI
```

### 方式二：CLI 配置

```bash
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI
```

### 查看配置

```bash
npx daxiapi-cli@latest config get token
```

## 验证配置

```bash
npx daxiapi-cli@latest dividend score -c 2.H30269
```

如返回正常数据，则配置成功。

## 常见问题

### Token 无效

**错误信息**：401 Unauthorized

**解决方案**：
1. 检查 Token 是否正确
2. 检查 Token 是否过期
3. 重新获取 Token

### Token 未配置

**错误信息**：Token not found

**解决方案**：
1. 确认环境变量已设置
2. 或通过 CLI 配置 Token

### 权限不足

**错误信息**：403 Forbidden

**解决方案**：
1. 检查会员状态
2. 确认 API 功能已开通
