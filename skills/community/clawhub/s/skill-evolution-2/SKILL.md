---
name: skill-evolution
display_name: 技能进化（知行环）
description: 技能进化（知行环，英文 id `skill-evolution`）——Agent 经验沉淀与自改进闭环框架，把 WikiSkill（arXiv:2608.27454）的经验存储机制与 RSI 路线图（arXiv:2609.11873）的能力判据合成为一条可运行闭环：HCI 选域 → 三层记忆沉淀 → 原子化提议 → 四大追问门控 → 可回滚迭代 → 自主权升阶。支持 WorkBuddy / CodeBuddy / Claude Code / Codex 四平台与 Windows / Linux / macOS。当用户报出「技能进化」或别号「知行环」，或要求经验复盘、记录轨迹、能力评估、自改进闭环设计、自主性分级，或引用 RSI / HCI / WikiSkill 相关概念时触发。
version: 2.0.0
agent_created: true
---

# 技能进化（知行环）· Skill Evolution — 两篇论文合成的一条闭环

不改模型权重，让 Agent 自己维护一本经验 Wiki，把成败提炼为可复用技能，用判据门控安全迭代。

> **本 skill 不是"三个模块的集合"，而是两篇论文的合成体。**
> WikiSkill 提供机制（经验**怎么存、怎么迭代**），RSI 路线图提供判据（改进**算不算数、能自动到哪**）。

---

## 为什么必须结合：两篇论文各缺一半

| | WikiSkill（arXiv:2608.27454） | RSI 路线图（arXiv:2609.11873） |
|---|---|---|
| 回答 | 经验**怎么存、怎么迭代** | 改进**算不算真的、能自动到哪** |
| 核心 | 三层记忆 Raw→Wiki→Skill；角色隔离；门控弧 `R_val > R_best` 否则回滚 | HCI 能力余量闭合指数；L1–L5 自主权分级；四大评估追问 |
| 缺口 | 门控**只有一条阈值**，缺"什么样的改进才算数"的判据 | 判据齐备，却**没有可持续存储与回滚的载体** |

**结合方式**：RSI 的四大追问**成为** WikiSkill 门控的评分卡；WikiSkill 的三层**成为** RSI 改进闭环的沉淀载体。
两边都不是外挂装饰，而是各自补上对方的缺口——这才是"结合"，不是"并排放三个模块"。

---

## 统一闭环（七步）

```
① 选域 ──── RSI / HCI：挑缺口最大的能力域
   │
② 执行记录 ── Raw 层：只记轨迹，不读 wiki（角色隔离红线）
   │
③ 提炼 ──── Wiki 层：同类失败 ≥2 次即立为模式
   │
④ 原子化提议 ─ Skill 层：一轮只改一个技能
   │
⑤ 门控 ──── ★ 融合点：四大追问评分卡 + WikiSkill 阈值
   │
⑥ 采纳 / 回滚 ─ 技能可回滚；Wiki 永不回滚（失败原因写回 patterns）
   │
⑦ 自主权升阶 ─ RSI / L1–L5：判定下轮能把哪些环节交给 AI
   └──────────────────────────→ 回到 ①
```

| 步骤 | 理论来源 | 主要产出 |
|:----:|---------|---------|
| ① 选域 | RSI（HCI） | 本轮投向哪个能力域、优先级排序 |
| ②③④ | WikiSkill（三层记忆） | `raw/` 轨迹 → `knowledge/patterns.md` → `skills/` |
| ⑤ 门控 | **两篇交集** | 采纳 / 观察 / 回滚 + 四问证据 |
| ⑥ 回滚 | WikiSkill | 技能版本回退（知识层只增不减） |
| ⑦ 升阶 | RSI（L1–L5） | 下一轮的自动化边界 |

---

## ⚠️ 角色隔离约束（最重要，不可放松）

WikiSkill 论文用消融实验证明：**执行任务的 Agent 一旦能访问 wiki，技能开发质量反而下降**（混淆变量）。
因此本框架强制角色隔离：

