---
name: tiered-recall
version: 1.1.0
description: 分层回忆系统 - 解决上下文长度限制，保持项目延续性。每次新session自动加载核心记忆+最近日志+活跃项目，支持手动深度回忆。索引含10字内摘要，方便区分同名条目。
license: MIT
author: davidme6
homepage: https://clawhub.com/skill/tiered-recall
repository: https://github.com/davidme6/tiered-recall
keywords: [memory, recall, context, session, continuity]
changelog: "v1.1.0: 增加10字内极致摘要，方便区分同名条目。v1.0.3: 加标题。v1.0.0: 初始版本"
---

# Tiered Recall 🧠📚

**分层回忆系统 - 解决大模型上下文长度限制，保持项目延续性**

---

## 🎯 核心问题

大模型上下文有限（约20万token），复杂项目可能跨多天、多窗口进行。每次新session开始时，如何快速恢复上下文，保持工作延续性？

**常见痛点：**
- 新开窗口，之前的项目背景丢失
- 跨天任务，第二天不记得昨天做了什么
- 多项目并行，切换时混乱
- 手动回顾太慢，浪费时间

---

## 🚀 解决方案：分层回忆

### 自动加载策略（每次新session）

| 层级 | 内容 | Token预算 | 加载条件 |
|------|------|-----------|----------|
| 🔴 L0 核心 | `MEMORY.md` | ~4k | 始终加载 |
| 🟠 L1 近期 | 最近2天日志 | ~10k | 始终加载 |
| 🟡 L2 项目 | 活跃项目文件 | ~5k | 自动检测 |
| 🟢 L3 索引 | 记忆索引 | ~1k | 始终加载 |
| **总计** | | **~20k** | |

**总预算：~20k token，约占总上下文的10%**

---

## 📂 文件结构

```
workspace/
├── MEMORY.md              # L0 核心记忆（长期）
├── memory/
│   ├── 2026-03-25.md      # 每日日志
│   ├── 2026-03-24.md
│   ├── 2026-03-23.md
│   └── ...
├── .tiered-recall/
│   ├── index.json         # 记忆索引
│   ├── projects.json      # 活跃项目清单
│   └── state.json         # 加载状态
└── skills/
    └── tiered-recall/
        └── SKILL.md       # 本技能
```

---

## 🔄 自动加载流程

### Step 1: 检测触发条件

**自动触发：**
- 新session开始
- 用户说"继续之前的项目"
- 用户提到项目名称

### Step 2: 加载L0核心记忆

```markdown
# MEMORY.md 加载
- 用户基本信息
- 重要偏好
- 长期决策
- 关键项目记录
```

### Step 3: 加载L1近期日志

```markdown
# 最近2天日志
- memory/2026-03-25.md
- memory/2026-03-24.md
```

**自动提取：**
- 昨天做了什么
- 今天待办事项
- 未完成任务

### Step 4: 加载L2活跃项目

```json
// .tiered-recall/projects.json
{
  "active": [
    {
      "name": "合成天选打工人",
      "path": "games/merge-worker/",
      "lastActive": "2026-03-24",
      "keyFiles": ["index.html", "README.md"]
    },
    {
      "name": "搞钱特战队",
      "path": "products/AI-Guide/",
      "lastActive": "2026-03-24",
      "keyFiles": ["chapter1/"]
    }
  ]
}
```

### Step 5: 加载L3记忆索引

```json
// .tiered-recall/index.json
{
  "topics": {
    "游戏开发": ["memory/2026-03-23.md:line100-200", "memory/2026-03-24.md:line50-150"],
    "搞钱特战队": ["memory/2026-03-24.md:line200-400"],
    "OpenClaw变现": ["memory/2026-03-24.md:line400-600"]
  },
  "lastUpdated": "2026-03-25T09:00:00"
}
```

---

## 🎮 手动深度回忆

当默认加载不够时，用户可以要求深度回忆：

