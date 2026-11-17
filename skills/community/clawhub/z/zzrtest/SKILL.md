---
name: dev-find-log-skill
description: >
  DEV 测试环境服务器日志搜索与分析工具。当用户需要搜索测试环境日志、查找错误、
  排查测试环境问题、查询 traceId/requestId/订单号/请求记录、或者说"帮我查一下测试日志"、
  "查 dev 日志"、"看看测试环境有没有"、"grep 一下测试服"时，必须使用此 skill。
  校验、生单、支付、申请出票等交易场景，按采购侧→平台侧→供应侧→order 分层搜索，且必须并行查询。
  平台侧判断为供应底层请求/响应问题时，Agent 必须自动继续查供应侧日志（禁止询问用户是否继续）；确认供应响应报错后必须告知用户并输出底层 HTTP 请求与响应报文。
  关键词：测试环境、dev、查日志、搜日志、找日志、grep、traceId、requestId、校验、生单、支付、出票、
  export、b2b、agg_deve、adapter_route_deve、adapter_api、ndcAdapter_deve、order_deve、
  ota_ztC、adapter_ota_ztC、服务泳道标签、agg_zzr、
  供应底层、请求报文、响应报文、supplierChannel。
---

# DEV 测试环境日志搜索与分析 Skill

## 配置说明

缓存目录：`~/.DEV_SKILL/dev-find-log/`（自动创建，与生产 prod-find-log-skill 隔离）

### 与生产环境的唯一网关差异

生产与测试**共用同一网关** `https://devtool.flightroutes24.com`，通过 Header `profile` 区分环境：

| 项 | 生产（prod-find-log-skill） | 测试（本 skill） |
|---|---|---|
| API 网关 | `https://devtool.flightroutes24.com` | 相同 |
| `profile` | `PROD` | **`DEV`** |
| `gray` | `zzr` | `zzr` |
| `user` | `{账号}-{token}`，如 `zhaorong.zhou-{token}` | **`{账号}_dev-{token}`**，如 `zhaorong.zhou_dev-{token}` |
| `webVersion` | `1.0.0` | `1.0.0` |
| 浏览器搜索接口 | `POST /sse/searchLog` + SSE `GET /sse/connectLogEmitter` | 相同 |
| Agent 脚本接口 | `POST /sse/syncSearchLog`（同步封装，无需手动连 SSE） | 相同 |
| SSE executeId 前缀 | `{账号}-{uuid}` | **`{账号}_dev-{uuid}`** |
| 服务名示例 | `order`、`export` | `b2b_deve`、`agg_deve`、`adapter_route_deve`、`adapter_api_deve`、`ndcAdapter_deve` 等 |

### DEV 与生产的核心差异（必读）

| 项 | 生产（prod-find-log-skill） | 测试（本 skill） |
|---|---|---|
| 平台服务 | `agg-deal`、`adapter-deal` | **`agg_deve`、`adapter_route_deve`**（无 deal 分层） |
| 供应服务 | `domestic-deal`、`ota-deal`、`ndc-deal` 等 | **`adapter_api_*`**、`ndcAdapter_deve`、`otaAdapter_deve` 等 |
| 环境后缀 | 无 | 从 traceId 解析，如 `-deve_` → **`_deve`**，默认 `deve` |
| 供应推断 | adapter-deal 路由 Bean | **adapter_route / agg 的 `supplierChannel`** → 底层 adapter |

### 默认内置配置（Agent 公共账号）

- `profile`: `DEV`
- `user`: `dev-agentskill`
- `gray`: `zzr`
- `webVersion`: `1.0.0`

### 个人账号覆盖（可选）

若使用 devtool 个人 token（浏览器 F12 里 `user` 头的 `{账号}_dev-{token}` 格式），在缓存目录创建 `config.json`：

```json
{
  "user": "你的账号_dev-你的token",
  "sshToken": "你的账号-你的token"
}
```

路径：`~/.DEV_SKILL/dev-find-log/config.json`