| 角色 | 何时 | 能读 wiki 吗 | 做什么 | 对应闭环步骤 |
|------|------|:-----------:|--------|:-----------:|
| **Inference Agent** | 日常任务执行中 | ❌ **不能** | 只干活 + 记录轨迹 | ② |
| **Wiki Maintainer** | 离线周期复盘 | ✅ 能 | 提炼 patterns | ③ |
| **Skill Proposer** | 离线周期进化 | ✅ 能 | 提技能改进、走门控 | ④⑤⑥ |

**这条约束不因"两篇论文合一"而放松**：即使全部步骤现在同属一个 skill，执行任务的 Agent 也**不得**
顺手读 `.wiki/knowledge/` 或 `.wiki/skills/` 来"指导当前任务"。这是设计红线，不是建议。

---

## Step ① 选域：用 HCI 决定往哪投（RSI）

**HCI（Headroom-Closed Index，能力余量闭合指数）**——衡量相较某项评测最初的前沿水平，模型填补了多少通往满分的差距：

```
HCI = 100 × (共识得分 − 基准前沿) ÷ (100 − 基准前沿)
```

- **基准前沿** = 该基准进入数据集**第一年**的第 90 百分位模型分
- **共识得分** = 按数据源加权，以抑制自报结果偏差
- 尺度：0 = 与基准年持平，100 = 追平满分

### 2026 年各领域 HCI（据 RSI 论文）

| 领域 | HCI | 读法 |
|------|----:|------|
| 网络安全 Agent | 91.9 | 已近饱和 |
| 前沿数学 | 86.4 | 标准化考试类，红利见顶 |
| 研究生级科学 | 85.8 | 同上 |
| 广博知识 | 77.2 | 偏记忆类 |
| 法律推理 | 64.5 | 中等缺口 |
| 多模态推理 | 62.2 | 中等缺口 |
| 前沿学术广度 | 60.4 | 中等缺口 |
| 搜索与终端 Agent | 56.8 | 缺口较大 |
| **软件工程** | **52.6** | **缺口大 = 红利高** |
| **工具调用 Agent** | **39.9** | **缺口最大** |

**结论**：模型在"标准化考试"上快摸到顶（数学/科学 >85），却在"真实任务执行"上刚起步
（软件工程 52.6、工具调用 Agent 仅 39.9）。同为 Agent，**网络安全 Agent 已达 91.9**，
与工具调用 Agent 相差 **52.0 点**——Agent 内部能力分化极大，不能一概而论。

**选域规则**：HCI 越低越优先。软件工程与工具型 Agent 是各家发力第一站，
因为**反馈廉价、验证明确、部署链路短**，RSI 循环最容易闭合。

---

## Step ②③④ 记录 → 提炼 → 提议（WikiSkill 三层）

### 目录结构与三层映射

```
.wiki/                          # 项目级 Wiki 根目录
├── raw/                        # Raw Layer  — 不可变的执行轨迹（② 的产出）
│   └── YYYY-MM-DD.md           # 按日期追加
├── knowledge/                  # Wiki Layer — 持久化知识（③ 的产出，只增不减）
│   ├── patterns.md             # 失败模式 + 成功策略
│   ├── evolution_log.md        # 技能演化日志
│   └── impact_tracker.md       # 提案验证结果追踪
├── skills/                     # Skill Layer — 可回滚的执行指令（④ 的产出）
│   └── <skill-name>.md
└── meta/
    └── config.md               # 当前任务域、迭代周期等
```

### RSI 四步闭环 ↔ WikiSkill 三层（同一件事的两种说法）

RSI 的「环境—数据—模型」四步，落到工程上就是 WikiSkill 的三层记忆。本框架直接复用：

| RSI 四步闭环 | 对应的 `.wiki/` 层 | 具体动作 |
|-------------|------------------|---------|
| 1. 重构环境 | （环境本身） | 把工作区标准化：可重跑测试、结构化日志、固定依赖 |
| 2. 暴露缺口 | `raw/` | 反复执行任务，记录失败轨迹与异常 |
| 3. 再训练/沉淀 | `knowledge/` → `skills/` | 提炼 patterns → 原子化提案 → 走门控 |
| 4. 迭代环境 | （下一轮 ①） | 用更强模型 / 更准验证器提升环境本身 |

> 注：RSI 原文的"再训练"指训练模型权重；本框架**不改权重**，改为"沉淀为可回滚技能"——
> 这是把 RSI 闭环移植到"无训练权限"场景的工程等价物。

