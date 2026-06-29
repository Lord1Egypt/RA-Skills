# 开发模式三件套模板

> 完整的 AI 能力清单（原子接口返回值、组件约束、API列表）见 `references/ai-capabilities.md`。
> 可直接填充的代码模板见 `templates/` 目录。

## 什么时候读取

用户要求开发模式落地、生成 `AGENTS.md`、业务 `SKILL.md`、`mcp.json`、原子接口示例、测试矩阵时，读取本文件。

## 输出原则

- 输出草案和结构，不声称是可直接通过审核的完整生产代码
- 用用户行业和业务对象替换模板中的占位词
- 接口名必须语义化，例如 `searchDrinks` 优于 `search`
- description 面向模型决策，不写内部实现细节
- ID 字段必须声明取值来源，不能让模型编造
- 行动类接口必须要求用户确认或校验前置状态
- content 用事实+动作两段式写法
- 失败/空结果包含三要素：事实+出口+禁令

## 三件套总览

| 文件 | 作用 | 限制 | 适合写什么 |
|---|---|---|---|
| `AGENTS.md` | 小程序整体说明 | ≤10000 字节 | 服务范围、Skill 分工、兜底策略、全局边界 |
| `SKILL.md` | 单个业务 Skill 说明 | ≤16000 字节 | 用户意图、业务流程、接口依赖、跨接口约束 |
| `mcp.json` | 原子接口声明 | ≤24000 字节（扣 outputSchema） | 接口名、description、inputSchema、字段约束 |

## 信息源分工（官方最佳实践）

写错位置会显著降低准确率：

| 信息源 | 注意力 | 写什么 |
|---|---|---|
| 原子接口返回的 content | ★★★★★ | 本次调用结果与下一步动作 |
| mcp.json 的 description | ★★★★ | 接口功能、调用时机、不适用场景 |
| mcp.json 的 inputSchema.description | ★★★★ | 参数语义、取值来源、缺省处理 |
| SKILL.md | ★★★ | 业务流程编排、跨接口规则、意图分流 |

## AGENTS.md 草案模板

```markdown
# {{行业}} AI 服务说明

本小程序为用户提供{{服务范围}}相关服务，包括{{核心服务1}}、{{核心服务2}}、{{核心服务3}}。

## Skill 分工

| Skill | 负责范围 | 不负责 |
|---|---|---|
| {{Skill名}} | {{搜索/推荐/下单/预约/查状态}} | {{退款/人工客服/超范围服务}} |

## 全局原则

1. 用户表达明确商品、服务、门店、时间或预算时，优先调用对应 Skill。
2. 用户只表达模糊需求时，先调用推荐类接口，不直接下单或预约。
3. 下单、预约、支付、提交手机号、提交地址前，必须让用户确认。
4. 核心交易流程优先在小程序 AI 内完成；文字链和页面元数据只做兜底。
5. 找不到结果时，说明具体原因，并给出替代商品、服务或时间。
```

## 业务 SKILL.md 草案模板

```markdown
# {{Skill名}}

## 服务范围

本 Skill 用于{{行业/业务对象}}的{{搜索、推荐、详情、规格、下单/预约、支付/状态查询}}。

## 用户意图入口

| 用户表达 | 应对流程 |
|---|---|
| 明确商品/服务，如"我要冰美式" | searchX → getXDetail → getSkuOptions |
| 模糊需求，如"想喝点清爽的" | recommendX |
| 下单/预约，如"帮我下单/预约" | 确认必要信息 → createXOrder/createBooking |
| 查状态，如"我的订单到哪了" | queryXStatus |

## 业务流程

用户意图 → 搜索/推荐 → 展示候选卡片 → 用户选择 → 补齐规格/门店/地址/时间
→ 创建订单或预约草稿 → 用户确认 → 支付或提交 → 返回状态

## 接口依赖

| 接口 | 前置条件 | 成功后下一步 |
|---|---|---|
| searchX | 用户有明确关键词 | 展示列表，等待用户选择 |
| recommendX | 用户只有场景/预算/偏好 | 展示推荐卡片 |
| getXDetail | 已有 xId | 展示详情或规格 |
| createXOrder | 已有 xId、sku、门店/地址 | 展示订单确认卡 |
| requestPayment | 用户确认订单 | 拉起支付 |

## 业务约束

1. 不要从用户自然语言编造业务 ID。
2. 没有库存、门店、地址、时间等必填信息时，不要创建订单。
3. 支付、预约、提交地址、提交手机号前必须用户确认。
4. 无结果时不要重复调用同一接口，应给替代路径。
```

## mcp.json 草案模板

