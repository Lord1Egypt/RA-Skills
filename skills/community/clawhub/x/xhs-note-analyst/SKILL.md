---
name: xhs-note-analyst
slug: xhs-note-analyst-v2
displayName: xhs 账号诊断 · 创作者后台数据漏斗体检 + 对标爆款
version: 1.1.6
summary: 用你自己的创作者后台官方数据做账号体检（rednote analytics 数据洞察）。导出最近 N 条笔记的官方数据（曝光/封面点击率/涨粉/人均观看时长），逐条提炼关键词搜同题材爆款做对标，生成含①数据总表②转化漏斗健康度诊断③逐条笔记对标爆款+改进动作的 HTML 报告。不需要任何第三方 API key 或付费额度，用你 Chrome 里已登录的账号跑。当用户要分析"我自己的账号"最近笔记表现、点击率/互动/涨粉为什么不行、或想给笔记找对标爆款和优化动作时唤起。
description: 用你自己的创作者后台官方数据做账号体检。导出最近 N 条笔记的官方数据（曝光/封面点击率/涨粉/人均观看时长），逐条提炼关键词搜同题材爆款做对标，生成含①数据总表②转化漏斗健康度诊断③逐条笔记对标爆款+改进动作的 HTML 报告。不需要任何第三方 API key 或付费额度，用你 Chrome 里已登录的账号跑。当用户要分析"我自己的账号"最近笔记表现、点击率/互动/涨粉为什么不行、或想给笔记找对标爆款和优化动作时唤起。
license: MIT
---

# 账号分析（xhs-note-analyst）

> **⚠️ 本 skill 无法独立运行，必须先安装 webclaw3。**
>
> 它依赖 webclaw3 提供的本地浏览器运行时（Relay `:3459` + pipeline `:3460`），直接复用你 Chrome 里已登录的账号——不必重新登录、不必交出密码、不易被站点访问限制拦截。**没有 webclaw3，本 skill 的每一步浏览器操作都会立即失败。**
>
> ```bash
> npx clawhub@latest install fatmind/webclaw3-browser-automation
> ```
>
> 主品页面：https://clawhub.ai/fatmind/skills/webclaw3-browser-automation
> 源码与安装指南（3 步，约 5 分钟）：https://github.com/fatmind/webclaw3
>
> 装好后对你的 Agent 说一句「检查 webclaw3 环境」确认 Relay 与 pipeline 就绪，再回来跑本 skill。

## 功能描述

分析**你自己的**账号，数据来自你的创作者后台官方看板（导出 Excel），不是爬来的第三方估算数字。流程：导出最近 N 条笔记（按首发时间倒序）→ 逐条提炼精准关键词 → 搜该词下的同题材爆款做对标 → 输出一份 HTML 报告：

1. **数据总表**：`min(notes_count, 实际笔记数)` 条，含标题/**类型（图文/视频）**/首发时间/**已发布天数**/曝光/**日均曝光**/观看量/封面点击率/点赞/评论/收藏/涨粉/分享/人均观看时长，按首发时间倒序；
2. **转化漏斗健康度诊断**：点击率 → 内容留存 → 互动 → 涨粉 四层，各有数值与合格/偏弱/断档判断（点击率 10%–20% 合格；互动率 5%–10% 为爆款线；留存断档线按体裁分设）；
3. **逐条笔记**：每条含 对标爆款表（同题材、过点赞门槛的高赞笔记，含标题+作者+点赞数）+ 3 条具体可执行的改进动作。

**目标口径（2026-09-17 定）**：核心目标是**涨粉**，逐条笔记的改进动作必须能落到涨粉链路上（关注钩子/系列感/封面 CTR），「有用但不涨粉」型结论要显式指出。输出强制收成三段，逐条笔记最后汇总为一节：**诊断**（哪层漏斗断了，官方数据说话）→ **归因**（封面/标题/正文结构/关注钩子的哪一环）→ **动作**（下一条笔记具体改什么，一句话一条）。动作写完还要回填实验体系：扫 `xhs-growth/lab/try/*/experiment.md` 找已到采集点（D+1 早期信号 / D+3 判定）的进行中实验，官方数据落快照到 `xhs-growth/lab/try/<exp-id>/`；D+3 复盘写方向对应的 `xhs-growth/lab/review/dir-XXX.md`（一个方向一份，只写判定和背后思考，具体改动落方向文件）。

**和市面上的 skill 有什么不同**：

- 大多数是**爬别人的数据**（榜单、竞品、KOL），本 skill 看的是**你自己的后台真实数据**——曝光、封面点击率、人均观看时长、涨粉数这些指标只有账号主人拿得到，爬虫拿不到；
- **不需要任何第三方数据平台的 API key，也不消耗付费额度**：数据源就是你自己的创作者后台，浏览器动作由本机 webclaw3 运行时驱动；
- 竞对侧只取搜索结果页**公开可见**的标题、作者与点赞数，不抓取任何登录后才可见的他人数据。

## 前置条件

- **webclaw3 已安装并运行**（见顶部安装说明）：它提供浏览器扩展与 Relay（HTTP `:3459`），以及本地 pipeline 服务（`:3460`）——本 skill 内嵌的 LLM 子会话（关键词提炼 / 对标爆款筛选 / 改进动作生成）都经 pipeline 代跑。
- 浏览器已登录创作者后台（creator 后台）与主站——你日常 Chrome 的登录态由 webclaw3 直接复用，无需重新登录。
- 本机安装 `python3` 与 `openpyxl`（用于解析创作者后台导出的 Excel 明细表）。
- 浏览器下载目录为 `~/Downloads`（导出 Excel 会落到这里）。

## 使用方式

```bash
node skill.mjs
```

从当前目录 `input.json` 读取入参；`input.json` 不存在时使用默认值。

## 入参（input.json）

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `notes_count` | int | 5 | 分析最近多少条笔记（按首发时间倒序） |
| `keyword_per_note` | int | 1 | 每条笔记提炼的关键词数量 |
| `report_path` | string | `<cwd>/账号分析报告_<日期>.html` | 报告输出路径 |
| `output_dir` | string | `/tmp/xhs-note-analyst-output` | 产出 res.json / data.md / HTML 报告的目录 |
| `output_files.result` | string | `res.json` | 状态摘要文件名 |
| `output_files.data` | string | `data.md` | 数据明细文件名 |

## 输出

- **`report_path`**：HTML 报告（本地可直接打开预览），含三个板块与 full/partial 标注；
- **`res.json`**：`{ status, summary, notes_count, note_count_analyzed, keywords, benchmark_shortages, report_path, output_dir }`，`status` ∈ success / partial / failed；
- **`data.md`**：报告的数据明细版（总表/漏斗/逐条笔记/执行过程记录）；
- **stdout**：一行 JSON 摘要 `{ status, summary, output_dir }`。