### ② 执行并记录（Inference Agent）

执行任务时，在 `.wiki/raw/YYYY-MM-DD.md` 末尾追加轨迹：

```markdown
### [HH:MM] 任务简述
- **域**：[coding/data/research/debug/...]
- **结果**：✅ 成功 / ❌ 失败 / ⚠️ 部分成功
- **轨迹**：
  1. [关键步骤 1] → [结果]
  2. [关键步骤 2] → [结果]
- **关键观察**：[遇到了什么意外、用了什么技巧]
```

**原则**：只记关键决策点和异常，不记流水账。每条轨迹控制在 10 行以内。

### ③ 知识提炼（Wiki Maintainer）

每完成 3-5 个任务后，或用户说"复盘 / wiki maintain"时：

1. 读取 `.wiki/raw/` 最近的轨迹
2. 识别重复出现的模式（**同一类错误出现 ≥2 次即为模式**）
3. 更新 `.wiki/knowledge/patterns.md`：

```markdown
## 失败模式

### FM-[编号]: [简短名称]
- **触发条件**：[什么情况下出现]
- **表现**：[具体症状]
- **根因**：[为什么]
- **解决方案**：[如何避免/修复]
- **发现日期**：YYYY-MM-DD | **出现次数**：N

## 成功策略

### SS-[编号]: [简短名称]
- **适用场景**：[什么情况下有效]
- **具体做法**：[步骤]
- **验证案例**：[日期]
```

4. 在 `evolution_log.md` 追加一条维护记录

### ④ 原子化提议（Skill Proposer）

1. 读取 `patterns.md` + `impact_tracker.md`
2. 提出**一个原子化改进**，写入 `.wiki/skills/` 或修改现有技能文件：

```markdown
---
name: [技能名]
version: 1.x
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
source_patterns: [FM-001, SS-002]
---
# [技能名]
## 适用场景
## 执行步骤
## 注意事项
## 变更历史
```

> `source_patterns` 字段等价于 WikiSkill 论文中 `PURPOSE.md` 的作用——把技能映射回启发它的 Wiki 模式。
> **没有 `source_patterns` 的技能不允许入库**：无法追溯来源的改进无法归因。

**原子化原则**：每轮只改一个技能，改动最小化，失败时能精确定位是哪个改动的问题。

---

## Step ⑤ 门控（★ 两篇论文的融合点）

WikiSkill 原本只有一条阈值：`R_val > R_best` 才保留，否则回滚到 `S_{k-1}`。
RSI 的四大追问补上了"这个改进到底算不算数"的判据。**两者合成一张评分卡**：

| # | 追问（RSI） | 判定什么 | 需要的证据 | 不通过的后果 |
|:-:|------------|---------|-----------|-------------|
| 1 | **可衡量** | 改进是否真实？ | ≥2 个同域任务，用**与提案前相同的判据**独立复测 | 退回"观察"，不得采纳。**自评分不算证据** |
| 2 | **可保持** | 是否持久不退化？ | 间隔一个复盘周期后复测仍成立 | 降级为"未验证"，重新计时 |
| 3 | **可迁移** | 换任务 / 项目 / 平台还灵吗？ | ≥1 个不同任务域，或另一平台复用成功 | 标记为**项目局部技能**，不进跨项目库 |
| 4 | **可回滚** | 失效时能否安全撤回？ | 技能文件有「变更历史」，可恢复到上一版 | **一票否决**——不可回滚就不许采纳 |

### 判定规则（RSI 四问 + WikiSkill 阈值）

| 结果 | 条件 |
|------|------|
| ✅ **采纳** | 四问全通过 **且** `R_val > R_best` |
| ⚠️ **观察** | 四问中任一为"未验证"，或 `R_val == R_best` |
| ❌ **回滚** | 四问中任一**明确失败**，或第 4 问不通过（一票否决） |

> **第 4 问是一票否决**：不可回滚的改进不允许上线，无论它多有效。
> 这条规则同时兑现了 RSI 的"可回滚"追问与 WikiSkill 门控弧的安全语义。

在 `impact_tracker.md` 记录提案与四问结果：

