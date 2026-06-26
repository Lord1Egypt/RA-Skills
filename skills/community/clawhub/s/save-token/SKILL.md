---
name: save-token
description: |
  💰 Save Token | Token 节省器
  
  TRIGGERS: Use when token cost is high, conversation is long, files read multiple times, or before complex tasks.
  
  Guiding skill that helps agents identify and avoid sending duplicate context to LLM APIs.
  Teaches agents to recognize repeated content and summarize instead of re-sending.
  
  触发条件：Token 成本高、对话长、文件多次读取、复杂任务前。
  指导 Agent 识别重复内容，避免重复发送，从而节省 Token。

metadata: {"clawdbot":{"emoji":"💰","triggers":["token","cost","duplicate","重复","节省","context","上下文","optimize","优化"],"categories":["productivity","cost-saving","optimization"]}}
---

# 💰 Save Token | Token 节省器

> A guiding skill that teaches agents how to save tokens by avoiding duplicate context.
> 
> 指导 Agent 如何通过避免重复上下文来节省 Token 的技能。

## ⚠️ Important Clarification | 重要说明

| Clarification | 说明 |
|---------------|------|
| **This is a guiding skill** | Skill itself cannot modify agent's runtime context |
| **Agent performs the action** | Agent follows the guidance to optimize context |
| **这是一个指导性 Skill** | Skill 本身不能修改 Agent 的运行时上下文 |
| **由 Agent 执行操作** | Agent 遵循指导来优化上下文 |

## 🎯 When to Use | 使用时机

**Agent 自动触发条件**（满足任一即应调用）：
- 用户提到 "token" / "成本" / "省钱" / "费用"
- 对话已超过 10 轮
- 同一文件被读取超过 1 次
- 任务前上下文超过 5000 字符

| Situation | Action | 场景 | 操作 |
|-----------|--------|------|------|
| User mentions "token" or "cost" | Apply save-token strategies | 用户提到 token 或成本 | 应用 save-token 策略 |
| Long conversation (>10 turns) | Summarize old context | 长对话（>10轮） | 摘要旧上下文 |
| File read multiple times | Reference previous read, don't re-read | 文件被多次读取 | 引用之前的读取，不重复读取 |
| Repeated error messages | Summarize error pattern, don't repeat full error | 重复错误消息 | 摘要错误模式，不重复完整错误 |

## 📋 Token-Saving Strategies | 节省 Token 策略

### Strategy 1: Summarize Instead of Re-sending | 策略1：摘要代替重发

**When**: Old conversation context is no longer directly relevant
**当**：旧对话上下文不再直接相关时

**Do**:
- Summarize key points from earlier conversation
- Replace full history with concise summary
- Keep only the most relevant recent messages

**做法**：
- 摘要早期对话的关键点
- 用简洁摘要替换完整历史
- 只保留最相关的最近消息

**Example**:
```
❌ Bad: Re-sending 50 turns of conversation (10,000+ tokens)
✅ Good: "Previous context: User was analyzing stock investment strategies. 
   Key decisions made: prioritize low P/E, check cash flow. 
   Now focusing on: specific company analysis."
```

### Strategy 2: Reference Instead of Repeat | 策略2：引用代替重复

**When**: Same file/content needs to be referenced again
**当**：需要再次引用同一文件/内容时

**Do**:
- Don't re-read the entire file
- Reference the key information already extracted
- Only read new sections if needed

**做法**：
- 不要重新读取整个文件
- 引用已提取的关键信息
- 仅在需要时读取新部分

**Example**:
```
❌ Bad: Reading the same 200KB file again
✅ Good: "As we found earlier in the file, the revenue is $50M..."
```

### Strategy 3: De-duplicate Identical Blocks | 策略3：去重相同块

**When**: Identical text appears multiple times in context
**当**：相同文本在上下文中多次出现时

**Do**:
- Identify identical blocks (≥100 characters)
- Keep only the first occurrence
- Note what was removed

**做法**：
- 识别相同块（≥100字符）
- 只保留首次出现
- 记录删除了什么

**Example**:
```
❌ Bad: Same error message appears 5 times (500 chars × 5 = 2500 chars)
✅ Good: "[Error message appeared 5 times, showing once]: Connection timeout..."
```

### Strategy 4: Compress Verbose Output | 策略4：压缩冗长输出

**When**: Tool output or file content is very long
**当**：工具输出或文件内容很长时

**Do**:
- Extract only relevant parts
- Summarize the rest
- Note the source for reference

**做法**：
- 只提取相关部分
- 摘要其余部分
- 记录来源以供参考

**Example**:
```
❌ Bad: Including full 1000-line log file
✅ Good: "Log file (1000 lines): Key errors on lines 45, 78, 234. 
   Pattern: Connection drops every 5 minutes. Full log available if needed."
```

## 🔄 Workflow | 工作流程

```
1. Agent receives task
2. Agent checks context size and duplicate content
3. If context > threshold OR duplicates found:
   a. Apply appropriate strategy from above
   b. Report token savings to user
4. Proceed with optimized context
```

## 📊 Reporting Format | 报告格式

When applying token-saving strategies, inform the user:

```
💡 Token Optimization Applied:
- Strategy: [Strategy Name]
- Context before: X tokens
- Context after: Y tokens  
- Saved: Z tokens (P%)
```

## ⚠️ What This Skill Cannot Do | 此 Skill 不能做的事

| Cannot Do | Reason | 不能做 | 原因 |
|-----------|--------|--------|------|
| Directly modify context | Skill is guidance, not execution | 直接修改上下文 | Skill 是指导，不是执行 |
| Automatically delete content | Agent must decide what to keep | 自动删除内容 | Agent 必须决定保留什么 |
| Guarantee exact savings | Depends on implementation | 保证精确节省量 | 取决于实现方式 |

## ✅ What This Skill Does | 此 Skill 能做的事

| Does | Description | 能做 | 描述 |
|------|-------------|------|------|
| Provide strategies | Teaches how to save tokens | 提供策略 | 教如何节省 Token |
| Identify opportunities | Helps recognize when to apply | 识别机会 | 帮助识别何时应用 |
| Guide implementation | Shows best practices | 指导实现 | 展示最佳实践 |

## 📝 Version | 版本

- Version: 1.1.0
- Updated: 2026-03-12
- Change: Clarified that this is a guiding skill, not an execution script
