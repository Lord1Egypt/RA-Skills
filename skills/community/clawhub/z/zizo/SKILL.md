---
name: zizo
description: Search images and boards in zizo library. Use when user asks to search for images, photos, pictures, visual assets, or boards/collections.
tools: Bash
credentials:
  - name: ZIZO_TOKEN
    description: API token for zizo
    required: true
environment_variables:
  - name: ZIZO_SERVER
    description: API server URL
    required: false
    default: https://zizo.pro
  - name: ZIZO_LIMIT
    description: Default result limit
    required: false
    default: "20"
  - name: ZIZO_SCOPE
    description: Default search scope
    required: false
    default: public
---

# Zizo Search

Search images and boards in zizo library using zizo.

## Configuration

### 获取 Token

1. 访问 [https://zizo.pro/#/?settings=token](https://zizo.pro/#/?settings=token)
2. 登录或注册 zizo 账号
3. 在页面上找到并复制你的 token
4. 将 token 设置到环境变量中

### 设置方式

**Environment Variables**

```bash
export ZIZO_TOKEN=<your_mcp_token>  # 从上述页面获取的 token
export ZIZO_SERVER=https://zizo.pro  # optional, default: https://zizo.pro
export ZIZO_LIMIT=20                 # optional, default: 20
export ZIZO_SCOPE=public             # optional, default: public
```

**Note**: Configuration is only read from environment variables. No config file is used.

## Prerequisites

Ensure zizo is configured:
- `node dist/index.js version` to verify installation
- `node dist/index.js config show` to verify configuration

## Usage

### Search Images
```bash
node dist/index.js search images "$QUERY" --limit ${LIMIT:-10} --scope ${SCOPE:-public}
```

### Search Boards
```bash
node dist/index.js search boards "$QUERY" --limit ${LIMIT:-10}
```

## Arguments

- `$QUERY`: Search query (required) - supports Chinese and English
- `--limit`: Number of results, default 10
- `--scope`: Search scope for images
  - `public`: Public images only
  - `mine`: User's own images
  - `all`: All accessible images

## Examples

User: "搜索 sunset 相关的图片"
```bash
node dist/index.js search images "sunset" --limit 10
```

User: "Find travel boards"
```bash
node dist/index.js search boards "travel" --limit 10
```

User: "帮我找 5 张风景图"
```bash
node dist/index.js search images "风景" --limit 5
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ZIZO_TOKEN` | API token (required) | - |
| `ZIZO_SERVER` | API server URL | `https://zizo.pro` |
| `ZIZO_LIMIT` | Default result limit | `20` |
| `ZIZO_SCOPE` | Default search scope | `public` |