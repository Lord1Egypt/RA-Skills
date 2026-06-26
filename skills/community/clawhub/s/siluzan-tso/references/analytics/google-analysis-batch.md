# `google-analysis-batch` —— 多账户 × 多维度 Google 数据批处理引擎

> 适用：账户数 ≥ 5 且需拉 ≥ 2 个 google-analysis 维度。**禁止**外层 for-loop 替代。中断后**必须** `resume`，不得重跑 `run`。
>
> **数据时效性**：维度的实时 / 每日同步口径见 `references/analytics/account-analytics.md` 顶部「数据时效性」表。当天高消耗排行只能用 `--sections overview`，且**禁止**加 `--min-spend`（其预筛选来自非实时 `accountsoverview`）。

单 Node 进程，复用 keep-alive，双层并发（账户级 × 维度级），断点续跑，错误自动分类重试。

---

## 子命令

| 子命令   | 用途                                            |
| -------- | ----------------------------------------------- |
| `run`    | 首次执行：自动拉账户清单 + 双层并发 + 落盘      |
| `resume` | 续跑：仅重做 pending / failed_retryable 的 task |
| `status` | 只读查询进度与失败样例（不发起 HTTP）           |

---

## 命令示例

### 获取所有google账号的指定section数据（省略 `-a`，CLI 自动拉账户清单）

```bash
siluzan-tso google-analysis-batch run \
  --start 2026-04-30 --end 2026-05-06 \
  --sections campaigns,geographic,keywords \
  --account-concurrency 4 --section-concurrency 6 \
  --keyword-limit 1000 --min-spend 1 \
  --json-out ./snap-batch
```

### 显式指定账户（仅用户给出 ID 子集时）

```bash
siluzan-tso google-analysis-batch run \
  -a 9526903813,8525573641,3686000282 \
  --start 2026-04-30 --end 2026-05-06 \
  --sections campaigns,geographic,keywords \
  --json-out ./snap-batch
```

`-a` 给定时：跳过清单拉取与余额/消耗查询；不应用 `--min-spend`；`accounts.json` 元信息为空。**任何情况下都不要**先 `list-accounts` 再把全部 ID 拼进 `-a`。

### 中断后续跑

```bash
siluzan-tso google-analysis-batch resume --json-out ./snap-batch --run-id <runId>
```

从 `state/tasks.jsonl` 重建状态，跳过 success / failed_permanent / skipped，重做 pending / running / failed_retryable。

### 只读进度

```bash
siluzan-tso google-analysis-batch status --json-out ./snap-batch --run-id <runId>
```

不发起 HTTP，只读 `progress.json` + `tasks.jsonl`。

---

## 参数

| 参数                                 | 说明                                                                                                           | 默认值                             |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `--json-out <dir>`                   | 必填，产物根目录                                                                                               | —                                  |
| `--run-id <id>`                      | 自定义 runId                                                                                                   | 自动 `run-YYYYMMDD-HHmmss-<rand4>` |
| `-a, --accounts <ids>`               | 显式 ID 列表；传入则跳过清单拉取与 `--min-spend`                                                               | 省略时自动拉全量 Google 账号       |
| `--start` / `--end`                  | 统计区间（YYYY-MM-DD）                                                                                         | 近 7 天截至昨天                    |
| `--sections <list>`                  | 维度（逗号分隔），合法值见 `references/analytics/account-analytics.md`                                         | `campaigns,geographic,keywords`    |
| `--account-concurrency <n>`          | 账户级并发（1~16）                                                                                             | 4                                  |
| `--section-concurrency <n>`          | 单账户内维度并发（1~16）                                                                                       | 6                                  |
| `--keyword-limit <n>`                | keywords / search-terms 条数上限                                                                               | google-analysis 默认               |
| `--campaign-geo-cost-greater <n>` 等 | 仅 **`campaign-geo`**：与网关 `GetCampaignsGeoReport` 可选 query 一致；写入 `run-manifest.json`，`resume` 沿用 | 不设                               |
| `--min-spend <n>`                    | 区间消耗 ≤ 此值跳过（与 `-a` 同传无效）                                                                        | 0                                  |
| `--deadline <dur>`                   | 整任务硬截止（如 `30m` / `2h`），到期标记 paused                                                               | 不设                               |
| `--task-timeout-ms <n>`              | 单 task 硬超时                                                                                                 | 60000                              |
| `--max-attempts <n>`                 | 可重试错误最大尝试次数                                                                                         | 3                                  |
| `--refresh-dp`                       | 执行前强制刷新 Datapermission                                                                                  | false                              |
| `--no-verbose-progress`              | 关闭 stderr 进度条（CI 推荐）                                                                                  | false                              |
| `-t, --token`                        | 临时覆盖 Token                                                                                                 | `~/.siluzan/config.json`           |

