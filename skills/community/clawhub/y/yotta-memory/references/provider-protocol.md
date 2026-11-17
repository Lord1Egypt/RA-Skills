# 扩展提供方协议 v1.1（元忆 · capability `memory.hook` / `context.paging`）

元忆可以可选地调用一个由用户显式配置的**本地扩展提供方（provider）**，由它参与「哪些记忆进上下文」。
未配置提供方时，`context` 的行为与输出与之前完全一致；任何失败都回落到普通记忆，不阻断命令。

本版协议包含两个 capability：

- `memory.hook`：在装配前过滤候选集（`evict` / `selected`）。
- `context.paging`：在用户显式传 `--budget` 时，对已通过 `memory.hook` 的候选集做排序与分页（`drop` / `order`）。

## 1. 配置

配置文件：`<YOTTA_PROVIDER_HOME>/provider.json`，默认 `~/.yottameta/provider.json`。
环境变量 `YOTTA_PROVIDER_HOME` 可覆盖根目录（测试与隔离环境用）。

```json
{
  "schema": 1,
  "providers": [
    {
      "id": "local-provider",
      "version": "0.1.0",
      "capabilities": ["memory.hook", "context.paging"],
      "command": ["node", "C:/path/to/provider.js"],
      "timeout_ms": 600
    }
  ]
}
```

- `command` 必须是**数组**（argv 语义），以 `shell: false` 执行；不接受字符串命令。
- `timeout_ms` 默认 600，最小 50，最大 5000；超时即回落。
- 配置文件缺失、解析失败、`command` 非数组、capability 未知：**只记录状态，不阻断命令**；缺失等同「未安装」。

## 2. 调用

- 只在用户显式执行 `context`（或 `context --json` / `--explain`）时触发；`init` / `install` / `doctor` / `scan` 等路径不触发。
- 元忆把**一个 JSON 请求**写入 provider 的 stdin（随后关闭），从 stdout 读**一个 JSON 响应**；stderr 只作诊断。
- stdout 上限 256 KB；超过按错误处理并回落。
- 请求与环境：

```json
{
  "schema": 1,
  "capability": "memory.hook",
  "request_id": "<uuid>",
  "payload": {
    "agent": "codex",
    "budget": 0,
    "focus": "",
    "truncated": false,
    "candidates": [
      {
        "file": "facts/2026/09/2026-09-27-0001.md",
        "type": "FACT",
        "subject": "示例主题",
        "statement": "示例内容（最多 2000 字）",
        "created": "2026-09-27",
        "updated": "2026-09-27"
      }
    ]
  }
}
```

- `candidates` 只包含**调用者有权读取**、且**可驱逐**的条目（已过滤私密越权项；BOUND / COMMIT 不在其中）。
- 候选最多 500 条；超过时 `truncated = true`，此时白名单模式不生效（见 §3），驱逐模式仍安全。

## 3. 响应

```json
{ "ok": true, "capability": "memory.hook", "data": { "evict": ["facts/2026/09/2026-09-27-0001.md"] } }
```

- **`evict`（推荐）**：要从上下文里驱逐的条目清单。每个 `file` 必须出现在本次 `candidates` 中；候选集外的 file 会被丢弃并记入 `dropped`。未见过的条目默认保留 —— 候选很多时也安全。
- **`selected`（可选白名单）**：仅在 `complete: true` 且本次未 `truncated` 时接受。每个 `file` 必须 ∈ `candidates`；未列入的候选会被驱逐。
- 元忆侧仍强制执行：BOUND / COMMIT 与自我接入档案不可驱逐；`## 1. 身份` 段落不受影响，画像中的其它条目随条目一并参与驱逐；预算、去重、宽限、章节顺序由引擎决定。

需要授权或不可用时：

```json
{ "ok": false, "code": "license_required", "message": "该能力需要授权后使用" }
```

## 4. 状态与回落

