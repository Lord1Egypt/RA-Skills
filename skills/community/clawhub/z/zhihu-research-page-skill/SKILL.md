---
name: zhihu-research-page
slug: zhihu-research-page
displayName: "一键生成知乎高质量回答网页（可自由剪裁）"
version: "22.0.2"
summary: "大规模联网搜索 + 知乎风深度知识网页生成，支持任意比例裁剪、单文件 HTML 交付"
license: MIT
title: "知乎研究页生成器 — 一句话生成知乎高质量回答网页"
author: "timeRATE-966"
description: 通过大规模联网搜索自动创建知乎风格的深度知识网页，样式高度还原 zhihu.com。默认生成含 10 个回答的多答主模拟回答页面，含 ≥10 万有效中文字和 ≥500 次真实搜索引用。支持手动裁剪为任意比例版本（如"执行 5% 版本"→ ≥5 千字 / ≥25 次搜索），多次执行自动创建带版本号的独立文件夹。适用于生成知识专题页、学习路径教程、产品深度百科、行业研究报告等需要系统整理某一主题知识的场景。**[重要]100%版本约需 100 分钟且token消耗巨大，建议先生成 2% 版本检验效果**
type: "agent"
category: "research"
invocation: "/zhihu-research-page"
tags:
  - "research"
  - "content-creation"
  - "web-generation"
  - "chinese"
  - "knowledge-base"
difficulty: "intermediate"
claude_version: ">=1.0.0"
permissions:
  read:
    - "project files"
    - "web content"
  write:
    - "project files"
  network: "extensive"
examples:
  - input: "/zhihu-research-page 执行2%版本\n主题：什么是 Harness Engineering？"
    output: "自动搜索 ≥10 次，生成 3 个回答的知乎风网页（约 2,000 字），约 2 分钟"
  - input: "/zhihu-research-page 执行100%版本\n主题：国际象棋怎么学？"
    output: "自动搜索 ≥500 次，生成 10 个回答的完整深度网页（≥100,000 字），约 100 分钟"
---

<!-- VERSION:v22.0.2 | 2026-11-09 | 表述统一：章节→回答（修正包内版本字段） -->
# 一句话生成知乎高质量回答网页（可自由剪裁）

## 用法示例

```
/ zhihu-research-page 执行5%版本
主题：什么是 Harness Engineering？

/ zhihu-research-page 执行100%的v2版本
主题：国际象棋怎么学？代数记谱法、西西里、西班牙主流开局这些是什么？

/ zhihu-research-page 执行200%的v2版本
主题：各种调式的流行歌曲都有什么特点，它们各有什么代表作？
```

---

## 概述

输入一个研究主题 → 自动产出：
- 📄 一个知乎风格的完整 HTML 单页（含顶栏/问题头/侧栏/10 个回答/页脚）
- 🔗 每个回答 ≥11,000 有效中文字，全页 ≥100,000 字
- 🔍 累计 ≥500 次真实 WebSearch（7~8 个并行搜索代理）
- 📎 242+ 条真实可点击外链（禁止编造 URL）
- 🧪 字数核验 + 结构校验脚本

该工作流基于已验证的 LILYGO T-WATCH-2020 项目实战流程提炼而成。

## Skill 版本与更新日志

当前版本：**v22.0.2**（2026-11-09）

> 运行时需检查此版本号：若高于上次执行记录，则从 skill 目录重新读取最新 SKILL.md 和脚本更新工作区。

更新日志（每行一句，格式 `vN [yyyy-MM-dd HH:mm:ss] 内容`）：
- v22.0.2 [2026-11-09 00:15:00] 重新发布：修正 22.0.1 包内 version 字段仍为 22.0.0 的问题（ClawHub 同版本不可覆盖）
- v22.0.1 [2026-11-09 00:05:00] 表述统一：面向用户的「章节」全部改为「回答」，与 README 对齐；侧栏标题改为「本页回答」
- v22 [2026-10-29 13:39:49] 新增单文件 HTML 交付（图片 base64 内嵌、删除 index.html）与可选上传 WorkBuddy 资料库
- v21 [2026-07-21 22:26:31] 新增教程/学习模式（提炼答主背景、面向学习目标），自动同步检查，版本头
- v20 [2026-07-19 07:41:47] 修复 f-string 转义、emoji 崩溃(→ASCII)、TARGET_WORDS 可配、Edit→Python 追加
- v19 [2026-07-18 22:05:01] 新增部分执行模式(N% 版本)，任意百分比等比缩放
- v18 [2026-07-18 21:32:27] 去硬编码重构，异常手册 TROUBLESHOOTING.md，蓝阈值收紧
- v17 [2026-07-18 21:27:14] 搜索配额感知、子代理文件验收、来源池外化、code自检前移、Win编码兼容
- v16 [2026-07-18 21:23:54] css-template.css code 样式对齐知乎、去硬编码style块、组装自查
- v15 [2026-07-18 16:47:18] assemble 新增 style 去重+蓝归一
- v14 [2026-07-18 15:37:47] zh-body→zh-page 类名隔离
- v13 [2026-07-18 15:50:15] 头像与身份解耦(已回滚)
- v12 [2026-07-18 15:35:44] 全图片本地化 ./images/
- v11 [2026-07-18 15:28:56] 头像本地缓存 ./images/
- v10 [2026-07-18 13:10:27] 目录组织 ./other/ ./research_result/
- v9  [2026-07-18 02:19:55] 答主身份与头像三级优先级+四步流程
- v8  [2026-07-18 00:17:07] scan_html.py 预扫描+子代理权限+code标签规范
- v7  [2026-07-17 17:31:26] search_result.md 存疑/争议+毫秒时间戳
- v6  [2026-07-17 17:27:14] search_result.md 格式对齐真实文件
- v5  [2026-07-16 16:24:43] assemble 注入改为 ASSEMBLE 标记，幂等剥离
- v4  [2026-07-14 14:30:00] search_result.md 协同积累机制
- v3  [2026-07-14 12:00:00] 诊断先于搜索，去硬编码路径
- v2  [2026-07-14 10:00:00] Skill 目录只读约定
- v1  [2026-07-13 22:00:00] 初始 8 阶段工作流

### 工作区目录约定

为避免工作区根目录散落大量中间文件，所有产出严格按以下目录存放：

```
工作区/
├── {文件夹名}_{ASCII主题名}.html  # 最终交付物：单文件，图片已 base64 内嵌
├── index.html                  # 中间产物：拼接骨架（阶段 7 打包后删除）
├── CHANGELOG.md                # 更新日志（可选）
├── images/                     # 所有图片资源（与 HTML 同目录，相对路径引用）
│   ├── ch-01.png               # 答主头像缓存（.png/.jpg/.svg）
│   ├── ch-02.svg               # DiceBear 头像缓存
│   ├── diagram-03.png          # 章节插图/截图/示意图/logo
│   └── ...
├── other/                      # 网页草稿、脚本、中间产物
│   ├── _draft_*.html           # 各章节 HTML 草稿
│   ├── assemble.py             # 从 skill 复制的拼接脚本
│   ├── scan_html.py            # 从 skill 复制的预扫描脚本
│   ├── *.ps1 / *.py / *.json   # 其他中间脚本和配置
│   └── index_skeleton.html     # 骨架备份（方便二次运行还原）
└── research_result/            # 搜索结果及中间产物
    ├── search_result.md        # 搜索结果累积文件
    └── *.md / *.json           # 来源池清单、搜索报告等
```

