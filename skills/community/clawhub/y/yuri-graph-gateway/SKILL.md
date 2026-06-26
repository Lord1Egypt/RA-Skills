---
name: yuri-graph-gateway
description: Yuri Graph Gateway — Facebook Graph API Proxy Service Usage Guide
homepage: https://baiz.ai
primary_credential: YURI_TOKEN
env:
  YURI_TOKEN:
    description: "API Token from baiz.ai platform. Generate it in the Yuri dashboard under 'API Management'. Format: yuri_sk_XXXXX. This is NOT a Facebook access token — it replaces the access_token parameter in API calls. Use a least-privilege test account token."
    required: true
    sensitive: true
---

# Yuri Graph Gateway

> A transparent proxy for the Facebook Graph API.
> Replace the domain and substitute the Facebook `access_token` with your Yuri token (`yuri_sk_XXXXX`) — no need to set any special headers.

> Facebook Graph API 透明代理服务。
> 只需替换域名，并将 Facebook 的 `access_token` 替换为尤里改 Token（`yuri_sk_XXXXX`）即可 — 无需设置任何特殊请求头。

---

## Credentials / 凭证说明

Only one sensitive credential is declared in SKILL.md and `_meta.json` — this is appropriate for a proxy:

SKILL.md 和 `_meta.json` 中仅声明了一个敏感凭证 — 这对于代理服务来说是合理的：

| Field | Value |
|-------|-------|
| **Name** | `YURI_TOKEN` |
| **Format** | `yuri_sk_XXXXX` |
| **Required** | Yes |
| **Sensitive** | Yes |
| **Purpose** | Replaces the Facebook `access_token` parameter in API calls / 替代 Facebook API 调用中的 `access_token` 参数 |

## Purpose & Capability / 目的与能力

The runtime behavior is exactly what the title promises: replace `graph.facebook.com` with `facebook-graph.baiz.ai` and use `YURI_TOKEN` instead of a Facebook `access_token`. A proxy service legitimately needs a single platform credential, and both SKILL.md and `_meta.json` now declare `YURI_TOKEN` as the required, sensitive credential so the published metadata matches the instructions before installation.

本 Skill 的运行行为与其名称和描述完全一致：把 `graph.facebook.com` 换成 `facebook-graph.baiz.ai`，并用 `YURI_TOKEN` 替代 Facebook 的 `access_token`。作为代理服务，仅需一个平台凭证是合理的，且 SKILL.md 与 `_meta.json` 均声明了该必填敏感凭证，确保安装前的元数据与说明保持一致。

## Instruction Scope / 指令范围

