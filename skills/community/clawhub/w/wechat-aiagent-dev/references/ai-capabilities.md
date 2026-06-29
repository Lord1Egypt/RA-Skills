# 微信小程序 AI 开发模式 · 能力清单

> 基于微信官方开放文档整理（2026年6月），当前为 beta 内测阶段。
> 官方文档入口：微信开放文档 → 开发 → AI 能力

## 什么时候读取

用户问"微信AI有哪些能力"、"原子接口能做什么"、"原子组件有什么限制"、"知识库怎么用"、"文字链怎么配"、"小程序和AI怎么交互"、"最佳实践怎么写"时，读取本文件。

---

## 一、核心概念

### 1. 小程序 AI

小程序 AI 是微信内的自然语言服务入口。用户用一句话表达需求，AI 理解意图后，通过小程序 MCP 协议调用开发者在 SKILL 中声明的原子接口和原子组件，完成数据处理和任务执行，最终整合结果返回给用户。

给商家的解释：

> 以前用户要先想起你的小程序、打开页面、自己找商品。现在用户只说一句"帮我点杯冰美式"，AI 就判断应该调用哪个小程序、哪个商品、哪个下单流程。

### 2. 小程序 MCP

小程序 MCP 是向小程序 AI 暴露可调用能力的一套协议。与标准 MCP 不同，小程序 MCP 适应于小程序开发的特点，开发者只需要按设计提供完整的 SKILL 实现，小程序 AI 就能正确地推理及执行相应的原子接口。

### 3. 原子接口

此模式的最小执行单元，封装单一的业务功能，具有标准化输入参数和输出结构，运行在微信客户端的独立 JS 环境中。

### 4. 原子组件

原子接口的可视化展示单元，将原子接口返回的结构化数据渲染为 GUI 卡片，展示在对话流中。

### 5. SKILL

完成特定场景任务的完整能力封装。一个小程序可封装多个 SKILLs，每个 SKILL 包含：业务说明（SKILL.md）、模型可调用能力的声明（mcp.json）、原子接口与原子组件的实现。

关键限制：

- 一个小程序最多声明 30 个 SKILL
- SKILL 必须封装在独立分包里
- 需要全局开启按需注入 `lazyCodeLoading: "requiredComponents"`
- 一个独立分包可以放置多个 SKILLs

### 6. 当前状态

- 处于内测 beta 阶段
- 暂未开放代码提审，提审时间另行通知
- 请勿将此模式相关代码合入正式版本提交审核
- 申请入口：微信公众平台 → 基础功能 → AI能力，或小程序「微信开发者助手」→ 管理 → 微信AI管理

---

## 二、SKILL 封装结构

### 目录结构

```
|-- path/to/pkg/weather-skill
|   |-- SKILL.md          # SKILL 的详细说明
|   |-- mcp.json           # 原子接口声明
|   |-- index.js           # 注册原子接口
|   |-- components/        # 原子组件代码
|   |-- apis/              # 原子接口代码
```

### 文件限制

| 文件 | 必填 | 说明 | 大小限制 |
|------|------|------|----------|
| SKILL.md | 是 | SKILL 的详细说明，只支持单文件，不支持引用其他 md 文件 | 16000 字节 |
| index.js | 是 | 注册当前 SKILL 所涉及的所有原子接口 | — |
| mcp.json | 是 | 原子接口声明（当前 SKILL 所涉及的所有接口） | 24000 字节（扣除 outputSchema 和空格换行后） |
| components/ | 否 | 原子组件代码实现目录，仅建议 | — |
| apis/ | 否 | 原子接口代码实现目录，仅建议 | — |

### app.json 声明

```json
{
  "lazyCodeLoading": "requiredComponents",
  "subPackages": [
    {
      "root": "path/to/pkg",
      "independent": true,
      "pages": []
    }
  ],
  "agent": {
    "skills": [
      {
        "name": "weather",
        "description": "查询天气业务",
        "path": "path/to/pkg/weather-skill"
      },
      {
        "name": "shopping",
        "description": "购物业务",
        "path": "path/to/pkg/shopping-skill"
      }
    ],
    "instruction": "path/to/AGENTS.md"
  }
}
```

agent.skills 字段说明：

| 字段 | 必填 | 说明 |
|------|------|------|
| name | 是 | 名称 |
| description | 是 | SKILL 简要说明 |
| path | 是 | SKILL 分包路径（绝对路径） |

### 全局提示词（AGENTS.md）

