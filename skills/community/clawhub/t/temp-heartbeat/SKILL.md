# Temp Heartbeat - 临时心跳任务

> 版本：v1.0 | 作者：Spark | 创建时间：2026-04-04

---

## 🎯 Skill 定位

**临时心跳任务管理器** - 允许用户设置一次性临时心跳任务，在指定时间后执行，执行完成后自动删除

**核心使命：** 提供灵活的心跳任务机制，避免 HEARTBEAT.md 永久化配置，适合临时提醒、定时任务等场景

---

## ⚡ 触发规则

### 主触发词
- `/heart` - 标准触发
- `临时心跳` - 中文触发
- `temp heartbeat` - 英文触发
- `定时任务` - 定时触发

### 场景触发
- 临时提醒（会议、约会）
- 定时任务（检查、备份）
- 一次性心跳（不需要重复执行）

### 不触发场景
- 简单查询（天气、时间等）
- 已有 HEARTBEAT.md 永久任务

---

## 🏗️ 核心工作流程

### Step 1: 任务解析 (Task Analysis)

**目标：** 理解用户的临时心跳需求

**检查清单：**
- [ ] 任务类型识别（提醒/检查/执行）
- [ ] 执行时间提取（多久后/具体时间点）
- [ ] 任务内容提取（要做什么）
- [ ] 重复性确认（一次性/重复）

**输出：**
```markdown
## 📋 临时心跳任务

**任务类型：** [提醒/检查/执行]
**执行时间：** [X 分钟后/具体时间点]
**任务内容：** [一句话描述]
**重复性：** 一次性（执行后删除）
```

---

### Step 2: 时间解析 (Time Parsing)

**支持的时间格式：**

| 格式 | 示例 | 解析结果 |
|------|------|----------|
| **相对时间** | `10 分钟后` | 当前时间 + 10 分钟 |
| **相对时间** | `1 小时后` | 当前时间 + 1 小时 |
| **相对时间** | `30 分钟后` | 当前时间 + 30 分钟 |
| **相对时间** | `2 天后` | 当前时间 + 2 天 |
| **绝对时间** | `今晚 8 点` | 今天 20:00 |
| **绝对时间** | `明天上午 10 点` | 明天 10:00 |
| **绝对时间** | `2026-04-05 15:00` | 指定日期时间 |

**时间单位支持：**
- 分钟 (minutes)
- 小时 (hours)
- 天 (days)

**输出：**
```markdown
## ⏰ 执行时间

**用户输入：** [原始时间描述]
**解析结果：** [ISO 8601 格式]
**距离现在：** [X 分钟/小时/天]
**执行时间：** [YYYY-MM-DD HH:mm:ss]
```

---

### Step 3: 任务创建 (Task Creation)

**目标：** 创建临时心跳任务文件

**文件位置：**
```
memory/temp-heartbeat-{timestamp}.md
```

**文件内容模板：**
```markdown
# Temp Heartbeat Task

> ⚠️ 此任务为临时心跳，执行后自动删除

## Task Info

- **Created At:** {创建时间}
- **Execute At:** {执行时间}
- **Task ID:** {唯一 ID}
- **Status:** pending

## Task Content

{任务内容}

## Execution

- [ ] 任务已执行
- [ ] 结果已记录
- [ ] 文件已删除
```

**输出：**
```markdown
## ✅ 临时心跳任务已创建

**任务 ID:** `{task_id}`
**执行时间:** {执行时间}
**任务内容:** {任务内容}

**提示:**
- 任务将在指定时间自动执行
- 执行完成后自动删除
- 输入 `/heart list` 查看所有临时心跳
```

---

### Step 4: 任务管理 (Task Management)

**支持的管理命令：**

| 命令 | 功能 | 示例 |
|------|------|------|
| `/heart` | 创建临时心跳 | `/heart 10 分钟后提醒我开会` |
| `/heart list` | 查看所有临时心跳 | 列出所有待执行任务 |
| `/heart cancel {ID}` | 取消指定心跳 | `/heart cancel task_123` |
| `/heart cancel all` | 取消所有心跳 | 清空所有临时任务 |

**输出示例（list）：**
```markdown
## 📋 临时心跳任务列表

| 任务 ID | 执行时间 | 任务内容 | 状态 |
|--------|----------|----------|------|
| task_123 | 2026-04-04 10:30 | 提醒开会 | 待执行 |
| task_456 | 2026-04-04 15:00 | 检查 API 状态 | 待执行 |

**共 X 个任务**

**管理命令:**
- 取消单个：`/heart cancel {任务 ID}`
- 取消所有：`/heart cancel all`
```

---

### Step 5: 任务执行 (Task Execution)

**触发条件：**
- 当前时间 >= 执行时间
- 任务状态 = pending

**执行流程：**
1. 读取任务文件
2. 执行任务内容
3. 记录执行结果
4. 删除任务文件

