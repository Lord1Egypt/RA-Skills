# 代码生成模板

## 什么时候读取

用户要求"帮我生成代码"、"给我完整项目"、"直接给我三件套代码"、"生成 mcp.json"、"生成 index.js"时，读取本文件。

## 生成流程

1. 根据 `references/industry-cases.md` 匹配行业接口组合
2. 用语义化名称替换模板占位符（`{{行业对象}}`、`{{接口名}}`等）
3. 填充 description（遵循 `references/ai-capabilities.md` 最佳实践写法）
4. 填充 inputSchema（ID字段声明来源、普通字段多举例+缺省处理）
5. 生成 index.js 注册代码
6. 生成 apis/ 下每个接口的骨架代码
7. 生成 components/ 卡片组件骨架
8. 生成 page-meta.json
9. 校验：mcp.json ≤ 24KB、SKILL.md ≤ 16KB、AGENTS.md ≤ 10KB

## 占位符说明

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{{SKILL_NAME}}` | SKILL名称（英文） | drink-ordering |
| `{{SKILL_DESCRIPTION}}` | SKILL简要说明 | 奶茶点单业务 |
| `{{SKILL_PATH}}` | SKILL分包路径 | pages/drink-skill |
| `{{INDUSTRY}}` | 行业名 | 奶茶店 |
| `{{SERVICE_SCOPE}}` | 服务范围 | 饮品搜索、推荐、下单、支付 |
| `{{APIS_JSON}}` | mcp.json的apis数组 | 接口声明JSON |
| `{{COMPONENTS_JSON}}` | mcp.json的components数组 | 组件声明JSON |

---

## 模板1：app.json

```json
{
  "lazyCodeLoading": "requiredComponents",
  "subPackages": [
    {
      "root": "{{SKILL_PATH}}",
      "independent": true,
      "pages": []
    }
  ],
  "agent": {
    "skills": [
      {
        "name": "{{SKILL_NAME}}",
        "description": "{{SKILL_DESCRIPTION}}",
        "path": "{{SKILL_PATH}}/{{SKILL_NAME}}"
      }
    ],
    "instruction": "AGENTS.md"
  }
}
```

---

## 模板2：AGENTS.md

```markdown
# {{INDUSTRY}} AI 服务说明

本小程序为用户提供{{SERVICE_SCOPE}}相关服务。

## Skill 分工

| Skill | 负责范围 | 不负责 |
|-------|---------|--------|
| {{SKILL_NAME}} | {{SERVICE_SCOPE}} | 退款/人工客服/超范围服务 |

## 全局原则

1. 用户表达明确商品、服务、门店、时间或预算时，优先调用对应 Skill。
2. 用户只表达模糊需求时，先调用推荐类接口，不直接下单或预约。
3. 下单、预约、支付、提交手机号、提交地址前，必须让用户确认。
4. 核心交易流程优先在小程序 AI 内完成；文字链和页面元数据只做兜底。
5. 找不到结果时，说明具体原因，并给出替代商品、服务或时间。
```

---

## 模板3：SKILL.md

```markdown
# {{SKILL_NAME}}

## 服务范围

本 Skill 用于{{INDUSTRY}}的{{SERVICE_SCOPE}}。

## 用户意图入口

| 用户表达 | 应对流程 |
|---------|---------|
| 明确商品/服务 | searchX → getXDetail → getSkuOptions |
| 模糊需求 | recommendX |
| 下单/预约 | 确认必要信息 → createXOrder |
| 查状态 | queryXStatus |

## 业务流程

用户意图 → 搜索/推荐 → 展示候选卡片 → 用户选择 → 补齐规格/门店/地址/时间
→ 创建订单或预约草稿 → 用户确认 → 支付或提交 → 返回状态

## 接口依赖

| 接口 | 前置条件 | 成功后下一步 |
|------|---------|------------|
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

---

## 模板4：mcp.json

```json
{
  "apis": [
    {{APIS_JSON}}
  ],
  "components": [
    {{COMPONENTS_JSON}}
  ]
}
```

mcp.json 属性说明：

| 属性 | 必填 | 说明 |
|------|------|------|
| name | 是 | 标识符，跟 index.js 中导出的原子接口函数名一致 |
| description | 是 | 原子接口的功能描述 |
| inputSchema | 是 | 原子接口的入参，需为对象格式，遵循 JSON Schema |
| outputSchema | 建议填 | 原子接口返回的 structuredContent 对应的 schema |
| _meta | 否 | 可指定渲染的原子组件，componentPath 相对于 SKILL 目录 |

---

## 模板5：index.js