---

## 产物目录

```
<json-out>/<runId>/
├── run-manifest.json           # 参数、账户总数、限流配置
├── progress.json               # 实时进度（每 5 task 原子刷新）
├── accounts.json               # 筛选后账户清单
├── results/<accountId>/
│   ├── <section>-<accountId>.json       # 与 google-analysis 同口径
│   ├── <section>-<accountId>.outline.txt
│   └── manifest-<accountId>.json
├── errors/<accountId>/
│   └── <section>.error.json     # class / status / message / attempts
└── state/
    ├── tasks.jsonl              # 事件溯源日志
    └── tasks.lock               # 运行时锁
```

**产物消费（Agent 强制顺序）**：**每个维度各读一份** `*.outline.txt`（同维度多账户同结构，读其一即可；一批并行把所有维度 outline 读全）了解字段类型 → 再写聚合脚本 → 由脚本读 `<section>-<accountId>.json`。**outline 没逐维读全，禁止开写脚本**（字段名以 outline 为准，不凭模板/通用命名猜——详见 `references/core/agent-conventions.md` §三 outline 门禁）。与单账户 `google-analysis` 完全同口径（含 **`campaigns`：`budgetAmountYuan` / `campaignTargetCpaYuan` / `maximizeConversionsTargetCpaYuan` 均为元**——outline 内嵌提示与单账户一致）。

**为什么先读 outline 而不是直接 `Read` JSON**：

- `*.outline.txt` 是与 `*.json` **同 stem 的纯文本**（**注意扩展名 `.txt` 不是 `.json`，不要 `require()`**），最后一行是 TS 式类型字面量（如 `{ items: { id: number; spend: number; ... }[]; meta: { ... } }`），通常几百字节。
- 真实 `<section>-<accountId>.json` 在批跑场景常见 `keywords-*.json` 数 MB、`campaigns-*.json` × N 账户合计几十万行，`Read` 会**几次就把对话窗口塞满**，还有截断风险。
- 读 outline 节省 **2~3 个数量级**的上下文 token，足够你确定字段路径再写脚本聚合。

读 outline 的最小写法（脚本里也只读最后一行）：

```js
const fs = require("node:fs");
// outlineFile 来自 manifest-<accountId>.json 的 sections[].outlineFile
const outline = fs.readFileSync(outlineFile, "utf8");
const tsType = outline
  .trimEnd()
  .split("\n")
  .filter((l) => !l.startsWith("//"))
  .pop();
// tsType 形如：{ items: { id: number; spend: number; ... }[]; meta: { ... } }
```

**禁止**：把 outline 内容当业务数据贴给用户当结论（第 1 行注释明确写了 `// outline of \`<xxx>.json\` — schema-only, NOT the data.`）。

---

## stdout 摘要协议

`run` / `resume` / `status` 的 stdout 始终一行 JSON（`kind=siluzan-tso-batch-summary`）：

```json
{
  "kind": "siluzan-tso-batch-summary",
  "runId": "run-20260507-150000-ab12",
  "state": "succeeded",
  "manifestFile": "<...>/snap-batch/run-.../run-manifest.json",
  "progressFile": "<...>/snap-batch/run-.../progress.json",
  "runDir": "<...>/snap-batch/run-...",
  "tokenInvalidated": false,
  "elapsedMs": 423000,
  "stats": {
    "totalTasks": 468,
    "success": 462,
    "failedPermanent": 4,
    "failedRetryable": 2,
    "skipped": 0,
    "throttleEvents": 1
  }
}
```

进度详情读 `progress.json` 与 `state/tasks.jsonl`，不在 stdout。

---

## 退出码

| 码  | 含义                                       | 后续动作                                      |
| --- | ------------------------------------------ | --------------------------------------------- |
| `0` | 全部成功，state=`succeeded`                | 继续后续                                      |
| `2` | 部分成功（`partial`）或超时（`paused`）    | 看 `errors/` 或消费已有产物                   |
| `3` | 全失败 / Token 失效 / 致命错误（`failed`） | `tokenInvalidated:true` → `siluzan-tso login` |
| `4` | 参数错误（命令未执行）                     | 修正参数重试                                  |

