# OpenClaw Context Budget 🎛️

<div align="center">
  <strong>上下文检查 / 上下文优化</strong> | <a href="README.en.md">🌐 English</a>
</div>

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="OpenClaw Context Budget — 把每个已启用模型的上下文窗口设为厂商标称的 60%；流程：检测 → 决策 → 执行">
</p>

> 上下文优化「调音师」：检测当前已启用的模型，去各厂商官方来源取最新标称窗口，按 **60%** 给出建议值——你回一个数字，它才写入配置并校验。
> OpenClaw context check / context optimization: enumerates the enabled models, fetches each vendor's published context length, proposes 60% of it, and applies only after a one-digit confirmation.

![license](https://img.shields.io/badge/license-MIT-green)
[![ClawHub downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fxiaoyaoclaw-context-budget&query=skill.stats.downloads&label=ClawHub%20downloads&color=blue)](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-context-budget)

## 为什么需要

各家模型的上下文窗口差别很大（200K / 1M…），而 OpenClaw 在模型未声明窗口时会退回一个**兜底默认值**，于是：

- 📉 **窗口被低估**：上下文**过早自动摘要**、长任务被打断、压缩时卡顿
- 📈 **窗口被高估**：模型在超长上下文里**注意力分散**，回答质量下滑
- 🧾 **配置无来源**：配置里那个数字是谁填的、依据是什么，无处可查
- 🧮 **比例算不过来**：「留 60% 余量」这条经验要人工换算成绝对 token 数，每个模型都算一遍

手工做法是：逐个查厂商官网 → 自己乘 60% → 改配置 → 重启验证。**这个 skill 把这一串变成一次检测 + 一个数字。**

## 特性

- 🎯 **固定最佳实践**：有效窗口 = 厂商标称窗口 × **60%**（留余量，减少注意力分散）
- 🔎 **动态枚举**：模型清单**运行时从配置读取**（在用 + 图像/PDF 这类旁路在用），不写死任何厂商或模型
- 🌐 **官方来源取数**：每次联网到厂商官方文档/接口取**最新**标称窗口，来源与抓取时间写在决策卡上
- 1️⃣ **一个数字确认**：流程 = 检测（只读）→ 决策（回一个数字）→ 执行（确认后写入），无需读文档
- 🧱 **只碰窗口**：`maxTokens` 等其它参数、压缩阈值（保持系统默认）**一律不动**
- 🕊️ **不留痕**：不写审计文件、不建历史清单；仅记录本次被改字段的旧值用于一步回退（一次性、覆盖式）
- 📦 **纯指令式**：无脚本、无数据文件、无第三方依赖，不联网装包，跨安装形态一致
- ↩️ **可回退**：一条指令撤销**本次**调整（记录只在会话内、不落盘）
- 🛡️ **写操作透明**：**只写窗口字段**；写入**必须经你确认**（决策卡回 `1`），走 `config.patch`；**不擅自重启运行时、不擅自清理会话状态**（只提示）；写完校验运行态并如实报差异
- 🔒 **联网只取数**：仅访问厂商官方来源读取标称窗口，不上传任何本地数据
- 👀 **读取范围受限**：只读**窗口相关字段**（模型 id / 窗口 / 输出上限 + 各 agent 的模型引用）；**不读取、不回显密钥或其它无关配置**
- ⏱️ **不做自动化**：**本技能不会自动运行**（无定时任务、无后台行为、不监听配置变化）

## 安装

```bash
# ClawHub（推荐）
clawhub install xiaoyaoclaw-context-budget

# 或从 GitHub 手动安装
git clone https://github.com/dtsola/xiaoyaoclaw-context-budget
# 把 SKILL.md 放到你的 skills 目录
```

## 使用

1. 把 skill 放到 OpenClaw 的 skills 目录
2. 对你的 agent 说：**「上下文优化」** / 「上下文检查」 / 「把上下文窗口配一下」
3. agent 先检测 → 给你一张决策卡 → 你回 `1` 采纳 → 它写入并校验，回报三行结果

触发词（自然语言即可）：上下文优化 / 上下文检查 / 检查上下文 / 优化上下文 / 上下文窗口检查 / 上下文体检 / 检查一下模型上下文
斜杠命令：`/xiaoyaoclaw-context-budget`

## 🚀 快速上手（三步，1 分钟）

### Step 1：安装技能

```bash
clawhub install xiaoyaoclaw-context-budget
```

装完你的 agent 就多了一项「上下文优化」能力，不需要任何 API key。

### Step 2：说一句话

> 上下文优化

agent 会：① 盘你系统里**在用**的模型 → ② 去各厂商官方来源取最新标称窗口（约 30–60 秒）→ ③ 给你决策卡：

```
🎛️ 检测到 1 项可调整
· <provider>/<model>（在用）｜ 官方标称 1,000,000 ｜ 现值 200,000 → 建议 600,000
· <provider>/<model>（在用）｜ 官方标称 1,000,000 ｜ 现值 600,000 ✅ 无需调整
回 1 采纳 ｜ 2 保持现状 ｜ 3 看详情
```

### Step 3：回一个数字

回 `1` → 它写入配置、刷新、校验，回报：

```
✅ 已改 1 项：<provider>/<model> 200,000 → 600,000
校验通过（窗口已生效）
如需回退回「撤销本次调整」
```

### 日常使用习惯

| 场景 | 做法 |
|---|---|
| 首次配置 / 定期检查 | 说「上下文优化」，看卡回一个数字 |
| 新增 / 更换模型 | 说「我换模型了，把窗口配上」——只针对新模型出卡 |
| 想调比例 | 说「上下文优化，比例用 50%」（默认 60%） |
| 怀疑长任务被打断 | 说「上下文优化」，先检测再给结论（不直接改） |
| 改错想退回（同一会话内） | 说「撤销本次调整」——记录只在会话内、不落盘 |
| 只看不配 | 决策卡阶段回 `2`（零改动），或回 `3` 看详情 |

## 和手工配置对比

| | 手工查官网 + 手填 | **xiaoyaoclaw-context-budget** |
|---|---|---|
| 取数 | 逐个逛厂商文档，靠印象 | ✅ 官方来源取最新值，附来源与时间 |
| 换算 | 自己乘 60%，容易算错 | ✅ 自动算，比例可临时指定 |
| 覆盖面 | 常漏掉图像/PDF 这类旁路模型 | ✅ 动态枚举在用 + 旁路在用 |
| 生效确认 | 改完靠感觉 | ✅ 写入后校验运行态，如实报差异 |
| 出错成本 | 不知道改前是什么 | ✅ 一条指令回退 |
| 干扰面 | 容易顺手改到别的参数 | ✅ 只碰窗口字段，其它参数一律不动 |

## 目录结构

```
xiaoyaoclaw-context-budget/
├── SKILL.md                    # 技能主体（口径 / 三段式流程 / 硬规则自检 / 触发词）
├── assets/readme/
│   ├── hero.svg                # README 封面（纯 SVG）
│   └── community-qr.png        # 交流群二维码
├── docs/
│   └── DESIGN.md               # 设计文档（机制取证 / 口径 / 流程 / 边界）
├── skill-card.md               # ClawHub 技能卡（描述 / 用例 / 风险与缓解）
├── README.md / README.en.md
└── LICENSE
```

## License

MIT — 随便用，署名可选。

---

## 🛠️ 需要定制？

**Agent & Skills 定制，价格 ¥800 起。**

- 微信：`dtsola`（添加好友时备注：**openclaw定制**）
- 服务范围：OpenClaw 多 agent 部署 / 工作区规范化 / 自定义 Skill 开发 / agent 记忆系统搭建 / 知识库搭建

## 💬 加入交流群

小遥全系产品用户交流群——产品反馈 · 使用交流 · 功能建议：

<p align="center">
  <img src="./assets/readme/community-qr.png" width="280" alt="小遥AI 用户交流群二维码：扫码加群，或添加微信 dtsola（备注：加群）">
</p>

<p align="center">扫码加群，或添加微信 <code>dtsola</code>（备注：<b>加群</b>）</p>

## 姊妹项目

- 🏠 **xiaoyaoclaw-workspace-initializer**（工作区初始化器）：给每个 agent 一个「家」——标准目录结构 + WORKSPACE.md 规范 + 多 agent 配置安全。<https://github.com/dtsola/xiaoyaoclaw-workspace-initializer>
- 🧠 **xiaoyaoclaw-memory-distill**（记忆蒸馏）：把对话蒸馏成 MEMORY.md + 日常日志，解决上下文溢出。<https://github.com/dtsola/xiaoyaoclaw-memory-distill>
- 🗂️ **xiaoyaoclaw-task-progress-tracker**（任务进度跟踪器）：目录即容器，PROGRESS.md 即进度——tasks/ 与 projects/ 生命周期管理。<https://github.com/dtsola/xiaoyaoclaw-task-progress-tracker>
- 📚 **xiaoyaoclaw-kb-retriever**（知识库检索器）：本地知识库检索——分层 data_structure.md 索引导航 + 渐进式检索（md/pdf/xlsx），无需 API key，Windows / macOS 双平台。<https://github.com/dtsola/xiaoyaoclaw-kb-retriever>
- 📎 **xiaoyaoclaw-web-clipper**（网页剪藏）：把任意网页保存为带 frontmatter 的本地 Markdown——双引擎正文提取（readability + trafilatura 降级链）、中文文件名安全、批量剪藏 + 去重。<https://github.com/dtsola/xiaoyaoclaw-web-clipper>
- 🤝 **xiaoyaoclaw-agent-orchestrator**（Agent 协作编排，**协作层**）：架在生态之上——拆任务、分 agent、管进度、聚结果、失败重试。<https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator>
- 📊 **xiaoyaoclaw-usage-report**（用量报告）：解析 session JSONL，回答「每次 agent 任务花了多久、用了哪些工具/技能/模型、消耗了多少 token」——零依赖纯本地。<https://github.com/dtsola/xiaoyaoclaw-usage-report>
- 🩺 **xiaoyaoclaw-workspace-auditor**（工作区体检，只读审计）：目录合规 / 任务健康 / 记忆日志 / 知识库索引 / 垃圾文件，分级报告 + 修复建议。<https://github.com/dtsola/xiaoyaoclaw-workspace-auditor>
- 🎛️ **xiaoyaoclaw-commander**（跨工具指挥官，**指挥层**）：让任意支持 Agent Skills 的工具（Claude Code / Codex / OpenCode / Trae / DSH）指挥小遥Claw / OpenClaw 多 agent 系统。<https://github.com/dtsola/xiaoyaoclaw-commander>
- 🔍 **xiaoyaoclaw-seo-skill**（SEO 技能）：网站搜索可见性分析与优化——audit / page / content / schema / geo 五流程 + 零依赖审计脚本。<https://github.com/dtsola/xiaoyaoclaw-seo-skill>
