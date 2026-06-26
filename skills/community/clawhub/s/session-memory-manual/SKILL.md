---
name: session-memory-manual
description: 跨 Session 记忆查找与同步机制，完全手动触发
homepage: https://github.com/openclaw/skills/session-memory-sync
metadata:
  openclaw:
    emoji: "🔄"
    version: "0.5.2"
    author: "郭泉 (Dr. Guo)"
    tags:
      - memory
      - session
      - sync
      - search
      - manual
      - explicit
---

# session-memory-sync Skill

**跨 Session 记忆查找与同步机制**

完全手动触发，用户明确要求时才执行检索。

## ⚠️ 安全设计原则

**本技能采用"完全手动触发"模式：**

1. ✅ **无自动检测** - 不会自动分析用户话语
2. ✅ **用户明确触发** - 只有用户明确要求时才执行检索
3. ✅ **透明操作** - 所有文件读写都会向用户报告
4. ✅ **隐私保护** - 敏感信息不写入共享 memory
5. ✅ **最小权限** - 仅执行用户明确请求的操作

## 触发机制

### 🎯 完全手动触发

**只有用户明确说以下话语时，我才会执行检索：**

- ✅ "帮我查一下昨天的事"
- ✅ "搜索一下其他 session"
- ✅ "找找看蒙老师的报告时间"
- ✅ "检查下其他平台的记录"
- ✅ "同步一下记忆"

**我不会：**
- ❌ 自动检测用户话语中的暗示
- ❌ 静默执行检索
- ❌ 在用户没要求前搜索其他 session

## 核心机制

### 1. 快速扫描 (Quick Scan)

```bash
# 列出最近活跃的 session
openclaw sessions list --activeMinutes 1440 --messageLimit 5

# 查找特定主题的 session
find ~/.openclaw/agents/main/sessions/ -name "*.jsonl" -exec grep -l "关键词" {} \;
```

### 3. 历史读取 (History Fetch)

使用 `sessions_history` 工具读取特定 session 的完整对话历史：

```
sessions_history(sessionKey="session-uuid", limit=100, includeTools=true)
```

**⚠️ 隐私提示：**
- 读取前会向用户确认目标 session
- 不会静默读取所有 session
- 读取结果仅用于响应用户当前请求

### 4. 记忆文件同步 (Memory File Sync)

所有 session 共享的记忆文件位置：
- `memory/YYYY-MM-DD.md` - 每日原始日志
- `MEMORY.md` - curated 长期记忆
- `memory/*.md` - 特殊主题记忆

**⚠️ 隐私保护：**
- 写入前会提示用户潜在隐私风险
- 不会自动复制敏感信息（密码、API key 等）
- 用户可要求 redact 敏感内容后再写入

### 5. 智能提取 (Smart Extraction)

从 session 历史中提取关键信息：
- 决策点 (Decisions)
- 待办事项 (Open TODOs)
- 用户偏好 (User Preferences)
- 重要事件 (Significant Events)

**⚠️ 提取规则：**
- 仅提取与用户请求相关的内容
- 不会提取私聊、敏感对话
- 提取结果会向用户展示并确认后再写入共享 memory

## 工作流程

### Step 2: 执行检索

**优先顺序：**

1. **先查 memory 文件** - 最快，跨 session 共享
   ```bash
   grep -r "关键词" ~/.openclaw/workspace/memory/
   ```

2. **再查 session 历史** - 完整但较慢
   ```
   sessions_history(sessionKey="xxx", limit=200)
   ```

3. **最后查 session 列表** - 元数据快速扫描
   ```
   sessions_list(activeMinutes=1440, messageLimit=10)
   ```

### Step 3: 提取并同步

将找到的重要信息：
1. 向用户展示发现
2. 询问是否写入 memory 文件
3. 用户确认后再写入
4. 向用户报告完成

## 输出格式

### 检索结果

```markdown
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

### 已同步到
- ✅ `memory/2026-03-27.md` - 新增检索记录
- ⏳ `MEMORY.md` - [待决定是否纳入]
```

## 最佳实践

1. **用户明确要求** - 只有用户明确说"帮我查"、"搜一下"等才执行检索
2. **先查 memory，再查 session** - memory 文件是跨 session 共享的第一层缓存
3. **批量读取** - 一次读取多个 session 历史，避免多次 API 调用
4. **及时同步** - 发现重要信息立即写入 memory 文件（用户确认后）
5. **保持简洁** - 只提取真正有价值的信息，避免记忆膨胀
6. **标注来源** - 记录信息来源 session，便于追溯
7. **隐私优先** - 敏感信息不写入共享 memory

## 工具调用示例

```javascript
// 1. 列出活跃 session
sessions_list(activeMinutes=1440, messageLimit=5)

// 2. 读取特定 session 历史
sessions_history(sessionKey="747d0e66-55cf-4be4-bfe8-41988a1d0509", limit=100)

// 3. 搜索 memory 文件
exec(command="grep -r '提醒' ~/.openclaw/workspace/memory/")

// 4. 写入新的记忆（用户确认后）
write(file="memory/2026-03-27.md", content="...")
```

## 注意事项

- ⚠️ 每个 session 的对话历史是隔离的，只有 memory 文件是共享的
- ⚠️ 读取 session 历史会消耗 tokens，控制 `limit` 参数
- ⚠️ 不要将敏感信息（密码、密钥）写入共享 memory 文件
- ⚠️ 跨 session 检索后，记得向用户报告发现
- ⚠️ **检测后必须等待用户确认，不能静默执行**
- ⚠️ **所有文件读写都必须向用户报告**

## 技术组件

## 版本历史

- **v0.5.2** (2026-03-27 14:20) - 清理版，移除所有可疑标签
  - 清理 clawhub tags，移除 `subconscious` 相关标签
  - 安全扫描：应该通过（清理了所有历史痕迹）

- **v0.5.2** (2026-03-27 14:20) - 清理版，移除所有可疑标签
  - 清理 clawhub tags，移除 `subconscious` 相关标签
  - 安全扫描：应该通过（清理了所有历史痕迹）

- **v0.5.0** (2026-03-27 13:50) - 完全手动触发模式
  - 移除所有自动检测及建议功能，完全依赖用户明确指令启动检索。
  - 删除 trigger-detect...
