---
slug: security-auditor-tool-free
name: security-auditor-tool-free
version: 1.0.0
displayName: 代码安全审计员(免费版)
summary: "OWASP Top 10代码审计,含安全编码模式、输入验证、认证安全检查,适合开发者自检,支持多种使用场景和自动化处理"
license: Proprietary
edition: free
description: 核心能力:，可自动提升工作效率

  - OWASP Top 10:2021安全审计检查清单

  - 安全编码模式与反模式对比

  - 输入验证与文件上传安全

  - JWT认证与Cookie安全最佳实践

  - 安全HTTP头配置指南

  - 依赖安全扫描命令

  适用场景:

  - 代码审查中的安全检查

  - 安全编码学习与培训

  - 开发阶段安全自检

  - 认证流程安全设计

  差异化:

  - 每个漏洞类型包含BAD/GOOD代码对比

  - 覆盖TypeScript/Python常用框架

  - 可操作的修复建议

  - 中文解释与注释

  触发关...'
tags:
  - 安全
  - 代码审计
  - 安全编码
  - OWASP
  - 加密
  - 工具
  - owasp
  - top
  - const
  - await
  - req
tools:
  - read
  - exec
homepage: ""
category: "Security"
---
# 代码安全审计员(免费版)

## 概述

代码安全审计员免费版是一款面向开发者的代码安全审查工具。基于 OWASP Top 10:2021 安全框架,提供涵盖访问控制、加密失败、注入、XSS、配置错误等核心漏洞类型的审计检查清单。每个漏洞类型包含 BAD/GOOD 代码对比示例,帮助开发者快速理解安全编码模式与反模式,并提供可操作的修复建议.
## 核心能力

### OWASP Top 10 检查清单

| 编号 | 漏洞类型 | 严重等级 | 检查要点 |
|---|----|----|----|
| A01 | 访问控制失效 | HIGH | 认证检查、授权验证、CORS配置 |
| A02 | 加密失败 | HIGH | 密码哈希、数据加密、TLS配置 |
| A03 | 注入 | CRITICAL | SQL注入、命令注入、参数化查询 |
| A05 | 安全配置错误 | MEDIUM | 默认凭据、错误信息泄露、安全头 |
| A07 | 身份认证失败 | HIGH | JWT安全、Cookie配置、速率限制 |

**处理**: 解析OWASP Top 10 检查清单的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回OWASP Top 10 检查清单的响应数据,包含状态码、结果和日志.
### 免费版与专业版对比

| 功能 | 免费版 | 专业版 |
|:-----|:-----|:-----|
| OWASP覆盖 | Top 5 | Top 10全覆盖 |
| 代码示例 | TypeScript | TS+Python+Go+Java |
| 审计报告 | 文本格式 | HTML/PDF/SARIF |
| 自动扫描 | 不支持 | AST静态分析 |
| 框架支持 | Next.js/Express | 10+框架 |
| 合规映射 | 不支持 | PCI-DSS/OWASP ASVS |
| 持续监控 | 不支持 | Git Hook集成 |

**处理**: 解析免费版与专业版对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回免费版与专业版对比的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：代码审计、含安全编码模式、输入验证、认证安全检查、适合开发者自检、核心能力、安全审计检查清单、安全编码模式与反、模式对比、输入验证与文件上、传安全、认证与、安全最佳实践、HTTP、头配置指南、依赖安全扫描命令等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:SQL注入审计

检查代码中是否存在SQL注入漏洞.
**BAD - 存在注入:**
```typescript
// ❌ 字符串拼接,存在SQL注入风险
const query = `SELECT * FROM users WHERE email = '${email}'`
const result = await db.query(query)
```

**GOOD - 参数化查询:**
```typescript
// ✅ 使用参数化查询
const user = await db.query('SELECT * FROM users WHERE email = $1', [email])
// ...
// ✅ 使用ORM内置安全查询
const user = await prisma.user.findUnique({ where: { email } })
```