> `sshToken` 对应浏览器请求体里的 `sshToken` 字段；测试环境 body 里也可能仍带生产侧 sshToken，以 devtool 实际要求为准。
> 脚本路径：用 `Glob` 查找 `dev-find-log-skill/scripts/dev_log.py` 的绝对路径，代入下文 `{SCRIPT}`。

---

## 交易场景：分层 + 并行搜索（核心）

**适用场景：** 校验、生单、支付、申请出票、搜索无报价

交易链路在 DEV 环境按四层分布。**禁止逐服务串行等待**，必须并行搜索：

| 层级 | 说明 | DEV 服务确定方式 |
|------|------|-----------------|
| ① 采购侧 | export / b2b | traceId 含 `web_b2b` / `web_export` + 环境后缀 → `b2b_deve` 等 |
| ② 平台侧 | agg + adapter_route | **固定**：`agg_{suffix}`、`adapter_route_{suffix}`（默认 `agg_deve`、`adapter_route_deve`） |
| ③ 供应侧 | adapter_api + 底层 adapter | **第一轮默认 `adapter_api_deve`**；从 adapter_route/agg 的 `supplierChannel` 推断 `ndcAdapter_deve` 等 |
| ④ 订单侧 | order | **生单 / 支付 / 申请出票** 时追加 `order_deve` |

> **测试环境没有 deal 服务**（不要用 `agg-deal`、`adapter-deal`、`ndc-deal`）。  
> 详细映射见 [references/service-layers.md](references/service-layers.md)。

### 并行搜索规则（必须遵守）

1. **第一轮必须并行**：采购侧 + `agg_deve` + `adapter_route_deve` + **`adapter_api_deve`** +（如有）`order_deve`，优先一条 `trace-search` 完成
2. **环境后缀**：从 traceId 解析（如 `dev_web_b2b-deve_snake-xxx` → `deve`），解析不到默认 `deve`
3. **默认用 deve 实例**：未特别说明的服务一律 `{服务名}_deve`（或 traceId 解析出的环境后缀）
4. **服务泳道标签（按需指定）**：用户说哪个服务用特殊标签，**仅该服务**走特殊实例；**没说的仍 deve**（见下文专节）。例如 `ota_ztC` 只影响 OTA → `adapter_ota_ztC`，export / b2b / agg / adapter_route 等不变
5. **禁止** 对每个服务单独串行 `search` 并等上一个结束
6. **Agent 工具调用**：若必须拆多条命令，必须在**同一轮**并行发起多个 Shell 调用
7. **第二轮（底层供应）**：读完 `adapter_route_deve` / `agg_deve` 的 `supplierChannel`，用 `infer-supplier` + `search-batch` 并行搜底层 adapter（带上用户指定的 `--lane`）
8. **adapter_route 失败必须继续查供应**：出现 `supplierSearchRs is empty`、`contextSnapshot is null`、`adapter search return failed` 时，**自动**按 `supplierChannel` 查底层 adapter；**禁止**询问用户
9. **供应底层深挖（条件触发）**：平台侧判断为供应 HTTP 问题时，**自动** download + `extract-reqresp` 输出 req/resp

### 推荐命令：trace-search（第一轮并行）

```bash
# 搜索 / 校验失败（DEV traceId）
python {SCRIPT} trace-search --text "dev_web_b2b-deve_snake-xxx" --option "-A 20"

# 生单 / 支付 / 申请出票
python {SCRIPT} trace-search --text "dev_web_b2b-deve_snake-xxx" --with-order --option "-A 20"

# 手动指定环境后缀
python {SCRIPT} trace-search --text "dev_web_b2b-deve_snake-xxx" --dev-suffix deve --option "-A 20"

# 手动指定单个或多个服务泳道（仅指定的服务走特殊标签，其余仍 deve）
python {SCRIPT} trace-search --text "xxx" --lane agg=zzr --option "-A 20"
python {SCRIPT} trace-search --text "xxx" --lane ota=ztC --option "-A 20"
python {SCRIPT} trace-search --text "xxx" --supplier agg_zzr ota_ztC --option "-A 20"
```

