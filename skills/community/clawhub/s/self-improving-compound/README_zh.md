# Self-Improving Compound

[English README](README.md)

一个可移植的 AgentSkill，用来把 Agent 记忆从零散 Markdown 升级成结构化自进化系统：实时捕获、SQLite 学习库、带显式上下文采集的 cron 审计、每日事实记忆、workspace 轻量维护。

## 核心能力

- **最终回复前捕获可复用经验**：用户纠正、工具/API 坑、非显然失败、workaround、缺失能力。
- **SQLite 作为执行学习源头**：默认写入 `learning/memory_tree/chunks.db`，支持 FTS5 搜索、确定性实体索引、去重、异步 job、生命周期、导出。
- **事实与教训分层**：事实连续性写入 `memory/YYYY-MM-DD.md`；可复用预防规则写入 `learning/`。
- **cron 自动审计**：轻量检查、重型审计、每日事实记忆、post-digest workspace steward。需要对话上下文的 cron 应优先使用确定性 collector，而不是依赖隐式会话可见性。
- **规则逐层沉淀**：稳定规则进入 `skills/`、`AGENTS.md`、`TOOLS.md`、`MEMORY.md` 等长期状态文件。


## 3+7 协同演化模型

这里的 **3+7** 指：3 个长期状态目录 + 7 个根目录 Markdown 控制面文件。

**3 个状态目录**

- `memory/`：每日事实连续性，记录发生了什么、做了什么决策、路径、链接、风险和 follow-up。
- `learning/`：SQLite 执行学习库，记录纠正、工具/API 坑、workflow 规则和可复用预防经验。
- `skills/`：沉淀后的可复用能力和流程说明。

**7 个根目录 Markdown**

- `AGENTS.md`：workspace contract、路由规则、执行策略、安全边界。
- `HEARTBEAT.md`：轻量 check-in 表面；当 cron 接管精确定时后可保持极简/空。
- `IDENTITY.md`：兼容入口或 identity 指针。
- `MEMORY.md`：pinned long-term hot context。
- `SOUL.md`：Agent 身份/persona。
- `TOOLS.md`：本地环境和工具事实。
- `USER.md`：用户画像、协作偏好、长期上下文。

Workspace Steward 只能做小而安全的一致性修正：不能重写人格、安全规则，也不能把每日事实堆进根文件。

## 安装：`clawhub install` 只是第一步

`clawhub install` 只会安装文件，不会自动完成自进化系统接线。真正可用至少需要：初始化 `learning/`、写入 capture gate、安装 cron、配置 delivery，必要时配置 hooks 和 daily collector。

```bash
clawhub install self-improving-compound
export OPENCLAW_WORKSPACE="/path/to/workspace"
# 可选：多个 workspace 共享同一套经验库。
# export SELF_IMPROVING_LEARNING_ROOT="$HOME/.openclaw/shared-learning"
export SELF_IMPROVING_SKILL_DIR="$OPENCLAW_WORKSPACE/skills/self-improving-compound"
export SELF_IMPROVING_LEARNINGS_CLI="$SELF_IMPROVING_SKILL_DIR/scripts/learnings.py"
python3 "$SELF_IMPROVING_LEARNINGS_CLI" --root "$OPENCLAW_WORKSPACE" init
python3 "$SELF_IMPROVING_LEARNINGS_CLI" --root "$OPENCLAW_WORKSPACE" status
```

完整安装配置流程见 `SKILL.md` 的 **Installation and activation** 部分。

建议 checklist：

1. 安装 skill 文件。
2. 设置 workspace / skill / CLI 环境变量；只有在多项目共享经验库时才设置 `SELF_IMPROVING_LEARNING_ROOT`。
3. 初始化 `learning/`。
4. 把 capture gate 写进 `AGENTS.md` 或等价 agent 指令。
5. 按 `scripts/setup-cron.json` 安装/更新 cron，并配置投递目标。
6. 可选：配置 `hooks/activator.sh` 和 `hooks/error-detector.sh`。
7. 可选：配置 `SELF_IMPROVING_LIGHT_CONTEXT_COLLECTOR` 保障 Light Check 上下文，配置 `SELF_IMPROVING_DAILY_COLLECTOR` 提升 Daily Memory Digest 质量。
8. 做 search / log / export / daily-memory / cron list smoke test。

要求：Python 3.8+、bash。本地 CLI 不需要网络访问。随包 `.sh` helper 明确依赖 bash；纯 POSIX `sh` 环境不保证可用，可直接调用 Python CLI。

## 快速开始

