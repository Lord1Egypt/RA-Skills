---
name: reactive-resume
description: Reactive Resume 开源简历构建器开发指南。使用 TanStack Start (React 19 + Vite)、PostgreSQL + Drizzle ORM、ORPC (Type-safe RPC)、Better Auth。当用户需要：(1) 本地开发环境搭建，(2) 自定义模板开发，(3) 数据库迁移管理，(4) PDF 导出配置，(5) 自部署配置，(6) 功能扩展开发。
---

# Reactive Resume 开发工作流

## 概述

Reactive Resume 是一个免费开源的简历构建器，使用现代化全栈 TypeScript 技术栈。本技能指导你进行本地开发、模板定制、功能扩展和自部署。

**核心特性**：
- 实时预览简历编辑
- 多模板系统（Pokémon 主题命名）
- PDF/JSON 导出
- AI 集成（OpenAI/Gemini/Claude）
- 多语言支持（Crowdin）
- 自部署友好（Docker）

## 快速开始

### 1. 环境要求

- Node.js 20+
- pnpm 9+
- Docker + Docker Compose
- Git

### 2. 克隆项目

```bash
git clone https://github.com/amruthpillai/reactive-resume.git
cd reactive-resume
```

### 3. 启动依赖服务

```bash
# 启动 PostgreSQL 和 Browserless（PDF 导出必需）
sudo dockerd &>/var/log/dockerd.log &
sudo docker compose -f compose.dev.yml up -d postgres browserless
```

### 4. 配置环境变量

```bash
cp .env.example .env
```

**关键配置**：
```bash
# 本地开发
APP_URL=http://localhost:3000

# Database (Docker PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/reactive_resume

# Printer (Browserless for PDF)
# 获取 Docker bridge IP:
# sudo docker network inspect reactive_resume_default --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}'
PRINTER_APP_URL=http://<GATEWAY_IP>:3000
PRINTER_ENDPOINT=ws://<GATEWAY_IP>:4000?token=1234567890

# Auth (可选，开发可留空)
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_COOKIE_DOMAIN=localhost

# S3/Storage (可选，开发用本地文件系统)
# 留空则使用本地存储
```

### 5. 安装依赖并启动

```bash
pnpm install
pnpm dev
```

访问 http://localhost:3000

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | TanStack Start (React 19, Vite, Nitro) |
| 语言 | TypeScript |
| 数据库 | PostgreSQL + Drizzle ORM |
| API | ORPC (Type-safe RPC) |
| 认证 | Better Auth |
| 样式 | Tailwind CSS |
| UI 组件 | Radix UI |
| 状态管理 | Zustand + TanStack Query |

## 项目结构

```
reactive-resume/
├── src/
│   ├── app/                    # TanStack Start 路由
│   │   ├── (public)/           # 公开页面
│   │   ├── (dashboard)/        # 仪表台页面
│   │   ├── api/                # API 路由 (ORPC)
│   │   └── __root.tsx          # 根路由
│   ├── components/
│   │   ├── ui/                 # 基础 UI 组件
│   │   ├── resume/             # 简历相关组件
│   │   ├── templates/          # 模板组件
│   │   └── forms/              # 表单组件
│   ├── lib/
│   │   ├── auth/               # 认证逻辑
│   │   ├── db/                 # 数据库配置
│   │   ├── printer/            # PDF 打印服务
│   │   └── utils.ts
│   ├── server/
│   │   ├── db/
│   │   │   ├── schema/         # Drizzle schema 定义
│   │   │   └── migrations/     # 数据库迁移
│   │   └── api/
│   │       └── routers/        # ORPC 路由定义
│   └── types/
├── public/
│   └── templates/              # 简历模板
│       ├── jpg/                # 模板预览图
│       └── [template-name]/    # 模板组件
├── locales/                    # 多语言文件
├── scripts/
├── docs/
└── compose*.yml                # Docker Compose 配置
```

## 核心工作流

### 开发新模板