```markdown
### PROP-[编号] | [日期]
- **目标**：[改了什么]
- **依据**：[引用 patterns]
- **验证任务**：[用哪些任务测试]
- **四问证据**：可衡量[…] / 可保持[…] / 可迁移[…] / 可回滚[…]
- **结果**：待验证 / ✅ 采纳 / ⚠️ 观察 / ❌ 回滚
- **效果**：[量化或定性对比]
```

---

## Step ⑥ 采纳 / 回滚（双轨原则）

| 轨道 | 回滚吗 | 说明 |
|------|:------:|------|
| **技能轨**（`skills/`） | ✅ 可以回滚 | 从技能文件的「变更历史」恢复到上一版本 |
| **知识轨**（`knowledge/`） | ❌ **永不回滚** | 失败原因写入 `patterns.md`，成为下一轮提案的输入 |

这不是两条独立规则的堆叠，而是 WikiSkill 的核心设计：**失败也是知识**。
技能被撤回，但"为什么会失败"必须留下——否则同一坑会反复踩。

---

## Step ⑦ 自主权升阶：L1–L5（RSI）

每轮闭环结束时，判定这一轮能不能把更多环节交给 AI。

| 级别 | 名称 | 人类负责 | AI 闭环接管 |
|---|---|---|---|
| L1 | 执行自主 | 设计任务、环境、更新策略 | 执行任务、更新 |
| L2 | 策略自主 | 设计任务、环境 | 设计更新策略（策略持久化） |
| L3 | 经验获取自主 | 设计环境 | 规划经验获取、执行、设计更新策略（经验设计持久化） |
| L4 | 环境适应自主 | 设定边界 | 与环境交互、设计更新策略（环境适应持久化） |
| L5 | 递归继承自主 | 设定边界 | 改进"改进系统本身"（系统设计持久化） |

**关键区分**：L1–L4 在既定改进机制下提升任务能力；**只有 L5 由 AI 接管"决定后续改进的机制"本身**，
才可能触及真正的递归。L5 的持续递归收益目前仍缺乏充分验证。

**安全边界**：总体目标与安全边界始终由人类把关；真正的提升必须在**同等预算下经独立评估**确认，
不能仅靠自我修改或自评分宣称进步。

### 本框架的自主权落点

| 闭环步骤 | 可自动到 | 依据 |
|---------|:-------:|------|
| ①②③④ 选域 / 记录 / 提炼 / 提议 | L2–L3 ✅ | 只写 `.wiki/`，全程可回滚 |
| ⑤ 门控 | ❌ **永远人工** | L4——判断"真的变强"必须人看实际效果 |
| ⑥ 回滚 | ✅ 可自动执行 | 但**触发判定**仍要人 |
| ⑦ 升阶 | ❌ 人工 | L5 不做承诺 |

> **结论：本框架稳定在 L2–L3**。宣称 L5 级递归收益是没有依据的。

---

## 快速命令（触发词）

| 触发词 | 对应闭环步骤 | 动作 | 主导角色 |
|--------|:-----------:|------|---------|
| "技能进化" / "知行环" | 全链 | 报出技能名即唤醒：载入本 skill，确认当前处于哪一步 | 任一 |
| "记录轨迹" / "wiki log" | ② | 追加当前任务轨迹到 `raw/` | Inference Agent |
| "复盘" / "wiki maintain" | ③ | 提炼 `patterns.md` | Wiki Maintainer |
| "进化技能" / "wiki evolve" | ④⑤⑥ | 提出技能改进并走四问门控 | Skill Proposer |
| "wiki 状态" / "wiki status" | — | 展示统计（轨迹数、模式数、技能数） | 任一 |
| "初始化 wiki" / "wiki init" | — | 创建 `.wiki/` 结构（`scripts/wiki_init.py`，全平台通用） | 任一 |
| "选域" / "该往哪投" | ① | 按 HCI 排优先级，给出投入建议 | 任一 |
| "自改进设计" / "闭环设计" | 全链 | 走五步设计工作流，产出原子化方案 | 任一 |
| "RSI 体检" / "能力评估" | ①⑦ | 按 L1–L5 与四大追问做诊断 | 任一 |

---

## 跨平台使用

本 skill 的核心是 `.wiki/` 目录结构与 Markdown 格式，与平台无关。

