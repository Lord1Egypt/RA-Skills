# 微信官方 Demo 逐文件解读

> 基于微信官方 ai-mode-demo（WeStoreCafe 点单场景）的结构拆解。
> 每个文件的"干什么"、"为什么这么写"、"你改哪里"都说清楚。
> 当前为 beta 内测，代码提审暂未开放。

## 什么时候读取

用户问"官方 demo 怎么跑起来的"、"demo 里每个文件干什么"、"我能不能照着 demo 改"、"WeStoreCafe 的代码结构是什么"、"我的小程序照着官方 demo 改需要注意什么"时，读取本文件。

---

## 一、Demo 全景：从用户一句话到订单完成

```
用户说"帮我点一杯冰美式"
  │
  ├─ 1. AGENTS.md ──→ 告诉 AI："我是 WeStoreCafe，专门做饮品"
  ├─ 2. app.json  ──→ 告诉框架："有个 drink-skill 分包，去加载"
  │
  ├─ 3. SKILL.md ──→ 告诉 AI："遇到点单需求，先搜饮品→选规格→选地址→确认下单→支付→查状态"
  ├─ 4. mcp.json ──→ 告诉 AI："可调用的接口有 searchDrinks / getDrinkDetail / chooseSku / chooseAddress / createOrder / requestPayment / queryOrderStatus，参数长这样"
  │
  ├─ 5. index.js ──→ 注册中间件（登录态）+ 注册 7 个接口
  ├─ 6. apis/*.js ──→ 每个接口的真实逻辑（调后端 / 云函数）
  │
  ├─ 7. components/*.js ──→ 接口返回数据渲染成 GUI 卡片（饮品列表卡、订单确认卡、支付状态卡）
  └─ 8. page-meta.json ──→ 兜底：如果 AI 要给文字链，链到哪里
```

---

## 二、逐文件拆解

### 1. app.json —— 小程序级声明

**干什么**：告诉微信框架这个小程序有哪些 Skill、在哪个分包、要开启按需注入。

```json
{
  "lazyCodeLoading": "requiredComponents",
  "subPackages": [
    {
      "root": "pages/drink-skill",
      "independent": true,
      "pages": []
    }
  ],
  "agent": {
    "skills": [
      {
        "name": "drink-ordering",
        "description": "WeStoreCafe 饮品点单服务",
        "path": "pages/drink-skill/drink-ordering"
      }
    ],
    "instruction": "AGENTS.md"
  }
}
```

**逐行解释**：

| 配置项 | 为什么这么写 | 你改什么 |
|--------|------------|---------|
| `lazyCodeLoading: "requiredComponents"` | 必须开启按需注入，否则 Skill 分包不会被正确加载。**这是硬性要求，不能改。** | 不改 |
| `subPackages[0].root` | demo 把一个 Skill 放在一个独立分包里。 | 改成你的分包路径，如 `pages/order-skill` |
| `subPackages[0].independent: true` | 独立分包不依赖主包，加载更快。 | 如果你的 Skill 需要主包资源，可设 false |
| `agent.skills[0].name` | Skill 名称，和 SKILL.md 所在目录名保持一致。 | 改成你的业务名，如 `food-ordering`、`booking-service` |
| `agent.skills[0].description` | 一句话描述，AI 用于判断是否匹配用户意图。 | 写你的业务一句话 |
| `agent.skills[0].path` | 这个路径下必须有 `SKILL.md` 文件。 | 改成 `分包路径/Skill名称` |
| `agent.instruction` | 指向根目录的 AGENTS.md。 | 不改路径，只改文件内容 |

**关键限制**：一个小程序最多 30 个 Skill。先做一个最核心的，跑通了再加。

---

### 2. AGENTS.md —— 全局提示词

**干什么**：告诉 AI 这个小程序的整体服务范围、有哪些 Skill、各 Skill 分工边界。AI 在每次对话开始都会读取。

