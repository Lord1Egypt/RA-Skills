# Smart Workspace 📁 / 智能项目文件组织助手

[English](#english) | [中文](#中文)

---

## English

### What is it?

Smart Workspace Organizer helps AI Agents automatically manage files and keep their workspace clean.

**Without it:** Agent may dump all files in one place, getting messy.

**With it:** Agent remembers your project folders and automatically categorizes new tasks.

---

### Installation

#### Option 1: GitHub (Recommended)

```bash
openclaw skills install https://github.com/yaoweizhang/smart-workspace
```

#### Option 2: ClawHub

```bash
# Login first (if needed)
clawhub login
openclaw skills install smart-workspace
```

---

### First-Time Setup

> **Important!**
>
> On first load, the skill will **automatically scan existing folders** in your workspace and generate `PROJECT-HISTORY.md`. No manual action needed.

**Auto-scan logic:**
1. Read all folders in workspace root
2. Filter out system folders (`.git`, `.openclaw`, `.learnings`, etc.)
3. Create entries for each real project in `PROJECT-HISTORY.md`
4. If `PROJECT-HISTORY.md` already exists, skip initialization

```
Scan workspace/
    ↓
Discover ./articles/, ./data-science-tutorial/, etc.
    ↓
Auto-generate PROJECT-HISTORY.md entries
    ↓
Continue to main workflow
```

---### First-Time Use / 首次使用

**方式一（推荐）:** 帮我整理一下 workspace 的文件，按项目分类放到不同文件夹，然后让 smart-workspace 记录。

**方式二:** 用 smart-workspace 整理和记录文件。

**Way 1 (Recommended):** Help me organize the files in my workspace — put each project's files into its own folder — then use smart-workspace to record them.

**Way 2:** Use smart-workspace to organize and record the files.



### How It Works

1. **First Load**: Auto-scan existing folders → Generate `PROJECT-HISTORY.md`
2. **Understand**: Agent analyzes your task and extracts 2-3 keywords
3. **Match**:
   - **Match found** → Use existing folder directly (auto update `last_used`)
   - **No match** → Auto-create new project folder
   - **Multiple matches** → Use first one and notify user
4. **Done**: Agent tells you what was done

---

### You Just Say

| You say | Agent automatically |
|---------|-------------------|
| "Analyze football data" | → Categorize to football project |
| "Do battery test" | → Categorize to battery project |
| "Shooting prediction" | → Categorize to shooting project |
| "New project: develop XX" | → Auto-create new folder |

---

### Supported Keywords

| Keywords | Project |
|----------|---------|
| football, prediction, verify | Football prediction |
| battery | Battery analysis |
| shooting | Shooting prediction |
| other | Auto-create new project |

---

### FAQ

**Q: Do I need to configure anything?**
A: No. It auto-scans your workspace on first load.

**Q: Will it delete my files?**
A: No. It only updates the record file, never deletes actual files.

**Q: How to add new projects?**
A: Just tell Agent "I want to start a new project: xxx", and Agent will auto-create it.

**Q: Can multiple Agents share it?**
A: Each Agent has its own project history, they don't affect each other.

---

## 中文

### 是什么？

智能项目文件组织助手。帮助 AI Agent 自动管理文件，保持工作区整洁。

**没有它：** Agent 可能每次都把文件堆在同一个地方，混乱不堪。

**有了它：** Agent 会记住你每个项目的文件夹，新任务自动归类。

---

### 安装

#### 方式1：GitHub 安装（推荐）

```bash
openclaw skills install https://github.com/yaoweizhang/smart-workspace
```

#### 方式2：ClawHub 安装

```bash
# 需要先登录（如果需要）
clawhub login
openclaw skills install smart-workspace
```

---

### 首次安装

> **重要！**
>
> 首次加载技能时，会**自动扫描 workspace 现有文件夹**，生成 `PROJECT-HISTORY.md`。无需手动操作。

---

### 工作原理

1. **首次加载**：自动扫描现有文件夹 → 生成 `PROJECT-HISTORY.md`
2. **理解任务**：Agent 分析任务，提取2-3个关键词
3. **智能匹配**：
   - **匹配成功** → 直接使用已有文件夹（自动更新 last_used）
   - **无匹配** → 自动创建新项目文件夹
   - **多个匹配** → 使用第一个并告知用户
4. **执行完成**：Agent 告知处理结果

---

### 你只需说

| 你说 | Agent 自动 |
|------|-----------|
| "分析足球数据" | → 归类到足球预测项目 |
| "做电池测试" | → 归类到电池分析项目 |
| "射击预测" | → 归类到射击预测项目 |
| "新项目：开发xx" | → 自动创建新文件夹 |

---

### 支持的关键词

| 关键词 | 项目 |
|--------|------|
| 足球、预测、验证 | 足球预测相关 |
| 电池 | 电池分析相关 |
| 射击 | 射击预测相关 |
| 其他 | 自动创建新项目 |

---

### 常见问题

**问：需要我配置什么吗？**
答：不需要。首次加载时自动扫描 workspace。

**问：会删我的文件吗？**
答：不会。只会更新记录文件，不会删除任何实际文件。

**问：怎么添加新项目？**
答：告诉 Agent "我要做一个新项目 xxx"，Agent 会自动创建。

**问：多个 Agent 共用吗？**
答：每个 Agent 有独立的项目历史，互不影响。

---

## Changelog / 更新日志

### v1.1.0
- **EN:** Auto-scan existing folders on first install, fully automatic flow, direct use on match
- **CN:** 首次安装自动扫描现有文件夹，全自动流程，匹配成功直接使用

### v1.0.0
- **EN:** Support Chinese keyword mapping, auto create and record projects
- **CN:** 支持中文关键词匹配，自动创建和记录项目