### 指令语法

| 指令 | 作用 | 示例 |
|------|------|------|
| `继续回忆` | 加载更多相关记忆 | "继续回忆游戏项目" |
| `回忆 [项目名]` | 加载该项目全部记忆 | "回忆搞钱特战队" |
| `回忆 [天数]` | 加载指定天数日志 | "回忆最近7天" |
| `回忆 [日期]` | 加载指定日期日志 | "回忆3月20日" |
| `回忆 [关键词]` | 按关键词搜索记忆 | "回忆抖音小游戏" |

### 执行流程

```
用户: "回忆搞钱特战队"
  ↓
1. 搜索 index.json 找到相关条目
2. 加载相关日期日志的相关段落
3. 加载项目文件
4. 生成项目上下文摘要
5. 输出给用户确认
```

---

## 📊 Token 预算控制

### 默认加载（~20k token）

```
L0 MEMORY.md        ████████░░  4k
L1 最近2天日志      ████████████████████████░░  10k
L2 活跃项目         ██████████░░  5k
L3 记忆索引         ██░░  1k
                    ─────────────────────
                    总计 ~20k token
```

### 深度回忆时（动态调整）

```
用户要求: "回忆搞钱特战队全部记忆"
  ↓
预估: 约50k token
  ↓
策略: 
1. 先加载摘要（~10k）
2. 询问用户是否继续
3. 分批加载，每批~20k
```

---

## 🛠️ 脚本命令

### 生成记忆索引

```bash
python skills/tiered-recall/scripts/build-index.py
```

**功能：**
- 扫描 `memory/` 目录所有日志
- 提取关键词和主题
- 生成 `index.json`

### 更新活跃项目

```bash
python skills/tiered-recall/scripts/update-projects.py
```

**功能：**
- 扫描最近日志中提到的项目
- 更新 `projects.json`

### 完整加载

```bash
python skills/tiered-recall/scripts/load.py [--deep] [--project NAME]
```

**参数：**
- `--deep` 深度加载，突破默认token限制
- `--project NAME` 只加载指定项目

---

## 📝 使用示例

### 场景1：新session自动加载

```
[新session开始]
AI: 
📖 加载核心记忆... ✓ (MEMORY.md)
📅 加载近期日志... ✓ (2026-03-25, 2026-03-24)
📂 加载活跃项目... ✓ (合成天选打工人, 搞钱特战队)
📑 加载记忆索引... ✓

=== 今日上下文 ===
1. 昨天完成：搞钱特战队商业模式确定
2. 今天待办：制作引流资料包
3. 活跃项目：合成天选打工人、搞钱特战队
================

早安！今天要继续哪个项目？
```

### 场景2：手动深度回忆

```
用户: 回忆合成天选打工人全部记忆

AI:
🔍 搜索中...
  找到相关记录: 2026-03-23, 2026-03-24
  
📖 加载2026-03-23相关段落...
  - 游戏版本迭代 v2.6 → v2.24
  - 修复7个Bug
  - 11人团队评估通过
  
📖 加载2026-03-24相关段落...
  - 准备软著材料
  - 抖音小游戏适配讨论

📂 加载项目文件...
  - games/merge-worker/index.html (108KB)
  - games/merge-worker/VERSION_HISTORY.md

=== 项目摘要 ===
游戏名称：天选打工人
当前版本：v2.24
状态：已完成，可上线
下一步：软著申请、抖音上线
================

需要继续回忆更多细节吗？
```

### 场景3：跨天任务延续

```
用户: 继续昨天的引流资料包制作

AI:
🔍 查找昨天记录...
  2026-03-24: "制作免费引流资料包"
  
📖 加载相关上下文...
  - 第一章教程已完成（17000字）
  - 封面v8已完成
  - 小红书账号已设置
  
📂 加载工作文件...
  - products/AI-Guide/chapter1/

好的，继续制作引流资料包。昨天第一章已完成，今天要做的是：
1. 整理成PDF
2. 添加封面
3. 准备下载链接

开始吗？
```

