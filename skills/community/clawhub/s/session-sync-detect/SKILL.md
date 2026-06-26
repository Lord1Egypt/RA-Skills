# session-sync-detect Skill

## 跨会话同步检测与询问

当用户谈到当前 session 没有的事情时，自动检测并询问是否进行跨会话同步。

## ⚠️ 安全设计原则

本技能采用**"检测 + 询问 + 执行"**模式：

- ✅ 自动检测 - 分析用户话语，判断是否涉及跨 session 内容
- ✅ 用户明确确认 - 必须得到用户允许后才执行同步
- ✅ 透明操作 - 所有文件读写都会向用户报告
- ✅ 隐私保护 - 敏感信息不写入共享 memory
- ✅ 最小权限 - 仅执行用户确认后的操作

## 触发机制

### 🎯 自动检测 + 手动确认

当检测到用户话语可能涉及当前 session 没有的内容时，**先询问用户**：

**检测信号：**
- "昨天的那个事..."（当前 session 没有昨天的上下文）
- "蒙老师的报告时间你记得吧？"（当前 session 没提到过）
- "微信里我发给你的消息..."（当前 session 是飞书）
- "之前说的那个提醒..."（当前 session 没有相关记录）
- "你查一下我说的..."（暗示需要查找）

**询问格式：**
```
🔍 检测到您可能在谈论其他 session 的内容：

"{{用户话语}}"

我可以在以下范围查找：
- ✅ 记忆文件 (memory/YYYY-MM-DD.md, MEMORY.md)
- ✅ 最近活跃的 session (过去 24 小时)

是否需要我帮您同步这些信息？
```

**用户回复：**
- ✅ "是" / "好的" / "查一下" → 执行同步
- ❌ "不用" / "跳过" / "不是那个" → 不执行
- 🤔 "先看看记忆文件" → 只查 memory 文件

## 核心机制

### 1. 检测逻辑

分析用户话语中的跨 session 信号：

**时间引用：**
- "昨天" / "上周" / "之前" - 当前 session 没有对应时间线
- "刚才在微信上说的那个" - 跨平台引用

**平台引用：**
- "微信里" / "飞书里" / "邮件里" - 当前不是该平台
- "群里发的消息" - 当前是私聊

**内容引用：**
- "那个报告" / "你说的" / "我说的" - 当前 session 没有上下文
- "蒙老师" / "张三" - 可能是其他 session 提到的人

**行为模式：**
- "帮我查一下" / "找找看" - 明确要求查找
- "你记得吧" / "你知道的" - 假设我有记忆

### 2. 快速扫描 (Quick Scan)

如果用户确认，先快速扫描 memory 文件：

```bash
# 列出最近活跃的 session
openclaw sessions list --activeMinutes 1440 --messageLimit 5

# 搜索 memory 文件
grep -r "关键词" ~/.openclaw/workspace/memory/
```

### 3. 历史读取 (History Fetch)

如果 memory 文件没有，读取相关 session 历史：

```javascript
sessions_history(sessionKey="session-uuid", limit=100, includeTools=true)
```

⚠️ **隐私提示：**
- 读取前会向用户确认目标 session
- 不会静默读取所有 session
- 读取结果仅用于响应用户当前请求

### 4. 记忆文件同步 (Memory File Sync)

所有 session 共享的记忆文件位置：

- `memory/YYYY-MM-DD.md` - 每日原始日志
- `MEMORY.md` - curated 长期记忆
- `memory/*.md` - 特殊主题记忆

⚠️ **隐私保护：**
- 写入前会提示用户潜在隐私风险
- 不会自动复制敏感信息（密码、API key 等）
- 用户可要求 redact 敏感内容后再写入

### 5. 智能提取 (Smart Extraction)

从 session 历史中提取关键信息：

- 决策点 (Decisions)
- 待办事项 (Open TODOs)
- 用户偏好 (User Preferences)
- 重要事件 (Significant Events)

⚠️ **提取规则：**
- 仅提取与用户请求相关的内容
- 不会提取私聊、敏感对话
- 提取结果会向用户展示并确认后再写入共享 memory

## 工作流程

### Step 1: 检测信号

分析用户话语，判断是否需要询问：

```
用户："蒙老师的报告时间你记得吧？"
分析：
- 当前 session 没有"蒙老师"相关上下文
- 用户假设我有记忆
- 可能是其他 session 或平台的内容
→ 触发询问
```

### Step 2: 询问确认

向用户展示检测到的信号，询问是否执行同步：

```
🔍 检测到您可能在谈论其他 session 的内容：

"蒙老师的报告时间你记得吧？"

我可以在以下范围查找：
- ✅ 记忆文件 (memory/YYYY-MM-DD.md, MEMORY.md)
- ✅ 最近活跃的 session (过去 24 小时)

是否需要我帮您同步这些信息？
```