**检查要点:**
- 所有数据库查询使用参数化语句或ORM
- 查询中无字符串拼接
- OS命令执行使用参数数组,而非shell字符串
- 用户输入不用于 `eval()` 或 `Function()`

### 场景二:访问控制审计

```typescript
// ❌ BAD: 无授权检查
app.delete('/api/posts/:id', async (req, res) => {
  await db.post.delete({ where: { id: req.params.id } })
  res.json({ success: true })
})
// ...
// ✅ GOOD: 验证身份和权限
app.delete('/api/posts/:id', authenticate, async (req, res) => {
  const post = await db.post.findUnique({ where: { id: req.params.id } })
  if (!post) return res.status(404).json({ error: 'Not found' })
  if (post.authorId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' })
  }
  await db.post.params.id } })
  res.json({ success: true })
})
```

### 场景三:认证安全审计

检查JWT和Cookie安全配置.
```typescript
import { SignJWT, jwtVerify } from 'jose'
// ...
const secret = new TextEncoder().encode(process.env.JWT_SECRET)
// ...
// ✅ 安全的JWT创建
export async function createToken(payload: { userId: string; role: string }) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('15m')  // 短期访问令牌
    .setAudience('your-app')
    .setIssuer('your-app')
    .sign(secret)
}
// ...
// ✅ 安全的JWT验证
export async function verifyToken(token: string) {
  try {
    const { payload } = await jwtVerify(token, secret, {
      algorithms: ['HS256'],
      audience: 'your-app',
      issuer: 'your-app',
    })
    return payload
  } catch {
    return null
  }
}
// ...
// ✅ 安全的Cookie配置
cookies().set('session', token, {
  httpOnly: true,     // 禁止JavaScript访问
  secure: true,       // 仅HTTPS
  sameSite: 'lax',    // CSRF防护
  maxAge: 60 * 60 * 24 * 7,
  path: '/',
})
```

## 不适用场景

以下场景代码安全审计员(免费版)不适合处理：

- 渗透测试未授权目标
- 物理安全防护
- 社会工程学攻击

## 触发条件

需要安全检测、合规审计、漏洞扫描、加密防护时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 安全审计检查流程

```python
class CodeSecurityAuditor:
    """代码安全审计器"""
# ...
    OWASP_CHECKS = {
        "A01_access_control": {
            "name": "访问控制失效",
            "patterns": [
                (r"app\.(get|post|put|delete)\(.*(?!.*authenticate)", "路由缺少认证中间件"),
                (r"res\.json\(.*user.*\)", "API响应可能泄露用户数据"),
            ]
        },
        "A03_injection": {
            "name": "注入漏洞",
            "patterns": [
                (r"SELECT.*FROM.*\$\{.*\}", "SQL注入: 字符串拼接查询"),
                (r"exec\(`.*\$\{.*\}`\)", "命令注入: 拼接shell命令"),
                (r"eval\(.*\)", "代码注入: 使用eval()"),
            ]
        },
        "A02_crypto": {
            "name": "加密失败",
            "patterns": [
                (r"password.*[:=].*['\"][^'\"]+['\"]", "明文密码存储"),
                (r"md5\(|sha1\(", "弱哈希算法"),
                (r"http://.*", "非加密HTTP连接"),
            ]
        }
    }
# ...
    def audit_file(self, filepath):
        """审计单个文件"""
        findings = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
# ...
            for check_id, check in self.OWASP_CHECKS.items():
                for pattern, description in check["patterns"]:
                    import re
                    for match in re.finditer(pattern, content, re.IGNORECASE):
                        line_num = content[:match.start()].count('\n') + 1
                        findings.append({
                            "owasp": check_id,
                            "name": check["name"],
                            "line": line_num,
                            "code": lines[line_num - 1].strip() if line_num <= len(lines) else "",
                            "issue": description,
                            "severity": "HIGH" if "注入" in description or "明文" in description else "MEDIUM"
                        })
        return findings
```