输出含 `executeId`、`plan.devSuffix`、`plan.laneOverrides`（如有）、各服务 `hit` 状态。

### 服务泳道标签（按需指定，未说则 deve）

**核心规则**：用户说哪个服务用特殊标签，就只对那个服务生效；**没提到的服务一律仍用 deve**（或 traceId 解析出的默认后缀）。

| 用户说法 | 生效范围 | 示例 |
|---------|---------|------|
| `ota_ztC` / `adapter_ota_ztC` | **仅 OTA 底层** | `adapter_ota_ztC` |
| `agg_zzr` | **仅 agg** | `agg_zzr`（adapter_route 未指定则仍 `adapter_route_deve`） |
| `agg_zzr` + `adapter_api_zzr` | agg + adapter_api | 两个都改，其余仍 deve |
| 未说明 | 全部 | `agg_deve`、`adapter_api_deve` 等 |

**Agent 必须：**

1. 从用户表述提取泳道覆盖，转为 `--lane` 或 `--supplier`：
   - `ota_ztC` → `--lane ota=ztC`
   - `agg_zzr` → `--lane agg=zzr` 或 `--supplier agg_zzr`
   - 可同时多个：`--lane ota=ztC --lane ndc=zzr`
2. **不要**因用户只说了 `ota_ztC` 就把整条链路切到 zzr
3. `infer-supplier` 必须带相同的 `--lane`，底层推断才用对应特殊实例
4. 第二轮 `search-batch` 只搜推断出的底层服务 + 默认 `adapter_api_deve`（除非用户也指定了 adapter_api）

```bash
# 例：仅 OTA 走 ztC，平台层全是 deve
python {SCRIPT} trace-search --text "{traceId}" --lane ota=ztC --option "-A 20"

python {SCRIPT} infer-supplier --file ~/.DEV_SKILL/dev-find-log/{executeId}/agg_deve-deve.log --lane ota=ztC

python {SCRIPT} search-batch \
  --text "{traceId}" \
  --service adapter_ota_ztC adapter_api_deve \
  --execute-id "{executeId}" \
  --option "-A 30"
```

> **不要全局推断**：用户没说 `agg_zzr` 就不要搜 `agg_zzr`；没说 `adapter_api_zzr` 就不要搜 `adapter_api_zzr`。

### 备选：search-batch（手动指定服务并行）

```bash
python {SCRIPT} search-batch \
  --text "dev_web_b2b-deve_snake-xxx" \
  --service b2b_deve agg_deve adapter_route_deve adapter_api_deve \
  --option "-A 20"
```

### Step 1A：从 traceId 确定采购侧 + 环境后缀

| traceId 信号 | 采购侧 | 环境后缀 |
|-------------|--------|---------|
| 含 `web_b2b` + `-deve_` | `b2b_deve` | `deve` |
| 含 `web_export` + `-deve_` | `export_*`（match 匹配） | `deve` |
| 含 `web_b2b` | `b2b_deve` | 默认 `deve` |
| 含 `web_export` | `export_*` | 默认 `deve` |
| 其他 | 用 `match` 或询问用户 | 默认 `deve` |

### Step 1C：从 adapter_route / agg 日志确定底层供应

在第一轮结果中读取 **`adapter_route_deve`** 或 **`agg_deve`**（agg 发起 adapter 搜索时也会打印 `supplierChannel`）：

- `"supplierChannel":"NDC"` → **`ndcAdapter_deve`**
- `"supplierChannel":"OTA"` + 用户指定 **`ota_ztC`** → **`adapter_ota_ztC`**（`infer-supplier --lane ota=ztC`）
- `"supplierChannel":"OTA"` + `domesticDealService` → **`otaAdapter-domestic_deve`**（无 OTA 标签时）
- `"supplierChannel":"OTA"` → **`otaAdapter_deve`**（无 OTA 标签时）
- `"supplierChannel":"GDS"` + AMADEUS/1A → **`amadeusAdapter_deve`**
- 路由 Bean：`*DealService` → 对应 `{channel}Adapter_deve`
- 无法判断 → **`adapter_api_deve`**

