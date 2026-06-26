---
name: serverless-template-generator
description: 生成 Serverless 脚手架，支持 AWS Lambda, Vercel, Netlify, Cloudflare Workers，一键部署到云端。
metadata: {"clawdbot":{"emoji":"☁️","requires":{},"primaryEnv":""}}
---

# Serverless Template Generator

快速生成 Serverless 函数脚手架，支持主流 Serverless 平台。

## 功能

- ⚡ 一键生成项目结构
- 🌐 多平台支持
- 📝 完整的配置文件
- 🧪 测试模板
- 🚀 部署脚本
- 📖 文档

## 支持的平台

| 平台 | 说明 | 特点 |
|------|------|------|
| Vercel | 免费的 Serverless | 简单、集成好 |
| Netlify | 静态网站托管 | 函数支持 |
| AWS Lambda | AWS 无服务器 | 功能最全 |
| Cloudflare Workers | 边缘计算 | 全球分布 |
| Supabase Edge | 开源替代 | 自托管 |

## 使用方法

### 基本用法

```bash
# 生成 Vercel 函数
serverless-template my-function --platform vercel

# 生成 Netlify 函数
serverless-template api-handler --platform netlify

# 生成 Cloudflare Worker
serverless-template worker --platform cloudflare
```

### 选项

| 选项 | 说明 |
|------|------|
| `--platform, -p` | 平台 (vercel/netlify/aws//cloudflare) |
| `--language, -l` | 语言 (js/ts/python) |
| `--output, -o` | 输出目录 |

## 生成的项目结构

### Vercel

```
my-function/
├── api/
│   └── my-function.js    # API handler
├── package.json
├── vercel.json
└── README.md
```

### Cloudflare Worker

```
my-worker/
├── src/
│   └── index.js           # Worker 入口
├── wrangler.toml          # Cloudflare 配置
└── package.json
```

## 代码示例

### Vercel API

```javascript
export default async function handler(req, res) {
  const { searchParams } = new URL(req.url);
  const name = searchParams.get('name') || 'World';
  
  return res.json({
    message: `Hello, ${name}!`,
    timestamp: new Date().toISOString()
  });
}
```

### Cloudflare Worker

```javascript
export default {
  async fetch(request, env, ctx) {
    return new Response('Hello, World!', {
      headers: { 'content-type': 'text/plain' }
    });
  }
};
```

## 部署命令

### Vercel

```bash
vercel deploy
```

### Netlify

```bash
netlify deploy --prod
```

### Cloudflare

```bash
wrangler publish
```

## 本地测试

```bash
# Vercel
vercel dev

# Netlify
netlify dev

# Cloudflare
wrangler dev
```

## 变现思路

1. **模板销售** - 专业 Serverless 模板
2. **咨询业务** - Serverless 架构咨询
3. **培训课程** - Serverless 开发教程
4. **代部署服务** - 帮企业部署到云端

## 安装

```bash
# 无需额外依赖
```
