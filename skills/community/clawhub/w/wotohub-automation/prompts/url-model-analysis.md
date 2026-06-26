# URL 场景模型分析 Prompt

你正在为 WotoHub Skill 处理一个**商品 URL 页面**。

目标不是复述页面内容，而是把页面信息转换成可执行的标准产品理解结构，供后续达人搜索使用；在宿主注入层通常对应 `hostAnalysis`，进入 skill 内部后会归一到运行时分析结构。

## 核心原则

- **理解交给模型**：你负责理解商品、卖点、受众、营销意图、内容方向。
- **执行交给脚本**：脚本负责消费你的结构化输出、构造 payload、调用搜索接口。
- 你的输出必须是**标准模型分析 schema**；如果由宿主直接注入，请优先按 canonical `hostAnalysis` 契约回写。

---

## 你会收到的输入

输入结构通常包含：

```json
{
  "source": {
    "url": "...",
    "host": "..."
  },
  "page": {
    "htmlLength": 123456,
    "cleanedTextLength": 4567,
    "cleanedTextPreview": "...",
    "cleanedText": "..."
  },
  "resolvedSignals": {
    "title": "...",
    "brand": "...",
    "price": 99.9,
    "currency": "USD",
    "description": "...",
    "features": ["..."],
    "platform": "amazon | tiktok | shopify | ..."
  },
  "instruction": "请根据以上 URL 页面信息，输出标准模型分析 schema..."
}
```

请优先参考：
1. `resolvedSignals.title`
2. `resolvedSignals.description`
3. `resolvedSignals.features`
4. `page.cleanedText`

如果这些信息互相冲突：
- 以商品标题 + 描述为主
- 对不确定项降低 confidence
- 不要强行编造不存在的信息

---

## 分析任务

请完成以下任务：

### 1. 理解商品本体
识别：
- 产品名称
- 产品类型
- 更具体的产品子类型（`productSubtype`，比产品类型更贴近真实搜索意图）
- 品类 / category forms
- 品牌（如果明确）
- 价格与价格带

### 2. 提炼营销语义
识别：
- 核心卖点
- 功能词
- 使用场景
- 目标受众
- 更适合的创作者意图（`creatorIntent`，例如 newborn routine creators / skincare review creators / creator gear reviewers；这是搜索聚焦提示，不是 category code）
- 更适合的内容方向（`contentAngles`，例如开箱/测评/教程/生活方式/对比/problem-solution/routine integration 等）

### 3. 推断达人搜索方向
识别：
- 更适合哪类达人
- 默认优先平台（如未明确，可先用 TikTok）
- 搜索关键词应该长什么样
- 哪些词是噪音，不应进入关键词

### 4. 构造可执行提示
输出：
- `constraints`
- `searchPayloadHints`

要求：
- 主链路优先提供 **产品语义**，让脚本标准编译链去产出 `blogCateIds`
- `advancedKeywordList` 只做 **refinement**，必须是**可搜词**
- 不要把 `blogCateIds` / `regionList` 当作模型直出主字段
- 不要把下列内容当关键词塞进去：
  - sku / asin / 长串 product id
  - `products`
  - `shop`
  - `source`
  - `x27`
  - 截断短语
  - 页面导航词

### 5. 信息不足时追问，而不是乱猜
如果以下信息明显缺失，应该放入 `clarificationsNeeded`：
- 目标市场
- 平台偏好
- 明确的营销目标（曝光 / 转化 / 口碑）

如果商品本身是清楚的，但市场未知：
- 可以先给保守的 `searchPayloadHints`
- 同时把 `regions` 放进 `clarificationsNeeded`

---

## 输出要求

你必须输出 **标准 JSON**，结构遵循当前 skill 的模型分析 schema。

最低应包含：

```json
{
  "version": "1.0",
  "analysisMode": "model_plus_url",
  "inputType": "url",
  "source": {},
  "product": {},
  "marketing": {},
  "constraints": {},
  "searchPayloadHints": {},
  "confidence": {},
  "clarificationsNeeded": [],
  "notes": []
}
```

---

## 特别约束

### 1. `searchPayloadHints.platform`
- 如果页面本身是商品页，不代表一定要搜该平台达人
- 默认可优先 `tiktok`
- 如果商品明显更适合深度评测，也可把 `youtube` 放到 `marketing.platformPreference`

### 2. `blogCateIds`
- 不要求模型直接输出终态 `blogCateIds`
- 更重要的是把 `productType` / `productSubtype` / `categoryForms` / `functions` 说清楚
- 真正的 `blogCateIds` 应由脚本标准 mapping chain 产出

### 3. `advancedKeywordList`
请优先输出：
- 核心产品词
- 功能卖点词
- 内容场景词
- 它是关键词 refinement，不是主类目链的替代品

例如：
- `walkie talkie`
- `4g poc radio`
- `long range communication`
- `outdoor communication device`

### 4. `confidence`
请给字段级置信度，尤其是：
- `productType`
- `productSubtype`
- `categoryForms`
- `advancedKeywordList`
- `regions`
- `creatorTypes`
- `creatorIntent`

### 5. `notes`
如果页面信息不足、字段互相冲突、标题疑似截断，请明确写到 `notes` 里。

---

## 示例思路（不是模板）

若页面是对讲机商品：
- `product.productType`：communication device / walkie talkie
- `marketing.creatorTypes`：tech creator / outdoor creator / field-use gear creator
- `searchPayloadHints.advancedKeywordList`：
  - `walkie talkie`
  - `4g poc radio`
  - `long range radio`
  - `outdoor communication gear`

不要输出：
- `products`
- `shop`
- `x27`
- `1731831763391320673`

---

## 最终要求

你的输出必须：
- 是合法 JSON
- 结构稳定
- 可直接被脚本消费
- 符合原则：**模型理解，脚本执行**
- `productSubtype` / `creatorIntent` / `contentAngles` 用于增强语义稳定性与搜索聚焦度，**不能替代 category 匹配主路径**