1. **在 `public/templates/` 创建模板目录**
```bash
public/templates/
└── my-template/
    ├── index.tsx          # 模板主组件
    ├── schema.ts          # 模板配置 schema
    └── preview.jpg        # 预览图
```

2. **实现模板组件**
```tsx
import { TemplateProps } from '@/types/template';

export function MyTemplate({ resume }: TemplateProps) {
  return (
    <div className="template my-template">
      {/* 简历内容 */}
    </div>
  );
}
```

3. **注册模板**
在 `src/lib/templates.ts` 中添加模板配置

4. **测试导出**
```bash
pnpm dev
# 访问 http://localhost:3000/editor
# 选择新模板，测试 PDF 导出
```

### 数据库迁移

```bash
# 修改 schema 后生成迁移
pnpm db:generate

# 运行迁移（开发启动时自动执行）
pnpm db:migrate

# 查看迁移状态
pnpm db:status
```

### 添加新功能 API

1. **在 `src/server/api/routers/` 创建路由**
```typescript
// src/server/api/routers/custom.ts
import { router, publicProcedure } from '../trpc';

export const customRouter = router({
  myFeature: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      // 业务逻辑
      return { data: 'result' };
    }),
});
```

2. **在根路由注册**
```typescript
// src/server/api/root.ts
import { customRouter } from './routers/custom';

export const appRouter = router({
  custom: customRouter,
  // ... 其他路由
});
```

3. **前端调用**
```typescript
import { api } from '@/lib/api';

const result = await api.custom.myFeature.query({ id: '123' });
```

### 自部署配置

**Docker Compose 部署**：

```yaml
# docker-compose.yml
version: '3.8'
services:
  reactive-resume:
    image: amruthpillai/reactive-resume:latest
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/reactive_resume
      - PRINTER_ENDPOINT=ws://printer:3000?token=1234567890
    depends_on:
      - postgres
      - printer

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=reactive_resume
    volumes:
      - postgres_data:/var/lib/postgresql/data

  printer:
    image: browserless/chrome:latest
    ports:
      - "4000:3000"
    environment:
      - TOKEN=1234567890

volumes:
  postgres_data:
```

## 常见问题

### Q: PDF 导出失败？
A: 检查 Browserless 服务是否运行，确认 `PRINTER_ENDPOINT` 配置正确（使用 Docker bridge IP 而非 localhost）。

### Q: 如何获取 Docker bridge IP？
A: 运行 `sudo docker network inspect reactive_resume_default --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}'`

### Q: 邮件验证跳过？
A: 开发环境点击注册后的 "Continue" 按钮可跳过邮件验证。

### Q: 如何添加新语言？
A: 在 `locales/` 目录添加语言文件，通过 Crowdin 管理翻译。

## 最佳实践

### ✅ 推荐

- 使用 ORPC 类型安全 API
- 所有数据库访问通过 Drizzle ORM
- 组件使用 Radix UI 基础组件
- 样式使用 Tailwind CSS
- 提交前运行 `pnpm lint` 和 `pnpm typecheck`

### ❌ 避免

- 直接写 SQL（使用 Drizzle）
- 跳过类型检查
- 硬编码配置（使用环境变量）
- 忽略多语言支持

## 资源导航

### 官方文档
- [Getting Started](https://docs.rxresu.me/getting-started)
- [Self-Hosting](https://docs.rxresu.me/self-hosting/docker)
- [Development](https://docs.rxresu.me/contributing/development)
- [Architecture](https://docs.rxresu.me/contributing/architecture)

### 社区
- [Discord](https://discord.gg/aSyA5ZSxpb)
- [GitHub](https://github.com/amruthpillai/reactive-resume)
- [Crowdin 翻译](https://crowdin.com/project/reactive-resume)

---

**参考文件**：
- `references/templates-guide.md` - 模板开发完整指南
- `references/deployment.md` - 部署配置参考
- `references/api-reference.md` - API 开发参考

**脚本工具**：
- `scripts/create-template.py` - 快速创建模板结构
- `scripts/db-reset.py` - 重置开发数据库

**资产模板**：
- `assets/template-boilerplate/` - 模板开发脚手架