### Step 3: 执行检索

用户确认后，按优先级执行：

**优先顺序：**
1. 先查 memory 文件 - 最快，跨 session 共享
   ```bash
   grep -r "蒙老师" ~/.openclaw/workspace/memory/
   ```

2. 再查 session 历史 - 完整但较慢
   ```javascript
   sessions_history(sessionKey="xxx", limit=200)
   ```

3. 最后查 session 列表 - 元数据快速扫描
   ```javascript
   sessions_list(activeMinutes=1440, messageLimit=10)
   ```

### Step 4: 展示发现

向用户展示找到的信息：

```
## 跨 Session 记忆检索结果

**搜索范围：** 记忆文件 + 最近活跃 session
**搜索主题：** 蒙老师 报告时间

### 发现

#### 1. memory/2026-03-26.md
- **时间：** 2026-03-26 14:30
- **内容：** 蒙老师报告定于 3 月 28 日 15:00，地点 A 栋 301
- **来源：** `memory/2026-03-26.md:15-20`

#### 2. Session: 飞书 direct
- **时间：** 2026-03-26 11:10
- **内容：** 确认报告主题和 PPT 准备进度
- **来源：** `sessions/xxx.jsonl`
```

### Step 5: 同步记忆

询问用户是否将发现写入共享 memory：

```
是否将以上发现写入 memory 文件？
- ✅ 写入 memory/2026-03-27.md（今日日志）
- ⏳ 考虑是否写入 MEMORY.md（长期记忆）

用户确认后执行写入。
```

## 输出格式

### 询问格式

```
🔍 检测到您可能在谈论其他 session 的内容：

"{{用户话语}}"

我可以在以下范围查找：
- ✅ 记忆文件 (memory/YYYY-MM-DD.md, MEMORY.md)
- ✅ 最近活跃的 session (过去 24 小时)

是否需要我帮您同步这些信息？
```

### 检索结果

```
## 跨 Session 记忆检索结果

**搜索范围：** [session 列表或时间范围]
**搜索主题：** [关键词或主题]

### 发现

#### 1. [Session Name/Channel]
- **时间：** 2026-03-27 11:10
- **内容：** [关键信息摘要]
- **来源：** `memory/2026-03-27.md:15-20`

#### 2. [Session Name/Channel]
- **时间：** 2026-03-26 14:30
- **内容：** [关键信息摘要]
- **来源：** `sessions/xxx.jsonl`
```

### 已同步

```
### 已同步到
- ✅ `memory/2026-03-27.md` - 新增检索记录
- ⏳ `MEMORY.md` - [待决定是否纳入]
```

## 最佳实践

- **检测要敏感** - 宁可多问，不要漏掉
- **询问要清晰** - 告诉用户要查什么、在哪查
- **检索要高效** - 先查 memory，再查 session
- **展示要简洁** - 只展示与用户请求相关的内容
- **同步要确认** - 写入前必须得到用户允许
- **隐私要保护** - 敏感信息不写入共享 memory

## 工具调用示例

```javascript
// 1. 检测用户话语（在 SKILL 运行时分析）
// 分析用户话语中的跨 session 信号

// 2. 列出活跃 session
sessions_list(activeMinutes=1440, messageLimit=5)

// 3. 读取特定 session 历史
sessions_history(sessionKey="747d0e66-55cf-4be4-bfe8-41988a1d0509", limit=100)

// 4. 搜索 memory 文件
exec(command="grep -r '蒙老师' ~/.openclaw/workspace/memory/")

// 5. 写入新的记忆（用户确认后）
write(file="memory/2026-03-27.md", content="...")
```

## 注意事项

- ⚠️ 检测信号要准确，避免频繁询问打扰用户
- ⚠️ 每个 session 的对话历史是隔离的，只有 memory 文件是共享的
- ⚠️ 读取 session 历史会消耗 tokens，控制 limit 参数
- ⚠️ 不要将敏感信息（密码、密钥）写入共享 memory 文件
- ⚠️ 跨 session 检索后，记得向用户报告发现
- ⚠️ 询问后必须等待用户确认，不能静默执行
- ⚠️ 所有文件读写都必须向用户报告

## 技术组件

- `sessions_list` - 列出活跃 session
- `sessions_history` - 读取 session 历史
- `exec` - 搜索 memory 文件
- `read/write/edit` - 操作 memory 文件

## 版本历史

- v0.1.0 (2026-03-27) - 初始版本
  - 检测用户话语中的跨 session 信号
  - 询问用户是否执行同步
  - 支持 memory 文件和 session 历史检索
  - 用户确认后写入 memory 文件