**铁律**：
- 阶段 0 第一步：`mkdir -p ./images ./other ./research_result`
- 所有路径在命令行和代码中**显式使用 `./other/` 和 `./research_result/` 前缀**，不依赖 `cd`
- 最终交付物是根目录下的**单文件 HTML**（`{文件夹名}_{ASCII主题名}.html`），`index.html` 是中间产物，阶段 7 打包后删除

### 异常处理（TROUBLESHOOTING）

**遇到异常时，必须先读取 `TROUBLESHOOTING.md`** 查找匹配方案。该文件覆盖 15 类高频异常的根因和修复步骤（配额耗尽、task-notification 不实、`<code>` 字体异常、Windows 编码崩溃、颜色归一误伤、字数失真、权限被拒、单文件打包、资料库上传等）。仅在文件中无匹配方案时，才自行分析处理。

---

## 工作流总览（8 阶段）

```
[0] 收集输入 → [1] 诊断问题 → [2] 创建骨架 HTML → [3] 并行搜索(500+) → [4] 规划章节(基于搜索) → [4.5] 答主身份与头像配置 → [5] 并行写章 → [6] 组装校验 → [7] 打包单文件 + 交付 + 可选上传资料库
```

**严禁跳过任何阶段**。搜索和撰写都通过 Subagent 委托执行，主流程不直接生成章节内容。

### 子代理权限配置（重要！）

使用 Agent 工具启动的 `general-purpose` 子代理在写入文件时经常遇到 Write/Bash 权限被拒。需在项目根目录的 `.claude/settings.local.json` 中显式授权：

```json
{
  "permissions": {
    "allow": [
      "Bash(python *:other/_draft_*.html *)",
      "Bash(python *:other/scan_html.py *)",
      "Bash(python *:other/assemble.py *)",
      "Write(*:other/_draft_*.html)",
      "Write(*:index.html)",
      "Write(*:other/assemble.py)",
      "Write(*:images/*.png)",
      "Write(*:images/*.jpg)",
      "Write(*:images/*.svg)",
      "Bash(curl *:images/*.png *)",
      "Bash(curl *:images/*.svg *)",
      "Edit(*:other/_draft_*.html)",
      "Edit(*:index.html)"
    ]
  }
}
```

若无此文件则创建。授予写入权限的文件类型：`_draft_*.html`（章节草稿）、`index.html`（骨架）、`assemble.py`（拼接脚本副本）。

另外，如果 `.claude/settings.local.json` 中有 `additionalDirectories` 配置，确保当前工作区路径被包含在内，以便子代理能访问工作区文件。

---

## 📝 search_result.md 协同积累机制（核心协同规则）

为保证 7 个并行搜索代理之间不重复劳动、且下游章节规划/撰写能读到一致的最新证据，**所有搜索结果统一沉淀到工作区文件 `search_result.md`**，采用「读上下文 → 搜索 → 返回即追加」闭环。

### 文件位置与生命周期

- 路径：**工作区**根目录 `./research_result/search_result.md`（读写，非 skill 目录）
- 创建时机：**阶段 3 启动前**由主流程初始化（写入文件头）
- 更新时机：**每一个搜索子代理返回后**，主流程立即把其结构化结果追加进去
- 消费方：阶段 4（章节规划）、阶段 5（撰写代理）直接读取该文件作为「已搜索上下文」

### 文件结构（实际格式，基于已验证的生产文件总结）

```markdown
# 搜索结果汇总 (search_result.md)

> 本文件由主流程在每个搜索子代理回传后**自动追加**生成。
> 记录每次回传的「已搜索次数」与「核心结果」，便于过程追溯与断点续跑。

> 生成时间：{DATE}
> 目标：累计 ≥{N} 次真实搜索
> 累计搜索次数：{N}
> 已覆盖子方向：{N}

---

## 学习路径问题诊断

### 答主背景
- 学历 / 已修课程 / 自学经验 / 欠缺 / 当前目标

### 学习路径核心问题
**核心问题**：{一句话概括}

### 关键子问题
1. ...
2. ...
（阶段 1 诊断产物，供下游搜索代理了解上下文）

---

## [{N}] {子方向名称} — 更新于 {ISO 时间戳，含毫秒}

**本次搜索次数**：{N}次（WebSearch）

**核心发现**：
- 发现要点 1
- 发现要点 2

**关键数据/事实**（每条附 URL）：
1. 数据/事实标题
   - 来源：https://...
2. 数据/事实标题
   - 来源：https://...

**存疑/争议**（可选，有则写）：
- 说法 A（来源 X）与说法 B（来源 Y）不一致
- 某数据在不同来源中有显著差异

---
```

**注意**：来源直接内联在 `**关键数据/事实**` 区块下，格式为 `N. 标题\n   - 来源：URL`。**不**单独拆「来源池」区块——来源跟着数据走，拆多了搜索代理反而容易省略。`**存疑/争议**` 为可选项，有矛盾信息时才写，服务于阶段 4 的「争议焦点」提取。

### 主流程闭环（每返回一个代理执行一次，具体追加代码见阶段 3.2）

1. **读上下文**：读取当前 `search_result.md`，提取「已搜索次数总计」与已覆盖子方向，作为派发下一个代理时的去重依据。
2. **追加**：调用下方「阶段 3.2」中的主流程 Python 片段（基于 `os.getcwd()` 与全局变量 `global_search_count`），以 `a` 模式把该代理的结构化结果追加为新区块，自动累加「累计搜索次数」、刷新「最后更新」时间戳。
3. **回读**：追加完成后再次读取 `search_result.md`，作为下一步（派发下一个搜索代理 / 进入阶段 4）的上下文输入。

### 并发安全约定

- 7 个搜索代理仍用 `run_in_background: true` 并行启动，但**写入 `search_result.md` 的动作只允许主流程串行执行**（代理本身不直接写该文件，只把结果回传给主流程）。
- 主流程按代理返回顺序逐条追加，互不竞争，避免并行写文件导致内容错乱。
- 各搜索代理在 Prompt 中被告知「启动前先读取 `search_result.md` 了解已有覆盖」，以尽量减少方向重叠。

---

### 🔒 Skill 目录只读约定（重要！）

用户可能通过指定目录路径的方式引用本 Skill（例如 `{用户目录}/zhihu-research-page`），该目录**是只读的技能定义源**。

| 目录 | 读/写 | 说明 |
|------|-------|------|
| `<skill_dir>/` | **只读** | 技能源码目录，包含 SKILL.md、references/、scripts/ |
| `<skill_dir>/references/css-template.css` | 只读 | 从中读取 CSS 模板 |
| `<skill_dir>/scripts/assemble.py` | 只读 | 从中**复制**到工作区后再编辑 CHAPTERS |
| `{当前工作区}/` | **读写** | 所有产出物的落点：index.html、_draft_*.html、assemble.py |

**铁律**：
- ❌ 绝不修改 `<skill_dir>/` 下的任何文件
- ✅ 所有文件创建/编辑都在当前工作区完成
- ✅ assemble.py 从 skill 目录**复制一份**到工作区，在工作区副本上编辑 CHAPTERS 并运行

---

## 阶段 0：收集输入

向用户确认以下信息（缺省用默认值）：