---

## 错误分类与重试

| 分类               | 触发条件                                         | 处理                                                                    |
| ------------------ | ------------------------------------------------ | ----------------------------------------------------------------------- |
| `abort`            | HTTP 401                                         | **立即终止整批**，`tokenInvalidated:true`，可 resume                    |
| `failed_permanent` | HTTP 400 / 403 / 404                             | 不重试，记入 `errors/`                                                  |
| `failed_retryable` | HTTP 408 / 429 / 5xx / 超时 / 网络错误           | 指数退避 `1s × 2^attempt + jitter`（cap 30s），最多 `--max-attempts` 次 |
| `skipped`          | `invalidOAuthToken=true` 或被 `--min-spend` 过滤 | 不发起 HTTP                                                             |

**自适应降级**：滚动 20 task 内错误率 ≥ 30% → 账户并发与维度并发同时减半；冷却 60s。`progress.throttleEvents` 记录次数。

---

## 与 google-analysis 的关系

`google-analysis` 会根据 `-a` 的 ID 数量自动选路，底层共享同一引擎：

|          | `google-analysis -a <单ID>` | `google-analysis -a id1,id2,id3`                        | `google-analysis-batch run` |
| -------- | --------------------------- | ------------------------------------------------------- | --------------------------- |
| 账户数   | 1                           | 2~10                                                    | 任意（含 0→自动拉全量）     |
| 调度     | 单账户多维度                | 双层并发                                                | 双层并发                    |
| 失败处理 | 抛错                        | 自动分类 + 退避 + 401 终止                              | 同左                        |
| 中断恢复 | 不支持                      | `resume`                                                | `resume`                    |
| stdout   | snapshot-batch              | `siluzan-tso-batch-summary`（含 `forwardedFrom`）       | `siluzan-tso-batch-summary` |
| 产物     | `<dir>/<section>-<id>.json` | `<dir>/<runId>/results/<accountId>/<section>-<id>.json` | 同左                        |

单 section JSON 结构完全一致，仅目录组织不同。

**选用**：1 账户 → `google-analysis -a id`；2~10 子集 → `google-analysis -a id1,id2,...`（隐式 batch）；≥10 子集/需 resume → `google-analysis-batch run -a id1,id2,...`；全量 → `google-analysis-batch run`（省略 `-a`）。

---

## 产物消费与 subagent（可选）

batch 完成后，主 Agent 按 `references/core/tips.md`：**先 outline 后 JSON**，脚本读盘聚合。

若宿主支持 subagent（见 `references/core/subagent-orchestration.md` § P5）：

- **batch `run` / `resume`**：主会话或**单次** Bash 执行，**禁止** per-account 子会话重复调 API。
- **按账户写报告片段**：可对每个 `results/<accountId>/` 并行 Task，handoff 见 `snippets/handoff-p5-batch.md` §阶段 B。
- 子会话**禁止**重新 `run` batch；401 由主 Agent 统一 `login` 后 `resume`。

---

## 常见问题

**Q：拉全量是不是先 `list-accounts` 再把 ID 拼进 `-a`？**
A：**不要**。`run` 不传 `-a` 时内部自动拉清单+余额+消耗，先 `list-accounts` 只是重复请求。直接 `google-analysis-batch run ...` 即可。

**Q：Ctrl+C 后能否重新 `run`？**
A：**不能**。会生成新 runId，所有 task 从零开始。只能 `resume --run-id <旧id>`。

**Q：怎么知道上次 runId？**
A：上次 stdout 摘要的 `runId` 字段，或浏览 `--json-out` 下最新 `run-*` 目录名。

**Q：401 后需要重跑全量吗？**
A：不需要。`siluzan-tso login` 后 `resume --run-id <id> --refresh-dp` 即可。

**Q：accounts.json 何时快照？能否手工改账户范围再 resume？**
A：首次 `run` 时写入并定型。要改账户范围，新建 runId 重新 `run`。

**Q：errors 文件能做什么？**
A：`class=permanent` → 对账户单独排查权限/参数；`class=retryable` 仍失败 → 过段时间 `resume`。