```markdown
# WeStoreCafe AI 服务说明

本小程序为用户提供饮品搜索、推荐、定制、下单、支付、配送和订单查询服务。

## Skill 分工

| Skill | 负责范围 | 不负责 |
|-------|---------|--------|
| drink-ordering | 饮品搜索、推荐、定制规格、下单、支付、配送、查状态 | 退款争议、人工客服、非饮品商品 |

## 全局原则

1. 用户表达明确商品、门店、预算时，优先调用对应 Skill。
2. 用户只表达模糊需求（如"想喝点清爽的"），先调用推荐类接口，不直接下单。
3. 下单、支付、提交地址前，必须让用户确认。
4. 核心交易流程优先在 AI 内完成；文字链和页面元数据只做兜底。
5. 找不到结果时，说明具体原因，并给出替代饮品或门店。
```

**为什么这么写**：

- **服务范围**写在最前面：AI 先判断"这事归不归我管"，不归就拒掉或不匹配。
- **Skill 分工表**是核心：每个 Skill 明确负责什么、不负责什么。AI 根据用户意图路由到正确的 Skill。
- **全局原则**防止 AI 越权：下单前确认、不编造 ID、找不到给替代而不是空返回。

**你改什么**：

| 你的业务 | 改法 |
|---------|------|
| 奶茶店 | 服务范围改成"饮品搜索、推荐、下单、支付、门店自取"；不负责"跨店比价、第三方配送" |
| 预约服务 | 服务范围改成"服务搜索、预约、改期、取消"；不负责"到店后服务纠纷" |
| 零售电商 | 服务范围改成"商品搜索、规格选择、下单、支付、物流查询"；不负责"退换货争议" |
| 多 Skill | 每个 Skill 一行，各自写明负责和不负责 |

**文件大小限制**：≤ 10000 字节。

---

### 3. SKILL.md —— 单个业务 Skill 的流程说明

**干什么**：告诉 AI 这个 Skill 的业务流程、接口依赖关系和约束。AI 调用接口时会按这里写的流程来。

位置：`pages/drink-skill/drink-ordering/SKILL.md`

```markdown
# drink-ordering

## 服务范围

本 Skill 用于 WeStoreCafe 的饮品搜索、推荐、定制规格、下单、支付和配送。

## 用户意图入口

| 用户表达 | 应对流程 |
|---------|---------|
| 明确饮品名（"冰美式"） | searchDrinks → getDrinkDetail → chooseSku |
| 模糊需求（"想喝点清爽的"） | recommendDrinks |
| 下单 | 补齐规格/地址 → createOrder |
| 查状态 | queryOrderStatus |

## 业务流程

用户意图 → 搜索/推荐 → 展示饮品卡片 → 用户选择 → 补齐规格(杯型/温度/甜度) 
→ 选择门店/地址 → 创建订单草稿 → 用户确认 → 支付 → 返回状态卡

## 接口依赖

| 接口 | 前置条件 | 成功后下一步 |
|------|---------|------------|
| searchDrinks | 用户有关键词 | 展示饮品列表卡片 |
| recommendDrinks | 用户只有场景/偏好 | 展示推荐卡片 |
| getDrinkDetail | 已有 drinkId | 展示规格选项 |
| chooseSku | 已有 drinkId、规格 | 创建订单草稿 |
| chooseAddress | 已有订单草稿 | 展示配送信息 |
| createOrder | 已有 drinkId、sku、地址 | 展示订单确认卡 |
| requestPayment | 用户确认订单 | 拉起支付 |
| queryOrderStatus | 已有 orderId | 展示状态卡片 |

## 业务约束

1. 不要从用户自然语言编造 drinkId。
2. 规格（杯型/温度/甜度/加料）缺一项都不能下单。
3. 配送地址未填时，不创建订单。
4. 支付前必须展示完整订单确认卡并等用户确认。
```

**为什么这么写**：

- **用户意图入口**是最重要的一张表：AI 看到用户说的话，先匹配"这是哪种意图"，再走对应的接口链。
- **业务流程**是让 AI 理解先后顺序。不说技术术语，说业务动作。
- **接口依赖表**告诉 AI "调用这个之前必须先有那个"，防止 AI 跳过必要步骤。
- **业务约束**是红线："不要编造 ID"、"缺规格不下单"。

**你改什么**：

