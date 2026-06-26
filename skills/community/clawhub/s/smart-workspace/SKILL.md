---
name: smart-workspace
version: 1.1.0
description: 轻量化的项目文件管理技能。自动管理智能体工作区，根据任务关键词匹配项目历史，全自动执行，无需确认。避免文件混乱，大大增强智能体的项目管理能力。支持文件整理、文件夹管理、项目追踪、自动归档、工作区清理等功能。
description_en: Lightweight project file management skill. Automatically manages agent workspace, matches task keywords to project history, intelligently decides whether to use existing folders or create new ones. Prevents file chaos, greatly enhances agent project management capabilities.
keywords: [文件整理, 项目管理, workspace, folder, organize, project]
metadata:
  openclaw:
    emoji: "📁"
---

# Smart Workspace Organizer 📁 / 智能项目文件组织助手

Lightweight project file management skill. / 轻量化的项目文件管理技能。

---

## First-Time Setup / 首次安装（自动初始化）

> **EN: On first load, auto-scan existing folders and generate PROJECT-HISTORY.md!**
> **CN: 首次加载此技能时，自动扫描 workspace 现有文件夹，生成 PROJECT-HISTORY.md！**

### Auto-Scan Logic / 自动扫描逻辑

```
EN:
Scan workspace/ root directory
    ↓
Find ./articles/, ./data-science/, etc.
    ↓
Filter system folders: .git, .openclaw, memory, skills, .learnings
    ↓
Create PROJECT-HISTORY.md entry for each real project folder
    ↓
Continue to normal workflow

CN:
扫描 workspace/ 根目录
    ↓
发现 ./articles/、./data-science/ 等文件夹
    ↓
过滤系统文件夹：.git、.openclaw、memory、skills、.learnings 等
    ↓
为每个真实项目文件夹创建 PROJECT-HISTORY.md 条目
    ↓
继续执行主流程
```

```
IF ./PROJECT-HISTORY.md does not exist:
    1. Scan all folders in workspace root directory
    2. Filter out system folders (.git, .openclaw, memory, skills, .learnings, etc.)
    3. For each real project folder, create an entry in PROJECT-HISTORY.md
    4. Set created = today, last_used = today
    5. Continue to Step 2
ELSE:
    Skip initialization, continue to Step 2
```

---

## Core Features / 核心功能

| # | English | 中文 |
|---|---------|------|
| 1 | **Project History Search** - Match keywords in `PROJECT-HISTORY.md` | **项目历史搜索** - 在 `PROJECT-HISTORY.md` 中匹配关键词 |
| 2 | **Smart Folder Direct Use** - Directly use matched folder, auto update `last_used` | **智能文件夹推荐** - 直接使用匹配到的文件夹，自动更新 last_used |
| 3 | **New Project Creation** - Create new folders and record automatically | **新项目创建** - 自动创建新项目文件夹并记录 |
| 4 | **History Updates** - Keep project history current | **历史记录更新** - 保持项目历史最新 |

---

## Project History File / 项目历史文件

**Location / 位置:** `workspace/PROJECT-HISTORY.md`

### Format / 格式

```markdown
# Project History / 项目历史

## project-key
- name: Project Name / 项目名称
- path: ./project-folder/
- desc: Project description / 项目描述
- created: YYYY-MM-DD
- last_used: YYYY-MM-DD
```

### Format Fields / 格式字段

| Field / 字段 | Description / 说明 | Example / 示例 |
|--------------|-------------------|----------------|
| `## key` | Unique project identifier (level-2 heading) / 项目唯一标识 | football |
| `name` | Project name / 项目名称 | 足球预测 |
| `path` | Path relative to workspace / 相对于workspace的路径 | ./data_analyzer/ |
| `desc` | Project description (for keyword matching) / 项目描述 | 足球数据分析 |
| `created` | Creation date / 创建时间 | 2026-03-01 |
| `last_used` | Last used date / 最后使用时间 | 2026-04-18 |

### Path Resolution / 路径解析

```
EN:
Current workspace: ~/.openclaw/workspace-[agentname]/
Project history: ~/.openclaw/workspace-[agentname]/PROJECT-HISTORY.md
New project folder: ~/.openclaw/workspace-[agentname]/[projectname]/

CN:
当前 workspace: ~/.openclaw/workspace-[agentname]/
项目历史文件: ~/.openclaw/workspace-[agentname]/PROJECT-HISTORY.md
新项目文件夹: ~/.openclaw/workspace-[agentname]/[projectname]/
```

---

## Chinese Keyword Mapping / 中文关键词映射

| Chinese / 中文 | Matches / 匹配key |
|----------------|------------------|
| 足球 / football | football |
| 电池 / battery | battery |
| 射击 / shooting | shooting |
| 预测 / prediction | football |
| 验证 / verification | verify |

---

## Execution Flow / 执行流程（全自动）