```bash
python3 scripts/learnings.py --root /path/to/workspace init
python3 scripts/learnings.py --root /path/to/workspace search "cron context" --limit 5
python3 scripts/learnings.py --root /path/to/workspace log-learning \
  --summary "需要对话上下文的 cron 应显式采集上下文" \
  --details "isolated cron 不会自动继承主对话；优先使用确定性 transcript/context collector，sessions_history 只作为验证过的 fallback。" \
  --pattern cron:explicit-context
python3 scripts/learnings.py --root /path/to/workspace process-jobs
python3 scripts/learnings.py --root /path/to/workspace maintain --apply
python3 scripts/learnings.py --root /path/to/workspace maintain --apply --auto-promote
bash scripts/learning-export.sh
```

长期运行时可启动本地 worker：

```bash
python3 scripts/learnings.py --root /path/to/workspace process-jobs --daemon --max-jobs 0
```

worker 会消费 `mem_tree_jobs`，生成 tree buffer/summary，并以 `maintain_lifecycle` job 执行 HOT/WARM/COLD 自动维护。

## 路径模型与架构边界

默认情况下，`--root /path/to/workspace` 会把经验库写到 `/path/to/workspace/learning/`。如果设置 `--learning-root` 或 `SELF_IMPROVING_LEARNING_ROOT`，SQLite、`index.md`、`heartbeat-state.md`、`promotion-queue.json` 会写到共享经验库；`promote` 和 `maintain --auto-promote` 仍然只会写入当前 workspace root 下的 `AGENTS.md`、`TOOLS.md` 等目标文件。

这不是完整复刻 OpenHuman 的内容管理平台，而是选择性移植：SQLite 存储、FTS 检索、实体索引、评分、hotness、异步 job、生命周期维护、确定性 tree buffer、promotion queue 已落地；LLM topic routing 和完整内容管理工作流不在这个 Python 层里承诺。

## 推荐 cron 管线

模板位于 `scripts/setup-cron.json`，安装说明位于 `scripts/setup-cron-agent.md`。

| Job | 默认时间 | 作用 |
|---|---:|---|
| Self-Improving Light Check | 08:00–22:00 每 2 小时 | 抓明显漏记的纠正、失败、blocker。 |
| Learning Audit Heavy | 09:00 / 22:00 | 审计系统/cron 失败，维护 HOT/WARM/COLD 生命周期。 |
| Daily Memory Digest | 23:50 | 写 `memory/YYYY-MM-DD.md`，再抽取可复用教训。 |
| Daily Workspace Steward | 00:20 | 导出 learning，轻量检查 `learning/`、`skills/`、7 个根目录 Markdown 控制面文件。 |

如果运行时能从本地 session/transcript store 导出近期可见对话，建议配置 Light Check collector：

```bash
export SELF_IMPROVING_LIGHT_CONTEXT_COLLECTOR="python3 /path/to/recent-context-collector.py --limit 60"
```

collector 规则：只有成功写出 Markdown/JSON 上下文文件才退出 0；找不到 transcript 时非零退出，让 cron 报 `BLOCKED: collector_unavailable`，不要假成功。

如果需要可观测队列和健康面板，使用内置 pipeline helper：

```bash
export SELF_IMPROVING_MEMORY_PIPELINE="$SELF_IMPROVING_SKILL_DIR/scripts/memory-pipeline.py"
python3 "$SELF_IMPROVING_MEMORY_PIPELINE" --base "$OPENCLAW_WORKSPACE/learning/pipeline" dashboard
```

它会在 `learning/pipeline/` 下写入 `candidates.jsonl`、`promotion-queue.json`、`cursor.json`、`status.json`、`dashboard.md`，并同步生成便捷入口 `learning/dashboard.md`。

安装 cron 需要用户确认。可以让 OpenClaw agent 执行：

> 使用 `scripts/setup-cron.json` 安装 self-improving compound cron jobs。先检查现有任务，有同名任务则 update，不要重复创建。

## 路径模型

- **Skill root**：本技能目录，包含 `scripts/`、`references/`、`hooks/`、`evals/`。
- **Workspace root**：实际项目或 Agent 状态目录，包含：
  - `learning/memory_tree/chunks.db`
  - `learning/index.md`
  - `memory/YYYY-MM-DD.md`
  - `AGENTS.md`、`MEMORY.md`、`TOOLS.md`、`USER.md`、`SOUL.md`、`HEARTBEAT.md`、`IDENTITY.md` 等根状态文件

不要把长期学习写进 skill 安装目录；始终使用 `--root /path/to/workspace`。

## 守护边界

- 先搜索再写入，避免重复。
- learning 条目要短、可搜索、偏预防规则。
- 不记录密钥、token、原始私密对话或易过期状态。
- cron audit 候选只是审计提示，不是自动真理。
- Workspace Steward 只能做小而安全的本地 Markdown 修正；不能重写人格、安全规则、删除文件或修改 cron。

维护者：Rockway Chen · <rockwaychen@gmail.com> · <https://github.com/LingmaFuture>