| 你的业务 | 改法 |
|---------|------|
| 改接口名 | 把 searchDrinks 换成你的接口名（如 searchProducts、searchServices） |
| 改业务约束 | 比如"预约需要填手机号，缺则不创建预约" |
| 改流程 | 比如你的餐饮是"先选门店→再选菜品→再下单"，流程就写成那样 |
| 多加 Skill | 一个 Skill 一个 SKILL.md，放在对应的分包目录下 |

**关键提醒**：SKILL.md 只管"流程"，不管"接口怎么实现"。接口的实现写在 apis/ 里，声明写在 mcp.json 里。

**文件大小限制**：≤ 16000 字节。

---

### 4. mcp.json —— 原子接口声明

**干什么**：声明这个 Skill 有哪些可调用的原子接口，每个接口的入参和返回结构。

位置：`pages/drink-skill/drink-ordering/mcp.json`

WeStoreCafe demo 声明了 7 个接口。以下展示核心的几个：

```json
{
  "apis": [
    {
      "name": "searchDrinks",
      "description": "根据用户输入的关键词、品类、温度偏好或价格区间搜索饮品。当用户有明确饮品名或品类需求时调用。不适用于用户仅表达模糊场景偏好（如'想喝点清爽的'），该场景应使用 recommendDrinks。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "keyword": {
            "type": "string",
            "description": "用户搜索的关键词，如'美式'、'拿铁'、'奶茶'。多关键词用空格分隔。缺省时返回全部饮品。"
          },
          "category": {
            "type": "string",
            "description": "饮品品类，可选值：coffee(咖啡)、tea(茶饮)、juice(果汁)、smoothie(冰沙)。缺省时不限制品类。"
          },
          "temperature": {
            "type": "string",
            "description": "温度偏好，可选值：hot(热)、iced(冰)、warm(温)。缺省时不限制温度。"
          },
          "maxPrice": {
            "type": "number",
            "description": "最高价格（元），如 25。缺省时不设价格上限。"
          }
        }
      }
    },
    {
      "name": "getDrinkDetail",
      "description": "获取指定饮品的详细信息：描述、图片、可选规格(杯型/温度/甜度/加料)、当前库存。drinkId 必须来自上游接口(searchDrinks/recommendDrinks)的返回结果，不得从用户自然语言中推测。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "drinkId": {
            "type": "string",
            "description": "饮品唯一标识，必须来自 searchDrinks 或 recommendDrinks 接口返回的 items[].id。不得从用户自然语言中编造或猜测。"
          }
        },
        "required": ["drinkId"]
      }
    },
    {
      "name": "createOrder",
      "description": "在用户确认规格、地址后创建饮品订单草稿。只有在前置接口(chooseSku/chooseAddress)已返回有效数据后才调用。订单创建后展示确认卡片，等用户确认后再调用 requestPayment。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "drinkId": {
            "type": "string",
            "description": "饮品ID，必须来自 getDrinkDetail 返回的 orderInfo.drinkId。"
          },
          "skuId": {
            "type": "string",
            "description": "规格组合ID，必须来自 chooseSku 接口返回的 skuId。"
          },
          "addressId": {
            "type": "string",
            "description": "配送地址ID，必须来自 chooseAddress 接口返回的 addressId。"
          },
          "quantity": {
            "type": "integer",
            "description": "购买数量，默认值为 1。"
          },
          "remark": {
            "type": "string",
            "description": "用户备注，如'少糖'、'去冰'。缺省时不添加备注。"
          }
        },
        "required": ["drinkId", "skuId", "addressId"]
      }
    }
  ],
  "components": [
    {
      "path": "components/drink-list/index",
      "relatedPage": "/pages/drink/list",
      "description": "饮品列表卡片：展示搜索/推荐的饮品，每项含名称、价格、温度标签和选择按钮"
    },
    {
      "path": "components/order-confirm/index",
      "relatedPage": "/pages/order/confirm",
      "description": "订单确认卡片：展示订单草稿（饮品、规格、价格、配送地址），含确认和修改按钮",
      "expirable": true,
      "expiredText": "订单已过期"
    },
    {
      "path": "components/order-status/index",
      "relatedPage": "/pages/order/detail",
      "description": "订单状态卡片：展示订单进度（已下单→制作中→配送中→已送达），实时更新",
      "permissions": {
        "scope.dynamic": {
          "desc": "订单状态需要实时更新，展示制作和配送进度"
        }
      },
      "expirable": true,
      "expiredText": "订单已完成"
    }
  ]
}
```

