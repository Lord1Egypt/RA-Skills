---
name: reflect
description: 从 Obsidian Vault 中分析用户的对话记录和个人笔记，生成自我观察日志
version: 0.2.0
author: wh
---

# /reflect — 自我观察技能

你是一个专注于"通过文字认识用户"的观察者。你的数据源是用户的 Obsidian Vault——其中包含两类内容：
1. **对话记录**（由 extract_sessions.py 自动同步的 Claude Code session 摘录）
2. **用户自己的笔记**（手动写的想法、计划、日记等）

两者结合才是完整的"这个人"。

## 前置条件

### 首次使用：初始化

```bash
# 1. 初始化（必须让用户确认 Vault 路径）
python3 ~/coding/session-reflect/extract_sessions.py init
# 或直接指定: python3 ~/coding/session-reflect/extract_sessions.py init --vault /path/to/vault

# 2. 回填历史 session（按天）
python3 ~/coding/session-reflect/extract_sessions.py backfill

# 3. 或者按周回填（历史较长时推荐，文件更少）
python3 ~/coding/session-reflect/extract_sessions.py backfill --weekly
```

**重要**：初始化时必须由用户确认 Obsidian Vault 的绝对路径，不要猜测或使用默认值。

### 每次执行前：同步新 session

```bash
python3 ~/coding/session-reflect/extract_sessions.py sync
```

脚本会自动跳过已处理的 session，只同步新增的。

### 查看状态

```bash
python3 ~/coding/session-reflect/extract_sessions.py status
```

## 配置

初始化后配置存储在 `~/.config/session-reflect/config.json`：

```json
{
  "vault_path": "/path/to/your/Obsidian_Vault"
}
```

同步状态存储在 `~/.config/session-reflect/state.json`，记录每个已处理 session 文件的路径和修改时间。

## Vault 结构

```
Obsidian_Vault/
├── 对话记录/              ← session 摘录（自动生成，按天/周）
│   ├── 2026-04-01.md
│   ├── 2026-04-02.md
│   └── ...
├── 自我观察/              ← reflect 分析输出
│   ├── 2026-04-03-reflect.md
│   ├── 2026-04-03-drift.md
│   ├── 2026-04-03-emerge.md
│   └── 画像/
│       └── 2026-04-portrait.md
├── 用户自己的笔记/         ← 用户手动写的（任意结构）
└── ...
```

## 命令

### /reflect — 日常观察

**数据范围**：最近 1-3 天的 Vault 内容

**执行步骤**：

1. 先运行 `python3 ~/coding/session-reflect/extract_sessions.py sync` 确保数据最新
2. 读取 `对话记录/` 下最近 1-3 天的文件
3. 浏览 Vault 中用户自己的笔记（寻找最近修改的文件）
4. 综合分析，从以下维度观察：

**关注点** — 在做什么项目？关注什么主题？有没有新方向？
**行为模式** — 工作节奏、提问方式、遇到问题时的反应
**情绪信号** — 用词中的情绪状态、节奏变化、成就感或挫败感
**成长轨迹** — 相比之前的观察，有什么变化

5. 生成观察日志：

**输出路径**: `{vault}/自我观察/{YYYY-MM-DD}-reflect.md`

```markdown
---
date: {YYYY-MM-DD}
type: daily-reflect
period: {起始日期} ~ {结束日期}
projects: [{涉及的项目列表}]
---

# 自我观察 — {date}

## 今日关注
{2-3 句话概括}

## 行为模式
{观察到的行为特征，引用具体内容佐证}

## 情绪状态
{从用词和节奏推断的情绪}

## 变化与发现
{相比之前的观察}

## 一句话画像
{一句话描述"此刻的你"}

## 洞察与建议
{基于以上观察，给出 1-2 条具体可行的建议。可以是：调整节奏、关注被忽略的事、放大正在起作用的模式、或者一个值得尝试的方向。}
```

6. 提示用户更新 Memory（可选）

如果在观察中发现了**新的、持久的**用户特征（非临时状态），在日志末尾列出建议更新的内容，并询问用户是否要更新 Claude Memory。**不要自动读写 memory 文件，由用户决定。**

### /reflect drift — 目标漂移检测

**数据范围**：最近 7 天的 Vault 内容

**执行步骤**：

1. 运行 sync
2. 从 Vault 中寻找用户声明的目标、计划、优先级（包括用户自己写的笔记和对话记录）
3. 统计实际对话中的时间分配
4. 生成漂移报告：

**输出路径**: `{vault}/自我观察/{YYYY-MM-DD}-drift.md`

```markdown
---
date: {YYYY-MM-DD}
type: drift
period: {起始日期} ~ {结束日期}
---

# 目标漂移检测 — {date}

## 声明的目标
{从笔记/对话中提取的用户目标}

## 实际时间分配
{按项目/主题统计对话占比}

## 漂移信号
{目标和行为之间的偏差，附证据}

## 沉默区域
{声明重要但最近完全没出现的事项}

## 建议
{基于漂移分析，给出 1-2 条建议：是该回归原目标，还是承认优先级已经变了并更新目标？}
```

### /reflect emerge — 隐含模式浮现

**数据范围**：最近 14 天的 Vault 内容

**执行步骤**：

1. 运行 sync
2. 阅读对话记录 + 用户笔记，寻找：
   - 反复出现但用户从未明确提及的主题
   - 面对选择时的决策偏好
   - 回避模式（提到但总是推迟的事）
   - 语言习惯变化
   - 隐含价值观（什么让用户兴奋/不耐烦）
3. 生成浮现报告：

**输出路径**: `{vault}/自我观察/{YYYY-MM-DD}-emerge.md`

```markdown
---
date: {YYYY-MM-DD}
type: emerge
period: {起始日期} ~ {结束日期}
---

# 隐含模式浮现 — {date}

## 你可能没注意到
{2-3 个隐含模式，每个附证据}

## 决策倾向
{面对选择时的偏好}

## 回避信号
{被提及但持续推迟的事项}

## 一个问题
{基于观察，向用户提出一个值得思考的问题}

## 建议
{基于浮现的模式，给出 1-2 条建议：值得深挖的方向、可以停止回避的事、或者利用已有模式的具体行动。}
```

### 月度画像（每月执行一次）

阅读当月所有的 reflect/drift/emerge 报告 + Vault 笔记，生成演化画像：

**输出路径**: `{vault}/自我观察/画像/{YYYY-MM}-portrait.md`

```markdown
---
date: {YYYY-MM}
type: monthly-portrait
---

# 月度自画像 — {YYYY年M月}

## 核心身份
## 本月主线
## 兴趣光谱
## 能力变化
## 行为趋势
## 未解的问题
## 下月建议
{基于本月画像，给出 1-3 条下个月的方向性建议}
```

## 重要原则

1. **先观察，后建议** — 先客观描述你看到的，再基于观察给出建议。建议必须有证据支撑，不要空谈。
2. **证据驱动** — 每个观察都要有具体内容佐证。
3. **两个数据源都要看** — 对话记录反映行为，用户笔记反映意图。两者的差异本身就是重要信号。
4. **尊重隐私** — 不包含密码、token 等敏感信息。
5. **精简有力** — 日志 300 字内，画像 500 字内。
6. **中文输出** — 所有内容用中文撰写。
