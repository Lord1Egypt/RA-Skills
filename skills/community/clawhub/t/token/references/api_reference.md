# OPC Headroom Ingest API 参考文档

> 接口地址：<ADDRESS_REMOVED>

数据上报接口，将 headroom 压缩节省数据写入仪表盘。

---

## 一、三种提交格式

```jsonc
// 1) 单条（裸对象）
{ "model": "...", "inputTokens": 0, "outputTokens": 0, "savedTokens": 0, ... }

// 2) 批量（裸数组）—— 推荐
[ { ... }, { ... }, ... ]

// 3) 批量（带 events 字段）
{ "events": [ { ... }, { ... }, ... ] }
```

**批量上限 100 条/次**。超过返回 `batch_too_large`。

---

## 二、Header 必带

| Header | 必填 | 示例 | 作用 |
|---|---|---|---|
| `X-API-Key` | ✅ | `opc_user_5a8c...` | 从 `/tools/headroom-dashboard` 复制；服务端查 `public.user_api_keys` 表反查 `user_id` |
| `Content-Type` | ✅ | `application/json` | 解析 body |

---

## 三、Body 字段（共 8 个）

### 必填 4 个

| 字段 | 类型 | 约束 | 服务端处理 | 用途 |
|---|---|---|---|---|
| **`model`** | string | 非空，trim 后非空 | 服务端截断到 64 字符 | 模型名，原样展示（"gpt-4o" / "claude-sonnet-4" / "deepseek-v3" 等） |
| **`inputTokens`** | number | 整数，≥ 0，finite | `Math.floor()`，负数拒绝 | 压缩**前**的输入 token 数 |
| **`outputTokens`** | number | 整数，≥ 0，finite | `Math.floor()`，负数拒绝 | 压缩**前**的输出 token 数 |
| **`savedTokens`** | number | 整数，≥ 0，finite | `Math.floor()`，负数拒绝 | 本次**实际节省**的 token 数（不是 input+output，是 Δ） |

### 选填 4 个

| 字段 | 类型 | 约束 | 服务端处理 | 用途 |
|---|---|---|---|---|
| `savedCny` | number | ≥ 0，4 位小数精度 | `Math.round(v * 10000) / 10000` | 本次节省的人民币估值（元）。**不传则记 0**，仪表盘显示 ¥0.00 |
| `compressionRate` | number | 0 ≤ x ≤ 1 | 自动夹到 [0,1] | 压缩率 0~1（如 0.35 = 压了 35%）。**不传则记 NULL** |
| `metadata` | object | 任意 JSON | 原样存 | 自由扩展字段（sessionId、agent 名称、压缩策略版本等）。**不传则存 `{}`** |
| `createdAt` | string | ISO 8601，可被 `new Date()` 解析 | 转 UTC ISO | 事件**发生**时间。**不传则 server 用 `now()`**（建议不传，按 server 时间走） |

---

## 四、服务端自动填充（调用方不能传，传了也会被覆盖）

| 字段 | 类型 | 来源 | 说明 |
|---|---|---|---|
| `id` | uuid | DB `gen_random_uuid()` | 主键 |
| `user_id` | uuid | 从 `X-API-Key` 反查 `public.user_api_keys` | 事件归属用户；调用方传了也无效 |
| `created_at` | timestamptz | 调用方传的 `createdAt`，否则 `now()` | 入库时间 |

---

## 五、响应（统一 HTTP 200 + 业务码）

| 场景 | 响应 |
|---|---|
| 单条成功 | `{ "ok": true, "inserted": 1, "ids": ["<uuid>"] }` |
| 批量成功 | `{ "ok": true, "inserted": N, "ids": ["<uuid>", ...] }` |
| 缺 API Key | `{ "ok": false, "code": "unauthenticated" }` |
| Key 无效/已撤销 | `{ "ok": false, "code": "invalid_key" }` |
| Body 非 JSON | `{ "ok": false, "code": "invalid_body" }` |
| 空数组 | `{ "ok": false, "code": "empty_batch" }` |
| 超过 100 条 | `{ "ok": false, "code": "batch_too_large", "limit": 100 }` |
| 全部条目缺必填字段 | `{ "ok": false, "code": "no_valid_event" }` |
| DB 写入失败 | `{ "ok": false, "code": "internal_error" }` |

---

## 六、调用示例

### curl 单条

```bash
curl -X POST https://www.mrkjai.com/api/ingest/headroom \
  -H "X-API-Key: opc_user_你的key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "inputTokens": 1500,
    "outputTokens": 980,
    "savedTokens": 520,
    "savedCny": 0.052,
    "compressionRate": 0.35,
    "metadata": { "sessionId": "abc-123", "agentVersion": "v1.2.0" }
  }'
```

### curl 批量

```bash
curl -X POST https://www.mrkjai.com/api/ingest/headroom \
  -H "X-API-Key: opc_user_你的key" \
  -H "Content-Type: application/json" \
  -d '[
    { "model": "gpt-4o",          "inputTokens": 1500, "outputTokens": 980,  "savedTokens": 520, "savedCny": 0.052, "compressionRate": 0.35 },
    { "model": "claude-sonnet-4", "inputTokens": 3200, "outputTokens": 2100, "savedTokens": 1100, "savedCny": 0.115, "compressionRate": 0.34 },
    { "model": "claude-haiku-4",  "inputTokens": 8000, "outputTokens": 3200, "savedTokens": 4800, "savedCny": 0.05,  "compressionRate": 0.43 }
  ]'
```

### Python 客户端

```bash
# 安装 headroom 后，使用本项目提供的上报脚本
python ~/.workbuddy/skills/大模型token成本节约/scripts/opc_headroom_reporter.py --help
```

---

## 七、`savedTokens` vs `inputTokens`/`outputTokens` 说明

仪表盘 KPI 卡「总节省 Token = sum(saved_tokens)」，所以：

- ✅ `savedTokens` 必须是**真实节省的差值**，不是 `inputTokens + outputTokens`
- 例子：压前 prompt=1500 tokens，压后 prompt=980 tokens → 这次 `savedTokens = 520`
- 如果只想记录**调用规模**（不强调节省），把 `savedTokens` 设为 0；`savedCny` 也设 0；`compressionRate` 设为 0
- 仪表盘「平均压缩率」 = avg(`compression_rate`)，想看压缩效果就传压缩率

---

## 八、调用频率建议

- 接口本身无限速，但 DB 有写入开销
- 建议调用方做**本地聚合**：攒够一批（10~50 条）或定时（5~10 分钟）再 flush 一次
- 单次 100 条上限足够覆盖 30 分钟内一个 agent 跑 100 次 LLM

---

## 九、用户归属（自动，不用调用方管）

`X-API-Key` 从 `public.user_api_keys` 查：
- 每个用户登录就自动生成一行
- 同一用户的所有调用方（无论多少个 agent/脚本）都共用这个 Key
- 调用方传 `user_id` 字段无效，服务端以 Key 反查的 `user_id` 为准（防冒充）
- Key 可以在 `/tools/headroom-dashboard` 页面**重置**（旧 Key 立即失效）