| 参数 | 默认 | 说明 |
|------|------|------|
| 研究主题 | **从对话上下文自动提炼** | 若用户未明确指定主题，扫描当前对话中涉及的课题/项目/问题域，提炼为一句中文主题 |
| 参考材料 | 空 | 用户提供的文档/链接/笔记，将注入所有子代理 |
| 回答建议 | 按主题自动规划 | 用户可指定 >5 个回答标题 |
| 输出路径 | `./{文件夹名}_{ASCII主题名}.html` | 单文件成品 HTML（图片全部内嵌）路径 |
| 语言 | 中文 | 回答撰写语言 |
| **部分执行比例** | 无（完整执行） | 如用户说"仅执行 3%"，则按比例缩减所有参数（见下方规则） |

> **主题提炼规则**：若用户只说"执行 skill"/N%"版本"而未给主题，**不追问用户**，直接从当前对话上下文中提取——优先扫描最近的课题讨论、项目描述、诊断报告、打开的文件夹名、工作区 `CLAUDE.md` 中项目描述，选最突出的一个作为主题。阶段 1 开头告知用户确认即可。

### 自动同步检查

**每次执行前**，主流程必须：
1. 读取 skill 源 `SKILL.md` 顶部的 `<!-- VERSION:v{N} -->` 注释，与工作区记录的版本对比
2. 若 skill 版本更高 → 将工作区旧文件**剪切**到 `./other/_OLD/` 归档（带时间戳前缀，不覆盖历史），再从 skill 目录复制最新文件

```bash
SKILL_DIR="<skill_dir>"  # 如 ~/.claude/skills/zhihu-research-page
CURRENT=$(cat ./other/.skill_version 2>/dev/null || echo "v0")
LATEST=$(grep -oP 'VERSION:\Kv\d+' "$SKILL_DIR/SKILL.md" | head -1)
if [ "$CURRENT" != "$LATEST" ]; then
  echo "Skill 已更新：$CURRENT → $LATEST，正在同步..."
  TS=$(date +%Y%m%d_%H%M%S)
  mkdir -p ./other/_OLD/"${TS}"
  # 归档旧文件（不覆盖历史记录）
  for f in ./other/assemble.py ./other/scan_html.py ./other/wordcount_check.py; do
    [ -f "$f" ] && mv "$f" "./other/_OLD/${TS}/"
  done
  # 复制新文件
  cp "$SKILL_DIR"/scripts/assemble.py "$SKILL_DIR"/scripts/scan_html.py "$SKILL_DIR"/scripts/wordcount_check.py ./other/ 2>/dev/null
  echo "$LATEST" > ./other/.skill_version
  echo "旧文件已归档到 ./other/_OLD/${TS}/，新文件已就位，继续执行。"
fi
```

### 教程/学习模式

当主题包含 **教程、教学、学习路径、学习、怎么做、入门、指南、上手、怎么用** 等关键词时，自动启用。在阶段 0 额外执行：

1. **提炼答主背景**：从对话上下文提取——已修课程、编程语言掌握程度、有无相关经验、当前项目阶段、已掌握/未掌握的知识点
2. **必要时提问**：若背景信息不足以判断入门门槛（如不确定是否会 Python、是否有 Linux 环境），发起 1~2 个简短确认问题，不追问超过 2 轮
3. **搜索目标调整**：优先搜索面向该背景的入门教程、实战案例、新手常见误区、避坑指南，而非学术文献或高阶架构
4. **写作目标调整**：整页结构设计为"跟着做就能上手"——每章含前置知识标注、操作步骤、预期结果截图描述、常见报错及解决。让答主从头看到尾就能**学会某些技能、扎实理解某些知识点、学会某些操作、会做某些事情**

### 部分执行模式（N% 版本）

当用户指定"仅执行 X% / N% 版本"时，按以下公式等比缩缩，且**主题与上一版本完全相同**。**N 可以是任意正数**（1%、30%、200%、500% 等均支持）。

| 参数 | 完整版 | N% 版本（N 为任意正数） |
|------|--------|-------------------------|
| 工作目录 | 当前工作区 | 新建 `v{M}_{N}pct/`（与上一版本目录同级，M = 上一版本号+1） |
| 搜索次数 | ≥500 | `max(5, floor(500 × N/100))` |
| 每个回答字数 | ≥11,000 | `max(100, floor(11000 × N/100))` |
| 全页字数 | ≥100,000 | `floor(100000 × N/100)`（无额外地板，1% 就是 1000） |
| 回答数 | 10 | `max(3, min(30, floor(10 × N/100)))`（N%≤100% 自动缩为 3~10 个回答；>100% 允许扩到最多 30 个回答） |
| 搜索代理数 | 3 轮串行 | N%≤100% 用 1 个；>100% 按 `min(6, floor(3 × N/100))` 代理 |
| HTML `<title>` | 主题 | `{主题}（{N}%版本）` |
| 知乎问题 `<h1>` | 主题 | `{主题}（{N}%版本）` |
| 答主头像 | DiceBear（默认） | DiceBear，跳过头像搜索 |

**各 N% 示例**：

| N% | 搜索 | 字数/回答 | 总字数 | 回答数 | 适用场景 |
|----|------|---------|--------|--------|----------|
| 1% | 5 | 110 | 1,000 | 3 | 极速预览 |
| 3% | 15 | 330 | 3,000 | 3 | 快速验证 |
| 30% | 150 | 3,300 | 30,000 | 3 | 中速草稿 |
| 100% | 500 | 11,000 | 100,000 | 10 | 完整版 |
| 200% | 1,000 | 22,000 | 200,000 | 20 | 深度加量 |
| 500% | 2,500 | 55,000 | 500,000 | 30 | 超深度（注意 token/时间预算） |

> **实用限制**：N%>300% 时建议分批次交付，避免单次 session token 耗尽。

**铁律**：
- 新目录 `v{N}_{percentage}pct/` 创建在与上一版本目录**同级**（如已有 `v2-学习路径/`，则创建 `v3_3pct/`）
- 目录内按标准约定建 `images/`、`other/`、`research_result/` 子文件夹
- HTML `<title>` 和问题 `<h1>` 必须包含"N%版本"字样，用户打开即知为缩略版
- 主题、大纲结构与上一版本保持一致，仅因子量被等比例压缩

---

## 阶段 1：诊断问题

**在搜索之前**，先对主题做结构化诊断，明确研究的范围和方向。

### 1.1 拆解问题

将用户的研究主题拆解为：
- **核心问题**：1 句话概括用户真正想知道什么
- **关键子问题**：3~5 个，覆盖不同维度（是什么、为什么、怎么办、有没有案例、要不要花钱）
- **预期答案轮廓**：回答这个主题需要覆盖哪几类信息

### 1.2 确定搜索方向

基于诊断结果，规划 7 个搜索子方向（对应阶段 3 的 7 个搜索代理），每个方向一句话描述。确保搜索方向之间互不重叠、加起来覆盖诊断的所有关键子问题。

### 1.3 拟定临时问题标题

给出一个知乎风的问题标题草稿，用于阶段 2 的骨架 HTML。标题应：
- 以问句形式（"XX 是什么？""为什么 XX？""怎么解决 XX？"）
- 有吸引力、能勾起点击欲
- 后续可根据阶段 3 的搜索结果微调

### 1.4 诊断示例

**主题**：排查最近几天 CPU 和磁盘占用异常升高的原因