```javascript
// {{SKILL_NAME}} - 原子接口注册
const skill = wx.modelContext.createSkill('{{SKILL_PATH}}/{{SKILL_NAME}}')

// === 中间件：统一登录态和错误监听 ===
skill.use(async (ctx, next) => {
  const start = Date.now()
  try {
    const token = wx.getStorageSync('token')
    if (!token) {
      const { code } = await wx.login()
      const res = await wx.request({
        url: 'https://your-server.com/login',
        data: { code }
      })
      wx.setStorageSync('token', res.data.token)
    }
    await next()
    console.log(`[{{SKILL_NAME}}] ${ctx.name} 耗时 ${Date.now() - start}ms`)
  } catch (err) {
    console.error(`[{{SKILL_NAME}}] ${ctx.name} 错误:`, err)
    throw err
  }
})

// === 注册原子接口 ===
// 以下接口按实际业务需求增减，name 必须与 mcp.json 中的 name 一致
// const searchDrinks = require('./apis/searchDrinks')
// skill.registerAPI('searchDrinks', searchDrinks)
```

---

## 模板6：单个接口骨架（apis/xxx.js）

```javascript
// {{API_NAME}} - {{API_DESCRIPTION}}
// 返回值结构：{ isError, content, structuredContent, _meta }
// - isError: false 时渲染卡片，true 时忽略 structuredContent
// - content: 返回给 LLM 的文本（事实+动作两段式）
// - structuredContent: 结构化数据传给原子组件渲染
// - _meta: 对 LLM 不可见，传给组件的私有数据

async function {{API_NAME}}({{API_PARAMS}}) {
  // 1. 参数校验（LLM 生成的参数不保证正确）
  // 2. 业务逻辑（wx.request 或 wx.cloud.callFunction）
  // 3. 返回结果（事实+动作两段式）
  return {
    isError: false,
    content: [
      { type: 'text', text: '已为您找到3款饮品。请展示饮品列表卡片供用户选择。' }
    ],
    structuredContent: {
      items: [
        { id: 'x001', name: '冰美式', price: 12, tags: ['低糖', '提神'] }
      ]
    }
  }

  // 4. 错误处理（三要素：事实+出口+禁令）
  // return {
  //   isError: true,
  //   content: [{ type: 'text', text: '未找到相关结果，可换关键词重试。' }]
  // }
}

module.exports = {{API_NAME}}
```

---

## 模板7：卡片组件骨架（components/xxx.js）

```javascript
// {{COMPONENT_NAME}} - 原子组件
// 注意：尺寸宽高比4:1到1:1，初始化后不可改
// 仅支持tap事件，不支持动画和滚动

Component({
  data: {
    items: [],
    loading: true
  },

  lifetimes: {
    created() {
      const modelCtx = wx.modelContext.getContext(this)
      const { NotificationType } = wx.modelContext
      const viewCtx = wx.modelContext.getViewContext(this)

      // 监听原子接口返回结果
      modelCtx.on(NotificationType.Result, (data) => {
        const result = data.result
        if (result.isError) {
          this.setData({ loading: false, error: true })
          return
        }
        this.setData({
          items: result.structuredContent.items || [],
          loading: false
        })
        // 设置关联页面 query（必填）
        viewCtx.setRelatedPage({ query: `from=agent` })
      })
    }
  },

  methods: {
    // 点击项目，上行消息让 AI 继续处理
    onTapItem(e) {
      const item = e.currentTarget.dataset.item
      const ctx = wx.modelContext.getContext(this)
      ctx.sendFollowUpMessage({
        content: [
          { type: 'text', text: `选择${item.name}` },
          { type: 'api/call', data: { name: '{{NEXT_API_NAME}}', arguments: { id: item.id } } }
        ]
      })
    },

    // 打开半屏页面查看详情
    onTapDetail(e) {
      const item = e.currentTarget.dataset.item
      const viewCtx = wx.modelContext.getViewContext(this)
      viewCtx.openDetailPage({ url: `/pages/detail/index?id=${item.id}` })
    }
  }
})
```

---

## 模板8：page-meta.json

```json
{
  "pages": [
    {
      "path": "pages/home/home",
      "name": "首页",
      "description": "展示推荐商品、门店入口和活动"
    },
    {
      "path": "pages/detail/detail",
      "name": "商品详情",
      "description": "展示特定商品的价格、规格、库存和购买入口",
      "query": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "description": "商品的唯一标识符" }
        },
        "required": ["id"]
      }
    },
    {
      "path": "pages/store/store",
      "name": "门店详情",
      "description": "展示门店地址、营业时间、服务能力",
      "query": {
        "type": "object",
        "properties": {
          "storeId": { "type": "string", "description": "门店唯一标识符" }
        },
        "required": ["storeId"]
      }
    },
    {
      "path": "pages/order/order",
      "name": "订单详情",
      "description": "展示订单状态、支付和售后入口",
      "query": {
        "type": "object",
        "properties": {
          "orderId": { "type": "string", "description": "订单唯一标识符" }
        },
        "required": ["orderId"]
      }
    }
  ]
}
```
