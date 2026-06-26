---
name: safe-web-fetch-for-save-token
description: 安全的智能网页抓取技能，节省 50-80% Token。替代内置 web_fetch，自动使用 Jina Reader 清洗服务获取干净 Markdown。内置 URL 白名单验证、SSL 强制验证、敏感数据检测，防止 SSRF 和数据泄露。
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# Safe Web Fetch

安全的智能网页内容获取技能。保留原版的核心功能（Token 节省 50-80%），但增加多层安全防护。

## 核心功能

- **智能清洗**: 自动使用 Jina Reader 获取干净 Markdown
- **Token 优化**: 去除广告、导航栏等噪音，节省 50-80% Token
- **安全防护**: 
  - ✅ 强制 SSL 验证（不跳过）
  - ✅ URL 白名单验证（阻止内网/私有 IP）
  - ✅ 敏感数据检测（不发送包含 API Key/Token 的页面）
  - ✅ 可配置允许列表

## 使用方式

### 基本用法

```bash
# 获取清洗后的 Markdown
python3 {baseDir}/scripts/safe_fetch.py "https://example.com/article"

# JSON 格式输出（包含元信息）
python3 {baseDir}/scripts/safe_fetch.py "https://example.com/article" --json

# 查看安全配置
python3 {baseDir}/scripts/safe_fetch.py --show-config
```

### 在 Agent 中使用

当用户需要获取网页内容时：

```
用户: "帮我查一下 https://example.com/article 的内容"
Agent 应该:
1. 运行: python3 ~/.openclaw/skills/safe-web-fetch/scripts/safe_fetch.py "https://example.com/article"
2. 获得清洗后的 Markdown 内容
```

## 安全特性

### 1. URL 白名单验证

阻止以下危险 URL：
- 私有 IP 地址（127.0.0.1, 192.168.x.x, 10.x.x.x, 172.16-31.x.x）
- localhost, *.local
- 内部域名（*.internal, *.localdomain）
- file://, ftp://, data:// 等非 HTTP 协议

### 2. 敏感数据检测

发送前检测页面内容，拒绝发送包含：
- API Keys（`api_key=`, `apikey=`, `key=`）
- Access Tokens（`access_token=`, `token=`）
- Bearer Tokens（`Bearer `, `Authorization: `）
- AWS Keys（`AKIA`, `aws_`）
- Private Keys（`-----BEGIN.*PRIVATE KEY-----`）

### 3. 强制 SSL 验证

不会禁用 SSL 证书验证，确保：
- 连接真实的服务器
- 防止中间人攻击
- 证书错误时拒绝连接

### 4. 可配置允许列表

在 `config.json` 中配置：

```json
{
  "allowed_domains": ["example.com", "docs.example.com"],
  "blocked_domains": ["ads.example.com"],
  "max_content_size": 10485760,
  "timeout": 30
}
```

## 输出格式

```json
{
  "success": true,
  "url": "https://r.jina.ai/http://example.com/article",
  "original_url": "https://example.com/article",
  "content": "# Article Title\n\nClean markdown content here...",
  "source": "jina",
  "content_length": 1234,
  "error": null
}
```

## 降级策略

1. **Jina Reader**（首选）- 免费，支持好
2. **原始内容**（兜底）- 直连获取，本地清洗

## 与原版区别

| 特性 | 原版 smart-web-fetch | 本技能 safe-web-fetch |
|------|---------------------|----------------------|
| SSL 验证 | ❌ 禁用 | ✅ 强制 |
| URL 白名单 | ❌ 无 | ✅ 有 |
| 敏感数据检测 | ❌ 无 | ✅ 有 |
| SSRF 防护 | ❌ 无 | ✅ 有 |
| 修改 Agent 配置 | ⚠️ 会修改 | ❌ 不修改 |
| Token 节省 | 50-80% | 50-80% |

## 优势

- 🚀 **Token 节省**: 去除广告、导航栏等噪音
- 🔒 **安全第一**: 多层防护，防止数据泄露和 SSRF
- 🆓 **零成本**: 使用免费服务，无需 API Key
- 📝 **干净输出**: 纯 Markdown，无需额外解析
- ⚙️ **可配置**: 允许列表、超时、大小限制均可配置

## 配置文件

创建 `config.json` 进行自定义配置：

```json
{
  "allowed_domains": [],
  "blocked_domains": [],
  "max_content_size": 10485760,
  "timeout": 30,
  "user_agent": "SafeWebFetch/1.0"
}
```

---

**安全提示**: 此技能不会修改 Agent 配置，不会自动接管 web_fetch。如需优先使用本技能，请手动在任务中调用。
