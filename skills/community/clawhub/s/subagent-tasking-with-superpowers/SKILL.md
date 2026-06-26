---
name: subagent-tasking-with-superpowers
description: 子代理任务拆分 + using-superpowers 技能执行。每次 spawn 子代理前必须遵守的铁律。结合 using-superpowers 和 subagent-tasking 规则。
---

# 子代理任务拆分 + Superpowers 执行（铁律！）

## 核心原则

**每次 spawn 子代理前，必须执行以下流程。没有例外。不可跳过。不可 rationalize。**

---

## 流程图

```
用户任务 → 调用 using-superpowers 技能 → 检查相关技能 → 任务拆分自检 → 写 Task Brief → Spawn 子代理 → 验证结果 → 论坛留痕
```

---

## 第1步：调用 using-superpowers 技能

**必须先调用 using-superpowers 技能**，确认是否有其他相关技能适用。

- 如果有 1% 可能技能适用 → 调用它
- 不得跳过此步骤
- 不得 rationalize 说不需要

### Red Flags（禁止这样想！）

| 错误想法 | 现实 |
|---------|------|
| "这只是简单任务" | 简单任务也需要检查技能 |
| "我先看看情况" | 技能检查在看情况之前 |
| "我知道怎么做" | 知道 ≠ 用技能，必须调用 |
| "技能太复杂了" | 越复杂越要用技能 |

---

## 第2步：任务拆分自检

```
问自己3个问题：

1. 这个任务能拆成 2 个以上独立的子任务吗？
   → 能就拆，每个子任务单独 spawn

2. 子代理需要访问多少个文件/目录？
   → 超过 3 个就拆

3. 子代理需要执行多少步操作？
   → 超过 5 步就拆
```

---

## 第3步：写 Task Brief 文件

每个子代理的任务必须写入 `/tmp/tasks/` 目录：

```
/tmp/tasks/{任务名}_{时间戳}.md

内容格式：
# 任务名
- 目标：1句话描述
- 步骤：不超过3步
- 输出：返回什么格式
- 限制：不能做什么
```

---

## 第4步：Spawn 规则

| 规则 | 要求 |
|------|------|
| 每个 spawn 只做一件事 | ✅ |
| task 描述不超过 200 字 | ✅ |
| 复杂任务拆成多个 spawn | ✅ |
| 子代理模型与父代理一致 | ✅ |
| 完成后在论坛留痕 | ✅ |

---

## 示例

### ❌ 错误：任务太大
```
spawn tiechui: "检查论坛状态、修复问题、清理文件、更新文档"
```

### ✅ 正确：拆分
```
spawn tiechui-ops: "检查端口8808服务状态，报告HTTP响应码"
spawn tiechui-forum: "检查 posts.json 完整性，报告帖子数"
spawn tiechui-dev: "列出 workspace-tiechui 下的 .py 文件"
```

---

## 违反后果

- 子代理超时无输出
- 浪费 Token
- 任务失败需要重试
- 记录到 corrections.md

---

*规则创建时间：2026-04-12*
*维护人：铁头 🤖*
