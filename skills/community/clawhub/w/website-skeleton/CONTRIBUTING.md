# 贡献指南

感谢你对建站骨架 (EdgeOne Pages) 的关注！

## 快速开始

```bash
git clone https://github.com/liuboacean/website-skeleton-skill.git
cd website-skeleton-skill
npm install
npm run build
```

## 项目结构

| 目录 | 用途 |
|------|------|
| `sharing/` | 跨运行时共享模块（类型、工具函数、校验器） |
| `edge-functions/` | Edge Functions（V8 + KV） |
| `cloud-functions/` | Cloud Functions（Node.js + D1） |
| `client/` | 前端 SPA |
| `db/migrations/` | D1 数据库迁移脚本 |
| `references/` | 能力参考文档 |
| `templates/` | 场景预设模板 |

## 开发工作流

1. **Fork 并 Clone**
2. **创建分支**：`git checkout -b feature/my-feature`
3. **编写代码**：遵循现有代码风格
4. **语法检查**：`node --check <your-file>.js`
5. **构建验证**：`npm run build`
6. **提交**：使用语义化提交信息（如 `feat:`, `fix:`, `docs:`）
7. **发起 PR**：填写 PR 模板

## 代码规范

- 所有 SQL 必须包含 `{tenant}` 占位符
- Edge Functions 与 Cloud Functions 各司其职（见 `references/edge-functions.md`、`references/cloud-functions.md`）
- KV 仅 Edge Functions 可直接访问
- 敏感操作（支付、bcrypt）必须在 Cloud Functions 中
- 使用 `sharing/validators.js` 进行参数校验
- 使用 `sharing/response.js` 构建统一 API 响应

## 安全

- 永远不要在客户端计算价格
- 支付回调不依赖 JWT（绕过认证中间件）
- JWT 不放在 localStorage（HttpOnly Cookie）
- 发现安全漏洞请私下报告，不要提交公开 Issue