### Step 1: Initialize (First Time Only) / 初始化（仅首次）

```
EN:
IF ./PROJECT-HISTORY.md does not exist:
    1. Scan workspace root directory for all folders
    2. Filter system folders (.git, .openclaw, memory, skills, .learnings, etc.)
    3. Create initial entries for each real project
    4. Continue to Step 2
ELSE:
    Skip, continue to Step 2

CN:
如果 ./PROJECT-HISTORY.md 不存在：
    1. 扫描 workspace 根目录所有文件夹
    2. 过滤系统文件夹（.git、.openclaw、memory、skills、.learnings 等）
    3. 为每个真实项目创建初始条目
    4. 继续 Step 2
否则：
    跳过初始化，继续 Step 2
```

### Step 2: Understand Task / 理解任务

```
EN: Analyze user's task, extract 2-3 keywords, determine project type
CN: 分析用户任务，提取2-3个关键词，判断属于哪类项目
```

### Step 3: Search & Match / 搜索匹配

```
EN:
Read PROJECT-HISTORY.md
    ↓
Match rules (priority order):
    1. key exact match → Direct use
    2. name/desc contains keyword → Direct use
    3. Chinese keyword mapping hit → Direct use
    4. No match → Auto-create new project
    5. Multiple matches → Use first one, notify user

CN:
读取 PROJECT-HISTORY.md
    ↓
匹配规则（优先级顺序）：
    1. key 完全匹配 → 直接使用
    2. name/desc 包含关键词 → 直接使用
    3. 中文关键词映射命中 → 直接使用
    4. 无匹配 → 自动创建新项目
    5. 多个匹配 → 使用第一个，并向用户说明
```

### Step 4: Execute & Record / 执行与记录

```
EN:
【Existing Project】
    1. Create ./[project]/ folder (if not exists)
    2. Update PROJECT-HISTORY.md: last_used = today
    3. Reply: "Task organized to [project] (last_used: today)"

【New Project】
    1. Create ./[project-name]/ folder
       - If folder exists, auto-add suffix _1, _2, etc.
    2. Append new entry to PROJECT-HISTORY.md
    3. Reply: "Created new project [project-name], files will be organized here"

CN:
【已有项目】
    1. 创建 ./[project]/ 文件夹（如不存在）
    2. 更新 PROJECT-HISTORY.md：last_used = 今天日期
    3. 回复："已将此任务整理到 [项目名]（last_used: 今天）"

【新项目】
    1. 创建 ./[project-name]/ 文件夹
       - 如文件夹已存在，自动追加 _1, _2 后缀
    2. 在 PROJECT-HISTORY.md 追加新条目
    3. 回复："已创建新项目 [项目名]，文件将整理到此目录"
```

---

## Decision Rules / 决策规则

### Project vs One-time Task / 项目 vs 一次性任务

| Type / 类型 | Example / 示例 | Handling / 处理方式 |
|-------------|----------------|---------------------|
| Ongoing project / 持续项目 | 足球预测系统 / Football prediction | Create independent folder / 创建独立文件夹 |
| Daily analysis / 日常分析 | 每日预测、周报 / Daily prediction | Put in related project folder / 放入相关项目文件夹 |
| One-time task / 一次性任务 | 临时数据整理 / Temp data整理 | Put in project folder or tmp / 放入项目文件夹或tmp |

### Folder Naming / 文件夹命名规范

```
EN:
- Use concise English/pinyin names
- Avoid Chinese folder names
- Example: myproject/, recommender/, dataprocessor/

CN:
- 使用简洁的英文/拼音名称
- 避免中文文件夹名
- 示例: myproject/, recommender/, dataprocessor/
```

---

## Example Dialogues / 示例对话

### Case 1: Match Found → Direct Use / 匹配成功 → 直接使用

**User / 用户**: "帮我分析今天足球数据" / "Analyze today's football data"

**Agent / 智能体**:
```
EN:
[Scan] ./PROJECT-HISTORY.md (init if not exists)
[Extract keyword] "足球" → football
[Match result] football -> ./data_analyzer/
  created: 2026-03-01, last_used: 2026-04-18

"Task organized to data_analyzer/ (last_used: today)"

CN:
[扫描] ./PROJECT-HISTORY.md（如不存在则初始化）
[提取关键词] "足球" → football
[匹配结果] football -> ./data_analyzer/
  created: 2026-03-01, last_used: 2026-04-18

"已将此任务整理到 data_analyzer/（last_used: 今天）"
```

### Case 2: No Match → Auto Create / 无匹配 → 自动创建

**User / 用户**: "我要开发一个新的推荐算法" / "I want to develop a new recommendation algorithm"