**输出：**
```markdown
## ✅ 临时心跳任务已执行

**任务 ID:** `{task_id}`
**执行时间:** {实际执行时间}
**任务内容:** {任务内容}

**执行结果:**
{任务执行的具体内容}

---
*此临时心跳任务已完成并删除*
```

---

## 📝 完整输出模板

### 创建任务

```markdown
## ✅ 临时心跳任务已创建

**任务 ID:** `task_{timestamp}_{random}`
**执行时间:** {YYYY-MM-DD HH:mm:ss}
**距离现在:** {X 分钟/小时}
**任务内容:** {任务描述}

**提示:**
- ✅ 任务已保存到 `memory/temp-heartbeat-{timestamp}.md`
- ⏰ 将在指定时间自动执行
- 🗑️ 执行完成后自动删除
- 📋 输入 `/heart list` 查看所有任务

**取消任务:**
- 取消单个：`/heart cancel {任务 ID}`
- 取消所有：`/heart cancel all`
```

### 查看任务列表

```markdown
## 📋 临时心跳任务列表

| 任务 ID | 执行时间 | 剩余时间 | 任务内容 | 操作 |
|--------|----------|----------|----------|------|
| task_123 | 10:30 | 25 分钟 | 提醒开会 | `/heart cancel task_123` |
| task_456 | 15:00 | 5 小时 | 检查 API | `/heart cancel task_456` |

**共 {X} 个任务**

**下次执行:** {最近的任务时间}
```

### 执行任务

```markdown
## ⏰ 临时心跳任务触发

**任务 ID:** `task_123`
**计划执行:** 10:30
**实际执行:** 10:30:05

## 📋 任务内容

{任务描述}

## ✅ 执行结果

{执行的具体内容}

---
*临时心跳任务已完成，文件已删除*
```

---

## 🔧 技术实现

### 时间解析函数

```typescript
function parseTime(timeStr: string): Date | null {
  // 相对时间解析
  const relativePatterns = [
    /(\d+)\s*分钟后?/,
    /(\d+)\s*小时后?/,
    /(\d+)\s*天后?/,
    /in\s+(\d+)\s*minutes?/,
    /in\s+(\d+)\s*hours?/,
    /in\s+(\d+)\s*days?/,
  ];
  
  for (const pattern of relativePatterns) {
    const match = timeStr.match(pattern);
    if (match) {
      const value = parseInt(match[1]);
      const now = new Date();
      
      if (pattern.toString().includes('分钟')) {
        now.setMinutes(now.getMinutes() + value);
      } else if (pattern.toString().includes('小时')) {
        now.setHours(now.getHours() + value);
      } else if (pattern.toString().includes('天')) {
        now.setDate(now.getDate() + value);
      }
      
      return now;
    }
  }
  
  // 绝对时间解析
  const absolutePatterns = [
    /今晚\s*(\d+)[点時]/,
    /明天\s*(\d+)[点時]/,
    /(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})/,
  ];
  
  for (const pattern of absolutePatterns) {
    const match = timeStr.match(pattern);
    if (match) {
      // 解析绝对时间
      // ...
    }
  }
  
  return null;
}
```

### 任务创建函数

```typescript
async function createTempHeartbeat(
  executeAt: Date,
  content: string
): Promise<TaskInfo> {
  const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
  const filePath = `memory/temp-heartbeat-${Date.now()}.md`;
  
  const taskContent = `# Temp Heartbeat Task

> ⚠️ 此任务为临时心跳，执行后自动删除

## Task Info

- **Created At:** ${new Date().toISOString()}
- **Execute At:** ${executeAt.toISOString()}
- **Task ID:** ${taskId}
- **Status:** pending

## Task Content

${content}

## Execution

- [ ] 任务已执行
- [ ] 结果已记录
- [ ] 文件已删除
`;
  
  await writeFile(filePath, taskContent);
  
  return {
    id: taskId,
    executeAt,
    content,
    filePath,
    status: 'pending',
  };
}
```

### 任务检查函数

```typescript
async function checkAndExecuteTasks(): Promise<void> {
  const tempHeartbeatFiles = await glob('memory/temp-heartbeat-*.md');
  const now = new Date();
  
  for (const file of tempHeartbeatFiles) {
    const content = await readFile(file, 'utf-8');
    const executeAtMatch = content.match(/Execute At:\s*(.+)/);
    const statusMatch = content.match(/Status:\s*(.+)/);
    
    if (!executeAtMatch || statusMatch?.[1] !== 'pending') {
      continue;
    }
    
    const executeAt = new Date(executeAtMatch[1]);
    
    if (now >= executeAt) {
      // 执行任务
      await executeTask(file, content);
      
      // 删除文件
      await unlink(file);
    }
  }
}
```

### 任务列表函数

