---
name: spm-standards
version: 1.0.0
description: 通用编码规范 — 语言无关的命名/注释/文件组织规则。Agent 经常忘记统一风格。SPM Phase 3 自动引用。
---

# SPM Standards — 通用编码规范

## 自动检测

SPM Phase 3 所有子代理 dispatch 前自动引用本技能（语言无关基础规范）。

## 独立使用

"按 spm-standards 规范写这段代码。"

---

## 命名

| 元素 | 规则 | ✅ | ❌ |
|------|------|-----|-----|
| 变量 | camelCase | `userList`, `isActive` | `user_list`, `data` |
| 常量 | UPPER_SNAKE | `MAX_RETRY`, `API_BASE_URL` | `maxRetry` |
| 函数 | verb + noun | `fetchUsers`, `calculateTotal` | `get`, `handle`, `doStuff` |
| 类/组件 | PascalCase | `UserCard`, `AuthService` | `userCard`, `auth_service` |
| 文件 | kebab-case 或 与默认导出同名 | `user-card.tsx`, `auth.service.ts` | `UserCard.tsx`(非组件), `utils.ts` |
| 布尔 | is/has/should 前缀 | `isLoading`, `hasError` | `loading`, `error` |
| 事件处理 | handle + 事件 | `handleClick`, `handleSubmit` | `onClick`, `clickHandler` |

---

## 注释

```
✅ 写 WHY（为什么这样设计）
✅ 写复杂算法的一句话解释

❌ 写 WHAT（代码已经说了）
❌ 写每个函数都有的模板注释 ("Creates a new user")
❌ 写 TODO 不跟 issue（TODO 必须配 ticket 链接）
```

```typescript
// ✅ WHY
// 用递归而非迭代——树深度不确定，栈空间足够
function walkTree(node: TreeNode) { ... }

// ❌ WHAT
// Walk the tree
function walkTree(node: TreeNode) { ... }
```

---

## 文件组织

```
✅ 一个文件一个主题（单一职责）
✅ 相关文件放一起（组件 + 测试 + 样式 同目录）
✅ index.ts 只做 re-export，不放逻辑

❌ utils.ts / helpers.ts / common.ts（垃圾场）
❌ 单文件超过 500 行（该拆了）
❌ 深层嵌套目录 (>4 层)
```

---

## 函数

```
✅ 单一职责（一个函数做一件事）
✅ 参数 ≤ 4 个（超过 → 用对象）
✅ 提前 return（减少嵌套）
✅ 纯函数优先（同样的输入永远同样输出）

❌ 函数超过 50 行
❌ 修改入参（side effect）
❌ boolean 参数（暗示函数做了两件事）
```

---

## 错误处理

```
✅ 明确错误类型（不要 catch 了只 console.error）
✅ 错误信息包含上下文（哪个用户、哪个操作）
✅ 边界情况显式处理（null、空数组、0）

❌ catch (e) {} 空处理
❌ throw "error" 字符串（throw new Error）
❌ 忽略 async 函数的 rejection
```



## 导入顺序

```typescript
// 1. 外部依赖
import React from 'react'
import { useQuery } from '@tanstack/react-query'

// 2. 内部模块 (alias)
import { Button } from '@/components/Button'
import { formatDate } from '@/utils/date'

// 3. 相对路径
import { type User } from './types'
import './styles.css'
```