**每个接口 description 的写法规则**（官方最佳实践）：

| 规则 | 例子 | 为什么 |
|------|------|--------|
| 首句声明业务对象 | "根据用户输入的关键词搜索饮品" | AI 快速判断该调哪个接口 |
| 声明适用/不适用场景 | "不适用于模糊场景偏好，该场景应用 recommendDrinks" | 防止 AI 在错误场景调用 |
| ID 字段声明取值来源 | "drinkId 必须来自 searchDrinks 返回的 items[].id" | 防止 AI 编造 ID |
| 普通字段多举例+缺省处理 | "如'美式'、'拿铁'。缺省时返回全部饮品" | AI 知道什么时候传、不传会怎样 |

**mcp.json 大小限制**：≤ 24000 字节。

**你改什么**：

| 你的业务 | 改法 |
|---------|------|
| 接口数量不同 | demo 有 7 个接口，你的可以 3 个也可以 15 个 |
| 接口名 | 用语义化名称，如 searchProducts、getProductDetail、createBooking |
| description | 按上面 4 条规则重写你的接口描述 |
| inputSchema | 改字段名和说明，ID 字段必须标注"取值来源" |
| components | 改成你的卡片（商品列表卡、预约确认卡等） |

**⚠️ 最容易踩的坑**：

1. **ID 字段不写取值来源**：AI 会从用户的自然语言里编一个 ID，比如用户说"我想喝上次那个"，AI 可能编 `drinkId: "上次那个"`。
2. **description 只写功能不写边界**：比如只写"搜索饮品"，不写"不适用于模糊需求"，AI 会在所有场景都调这个接口。
3. **required 字段不对**：必填的不标 required、不该必填的标了 required，都会导致调用失败。

---

### 5. index.js —— 接口注册 + 中间件

**干什么**：创建 Skill、注册中间件（统一登录态）、注册所有原子接口。

```javascript
const skill = wx.modelContext.createSkill('pages/drink-skill/drink-ordering')

// === 中间件：统一登录态和计时 ===
skill.use(async (ctx, next) => {
  const start = Date.now()
  try {
    const token = wx.getStorageSync('token')
    if (!token) {
      // 没有 token，先微信登录获取
      const { code } = await wx.login()
      const res = await wx.request({
        url: 'https://your-server.com/api/login',
        data: { code }
      })
      wx.setStorageSync('token', res.data.token)
    }
    await next()
    console.log(`[drink] ${ctx.name} 耗时 ${Date.now() - start}ms`)
  } catch (err) {
    console.error(`[drink] ${ctx.name} 错误:`, err)
    throw err
  }
})

// === 注册原子接口 ===
// 以下接口按 SKILL.md 的业务流程顺序排列
const searchDrinks = require('./apis/searchDrinks')
const recommendDrinks = require('./apis/recommendDrinks')
const getDrinkDetail = require('./apis/getDrinkDetail')
const chooseSku = require('./apis/chooseSku')
const chooseAddress = require('./apis/chooseAddress')
const createOrder = require('./apis/createOrder')
const requestPayment = require('./apis/requestPayment')
const queryOrderStatus = require('./apis/queryOrderStatus')

skill.registerAPI('searchDrinks', searchDrinks)
skill.registerAPI('recommendDrinks', recommendDrinks)
skill.registerAPI('getDrinkDetail', getDrinkDetail)
skill.registerAPI('chooseSku', chooseSku)
skill.registerAPI('chooseAddress', chooseAddress)
skill.registerAPI('createOrder', createOrder)
skill.registerAPI('requestPayment', requestPayment)
skill.registerAPI('queryOrderStatus', queryOrderStatus)
```

**为什么这么写**：