```bash
python {SCRIPT} infer-supplier --file ~/.DEV_SKILL/dev-find-log/{executeId}/agg_deve-deve.log
# 用户指定了服务泳道时带上相同 --lane，如 --lane ota=ztC
python {SCRIPT} infer-supplier --file ~/.DEV_SKILL/dev-find-log/{executeId}/agg_deve-deve.log --lane ota=ztC
```

**adapter_route 失败时（必须自动执行）**：例如 agg 报 `supplierSearchRs is empty` + `"supplierChannel":"NDC"` → 立即 `search-batch` 查 **`ndcAdapter_deve`**：

```bash
python {SCRIPT} search-batch \
  --text "dev_web_b2b-deve_snake-xxx" \
  --service ndcAdapter_deve adapter_api_deve \
  --execute-id "{executeId}" \
  --option "-A 30"
```

---

## 供应底层深挖（条件触发，自动执行，禁止询问用户）

当**平台侧**分析表明失败来自**供应底层**或 **adapter_route 搜索失败**时，Agent **必须**在本轮对话内自动完成底层 adapter 搜索、下载、提取报文。

### Agent 行为约束（必须遵守）

| 规则 | 说明 |
|------|------|
| **禁止询问** | 不得问「是否需要查供应侧」「要不要看底层报文」等；直接执行 |
| **自动推断供应侧** | 优先 `infer-supplier` + `adapter_route_deve` / `agg_deve` 的 `supplierChannel` |
| **adapter_route 失败必查** | `supplierSearchRs is empty`、`contextSnapshot is null` → 按 channel 查 `ndcAdapter_deve` 等 |
| **同轮完成** | 供应侧 `search-batch` → `download` → `extract-reqresp` |
| **确认后必说** | 供应响应报错时**必须告知用户**并贴出 req/resp |

### 触发条件（满足任一即触发）

在 `adapter_route_deve` 或 `agg_deve` 日志中出现：

| 类型 | 典型信号 |
|------|---------|
| adapter 失败 | `supplierSearchRs is empty`、`contextSnapshot is null`、`adapter search return failed` |
| 供应错误码 | `303200006`、`3032*`、`301001033` 等 |
| 供应结果日志 | `deal.verify result`、`ufo verify` |
| HTTP 调用痕迹 | `Post url=`、`Request:`、`responseContent=` |
| 业务描述 | `无运价`、`supplierChannel`、`supplierCode=` |
| 路由信号 | `"supplierChannel":"NDC"` 等（agg 发起 adapter 搜索时可见） |

```bash
python {SCRIPT} infer-supplier --file ~/.DEV_SKILL/dev-find-log/{executeId}/agg_deve-deve.log
```

当 `needSupplierDig: true` 或 `adapterRouteFailed: true` 时**必须**进入本流程。

### 执行步骤

1. 从 `adapter_route_deve` / `agg_deve` 推断底层 adapter（`infer-supplier`）
2. **并行搜索** `ndcAdapter_deve` 等 + `adapter_api_*`
3. download（`--server deve` 常见）
4. `extract-reqresp` 或 grep 提取报文
5. 回复用户：先供应底层结论，再平台链路结论

```bash
python {SCRIPT} search-batch \
  --text "dev_web_b2b-deve_snake-xxx" \
  --service ndcAdapter_deve adapter_api_deve \
  --execute-id "{executeId}" \
  --option "-A 30"

python {SCRIPT} extract-reqresp \
  --file ~/.DEV_SKILL/dev-find-log/{executeId}/ndcAdapter_deve-deve.log \
  --trace "dev_web_b2b-deve_snake-xxx"
```

### 输出要求（回复用户时必须包含）

**若供应侧确认返回错误**，须先写：

> **供应底层返回错误**：{supplierCode} 接口返回 `{errorCode}` — {msg}

分析中**必须单独一节「供应底层请求 / 响应」**，包含：供应侧服务（如 `ndcAdapter_deve`）、supplierCode、HTTP URL、请求/响应 JSON、错误映射。

---

## 通用工作流程

### Step 2：解析时间

