---
name: task-delegator
description: 任务委派模式 - 自动将所有需要使用工具的任务委派给子 agent 处理。始终用于：搜索、浏览、读写文件、代码执行、API 调用、数据分析。绝不用于：闲聊、无需工具的简单问答、确认事项。触发短语：委托这个 OR 当任何工具操作需要时隐式触发。核心行为：使用 sessions_spawn() 配合 cleanup:"delete" 保持主会话上下文精简。
user-invokable: true
---

# 任务委派器 (Task Delegator)

## 作用

通过将所有实际工作委派给临时子 agent，保持主对话上下文整洁。

**主会话 = 调度器 + 汇报者，不是工作者**

---

## 触发方式

### 显式触发
用户说：
- "委托这个" / "delegate this"
- "使用子 agent" / "use subagent"
- "生成 agent" / "spawn agent"

### 隐式触发（自动）
**以下任何情况需要时自动激活：**
- 网络搜索或浏览
- 读取/写入/编辑文件
- 代码执行或分析
- API 调用或外部操作
- 数据处理或转换
- 使用任何工具（bash、web、read、write、edit 等）

---

## 核心规则（必须遵循）

### 规则 1：委派所有需要工具的任务

```javascript
// 应该做 - 委派给子 agent
sessions_spawn({
  task: "清晰具体的任务描述",
  runtime: "subagent",
  mode: "run",
  cleanup: "delete",  // 关键 - 自动清理记录
  model: "zai/glm-4.7-flash"  // 可选：简单任务使用快速模型
})

// 不要做 - 在主会话直接执行
// 不要直接使用 web_search、browser、read、write、edit、bash 等
// 特别注意：写入 soul.md 也必须委派，绝不能在主会话直接写入
```

### 规则 2：只有纯对话留在主会话

以下情况才不委派：
- 纯对话（问候、闲聊）
- 无需工具的简单问答（如"2+2等于几"）
- 确认/澄清事项
- 关于委派本身的元讨论

### 规则 3：记忆判断（两个检查点）

**检查点 1：委派前**
```javascript
// 如果任务重要则存储：决策、偏好、重大项目
if (任务涉及重要决策 || 用户偏好 || 重大项目) {
  memory_store({
    text: "决策/偏好/项目的简要总结",
    category: "decision" | "preference" | "fact",
    importance: 0.7
  })
}
```

**检查点 2：收到结果后**
```javascript
// 如果结果有长期价值则存储：配置、事实、决策
if (结果是重要事实 || 配置 || 决策结果) {
  memory_store({
    text: "简短的1-2句话总结",
    category: "fact" | "decision" | "other",
    importance: 0.6
  })
}

// 不要存储：临时信息（新闻、天气）、一次性查询、聊天内容
```

### 规则 4：写入 soul.md

**重要：任何写入 soul.md 的操作都必须委派给子 agent**

```javascript
// 正确 - 委派给子 agent
sessions_spawn({
  task: "将以下内容写入 soul.md：[具体内容]",
  runtime: "subagent",
  mode: "run",
  cleanup: "delete"
})

// 错误 - 不要在主会话直接写入
// write({ file_path: "soul.md", content: "..." })
```

**写入场景示例：**
- 记录重要对话总结
- 保存用户偏好设置
- 存储项目决策和里程碑
- 记录学习笔记和知识点

### 规则 5：简洁汇报结果

- 使用要点列表
- 给出结果，不描述过程
- 绝不要向用户提及"子 agent"、"生成"、"委派"、"subagent"、"runtime"
- 用户应该只看到结果

---

## 使用示例

### 示例 1：网络搜索

**用户：** "查看今天的科技新闻"

```javascript
// 正确
sessions_spawn({
  task: "搜索今天的主要科技新闻，总结3-5条关键内容并附带简要描述",
  runtime: "subagent",
  mode: "run",
  cleanup: "delete",
  model: "zai/glm-4.7-flash"  // 简单任务，使用快速模型
})

// 错误 - 不要这样做
// web_search({ query: "tech news today" })
```