| 平台 | 自动调用机制 | Windows | Linux | macOS |
|------|-------------|:------:|:-----:|:-----:|
| WorkBuddy | 定时 automation（平台原生、持久保存）；触发词自动识别 | ✅ | ✅ | ✅ |
| CodeBuddy | **IDE / 插件无定时任务**；CodeBuddy Code（CLI）的定时为**会话级**（退出即清除、3 天过期、中断不补跑），持久周期需 **headless + 外部调度器** | ✅ | ✅ | ✅ |
| Claude Code | `CLAUDE.md` 常驻指令（用 `references/CLAUDE.template.md`）+ Stop hook 提醒 | ✅ | ✅ | ✅ |
| Codex | `AGENTS.md` 常驻指令（用 `references/AGENTS.template.md`）+ git `post-commit` 提醒 | ✅* | ✅ | ✅ |

\* Codex 在 Windows 上依赖 Git for Windows 自带的 bash 运行 git hook。

所有平台共享同一个 `.wiki/` 目录，经验可跨平台迁移——
这正好兑现了 RSI 四问里的「**可迁移**」。详见 `references/platforms.md`。

---

## 从旧版迁移

**触发信号**（出现任一条即需迁移）：

- 用户提到自己装过 `wikiskill` / `rsi-knowledge` / `rsi-self-improvement-designer`；
- `~/.workbuddy/skills/` 下仍存在上述任一目录；
- `~/.claude/settings.json` 的 `hooks.Stop` 命令指向 `scripts/wikiskill/` 或包含旧 skill 名；
- 项目内 `CLAUDE.md` / `AGENTS.md` 引用了 `~/.workbuddy/skills/wikiskill/...` 之类的旧路径。

**四步动作**：

| 步骤 | 做什么 |
|------|--------|
| 1. 归档 | 把三个旧 skill 目录整体移入 `~/.workbuddy/skills_archived/<日期>_merged_into_skill-evolution/`（已存在则跳过，不删除） |
| 2. 换 hook | `python <skill目录>/scripts/install.py --platform claude --user`（自动替换旧命令，保留其余配置） |
| 3. 改引用 | 项目内 `CLAUDE.md` / `AGENTS.md` 里的旧 skill 路径 → 项目内 `.wiki/references/`；定时任务 prompt 里的旧 skill 名 → `skill-evolution` |
| 4. 自检 | 见下表 |

**项目内已有 `.wiki/` 时：数据不用迁移。** `.wiki/` 是项目级的，且目录名与文件格式
从旧版到新版从未改变，新 skill 直接读写同一份、无缝续用。只需刷新项目内那份运行时快照：

```bash
python <skill目录>/scripts/install.py --platform claude --target <项目目录> --no-hook
```

`raw/`、`knowledge/`、`skills/` 完全不碰；`scripts/` 与 `references/` 刷新为新版；
已有的 `CLAUDE.md` / `AGENTS.md` 跳过不覆盖。加 `--no-hook` 是为了保留项目里已有的
hook 配置（例如其他插件注入的 `SessionStart`），只刷运行时、不动配置。

**硬红线**：不删除、不重命名 `.wiki/` 目录，不改动 `.wiki/scripts/` 与 `.wiki/knowledge/`
下的文件名——目录名 `.wiki/`、脚本名 `wiki_init.py` / `wiki_remind.py` 是**跨项目的运行时契约**，
改名会让所有已初始化的项目失效。

迁移后自检：`~/.workbuddy/skills/` 只剩 `skill-evolution`；hook 指向 `scripts/skill-evolution/wiki_remind.py`；
旧项目 `.wiki/` 内容一字未变；说「记录轨迹」「复盘」能正常触发。

> 完整操作手册（含可直接粘贴给 AI 的迁移指令、分平台步骤、回滚方式）见 `README.md` 的「从旧版迁移」。

---

## 自动化运行

自动化的可行度分四层——**这个分层本身就是 RSI 的 L1–L5 落到本框架的结果**，不要试图全自动：

| 层次 | 能否自动 | 对应自主权级别 | 方案 |
|------|:-------:|:-------------:|------|
| L1 指令常驻 | ✅ 能 | L1 | CLAUDE.md / AGENTS.md 全量加载 |
| L2 自动记录轨迹 | ✅ 能 | L2 | Claude Code Stop hook / git hook |
| L3 周期复盘进化 | ✅ 能 | L3 | WorkBuddy 定时 automation（CodeBuddy 需 headless + 外部调度器） |
| L4 门控验证 | ❌ **不能** | L4 | 需人判断，设计如此 |