| 维度 | 内容 |
|------|------|
| 核心问题 | 最近几天系统 CPU 和磁盘 I/O 突然飙升的根本原因是什么？ |
| 关键子问题 | ① 哪个进程/服务占用最高？② 是系统服务还是第三方程序？③ 是否有定时任务/计划任务触发？④ 磁盘 I/O 是随机读写还是顺序读写？⑤ 最近安装了哪些软件/更新？ |
| 7 个搜索方向 | 系统性能监控方法、常见高 CPU 进程排查、磁盘 I/O 诊断工具、Windows 资源监视器分析、Sysinternals 工具链、杀软/索引服务资源占用、最近 Windows 更新已知性能问题 |
| 临时标题 | 最近几天电脑风扇狂转、磁盘灯长亮？可能是这几个原因在搞鬼 |

---

## 阶段 2：创建骨架 HTML（index.html）

### 2.1 使用 CSS 模板

直接读取 `references/css-template.css` 的完整内容，嵌入 `<style>...</style>` 块。**不要修改 CSS**（它已包含完整的知乎设计 Token、顶栏、卡片、回答、侧栏及响应式规则）。

### 2.2 构建 HTML 结构

模板如下（`{...}` 部分根据主题替换）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>知乎 · {主题的一句话问题}</title>
<style>
  /* 粘贴 references/css-template.css 完整内容 */
</style>
</head>
<body>

<header class="zh-header">
  <div class="zh-header__inner">
    <a class="zh-logo" href="#">知乎</a>
    <nav class="zh-nav">
      <a href="#" class="active">首页</a><a href="#">会员</a><a href="#">发现</a><a href="#">等你来答</a>
    </nav>
    <div class="zh-search"><input class="zh-search__input" placeholder="{根据主题填占位}"></div>
    <div class="zh-actions"><button class="zh-btn--follow" style="margin-left:0;padding:4px 16px;font-weight:600;">提问</button></div>
  </div>
</header>

<div class="zh-page"><div class="zh-container">
<main class="zh-main">

  <div class="zh-card">
    <h1 class="zh-question__title">{主题的知乎风问题标题}</h1>
    <div class="zh-question__meta"><span>被浏览 12,847 次</span><span style="margin-left:12px;">关注问题 · 分享</span></div>
    <button class="zh-question__follow">关注问题</button>
    <span style="font-size:14px;color:var(--text-secondary);margin-left:12px;">5 个回答</span>
  </div>

  <!-- 预留 1~2 条引导回答（可选） -->

  <!-- ASSEMBLE -->

</main>

<aside class="zh-sidebar">
  <div class="zh-card zh-sideblock">
    <h3>📑 本页回答</h3>
    <ol><li>（组装时自动填充）</li></ol>
  </div>
</aside>

