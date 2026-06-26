# WHOOP API 申请指南 (修正版)

## OAuth 2.0 流程

### 1. 生成 state 参数

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(16))"
# 例如输出: m5cC5aC6l_SUT-ytWUlhig
```

### 2. 浏览器打开授权 URL

把 `YOUR_CLIENT_ID` 和 `YOUR_STATE` 替换后访问：

```
https://api.prod.whoop.com/oauth/oauth2/auth?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https://localhost:3000/callback&state=YOUR_STATE
```

### 3. 获取授权码

授权后跳转到：
```
https://localhost:3000/callback?code=xxxxx&state=YOUR_STATE
```

记录 `code=` 后面的值

### 4. 用 code 换 token

```bash
curl -X POST https://api.prod.whoop.com/oauth/oauth2/token \
  -d "grant_type=authorization_code" \
  -d "code=刚才获得的code" \
  -d "client_id=你的CLIENT_ID" \
  -d "client_secret=你的CLIENT_SECRET" \
  -d "redirect_uri=https://localhost:3000/callback"
```

### 5. 响应会包含

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_in": 3600
}
```

记录 `refresh_token` 的值

### 6. 配置凭证

创建 `~/.clawdbot/whoop-credentials.env`:

```bash
WHOOP_CLIENT_ID="your_client_id"
WHOOP_CLIENT_SECRET="your_client_secret"
WHOOP_REFRESH_TOKEN="your_refresh_token"
```

---

## 参考

- 开发者平台: https://developer.whoop.com
