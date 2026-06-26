---
name: spm-testing
version: 1.0.0
description: 测试规范 — Agent 最容易写假测试，本技能纠正最常见错误。SPM Phase 3/4 自动引用。
---

# SPM Testing — 测试规范

## 自动检测

SPM Phase 3 执行阶段检测到项目含 `vitest`/`jest`/`pytest` → 子代理 dispatch 时自动引用本技能。Phase 4 Eval Delta 也引用。

## 独立使用

不走 SPM 也可以直接说："按 spm-testing 规范给这段代码写测试。"

---

> 不教 Jest 语法。专治 Agent 写的假测试——全是 mock、不测边界、不报错也敢打勾。

## 测试金字塔

```
        /\
       /E2E\        关键用户流程 (Playwright)
      /------\
     / 集成  \       API + 数据库 + 服务交互
    /----------\
   /   单元测试  \    函数、组件、工具 (主力)
  /--------------\
```

比例：**70% 单元 + 20% 集成 + 10% E2E**

---

## Agent 测试 7 大反模式

| # | 反模式 | 症状 | 怎么改 |
|---|--------|------|--------|
| 1 | **Mock 一切** | `jest.mock('@/lib/supabase')` 出现在每个测试文件头部 | 只 mock 外部边界(API/数据库)。内部函数不 mock |
| 2 | **不测边界** | 只有 happy path：输入正常值→断言返回 | 至少加：空值/null/undefined/极大值/极长字符串 |
| 3 | **假断言** | `expect(true).toBe(true)` 或 `expect(result).toBeDefined()` | 断言具体行为：`expect(result.data.name).toBe('xxx')` |
| 4 | **测实现而非行为** | `expect(component.state.count).toBe(5)` | 测用户看到的：`expect(screen.getByText('5')).toBeInTheDocument()` |
| 5 | **不测错误路径** | 只有 `it('works')`，没有 `it('handles error')` | 每个函数至少一个错误路径测试 |
| 6 | **测试互相依赖** | 测试2依赖测试1创建的数据 | 每个测试独立创建数据，beforeEach 清理 |
| 7 | **只说"测试通过"不贴证据** | SPM Phase 4 的 Eval Delta 需要真实输出 | 贴命令+输出，不要口述 |

---

## 什么该 Mock、什么不该 Mock

```
✅ 该 Mock:
  - 外部 API 调用 (fetch, axios)
  - 数据库连接
  - 第三方服务 (支付、邮件、存储)
  - 时间 (Date.now)

❌ 不该 Mock:
  - 项目内部函数
  - 工具函数 (formatDate, calculateTax)
  - 组件内部逻辑
  - 类型/接口
```

---

## 每种测试该测什么

### 单元测试

```typescript
// ✅ 完整的单元测试
describe('formatCurrency', () => {
  it('formats positive integer', () => {
    expect(formatCurrency(1234)).toBe('$1,234.00')
  })

  it('handles zero', () => {
    expect(formatCurrency(0)).toBe('$0.00')
  })

  it('throws on negative', () => {
    expect(() => formatCurrency(-1)).toThrow()
  })

  it('formats large number', () => {
    expect(formatCurrency(1234567)).toBe('$1,234,567.00')
  })

  it('handles NaN input', () => {
    expect(() => formatCurrency(NaN)).toThrow()
  })
})
```

**单元测试自检：** 每个函数 ≥ 3 个测试，至少含 1 个边界 + 1 个错误路径。

### 集成测试

```typescript
// ✅ API 集成测试
describe('POST /api/auth/login', () => {
  it('returns token on valid credentials', async () => {
    const res = await request(app).post('/api/auth/login').send({
      username: 'test', password: 'password123'
    })
    expect(res.status).toBe(200)
    expect(res.body.access_token).toBeDefined()
  })

  it('returns 401 on wrong password', async () => {
    const res = await request(app).post('/api/auth/login').send({
      username: 'test', password: 'wrong'
    })
    expect(res.status).toBe(401)
  })

  it('returns 400 on missing fields', async () => {
    const res = await request(app).post('/api/auth/login').send({})
    expect(res.status).toBe(400)
  })
})
```

### E2E 测试

```typescript
// ✅ 关键用户流程
test('user can login and see dashboard', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[data-testid="username"]', 'test')
  await page.fill('[data-testid="password"]', 'password123')
  await page.click('[data-testid="login-btn"]')
  await expect(page).toHaveURL('/dashboard')
  await expect(page.locator('[data-testid="welcome"]')).toBeVisible()
})
```

**E2E 不要测**：每个字段的每个边界值——留给单元测试。

## E2E 测试专项

### 什么必须有 E2E

```
✅ 用户注册→登录→使用核心功能 的完整流程
✅ 支付流程 (加购→结算→支付→确认)
✅ 权限流程 (普通用户看不到管理页面)
✅ 关键表单提交流程

❌ 每个按钮的每种状态
❌ 纯展示页面 (无交互)
❌ 后端 API (那是集成测试的事)
```

### E2E 反模式

| # | 反模式 | 修复 |
|---|--------|------|
| 1 | 用 CSS class 定位 → 改样式就挂 | 用 `data-testid` |
| 2 | 硬编码 `waitForTimeout(3000)` | 用 `waitForSelector` / `waitForResponse` |
| 3 | 测试依赖执行顺序 | 每个 test 独立，`beforeEach` 重置状态 |
| 4 | 只测 Chrome | CI 里跑 2+ 浏览器 |
| 5 | E2E 测试太多 → CI 跑 30 分钟 | 控制在 20 个以内，关键流程 |

### Page Object 模式

```typescript
// ✅ 封装页面操作
class LoginPage {
  constructor(private page: Page) {}
  async login(user: string, pass: string) {
    await this.page.fill('[data-testid="username"]', user)
    await this.page.fill('[data-testid="password"]', pass)
    await this.page.click('[data-testid="login-btn"]')
  }
}

test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.login('test', 'password123')
  await expect(page).toHaveURL('/dashboard')
})
```

---

## 覆盖率底线

```
✅ 代码项目: lines ≥ 80%, branches ≥ 70%
✅ 非代码项目: 跳过覆盖率检查
```

**仅当新增功能时才检查覆盖率。** 不要为了覆盖率补老代码的测试——放到单独的技术债任务中。

---

## 测试文件命名

```
src/utils/formatDate.ts   →  src/utils/formatDate.test.ts
src/routes/auth.ts        →  src/routes/auth.test.ts
src/components/Button.tsx →  src/components/Button.test.tsx
```

**铁律：测试文件紧挨源文件，不放到顶层的 `tests/` 目录。**