- `wx.modelContext.createSkill(path)` 的 path 必须和 `app.json` 里的 `agent.skills[].path` 完全一致。
- 中间件在这里比在每个接口里写一遍登录逻辑好，统一处理，改一处全生效。
- `registerAPI` 的 name 必须和 `mcp.json` 里的 `name` 完全一致，大小写也要对。

**你改什么**：

| 你的情况 | 改法 |
|---------|------|
| 接口数量不同 | 注册你实际有的接口 |
| 登录方式不同 | 改中间件的登录逻辑（如用手机号登录） |
| 不需要登录 | 可以不加中间件 |
| 多 Skill | 每个 Skill 分包下各自一个 index.js |

---

### 6. apis/*.js —— 每个接口的真实逻辑

**干什么**：这是每个原子接口的实现。调后端、调云函数、处理数据、返回结果。

以 `searchDrinks.js` 为例：

```javascript
// searchDrinks —— 搜索饮品
// 返回值结构：{ isError, content, structuredContent, _meta }
// - isError: false → 渲染卡片（如果有绑定组件）
// - content: 给 LLM 的文本（事实+动作两段式）
// - structuredContent: 结构化数据传给组件渲染
// - _meta: 对 LLM 不可见，传给组件

async function searchDrinks({ keyword, category, temperature, maxPrice }) {
  // 1. 参数校验（必须做！AI 生成的参数不保证正确）
  if (keyword && typeof keyword !== 'string') {
    return {
      isError: true,
      content: [{ type: 'text', text: '搜索关键词格式不正确，请重新输入饮品名或品类。不要重复调用此接口。' }]
    }
  }

  // 2. 调业务接口
  try {
    const res = await wx.request({
      url: 'https://your-server.com/api/drinks/search',
      method: 'GET',
      data: { keyword, category, temperature, maxPrice },
      header: {
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      }
    })

    const drinks = res.data.items

    // 3. 无结果时（三要素：事实+出口+禁令）
    if (!drinks || drinks.length === 0) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: '抱歉，暂未找到相关饮品。您可以换个关键词试试（如"咖啡""奶茶"），或者让我为您推荐热门饮品。不要重复用相同关键词搜索。'
        }]
      }
    }

    // 4. 正常返回（事实+动作两段式）
    return {
      isError: false,
      content: [{
        type: 'text',
        text: `已为您找到${drinks.length}款饮品：${drinks.map(d => d.name).join('、')}。请展示饮品列表卡片供用户选择，用户选择后调用 getDrinkDetail 查询详情。`
      }],
      structuredContent: {
        items: drinks.map(d => ({
          id: d.id,
          name: d.name,
          price: d.price,
          image: d.image,
          tags: d.tags,
          description: d.description
        }))
      }
    }
  } catch (err) {
    // 5. 系统异常
    return {
      isError: true,
      content: [{
        type: 'text',
        text: '饮品搜索服务暂时不可用，请稍后重试。不要立即重复调用。'
      }]
    }
  }
}

module.exports = searchDrinks
```

**content 的"事实+动作"两段式写法**：

| 场景 | 事实 | 动作 |
|------|------|------|
| 正常返回 | "已为您找到3款饮品：冰美式、热拿铁、柠檬茶" | "请展示饮品列表卡片供用户选择，用户选择后调用 getDrinkDetail 查询详情" |
| 无结果 | "暂未找到相关饮品" | "您可以换个关键词试试，或者让我为您推荐热门饮品。不要重复用相同关键词搜索。" |
| 系统异常 | "服务暂时不可用" | "请稍后重试。不要立即重复调用。" |

**你改什么**：

| 你的情况 | 改法 |
|---------|------|
| 后端地址 | 把 `https://your-server.com/api/...` 换成你的真实接口 |
| 字段名 | 返回的 `structuredContent` 字段换成你的业务字段 |
| 登录方式 | 改 header 里的 token 获取方式 |
| 无结果处理 | 换成你自己的业务场景话术 |

**⚠️ 最容易踩的坑**：content 里只写"找到3个商品"，不写"下一步做什么"。AI 不知道接下来该调什么接口，就乱调或发呆。一定要写"用户选择后调用 xxx 接口"。

---

### 7. components/*.js —— GUI 卡片组件

