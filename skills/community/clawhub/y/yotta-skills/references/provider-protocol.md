# 扩展提供方协议 v1（元阁 · capability `o1.route` / `m1.adjudicate`）

> O1 动态路由的请求 payload 已加法扩展到 schema 2（新增 `request_features` / `usage` / `playbooks`）；
> 旧 provider 仍可按原 `skills[]` 响应工作，新 provider 可返回 `confidence` / `reasons` / `summary` / `alternatives`。

元阁可以可选地调用一个由用户显式配置的**本地扩展提供方（provider）**：

- `o1.route`：在已装技能白名单内对静态路由结果做增补 / 重排；未配置时 `--route` 行为与输出与之前完全一致。
- `m1.adjudicate`：对已装技能做 M1 记忆裁决，返回 `promote / hold / demote` 只读建议；未配置时 `decide-memory` 返回 `not_installed`，不写任何文件。

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
      "capabilities": ["o1.route"],
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

- 只在用户显式执行 `--route`（CLI）或 `route_request`（MCP，内部走同一 CLI）时触发；安装 / 更新 / 盘点等路径不触发。
- 元阁把**一个 JSON 请求**写入 provider 的 stdin（随后关闭），从 stdout 读**一个 JSON 响应**；stderr 只作诊断。
- stdout 上限 256 KB；超过按错误处理并回落。

```json
{
  "schema": 1,
  "capability": "o1.route",
  "request_id": "<uuid>",
  "payload": {
    "request": "帮我做发布前质量检查",
    "static_result": {
      "playbook": "delivery-quality-gate",
      "confidence": "high",
      "skills": ["yotta-anti-shallow", "yotta-code-quality", "yotta-publish-guard"]
    },
    "installed_skills": [
      { "slug": "yotta-code-quality", "version": "0.3.0", "sources": ["Codex"] }
    ]
  }
}
```

### 2.1 O1 动态路由 payload（schema 2）

```json
{
  "schema": 1,
  "capability": "o1.route",
  "request_id": "<uuid>",
  "payload": {
    "schema": 2,
    "request": "帮我做发布前质量检查",
    "request_features": {
      "request_hash": "<sha256>",
      "english_tokens": ["release", "quality"],
      "cjk_bigrams": ["发布", "质量", "检查"],
      "playbook_matches": [
        { "id": "delivery-quality-gate", "score": 6, "matched_keywords": ["检查", "质量", "发布"] }
      ]
    },
    "static_result": {
      "playbook": "delivery-quality-gate",
      "confidence": "high",
      "skills": ["yotta-anti-shallow", "yotta-code-quality", "yotta-publish-guard"]
    },
    "installed_skills": [
      {
        "slug": "yotta-code-quality",
        "version": "0.3.0",
        "description": "代码质量评审...",
        "status": "known",
        "sources": ["Codex"],
        "first_seen": "2026-08-23T00:00:00Z",
        "last_seen": "2026-10-01T00:00:00Z",
        "trust": "yottameta"
      }
    ],
    "usage": {
      "enabled": false,
      "skills": {},
      "last_route": null
    },
    "playbooks": [
      {
        "id": "delivery-quality-gate",
        "name": "交付质量门",
        "keywords": ["检查", "代码", "质量", "发布"],
        "skills": ["yotta-anti-shallow", "yotta-code-quality", "yotta-publish-guard"]
      }
    ]
  }
}
```

- `request_features` 由元阁本地确定性提取；`request_hash` 只用于审计关联，不用于还原原文。
- `usage.enabled=false` 时 `usage.skills` 为空；只有用户显式启用使用记录后，才发送聚合计数。
- `installed_skills` 只含 slug / 版本 / frontmatter description / 状态 / 来源标签 / 时间戳 / 信任标注；不含安装路径。
- `playbooks` 只含公开静态 playbook 元数据。

## 3. 响应

```json
{
  "ok": true,
  "capability": "o1.route",
  "data": {
    "policy": { "version": "o1-mvp-1" },
    "confidence": "high",
    "summary": "建议先跑防敷衍，再做代码质量评审，最后过发布守门。",
    "skills": [
      { "slug": "yotta-anti-shallow", "role": "先做防敷衍检查", "score": 82, "reason": "意图匹配 + 静态场景" },
      { "slug": "yotta-code-quality", "role": "补充代码质量评审", "score": 76, "reason": "历史使用 x2" },
      { "slug": "yotta-publish-guard", "role": "最后做发布守门", "score": 70, "reason": "静态场景 + 组合出现" }
    ],
    "reasons": [
      "意图匹配：检查 / 代码 / 质量 / 发布",
      "静态场景：交付质量门"
    ],
    "alternatives": [
      { "slug": "yotta-verify", "score": 54, "reason": "可补充装前安全扫描" }
    ]
  }
}
```

- `skills[].slug` 必须 ∈ `installed_skills` 白名单；未安装或未知的 slug 会被丢弃并记入 `dropped`，不会写入结果。
- `role` 可选；缺省时增补条目使用「由扩展提供方补充」。
- `confidence` 只接受 `high / medium / low`；非法值回落静态置信度。
- `reasons` / `summary` 只作为展示数据，限长并去除控制字符；不作为指令执行。
- `alternatives` 只接受白名单内、且未进入主组合的技能。
- 元阁先算静态结果：provider 给出的顺序用于重排；静态结果中未被提及的技能会**追加保留**，不会丢失。
- 返回空列表 / 全是不合法 slug：视为未应用（`applied = false`），静态结果原样返回。

