# Virsical OAuth2 认证流程

## 概述

Virsical 使用 OAuth2 Authorization Code Grant 进行用户认证。认证完成后，所有 API 请求需携带 Bearer Token 和请求签名。

## 认证架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   客户端     │     │  Virsical    │     │  Virsical   │
│ (WorkBuddy) │     │  Auth Server │     │  API Server │
└──────┬──────┘     └──────┬───────┘     └──────┬──────┘
       │                   │                     │
       │ 1. GET /authorize │                     │
       │──────────────────>│                     │
       │                   │                     │
       │ 2. 浏览器授权页面  │                     │
       │<──────────────────│                     │
       │                   │                     │
       │ 3. 用户授权后回调   │                     │
       │   (code + state)  │                     │
       │<──────────────────│                     │
       │                   │                     │
       │ 4. POST /token    │                     │
       │   (exchange code) │                     │
       │──────────────────>│                     │
       │                   │                     │
       │ 5. access_token   │                     │
       │   + refresh_token │                     │
       │<──────────────────│                     │
       │                   │                     │
       │ 6. API 请求        │                     │
       │ (Bearer + 签名)    │                     │
       │─────────────────────────────────────────>│
       │                   │                     │
       │ 7. API 响应        │                     │
       │<─────────────────────────────────────────│
       │                   │                     │
```

## 凭证配置

OAuth 凭证已使用固定值，无需用户配置。Base URL 默认值通过 `scripts/config.py` 获取，见 SKILL.md 概述。

| 变量 | 说明 | 默认值 |
|------|------|--------|
| VIRSICAL_BASE_URL | API 基础地址 | 通过 config 获取 |

## 登录模式

### 1. Agent 授权码登录（推荐）

适用于 WorkBuddy Skill 对话场景，避免本地回调地址未注册、浏览器回调不可达等问题。

**流程**:
1. Skill 检测到本地未登录或 token 已失效
2. Skill 提示用户按以下步骤获取授权码：打开浏览器访问威思客系统，登录后点击右上角用户信息，找到「Agent授权码」并复制
3. 用户将授权码粘贴到对话中
4. Skill 将授权码作为 `authCode` 调用 `POST {agent_auth_base_url}/vsk/virsical-auth/agent/getAgentToken`
5. 服务返回 `access_token`、`refresh_token`、`expires_in`、`username` 等数据
6. Skill 保存 token，并友好提示登录成功

**接口配置**:

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `VIRSICAL_AGENT_AUTH_BASE_URL` | Agent 认证服务地址 | 同 Base URL（通过 config 获取） |

**已知错误码**:

| 错误码 | 说明 |
|--------|------|
| `101100` | Agent 授权码不存在或已过期，需要重新获取授权码 |

### 2. 本地登录（桌面环境，备用）

适用于 Web Chat / 桌面应用等可以自动打开浏览器的场景。

**流程**:
1. 生成 32 字节随机 state（hex 格式）用于 CSRF 防护
2. 构建授权 URL：`{baseUrl}/vsk/virsical-auth/oauth2/authorize?response_type=code&client_id=login-agent&redirect_uri=http://127.0.0.1:1455/callback&state={state}`
3. 启动本地 HTTP 服务器监听 `127.0.0.1:1455`
4. 使用系统默认浏览器打开授权 URL
5. 用户在浏览器中授权
6. Virsical 回调 `http://127.0.0.1:1455/callback?code={code}&state={state}`
7. 验证 state 参数
8. 使用 code 换取 token
9. 保存 token 到本地文件
10. 返回成功/失败 HTML 页面给浏览器

**超时**: 10 分钟

### 3. 远程登录（飞书/Teams 等，备用）

适用于无法自动打开浏览器的场景。

**流程**:
1. 生成 32 字节随机 state
2. 将 state 持久化到 `oauth-state.json`（10 分钟有效期）
3. 返回授权 URL 给用户
4. 用户在外部浏览器中打开 URL 并授权
5. Virsical 回调到 `http://127.0.0.1:1455/callback`（如果本地不可达则失败）
6. 用户手动复制浏览器地址栏中的 `code` 和 `state` 参数
7. 调用 exchange 接口，验证 state 并换取 token
8. state 仅使用一次（防重放攻击）

## Token 管理

### Token 存储

Token 存储在本地 JSON 文件中：

```json
{
  "virsical:default": {
    "access": "access_token_value",
    "refresh": "refresh_token_value",
    "expires": 1717000000,
    "username": "user_id",
    "userId": "xxx",
    "tenantId": "xxx",
    "loginTime": "2026-06-02T09:00:00+08:00"
  }
}
```

### Token 刷新策略

- **主动刷新**: 距离过期时间不足 10 分钟时，在 API 请求前自动刷新
- **被动刷新**: API 返回 401 时，刷新 token 并重试一次
- **刷新失败处理**: 
  - 主动刷新失败：仍返回现有 token，记录失败日志
  - 被动刷新失败：清除本地 token，要求重新登录

### Token 检查

可以使用 `POST /vsk/virsical-auth/oauth/check_token` 接口验证 token 有效性。此接口使用 Basic Auth（clientId:clientSecret）认证。

### 登出

调用 `POST /vsk/virsical-auth/token/logout` 接口，传入 access_token 使服务端 token 失效，同时清除本地存储的 token。

## CSRF 防护

- 使用 `crypto.randomBytes(32)` 生成随机 state
- State 存储在本地 JSON 文件中
- State 有效期为 10 分钟
- State 只能使用一次（使用后立即删除）
- 回调时验证 state 是否匹配

## 安全注意事项

1. Client Secret 不应提交到代码仓库
2. Token 文件应设置适当权限（0600）
3. 本地回调服务器仅监听 127.0.0.1（不接受外部连接）
4. State 参数严格验证，防止 CSRF 攻击
5. Refresh token 也有过期时间，需要处理刷新失败的情况
