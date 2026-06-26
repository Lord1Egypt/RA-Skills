# LUI 定时任务三方权限 SQL 判断

## 使用场景

在 LUI/Claw 定时任务创建前，需要先判断两个三方权限问题：

1. 用户是否已经绑定下游店铺，以及店铺授权是否有效。
2. 用户要创建高级版任务时，对应店铺是否具备 ISV 高级版权限。

本文件给出 SQL 判断模板。实际接入时，把 `shopkeeper_bound_shop_result` 和 `isv_paid_status_result` 替换成真实落表、临时表、CTE 或接口批量调用后的结果表。为了兼容历史字段，SQL 输出仍可保留 `sv_*` 字段名和 `sv_not_paid` reason code，但面向用户展示时必须写作 ISV。

## 1. 店铺绑定与授权判断

绑定与授权状态来自 `1688-shopkeeper` 的店铺查询能力。其 `shops` 查询链路会调用 `/1688claw/skill/searchshop`，店铺结果至少需要落出以下字段：

| 字段 | 含义 |
| --- | --- |
| `ali_id` | 1688 用户 ID。 |
| `shop_code` | 下游店铺唯一编码，对应 `1688-shopkeeper` 返回的 `shopCode`。 |
| `shop_name` | 店铺名称，对应 `shopName`。 |
| `channel` | 平台类型，对应 `channel`，例如 `pinduoduo`、`douyin`、`kuaishou`、`thyny`、`xiaohongshu`。 |
| `tool_expired` | 工具授权是否过期，对应 `toolExpired`。 |
| `shop_expired` | 店铺授权是否过期，对应 `shopExpired`。 |
| `is_authorized` | 授权是否有效，推荐口径：`NOT (tool_expired OR shop_expired)`。 |

如果 LUI 已经解析出具体店铺范围，用下面的 SQL 判断每个目标店铺是否已绑定、是否授权有效：

```sql
-- 参数：
--   ${ali_id}：当前 1688 用户 ID
--   proposed_shops：LUI 解析出的目标店铺，至少包含 shop_code/channel

WITH proposed_shops AS (
  SELECT 'pdd_shop_code_1' AS shop_code, 'pinduoduo' AS channel
  -- UNION ALL SELECT 'dy_shop_code_1', 'douyin'
),
shopkeeper_bound_shop_result AS (
  -- 替换为 1688-shopkeeper shops 查询结果落表/临时表。
  -- 字段口径：
  --   shop_code = shopCode
  --   shop_name = shopName
  --   channel = channel
  --   tool_expired = toolExpired
  --   shop_expired = shopExpired
  --   is_authorized = NOT (toolExpired OR shopExpired)
  SELECT
    ali_id,
    shop_code,
    shop_name,
    channel,
    tool_expired,
    shop_expired,
    CASE
      WHEN COALESCE(tool_expired, false) = false
       AND COALESCE(shop_expired, false) = false
      THEN true ELSE false
    END AS is_authorized
  FROM your_shopkeeper_bound_shop_table
  WHERE ali_id = '${ali_id}'
)
SELECT
  p.shop_code,
  p.channel,
  s.shop_name,
  CASE WHEN s.shop_code IS NOT NULL THEN true ELSE false END AS is_bound,
  COALESCE(s.is_authorized, false) AS is_authorized,
  CASE
    WHEN s.shop_code IS NULL THEN 'not_bound'
    WHEN COALESCE(s.is_authorized, false) = false THEN 'authorization_invalid'
    ELSE 'ok'
  END AS permission_status
FROM proposed_shops p
LEFT JOIN shopkeeper_bound_shop_result s
  ON p.shop_code = s.shop_code
 AND p.channel = s.channel;
```

如果 LUI 没有指定店铺范围，先用下面的 SQL 统计用户可用店铺数量：

```sql
WITH shopkeeper_bound_shop_result AS (
  SELECT
    ali_id,
    shop_code,
    shop_name,
    channel,
    CASE
      WHEN COALESCE(tool_expired, false) = false
       AND COALESCE(shop_expired, false) = false
      THEN true ELSE false
    END AS is_authorized
  FROM your_shopkeeper_bound_shop_table
  WHERE ali_id = '${ali_id}'
)
SELECT
  COUNT(1) AS bound_shop_count,
  SUM(CASE WHEN is_authorized THEN 1 ELSE 0 END) AS valid_shop_count,
  SUM(CASE WHEN NOT is_authorized THEN 1 ELSE 0 END) AS invalid_auth_shop_count
FROM shopkeeper_bound_shop_result;
```

判断规则：

| SQL 结果 | 创建前决策 |
| --- | --- |
| `bound_shop_count = 0` | `block`，提示用户先绑定店铺。 |
| `valid_shop_count = 0` 且 `bound_shop_count > 0` | `block`，提示用户重新授权。 |
| `valid_shop_count = 1` 且 LUI 未指定店铺 | 可默认选择该唯一有效店铺。 |
| `valid_shop_count > 1` 且 LUI 未指定店铺 | `ask_confirmation`，要求用户选择店铺范围。 |
| 指定店铺中部分未绑定或授权失效 | `partial_create` 或 `block`，有效店铺可继续，无效店铺需提示原因。 |

## 2. ISV 高级版权限判断

ISV 高级版权限来自店铺付费状态接口：

```text
POST /DistributeApiNew/checkShopPaidStatus
Content-Type: application/json
```

请求体：

```json
{
  "aliId": "1688账号用户ID",
  "outShops": {
    "shopCode": "下游店铺唯一编码",
    "channel": "pinduoduo"
  }
}
```

返回口径：

