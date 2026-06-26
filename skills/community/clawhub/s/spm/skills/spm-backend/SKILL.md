---
name: spm-backend
version: 1.0.0
description: 后端架构规范 — 分层/依赖注入/错误处理/中间件。Agent 写后端常见问题：一层到底、错误处理不一致。SPM Phase 2/3 自动引用。
---

# SPM Backend — 后端架构规范

## 自动检测

SPM Phase 2/3 检测到后端任务（Express/Fastify/Koa/Spring）→ 自动引用本技能。

## 独立使用

"按 spm-backend 规范设计这个 API 服务。"

---

## 分层架构

```
Request → Router → Controller → Service → Repository → Database
         (路由)    (控制器)     (业务逻辑) (数据访问)  (数据库)
```

| 层 | 职责 | 不该做 |
|----|------|--------|
| Router | URL 匹配、中间件挂载 | 业务逻辑、数据库查询 |
| Controller | 解析请求、调用 Service、格式化响应 | 业务逻辑 |
| Service | 业务逻辑、事务管理 | 直接操作数据库 |
| Repository | 数据库查询 | 业务逻辑 |

```typescript
// ❌  Router 里做了所有事
router.post('/users', async (req, res) => {
  const { name, email } = req.body
  const hash = await bcrypt.hash(req.body.password, 12)
  const user = await db.insert('users', { name, email, password: hash })
  res.json(user)
})

// ✅ 分层
// router:    router.post('/users', userController.create)
// controller: const user = await userService.create(req.body); res.status(201).json(user)
// service:   const hash = await bcrypt.hash(password, 12); return userRepo.create({...})
// repository: return db.insert('users', data)
```

---

## 错误处理

```
✅ 统一 error handler 中间件（不在每个路由写 try-catch）
✅ 自定义错误类 (NotFoundError, ValidationError, AuthError)
✅ 生产环境错误信息不暴露栈跟踪
✅ async 路由用 wrapper（express-async-errors 或手动 wrap）

❌ 每个路由里 try { ... } catch (e) { res.status(500).json({ error: e.message }) }
❌ 不一样的错误格式（有的 `{error}`, 有的 `{message}`, 有的 `{errors}`）
```

---

## 中间件链

```typescript
// ✅ 中间件顺序
app.use(cors())
app.use(helmet())
app.use(rateLimiter)
app.use(bodyParser.json())
app.use(authMiddleware)     // 认证
app.use('/api', apiRouter)
app.use(errorHandler)       // 最后！捕获所有错误
```

---

## 环境配置

```
✅ 所有配置通过环境变量（process.env.XXX）
✅ 不同环境不同配置（development / staging / production）
✅ 敏感信息不进代码（API keys, DB passwords, JWT secrets）

❌ const DB_URL = "postgres://localhost:5432/mydb" (硬编码)
❌ if (process.env.NODE_ENV === 'production') { ... } 散落各处
```

---

## Agent 后端常见反模式

| # | 反模式 | 修复 |
|---|--------|------|
| 1 | Router 里写业务逻辑 | Controller → Service → Repository 分层 |
| 2 | 每个路由自己处理错误 | 统一 error handler 中间件 |
| 3 | 同步阻塞操作 | 数据库调用/文件读写全部 async |
| 4 | 不验证用户输入 | 每个端点先 validate 再处理 |
| 5 | 不设超时 | 外部 API 调用设 timeout (axios: 10s) |
| 6 | `SELECT *` 无 LIMIT | 永远加 LIMIT，除非明确需要全量 |
