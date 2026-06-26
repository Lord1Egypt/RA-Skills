---
name: spm-onboarding
version: 1.0.0
description: 代码库接入规范 — Agent 接入已有项目最常见的错误：不看代码就写，不看约定就改。本技能给正确接入流程。
---

# SPM Onboarding — 代码库接入规范

## 自动检测

SPM Phase 1 或 Phase 3 检测到"现有项目"而非"新建项目" → 子代理 dispatch 前自动引用。

## 独立使用

"帮我了解一下这个项目" → Agent 按本技能走，不上来就写。

---

## Agent 接入反模式

| # | 反模式 | 症状 |
|---|--------|------|
| 1 | **上来就写** | 没看 `package.json` 就开始 `npm install xxx` |
| 2 | **猜代码结构** | "应该是放在 `src/components/`"——其实在 `app/ui/` |
| 3 | **忽略 lint/formatter 配置** | 写的代码格式和其他文件完全不同 |
| 4 | **不管已有抽象** | 重新写了一个 fetch wrapper，其实已有 `lib/api.ts` |

---

## 接入流程（5 步，按顺序）

### Step 1: 读入口文件

```bash
# 1. 包管理器 + 脚本
cat package.json | grep -E '"name"|"scripts"|"dependencies"'

# 2. TypeScript 配置
cat tsconfig.json 2>/dev/null | head -20

# 3. Lint/Format 配置
ls .eslintrc* .prettierrc* eslint.config.* 2>/dev/null
```

### Step 2: 读项目结构

```bash
# 不要 cat，用 tree 或 ls -R 理解层次
ls -la src/ 2>/dev/null || ls -la app/ 2>/dev/null
# 关键目录: components, routes, utils, hooks, lib, types
```

### Step 3: 读一个已有组件/模块

```bash
# 找一个典型组件，理解代码模式:
# - 怎么 import? (相对路径? alias?)
# - 怎么 export? (default? named?)
# - 怎么处理 props? (type? interface?)
# - 怎么处理样式? (CSS Modules? Tailwind?)
# - 怎么处理错误? (try-catch? error boundary?)

head -30 src/components/SomeComponent.tsx
```

### Step 4: 确认框架约定

```bash
# 路由方式? (Next.js pages? React Router?)
# 状态管理? (Zustand? Redux? Context?)
# 数据获取? (React Query? SWR? useEffect?)
# 测试框架? (Jest? Vitest? Playwright?)
# 样式方案? (Tailwind? CSS Modules? styled-components?)
```

### Step 5: 跑一遍测试

```bash
npm test 2>&1 | tail -5
# 确认基线: 多少个测试? 全过吗?
```

---

## 接入后规则

```
✅ 新代码模仿已有代码的风格（不是自己的偏好）
✅ 用已有的工具函数和抽象
✅ 先问再改架构约定

❌ "这个项目太乱了，我重写一下"
❌ "这个没用 TypeScript，我加上"
❌ "这个没用 Tailwind，我装上"
```

**铁律：接入 = 先理解，再动手。不理解就写 = 一定写错。**