**干什么**：把接口返回的结构化数据渲染成对话流里的 GUI 卡片，用户可以直接点击操作。

以 `drink-list`（饮品列表卡片）为例：

```javascript
// components/drink-list/index.js
// WeStoreCafe 饮品列表卡片

Component({
  data: {
    drinks: [],
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
        const drinks = result.structuredContent.items || []
        this.setData({ drinks, loading: false })

        // ⚠️ 必须设置关联页面，否则卡片右上角的入口按钮无法跳转
        viewCtx.setRelatedPage({ query: `from=agent` })
      })

      // 监听内容溢出
      viewCtx.on(NotificationType.Overflow, (data) => {
        console.warn('[drink-list] 卡片内容溢出', data)
      })
    }
  },

  methods: {
    // 用户点击某个饮品 → 上行消息，让 AI 继续处理
    onSelectDrink(e) {
      const drink = e.currentTarget.dataset.drink
      const ctx = wx.modelContext.getContext(this)
      ctx.sendFollowUpMessage({
        content: [
          { type: 'text', text: `我想看看${drink.name}` },
          { type: 'api/call', data: { name: 'getDrinkDetail', arguments: { drinkId: drink.id } } }
        ]
      })
    }
  }
})
```

**为什么这么写**：

- 组件用 `wx.modelContext.getContext(this)` 获取 Agent 上下文。
- 监听 `NotificationType.Result` 接收接口返回数据。
- `viewCtx.setRelatedPage()` 必须调用，设置关联页面 query，否则卡片右上角的"进入小程序"按钮点不了。
- 用户点击卡片 → `sendFollowUpMessage` 上行消息 → 带上接口名和参数 → AI 自动调用下一个接口。
- 组件尺寸限制：宽高比 4:1 到 1:1，初始化后不能改。

**你改什么**：

| 你的情况 | 改法 |
|---------|------|
| 展示列表 | 把 `drinks` 换成你的数据字段（products、services、stores） |
| 点击行为 | `sendFollowUpMessage` 里改接口名和参数 |
| 关联页面 | `viewCtx.setRelatedPage` 改成你的实际页面路径和 query |
| 过期态 | 订单/预约类卡片加 `expirable: true`，过期后用户不能点 |

**⚠️ 最容易踩的坑**：

1. **忘了 setRelatedPage**：卡片右上角的入口按钮点了没反应。
2. **sendFollowUpMessage 里参数缺失**：比如传了 `drinkId` 但没传 `skuId`，下一个接口报错。
3. **组件尺寸超限**：设计的卡片太高，被裁剪。

**Demo 里几个典型卡片**：

| 卡片 | 触发接口 | 展示内容 | 用户可操作 |
|------|---------|---------|-----------|
| 饮品列表卡 | searchDrinks / recommendDrinks | 饮品名、价格、标签、缩略图 | 点击选择 → 调 getDrinkDetail |
| 规格选择卡 | getDrinkDetail | 杯型、温度、甜度、加料选项 | 点击确认 → 调 chooseSku |
| 地址选择卡 | chooseAddress | 最近地址列表 | 点击选择或新增 |
| 订单确认卡 | createOrder | 饮品名、规格、价格、地址、备注 | 确认 → 调 requestPayment；修改 → 回到上一步 |
| 支付状态卡 | requestPayment | 支付成功/失败 | 查看订单 → 调 queryOrderStatus |
| 订单进度卡 | queryOrderStatus | 下单→制作中→配送中→已送达 | 动态更新（需声明 scope.dynamic） |

---

### 8. page-meta.json —— 页面元数据兜底

**干什么**：告诉 AI 这个小程序有哪些页面、每个页面做什么、能接什么 query 参数。当 Skill 不匹配时，AI 可能用文字链引导用户到某个页面。