---

## ⚙️ 配置选项

### `.tiered-recall/config.json`

```json
{
  "defaultLayers": ["L0", "L1", "L2", "L3"],
  "recentDays": 2,
  "maxTokensPerLayer": {
    "L0": 4000,
    "L1": 10000,
    "L2": 5000,
    "L3": 1000
  },
  "deepRecallBudget": 50000,
  "autoLoadOnNewSession": true
}
```

---

## 🔧 技术实现

### 记忆索引生成算法

```python
def build_index(memory_dir):
    """扫描日志，提取主题和关键词"""
    index = {"topics": {}, "lastUpdated": datetime.now().isoformat()}
    
    for file in sorted(memory_dir.glob("*.md"), reverse=True):
        content = file.read_text(encoding="utf-8")
        
        # 提取标题和章节
        sections = extract_sections(content)
        
        # 识别主题
        for section in sections:
            topic = classify_topic(section["title"])
            if topic:
                index["topics"].setdefault(topic, []).append({
                    "file": file.name,
                    "lines": section["lines"],
                    "summary": summarize(section["content"])
                })
    
    return index
```

### 活跃项目检测

```python
def detect_active_projects(memory_dir, days=7):
    """从最近日志中检测活跃项目"""
    projects = {}
    
    for file in get_recent_files(memory_dir, days):
        content = file.read_text(encoding="utf-8")
        
        # 匹配项目关键词
        for match in PROJECT_PATTERNS:
            if match["pattern"] in content:
                project = match["name"]
                projects[project] = {
                    "lastMentioned": file.stem,
                    "path": match.get("path"),
                    "keyFiles": match.get("keyFiles", [])
                }
    
    return projects
```

---

## 🎯 最佳实践

### 1. 保持MEMORY.md精简

- ✅ 只放长期重要的信息
- ❌ 不要放每日琐事
- 目标：< 200行

### 2. 每日日志结构化

```markdown
# 2026-03-25 日志

## 📌 今日重点
- [x] 任务A
- [ ] 任务B

## 🎮 项目：合成天选打工人
进度：v2.24完成
下一步：软著申请

## 💰 项目：搞钱特战队
进度：商业模式确定
下一步：制作资料包
```

### 3. 项目关键词规范

在日志中使用统一的项目名称：
- ✅ "合成天选打工人"、"搞钱特战队"
- ❌ "那个游戏"、"赚钱的项目"

### 4. 定期清理索引

```bash
# 每周运行一次
python skills/tiered-recall/scripts/build-index.py --clean
```

---

## 📈 效果对比

| 场景 | 无分层回忆 | 有分层回忆 |
|------|-----------|-----------|
| 新session启动 | 手动回顾5-10分钟 | 自动加载，即刻恢复 |
| 跨天任务 | "我们昨天做什么来着" | "继续昨天的X任务" |
| 多项目切换 | 混乱、遗忘 | 自动加载项目上下文 |
| Token消耗 | 随机、不稳定 | 可控、~20k预算 |

---

## 🤝 与其他技能协作

| 技能 | 协作方式 |
|------|----------|
| `self-improving-enhancement` | 共享记忆结构，增量更新 |
| `team-collab` | 团队会议记录自动索引 |
| `proactive-agent` | 心跳检查时更新索引 |

---

## 📝 Changelog

### v1.0.0 (2026-03-25)
- ✨ 初始版本
- 🔄 支持分层自动加载
- 🔍 支持手动深度回忆
- 📊 Token预算控制
- 🗂️ 记忆索引生成

---

## 💬 Feedback

- Issues: GitHub Issues
- Rate: `clawhub star tiered-recall`
- Update: `clawhub sync tiered-recall`

---

**Made with 🧠 by davidme6**