需要授权或不可用时：

```json
{ "ok": false, "code": "license_required", "message": "该能力需要授权后使用" }
```

## 4. 状态与回落

| 状态 | 触发 | 元阁行为 |
| --- | --- | --- |
| `not_installed` | 无配置 / 无匹配 capability | 纯静态路由，文本输出与历史一致 |
| `active` | 调用成功且响应合法 | 白名单内增补 / 重排，静态结果保留 |
| `license_required` | provider 明确返回该 code | 纯静态路由 +「需授权」提示 |
| `timeout` | 超过 `timeout_ms` | 纯静态路由 + 一行状态提示 |
| `invalid_output` | 非 JSON / 缺 `ok` | 纯静态路由 + 一行状态提示 |
| `error` | 启动失败 / 退出码非 0 / 输出超限 / 配置非法 | 纯静态路由 + 一行状态提示 |

`--json` 输出始终包含 `dynamic` 块：`status` / `provider_id` / `applied` / `added` / `dropped` / `note`；
CLI 文本输出只在状态非 `not_installed` 时多一行「动态路由: ...」，退出码不受影响（始终 0）。

## 5. 审计与边界

- 每次实际调用写一行 `<YOTTA_PROVIDER_HOME>/provider-audit.jsonl`：`ts` / `capability` / `provider_id` / `status` / `duration_ms` / `bytes_out`。
- 审计**不记录**需求原文或任何 payload 内容。
- `usage` 只含聚合计数与技能 slug；不记录需求原文、记忆正文、路径或身份信息。
- P3 仅面向用户显式配置的本地 provider；未来云端 provider 的「只发特征、不传原文」模式留 P5。
- 元阁不替 provider 联网；provider 自身行为由它自己的包声明。
- 删除 `provider.json` 即回到纯静态路由，无残留依赖。
- provider 输出只当数据使用：白名单外的 slug、非法结构一律丢弃，不作为指令执行。

## 6. capability `m1.adjudicate`

### 6.1 触发

只在用户显式执行 `yotta-skills decide-memory`（CLI）或 MCP `decide_memory` 时触发。
安装 / 更新 / 盘点 / re-index / doctor 等路径不执行 M1 provider。

### 6.2 请求

元阁先把注册表与本地使用记录转成确定性特征快照，再发给 provider：

```json
{
  "schema": 1,
  "capability": "m1.adjudicate",
  "request_id": "<uuid>",
  "payload": {
    "schema": 1,
    "generated_at": "2026-09-30T00:00:00Z",
    "skills": [
      {
        "slug": "yotta-memory",
        "version": "0.20.0",
        "status": "known",
        "description": "文件式智能体记忆...",
        "first_seen": "2026-08-23T00:00:00Z",
        "last_seen": "2026-09-30T00:00:00Z",
        "last_signal_at": "2026-09-30T00:00:00Z",
        "pinned": false,
        "signals": {
          "used": 2,
          "named": 0,
          "accepted": 1,
          "route_hits": 5,
          "distinct_pairs": 3
        }
      }
    ]
  }
}
```

payload 不含需求原文、记忆正文、凭据、主机名、用户名、来源目录或任意文件路径。

### 6.3 响应

```json
{
  "ok": true,
  "capability": "m1.adjudicate",
  "data": {
    "policy": {
      "version": "m1-mvp-1",
      "promote_threshold": 60,
      "hold_threshold": 30,
      "cooling_days": 7
    },
    "decisions": [
      {
        "slug": "yotta-memory",
        "verdict": "promote",
        "score": 78,
        "reasons": ["used x2：+24", "组合出现 x3：+9"],
        "signals": {
          "used": 2,
          "named": 0,
          "accepted": 1,
          "route_hits": 5,
          "distinct_pairs": 3,
          "description_quality": 12,
          "recency": 10
        }
      }
    ]
  }
}
```

元阁只接受：slug 在本次注册表白名单内、verdict 为 `promote / hold / demote`、score 为 0-100。
未知 slug / 非法 verdict / 非法 score 一律丢弃并记入 `dropped`。

### 6.4 授权与回落

| 状态 | 触发 | 元阁行为 |
| --- | --- | --- |
| `not_installed` | 无配置 / 无匹配 capability | `decide-memory` 返回 `not_installed`，不写文件 |
| `active` | provider 返回合法 decisions | 展示建议；`--promote` 可写本地建议文件 |
| `license_required` | provider 明确返回该 code | 显示需授权；不阻断其他能力 |
| `timeout` / `invalid_output` / `error` | 超时 / 非法 JSON / 执行失败 | 显示状态；不写文件、不阻断 |

provider 内部应使用路线 B 授权门（capability `m1.adjudicate`）。未授权时返回：

```json
{ "ok": false, "code": "license_required", "message": "该能力需要授权后使用" }
```

### 6.5 建议文件与元忆边界

`--promote` 只写 `~/.yottaskills/memory-adjudication.json`，包含 decisions 与 `memory_candidates`。
`memory_candidates` 默认使用私密 `PREF`，不自动写元忆；用户或 AI 需要再显式调用元忆写入。
MCP `decide_memory` 始终只读，不写建议文件、不写元忆。