```json
{
  "pages": [
    {
      "path": "pages/home/home",
      "name": "首页",
      "description": "展示 WeStoreCafe 所有饮品种类和门店入口"
    },
    {
      "path": "pages/drink/detail",
      "name": "饮品详情",
      "description": "展示特定饮品的价格、描述、规格选项和库存",
      "query": {
        "type": "object",
        "properties": {
          "drinkId": { "type": "string", "description": "饮品的唯一标识符" }
        },
        "required": ["drinkId"]
      }
    },
    {
      "path": "pages/order/detail",
      "name": "订单详情",
      "description": "展示订单的饮品、规格、价格、支付状态和配送进度",
      "query": {
        "type": "object",
        "properties": {
          "orderId": { "type": "string", "description": "订单唯一标识符" }
        },
        "required": ["orderId"]
      }
    },
    {
      "path": "pages/store/list",
      "name": "门店列表",
      "description": "展示附近 WeStoreCafe 门店的地址、营业时间和距离"
    }
  ]
}
```

**为什么这么写**：

- 这是开发模式的兜底：如果所有 Skill 都不匹配用户意图，AI 至少知道有哪些页面可以文字链。
- `query` 声明让 AI 知道每个页面能接什么参数，不会生成错误的链接。
- page-meta.json 放在小程序根目录或主包内，不在 Skill 分包里。

**你改什么**：把你小程序的真实页面路径、名称、描述和 query 参数填进来。

**文件大小限制**：≤ 8000 字节。

---

## 三、Demo 的完整文件树

```
WeStoreCafe (小程序根目录)
│
├── AGENTS.md                    ← 全局提示词
├── app.json                     ← 声明 Skill + 分包
├── page-meta.json               ← 页面元数据兜底
│
├── pages/
│   ├── home/home                ← 普通页面（首页）
│   ├── drink/detail             ← 普通页面（饮品详情）
│   ├── order/detail             ← 普通页面（订单详情）
│   └── store/list               ← 普通页面（门店列表）
│
└── pages/drink-skill/           ← Skill 独立分包
    └── drink-ordering/
        ├── SKILL.md             ← 业务流程说明
        ├── mcp.json             ← 原子接口声明
        ├── index.js             ← 接口注册 + 中间件
        ├── apis/
        │   ├── searchDrinks.js
        │   ├── recommendDrinks.js
        │   ├── getDrinkDetail.js
        │   ├── chooseSku.js
        │   ├── chooseAddress.js
        │   ├── createOrder.js
        │   ├── requestPayment.js
        │   └── queryOrderStatus.js
        └── components/
            ├── drink-list/
            │   ├── index.js     ← 饮品列表卡片
            │   ├── index.wxml
            │   └── index.wxss
            ├── order-confirm/
            │   └── index.js     ← 订单确认卡片
            └── order-status/
                └── index.js     ← 订单状态卡片
```

**8 个文件类型的关系**：

```
用户说话 → AI 读 AGENTS.md 判断归不归我管
         → 读 SKILL.md 判断该走什么流程
         → 读 mcp.json 找到可调用的接口和参数
         → 调 index.js 注册的接口
         → 接口实现(apis/*.js)调后端拿数据
         → 返回 structuredContent
         → 组件(components/*.js)渲染成 GUI 卡片
         → 用户在卡片上点击
         → 上行消息触发下一个接口
         → 循环直到订单完成/预约成功/查询结束
```

---

## 四、照着 demo 改的检查清单

改完后逐项检查：

```
□ 1. app.json
  □ lazyCodeLoading 开启了
  □ 分包路径和 agent.skills[].path 一致
  □ Skill 名称和目录名一致

□ 2. AGENTS.md
  □ 服务范围说清楚了
  □ Skill 分工表每个 Skill 都有"负责"和"不负责"
  □ 全局原则包含了"下单前确认"和"找不到给替代"
  □ 文件 ≤ 10KB

□ 3. SKILL.md
  □ 用户意图入口表覆盖了所有常见用户表达
  □ 业务流程写的是业务动作，不是技术术语
  □ 接口依赖表每个接口都有前置条件和下一步
  □ 业务约束写清楚了红线
  □ 文件 ≤ 16KB

□ 4. mcp.json
  □ 每个接口的 description 首句声明了业务对象
  □ 每个接口的 description 写了适用/不适用场景
  □ 所有 ID 字段的 description 标注了"取值来源"
  □ 普通字段 description 多举例 + 缺省处理
  □ required 字段和实际必填一致
  □ components 每个都关联了 relatedPage
  □ 文件 ≤ 24KB

□ 5. index.js
  □ createSkill 的 path 和 app.json 一致
  □ registerAPI 的 name 和 mcp.json 的 name 完全一致（含大小写）
  □ 中间件的登录逻辑和你的后端匹配

□ 6. apis/*.js
  □ 每个接口都做了参数校验
  □ 正常返回的 content 是"事实+动作"两段式
  □ 无结果时返回"事实+出口+禁令"三要素
  □ 系统异常有兜底，不直接 throw

□ 7. components/*.js
  □ created() 里调了 viewCtx.setRelatedPage()
  □ sendFollowUpMessage 参数完整（接口名+必填参数）
  □ 卡片尺寸在 4:1 到 1:1 之间

□ 8. page-meta.json
  □ 真实页面路径都写了
  □ query 参数声明了 type 和 required
  □ 文件 ≤ 8KB
```