```json
{
  "apis": [
    {
      "name": "recommendProducts",
      "description": "推荐商品。用户只表达场景、预算、偏好或模糊需求时调用，例如想喝点清爽的、找个适合通勤的。用户明确说出商品名称时，应优先调用 searchProducts。",
      "_meta": {
        "ui": { "componentPath": "components/product-card/index" }
      },
      "inputSchema": {
        "type": "object",
        "properties": {
          "scene": {
            "type": "string",
            "description": "用户表达的使用场景或需求，例如提神、下午茶、通勤、送礼。用户没有表达时不要填写。"
          },
          "budget": {
            "type": "number",
            "description": "用户明确提出的预算上限。用户未提预算时不要填写。"
          },
          "storeId": {
            "type": "string",
            "description": "门店唯一标识，取自上游门店选择、定位或用户当前上下文。不要从门店名称硬猜。"
          }
        }
      }
    },
    {
      "name": "searchProducts",
      "description": "搜索商品。用户明确说出商品名、别名、类目或规格时调用。用户只表达模糊需求时，不要调用本接口，应调用 recommendProducts。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "keyword": {
            "type": "string",
            "description": "商品关键词，例如冰美式、拿铁、奶茶。用户未说出具体商品或类目时不要填写。"
          },
          "category": {
            "type": "string",
            "description": "商品类目，例如咖啡、套餐、女鞋。仅在用户明确表达类目时填写。"
          }
        },
        "required": ["keyword"]
      }
    },
    {
      "name": "getProductDetail",
      "description": "查看商品详情。用户选择某个商品，或需要价格、规格、库存、适用门店等详情时调用。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "productId": {
            "type": "string",
            "description": "商品唯一标识，必须取自 searchProducts 或 recommendProducts 返回的 productId 原值。不要从商品名称推断。"
          }
        },
        "required": ["productId"]
      }
    },
    {
      "name": "createOrderDraft",
      "description": "创建订单草稿。仅在商品、规格、数量、门店或地址等必要信息已补齐后调用。调用成功后只展示订单确认卡，不代表用户已支付。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "productId": {
            "type": "string",
            "description": "商品唯一标识，取自上游接口返回。"
          },
          "sku": {
            "type": "object",
            "description": "用户已确认的规格信息，例如温度、冰量、糖度、尺码、颜色。缺少规格时应先询问用户。"
          },
          "quantity": {
            "type": "integer",
            "description": "购买数量。用户未说明时默认 1。"
          },
          "addressId": {
            "type": "string",
            "description": "收货地址标识，取自用户授权选择地址后的返回值。不要明文拼接地址。"
          }
        },
        "required": ["productId", "quantity"]
      }
    }
  ],
  "components": [
    {
      "path": "components/product-card/index",
      "relatedPage": "/pages/detail/detail"
    }
  ]
}
```

## index.js 草案模板

```javascript
const skill = wx.modelContext.createSkill('path/to/skill')

// 中间件：统一登录和错误监听
skill.use(async (ctx, next) => {
  const start = Date.now()
  try {
    await next()
    console.log(`[${ctx.name}] ${Date.now() - start}ms`)
  } catch (err) {
    console.error(`[${ctx.name}]`, err)
    throw err
  }
})

// 注册接口
const searchProducts = require('./apis/searchProducts')
const recommendProducts = require('./apis/recommendProducts')
const getProductDetail = require('./apis/getProductDetail')
const createOrderDraft = require('./apis/createOrderDraft')

skill.registerAPI('searchProducts', searchProducts)
skill.registerAPI('recommendProducts', recommendProducts)
skill.registerAPI('getProductDetail', getProductDetail)
skill.registerAPI('createOrderDraft', createOrderDraft)
```

## 原子接口实现示例

```javascript
async function searchProducts({ keyword, category, storeId }) {
  // 1. 参数校验
  if (!keyword) {
    return {
      isError: true,
      content: [{ type: 'text', text: '缺少搜索关键词，请告诉用户输入商品名称。' }]
    }
  }

  // 2. 请求后端
  const res = await wx.request({
    url: 'https://your-server.com/api/search',
    data: { keyword, category, storeId }
  })

  // 3. 空结果处理
  if (!res.data.items || res.data.items.length === 0) {
    return {
      isError: false,
      content: [
        { type: 'text', text: `未找到「${keyword}」相关商品。请引导用户换关键词或查看推荐商品。不要再以相同关键词重复调用本接口。` }
      ],
      structuredContent: { items: [] }
    }
  }

  // 4. 正常返回（事实+动作）
  return {
    isError: false,
    content: [
      { type: 'text', text: `已为您找到${res.data.items.length}款商品。请展示商品列表卡片供用户选择。` }
    ],
    structuredContent: { items: res.data.items }
  }
}

module.exports = searchProducts
```

## 代码生成模板

如果用户要求"直接给我完整项目代码"，读取 `templates/` 目录下的模板文件，按以下流程生成：

1. 从 `references/industry-cases.md` 匹配行业接口组合
2. 用语义化名称填充模板占位符
3. 生成 app.json、AGENTS.md、SKILL.md、mcp.json、index.js
4. 为每个接口生成 apis/ 下的骨架代码
5. 生成 components/ 卡片组件骨架
6. 生成 page-meta.json
7. 校验文件大小是否超限

## 测试矩阵模板

| 用户表达 | 期望意图 | 期望接口 | 必填参数 | 期望返回 | 失败兜底 | 风险点 |
|---|---|---|---|---|---|---|
| 想喝点清爽的 | 场景推荐 | recommendProducts | scene | 推荐卡片 | 返回热销商品 | 无 |
| 帮我点一杯冰美式少冰 | 下单前确认 | searchProducts → getProductDetail → createOrderDraft | keyword、productId、sku | 订单确认卡 | 缺地址时引导选择地址 | 地址、支付 |
| 这个还有 M 码吗 | 库存查询 | getProductDetail/checkInventory | productId、sku | 库存状态 | 推荐相近尺码 | 无 |

## 交付格式

当用户要求完整方案时，按这个顺序输出：

1. 接入模式结论
2. 用户路径
3. 业务能力拆解
4. 开发模式三件套草案（AGENTS.md + SKILL.md + mcp.json）
5. index.js 接口注册
6. apis/ 接口骨架代码
7. components/ 卡片组件骨架
8. page-meta.json
9. GEO 数据补全表
10. 自动模式兜底
11. 测试矩阵
12. 上线检查