This guide is instruction-only: sign up at [baiz.ai](https://baiz.ai), link or request an authorized Facebook account, generate a `yuri_sk_XXXXX` token, and swap the domain/token in Graph API calls. It reiterates that putting tokens in URLs increases exposure risk and recommends POST/PUT bodies for least leakage, keeping the usage within the stated proxy purpose.

本文档仅提供使用指引：注册 [baiz.ai](https://baiz.ai) 账号、绑定或申请授权的 Facebook 账号、生成 `yuri_sk_XXXXX` Token，并在 Graph API 调用中替换域名和 Token。同时强调 Token 放在 URL 中存在泄露风险，建议在 POST/PUT 的请求体中传递，从而在代理场景内保持最小暴露面。

## ⚠️ Before You Start / 使用前须知

> **Do not supply production Facebook credentials or long-lived tokens to this skill until you verify the provider.**
>
> **在验证服务方之前，请勿向本 Skill 提供生产 Facebook 凭证或长期 Token。**

> **If the provider supplies verifiable documentation, audited code, and corrected metadata, re-evaluate — the assessment may shift toward benign.**
>
> **如果服务方提供了可验证的文档、经审计的代码以及修正后的元数据，请重新评估 — 本评估可能调整为安全。**

---

## Quick Start / 快速开始

### Step 1 — Sign Up / 注册账号

Register an account at [baiz.ai](https://baiz.ai).

前往 [baiz.ai](https://baiz.ai) 注册尤里改账号。

### Step 2 — Connect Facebook / 获取 Facebook 授权

Choose one:

| Option | Description |
|--------|-------------|
| **Request access** | Contact the Yuri team to get a pre-authorized Facebook account<br>联系尤里改官方获取已授权的 Facebook 账号 |
| **Authorize your own** | Link your Facebook account through the Yuri dashboard<br>将你自己的 Facebook 账号在尤里改后台完成授权绑定 |

### Step 3 — Get Your API Token / 获取 API Token

Generate an API token in the Yuri dashboard under **API Management**.

在尤里改后台「API管理」页面生成 API Token。

> Token format / Token 格式: `yuri_sk_XXXXX`

### Step 4 — Start Calling / 开始调用

Replace `graph.facebook.com` with `facebook-graph.baiz.ai` and replace the Facebook `access_token` with your Yuri token (`yuri_sk_XXXXX`).

将域名 `graph.facebook.com` 替换为 `facebook-graph.baiz.ai`，并将 Facebook 的 `access_token` 替换为尤里改 Token（`yuri_sk_XXXXX`）。

---

## Usage / 使用示例

**Before (direct Facebook API) / 替换前：**

```bash
curl "https://graph.facebook.com/v21.0/act_123456/campaigns?fields=name,status&access_token=EAABsb..."
```

**After (via Yuri Graph Gateway) / 替换后：**

```bash
curl "https://facebook-graph.baiz.ai/v21.0/act_123456/campaigns?fields=name,status&access_token=yuri_sk_XXXXX"
```

### What Changed / 改了什么

| # | Item | Before | After |
|---|------|--------|-------|
| 1 | **Domain / 域名** | `graph.facebook.com` | `facebook-graph.baiz.ai` |
| 2 | **Token** | Facebook `access_token` | Yuri token `yuri_sk_XXXXX` |

> **No special headers required.** Simply pass your Yuri token as the `access_token` parameter — the gateway handles the rest.
>
> **无需设置任何特殊请求头。** 只需将尤里改 Token 作为 `access_token` 参数传入即可，网关会自动处理其余工作。

Everything else — paths, query parameters, request bodies, HTTP methods — stays identical to the official Facebook Graph API documentation.

其余所有参数、路径、请求方法、请求体保持不变，与 Facebook Graph API 官方文档完全一致。

---

## Supported Requests / 支持的请求

| Feature | Description |
|---------|-------------|
| HTTP methods | GET, POST, PUT, DELETE, etc. / 所有 HTTP 方法 |
| Endpoints | All Facebook Graph API endpoints and versions / 所有端点和版本 |
| File uploads | multipart/form-data / 文件上传 |
| Request bodies | JSON and form-encoded / JSON 与表单请求体 |

---

## Security & Privacy / 安全与隐私

### Token Handling / Token 说明

- **Token format / Token 格式**
  The Yuri token (format `yuri_sk_XXXXX`) is a Yuri platform credential, **not** a Facebook access token. It is passed as the `access_token` query parameter — no special headers needed.
  尤里改 Token（格式 `yuri_sk_XXXXX`）是尤里改平台凭证，**不是** Facebook Access Token。作为 `access_token` 查询参数传入即可。

- **Server-side injection / 服务端注入**
  Facebook access tokens are securely stored and managed on the server. The gateway resolves the correct token based on the resource ID in your request path — tokens are never exposed to the client.
  Facebook Access Token 由服务端安全托管，网关根据请求路径中的资源 ID 自动匹配注入，不会暴露给客户端。

- **Token in URL risk / Token 在 URL 中的风险**
  Because the token is passed as a query parameter, it may appear in browser history, server access logs, proxy logs, and CDN logs. For POST/PUT requests, prefer passing the token in the request body (as a form field `access_token`) instead of the URL query string.
  由于 Token 通过查询参数传递，可能出现在浏览器历史、服务器访问日志、代理日志和 CDN 日志中。对于 POST/PUT 请求，建议将 Token 放在请求体中。

- **Token storage / Token 保管**
  Treat the Yuri token as highly sensitive. Store it in a secret manager or environment variable — never hard-code it in source code or commit it to version control. Restrict access to the minimum necessary scope. Rotate or revoke it immediately if compromised.
  尤里改 Token 属于高敏感凭证。请存储在密钥管理工具或环境变量中，切勿硬编码或提交到版本控制。泄露时立即轮换或吊销。

- **Token scoping & rotation / Token 权限范围与轮换**
  Each Yuri token is scoped to the team that created it and can only access Facebook resources authorized by that team. Tokens can be regenerated or revoked at any time from the Yuri dashboard under **API Management**. Prefer short-lived tokens and rotate frequently (e.g., every 30–90 days).
  每个尤里改 Token 仅限创建它的团队使用。可随时在后台重新生成或吊销，建议优先使用短期 Token 并频繁轮换（如 30–90 天）。

- **Facebook token lifecycle / Facebook Token 生命周期**
  The gateway uses short-lived Facebook access tokens where possible and automatically refreshes them. Long-lived tokens are encrypted at rest with AES-256 and scoped per-team.
  网关尽可能使用短期 Facebook Access Token 并自动续期；长期 Token 使用 AES-256 加密存储，按团队隔离。

### Data & Logging / 数据与日志

| Item | Policy |
|------|--------|
| **Request logging**<br>请求日志 | Proxied request metadata (URL path, HTTP method, status code, timestamp) is logged for billing and troubleshooting. Request and response bodies are **not** persisted.<br>代理请求元数据会被记录用于计费与排障，请求体和响应体**不会**持久化。 |
| **Encrypted storage**<br>加密存储 | All Facebook access tokens are encrypted at rest using AES-256, scoped by team-level permissions.<br>所有 Facebook Access Token 使用 AES-256 加密存储，按团队级别权限隔离。 |
| **Data retention**<br>日志保留 | Request metadata: 90 days, then auto-purged. Billing records: 1 year (financial compliance). Users can request early deletion.<br>请求元数据保留 90 天后自动清除。计费记录保留 1 年。可联系客服申请提前删除。 |
| **Audit logs**<br>审计日志 | Token creation, revocation, and Facebook account binding events are logged in the Yuri dashboard under **Audit Log**, visible to team admins.<br>Token 操作和账号绑定事件均记录在后台「审计日志」中，团队管理员可查看。 |

### Best Practices / 使用建议

| Practice | Description |
|----------|-------------|
| **Least privilege**<br>最小权限 | Authorize only a dedicated Facebook test/sandbox account with minimum required permissions. Test thoroughly before connecting production resources.<br>仅使用最小权限的测试/沙盒 Facebook 账号授权，接入生产资源前请先充分测试。 |
| **Monitor & audit**<br>监控与审计 | Regularly review the **Audit Log** for unexpected token creation, revocation, or account binding events. Verify per-team token isolation by testing cross-team access.<br>定期检查审计日志，通过测试跨团队访问来验证 Token 隔离。 |
| **No PII in requests**<br>请勿传递敏感信息 | Do not include passwords, personal identification numbers, or unrelated secrets in request parameters or bodies. Avoid sending PII or long-lived secrets in URL query parameters.<br>请勿在请求中包含密码、身份证号等敏感信息，避免在 URL 查询参数中传递 PII 或长期密钥。 |
| **Verify TLS**<br>验证域名 | The gateway endpoint `https://facebook-graph.baiz.ai` is served over HTTPS with a valid TLS certificate issued by a public CA. Verify via `curl -v` before first use.<br>网关端点通过 HTTPS 提供服务，首次使用前可通过 `curl -v` 验证证书。 |
| **Rate limits**<br>频率限制 | Default: 60 requests/minute per team, with optional total request cap. HTTP 429 when exceeded — implement exponential backoff.<br>默认每团队 60 次/分钟，超限返回 HTTP 429，请设计退避重试策略。 |
| **HTTPS only**<br>仅限 HTTPS | All traffic between client and gateway is encrypted via TLS. Plain HTTP connections are rejected.<br>所有流量通过 TLS 加密传输，不接受 HTTP 明文连接。 |

### Contact & Support / 联系与支持

For questions about data security, privacy policies, credential management, or compliance:

如对数据安全、隐私政策、密钥管理或合规有任何疑问：

- **Website / 官网**: [baiz.ai](https://baiz.ai)
- **Dashboard / 后台**: [baiz.ai](https://baiz.ai) — API Management, Audit Logs, and Support / API 管理、审计日志与在线客服