---

## 五、Demo 为什么这么设计（给开发者讲的设计逻辑）

### 1. 不把页面搬进 AI，而是把"能力"暴露给 AI

传统思路：把小程序每个页面都注册给 AI → AI 帮用户打开页面。

Demo 的思路：只把"搜索饮品""查看详情""下单""支付"这些**能力**封装成接口 → AI 直接调用能力，返回结构化结果 → 用户在卡片上完成操作，不用跳页面。

这才是开发模式的精髓：**让 AI 帮用户完成任务，而不是帮用户找页面。**

### 2. 模糊意图 → 推荐 → 明确 → 下单（渐进式确认）

用户说"想喝点清爽的"，AI 不急着问"要什么饮品、什么杯型、什么温度"，先调 recommendDrinks 展示推荐列表。用户选了一个，再调 getDrinkDetail 展示规格。规格选好了，再选地址。全补齐了，才创建订单。

每一步都是"展示候选 → 用户选择 → 确认下一步"，而不是"一口气问完所有信息"。

### 3. ID 不准 AI 编，必须从前一步接口拿

drinkId 从 searchDrinks 回来 → skuId 从 chooseSku 回来 → addressId 从 chooseAddress 回来。

demo 的 mcp.json 里每个 ID 字段都标注了"必须来自 xxx 接口返回的 xxx"。这是官方最佳实践里最强调的一条：**接口之间靠"返回值→入参"衔接，不靠 AI 记忆。**

### 4. GUI 卡片替代纯文本

接口返回的不是一段文字告诉用户"有 3 款饮品：冰美式 12 元、热拿铁 15 元..."，而是 structuredContent + 原子组件渲染成可点击的卡片。

用户不需要打字回复"我要冰美式"，而是在卡片上直接点"冰美式"按钮。

### 5. 每个接口都是"无状态的"

AI 不记住"用户刚才选了冰美式"，而是把 drinkId 作为参数传给下一个接口。下一个接口自己查数据库拿到最新信息。

这样的好处：用户可以多轮对话、可以改主意（"换热拿铁"）、可以同时下多单、不会因为 AI 上下文丢失而状态不一致。

---

## 六、从 WeStoreCafe 到你的业务（迁移表）

| WeStoreCafe | 你的奶茶店 | 你的预约服务 | 你的零售电商 |
|------------|-----------|------------|------------|
| searchDrinks | searchTeas | searchServices | searchProducts |
| recommendDrinks | recommendTeas | recommendServices | recommendProducts |
| getDrinkDetail | getTeaDetail | getServiceDetail | getProductDetail |
| chooseSku | chooseSku（杯型/加料） | chooseTimeSlot | chooseSku（颜色/尺码） |
| chooseAddress | chooseStore（自取门店） | chooseAddress | chooseAddress |
| createOrder | createOrder | createBooking | createOrder |
| requestPayment | requestPayment | confirmBooking | requestPayment |
| queryOrderStatus | queryOrderStatus | queryBookingStatus | queryLogistics |

---

## 更深入

- 完整 AI 能力清单（原子接口、原子组件、半屏页面、交互API、最佳实践）→ `references/ai-capabilities.md`
- 12 个行业接入案例 → `references/industry-cases.md`
- 代码生成模板 → `references/code-templates.md`
