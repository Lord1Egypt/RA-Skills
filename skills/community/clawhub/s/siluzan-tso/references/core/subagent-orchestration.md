# Subagent 自主委派（宿主客户端）

> 本文件定义：在已激活 **siluzan-tso** Skill 的前提下，**主 Agent 如何根据当前任务自行决定**是否在子会话中执行部分步骤，以及如何 handoff。  
> 不预置固定 `agents/` 目录；不修改 CLI。若宿主**无** Task / subagent 能力，**整节不适用**，按 `playbooks.md` 在主会话执行即可。

协议背景：[Agent Skills — Subagent delegation](https://agentskills.io/client-implementation/adding-skills-support)（可选：子会话执行 + 摘要回传）。Cursor 对照：[Skills vs Subagents](https://cursor.com/docs/subagents)。

---

## 主 Agent 与主会话的职责（不可下放）

| 保留在主 Agent                            | 禁止默认交给子会话                       |
| ----------------------------------------- | ---------------------------------------- |
| 时间范围反问（见 `agent-conventions.md`） | 写入/修改/删除及 `--commit` 确认         |
| 向用户说明计划并获确认                    | 401 后统一停批、引导 `login` 再 `resume` |
| 合并子会话摘要并交付用户                  | 编造 `mediaCustomerId`、金额、业务数据   |
| 选择 Playbook（P1–P7）与必读 references   | 用子会话替代「每任务 Read references」   |

子会话**不继承**父对话历史；handoff 必须**自包含**（见下文）。

---

## 每任务决策流程（建议顺序）

1. Read 当次任务必读 references（`SKILL.md` 任务表 + `agent-conventions.md`）。
2. **若**任务属于 P5 / P6 / P7，或预计 CLI 日志冗长 / 需并行拉数 / 需读大段只读 SOP → **Read 本节决策矩阵**。
3. 选定执行模式：**主会话** | **单次 Bash 子会话** | **单次 Task handoff** | **并行多个 Task**。
4. 执行；子会话仅回传 `returnSchema`（见下），主 Agent 再脚本聚合或写报告。

**默认路径**：不确定时 → **主会话直接执行**（与「简单任务不滥用 subagent」一致）。

---

## 决策矩阵

| 信号                                            | 倾向                  | 推荐子会话类型                                         | 勿委派                   |
| ----------------------------------------------- | --------------------- | ------------------------------------------------------ | ------------------------ |
| 单次 `list-accounts -k`、P1 三步拉数、`-h` 查参 | **主会话**            | —                                                      | 为查一个账户开子会话     |
| `balance-scan` / `accounts-digest` 单命令       | **主会话**            | —                                                      | 外层 for-loop 逐账户     |
| 预计 CLI **>2 分钟** 或 stderr/stdout 很长      | **委派**              | 内置 **Bash** 或 Task + `snippets/handoff-*.md` 拉数段 | 在主会话逐行读日志       |
| **P6 OKKI**：拉数 → 写 xlsx（两阶段）           | **委派**              | 阶段 1：Bash/Task 拉数；阶段 2：Task 只读 snap 写脚本  | 子会话做写操作确认       |
| **P7 询盘**：`m1`/`m2`/`m3` 三月拉数            | **并行委派**          | 3× Task（`handoff-p7-inquiry.md` 子目录变体）          | 3× 主会话顺序跑          |
| **P5** `google-analysis-batch run` 全量         | **主会话或单次 Bash** | **一次** batch；CLI 内置并发                           | per-account 子会话调 API |
| **P5** batch **完成后** 按账户聚合              | **可选并行**          | N× Task，只读 `results/<accountId>/`                   | 子会话 `run` 新 batch    |
| 读 `google-ads/rules/*` 全文做方案              | **委派**              | **Explore** + `readonly`                               | 主会话 Read 全文进上下文 |
| 用户仅闲聊 / 解释字段口径                       | **主会话**            | —                                                      | —                        |

---

## Handoff 规范

### 必填字段（写入 Task prompt 或 Bash 说明）

| 字段              | 说明                                                                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `playbookId`      | `P5` / `P6` / `P7` 等                                                                                                                                  |
| `snapDir`         | `--json-out` 根目录（绝对或相对 cwd）                                                                                                                  |
| `mediaCustomerId` | 来自当次 `list-accounts`，禁止猜                                                                                                                       |
| `dateRange`       | `start` / `end`（YYYY-MM-DD）；P7 另附 `m1`/`m2`/`m3`                                                                                                  |
| `commands[]`      | 可复制 bash 块（来自 playbook 或 report-template）                                                                                                     |
| `forbidden[]`     | 至少包含：禁止 Read/cat 打开落盘业务 `*.json`（须 node/python 脚本读盘）；禁止把 JSON 贴进回复；禁止编造 ID/金额；禁止 batch 重新 `run`（仅 `resume`） |
| `returnSchema`    | 子会话**只**回传下列内容                                                                                                                               |

### returnSchema（子会话结束时的回复格式）

```text
exitCode: <number>
manifestFile: <path or "">
writtenFiles: [<path>, ...]
outlineFiles: [<path>, ...]
stderrTail: <last ~20 lines or "">
summary: <1-3 句中文，无业务数字除非来自 manifest>
```

主 Agent **不得**要求子会话生成 xlsx 话术或向用户确认写操作。

### Handoff 模板文件（复制进 Task prompt）

| Playbook    | 文件                                         |
| ----------- | -------------------------------------------- |
| P6 OKKI     | `{skillRoot}/snippets/handoff-p6-okki.md`    |
| P5 batch 后 | `{skillRoot}/snippets/handoff-p5-batch.md`   |
| P7 询盘     | `{skillRoot}/snippets/handoff-p7-inquiry.md` |

> **路径说明**：`snippets/` 与 `SKILL.md`、`references/` 同级（skill 安装根目录）。主 Agent 派发 Task 前先 Read 对应 handoff 文件，替换占位符后写入子会话 prompt。

---

## 内置 subagent vs 自定义 Task prompt

| 宿主能力                 | 何时优先                               |
| ------------------------ | -------------------------------------- |
| **Bash**（Cursor 内置）  | 纯 `siluzan-tso` 命令序列、长输出隔离  |
| **Explore** + `readonly` | 只读搜 reference / `rules/`，不改 snap |
| **Task + 自写 prompt**   | 需嵌入上表 `forbidden` 且 Bash 不够用  |

不要求固定子 Agent 名称；在 prompt 中写清角色即可（例：「TSO 拉数子任务，仅执行下列命令」）。

---

## Playbook 编排（P5 / P6 / P7）

### P6 · OKKI 周报

**必读**：`report-templates/okki-weekly-google-client.md`、`core/playbooks.md` P6。

1. 主 Agent：确认账户与日期区间。
2. **决策**：拉数阶段若日志长 → Bash/Task + `handoff-p6-okki.md` §拉数；否则主会话执行模板 §拉数命令。
3. **决策**：写 xlsx 阶段 → Task handoff（只读 `snapDir`，先 outline 后 JSON，见 `core/tips.md`）；或主会话若上下文充足。
4. 主 Agent：合并交付话术 + 文件路径；金额与 ID 与 manifest 一致。

### P5 · 多账户多维度

**必读**：`analytics/google-analysis-batch.md`、`core/playbooks.md` P5。

1. 主 Agent：确认区间与 `--sections`。
2. **batch 本身**：主会话或**单次** Bash 执行 `google-analysis-batch run`（全量省略 `-a`）或 `resume` — **禁止** per-account 子会话调 API。
3. 处理 stdout `kind=siluzan-tso-batch-summary` 与退出码；401 → 登录后 `resume`。
4. **可选**：账户数多且需分账户聚合 → 并行 Task，handoff 见 `handoff-p5-batch.md` §聚合，只读 `results/<accountId>/`。
5. 主 Agent：汇总报告；跨账户禁止心算。

### P7 · Google 询盘分析

**必读**：`report-templates/google-inquiry-analysis.md`、`core/playbooks.md` P7。

1. 主 Agent：询盘资料落盘或流程 B 反问。
2. **决策**：主 snap 拉数 + **并行** 3× Task 跑 `m1`/`m2`/`m3`（`handoff-p7-inquiry.md`），或主会话顺序执行若客户端不支持并行。
3. **单实例**写 8 Sheet xlsx：主会话或一次 Task（读 `geo-continents.json` 运行时加载）。
4. 主 Agent：交付；禁止扩展为 7 个月窗口。

---

## 客户端兼容说明

| 客户端             | 行为                                                                     |
| ------------------ | ------------------------------------------------------------------------ |
| **Cursor**         | 主 Agent 通过 Task 或内置 Bash/Explore 委派；不依赖 skill 包内 `agents/` |
| **无 subagent**    | 忽略本节，全部在主会话完成，仍遵守 `--json-out` 与 outline 纪律          |
| **Claude Code 等** | 若有子 Agent API，同样遵循 handoff + returnSchema                        |

---

## 反模式

- 为每个 Playbook 建固定 `.cursor/agents/` 文件且与 skill 双源维护。
- 子会话内 `Read` 多份 MB 级 `keywords-*.json` 并把内容贴回父会话。
- 用多个子会话替代 `google-analysis-batch` 内置并发。
- 子会话代替主 Agent 向用户确认 `--commit` 写操作。