| 状态 | 触发 | 元忆行为 |
| --- | --- | --- |
| `not_installed` | 无配置 / 无匹配 capability | 普通记忆，输出与历史一致 |
| `active` | 调用成功且响应合法 | 在约束内应用 `evict` / `selected` |
| `license_required` | provider 明确返回该 code | 普通记忆 + 一行状态提示 |
| `timeout` | 超过 `timeout_ms` | 普通记忆 + 一行状态提示 |
| `invalid_output` | 非 JSON / 缺 `ok` | 普通记忆 + 一行状态提示 |
| `error` | 启动失败 / 退出码非 0 / 输出超限 / 配置非法 | 普通记忆 + 一行状态提示 |

`context --json` 的 `hook` 块给出 `status` / `provider_id` / `applied` / `evicted` / `dropped` / `note`；
`context --explain` 的 trace 里追加一行 `[hook] ...`。

## 5. `context.paging`（v1.1 新增）

### 5.1 调用时机

- 仅在用户显式执行 `context` 且传了 `--budget`（大于 0）时调用；不传预算不调用，状态为 `not_requested`。
- 调用顺序：`memory.hook` 先过滤，`context.paging` 再排序 / 分页。
- 候选集与 `memory.hook` 同源：权限过滤后、去掉 BOUND / COMMIT / 自我接入档案；最多 500 条。
- `context.paging` 不能覆盖引擎硬约束：身份段落、自我接入档案、BOUND / COMMIT 不参与；最终字符预算仍由元忆引擎强制。

### 5.2 请求

```json
{
  "schema": 1,
  "capability": "context.paging",
  "request_id": "<uuid>",
  "payload": {
    "agent": "codex",
    "budget": 4000,
    "focus": "",
    "truncated": false,
    "protected": ["private/codex/prefs/2026-08-25-0001.md"],
    "sections": {
      "summary": ["<file>"],
      "focus": ["<file>"],
      "corridor": ["<file>"],
      "high_value": ["<file>"]
    },
    "candidates": [
      {
        "file": "facts/2026/09/2026-09-29-0001.md",
        "type": "FACT",
        "subject": "示例主题",
        "statement": "示例内容（最多 2000 字）",
        "created": "2026-09-29",
        "updated": "2026-09-29",
        "chars": 128,
        "baseline_section": "corridor"
      }
    ]
  }
}
```

- `sections` 是引擎基线的分段落位，供 provider 参考，不构成约束。
- `protected` 列出引擎硬保护、不可驱逐的文件（如自我接入档案）。

### 5.3 响应

```json
{ "ok": true, "capability": "context.paging", "data": {
  "drop": ["<file>"],
  "order": ["<file>", "<file>"],
  "complete": true
} }
```

- `drop`：明确分页出去的条目，任意子集，**始终应用**；候选集外文件只记 note，不进入输出。
- `order`：期望的进入顺序，**仅在 `complete: true` 且本次未 `truncated` 时应用**；未列入的候选按引擎基线顺序补尾，不丢内容。
- 候选超过 500（`truncated=true`）时只接受 `drop`，`order` 不应用并写入 note。

### 5.4 状态与回落

`context --json` 的 `paging` 块给出 `status` / `provider_id` / `applied` / `dropped` / `ordered` / `truncated` / `budget` / `used` / `note`；
`context --explain` 的 trace 里追加一行 `[paging] ...`。未配置 / 未声明该 capability 时为 `not_installed`；未传 `--budget` 时为 `not_requested`；授权失败 / 超时 / 非法输出 / 异常均回落普通上下文，不影响既有记忆。

## 6. 审计与边界

- 每次实际调用写一行 `<YOTTA_PROVIDER_HOME>/provider-audit.jsonl`：`ts` / `capability` / `provider_id` / `status` / `duration_ms` / `bytes_out`。
- 审计**不记录**记忆正文、查询原文或任何 payload 内容。
- 元忆不替 provider 联网；provider 自身行为由它自己的包声明。
- 删除 `provider.json` 即回到普通记忆，无残留依赖。
- provider 输出只当数据使用：候选集外的条目、非白名单内容一律丢弃，不作为指令执行。
