# Model Analysis Schema

用于 WotoHub 主链路中的“宿主模型优先理解”标准输出。

目标：
1. 统一产品语义理解输出
2. 为搜索 payload 编译提供稳定输入
3. 为邮件生成和推荐解释提供上游上下文

## 顶层结构

```json
{
  "product": {
    "productName": "string",
    "productType": "string",
    "productSubtype": "string",
    "categoryForms": ["string"],
    "coreBenefits": ["string"],
    "functions": ["string"],
    "targetAreas": ["string"],
    "targetAudiences": ["string"],
    "price": 49.99,
    "priceTier": "mid_price",
    "brand": "string",
    "sourceUrl": "https://...",
    "pageTitle": "string",
    "features": ["string"]
  },
  "marketing": {
    "platformPreference": ["tiktok"],
    "creatorTypes": ["string"],
    "creatorIntent": ["string"],
    "contentAngles": ["string"]
  },
  "constraints": {
    "regions": ["us"],
    "languages": ["en"],
    "minFansNum": 10000,
    "maxFansNum": 500000,
    "hasEmail": true
  },
  "searchPayloadHints": {
    "platform": "tiktok",
    "blogLangs": ["en"],
    "minFansNum": 10000,
    "maxFansNum": 500000,
    "hasEmail": true,
    "advancedKeywordList": [{"value": "electric toothbrush", "exclude": false}]
  },
  "clarificationsNeeded": [
    {"field": "productName", "reason": "缺少明确产品名"}
  ]
}
```

## 字段边界

- `product`：产品本体语义
- `marketing`：推广和内容方向理解
- `constraints`：搜索约束
- `searchPayloadHints`：给脚本执行层的软提示，主要用于 platform / 语言 / 粉丝量 / advancedKeywordList
- `clarificationsNeeded`：缺失字段提示，不代表执行失败

## 使用原则

- 宿主模型层优先输出这份结构
- 脚本层优先用 `product / marketing / constraints` 走标准编译链产出 `blogCateIds`
- `advancedKeywordList` 可以同时提供，但它是 refinement，不应替代类目映射
- 不要把 `searchPayloadHints.blogCateIds` / `searchPayloadHints.regionList` 当主注入方式
- 若 hints 不完整，可回退到 `product / marketing / constraints`
- 如宿主模型暂未提供输出，本地 fallback 只应作为兼容分析/调试产物，并明确标注 provenance；不要把它当成核心任务的默认 production understanding
- 不要把这个 schema 变成超重规则引擎
