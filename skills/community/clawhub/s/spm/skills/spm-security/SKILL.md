---
name: spm-security
version: 1.0.0
description: 安全规范 — Web应用最低安全标准。Agent 常见遗漏：输入验证、XSS、CSRF、密钥管理。SPM Phase 4 质量门中自动引用。
---

# SPM Security — 安全规范

## 自动检测

SPM Phase 4 质量门自动引用本技能——在标准化验证报告的 Security 阶段使用。

## 独立使用

不走 SPM 也可以直接说："按 spm-security 检查这个 PR。"

---

> 不教渗透测试。Agent 代码里最常见的 5 个安全漏洞，一个都别漏。

---

## 输入验证

```
✅ 所有用户输入 → 服务端验证 (不只是前端)
✅ 白名单 > 黑名单
✅ 长度限制 (防止超长输入)
✅ 类型强制 (parseInt, zod schema)

❌ 前端验证了就放行 (curl 绕过)
❌ 信任 URL 参数
❌ 直接 req.body.xxx 进数据库
```

```typescript
// ✅ Zod schema 验证
const loginSchema = z.object({
  username: z.string().min(3).max(50),
  password: z.string().min(8).max(128),
})
const body = loginSchema.parse(req.body)
```

---

## 认证 & 授权

```
✅ 密码: bcrypt hash, salt rounds ≥ 12
✅ Token: JWT + 过期时间(≤24h access, ≤7d refresh)
✅ 密钥: process.env.JWT_SECRET, 不小于 256 bits
✅ 权限: 每个端点检查角色, 不在前端判断

❌ 密码明文或 MD5/SHA1 存储
❌ 无过期时间的 token
❌ 硬编码密钥
❌ 前端 hide 了 admin 按钮以为就安全了
```

---

## XSS 防护

```typescript
// ❌ 直接插用户输入到 HTML
<div>{user.bio}</div>  // 如果 bio 是 "<script>alert(1)</script>"

// ✅ React 自动转义 (curl括号没问题)
<div>{user.bio}</div>  // React 默认安全

// ⚠️ dangerouslySetInnerHTML 必须 sanitize
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(user.bio) }} />
```

**规则：永远不要 `dangerouslySetInnerHTML` 未经 sanitize 的用户内容。**

---

## 密钥管理

```
✅ process.env.XXX (环境变量)
✅ .env → .gitignore (不提交)
✅ .env.example (只有 key 名，没有值)
✅ 生产环境用密钥管理服务

❌ const API_KEY = "sk-xxx" (硬编码)
❌ git历史里有密钥 (及时轮换)
❌ 前端代码里有密钥 (看得见)
```

---

## 依赖安全

```bash
# ✅ 定期检查
npm audit          # 已知漏洞
npm outdated       # 过期依赖

# ✅ 在 CI 中加:
npm audit --audit-level=high  # high/critical → CI 失败
```

---

## Agent 常见安全遗漏

| # | 遗漏 | 后果 | 修复 |
|---|------|------|------|
| 1 | 不验证输入类型和范围 | SQL注入、溢出 | Zod/Yup schema |
| 2 | CORS 配成 `*` | 任何网站能调你的 API | 指定域名白名单 |
| 3 | 错误信息暴露内部细节 | 攻击者获得线索 | 生产环境只返回通用错误 |
| 4 | 不设 rate limit | 暴力破解 | 登录端点 + rate limiter |
| 5 | 文件上传不校验类型 | 上传 .php 执行 | 白名单 mime type + 大小限制 |
| 6 | Cookie 不设 HttpOnly/Secure | XSS 偷 token | `httpOnly: true, secure: true, sameSite: 'strict'` |

---

## 安全自查清单

每个 PR 合并前跑一遍：

```
□ 所有用户输入有服务端验证？
□ 密码用 bcrypt 且 salt ≥ 12？
□ JWT 有过期时间？
□ 密钥在环境变量，不在代码里？
□ .env 在 .gitignore？
□ CORS 不是 *？
□ 生产环境错误信息不暴露栈跟踪？
□ npm audit 无 high/critical？
□ SQL 用参数化查询？
□ 文件上传有类型校验？
```

**任何一项不通过 → 不允许合并。**