全局提示词用来整体说明服务范围、背景知识、行为逻辑和回答风格，引导 AI 生成"猜你想问"的内容。多个 SKILLs 的关联关系和分工也在这里说明。

- 文件名通常为 `AGENTS.md`
- 在 app.json 的 `agent.instruction` 字段指定路径
- 目前非必填
- 最大 10000 字节

---

## 三、原子接口能力

### mcp.json 声明格式

```json
{
  "apis": [
    {
      "name": "getWeather",
      "description": "查询当前位置或某地的未来一段时间的天气",
      "_meta": {
        "ui": {
          "componentPath": "path/to/comp"
        }
      },
      "inputSchema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "要查询天气的地点，如城市名、行政区名或经纬度。不传则默认取当前位置"
          },
          "days": {
            "type": "number",
            "description": "预报天数，范围1-15，默认7"
          }
        },
        "required": ["days"]
      },
      "outputSchema": {}
    }
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

### 多模态支持

小程序 AI 输入框支持多模态上传，用户可以发送图片/文件。在 inputSchema 中定义字段时填写 `"format": "image"` 或 `"format": "file"`，AI 会将接收到的图片/文件传给对应字段。

```json
{
  "name": "EditPhoto",
  "description": "帮用户 P 图",
  "inputSchema": {
    "type": "object",
    "properties": {
      "imagePath": {
        "type": "string",
        "description": "本地图片路径",
        "format": "image"
      },
      "query": { "type": "string", "description": "用户的 P 图需求" }
    },
    "required": ["imagePath", "query"]
  }
}
```

### 原子接口返回值

| 属性 | 类型 | 必填 | 说明 |
|------|------|------|------|
| isError | boolean | 否，默认 false | 为 true 时不渲染卡片，structuredContent 被忽略 |
| content | ContentBlock[] | 是 | 返回给 LLM 的文本内容，不超过 200KB |
| structuredContent | object | 否 | 返回给 LLM 的结构化数据，不超过 200KB |
| _meta | object | 否 | 对 LLM 不可见，携带元数据传给原子组件，不超过 200KB |

- `isError`、`structuredContent`、`content` 会作为 LLM 上下文
- `_meta` 对 LLM 不可见，用于携带私有数据传递给原子组件
- `ContentBlock[]` 目前只支持 `TextContent`：`{ type: "text", text: string }`
- `isError: false` 且有绑定原子组件时，AI 倾向渲染 GUI 卡片
- `isError: true` 时，content 常用于异常流程引导

接口实现示例：

```javascript
async function getWeather({ location, days }) {
  // 内部可通过 wx.request 请求服务器
  // 也可通过 wx.cloud.callFunction 调用云函数
  return {
    isError: false,
    content: [{ type: "text", text: "已为您查询到北京未来3天天气" }],
    structuredContent: {
      location: "北京",
      forecasts: [
        { date: "2026-04-23", dayWeather: "晴", tempHigh: 28, tempLow: 14 }
      ]
    }
  }
}
```

### 接口注册

```javascript
const getWeather = require('./apis/getWeather')