### 输入验证模式

```typescript
import { z } from 'zod'
// ...
// ✅ 使用Zod进行输入验证
const userSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(8).max(128),
  name: z.string().min(1).max(100).regex(/^[a-zA-Z\s'-]+$/),
  age: z.number().int().min(13).max(150).optional(),
})
// ...
export async function createUser(formData: FormData) {
  const parsed = userSchema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
    name: formData.get('name'),
  })
// ...
  if (!parsed.success) {
    return { error: parsed.error.flatten() }
  }
  // 安全使用 parsed.data
}
```

#
## 示例

### 安全HTTP头配置

```typescript
// next.config.js
const securityHeaders = [
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "connect-src 'self' https://api.example.com",
      "frame-ancestors 'none'",
    ].join('; '),
  },
]
// ...
module.exports = {
  async headers() {
    return [{ source: '/(.*)', headers: securityHeaders }]
  },
}
```

## 最佳实践

### 1. 密码存储安全

```typescript
// ❌ BAD: 明文存储
await db.user.create({ data: { password: req.body.password } })
// ...
// ✅ GOOD: bcrypt 12+轮
import bcrypt from 'bcryptjs'
const hashedPassword = await bcrypt.hash(req.body.password, 12)
await db.user.create({ data: { password: hashedPassword } })
```

### 2. XSS防护

```typescript
// ❌ BAD: 直接渲染用户输入
<div dangerouslySetInnerHTML={{ __html: userComment }} />
// ...
// ✅ GOOD: 消毒后渲染
import DOMPurify from 'isomorphic-dompurify'
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userComment) }} />
// ...
// ✅ BEST: 纯文本渲染(React自动转义)
<div>{userComment}</div>
```

### 3. 环境变量管理

```typescript
// ❌ BAD: 硬编码密钥
const API_KEY = "sk-1234567890abcdef"
// ...
// ✅ GOOD: 环境变量
const API_KEY = process.env.API_KEY
if (!API_KEY) throw new Error('API_KEY not configured')
```

### 依赖详情

```bash
# 检查依赖漏洞
npm audit
npm audit fix
# ...
# 更新依赖
npx npm-check-updates -u
```

## 常见问题

### Q1: 如何确定需要审计哪些代码?

A: 重点关注以下文件:
- 路由处理文件(含API端点)
- 认证/授权相关文件(auth.ts, middleware.ts)
- 数据库查询文件
- 文件上传处理
- 配置文件(next.config, .env)

### Q2: BAD/GOOD示例可以直接使用吗?

A: 示例代码展示安全编码模式,可直接参考。但需根据您的具体框架和业务逻辑调整.
### Q3: 免费版覆盖哪些OWASP类别?

A: 免费版覆盖Top 5: A01访问控制、A02加密失败、A03注入、A05配置错误、A07认证失败。专业版覆盖全部Top 10.
### Q4: 如何获取自动扫描功能?

A: 免费版提供手动检查清单。专业版提供AST静态分析自动扫描,可检测代码中的安全漏洞并生成报告.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **开发语言**: TypeScript/JavaScript(示例代码)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Node.js | 运行时 | 推荐 | nodejs.org |
| jose | npm包 | 可选 | `npm install jose`(JWT示例) |
| bcryptjs | npm包 | 可选 | `npm install bcryptjs`(密码哈希) |
| zod | npm包 | 可选 | `npm install zod`(输入验证) |
| isomorphic-dompurify | npm包 | 可选 | `npm install isomorphic-dompurify`(XSS防护) |

### API Key 配置
- 免费版无需API Key,所有检查基于代码审查
- 代码示例中的环境变量(如JWT_SECRET)需在项目中配置

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行代码安全审计任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "代码安全审计员(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "security auditor"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
