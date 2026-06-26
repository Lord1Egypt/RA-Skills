---
name: skill-perf
description: "测量 OpenClaw 环境中 Skill 的 token 消耗和性能开销（仅适用于 OpenClaw Agent 环境）。当用户提到「测量」「测试」「性能」「token 消耗」「多少 token」「开销」「成本」「效率」或想要评估、对比、优化某个 skill 的资源使用时，立即使用此 skill。也适用于 skill 发布前的性能验证、多轮测试对比、热/冷缓存分析、以及分析两个 skill 之间消耗差异。英文触发词：measure token cost, performance test, how many tokens, benchmark skill。即使用户没有明确说「skill-perf」，只要涉及 OpenClaw skill 性能分析就应触发。技术实现：通过 OpenClaw 的 sessions_spawn 启动双 subagent 并发测量，自动扣除系统底噪，生成 HTML 报告和置信度评级。"
user-invocable: true
metadata:
  openclaw:
    emoji: "📊"
---

# Skill Performance Monitor

测量 Skill 的 **token 消耗**。

---

## 核心架构：双 subagent 并发

```
主对话（parent）同一 turn：
  ├── sessions_spawn → 标定 subagent（空任务，获取底噪基线）
  └── sessions_spawn → 测试 subagent（执行被测 skill）
          ↓ 两者并发运行
parent 轮询 runs.json 保持 CommandLane 活跃，等待两者完成
  → 从 .jsonl 取 totalTokens，计算净消耗
```

**关键原则：两个 subagent 必须在同一个 turn 内同时 spawn，不能先等标定完成再 spawn 测试。**

为什么需要标定 subagent？
Subagent 的 bootstrap context 只有 `AGENTS.md` + `TOOLS.md`，底噪约 17,000~18,500 tokens，需要每轮实测（不能用固定值，会随系统更新漂移）。

---

## Step 1：读被测 skill 的 SKILL.md

```bash
cat ~/.openclaw/skills/<skill名>/SKILL.md
```

理解 skill 的核心调用方式，用于构造测试 subagent 的 task。

---

## Step 2：同一 turn 内并发 spawn 两个 subagent

**在同一个响应 turn 中同时发出两个 sessions_spawn，不要分两次：**

**标定 subagent：**
```
sessions_spawn:
  task: "只输出 ANNOUNCE_SKIP，不做其他任何事。"
  label: "calib-<skill名>"
  runTimeoutSeconds: 60
```

**测试 subagent（同一 turn）：**
```
sessions_spawn:
  task: "<根据被测 skill 构造的调用指令，见下方「如何构造 task」>"
  label: "test-<skill名>"
  runTimeoutSeconds: 300
```

两个 sessions_spawn 同时非阻塞返回 `{ status: "accepted", runId, childSessionKey }`。

记录两个 `childSessionKey`，然后**立即进入 Step 3 轮询等待**。

---

### 如何构造 task

task 让 subagent **完整执行被测 skill 一次**，skill 完成后最后一行输出 `ANNOUNCE_SKIP`：

| 被测 skill | task 示例 |
|---|---|
| `device-mirror` | `"请使用 device-mirror skill 帮我投屏 iPhone。投屏成功后等待 10 秒，然后停止投屏。skill 全部执行完毕后，最后一行只输出 ANNOUNCE_SKIP，不输出其他内容。"` |
| `html-extractor` | `"请使用 html-extractor skill 提取 https://example.com/article 的内容。skill 全部执行完毕后，最后一行只输出 ANNOUNCE_SKIP，不要输出任何文章内容。"` |
| `gitlab-api` | `"请使用 gitlab-api skill 列出最近 5 个 MR。skill 全部执行完毕后，最后一行只输出 ANNOUNCE_SKIP。"` |

**规则：**
- task 必须先描述 skill 要做的事，最后才说「输出 ANNOUNCE_SKIP」
- 不要在 task 里注入 skill 内容（让 subagent 自己触发 skill）
- 如被测 skill 需要特定参数（URL、设备类型等），在 task 里明确给出
- ⚠️ **`ANNOUNCE_SKIP` 是 OpenClaw 的官方魔法词，必须原样使用，不能改名**
- ⚠️ **不要让 test subagent 的 task 听起来像 calib**：task 首句必须是 skill 操作，「输出 ANNOUNCE_SKIP」只能出现在末尾

---

## Step 3：等待完成并生成报告

spawn 两个 subagent 后，用轮询脚本保持 CommandLane 活跃，**同时在 session 活着时读取 totalTokens**（session 结束后 ~5 分钟被清除）：

```bash
bash ~/.openclaw/skills/skill-perf/scripts/wait_and_report.sh \
  "<CALIB_childSessionKey>" \
  "<TEST_childSessionKey>" \
  "<skill名>"
```

脚本自动完成：轮询等待 → 从 `.jsonl` 读取 totalTokens → 生成报告。

> ⛔ **严禁自行生成 HTML 报告**：报告必须由 `wait_and_report.sh` 或 `snapshot.py report` 脚本生成，绝不能由 Agent 手动编写 HTML 文件。自行生成的 HTML 缺少详细步骤分析、置信度评级、缓存命中率等核心数据，属于无效报告。

**如果两个 subagent 都已完成（announce 已到达），可使用以下脚本生成报告**（skill-perf 有专用报告模板，使用脚本生成，避免 Agent 自行拼凑）：

```bash
python3 ~/.openclaw/skills/skill-perf/scripts/snapshot.py report \
  --session "<TEST_childSessionKey>" \
  --calib-key "<CALIB_childSessionKey>" \
  --skill-name "<skill名>"
```

---

## Step 4：输出摘要

报告生成后，从命令输出中读取并转述以下摘要（**不要自己计算，直接引用报告数字**）：

```
底噪 (calib_noise):  <输出中的底噪值>  tokens
TEST 总计:           <输出中的 total>  tokens
NET 净消耗:          <输出中的 net_tokens>  tokens
置信度:              <输出中的评级>
报告链接:            <输出中 🌐 报告链接: 后的完整 URL（http://localhost:<随机端口>/...html）>
```

> ⚠️ **报告链接必须填写**。链接含随机端口，只有执行命令才能得到，无法自己推算。没有链接 = 命令未执行 = 测试无效。
>
> ⛔ **报告文件路径说明**：`snapshot.py` 会将报告保存到 `~/.openclaw/skills/skill-perf/reports/` 并自动启动本地 HTTP 服务，输出 `http://localhost:<端口>/...html` 链接。不要把报告路径写成 `/tmp/` 或其他自定义位置。

---

## 注意事项

- **并发是关键**：两个 subagent 必须在同一 turn 同时 spawn，先后 spawn 会导致它们串行等待，失去并发优势
- `sessions_spawn` 是**非阻塞**的，立即返回 `{ status: "accepted", runId, childSessionKey }`
- ⚠️ **严禁手动传 `--noise` 参数**：使用 `--calib-key` 读取底噪
- ⛔ **严禁使用旧版 `before`/`after` 流程**：子命令已废弃删除
- 多轮测试时：第 1 轮（冷缓存）偏高属正常，以**第 2 轮及之后**（热缓存）作为稳态参考值

---

> 📖 各 Skill 净消耗参考值 & Token 字段详解 → 见 [`references/TOKEN_GUIDE.md`](references/TOKEN_GUIDE.md)