const skill = wx.modelContext.createSkill('/path/to/pkg/weather-skill')
skill.registerAPI('getWeather', getWeather)
```

### 中间件机制

用于统一登录态、统一上报和错误监听等场景。

```javascript
const skill = wx.modelContext.createSkill('pages/weather')
skill.use(async (ctx, next) => {
  // 前置逻辑（如统一登录）
  const start = Date.now()
  try {
    await next()  // 执行实际 handler
    // 后置逻辑（如成功上报）
  } catch (err) {
    // 错误监听
  }
})
```

核心语义：

- 每次原子接口调用都会执行中间件
- `next()` 前是前置逻辑，`next()` 后是后置逻辑
- 整个中间件链与原子接口执行时间共享超时上限（当前为 300 秒）
- 支持多个中间件，按注册顺序形成链

### 关键 API

| API | 用途 |
|-----|------|
| wx.modelContext.createSkill(skillPath) | 创建 skill，参数与 app.json 的 agent.skills[].path 一致 |
| skill.use(Middleware) | 注册中间件 |
| skill.registerAPI(name, handler) | 注册原子接口 |
| wx.login | 获取用户登录凭证 |
| wx.getPhoneNumber | 获取手机号 |
| wx.request | 发起网络请求 |
| wx.cloud.callFunction | 调用云函数 |

---

## 四、原子组件能力

### 组件定义

原子组件用于承接原子接口返回的结构化数据的展示。编码上与小程序自定义组件一致，但不可声明为虚拟组件。

```javascript
Component({
  lifetimes: {
    created() {
      const modelCtx = wx.modelContext.getContext(this)
      const { NotificationType } = wx.modelContext
      modelCtx.on(NotificationType.Input, (data) => {
        // 原子接口的入参数据
      })
      modelCtx.on(NotificationType.Result, (data) => {
        // 原子接口的出参数据
      })

      const viewCtx = wx.modelContext.getViewContext(this)
      const { minHeight, maxHeight, width } = viewCtx.getDimensions()
      viewCtx.on(NotificationType.Overflow, (data) => {
        // 内容溢出事件
      })
    }
  }
})
```

### 尺寸约束

- 宽度随屏幕宽度变化
- 最小高度：宽高比 4:1
- 最大高度：宽高比 1:1
- 不超出最小最大高度时，随内容自动撑高
- 初始化时决定卡片高度，后续不可再改变

### 交互限制

- 仅支持 tap 点击、Image load、Image error 事件
- 不支持其他交互事件
- 默认不支持网络请求和云开发接口（需声明为「实时动态组件」）
- 默认不支持定时器（setTimeout、setInterval）
- 不支持打开小程序接口
- 不支持动画
- 禁止上下滚动（禁止 overflow-y）
- 支持点击后上行一条文本消息（ModelContext.sendFollowUpMessage）
- 支持点击后打开半屏页面

### 实时动态组件

需要展示实时动态内容的场景，可在 mcp.json 声明 `scope.dynamic` 权限。此能力需要单独审核，非必要场景不建议使用。

```json
{
  "components": [
    {
      "path": "path/to/comp",
      "permissions": {
        "scope.dynamic": {
          "desc": "声明使用场景"
        }
      }
    }
  ]
}
```

### 关联小程序页面（必填）

原子组件渲染的 GUI 卡片上方有标题栏，右上方提供进入小程序的入口，必须配置关联的小程序页面。场景值为 1442 或 1443。

在 mcp.json 声明：

```json
{
  "components": [
    {
      "path": "path/to/comp",
      "relatedPage": "/path/to/related-page"
    }
  ]
}
```

在组件中动态设置 query 参数：

```javascript
const viewCtx = wx.modelContext.getViewContext(this)
viewCtx.setRelatedPage({ query: `orderId=${orderId}` })
// 也可指定不同页面
viewCtx.setRelatedPage({ path: '', query: `orderId=${orderId}` })
```

### 组件过期态

支持将已渲染的原子组件置为过期态，防止用户再次点击。

mcp.json 声明：

```json
{
  "components": [
    {
      "path": "components/ride-card/index",
      "expirable": true,
      "expiredText": "店铺已关闭"
    }
  ]
}
```

两种过期 API：

1. `wx.modelContext.expireAllCards()` — 可在原子接口/组件调用，过期所有声明了 expirable 的组件
   - 支持按 componentPath 过滤
   - 支持 `match: 'latest'` 只过期最近一张

2. `viewCtx.expirePreviousCards()` — 只能在原子组件调用，过期之前渲染过的组件

### 半屏原子组件（collapsible-view）

列表场景下可使用半屏原子组件，展示更多内容。

```html
<collapsible-view>
  <view slot="button">展开</view>
