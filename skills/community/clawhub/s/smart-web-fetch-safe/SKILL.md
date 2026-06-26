---
name: smart-web-fetch-safe
description: 安全版智能网页内容获取技能。本地解析 + 可选远程清洗，隐私优先，Token 优化。
metadata: { "openclaw": { "emoji": "🔐", "requires": { "bins": ["python3"], "env":[] } } }
---

# Smart Web Fetch Safe

安全版智能网页内容获取技能，隐私优先，支持本地解析和远程清洗两种模式。

## 核心功能

- **本地解析默认**: 使用本地 HTML 解析，隐私安全
- **可选远程清洗**: 用户可选择使用 Jina Reader 远程服务
- **Token 优化**: 自动去除广告、导航栏等噪音内容
- **域名白名单**: 可配置允许访问的域名列表
- **字符数限制**: 内置最大字符数限制，避免超长输出

## 安全特性

⚠️ **隐私提示**: 
- 本地解析模式：数据完全保留在本地，隐私安全
- 远程清洗模式：URL 和内容会经过 Jina AI 服务处理

## 使用方式

### 命令行

```bash
# 本地解析模式（默认，隐私安全）
python3 skills/smart-web-fetch-safe/scripts/fetch.py "https://example.com/article"

# 远程清洗模式（更节省 Token，但数据经过第三方）
python3 skills/smart-web-fetch-safe/scripts/fetch.py "https://example.com/article" --remote

# 指定最大字符数
python3 skills/smart-web-fetch-safe/scripts/fetch.py "https://example.com/article" --max-chars 5000

# 组合使用
python3 skills/smart-web-fetch-safe/scripts/fetch.py "https://example.com/article" --remote --max-chars 3000
```

### JSON 输出

```bash
python3 skills/smart-web-fetch-safe/scripts/fetch.py "https://example.com/article" --json
```

## 配置说明

### 环境变量（可选）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| ALLOWED_DOMAINS | * | 允许访问的域名，用逗号分隔 |
| MAX_CHARS | 10000 | 最大返回字符数 |
| DEFAULT_MODE | local | 默认模式：local（本地）或 remote（远程） |

### 白名单示例

```bash
export ALLOWED_DOMAINS="example.com,github.com,wikipedia.org"
export MAX_CHARS=5000
export DEFAULT_MODE=local
```

## 模式对比

| 特性 | 本地解析 (local) | 远程清洗 (remote) |
|------|------------------|-------------------|
| 隐私 | ✅ 完全本地 | ⚠️ 数据经第三方 |
| Token 优化 | ✅ 基础优化 | ✅ 深度优化 50-80% |
| 速度 | 较快 | 依赖网络 |
| 依赖 | beautifulsoup4, requests | 无额外依赖 |

## 安装依赖

```bash
pip install beautifulsoup4 requests
```

## 当前状态

开发中。
