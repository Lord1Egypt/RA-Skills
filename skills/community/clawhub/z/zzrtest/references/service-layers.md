# 交易链路分层与服务映射（DEV 测试环境）

> **与生产的最大差异**：测试环境**没有独立的 deal 服务**（无 `agg-deal` / `adapter-deal` / `ota-deal` 等），平台与供应均为 **`_{deve}` 等 DEV 后缀**的实例；供应底层多为 **`adapter_api_*`** 或 **`{channel}Adapter_deve`**。

## traceId → 环境后缀 + 采购侧

| traceId 模式 | 环境后缀 | 采购侧服务 |
|-------------|---------|-----------|
| `dev_web_b2b-deve_snake-...` | `deve` | `b2b_deve` |
| `dev_web_export-deve_snake-...` | `deve` | `export_*`（按 gray/后缀匹配，常见 `export_zzr`） |
| `web_b2b_*` / 含 `web_b2b` | 默认 `deve` | `b2b_deve` |
| `web_export_*` / 含 `web_export` | 默认 `deve` | `export_*` |
| 其他前缀 | 用 `match` 或询问用户 | 不要猜测 |

脚本从 traceId 中 `-deve_` / `_deve_` 等片段自动解析后缀，默认 `deve`。

---

## 平台侧（DEV，固定并行）

| 层级 | 服务名 | 说明 |
|------|--------|------|
| 平台-agg | `agg_deve` | 聚合、供应过滤、发起 adapter 搜索 |
| 平台-adapter | `adapter_route_deve` | 路由层（读 `supplierChannel` 判断底层） |

**不存在** `agg-deal`、`adapter-deal`。

---

## 供应侧（DEV）

### 第一轮必搜：`adapter_api_deve`

测试环境默认供应入口是 **`adapter_api_deve`**（与 traceId 环境后缀一致，默认 `deve`）。  
**不要用 gray 推断 `adapter_api_zzr`**；仅当用户**明确指定**某服务标签时才切换，例如：

```bash
python {SCRIPT} trace-search --text "{traceId}" --lane agg=zzr --lane adapter_api=zzr
python {SCRIPT} trace-search --text "{traceId}" --supplier agg_zzr adapter_api_zzr
```

### 服务泳道标签（按需指定，未说则 deve）

**规则**：用户说哪个服务用特殊标签，就只改那个服务；**没说的仍 deve**。

| 用户说法 | 影响 |
|---------|------|
| `ota_ztC` | 仅 OTA → `adapter_ota_ztC` |
| `agg_zzr` | 仅 agg → `agg_zzr` |
| `ndc_zzr` | 仅 NDC → `ndcAdapter_zzr` |
| 未说明 | 全部 `{服务}_deve` |

```bash
python {SCRIPT} trace-search --text "{traceId}" --lane ota=ztC
python {SCRIPT} infer-supplier --file .../agg_deve-deve.log --lane ota=ztC
```

> 例：`ota_ztC` 不会连带把 export / agg / adapter_route 改成 zzr。

### 从 `adapter_route` / `agg` 日志 → 底层 adapter

在 `adapter_route_deve` 或 `agg_deve` 日志中读取 **`supplierChannel`**（agg 发起 adapter 搜索时也会带）：

| supplierChannel | gdsType | 底层 DEV 服务 |
|-----------------|---------|--------------|
| `NDC` | 任意 | `ndcAdapter_deve` |
| `OTA` | 任意（无 domestic 路由） | `otaAdapter_deve`；用户指定 **`ota_{tag}`** → **`adapter_ota_{tag}`** |
| `OTA` + `domesticDealService` | 任意 | `otaAdapter-domestic_deve`（无 OTA 标签时） |
| `GDS` | `AMADEUS` / `1A` | `amadeusAdapter_deve` |
| `GDS` | `SABRE` | `sabreAdapter_deve` |
| `SPIDER` | 任意 | `spiderAdapter_deve` |
| `API` | 任意 | `apiAdapter_deve` / `adapter_api_*` |
| 无法判断 | — | `adapter_api_*`（兜底） |

脚本推断：

```bash
python {SCRIPT} infer-supplier --file ~/.DEV_SKILL/dev-find-log/{executeId}/agg_deve-deve.log
```

---

## adapter_route 失败 → 自动查底层供应

当 `adapter_route_deve` 或 agg 出现以下信号，**必须**继续查底层 adapter（禁止问用户）：

| 信号 | 说明 |
|------|------|
| `supplierSearchRs is empty` | adapter 返回空 |
| `adapter search return failed` | adapter 搜索失败 |
| `contextSnapshot is null` | 异步上下文丢失 |
| `supplierChannel=NDC` 等 | 从 agg/adapter_route 读 channel 定位 `ndcAdapter_deve` 等 |

示例（TRN / NDC）：agg 日志 `"supplierChannel":"NDC","supplierCode":"TRN"` → 第二轮搜 **`ndcAdapter_deve`** + **`adapter_api_deve`**。

---

## 供应底层深挖：触发信号

| 类型 | 典型关键字 |
|------|-----------|
| adapter 失败 | `supplierSearchRs is empty`、`contextSnapshot is null` |
| 供应错误码 | `303200006`、`3032*`、`301001033` |
| 校验/生单结果 | `deal.verify result`、`ufo verify` |
| HTTP 报文 | `Post url=`、`Request:`、`responseContent=` |
| 业务描述 | `舱位售罄`、`无运价`、`supplierCode=` |

---

## 生单 / 支付 / 申请出票

| 场景 | 额外并行搜索 |
|------|-------------|
| 生单 / 支付 / 申请出票 | `order_deve`（`trace-search --with-order`） |

---

## 并行搜索顺序

### 第一轮（必须并行，一条命令）

```bash
python {SCRIPT} trace-search --text "dev_web_b2b-deve_snake-xxx" --option "-A 20"
```

等价服务：`[b2b_deve, agg_deve, adapter_route_deve, adapter_api_deve, (order_deve)]`

### 第二轮（adapter_route 失败或需深挖时）

```bash
python {SCRIPT} infer-supplier --file ~/.DEV_SKILL/dev-find-log/{executeId}/agg_deve-deve.log

python {SCRIPT} search-batch \
  --text "dev_web_b2b-deve_snake-xxx" \
  --service ndcAdapter_deve adapter_api_deve \
  --execute-id "{executeId}" \
  --option "-A 30"
```

### 第三轮（供应底层 HTTP）

1. download 底层 adapter 日志（server 多为 `deve`）
2. `extract-reqresp` 或 grep 提取 req/resp

### 重试

全部无命中 → **统一扩大 ±5 分钟**后再并行 `trace-search` / `search-batch`；traceId 无时间戳时需手动 `--start-date`。

---

## download 说明

DEV 环境 download 的 `--server` 多为实例后缀，如 **`deve`**：

```bash
python {SCRIPT} download --execute-id "{uuid}" --service agg_deve --server deve
```