</div></div>
</body>
</html>
```

### 2.3 CSS 注入方式

从 **skill 目录**（只读）的 `references/css-template.css` 读取，写入**工作区**的 `index.html`。示例：
```python
import os
skill_dir = "<skill_dir>"  # 用户指定的技能目录路径
workspace = os.getcwd()     # 当前工作区
css_path = os.path.join(skill_dir, "references", "css-template.css")
css = open(css_path, encoding="utf-8").read()
html = html.replace("/* 粘贴 references/css-template.css 完整内容 */", css)
# index.html 写入工作区
open(os.path.join(workspace, "index.html"), "w", encoding="utf-8").write(html)
```
**必须完整嵌入** CSS，不缩略。CSS 文件只读，不修改。

---

## 阶段 3：并行搜索（≥500 次真实搜索）

### 3.1 启动搜索代理（配额感知，3 轮串行）

**核心教训**：per-session 搜索配额是主子代理共享硬限——7 代理并行各要求 ≥72 次，总需 ≥504 次，多数代理在 20-30 次即触顶，大量 token 消耗在"尝试→失败→请提升配额"空转。**改为 3 轮串行**：

```python
remaining = 200           # 全局剩余配额（主子代理共享）
agents_per_round = min(3, remaining // 72)  # 每轮最多 3 个，确保每个 ≥72 次
if agents_per_round == 0:
    # 剩余不足 72 次时，剩余配额集中给 1 个代理
    agents_per_round = 1
```

**执行方式**：
- 第 1 轮：3 个代理 × 72 次 = 216 次（如配额足够）
- 第 2 轮：另 3 个代理（剩余配额允许���）
- 第 3 轮：剩余代理
- 每轮串行等待完成后再启动下一轮，避免同时触顶的 token 空转
- 官方文档（espressif、arduino、github docs 等）优先用 `WebFetch` 抓取——不计入搜索配额

**搜索代理通用 Prompt 模板**：完整模板见 `templates/search_agent_prompt.md`。

使用时读入并替换 `{direction}` 占位符：

```python
prompt = open('<skill_dir>/templates/search_agent_prompt.md', encoding='utf-8').read()
prompt = prompt.replace('{direction}', agent_direction)
```

**子代理完成验收标准（重要）**：
- ⚠️ task-notification 元数据声明（"搜索 85 次"等）不可信——实际文件状态才是真相
- ✅ 唯一验收方式：`ls` 检查指定文件已生成 + 文件大小 > 0
- ✅ 代理必须将结构化报告**写入明确的文件路径**（如 `./research_result/report_XX.md`）作为完成凭证
- ❌ 仅通过 SendMessage 回传文本、无文件落盘的，视为未完成

### 3.2 每个代理回传即追加 ./research_result/search_result.md（重要）

> **追加策略**：优先用 Python `open(path, "a")` 追加字符串——比 Edit 工具更稳定（Edit 在 old_string 含反引号/公式/特殊字符时匹配脆弱，易失败需重试）。仅当需要更新文件头计数器时才用 Edit 做精准替换。

**核心要求**：每收到一个搜索子代理的回传，主流程必须**立即**将该代理的结构化报告追加写入工作区的 `./research_result/search_result.md`，而不是等 7 个代理全部回传后再统一处理。

**首次写入（第 1 个代理回传前）**：若 `./research_result/search_result.md` 不存在，先以写入模式创建并写入文件头。文件头应包含「目标搜索次数」「累计搜索次数」「已覆盖子方向」三个实时计数器，并在文件尾预留 `---` 分隔：

```python
import os, datetime
ws = os.getcwd()
path = os.path.join(ws, "research_result", "search_result.md")
target = 504                           # 目标总搜索次数（7 代理 × 72）
header = (
    "# 搜索结果汇总 (search_result.md)\n\n"
    "> 本文件由主流程在每个搜索子代理回传后**自动追加**生成。\n"
    "> 记录每次回传的「已搜索次数」与「核心结果」，便于过程追溯与断点续跑。\n\n"
    f"> 生成时间：{datetime.date.today().isoformat()}\n"
    f"> 目标：累计 ≥{target} 次真实搜索\n"
    "> 累计搜索次数：0\n"
    "> 已覆盖子方向：0\n\n"
    "---\n"
)
open(path, "w", encoding="utf-8").write(header)
```

**注意**：文件头中的 `累计搜索次数` 和 `已覆盖子方向` 每次追加后需由主流程回写更新，以便断点续跑时读取当前进度。

**后续每个代理回传**：以追加模式写入一个区块，并维护全局累计搜索次数 `global_search_count`（主流程内部变量，初始 0）。区块标题统一用 `## [{N}] {子方向名称} — 更新于 {ISO 时间戳}` 格式（精确到毫秒）：

```python
import os, datetime
ws = os.getcwd()
path = os.path.join(ws, "research_result", "search_result.md")

# agent_report      = 该搜索代理回传的结构化报告字符串
# agent_search_count = 代理自报的本方向搜索次数（从报告第 3 项解析）
# global_search_count 已在主流程初始化
# agent_direction   = 该代理负责的方向描述
global_search_count += agent_search_count          # 累加全局计数
batch_no = global_search_count                     # 用累计次数做序号（断点续跑友好）
now_ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # 精确到毫秒

block = (
    f"## [{batch_no}] {agent_direction} — 更新于 {now_ts}\n\n"
    f"**本次搜索次数**：{agent_search_count}次（WebSearch）\n\n"
    f"{agent_report}\n\n"                         # 代理的原始结构化报告
    "---\n\n"
)
with open(path, "a", encoding="utf-8") as f:       # 始终用 "a" 追加
    f.write(block)

# 追加完成后回写文件头中的累计搜索次数和已覆盖子方向（用于断点续跑读取）
content = open(path, encoding="utf-8").read()
content = re.sub(r'> 累计搜索次数：\d+', f'> 累计搜索次数：{global_search_count}', content)
content = re.sub(r'> 已覆盖子方向：\d+', f'> 已覆盖子方向：{batch_no}', content)
open(path, "w", encoding="utf-8").write(content)
```

**文件内容约定**：
- 顶部固定为文件头（含生成时间、目标、累计搜索次数、已覆盖子方向）
- 阶段 1 诊断信息以 `## 学习路径问题诊断` 开头（含答主背景、核心问题、关键子问题）
- 每个搜索代理回传一个 `## [{N}] {方向} — 更新于 {ISO 时间戳}` 区块，包含 `**本次搜索次数**`、`**核心发现**`、`**关键数据/事实**（每条附 URL）`、可选的 `**存疑/争议**`
- 来源直接内联在 `**关键数据/事实**` 区块下，格式：`N. 标题\n   - 来源：URL`
- 区块间用 `---` 分隔
- 保留代理原始结构化报告原文（不做二次加工）

**用途**：该文件是搜索过程的可追溯日志，既可用于断点续跑（下次运行先读文件头的累计搜索次数），也可在阶段 4 规划章节时作为证据参考。

### 3.3 汇总来源池

各代理回传并写入 `./research_result/search_result.md` 后，从所有区块的 `**关键数据/事实**` 下提取 `N. ... \n   - 来源：URL` 格式的链接，合并为一个去重清单。提取正则：`re.findall(r'- 来源：(https?://[^\s\n]+)', content)`。此清单将在阶段 5 传给每个撰写代理。

---

## 阶段 4：规划章节（基于搜索结果的证据驱动）

> **术语说明**：本 skill 内部把每一个「知乎回答」称作一个**章节**——代码里是 `CHAPTERS`、锚点 `ch-01`、草稿文件 `_draft_ch_01.html`。对外呈现时，一个章节 = 页面上一条独立的答主回答。下文「章节」与「回答」同义。

**严禁在搜索之前猜测章节标题。** 章节规划必须基于阶段 3 的搜索发现。

### 4.1 从搜索报告中提取章节主题

分析阶段 3 各搜索代理的结构化报告，提取：
- **高频主题**：多个搜索代理都提到的核心议题
- **争议焦点**：搜索结果中存在不同说法/矛盾的话题（值得单列一章呈现多元观点）
- **知识缺口**：搜索结果中哪些方面信息充分、哪些不足（不足的标注"需在撰写阶段补充搜索"）

### 4.2 设计 10 个章节

确保：
- 逻辑递进（概念→原理→实践→生态/常见方案/避坑）
- 覆盖维度全面（定义背景/技术细节/实战案例/对比选型/未来趋势/社区资源）
- 标题简洁（≤20字）、有吸引力（知乎风）
- **每个章节标题直接对应搜索报告中的具体发现**，不是凭空拟的

### 4.3 填入 CHAPTERS

将章节列表写入**工作区**的 `assemble.py` 的 `CHAPTERS` 变量（此文件是从 skill 目录的 `scripts/assemble.py` 复制到工作区的副本）。参考格式：
```python
CHAPTERS = [
    ("基于诊断命名的章节1",   "ch-01",     ["_draft_ch_01.html"]),
    ("基于诊断命名的章节2",   "ch-02",     ["_draft_ch_02.html"]),
    # ... 其余 8 章
]
```

### 4.4 为每章拟定子方向

为每个章节写 3~5 条预期覆盖要点（传给阶段 5 的撰写代理），这些要点直接来自搜索报告中的发现。如果某章的搜索结果不足，标注"本章需在撰写阶段补充 ≥30 次专项搜索"。

---

## 阶段 4.5：答主身份与头像配置

> **默认策略**：使用 DiceBear 风格化 SVG 头像（稳定、统一、零搜索成本）。仅当用户**明确要求**真实头像时才启动身份搜索——子 agent 搜索真实头像的性价比极低（消耗 ~150 次调用、~64K token、~30 分钟，常见收获仅 8 个可用头像）。

### 头像选取三级优先级

| 优先级 | 来源 | 判定标准 |
|--------|------|----------|
| 1 级 | 真实人物公开头像 | 公开可独立验证的直链（GitHub CDN `avatars.githubusercontent.com/u/<id>`、豆瓣影人页、雪球/掘金/丁香园等平台公开头像、个人官网） |
| 2 级 | DiceBear 风格化 SVG | `https://api.dicebear.com/7.x/{bottts-neutral|avataaars|notionists}/svg?seed=<英文短语>&backgroundColor=<hex>&radius=50`，三种风格交替配合不同配色 |
| 3 级 | 单字符占位 | `<div class="zh-avatar" aria-hidden="true">{首字}</div>`（仅在前两级均不可用时使用） |

**铁律**：
- ❌ 绝不编造图链（包括看似合理的 `<platform>.com/v2-...` 占位路径）
- ❌ 身份不明的真实人物宁弃用（仅查到 ID/账号存在但查不到是谁的，不纳入）
- ❌ 不依赖 WebFetch 测可达（企业策略/网络限制下 WebFetch 常不可靠）

### 完整流程（五步）

#### 步骤 1：通道探测（阶段 4.5 的第一步，只做一次）

先确认本机可用的头像图链源及代理端口：

```bash
# 测 GitHub CDN（通常最可靠）
curl -sI --max-time 5 "https://avatars.githubusercontent.com/u/1" | head -3

# 测 DiceBear API
curl -sI --max-time 5 "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=test" | head -3

# 如有企业代理，补充 -x <代理地址>
curl -x http://proxy:port -sI --max-time 5 "https://avatars.githubusercontent.com/u/1" | head -3
```

记录**实际可达的源**和端口，作为后续验证的基础。不同机器结果可能不同，不预设。

#### 步骤 2：身份搜索与即验（每章独立，可并行）

对每个章节的人设领域，并行派发 ≥2 个子 agent 搜索真实人物公开身份：

```
任务：搜索「{章节领域}」领域的真实公开人物，获取其公开头像 URL。
要求：
- 搜索该领域的知名专家/博主/贡献者（GitHub、技术博客、学术主页等）
- 仅返回可独立验证的人物：姓名明确 + 领域身份可交叉印证
- 头像 URL 必须是公开直链（如 GitHub avatar CDN），非需登录的平台内链
- 身份不明者（仅知 ID 但查不到真实身份）不返回
- 每人返回：姓名、身份简述、头像直链 URL、印证来源
```

**即验**：主流程不等待所有子 agent 回传——候选图链一到就用 `curl -sI` 亲测可达，取"**身份交叉印证 + 图链可达**"双重确认的锚定值。无双重印证的降级到 DiceBear。

#### 步骤 2.5：缓存头像到本地 `./images/`（关键——避免外链失效）

所有确认为有效（图链可达）的头像必须下载缓存到工作区 `./images/` 子目录，HTML 中引用本地路径而非外链：

```bash
# 真实头像：curl 下载并根据 Content-Type 确定扩展名
curl -sL -o "./images/ch-01.tmp" "https://avatars.githubusercontent.com/u/20641750?v=4"
EXT=$(file --mime-type -b "./images/ch-01.tmp" | cut -d'/' -f2 | sed 's/jpeg/jpg/')
mv "./images/ch-01.tmp" "./images/ch-01.${EXT}"

# DiceBear SVG：直接保存为 .svg（远程 API 可能失效或限流）
curl -sL -o "./images/ch-02.svg" \
  "https://api.dicebear.com/7.x/avataaars/svg?seed=arduino-fan&backgroundColor=f4b400&radius=50"
```

**缓存规则**：
- 真实头像保留原始格式（`.png` / `.jpg`），命名 `ch-<序号>.<ext>`
- DiceBear SVG 以 `.svg` 后缀缓存
- 缓存完成后，JSON 映射表中的 `avatar` 字段改为本地相对路径（如 `./images/ch-01.png`、`./images/ch-02.svg`）
- 原始外链保留在 `avatar_remote` 字段供溯源

#### 步骤 3：注入并统一结构（使用本地缓存路径）

将每章作者块统一为以下结构，`src` 指向本地 `./images/` 缓存路径：

```html
<div class="zh-answer__author">
  <div class="zh-answer__author-avatar">
    <img src="./images/ch-01.png" alt="{答主名}头像" width="44" height="44" style="border-radius:50%;display:block">
  </div>
  <div class="zh-author__meta">
    <div class="zh-author__name">{答主名}</div>
    <div class="zh-author__bio">{一句话简介}</div>
  </div>
  <button class="zh-btn--follow" type="button">关注</button>
</div>
```

- 头像路径由阶段 4.5 缓存后确定，**注入到章节写作代理的 Prompt 中**，代理不得自行编造
- DiceBear 示例：`./images/ch-02.svg`
- GitHub 真实头像示例：`./images/ch-01.png`

#### 步骤 4：最终确认（Dump）

注入章节后，用精确命令验证，**不依赖跨行正则**（跨行正则会被换行符截断，误判为未注入）：

```bash
# ✅ 正确的验证方式——grep -o 按行匹配
grep -o 'author-avatar[^<]*' ./other/_draft_*.html | head -20

# 或用 Python 上下文打印
python -c "
import re
html = open('./other/index_skeleton.html', encoding='utf-8').read()
# 找每个 author-avatar 块内容
for m in re.finditer(r'<div class=\"zh-answer__author-avatar\">(.*?)</div>', html, re.S):
    print(m.group(1).strip()[:100])
"
```

**不要**用 `[^>]*` 跨行匹配（会因换行截断匹配不到，误报"未注入"）。

### 4.5 产出

阶段 4.5 完成后，应有一个明确的 JSON 映射表传给阶段 5 写作代理：

```json
{
  "ch-01": {"name": "嵌入式老潘", "bio": "10年嵌入式开发经验", "avatar": "./images/ch-01.svg", "tier": "dicebear"},
  "ch-02": {"name": "创客阿杰", "bio": "Arduino中文社区活跃贡献者", "avatar": "./images/ch-02.svg", "tier": "dicebear"},
  "ch-03": {"name": "开源极客小凯", "bio": "智能硬件独立开发者, GitHub 5K star 项目作者", "avatar": "./images/ch-03.png", "avatar_remote": "https://avatars.githubusercontent.com/u/20641750", "tier": "real", "avatar_source": "GitHub用户头像（仅作视觉素材）"}
}
```

每个章节一条记录，含：
- `name` — 答主名（与章节领域匹配）
- `bio` — 简介，与章节领域匹配
- `avatar` — 本地缓存路径（`./images/ch-XX.<ext>`）
- `tier` — real / dicebear / fallback（仅指头像图源的来源等级）
- `avatar_remote` — 真实头像原始外链（仅 `tier=real` 时存在）
- `avatar_source` — 头像出处说明（如"GitHub用户头像（仅作视觉素材）"）

---

### 5.1 启动 10 个并行撰写代理

在一条消息中批量启动 10 个 Agent（`subagent_type: "general-purpose"`, `run_in_background: true`）。每个代理：
- 负责一个章节
- 必须写入指定的 `_draft_ch_XX.html` 文件
- 用 Python 脚本自验有效中文字 ≥11,000

### 5.2 章节撰写代理 Prompt 模板

完整模板见 `templates/writing_agent_prompt.md`。使用时读入并替换占位符：

```python
prompt = open('<skill_dir>/templates/writing_agent_prompt.md', encoding='utf-8').read()
prompt = prompt.replace('{topic}', topic)
prompt = prompt.replace('{chapter_title}', ch_title)
prompt = prompt.replace('{chapter_points}', ch_points)
prompt = prompt.replace('{chapter_urls}', ch_urls)
prompt = prompt.replace('{chapter_id}', ch_id)
```

- 作者块 HTML 模板见 `templates/author_block.html`
- 写完后运行独立验收：`python -X utf8 scripts/wordcount_check.py ./other/_draft_ch_XX.html`
- 结果 ≥11,000 且与 agent 自述差 ≤5% 才算完成，否则扩写

### 5.3 并行启动方式

```python
for ch in chapters:
    Agent(name=f"writer-{ch.anchor}", subagent_type="general-purpose",
          run_in_background=True, prompt=chapter_prompt)
```

**建议至少额外补充 30~60 次搜索在每个撰写代理中**，用于核实所引用的具体数据点。

---

## 阶段 6：组装与核验

### 6.1 准备脚本（复制到工作区）

从 skill 目录（只读）复制两个脚本到工作区：

```bash
cp <skill_dir>/scripts/scan_html.py ./other/scan_html.py
cp <skill_dir>/scripts/assemble.py ./other/assemble.py
```

编辑工作区副本的 `assemble.py`：将阶段 4 规划的章节列表填入 `CHAPTERS` 变量。`scan_html.py` 无需编辑——它自动扫描所有 `_draft_*.html`。

### 6.2 预扫描 HTML — <code> 标签完整性检查（assembler 兜底，问题消灭在草稿阶段更高效）

**在运行 assemble.py 之前**，必须先运行预扫描：

```bash
# Windows 注意：必须设置编码，否则 emoji 输出崩溃
python -X utf8 ./other/scan_html.py
# 或 set PYTHONIOENCODING=utf-8 && python ./other/scan_html.py
```

> **Windows 编码警告**：`scan_html.py` 使用 emoji（⚠️✅）输出，Windows 控制台默认 cp936 编码会导致 `UnicodeEncodeError`。必须加 `-X utf8` 标志或设 `PYTHONIOENCODING=utf-8`，否则脚本在 Windows 上首次运行即崩溃。

脚本自动检测三类高频 `<code>` 标签问题（子代理生成内容的最大翻车点）：

| 问题类型 | 检测项 | 后果 |
|----------|--------|------|
| A. 开闭不匹配 | `<code>` 开启与 `</code>` 闭合数量不一致 | 后续全文变等宽字体 |
| B. 块级标签嵌套 | `<code>...</code>` 内出现 `<p>`/`<table>`/`<h3>`/`<blockquote>` 等 | `font-family: monospace` 泄漏到正文 |
| C. 异常闭合 | 闭合标签含中文字符（如 `</strong文>`、`</code。>`） | 标签不闭合，浏览器行为不可预期 |
| D. 交叉嵌套 | `<code>` 与 `<strong>` 开闭顺序交叉 | 字体继承链断裂 |

若发现问题，按报告逐文件修复（常见修复：把 `<code>` 内的块级标签移到外面，补上缺失的 `</code>`，修正错位的 `</strong>`）。修复后重跑 `scan_html.py` 确认清零，再进入 6.3。

> **排查优先级（重要）**：当用户引用本 skill 要求"修复网页结构问题"或"字体异常/全是等宽字"时，**优先排查 `<code>` 标签完整性**，而非修改 CSS。99% 的字体泄漏和结构异常来自 `<code>` 标签封闭不当，`css-template.css` 本身已验证无误。

### 6.3 运行 assemble.py

```bash
python ./other/assemble.py
```

脚本会依次：
1. 补 h2/h3 样式（若缺失）
2. 剥离旧章节（幂等），注入锚点 id
3. 一次性将全部章节替换骨架的 `<!-- ASSEMBLE -->` 占位标记
4. **去重 `<style>` 块**：内容相同的只保留首次出现
5. **统一硬编码主题蓝**：蓝系 hex → `var(--zhihu-blue)`，非蓝系保留
6. 自动更新回答数
7. 重建侧栏（纯章节导航）
8. **自动自查**（5 项，不通过立即终止）：
   - ① `:root` 中 `--zhihu-blue` 定义数（须为 1）及 `var()` 用法数
   - ② 检测残留硬编码蓝系 hex（非 `:root` 行）
   - ③ 重复 `<style>` 块检测
   - ④ `.zh-answer__body code` 样式一致性校验
   - ⑤ `.zh-body` 类名出现次数（须为 0）
9. 写入成品 HTML
10. 打印每章及总计有效中文字数

> **CSS 类名隔离**：页面级包裹层已改名为 `zh-page`（v14 前叫 `zh-body`）。同名类在不同层级复用会导致模板强调色泄漏——assemble.py 的去重（步骤 4）和颜色归一（步骤 5）已内置防护。章节草稿内覆盖样式建议用更具体的选���器链（如 `#ch-01 .zh-body h2`）。

### 6.4 幂等性注意事项

`assemble.py` 首次运行后会**消费**骨架中的 `<!-- ASSEMBLE -->` 占位标记。如果需要在同一次会话中重跑（如补完章节后再次拼接），需先手工恢复占位符：

```bash
# 用 sed/Python 把已注入的章节替换回占位标记
python -c "
import re
html = open('./other/index_skeleton.html', encoding='utf-8').read()
# 找 </main> 的位置，在它前面还原占位符
html = re.sub(r'(\s*)(</main>)', r'\n  <!-- ASSEMBLE -->\n\2', html, count=1)
open('./other/index_skeleton.html', 'w', encoding='utf-8').write(html)
"
```

或更简单的方式：在最初写骨架时保存一份原始副本 `index_skeleton.html`，每次重跑前还原。

### 6.5 判断达标

若 `总计 < 100,000`：
- 找出最薄弱的 2~3 章（有效字最少的）
- 返回阶段 5，用独立 Agent 聚焦扩写补足
- 重跑 scan_html.py → assemble.py 直至达标

若 `总计 ≥ 100,000`：进入阶段 7。

> **N% 模式注意**：运行 `assemble.py` 前先编辑 `TARGET_WORDS = floor(100000 × N/100)`，避免 N% 版本误报"还差 97801 字"。Windows 运行统一使用 `PYTHONIOENCODING=utf-8 python ./other/assemble.py`，防止 emoji 输出在 GBK 控制台崩溃。

---

## 阶段 7：交付与收尾

### 7.1 结构校验

确认成品 HTML 中：
- 含 `zh-header`、`zh-sidebar`、`zh-main`、`</main>` 等关键结构
- `<article>` 数与回答数匹配
- 章节锚点 id 与侧栏导航 href 一致
- `<code>` 标签开闭数量匹配（可用 `grep -c '<code' ./other/_draft_*.html` 和 `grep -c '</code>' ./other/_draft_*.html` 快速核对）
- 无 `<code>...</code>` 内嵌套块级标签（若阶段 6.2 scan_html.py 已通过则无需重检）
- 每章作者块含 `zh-answer__author-avatar` 且有非空 `src`（用 `grep -o 'author-avatar[^<]*' ./other/_draft_*.html` 逐行确认，不依赖跨行正则）

### 7.2 链接抽检

用 WebFetch 对 2~3 条最关键的官方/核心链接做可达性验证，确保不是死链。

### 7.3 打包单文件 HTML（图片全部 base64 内嵌）

把 `index.html` 里所有本地图片转成 base64 data URI，输出可独立分发的单文件 HTML，然后删除 `index.html`。

**命名规则**：`{工作区文件夹名}_{ASCII 主题名}.html`
- 文件夹名 = `basename(cwd)`，如 `v3_5pct`
- ASCII 主题名 = 由阶段 1 拟定标题**意译成英文**：中文→英文（不是拼音）、单词首字母大写、空格→`-`、去标点、每个词首字母大写、≤32 字符
- 例：
  - 「什么是 Harness Engineering？」→ `v3_5pct_What-Is-Harness-Engineering.html`
  - 「国际象棋怎么学？」→ `v2_How-to-Learn-Chess.html`
  - 「各种调式的流行歌曲都有什么特点」→ `v2_Musical-Modes-in-Pop-Music.html`
- 主题过长时保留核心词，删修饰语，确保 ≤32 字符

```bash
python -X utf8 <skill_dir>/scripts/inline_images.py \
  --src index.html \
  --topic What-Is-Harness-Engineering
```

脚本行为：
1. 替换三类图片引用：`<img src>` / `<style>` 与 `style=` 内的 `url()` / `<source srcset>`
2. 缺失图片保留原路径并打印警告，不中断
3. 生成新文件后做**三重校验**，通过才删除 `index.html`
4. 打印 `内嵌 N 张 / 缺失 M 张 / X KB -> Y KB`

**三重校验（缺一不可，防止删了原文件但新文件是坏的）**：
- 新文件含 `zh-header` 与 `</main>`
- 新文件 `<article ... id="ch-` 计数 == 原文件
- 新文件 `data:image/` 出现次数 ≥ 成功内嵌张数

校验失败 → 两个文件都保留，报错终止，**不得交付**。

### 7.4 交付

运行 `present_files` 交付**单文件 HTML**（`{文件夹名}_{ASCII主题名}.html`），并通报：
- 全页有效中文字数
- 各章字数分布
- 搜索总次数
- 外链总数
- 链接抽检结果
- 单文件体积 + 内嵌图片张数

### 7.5 可选：上传 WorkBuddy 资料库

交付完成后，**主动询问一次**：

> 是否将 `{文件名}.html` 上传到 WorkBuddy 资料库？（保存为「网页」，仅你私有、可检索，不生成分享链接）

- 用户同意 → 调用 `LibraryUpload`，`path` 传**绝对路径**
- 用户拒绝或未回应 → 跳过，不影响交付
- 单文件 > 100 MiB → 直接告知「体积超限，不支持上传」，不要再问

**铁律**：
- ❌ 不得自动上传（对外动作，必须先问）
- ❌ 不得替用户回答

### 7.6 工作记忆

使用模型的 Memory 机制，将任务完成记录追加到当前工作区的 `.workbuddy/memory/YYYY-MM-DD.md`。不要硬编码绝对路径。

---

## 质量规则（贯穿全局）

| 规则 | 标准 |
|------|------|
| 有效中文字数口径 | 去 `<script>`/`<style>`/所有 HTML 标签后的汉字（`\u4e00-\u9fff`）+ 中文标点（`\u3000-\u303f`、`\uff00-\uffef`），英文代码和英文链接文本不计 |
| 链接真实性 | 禁止编造任何 URL，每个链接必须来自真实搜索或已核验来源池 |
| 搜索次数 | 阶段 3 总搜索 ≥500 次；阶段 5 每章再补 30~60 次用于核实 |
| 每章字数 | 每章 ≥11,000 有效中文，全页 ≥100,000 |
| 风格一致 | 所有章节必须用知乎回答体，含作者块 + 操作条 |
| 诚实性 | 不同版本/来源的矛盾信息如实标注，不隐瞒不谈化 |
| 结构完整性 | 拼接后 HTML 含顶栏/问题头/侧栏/页脚，不丢 CSS class |
| <code> 标签 | 每章 `<code>` 开闭数量必须匹配，`<code>` 内不得嵌套块级标签；严禁 `<code>` 与 `<strong>` 交叉嵌套 |
| 头像真实性 | 禁止编造头像图链；真实人物身份须交叉印证（≥2 独立来源）；图链须经 curl 亲测可达；不足时诚实降级 DiceBear |
| 作者块统一 | 所有章节作者块使用同一 HTML 结构（`zh-answer__author-avatar > img`），禁止变体；头像 URL 由阶段 4.5 统一配置 |
| 图片路径 | 网页中所有 `<img>` 的 `src` 必须指向本地 `./images/` 相对路径（如 `./images/ch-01.png`），禁止外链图片 |
| CSS 类名隔离 | 页面级包裹层使用 `zh-page`（非 `zh-body`），章节正文容器使用 `zh-answer__body`；避免同名类在不同层级复用；多个 `<style>` 块合并去重 |
| 组装前扫描 | 运行 `assemble.py` 前必须先跑 `scan_html.py`，问题清零后方可拼接 |
| 单文件交付 | 交付物必须是单文件 HTML：所有 `<img src>` 与 CSS `url()` 均为 `data:` 内嵌，零外链图片；`index.html` 打包后删除 |
| 删除前校验 | 删除 `index.html` 前必须通过三重校验（`zh-header` + `</main>`、`<article id="ch-` 计数一致、`data:image/` 计数达标）；校验失败两个文件都保留 |
| 资料库上传 | 必须先询问用户；不得自动上传；单文件 > 100 MiB 直接跳过并告知体积超限 |

---

## 报错与降级

| 异常 | 处理 |
|------|------|
| 某搜索代理返回 <50 条来源 | 要求该代理补充，或补派一个额外搜索代理 |
| 某章节有效字 <11,000 | 要求该撰写代理扩写，或补派一个"扩写代理"追加内容到同文件 |
| assemble.py 提示某文件缺失 | 检查文件名映射，更新 CHAPTERS 候补列表 |
| 组装后全页 <100,000 | 找出最弱 3 章，每章补 ≥(缺口÷3+2000) 字 |
| 撰写代理报错（无来源/编造 URL） | 在对应章节末尾追加警告标记，必要时重写该章 |
| scan_html.py 报 <code> 问题 | 逐文件手工修复后重跑 scan_html.py 确认清零，再进入 assemble.py |
| 组装后页面字体异常/全是等宽字 | **优先排查 <code> 标签完整性**（而非修改 CSS），运行 scan_html.py；常见根因是 <code> 内嵌套了块级标签 |
| assemble.py 二次运行无效 | `<!-- ASSEMBLE -->` 首次运行后被消费，需手工还原占位符（见 6.4）或从 `index_skeleton.html` 还原骨架 |
| 子代理 Write/Bash 权限被拒 | 检查 `.claude/settings.local.json` 中 permissions.allow 是否包含 Write/Edit/Bash 对 `_draft_*.html` 的授权（见阶段 6 前置说明） |
| 头像图链全不可达（通道探测失败） | 降级到 DiceBear 风格化 SVG，标注"本轮头像因网络限制使用 DiceBear 替代" |
| 真实人物身份无法交叉印证 | 降级到 DiceBear，标注原因（如"GitHub 用户 X 身份无法确认，以 DiceBear 替代"） |
| 组装后 author-avatar 缺失 | 用 `grep -o 'author-avatar[^<]*' ./other/_draft_*.html` 逐行确认（不依赖跨行正则），缺失的章节回阶段 4.5 补配头像 |
| 搜索代理集体触顶（主配额耗尽） | 减少并发数至 `floor(剩余配额/72)`，优先 WebFetch 抓取官网文档（不计入搜索配额） |
| scan_html.py 在 Windows 上报 UnicodeEncodeError | 加 `-X utf8` 标志运行：`python -X utf8 ./other/scan_html.py`；或 `set PYTHONIOENCODING=utf-8` |
| 撰写代理 `<code>` 自检不通过 | 代理在草稿完成后立即修复 `<code>` 开闭/嵌套问题；问题消灭在草稿内，避免 assemble 阶段重跑多轮 |
| inline_images.py 报「缺失 M 张」 | 核对 `./images/` 实际文件名与 HTML 引用（常见为大小写差异或 curl 下载失败），补图后重跑；只差 1-2 张可接受，但需在交付通报中说明 |
| 单文件 HTML > 100 MiB 无法上传资料库 | 交付本身不受影响，仅告知体积超限；如需上传，先压缩 `./images/`（转 webp / 降分辨率）再重跑 `inline_images.py` |

---

## 资源文件

- `references/css-template.css` — 知乎风格 CSS（直接嵌入 `<style>`）
- `scripts/assemble.py` — 通用拼接与字数核验脚本（使用前编辑 CHAPTERS）
- `scripts/scan_html.py` — HTML `<code>` 标签预扫描脚本（assembly 前兜底）
- `scripts/wordcount_check.py` — 独立字数核验 + `<code>` 完整性检查（每章写完后运行）
- `scripts/inline_images.py` — 单文件 HTML 打包脚本（图片 base64 内嵌 + 删 index.html 前三重校验）
- `templates/writing_agent_prompt.md` — 章节撰写代理 Prompt 模板
- `templates/search_agent_prompt.md` — 搜索代理 Prompt 模板
- `templates/author_block.html` — 统一作者块 HTML 模板
- `TROUBLESHOOTING.md` — 15 类高频异常及处理方法（遇到异常先读此文件）