</collapsible-view>
```

最佳实践：把每一项作为 collapsible-view 的直接子节点，避免嵌套结构。

---

## 五、半屏页面

半屏页面是原子组件内容的延伸，非必要流程。只有需要展示更多详情信息或用户补充信息时才使用。

### 打开半屏页面

在原子组件内（原子接口内不可调用）：

```javascript
const viewCtx = wx.modelContext.getViewContext(this)
viewCtx.openDetailPage({
  url: '/packageA/pages/weather-detail?foo=bar'
})
```

### 从半屏页面上行消息

```javascript
const ctx = wx.modelContext.getContext()
ctx.sendFollowUpMessage({
  content: [
    { type: 'text', text: '选择拿铁' },
    { type: 'api/call', data: { name: 'selectGoods', arguments: {} } }
  ]
})
```

- 必须以用户第一人称角度发送
- `type: 'api/call'` 可指定下一步调用的原子接口，不传则由模型推理

### 半屏页面预加载

```javascript
viewCtx.preloadDetailPage({
  url: '/packageA/pages/weather-detail?foo=bar'
})
```

### 从半屏页面返回并更新卡片

```javascript
const modelCtx = wx.modelContext.getContext()
modelCtx.reapplyApiCall({
  arguments: { city: '广州', days: 3 }
})
```

### 半屏页面约束

- 执行环境与小程序页面一致，但部分接口受限
- 不允许任何跳转（跳出半屏的接口、页面路由、广告接口组件）
- 场景值 1433 或 1434

---

## 六、知识库

小程序 AI 开发模式下，添加知识库后，模型可根据情况选择检索知识库内容作为回答依据。适合专业领域问答、企业智能助手等场景。

### 文件要求

- 格式：PDF、DOC、DOCX、PPT、PPTX、TXT、MD、XLSX
- 单文件上限：10MB
- 文件总数上限：10 个
- 上传入口：微信公众平台 → 基础功能 → AI能力 → 知识库

### 调用逻辑

1. 用户输入问题，模型分析意图
2. 模型尝试根据语义匹配 SKILL
3. 如果与所有 SKILL 都不匹配，才会调用知识库
4. 拿到结果后组织语言回复

注意：

- 模型自主决策调用时机，建议优化 SKILL 描述让模型更容易判断
- 可在 AGENTS.md 或 SKILL.md 中引导倾向调用知识库
- 如果所有 SKILL 都不匹配，知识库兜底

### 测试

- 开发版/体验版可测完整效果（SKILL + 知识库）
- 公众平台调试器可快速验证文件召回（简易效果，无上下文）
- 文件解析完成后即可测试，不需要等审核通过

### 发布

- 文件审核通过且召回效果符合预期后点击「发布」
- 文件状态变为「已发布」即生效
- 内测阶段知识库效果仅在开发版和体验版开放体验

---

## 七、文字链拉起小程序

小程序 AI 可在回复中带上小程序短链，供用户点击打开小程序页面。

### 实现方式

在 app.json 声明 pageMetadata：

```json
{
  "agent": {
    "skills": [],
    "pageMetadata": "path/to/page-meta.json"
  }
}
```

page-meta.json 格式（最大 8000 字节）：

```json
{
  "pages": [
    {
      "path": "pages/home/home",
      "name": "首页",
      "description": "展示最新的内容和推荐"
    },
    {
      "path": "pages/detail/detail",
      "name": "商品详情",
      "description": "展示特定商品的信息",
      "query": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "description": "商品的唯一标识符" }
        },
        "required": ["id"]
      }
    }
  ]
}
```

| 字段 | 必填 | 功能 |
|------|------|------|
| path | 是 | 页面路径，可带固定 query |
| name | 是 | 页面标题 |
| description | 是 | 页面的功能描述 |
| query | 否 | 页面 query，标准 JSON-Schema 格式 |

重要提醒：

- 文字链是**兜底策略**，核心流程不应依赖
- 核心功能使用文字链可能影响审核或触发召回降权
- 场景值 1435 或 1436

---

## 八、小程序与 AI 交互

### 打开 AI 界面

```javascript
wx.openAgent({
  followUpMessage: '帮我看下今天的订单',
  context: '当前在订单管理页面'
})
```

也可通过胶囊入口打开，触发回调：

```javascript
wx.onAgentOpen(callback)
// callback 返回 { followUpMessage, context }
wx.offAgentOpen(callback)
```

兼容性检查：

```javascript
wx.checkIsSupportAgent({
  success(res) {
    if (res.isSupport) wx.openAgent()
  }
})
```

### 返回 AI 界面

从文字链或卡片入口进入小程序后，可返回 AI 界面并携带数据：

```javascript
wx.navigateBackAgent({
  followUpMessage: {
    content: [
      { type: 'text', text: '选择拿铁' },
      { type: 'api/call', data: { name: 'selectGoods', arguments: {} } }
    ]
  },
  context: ''
})
```

### 场景值表

| 场景值 | 含义 |
|--------|------|
| 1433 | 半屏页面打开小程序页面 |
| 1434 | 半屏页面打开小程序页面（另一入口） |
| 1435 | 文字链拉起小程序 |
| 1436 | 文字链拉起小程序（另一入口） |
| 1442 | 卡片标题栏入口进入小程序 |
| 1443 | 卡片标题栏入口进入小程序（另一入口） |

---

## 九、最佳实践规范

### 信息源注意力权重

AI 在决策时综合多个信息源，写在错误的位置会显著降低准确率。

| 信息源 | 注意力 | 写什么 |
|--------|--------|--------|
| 原子接口返回的 content | ★★★★★ | 本次调用结果与下一步动作 |
| mcp.json 的 description | ★★★★ | 接口本身的功能、调用时机、不适用场景 |
| mcp.json 的 inputSchema.description | ★★★★ | 参数语义、取值来源、缺省处理 |
| SKILL.md | ★★★ | 业务流程编排、跨接口规则、意图分流、通用规范 |

### 常见错位

- 把"接口功能"写到 SKILL.md → 应写在 mcp.json 的 description
- 把"跨多接口规则"写到单个接口的 description → 应写在 SKILL.md
- 把"接口功能描述"写到 content → content 只承载本次结果与下一步动作

### 通用写作原则

1. 同一约束在一处书写，避免重复不一致
2. 硬约束放在权重更高的位置
3. 给出可执行出口，每条禁令都配一个替代动作

### 接口 description 写法

- 接口名语义化：`searchDrinks` 优于 `search`
- 首句声明业务对象，而非入参
- 不写内部实现细节
- 职责单一，描述互不重叠
- 同名字段统一命名（如 drinkId 不要混用 itemId）

反例：`"按关键词、温度、杯型搜索商品列表（仅饮品）……"`

推荐：`"搜索饮品。按关键词、温度、杯型检索……"`

### 字段 description 写法

普通字段：多举例 + 缺省处理

```json
// 反例
"keyword": { "description": "饮品关键词，如『拿铁』" }