**核心原则**：WikiSkill 论文里 Wiki 维护是离线批量做的，Inference Agent 执行时不读 Wiki。
对应到实践——**在线**（每次任务）只做 ② 记录，**离线**（周期性）做 ③④⑤⑥。
别在每次任务里跑完整七步闭环。

**三种自动化方案**：

1. **WorkBuddy 定时复盘**（推荐）：创建定时任务周期性跑 ③④⑤⑥，或跑全链联合编排。
   prompt 模板见 `references/automation.md`。**CodeBuddy 不能直接套用**：其定时任务仅存在于
   CodeBuddy Code（CLI），且为会话级；若要在 CodeBuddy 上做持久周期，改用 headless 模式
   `codebuddy -p -y "<prompt>"` + 外部调度器（Windows 计划任务 / cron / GitHub Actions）。
2. **Claude Code Hook**：会话结束时自动提醒记录轨迹。安装：
   ```bash
   # 项目级（推荐）：hook 用相对路径，项目自包含，可提交 Git
   python <skill目录>/scripts/install.py --platform claude --target <项目目录>

   # 用户级：运行时装到 ~/.claude/scripts/skill-evolution/，对所有项目生效
   python <skill目录>/scripts/install.py --platform claude --user
   ```
   安装器会**合并**而非覆盖已有配置（保留 permissions、其他 hooks）；若已存在**命令相同**的
   hook 则跳过，若存在**指向旧目录**（如 `scripts/wikiskill/`）的 hook 则**自动替换**为当前命令。
   `--uninstall` 只摘除本框架的 hook 条目，**同组内其他人的 hook 原样保留**（不删 `.wiki/` 数据）。
   它还会探测 `python` / `python3` / `py -3`，避免机器上没装 `python` 命令时静默失效。
3. **Git Hook**（跨平台通用）：`post-commit` 里加提醒，任何工具链都能用。

**注意**：⑤ 门控验证不建议自动化。判断"技能改进是否真的有用"需要人看实际效果；
强行自动化会导致无效技能污染技能库——这正是四问里「可衡量」的红线。

### 联合自动化

`references/automation.md` 提供三种粒度的自包含 prompt：**全链联合编排**（①–⑦）、**仅 RSI 体检**（①⑦）、
**仅自改进设计**。整条链只有 ②③④⑥ 写文件（全部落在 `.wiki/` 内，可回滚），
因此可被定时任务安全驱动；**唯一的人工介入点是 ⑤ 门控**。

---

## 关键原则

1. **角色隔离**：执行任务的 Agent 不读 Wiki（论文消融实证，见上文红线）
2. **技能可回滚，Wiki 永不回滚**：失败原因必须留在知识层，成为下一轮输入
3. **原子化改进**：每轮只改一个技能，便于归因
4. **四问全过才采纳**：尤以「可回滚」为一票否决
5. **轻量记录**：轨迹不记流水账，只记决策点和异常
6. **只靠自评分宣称进步无效**：必须在独立评估下确认（RSI「可衡量」）
7. **不承诺 L5**：本框架的现实目标是 L2–L3

---

## 能力边界：什么时候不该用它

**它擅长**：把「项目内、你亲自踩过、有明确反馈」的经验沉淀成可复用技能。
反馈越廉价（编译 / 测试 / 报错）、验证越明确，闭环闭合得越快。

**它不擅长，别硬上**：

| 场景 | 为什么不行 | 替代做法 |
|------|-----------|---------|
| 跨项目、跨团队的通用知识库 | `.wiki/` 是**项目级**的，设计上刻意不过度泛化 | 手动复制通用性强的 `skills/*.md` 到别的项目 |
| 语义检索 / 海量经验召回 | 就是一堆 Markdown 文件，**没有向量检索与排序** | 用向量库或知识库产品 |
| 完全无人值守的自改进 | ⑤ 门控**必须人工**：没有 held-out 验证集，自动化只会让无效技能污染技能库 | 接受"半自动"——自动化跑 ②③④，你来拍板 ⑤⑥ |
| 追求 L5 级递归自我改进 | 论文亦未充分验证，本框架**明确不承诺** | 现实目标 L2–L3 |
| 一次性的、不会重复的坑 | 没有第二次，沉淀没有收益 | 写进 commit message 或代码注释即可 |
| 需要长期留存的敏感数据经验 | `.wiki/` 是**纯文本且建议提交 Git** | 脱敏后再记，或改用私有存储 |