**给用户的结果（简洁）：**
```
以下是今天的主要科技新闻：

• Apple 发布 iOS 18.2，新增 AI 功能
• OpenAI 宣布 GPT-5 预览版
• Tesla 揭晓新机器人出租车设计
• Chrome 获得重大隐私更新
```

### 示例 2：文件分析

**用户：** "分析这个代码文件"

```javascript
// 正确
sessions_spawn({
  task: "阅读并分析 /path/to/file.js 的代码，识别主要函数、使用的模式，以及任何潜在问题",
  runtime: "subagent",
  mode: "run",
  cleanup: "delete"
})
```

### 示例 3：代码编写

**用户：** "写一个解析 JSON 的函数"

```javascript
// 正确
sessions_spawn({
  task: "编写一个带错误处理的 JavaScript JSON 安全解析函数。包含使用示例。",
  runtime: "subagent",
  mode: "run",
  cleanup: "delete"
})
```

---

## 记忆判断示例

### 委派前存储
```javascript
// 用户："以后简单搜索用快速模型"
memory_store({
  text: "用户偏好：简单搜索任务使用 glm-4.7-flash",
  category: "preference",
  importance: 0.8
})

// 用户："我要开始一个新项目，构建 Rust 网络服务器"
memory_store({
  text: "用户开始新项目：Rust 网络服务器",
  category: "other",
  importance: 0.7
})
```

### 收到结果后存储
```javascript
// 子 agent 返回："OpenClaw 版本 2026.3.8 支持 skill 热重载"
memory_store({
  text: "OpenClaw 2026.3.8 支持 skill 热重载功能",
  category: "fact",
  importance: 0.7
})
```

### 不存储
```javascript
// 今天的新闻（明天就过时）
// 天气（临时信息）
// "这个文件有多少行"（一次性查询）
// 闲聊内容
```

---

## 决策流程

```
┌─────────────────────┐
│   用户请求          │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ 需要工具？   │ ← 包括：搜索、读写、执行、API 调用、写入 soul.md
    └──────┬───────┘
           │
    ┌──────┴──────┐
    │             │
   否            是
    │             │
    ▼             ▼
┌─────────┐  ┌─────────────────┐
│ 在主会话│  │ 🧠 记忆检查     │
│ 处理    │  │ （委派前）       │
└─────────┘  └────────┬────────┘
                      │
                      ▼
              ┌──────────────────┐
              │ 生成子 agent     │
              │ cleanup:"delete" │
              └────────┬─────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ 子 agent 执行   │
              └────────┬────────┘
                       │
                       ▼
              ┌───────────────────┐
              │ 🧠 记忆检查       │
              │ （结果后）         │
              └────────┬──────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ 汇报结果       │
              │ （简洁）       │
              └─────────────────┘
```

---

## 配置

### 在 AGENTS.md 或 USER.md 中启用：

```markdown
## 任务委派模式

所有需要工具的任务都自动委派给子 agent 处理。

- 主会话绝不直接使用工具（除了 memory_store）
- 始终使用 sessions_spawn() 配合 cleanup:"delete"
- 在两个检查点判断记忆存储
- 简洁汇报结果，不要提及委派过程

## 特别注意：写入 soul.md

写入 soul.md 是工具操作，必须委派给子 agent：
- 绝不在主会话直接使用 write 工具写入 soul.md
- 任何需要记录到 soul.md 的内容都通过 sessions_spawn 委派
```

### 清理机制

`cleanup: "delete"` 参数确保：
- 子 agent 记录自动标记为待删除
- 系统定期运行清理
- 无需人工干预
- 主会话永久保持精简

---

## 为什么这很重要

**问题：** 长对话会积累大量工具输出到上下文中
**解决：** 只保留任务摘要，丢弃执行细节
**收益：** 会话保持快速、低成本、专注于结果