// 推荐
"keyword": {
  "description": "饮品关键词，例如『拿铁』『美式』『奶茶』。用户未说出具体饮品时，不要填写本字段，应改走饮品推荐接口。"
}
```

ID 类字段：声明取值来源

```json
// 反例
"drinkId": { "description": "饮品 ID" }

// 推荐
"drinkId": {
  "description": "饮品唯一标识，取自上游接口 searchDrinks 或 getRecommendedDrinks 返回的 drinkId 原值。不要从用户自然语言推断，也不要使用示例值。上下文无可用 drinkId 时，应先调 searchDrinks。"
}
```

### content 写法：事实 + 动作两段式

```javascript
// 反例：仅给动作
{ type: "text", text: "接下来请务必为用户展示订单确认卡片。" }

// 推荐：事实 + 动作
{ type: "text", text: "已根据所选规格生成订单。请展示订单确认卡片，并用一句话引导用户核对后下单。" }
```

### 失败/空结果三要素

失败时 content 应包含三件事：

1. 陈述具体事实（问题原因）
2. 给出下一步出口（接下来应该做什么）
3. 指出不应做的动作（如禁止重复调用）

示例：

```
未匹配到「圣诞限定款」，已附带「本店热销饮品」兜底数据。
请先告诉用户"未找到「圣诞限定款」"，并引导用户在以下本店热销饮品中挑选。
不要再以相同关键词重复调用本接口。
```

### 上行消息文案规范

| 原则 | 说明 |
|------|------|
| 用户视角出发 | 以用户口吻表达，可使用第一人称 |
| 不可上行系统消息 | 异常系统消息需转换成用户操作 |
| 自然语言表达 | 摒弃字段罗列、编码等技术性描述 |
| 使用生活化语言 | 优先口语，规避专业术语 |
| 仅限已明确表达的信息 | 不擅自补充用户未说明的偏好 |
| 描述当前操作 | 不描述其他环节或提前预判 |
| 信息充分但不过载 | 只保留推动对话的必备信息 |
| 简洁但不歧义 | 多选择场景不用"这个""那个" |
| 处理敏感信息 | 身份证号、手机号禁止明文展示 |

---

## 十、运行环境

### 脚本执行环境

- 由 JavaScriptCore / V8 引擎创建的独立环境
- 原子接口、原子组件、实时动态组件分别在不同执行上下文中运行
- 不同的 JavaScript 执行上下文不共享全局变量
- 半屏页面运行环境与小程序一致，但部分接口受限

### 渲染环境

- 原子组件使用微信小程序团队自研的卡片渲染引擎
- 组件框架采用 glass-easel 框架
- 编码上与小程序自定义组件一致
- WXSS 样式集与 WebView / Skyline 引擎有所差异

### 生命周期

- 用户与 AI 开始对话时起新会话
- 聊天记录对用户与 AI 可见，直到客户端运行时结束
- 客户端运行时结束的情况：
  - AI 退至后台 30 分钟后
  - 系统内存告警时微信可能清理运行时
  - 用户重新启动 AI

### 调试

- 需下载微信开发者工具（Nightly Electron Build 最新版本）
- demo 代码的 appid 需改成已申请开发模式的 appid