```typescript
async function listTempHeartbeats(): Promise<TaskInfo[]> {
  const tempHeartbeatFiles = await glob('memory/temp-heartbeat-*.md');
  const tasks: TaskInfo[] = [];
  
  for (const file of tempHeartbeatFiles) {
    const content = await readFile(file, 'utf-8');
    
    const taskIdMatch = content.match(/Task ID:\s*(.+)/);
    const executeAtMatch = content.match(/Execute At:\s*(.+)/);
    const contentMatch = content.match(/## Task Content\n\n(.+)/s);
    
    if (taskIdMatch && executeAtMatch && contentMatch) {
      tasks.push({
        id: taskIdMatch[1].trim(),
        executeAt: new Date(executeAtMatch[1].trim()),
        content: contentMatch[1].trim(),
        filePath: file,
        status: 'pending',
      });
    }
  }
  
  // 按执行时间排序
  return tasks.sort((a, b) => a.executeAt.getTime() - b.executeAt.getTime());
}
```

---

## 💡 使用示例

### 示例 1：临时提醒

**用户输入：**
```
/heart 10 分钟后提醒我开会
```

**输出：**
```markdown
## ✅ 临时心跳任务已创建

**任务 ID:** `task_1775245200000_abc123`
**执行时间:** 2026-04-04 10:40:00
**距离现在:** 10 分钟
**任务内容:** 提醒我开会

**提示:**
- ✅ 任务已保存到 `memory/temp-heartbeat-1775245200000.md`
- ⏰ 将在 10 分钟后自动执行
- 🗑️ 执行完成后自动删除
- 📋 输入 `/heart list` 查看所有任务

**取消任务:**
- 取消单个：`/heart cancel task_1775245200000_abc123`
- 取消所有：`/heart cancel all`
```

**10 分钟后自动执行：**
```markdown
## ⏰ 临时心跳任务触发

**任务 ID:** `task_1775245200000_abc123`
**任务内容:** 提醒我开会

## ✅ 执行结果

🔔 提醒：您有一个会议要参加！

---
*临时心跳任务已完成，文件已删除*
```

---

### 示例 2：定时检查

**用户输入：**
```
/heart 1 小时后检查 GitHub API 限流状态
```

**输出：**
```markdown
## ✅ 临时心跳任务已创建

**任务 ID:** `task_1775248800000_def456`
**执行时间:** 2026-04-04 11:40:00
**距离现在:** 1 小时
**任务内容:** 检查 GitHub API 限流状态

...
```

**1 小时后自动执行：**
```markdown
## ⏰ 临时心跳任务触发

**任务内容:** 检查 GitHub API 限流状态

## ✅ 执行结果

**GitHub API 状态:**
- 剩余：58/60
- 重置时间：2026-04-04 12:00

---
*临时心跳任务已完成，文件已删除*
```

---

### 示例 3：查看任务列表

**用户输入：**
```
/heart list
```

**输出：**
```markdown
## 📋 临时心跳任务列表

| 任务 ID | 执行时间 | 剩余时间 | 任务内容 | 操作 |
|--------|----------|----------|----------|------|
| task_abc123 | 10:40 | 10 分钟 | 提醒开会 | `/heart cancel task_abc123` |
| task_def456 | 11:40 | 1 小时 | 检查 API | `/heart cancel task_def456` |
| task_ghi789 | 明天 09:00 | 14 小时 | 每日检查 | `/heart cancel task_ghi789` |

**共 3 个任务**

**下次执行:** 10 分钟后 (task_abc123)
```

---

### 示例 4：取消任务

**用户输入：**
```
/heart cancel task_abc123
```

**输出：**
```markdown
## ✅ 临时心跳任务已取消

**任务 ID:** `task_abc123`
**原计划执行:** 2026-04-04 10:40:00
**任务内容:** 提醒开会

**操作:**
- ✅ 任务文件已删除
- ✅ 任务已从列表中移除
```

---

### 示例 5：取消所有任务

**用户输入：**
```
/heart cancel all
```

**输出：**
```markdown
## ✅ 已取消所有临时心跳任务

**取消任务数:** 3 个

**取消列表:**
1. task_abc123 - 提醒开会
2. task_def456 - 检查 API
3. task_ghi789 - 每日检查

**操作:**
- ✅ 所有任务文件已删除
- ✅ 任务列表已清空
```

---

## ⚠️ 注意事项

### 1. 临时性

- ✅ 执行后自动删除
- ✅ 不会写入 HEARTBEAT.md
- ✅ 适合一次性任务

### 2. 时间限制

- 最小时间间隔：1 分钟
- 最大时间间隔：30 天
- 建议时间间隔：5 分钟 - 24 小时

### 3. 任务数量

- 单个用户最多：20 个临时心跳
- 超出时提示：请先取消部分任务

### 4. 执行时机

- 检查频率：每 30 秒检查一次
- 执行误差：< 1 分钟
- 超时处理：任务过期后自动删除

---

## 🚀 版本记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-04 | 初始版本，临时心跳管理 |

---

**Temp Heartbeat Skill 开发完成 · 让临时任务更灵活**
