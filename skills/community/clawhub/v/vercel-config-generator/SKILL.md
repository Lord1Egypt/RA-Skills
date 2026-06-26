---
name: vercel-config-generator
description: 生成专业的 Vercel 配置文件 vercel.json，支持 Serverless Functions、Edge Functions、静态网站、SSR 等多种部署模式。
metadata: {"clawdbot":{"emoji":"▲","requires":{},"primaryEnv":""}}
---

# Vercel Config Generator

生成专业的 Vercel 配置文件。

## 功能

- ⚡ 一键生成配置
- 🌐 多部署模式支持
- ⚙️ Serverless 配置
- 📦 边缘计算支持

## 部署模式

| 模式 | 说明 |
|------|------|
| static | 静态网站 |
| serverless | Serverless Functions |
| edge | Edge Functions |
| swa | Single Page App |

## 使用方法

### 静态网站

```bash
vercel-config-generator --type static
```

### Serverless

```bash
vercel-config-generator --type serverless
```

### Edge Functions

```bash
vercel-config-generator --type edge
```

## 输出示例

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": null,
  "version": 2,
  "regions": ["iad1"],
  "functions": {
    "api/**/*.js": {
      "runtime": "nodejs18.x",
      "maxDuration": 10,
      "memory": 1024
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/$1"
    }
  ]
}
```

## 常见配置

### React/Next.js

```bash
vercel-config-generator --framework nextjs
```

### Vite

```bash
vercel-config-generator --framework vite
```

### 自定义

```bash
vercel-config-generator --type serverless --region iad1
```

## 部署

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
vercel deploy
```

## 变现思路

1. **模板销售** - 项目配置模板
2. **咨询服务** - Vercel 部署咨询

## 安装

```bash
# 无需额外依赖
```
