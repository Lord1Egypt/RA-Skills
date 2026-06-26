---
name: r2-uploader
description: 使用 wrangler CLI 上传文件到 Cloudflare R2 对象存储，返回公开访问 URL。支持单文件上传、从远程 URL 直接上传、批量上传。当用户说"上传到 R2"、"传到 Cloudflare"、"存到 R2"、"上传图片/文件/附件"并提到 R2 或 wrangler 时使用。触发词：上传、R2、Cloudflare、存储、wrangler、bucket、对象存储、CDN 上传。
---

# R2 文件上传

使用 wrangler CLI 上传文件到 Cloudflare R2 对象存储。

## 环境变量

| 变量 | 说明 |
|------|------|
| `$R2_BUCKET` | R2 存储桶名称（也可由用户指定） |
| `$R2_DOMAIN` | 自定义域名（可选，未设置则用默认 URL） |

## 核心流程

### 1. 定位文件

```bash
# 用户提供文件名时，查找文件
find ~ -name "<filename>" -type f 2>/dev/null | head -5

# 验证文件存在
ls -la "<file-path>"
```

### 2. 生成路径

```bash
R2_PATH="agent/$(date +%Y%m%d)/$(basename "<file>")"
```

### 3. 执行上传

```bash
wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "<file-path>" --remote
```

### 4. 返回 URL

```bash
# 有自定义域名
echo "https://$R2_DOMAIN/$R2_PATH"

# 无自定义域名（默认）
echo "https://pub-<account-id>.r2.dev/$R2_PATH"
```

## 从 URL 直接上传

```bash
curl -sL "<url>" | wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file - --remote
```

## 常用管理命令

```bash
# 列出 buckets
wrangler r2 bucket list

# 删除对象
wrangler r2 object delete "<bucket>/<path>/<file>" --remote
```

## 高级功能与错误处理

- **批量上传、并发上传**: 见 [references/advanced.md](references/advanced.md)
- **错误处理、重试机制、特殊路径**: 见 [references/error-handling.md](references/error-handling.md)