**用高级功能（④ 提议 → ⑤ 门控）前，先弄懂这三件事**：

- 为什么「可回滚」是**一票否决** → `references/workflow.md` 的门控章节
- 为什么**自评分不算证据** → 同上「四问评分卡」
- 为什么执行任务的 Agent **不许读 Wiki** → 本文件开头的角色隔离红线

没弄懂就去用高级功能，最常见的后果是**技能库被无效技能污染**，
且因缺乏变更历史而**无法回退**——这比不用更糟。

**常见用错方式已单独汇总**：`references/anti-patterns.md`（含报错速查表）。

---

## 参考资源

| 文档 | 内容 |
|------|------|
| `references/workflow.md` | 三角色详细职责 + 四问门控评分卡完整版 |
| `references/rsi-framework.md` | RSI：HCI 度量 / L1–L5 / 产业实践数据 |
| `references/design-playbook.md` | 自改进设计五步工作流与方案模板 |
| `references/anti-patterns.md` | **反模式清单（"别这样做"）+ 报错速查表** |
| `references/automation.md` | 自动化方案 + 三种粒度的 prompt 模板 |
| `references/platforms.md` | 跨平台适配指南（跨 OS 路径陷阱的唯一权威源） |
| `references/templates.md` | Markdown 模板集合 |
| `README.md` | **给人读**的操作手册（哪些自动 / 哪些手动 / 什么时候做 / 具体怎么做） |

### 脚本

| 脚本 | 用途 | 适用 shell |
|------|------|-----------|
| `scripts/install.py` | **统一安装器**（项目自包含，推荐入口） | 全平台 |
| `scripts/wiki_init.py` | 初始化 `.wiki/` | Windows CMD / PowerShell、Linux、macOS |
| `scripts/wiki_init.sh` | 初始化 `.wiki/` | Linux / macOS / **Git Bash** / WSL |
| `scripts/wiki_init.ps1` | 初始化 `.wiki/` | Windows PowerShell 原生 |
| `scripts/wiki_remind.py` | Stop hook 提醒脚本 | 全平台（Windows 必用） |
| `scripts/wiki_remind.sh` | Stop hook 提醒脚本 | Unix |
| `scripts/selfcheck.py` | 包体自检（只读；改动后 / 分发前跑） | 全平台 |

**Windows 路径陷阱（必读）**：CMD/PowerShell 原生环境没有 bash，`.sh` 跑不了；
反过来，**在 Git Bash 里不能用 `python "$HOME/..."`**——Git Bash 的 `$HOME` 是
POSIX 格式（`/c/Users/xxx`），Windows 原生 Python 会解析成 `C:\c\Users\xxx`。

按 shell 选命令（下文的 `SKILL_DIR` = 本 skill 所在目录，换成实际路径即可）：

```powershell
# Windows PowerShell
python "$SKILL_DIR\scripts\wiki_init.py"
```
```cmd
:: Windows CMD
python "%SKILL_DIR%\scripts\wiki_init.py"
```
```bash
# Linux / macOS / Git Bash / WSL
bash "<skill目录>/scripts/wiki_init.sh"
```

**更省事的写法**——若项目已用 `install.py` 安装过，直接跑项目内脚本，
这条命令在所有 shell 下都成立（不含任何 `$HOME` 变量）：

```bash
python .wiki/scripts/wiki_init.py
```

Claude Code 在 Windows 上执行 hook 走 cmd.exe/PowerShell（**不走 Git Bash**），
因此提醒脚本必须用 `.py` 版本——安装器会自动处理。

> **不要用 `~/.workbuddy/skills/<skill名>/` 作为路径**。那是 WorkBuddy 的私有目录，
> Claude Code / Codex 用户机器上不存在。坚持用项目内路径或 `install.py`。
