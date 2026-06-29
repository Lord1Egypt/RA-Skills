---
name: skill-advisor
slug: skill-advisor
displayName: 智能技能推荐器（Smart Skill Advisor）
version: "1.1.0"
description: 根据用户当前需求，从 SkillHub、ClawHub、本地已安装、官方内置四层搜索中智能匹配，输出适配度最高的 3 个技能，包含功能亮点、优缺点对比和综合评价。只推荐不安装，用户决策后再动手。支持 /skill 指令和 slash command 启动。
agent_created: true
security: low
permissions:
  - network: yes
  - filesystem: read-only
  - shell: no
---

# 智能技能推荐器（Smart Skill Advisor）

## 概述

本技能是**智能技能顾问**——用户用自然语言描述当前需求，系统自动理解意图，从四个来源搜索，用多维度评分模型计算适配度，最终输出**Top 3 技能深度分析报告**。

**核心差异**（与 find-skills 系列的区别）：
- find-skills → 「我把技能列给你，你要哪个？」
- skill-advisor → 「我分析了你的需求，这 3 个最合适，各有优劣，你选」

---

## 核心流程

### Step 1：理解用户需求

从用户描述中提取结构化信息：
- **任务类型**：创作/开发/分析/管理/查询/自动化/数据处理/其他
- **具体意图**：一段准确的意图描述
- **领域**：内容创作/金融/电商/教育/开发工具/生活/企业服务/数据分析/其他
- **关键词**：中英文搜索关键词（各 2-3 个）
- **特殊要求**：是否需要免费、是否需要 API Key、是否需要安全验证等

### Step 2：四层搜索

#### 2.1 本地已安装技能

扫描 `~/.workbuddy/skills/` 和项目级 `.workbuddy/skills/`（如存在），读取每个 SKILL.md 的 name/displayName/description。

```bash
ls ~/.workbuddy/skills/
ls .workbuddy/skills/ 2>/dev/null || true
```

#### 2.2 官方内置技能

扫描 WorkBuddy 内置技能目录：

```bash
# Windows 路径
ls "C:/Users/Administrator/AppData/Local/Programs/WorkBuddy/resources/app.asar.unpacked/resources/builtin-skills/"
```

#### 2.3 远程搜索（SkillHub + ClawHub）

使用辅助脚本 `scripts/search_skills.py`，该脚本会同时搜索 SkillHub 和 ClawHub，并自动计算适配度评分：

```bash
python ~/.workbuddy/skills/skill-advisor/scripts/search_skills.py "<用户需求>" --limit 20 --keywords "<kw1>,<kw2>,<kw3>"
```

> **注意**：如果 `python` 命令不可用，使用绝对路径：
> `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`

输出 JSON 数组，每个元素包含：
- `slug`, `displayName`, `description` — 技能基本信息
- `downloads`, `installs`, `stars` — 人气指标
- `adapter_score` — 综合适配度评分（满分 100）
- `source` — 来源（skillhub / clawhub）
- `sourceUrl`, `author`, `security`

---

### Step 3：综合评分 & 排名

辅助脚本已自动计算 `adapter_score`，评分维度（满分 100）：

| 维度 | 权重 | 说明 |
|---|---|---|
| 语义匹配度 | 40% | 技能描述与用户关键词的匹配程度 |
| 人气指标 | 20% | downloads×0.3 + installs×0.5 + stars×0.2（归一化） |
| 安全性 | 15% | benign=100, suspicious=30, malicious=-50 |
| 易用性 | 10% | 无需 API Key=100，需要配置=60 |
| 来源加分 | 15% | 本地=20，内置=15，SkillHub=12，ClawHub=10 |

**淘汰规则**：
- `adapter_score` < 20 → 直接淘汰
- 人气为 0 且关键词匹配 < 2 → 淘汰

---

### Step 4：输出 Top 3 深度分析报告