| 字段 | 口径 |
| --- | --- |
| `code = 200` | 接口成功。 |
| `result.isPaid = true` | 店铺为付费店铺，可使用 ISV 高级版功能。 |
| `result.isPaid = false` | 店铺为免费店铺，不可使用 ISV 高级版功能。 |
| `code = 1002` | 参数错误、缺少必填或店铺不存在，应阻断该店铺。 |
| `code = 500` | 签名校验失败或系统错误，应走接口异常处理，不要误判为免费。 |

接口结果需要按目标店铺批量调用后落到 `isv_paid_status_result`，再用 SQL 与目标店铺合并：

```sql
-- 参数：
--   ${ali_id}：当前 1688 用户 ID
--   proposed_shops：经过绑定/授权过滤后的目标店铺
--   isv_paid_status_result：/DistributeApiNew/checkShopPaidStatus 接口结果落表

WITH proposed_shops AS (
  SELECT 'pdd_shop_code_1' AS shop_code, 'pinduoduo' AS channel
),
isv_paid_status_result AS (
  -- 替换为接口批量调用后的结果表。
  -- 必须保留 code/message/result.isPaid 的判断能力。
  SELECT
    ali_id,
    shop_code,
    channel,
    code,
    message,
    is_paid
  FROM your_isv_paid_status_result_table
  WHERE ali_id = '${ali_id}'
)
SELECT
  p.shop_code,
  p.channel,
  r.code AS paid_status_code,
  r.message AS paid_status_message,
  CASE
    WHEN r.code = 200 AND r.is_paid = true THEN true
    ELSE false
  END AS has_sv_advanced_permission,
  CASE
    WHEN r.code = 200 AND r.is_paid = true THEN 'ok'
    WHEN r.code = 200 AND COALESCE(r.is_paid, false) = false THEN 'sv_not_paid'
    WHEN r.code = 1002 THEN 'shop_not_found_or_param_error'
    WHEN r.code = 500 THEN 'paid_status_api_error'
    WHEN r.code IS NULL THEN 'paid_status_missing'
    ELSE 'paid_status_unknown_error'
  END AS sv_permission_status
FROM proposed_shops p
LEFT JOIN isv_paid_status_result r
  ON p.shop_code = r.shop_code
 AND p.channel = r.channel;
```

判断规则：

| SQL 结果 | 创建前决策 |
| --- | --- |
| `has_sv_advanced_permission = true` | 可继续创建高级版任务。 |
| `sv_permission_status = 'sv_not_paid'` | `block`，提示该店铺未开通 ISV 高级版，可开通或改成普通/低频任务。 |
| `sv_permission_status = 'shop_not_found_or_param_error'` | `block`，提示店铺信息异常或未查询到店铺。 |
| `sv_permission_status in ('paid_status_api_error', 'paid_status_unknown_error')` | 不要当作免费；提示系统暂时无法校验 ISV 权限，建议稍后重试或转人工。 |
| 多店铺中部分有 ISV 权限、部分没有 | `partial_create`，仅对有权限店铺继续，或让用户确认是否取消。 |

## 3. 创建前综合 SQL

高级版任务创建前，推荐把绑定/授权和 ISV 权限合并成一张预检结果表：

```sql
WITH proposed_shops AS (
  SELECT 'pdd_shop_code_1' AS shop_code, 'pinduoduo' AS channel
),
shopkeeper_bound_shop_result AS (
  SELECT
    ali_id,
    shop_code,
    shop_name,
    channel,
    CASE
      WHEN COALESCE(tool_expired, false) = false
       AND COALESCE(shop_expired, false) = false
      THEN true ELSE false
    END AS is_authorized
  FROM your_shopkeeper_bound_shop_table
  WHERE ali_id = '${ali_id}'
),
isv_paid_status_result AS (
  SELECT
    ali_id,
    shop_code,
    channel,
    code,
    message,
    is_paid
  FROM your_isv_paid_status_result_table
  WHERE ali_id = '${ali_id}'
)
SELECT
  p.shop_code,
  p.channel,
  b.shop_name,
  CASE WHEN b.shop_code IS NOT NULL THEN true ELSE false END AS is_bound,
  COALESCE(b.is_authorized, false) AS is_authorized,
  CASE
    WHEN s.code = 200 AND s.is_paid = true THEN true
    ELSE false
  END AS has_sv_advanced_permission,
  CASE
    WHEN b.shop_code IS NULL THEN 'not_bound'
    WHEN COALESCE(b.is_authorized, false) = false THEN 'authorization_invalid'
    WHEN s.code = 200 AND s.is_paid = true THEN 'ok'
    WHEN s.code = 200 AND COALESCE(s.is_paid, false) = false THEN 'sv_not_paid'
    WHEN s.code = 1002 THEN 'shop_not_found_or_param_error'
    WHEN s.code = 500 THEN 'paid_status_api_error'
    WHEN s.code IS NULL THEN 'paid_status_missing'
    ELSE 'paid_status_unknown_error'
  END AS create_permission_status
FROM proposed_shops p
LEFT JOIN shopkeeper_bound_shop_result b
  ON p.shop_code = b.shop_code
 AND p.channel = b.channel
LEFT JOIN isv_paid_status_result s
  ON p.shop_code = s.shop_code
 AND p.channel = s.channel;
```

综合判断：

| `create_permission_status` | 决策 |
| --- | --- |
| `ok` | 允许进入重复/冲突检测。 |
| `not_bound` | 阻断，提示先绑定店铺。 |
| `authorization_invalid` | 阻断该店铺，提示重新授权。 |
| `sv_not_paid` | 阻断高级版任务，提示开通 ISV 高级版或降级任务。 |
| `shop_not_found_or_param_error` | 阻断该店铺，提示店铺参数异常。 |
| `paid_status_api_error` / `paid_status_unknown_error` / `paid_status_missing` | 不创建任务，提示权限校验暂不可用，不要误判为免费。 |
