# Session 回溯技能

## 概述

Session 回溯技能，用于从 OpenClaw 的会话历史中提取信息、管理记忆和回溯对话。

## 功能

### 1. 提取关键信息写入 memory/YYYY-MM-DD.md

将 session 中的关键信息提取并保存到记忆文件中。

**使用方式：**
- 调用 `write` 工具将内容写入 `memory/YYYY-MM-DD.md` 文件
- 日期格式：当天日期，如 `memory/2026-03-05.md`

**提取内容建议：**
- 对话中的重要决策
- 关键信息点
- 待办事项
- 学习到的关于主人的信息

**示例：**
```markdown
# 2026-03-05 记忆

## 重要信息
- 主人想要了解如何回溯 session
- 主人让我发布了一个飞书文档技能到 ClawHub

## 待办
- [ ] 创建 session 回溯 skill

## 对话摘要
今天主人问了关于 session 的问题...
```

### 2. 查询关键词在 session 中的出现次数/上下文

**工具：**
- 使用 `sessions_list` 工具列出所有 session
- 使用 `sessions_history` 工具获取特定 session 的历史
- 使用 `read` 工具直接读取 JSONL 文件

**方法：**

#### 方法一：使用 sessions_list
```bash
# 列出最近所有 session
sessions_list
```

#### 方法二：使用 sessions_history
```bash
# 获取特定 session 的历史
sessions_history --sessionKey "agent:lin_xiaoman:feishu:direct:ou_xxx"
```

#### 方法三：直接读取 JSONL 文件
```bash
# 读取 session 文件
# 路径格式：~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl

# 示例：查找关键词 "外卖"
# 使用 read 工具读取文件，然后分析内容
```

**查找关键词的上下文：**
1. 使用 `sessions_list` 获取所有 session 的基本信息
2. 根据 sessionKey 确定目标 session
3. 使用 `sessions_history` 获取完整历史
4. 在内容中搜索关键词并记录上下文

### 3. 回溯某段 session 并添加到当前对话

**方式一：使用 sessions_history 工具**

1. 找到目标 session 的 sessionKey
2. 使用 sessions_history 获取历史
3. 将需要回溯的内容通过对话方式告诉模型

**方式二：直接读取 JSONL 文件**

1. 确定 sessionId（可以从 sessions.json 或 sessions_list 获取）
2. 读取 JSONL 文件：
   ```
   ~/.openclaw/agents/lin_xiaoman/sessions/<sessionId>.jsonl
   ```
3. 提取需要的对话片段
4. 将内容告诉用户或添加到当前上下文

**重要提示：**
- 当前 session 的 sessionKey 格式：`agent:lin_xiaoman:feishu:direct:ou_2545d3b430b99a135bdab87d5a09b68a`
- 当前 session 的 sessionId：`3fefc0bb-b7e9-4736-b374-d1be9d12caec`
- JSONL 文件路径：`~/.openclaw/agents/lin_xiaoman/sessions/3fefc0bb-b7e9-4736-b374-d1be9d12caec.jsonl`

## Session 文件位置

- 索引文件：`~/.openclaw/agents/<agentId>/sessions/sessions.json`
- 对话记录：`~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`
- 被 reset 的记录：`~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl.reset.<时间戳>`
- 被删除的记录：`~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl.deleted.<时间戳>`

## 使用示例

### 示例 1：查找今天关于"外卖"的对话

1. 列出所有 session：
   ```
   sessions_list
   ```

2. 获取当前飞书会话的历史：
   ```
   sessions_history --sessionKey "agent:lin_xiaoman:feishu:direct:ou_2545d3b430b99a135bdab87d5a09b68a"
   ```

3. 分析内容，找到关于"外卖"的对话

### 示例 2：保存今天的重要对话到记忆

将今天的对话摘要写入 `memory/2026-03-05.md`

### 示例 3：回溯之前的某个 session

1. 列出所有 session：`sessions_list`
2. 找到目标 session 的 sessionKey
3. 使用 `sessions_history` 获取历史
4. 将需要的片段告诉用户

## 注意事项

- 使用完 `sessions_history` 后，需要在回复中告诉用户找到的内容
- JSONL 文件可以直接用 `read` 工具读取
- 被 reset 的 session 文件后缀包含 `.reset.`
- 被删除的 session 文件后缀包含 `.deleted.`