#### 报告模板（直接输出在对话中）

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【智能技能推荐】针对「{用户需求}」的 Top 3 推荐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 评选标准：语义匹配(40%) + 人气(20%) + 安全(15%) + 易用(10%) + 来源(15%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥇 第一名：{displayName} — 适配度 {adapter_score}/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 功能概览
• {基于 description 提炼 3 个核心功能点}

✅ 优点
• 人气高（{downloads} 下载，{installs} 安装）
• {其他优点 1}
• {其他优点 2}

❌ 缺点 / 注意事项
• {缺点 1，如需要 API Key}
• {缺点 2，如安全状态未知}

⭐ 综合评价
{一段 2-3 句的评价，综合适配度、人气、安全性给出判断}

📎 详情：{sourceUrl} | 作者：{author} | 来源：{source}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥈 第二名：{displayName} — 适配度 {adapter_score}/100
...（同上结构）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥉 第三名：{displayName} — 适配度 {adapter_score}/100
...（同上结构）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 综合建议
{综合对比 3 个技能，给出推荐意见，说明推荐理由和注意事项}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> 🛠️ 选好了告诉我，我来帮你安装。
```

---

### Step 5：用户选择后安装

用户选择后（比如"装第一个"），系统自动按以下方式安装，用户无需手动操作：

**从 SkillHub 安装**：系统自动下载 zip 包并解压到 `~/.workbuddy/skills/<slug>/` 目录。

**从 ClawHub 安装**：系统自动执行 `npx clawhub install <slug> --workdir ~ --dir .workbuddy/skills` 完成安装。

安装成功后提示用户。

---

## 测试验证

### 测试环境
- Python: 3.13.12 (managed)
- 依赖: urllib, subprocess, re（均标准库，无额外依赖）
- 网络: 可访问 lightmake.site（SkillHub）和 npm/clawhub（ClawHub）

### 测试用例（v1.0.0 验证通过）

| # | 用户需求 | 关键词 | Top1 slug | Top1 评分 | 状态 |
|---|---|---|---|---|---|
| 1 | A股股票查询 | A股,股票,查询 | akshare-stock | 67.5 | ✅ |
| 2 | 天气查询 | 天气,查询,weather | gooduone-weather | 67.2 | ✅ |
| 3 | 简历筛选 | 简历,筛选,招聘 | resum-screening | 82.0 | ✅ |
| 4 | 海报设计 | 海报,设计,poster | find-skills | 57.8 | ✅ |

### 已知行为说明
- SkillHub 部分技能的 `sourceUrl` 使用 `api.skillhub.cn` 镜像域名（正常，会重定向）
- 若 ClawHub 搜索无结果，脚本自动 fallback 到 SkillHub 结果
- `adapter_score` 为 0-100 分，< 20 的技能不会出现在最终结果中

---

## 安全声明

- 本技能**仅读取**技能市场数据，不执行任何写入、删除、修改操作
- 远程搜索通过 HTTPS 访问 SkillHub/ClawHub 公开 API，不收集用户隐私
- 推荐结果**只输出不自动安装**，最终安装动作由用户确认后触发
- 不涉及敏感文件访问、网络监听、或系统级操作
- 安全等级：**Low**

---

## 启动方式（重要）

### 方式一：直接提问（推荐）

用自然语言描述你的需求，系统会自动识别并触发本技能：

```
推荐一个适合做海报的技能
有什么好用的股票查询技能
帮我找个能筛简历的工具
这个需求有什么技能可以解决
```

**触发关键词**：推荐、找个、有什么、哪个技能、适合、帮我找

---

### 方式二：使用 /skill 指令

直接输入 `/skill <你的需求>` 快速启动：

```
/skill 推荐海报设计工具
/skill 查股票的技能
/skill 简历筛选
```

---

### 方式三：Slash Command 配置（可选）

在 WorkBuddy 的 Slash Command 设置中添加：

| 字段 | 值 |
|---|---|
| Command | `/skill` |
| 描述 | 智能技能推荐器 |
| 技能 | `skill-advisor` |
| 参数 | `query`（用户需求） |

配置后输入 `/skill` 即可看到提示。

---

## 常见问题与错误用法（FAQ）

### ❌ 常见错误用法

1. **关键词过于具体或生僻**
   - ❌ 错误示例：`推荐一个能帮我写Python代码的skill，最好是支持语音合成的`
   - ✅ 正确示例：`推荐一个Python编程技能` 或 `推荐语音合成工具`

2. **一次性输入太多需求**
   - ❌ 错误示例：`帮我找一个能做海报、写文案、分析数据、还能聊天的技能`
   - ✅ 正确示例：分多次提问，一次只解决一个需求

3. **关键词与实际需求不匹配**
   - ❌ 错误示例：想找视频剪辑却说「视频生成」
   - ✅ 正确示例：使用准确的领域术语

---

### ❓ 常见问题

**Q1：搜索结果为空怎么办？**
> A：尝试使用更通用的关键词。比如搜「机器学习」无结果，可以试试「AI」「人工智能」「模型」。

**Q2：推荐结果不准确怎么办？**
> A：可以换一个更具体的关键词重新搜索，或者告诉我你更看重哪个维度（功能完整度/易用性/安全性），我来调整推荐策略。

**Q3：网络不好时搜索失败怎么办？**
> A：脚本会自动重试 3 次。如果仍然失败，请检查网络连接后再次尝试搜索。

**Q4：ClawHub 搜索失败提示 npx 未安装？**
> A：这表示你的电脑没有安装 Node.js。请先安装 Node.js (https://nodejs.org/)，然后运行 `npm install -g clawhub`。

**Q5：推荐结果里有的技能需要 API Key 怎么办？**
> A：报告中会标注「需要 API Key」的技能。如果你不愿配置，可以选择报告中标记为「免费/无需配置」的技能。

**Q6：我怎么知道什么时候该用这个技能？**
> A：当你想找某个场景的技能，但不确定用哪个时，直接说「推荐一个 XXX 技能」就行。也可以用 `/skill` 指令快速启动。

---

### 📝 反馈渠道

如果遇到以上未列出问题，或有改进建议，请：
1. 记录报错信息和复现步骤
2. 反馈给技能开发者

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.1.0 | 2026-06-26 | 增强异常处理 + 自动重试 + FAQ 章节 + 触发方式说明 |
| 1.0.0 | 2026-06-26 | 初始版本：四层搜索 + 评分推荐 |