**Agent / 智能体**:
```
EN:
[Extract keyword] "推荐"
[Match result] No match

1. Create ./recommender/ folder
2. Append new entry to PROJECT-HISTORY.md
3. Reply: "Created new project recommender, files will be organized here"

CN:
[提取关键词] "推荐"
[匹配结果] 无匹配

1. 创建 ./recommender/ 文件夹
2. 在 PROJECT-HISTORY.md 追加新条目
3. 回复："已创建新项目 recommender，文件将整理到此目录"
```

### Case 3: Multiple Matches → Use First / 多个匹配 → 使用第一个

**User / 用户**: "做一下射击项目的数据分析" / "Do data analysis for the shooting project"

**Agent / 智能体**:
```
EN:
[Extract keyword] "射击" → shooting
[Match result] Multiple matches: ./shooting/, ./shooting_v2/
[Decision] Use first one: ./shooting/

"Multiple matches found, using ./shooting/ (last_used: today)"

CN:
[提取关键词] "射击" → shooting
[匹配结果] 多个匹配：./shooting/, ./shooting_v2/
[决策] 使用第一个：./shooting/

"发现多个匹配项目，已使用 ./shooting/（last_used: 今天）"
```

---

## Test Cases / 测试案例

### ✅ Test 1: Match Existing / 匹配已有项目
```
EN:
Input: "分析今天足球数据" / "Analyze today's football data"
Expected: Match football → Use ./data_analyzer/, update last_used

CN:
输入: "分析今天足球数据"
预期: 匹配 football → 使用 ./data_analyzer/，更新 last_used
```

### ✅ Test 2: Auto Create New / 自动创建新项目
```
EN:
Input: "开发一个天气预测系统" / "Develop a weather prediction system"
Expected: No match → Auto-create ./weather-prediction/ folder

CN:
输入: "开发一个天气预测系统"
预期: 无匹配 → 自动创建 ./weather-prediction/ 文件夹
```

### ✅ Test 3: First-Time Auto-Scan / 首次自动扫描
```
EN:
Scenario: Workspace has ./articles/, ./data-science/, memory/, .git/
Expected:
  - Filter .git, memory, skills (system folders)
  - Create entries for articles, data-science in PROJECT-HISTORY.md
  - created = today, last_used = today

CN:
场景: Workspace 有 ./articles/, ./data-science/, memory/, .git/
预期:
  - 过滤 .git, memory, skills 等系统文件夹
  - 为 articles, data-science 创建 PROJECT-HISTORY.md 条目
  - created = 今天日期，last_used = 今天日期
```

---

## Cross-Agent Compatibility / 跨Agent兼容性

```
EN:
Agent A workspace:
  ~/.openclaw/workspace-data_analyzer/
  ├── PROJECT-HISTORY.md
  └── data_analyzer/

Agent B workspace:
  ~/.openclaw/workspace-mlbots/
  ├── PROJECT-HISTORY.md
  └── baseball_project/

Path ./PROJECT-HISTORY.md automatically resolves to the corresponding workspace.

CN:
Agent A workspace:
  ~/.openclaw/workspace-data_analyzer/
  ├── PROJECT-HISTORY.md
  └── data_analyzer/

Agent B workspace:
  ~/.openclaw/workspace-mlbots/
  ├── PROJECT-HISTORY.md
  └── baseball_project/

路径 ./PROJECT-HISTORY.md 自动解析到对应的 workspace。
```

---

## Permission Notes / 权限说明

| Permission / 权限 | Scope / 范围 |
|-------------------|-------------|
| Read / 读取 | `PROJECT-HISTORY.md` in current workspace |
| Write / 写入 | Create new folders, update history in current workspace |
| No access / 不访问 | System files, credentials, other agents' files |

---

## Notes / 注意事项

| # | English | 中文 |
|---|---------|------|
| 1 | **Be direct**: If match found, use it directly and notify user | **直接处理**: 如匹配到项目，直接使用并告知用户 |
| 2 | **Auto-create**: If no match, create new folder without asking | **自动创建**: 无匹配时直接创建新文件夹，无需询问 |
| 3 | **Update always**: Always update `last_used` when using existing project | **始终更新**: 使用已有项目时必须更新 last_used |
| 4 | **Record all**: Must update `PROJECT-HISTORY.md` for new projects | **记录新项目**: 创建新项目时必须更新 PROJECT-HISTORY.md |
| 5 | **Bilingual**: Support both Chinese and English keyword matching | **双语兼容**: 同时支持中文关键词和英文key直接匹配 |
| 6 | **Workspace isolation**: Different agents have independent histories | **workspace隔离**: 不同Agent的项目历史互相独立 |
| 7 | **System folders**: Skip .git, .openclaw, memory, skills, .learnings, .env, .DS_Store | **系统文件夹**: 跳过 .git, .openclaw, memory, skills 等 |
| 8 | **Monthly archive**: Mark projects with `last_used` > 3 months as archived | **定期归档**: 每月检查，将 last_used > 3个月的项目标记为归档 |