traceId / requestId 会在 `search` / `trace-search` 时自动解析时间，**不需要单独调用 parse-time**。

时间规则：
- **长格式**（末尾 ≥13 位数字）：前 13 位毫秒 epoch，UTC 转 CST
- **短格式**（字母/下划线 + 12 位 YYMMDDHHmmss）：直接解析为 CST
- `startDate` 等于日志时间（不减分钟）

### Step 3：搜不到时的重试（并行重试）

**所有服务统一扩大时间后，再次并行搜索**（不要逐个串行重试）：

1. 第一轮：精确时间 `trace-search`
2. 全部无命中 → 扩大 ±5 分钟，用同一 `executeId` 或新 `executeId` 再跑一轮 `trace-search` / `search-batch`
3. 仍无结果 → 记录各层无日志，继续分析已有命中的服务

```bash
python {SCRIPT} trace-search \
  --text "web_export_xxx" \
  --start-date "2026-06-30 16:15:40" \
  --end-date "2026-06-30 16:25:40" \
  --option "-A 20"
```

**`--option` 建议：**
- `-A 10` ~ `-A 20`：交易场景推荐
- 信息截断时增大 `-A`（如 `-A 50`）

### Step 4：下载日志文件

对每个有结果的条目**并行 download**（同一轮多个 Shell 调用）：

```bash
python {SCRIPT} download \
  --execute-id "uuid" \
  --service "agg_deve" \
  --server "deve"
```

traceId 无内嵌时间戳时（如 `dev_web_b2b-deve_snake-{uuid}`），需手动指定 `--start-date`（从已命中日志或用户处获取）。

### Step 5：分层分析

按链路顺序还原时间线：采购侧 → `agg_deve` → `adapter_route_deve` → `adapter_api_*` / 底层 adapter → `order_deve`。

分析要点：

1. 查找 `ERROR`、`Exception`、业务错误码，给出根因与建议
2. **若触发「供应底层深挖」**（见上文）：**自动**查供应侧，禁止询问用户；供应响应报错时**必须先告知用户**并输出底层 HTTP **请求 + 响应**报文及错误码映射

---

## 非交易场景

用户未描述校验/生单/支付/出票，或明确指定单个服务时：

```bash
python {SCRIPT} match "关键词"
```

- `matched` 非空 → 直接用
- `matched` 为空 → 展示 `candidates` 让用户选择

---

## 注意事项

- **仅用于测试环境**：本 skill 固定 `profile=DEV`，不要用于生产排障（生产请用 `prod-find-log-skill`）
- **不要用 deal 服务名**：测试环境用 `agg_deve`、`adapter_route_deve`，不是 `agg-deal` / `adapter-deal`
- **默认 deve 实例**：未特别说明的服务一律 `{服务}_deve`；**不要用 gray 全局推断 zzr**
- **服务泳道标签**：用户说哪个服务用特殊标签就只改那个；例 `ota_ztC` → 仅 `adapter_ota_ztC`，其余仍 deve
- **zzr / 其他标签**：仅用户明确提到时才加 `--lane`，如 `--lane agg=zzr --lane adapter_api=zzr`
- **第一轮必含 adapter_api_deve**：`trace-search` 默认加入，非 `adapter_api_zzr`
- **环境后缀默认 deve**：从 traceId `-deve_` 解析；采购侧 `b2b_deve`、平台 `agg_deve` + `adapter_route_deve`
- **adapter_route 失败必查底层**：按 `supplierChannel` 继续搜 `ndcAdapter_deve` 等；禁止问用户
- **交易场景必须并行分层搜索**
- **禁止串行逐服务搜索**
- **供应底层问题**：自动查底层 adapter 并输出 req/resp
- **生单/支付/出票**：`trace-search --with-order`（追加 `order_deve`）
- **devtool NPE 误报**：若搜索结果仅为 `java.lang.NullPointerException` 字符串，视为无效命中，需 download 或手动 `--start-date` 重试
- **敏感信息**：分析完成后可提示删除 `~/.DEV_SKILL/dev-find-log/{executeId}/`
