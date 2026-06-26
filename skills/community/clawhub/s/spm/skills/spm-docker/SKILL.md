---
name: spm-docker
version: 1.0.0
description: Docker规范 — Dockerfile最佳实践、多阶段构建、compose、安全。Agent经常写出10GB镜像。SPM Phase 5 自动引用。
---

# SPM Docker — Docker 规范

## 自动检测

SPM Phase 5 检测到 `Dockerfile` / `docker-compose.yml` → 自动引用本技能。

## 独立使用

"按 spm-docker 规范写 Dockerfile。"

---

## Dockerfile 最佳实践

```dockerfile
# ✅ 多阶段构建（减小镜像）
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]

# ❌ 单阶段：COPY . . → npm install → npm run build
# 结果：node_modules + 源码 + 构建产物 = 1.2GB 镜像
```

---

## Agent Docker 反模式

| # | 反模式 | 修复 |
|---|--------|------|
| 1 | 单阶段，`COPY . .` | 多阶段构建，只拷需要的 |
| 2 | `npm install` (不是 `npm ci`) | 用 `npm ci --production=false` |
| 3 | `FROM node:latest` (不可复现) | 固定版本 `node:20-alpine` |
| 4 | `RUN apt-get install ...` (不清理) | `&& rm -rf /var/lib/apt/lists/*` |
| 5 | root 用户运行 | `USER node` |
| 6 | `.dockerignore` 缺失 | 忽略 `node_modules`, `.git`, `dist` |
| 7 | 环境变量写死 | `ENV NODE_ENV=production` 放 Dockerfile |
| 8 | 镜像里跑 dev 依赖 | `npm ci --production` |

---

## 基础镜像选择

```
✅ node:20-alpine (Node.js, 最小)
✅ python:3.12-slim (Python)
✅ golang:1.22-alpine (Go)

❌ ubuntu:latest → 77MB 基础镜像，然后装 Node
❌ node:latest → 下次构建可能变版本
```

---

## docker-compose

```yaml
# ✅
services:
  app:
    build: .
    ports: ["3000:3000"]
    depends_on:
      db:
        condition: service_healthy   # 等 DB 就绪
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      retries: 5

volumes:
  pgdata:
```

---

## 安全

```dockerfile
# ✅
USER node                          # 非 root
COPY --chown=node:node . .        # 文件归属
RUN npm ci --ignore-scripts       # 禁 postinstall 脚本

# ❌
USER root
RUN npm install -g some-tool       # 全局安装
```

**.dockerignore 最小内容：**
```
node_modules
.git
dist
.env
*.log
```
