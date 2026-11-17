# OpenClaw Memory Distill 🧠

<div align="center">
  <strong>🇨🇳 中文</strong> | <a href="README.en.md">🌐 English</a>
  <br><sub>两种文档内容一致，任选；回答语言跟随用户 —— Language is optional, docs are equivalent.</sub>
</div>

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="OpenClaw Memory Distill — distill conversations into structured memory: semantic classification into core (MEMORY.md), daily (memory/YYYY-MM-DD.md), with dedup and sensitive-info skip">
</p>

> 把对话蒸馏成结构化记忆，解决会话上下文溢出。
> OpenClaw memory distillation & organization — distill conversations into MEMORY.md + daily logs, so your agent never forgets.

![license](https://img.shields.io/badge/license-MIT-green)
[![ClawHub downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fxiaoyaoclaw-memory-distill&query=skill.stats.downloads&label=ClawHub%20downloads&color=blue)](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-memory-distill)

## 为什么需要它

OpenClaw agent 每次会话都是全新启动。没有记忆整理，你的 agent 会：
- ❌ **上下文溢出**：对话一长，重要信息被挤掉，只能 /reset 失忆重来
- ❌ **记忆碎片化**：决策、项目状态散落在各天日志里，永远找不到
- ❌ **MEMORY.md 缺失**：没有长期记忆文件，每次醒来都像第一次见面
- ❌ **重复膨胀**：反复写入同样内容，记忆文件越堆越臃肿

这个 skill 一次性解决：**蒸馏分级 + 首次建忆 + 增量去重 + 敏感信息防护**。

## 特性

- 🧪 **语义分级**：核心级 → 根目录 MEMORY.md；日常级 → memory/YYYY-MM-DD.md；临时级 → 只留当日（靠语义理解，不靠关键词匹配）
- 🏗️ **首次建忆**：MEMORY.md 缺失时，扫描历史日志自动提炼生成初版——不用从空骨架开始
- 🔁 **增量去重**：写入前查重，只追加新条目、合并重复项，防记忆膨胀
- 🔒 **敏感信息跳过**：token/密码/密钥自动检测，默认不落盘
- 🗄️ **只归档不删除**：过期日志移动到 archive/，删除必须人工确认
- 🕐 **三种触发**：手动一句话 / Cron 每日定时 / HEARTBEAT 动态触发
- 🧍 **多 agent 隔离**：每个 agent 只整理自己的工作区记忆，互不干扰
- 🏠 **与 initializer 互补**：它管记忆系统的「家」，本技能管记忆系统的「内容」

## 安装

```bash
# ClawHub（推荐）
clawhub install xiaoyaoclaw-memory-distill

# 或从 GitHub 手动安装
git clone https://github.com/dtsola/xiaoyaoclaw-memory-distill
# 把 SKILL.md 和 templates/ 放到你的 skills 目录
```

## 使用

> ⚠️ **它会写工作区文件**（默认只在**你确认后**写）：蒸馏会把对话内容整理进根 `MEMORY.md` 与
> `memory/YYYY-MM-DD.md`（覆盖前先归档到 `memory/archive/`），首次配置还会创建 `distill-config.json`。
> 定时（cron）模式**默认只报告**，不自动落盘；要自动落盘须显式把 `autoWrite` 改成 `true`。
> 🌐 **语言可选**：中英文档任选，回答语言跟随你（中文文档按中文回复，英文提问按英文回复）。

1. 把 skill 放到 OpenClaw 的 skills 目录
2. **明确说**「**蒸馏记忆**」「整理记忆」「把这轮对话蒸馏一下」，agent 才会：
   - 检测 memory/ 与 MEMORY.md（缺失则从历史日志**首次建忆**）
   - 扫描会话 → 语义分级 → 出蒸馏报告（含敏感信息提示）
   - 增量去重写入 → 汇报结果
3. 可选：说「配置每天 22:00 自动执行记忆蒸馏」开启定时蒸馏

**什么时候不会触发**：随口说的「整理一下」「总结下今天」、问记忆机制怎么工作、或只是讨论要不要整理 —— 都不会被当成调用指令；先问一句「要执行蒸馏并写入 MEMORY.md 吗？」再说。


## 🚀 快速上手（三步，5 分钟）

### Step 1：安装技能

```bash
clawhub install xiaoyaoclaw-memory-distill
```

### Step 2：一句话触发首次蒸馏

对你的 agent 说：

> 蒸馏记忆

agent 自动完成：检测记忆状态 → （MEMORY.md 缺失则扫描历史日志首次建忆）→ 扫描本次会话 → 语义分级 → 出报告 → 确认写入 → 汇报结果。

### Step 3：验收 + 开启自动蒸馏

打开工作区目录验收：

```
工作区根目录/
├── MEMORY.md               ← 长期记忆（核心级）已就位
├── distill-config.json     ← 蒸馏配置
└── memory/
    └── YYYY-MM-DD.md       ← 今日蒸馏日志
```

想要每天自动蒸馏，对 agent 说：

> 配置每天 22:00 自动执行记忆蒸馏

上下文快满时：先「蒸馏记忆」再 `/reset`，记忆不丢。

### 日常使用习惯

| 场景 | 动作 |
|---|---|
| 会话结束 / 上下文快满 | 手动说「蒸馏记忆」，再 /reset |
| 长期使用 | 配置 cron 每日 22:00 自动蒸馏 |
| 每周沉淀 | 说「提炼记忆」→ 近 7 天日志精华合并进 MEMORY.md |
| 敏感对话 | 蒸馏报告自动跳过敏感信息，无需手动处理 |

## 与其他方案的区别

| | systiger/memory-distill | **xiaoyaoclaw-memory-distill** |
|---|---|---|
| 信息分类 | 关键词匹配 | ✅ 语义分级（核心/日常/临时） |
| MEMORY.md 缺失 | 只建空骨架 | ✅ 首次建忆：从历史日志提炼生成 |
| 重复写入 | 无防护，会膨胀 | ✅ 增量查重合并 |
| 敏感信息 | 一句话提示 | ✅ 自动检测默认跳过 |
| 过期清理 | 自动删除（retentionDays） | ✅ 只归档不删除，删除需确认 |
| 自动 /reset | 配置项存在 | ✅ 不提供该配置（重置由用户自行决定） |
| 多 agent 记忆 | 不区分 | ✅ 每个 agent 独立处理自己的 |
| 与工作区规范 | 无关联 | ✅ 路径按 WORKSPACE.md，配置安全继承 initializer 铁律 |

## 目录结构

```
xiaoyaoclaw-memory-distill/
├── SKILL.md                    # 技能主体（工作流 Step 1-7）
├── templates/
│   ├── distill-config.json     # 蒸馏配置模板
│   ├── MEMORY.md               # 长期记忆结构模板（首次建忆底子）
│   └── AGENTS-memory-safety.md # 记忆安全规范（追加到 AGENTS.md）
├── docs/
│   └── DESIGN.md               # 设计方案
├── README.md
└── LICENSE
```

## License

MIT — 随便用，署名可选。

---

## 🛠️ 需要定制？

**Agent & Skills 定制，价格 ¥800 起。**

- 微信：`dtsola`（添加好友时备注：**openclaw定制**）
- 服务范围：OpenClaw 多 agent 部署 / 工作区规范化 / 自定义 Skill 开发 / agent 记忆系统搭建

## 💬 加入交流群

小遥全系产品用户交流群——产品反馈 · 使用交流 · 功能建议：

<p align="center">
  <img src="./assets/readme/community-qr.png" width="280" alt="小遥AI 用户交流群二维码：扫码加群，或添加微信 dtsola（备注：加群）">
</p>

<p align="center">扫码加群，或添加微信 <code>dtsola</code>（备注：<b>加群</b>）</p>

## 姊妹项目

- 🏠 **xiaoyaoclaw-workspace-initializer**（工作区初始化器）：给每个 agent 一个「家」——标准目录结构 + WORKSPACE.md 规范 + 多 agent 配置安全。<https://github.com/dtsola/xiaoyaoclaw-workspace-initializer>
- 📚 **xiaoyaoclaw-kb-retriever**（知识库检索器）：本地知识库检索——分层 data_structure.md 索引导航 + 渐进式检索（md/pdf/xlsx），零依赖零 API key，Windows / macOS 双平台。<https://github.com/dtsola/xiaoyaoclaw-kb-retriever>
- 🩹 **xiaoyaoclaw-workspace-auditor**：工作区体检（只读审计），5 类检查 + 分级报告 + 修复建议，零依赖脚本永不改文件。<https://github.com/dtsola/xiaoyaoclaw-workspace-auditor>
- 🗂️ **xiaoyaoclaw-task-progress-tracker**（任务进度跟踪器）：目录即容器，PROGRESS.md 即进度——tasks/ 与 projects/ 生命周期管理（状态 + 进度日志 + 文档索引）。<https://github.com/dtsola/xiaoyaoclaw-task-progress-tracker>
- 📎 **xiaoyaoclaw-web-clipper**（网页剪藏）：把任意网页保存为带 frontmatter 的本地 Markdown——双引擎正文提取（readability + trafilatura 降级链）、中文文件名安全、批量剪藏 + 去重；输出直通 knowledge/clippings/，配合 kb-retriever 建索引即可检索。<https://github.com/dtsola/xiaoyaoclaw-web-clipper>
- 🤝 **xiaoyaoclaw-agent-orchestrator**（Agent 协作编排，**协作层**）：架在生态之上——拆任务、分 agent、管进度、聚结果、失败重试。<https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator>
- 📊 **xiaoyaoclaw-usage-report**（用量报告）：解析 session JSONL，回答「每次 agent 任务花了多久、用了哪些工具/技能/模型、消耗了多少 token」——零依赖纯本地，token 为主指标。<https://github.com/dtsola/xiaoyaoclaw-usage-report>
- 🎛️ **xiaoyaoclaw-commander**（跨工具指挥官，**指挥层**）：让任意支持 Agent Skills 的工具（Claude Code / Codex / OpenCode / Trae / DSH）指挥小遥Claw / OpenClaw 多 agent 系统。<https://github.com/dtsola/xiaoyaoclaw-commander>
- 🔍 **xiaoyaoclaw-seo-skill**（SEO 技能）：网站搜索可见性分析与优化——audit（技术SEO）/page（页面）/content（内容质量）/schema（结构化数据）/geo（AI搜索优化）五流程 + 零依赖审计脚本，跨工具通用。<https://github.com/dtsola/xiaoyaoclaw-seo-skill>

## 