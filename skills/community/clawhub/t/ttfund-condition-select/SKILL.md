---
name: ttfund-condition-select
description: "天天条件选基 Skill。使用 FUND_CONDITION_SELECT 能力按基金分类、风险等级、费率、收益和回撤等条件进行筛选，返回候选基金与关键分析字段。"
---

# 天天条件选基skill

通过自然语言或结构化参数调用 `FUND_CONDITION_SELECT` 对应能力，接口返回 JSON 格式内容。

## 使用方式

1. 在调用任何接口前，必须先检查本地环境变量 `TTFUND_APIKEY` 是否存在。
2. 若本地已存在 `TTFUND_APIKEY`，则直接使用该 apikey 发起请求。
3. 若本地不存在 `TTFUND_APIKEY`，必须强制引导用户先配置 apikey，不得跳过。
4. apikey 获取路径：
   - 打开天天基金
   - 搜索 skills
   - 在对应 Skills 页面获取 `天天条件选基skill` 对应的 apikey
5. 当检测到 apikey 缺失时，必须明确提示用户：
   - `当前未检测到本地环境变量 TTFUND_APIKEY，请先前往天天基金搜索 skills 获取 apikey，并在本机配置该环境变量后再继续使用。`
6. 在用户未完成 apikey 配置前，不继续执行 skill 查询请求。
7. 配置完成后，使用 POST 请求调用统一网关接口，并将 apikey 放入 `X-API-Key` 请求头中。

## 调用规范

- URL：`https://skills.tiantianfunds.com/ai-smart-skill-service/openapi/skill/invoke`
- Method：`POST`
- Headers：
  - `X-API-Key: $TTFUND_APIKEY`
  - `Content-Type: application/json`
- Body：

```json
{
  "skill_id": "FUND_CONDITION_SELECT",
  "pageIndex": 1,
  "pageNum": 20,
  "rsfType": "002",
  "rsbType": "002001",
  "fundLevel": "4,5",
  "riskLevel": "3,4",
  "orderField": "5_6_-1"
}
```

说明：
- `skill_id` 固定为 `FUND_CONDITION_SELECT`。
- 其余筛选参数按用户问题按需补充，不要无关参数全部硬塞。

## 示例 curl

```bash
curl --location 'https://skills.tiantianfunds.com/ai-smart-skill-service/openapi/skill/invoke' \
--header "X-API-Key: $TTFUND_APIKEY" \
--header 'Content-Type: application/json' \
--data '{
  "skill_id": "FUND_CONDITION_SELECT",
  "pageIndex": 1,
  "pageNum": 20,
  "rsfType": "002",
  "rsbType": "002001",
  "fundLevel": "4,5",
  "riskLevel": "3,4",
  "orderField": "5_6_-1"
}'
```

## 问句示例

- 帮我调用 FUND_CONDITION_SELECT
- 按风险等级 3-4 且基金评级 4-5 筛选可购买基金
- 给我找近一年收益靠前、最大回撤较小的主动权益基金

## 返回解释（核心）

优先解释这些字段：
- `Succeed`
- `ErrCode`
- `Message`
- `TotalCount`
- `Data.fundCode`
- `Data.fundName`
- `Data.company`
- `Data.fundtype`
- `Data.yearSyl`
- `Data.yearReturn`
- `Data.riskLevel`

## 交互规范

1. 优先检查环境变量 `TTFUND_APIKEY`。
2. 若环境变量存在，则继续调用接口。
3. 若环境变量不存在，必须中断当前调用，并强制提示用户先完成 apikey 配置。
4. 若缺少关键筛选参数，先澄清后再调用。
5. 返回结果时优先给出结论和推荐候选，不要原样堆砌全部字段。

## 错误处理

- 若缺少 apikey，应提示：
  - `当前未检测到 TTFUND_APIKEY，请先前往天天基金搜索 skills 获取 apikey，并在本机配置该环境变量后重试。`
- 若 HTTP 请求失败、超时或返回非 2xx 状态码，应提示：
  - `天天条件选基skill服务暂时不可用，请稍后重试。`
- 若业务 `ErrCode` 非 0，视为失败并简要说明错误原因。
- 若结果为空，提示用户放宽筛选条件（例如放宽风险等级、回撤阈值、时间范围）。

## 安全与边界

- 该 Skill 返回的是天天条件选基能力对应的数据，请按业务场景谨慎使用。
- 返回内容仅用于当前用户请求的查询与分析，不应伪造结果或输出未验证内容。
- 输出不构成投资建议。
