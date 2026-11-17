# OpenClaw Agent Orchestrator 🤝

<div align="center">
  <strong>🇨🇳 中文</strong> | <a href="README.en.md">🌐 English</a>
</div>

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="OpenClaw Agent Orchestrator — multi-agent daily collaboration: split tasks, dispatch via sessions_send, track progress, aggregate results, retry failures">
</p>

> 多 Agent 日常协作编排器——把「拆任务 → 分 agent → 管进度 → 聚结果 → 失败重试」封装成标准工作流，让多个常驻 agent 像团队一样协作。
> OpenClaw multi-agent daily collaboration orchestrator — split tasks, dispatch to resident agents via sessions_send, track progress, aggregate results with source attribution, retry failures (default max 3).

![license](https://img.shields.io/badge/license-MIT-green)
[![ClawHub downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fxiaoyaoclaw-agent-orchestrator&query=skill.stats.downloads&label=ClawHub%20downloads&color=blue)](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-agent-orchestrator)

## 为什么需要它

你有多个 OpenClaw agent（绘图 / 调研 / 编码……），想让它们并行干活时，常见问题：
- ❌ **手动配通道**：跨 agent 要改两层配置（visibility + agentToAgent），allow 还要求**双向**，一堆坑
- ❌ **手动一个个发**：让 A 画图、B 调研、C 汇总，得自己挨个 sessions_send
- ❌ **等得焦虑**：sessions_send 60s 超时，不知道对方在跑还是死了
- ❌ **手动拼结果**：各 agent 回复散落各处，汇总全靠手
- ❌ **失败没人管**：某 agent 任务失败，整个流程卡住

这个 skill 一次性解决：**一句话派活 → 自动分发 → 进度透明 → 带来源汇总 → 失败自动重试（≤3 次）**。

## 特性

- 🤝 **强制 sessions_send**：任务发到对方**常驻会话**——完整人格 + 记忆 + 技能，像真实同事一样干活
- 🚦 **三档触发**：点名/编排动词直接执行；模糊大任务**先问一句**；日常问答保持沉默——从不抢活
- 🔀 **并行分发**：多个子任务同时发出（fire-and-forget），总时长 ≈ 最慢那个，不串行等
- 📡 **进度透明**：sessions_list / sessions_history 实时查状态，**60s 超时 ≠ 失败**（任务后台继续）
- 📊 **带来源汇总**：聚合报告标注「哪条结论来自哪个 agent」，可追溯
- 🔁 **失败重试**：默认最多 3 次（可配置），重试带上下文（不重复已完成部分）；3 次仍败上报用户
- 📖 **直接读 openclaw.json**：agents.list + agentToAgent.allow 双向白名单，真相源只有一个，不搞探测
- 🐍 **零依赖脚本**：配置检测 + 状态汇总，纯 Python 标准库，Windows / macOS 双平台

## 安装

```bash
# ClawHub（推荐）
clawhub install xiaoyaoclaw-agent-orchestrator

# 或从 GitHub 手动安装
git clone https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator
# 把 SKILL.md、references/、scripts/、templates/ 放到你的 skills 目录
```

## 使用

### Step 1：配置自动检测（一般不用管）

技能启动时会自动检测多 agent 配置：
1. `agents.list` 里配置了多个 agent
2. `tools.agentToAgent.enabled = true`
3. `tools.sessions.visibility = "all"`
4. `tools.agentToAgent.allow` **同时包含发送方和接收方**（双向）

**配置缺失时技能会先询问你**：「要不要帮你补配置？」——你同意后自动执行 `config.patch`（只动必要字段，安全合并），改完即可编排。你不想让技能改，也可以手动配（详见 `references/agent_to_agent.md`）。

手动检测命令（零依赖，可选）：

```bash
python scripts/check_config.py
```

输出 `[OK]` 即就绪；`[FAIL]`/`[WARN]` 会给出修复指引。

### Step 2：对 agent 说一句话

**点名分工**（直接执行）：
> 「让小光把产品矩阵画出来，小智调研竞品，最后汇总成报告给我」

**模糊大任务**（技能先问一句）：
> 「调研一下这个软件」

技能会问：要不要并行编排？展示可用 agent 与拆法 → 你点头才执行。

### Step 3：看进度、拿结果

```
📋 编排计划：小光→绘图 / 小智→调研 / 天桐→技术
⏳ 投递中 → 小光执行中（60%）→ 小智完成 → 天桐完成
✅ 3/3 完成 → 聚合报告（带来源）→ 交付
```

## 🚀 快速上手（三步，5 分钟）

### Step 1：安装 + 检测配置

```bash
clawhub install xiaoyaoclaw-agent-orchestrator
python scripts/check_config.py    # 确认 [OK]
```

### Step 2：确认可用 agent

技能直接读 `agents.list` 展示可用 agent（如：小光 / 小智 / 天桐），分工时按名字指定即可。

### Step 3：一句话编排

> 「让小光画一个架构图，画完发我」

技能自动：检测配置 → 投递（sessions_send）→ 追踪（sessions_list/history）→ 收到 [DONE] → 汇总交付。

### 日常使用习惯

| 场景 | 动作 |
|---|---|
| 点名分工 | 「让小光画图，小智调研，最后汇总成报告」 |
| 模糊大任务 | 「调研一下 XX」→ 技能先问要不要并行编排 |
| 并行批量巡检 | 「让所有 agent 检查各自工作区」 |
| 发布前多视角审查 | 「让 小X 从用户视角审查这个页面」 |
| 团队日报汇总 | 「汇总各 agent 今天的工作」 |
| 失败重试 | 自动 ≤3 次带上下文重试，无需干预 |

## 常见问题

| 问题 | 答案 |
|---|---|
| 提示 allow 白名单 denied？ | allow 必须**双向**（发送方 + 接收方都在内），见 references/agent_to_agent.md |
| sessions_send 超时了，失败了吗？ | **不是**。60s 只是等待超时，任务后台继续，用 sessions_list/history 查真实状态 |
| 对方一直来回回复？ | 指令模板内置「一次回复即完成」，另有 maxPingPongTurns 上限双保险 |
| 没有多 agent 配置能用吗？ | 不能编排（无可分发对象），技能保持沉默并提示先配置 |

## 目录结构

```
xiaoyaoclaw-agent-orchestrator/
├── SKILL.md                    # 技能主体（三档触发 + 8 步流程 + 规则）
├── manifest.json               # 兼容 openclaw 等
├── references/
│   ├── sessions_send.md        # sessions_send 机制详解（超时语义/announce/ping-pong）
│   ├── agent_to_agent.md       # agentToAgent 配置指南（visibility/allow 双向/坑）
│   └── config_patch.md         # 配置修改安全规范（config.patch vs apply）
├── scripts/
│   ├── check_config.py         # 【亮点】检测 openclaw.json 协作配置 → 状态报告
│   └── check_status.py         # 【亮点】解析 sessions_list → 子任务状态汇总（零 token）
├── templates/
│   └── task_prompt.md          # 分发指令模板（[DONE] 约定 + 防 ping-pong）
├── assets/readme/              # hero + 群二维码
├── docs/
│   └── DESIGN.md               # 设计文档（含竞品分析）
├── README.md / README.en.md
└── LICENSE
```

## 编排流程（8 步）

```
① 触发判定（三档）→ ② 配置检查（双向白名单）→ ③ 编排规划（子任务+agent 匹配+确认）
→ ④ 并行分发（sessions_send timeoutSeconds=0）→ ⑤ 进度追踪（list/history 判定）
→ ⑥ 结果聚合（带来源）→ ⑦ 失败重试（≤3 次，带上下文）→ ⑧ 交付（汇总+产出位置）
```

## License

MIT — 随便用，署名可选。

---

## 🛠️ 需要定制？

**Agent & Skills 定制，价格 ¥800 起。**

- 微信：`dtsola`（添加好友时备注：**openclaw定制**）
- 服务范围：OpenClaw 多 agent 部署 / 工作区规范化 / 自定义 Skill 开发 / agent 记忆系统搭建 / 多 agent 协作编排

## 💬 加入交流群

小遥全系产品用户交流群——产品反馈 · 使用交流 · 功能建议：

<p align="center">
  <img src="./assets/readme/community-qr.png" width="280" alt="小遥AI 用户交流群二维码：扫码加群，或添加微信 dtsola（备注：加群）">
</p>

<p align="center">扫码加群，或添加微信 <code>dtsola</code>（备注：<b>加群</b>）</p>

## 姊妹项目（十件套）

- 🏠 **xiaoyaoclaw-workspace-initializer**（工作区初始化器）：给每个 agent 一个「家」——标准目录结构 + WORKSPACE.md 规范 + 多 agent 配置安全。<https://github.com/dtsola/xiaoyaoclaw-workspace-initializer>
- 🧠 **xiaoyaoclaw-memory-distill**（记忆蒸馏）：把对话蒸馏成 MEMORY.md + 日常日志，解决上下文溢出。<https://github.com/dtsola/xiaoyaoclaw-memory-distill>
- 🗂️ **xiaoyaoclaw-task-progress-tracker**（任务进度跟踪器）：目录即容器，PROGRESS.md 即进度——tasks/ 与 projects/ 生命周期管理。<https://github.com/dtsola/xiaoyaoclaw-task-progress-tracker>
- 📚 **xiaoyaoclaw-kb-retriever**（知识库检索器）：分层索引导航 + 渐进式检索，零依赖零 API key。<https://github.com/dtsola/xiaoyaoclaw-kb-retriever>
- 🩹 **xiaoyaoclaw-workspace-auditor**（工作区体检）：只读审计 5 类检查 + 分级报告 + 修复建议，零依赖脚本永不改文件。<https://github.com/dtsola/xiaoyaoclaw-workspace-auditor>
- 📎 **xiaoyaoclaw-web-clipper**（网页剪藏）：任意网页 → 带 frontmatter 的本地 Markdown，双引擎提取 + 批量剪藏 + 知识库闭环。<https://github.com/dtsola/xiaoyaoclaw-web-clipper>
- 🤝 **xiaoyaoclaw-agent-orchestrator**（Agent 协作编排，**协作层**）：架在生态之上——拆任务、分 agent、管进度、聚结果、失败重试。<https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator>
- 📊 **xiaoyaoclaw-usage-report**（用量报告）：解析 session JSONL，回答「每次 agent 任务花了多久、用了哪些工具/技能/模型、消耗了多少 token」——零依赖纯本地，token 为主指标。<https://github.com/dtsola/xiaoyaoclaw-usage-report>
- 🎛️ **xiaoyaoclaw-commander**（跨工具指挥官，**指挥层**）：让任意支持 Agent Skills 的工具（Claude Code / Codex / OpenCode / Trae / DSH）指挥小遥Claw / OpenClaw 多 agent 系统。<https://github.com/dtsola/xiaoyaoclaw-commander>
- 🔍 **xiaoyaoclaw-seo-skill**（SEO 技能）：网站搜索可见性分析与优化——audit（技术SEO）/page（页面）/content（内容质量）/schema（结构化数据）/geo（AI搜索优化）五流程 + 零依赖审计脚本，跨工具通用。<https://github.com/dtsola/xiaoyaoclaw-seo-skill>
