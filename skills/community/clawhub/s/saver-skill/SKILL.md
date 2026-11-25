# Saver Skill

Smart shopping assistant - Connects to Saver MCP Server for product search and price comparison services.

**Note: Currently serving users in Mainland China only. More countries and regions coming soon.**

## Features

- 🎯 Requirement analysis (auto-determine if confirmation is needed)
- 🔍 Product search (JD.com / Taobao)
- 📊 Smart sorting (sales / price / rating)
- 🔗 Auto link conversion (generate affiliate links)
- 💰 Price calculation (coupon price + government subsidies)
- 🌊 **SSE Streaming** - Real-time progress updates

---

## ⚠️ Recommended Workflow (Important)

**AI Agent should call tools in the following order:**

```
┌─────────────────────────────────────────────────────────┐
│  User request: "Help me buy a phone"                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 1: Call analyze_shopping_need                     │
│  Analyze requirements, determine if confirmation needed │
└─────────────────────────────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
    needConfirm=false            needConfirm=true
            │                           │
            │                           ▼
            │                 ┌─────────────────────┐
            │                 │ Communicate with    │
            │                 │ user to confirm     │
            │                 │ (price, brand, etc) │
            │                 └─────────────────────┘
            │                           │
            └─────────────┬─────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: Call unified_search                            │
│  Search → Sort → Link conversion (all in one call)      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: Return results to user                         │
│  Product names are hyperlinks, click to buy             │
└─────────────────────────────────────────────────────────┘
```

**Key Points**:
- ✅ Must call `analyze_shopping_need` first
- ✅ If requirements are unclear, communicate with user to confirm
- ✅ After requirements are clear, call `unified_search`

---

## Tools

| Tool | Description | When to use |
|-----|------|---------|
| `unified_search` | Search + Sort + Link conversion (all in one) | **After requirements are clear** |
| `analyze_shopping_need` | Analyze user requirements | **Must call first** |
| `complete_shopping` | Complete flow (auto analyze + search) | Alternative to above two |
| `search_products` | Search only (no link conversion) | Not recommended |

---

## unified_search Parameters

| Parameter | Type | Required | Description |
|-----|------|-----|------|
| keyword | string | ✅ | Search keyword |
| minPrice | number | ❌ | Minimum price |
| maxPrice | number | ❌ | Maximum price |
| pageSize | number | ❌ | Results per platform (default: 10) |
| sortBy | string | ❌ | Sort method (default: sales) |

**Sort Options**:
- `sales` - Sort by sales (default)
- `price_asc` - Sort by price ascending
- `price_desc` - Sort by price descending
- `rating` - Sort by rating

---

## Technical Details

- **MCP Server**: `http://81.70.235.20:3001/mcp`
- **Protocol**: MCP 2024-11-05 (Streamable HTTP + SSE)
- **Supported Platforms**: JD.com (self-operated only), Taobao (Tmall only)
- **No Authentication Required**: Public service, direct access
- **Capabilities**: streaming, sse

---

## Notes

- ⚠️ **Commission info is NOT exposed to users**
- ⚠️ Product names contain affiliate links, users can click to buy
- ⚠️ Only searches JD self-operated and Tmall products (quality first)

---

*Version: 1.2.0*

---

## 中文版

# Saver Skill (省心买)

智能购物助手 - 连接省心买 MCP Server，提供商品搜索和比价推荐服务。

**注意：目前仅服务中国大陆用户，更多国家、地区服务陆续开通中。**

## 功能

- 🎯 需求分析（判断是否需要确认）
- 🔍 商品搜索（京东/淘宝）
- 📊 智能排序（销量/价格/评分）
- 🔗 自动转链（生成推广链接）
- 💰 价格计算（券后价+国家补贴）
- 🌊 **SSE 流式输出** - 实时进度推送

---

## ⚠️ 推荐调用流程（重要）

**AI Agent 应按以下顺序调用工具：**

```
┌─────────────────────────────────────────────────────────┐
│  用户请求："帮我买个手机"                                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 1: 调用 analyze_shopping_need                     │
│  分析需求，判断是否需要与用户确认                         │
└─────────────────────────────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
    needConfirm=false            needConfirm=true
            │                           │
            │                           ▼
            │                 ┌─────────────────────┐
            │                 │ 与用户沟通确认需求   │
            │                 │ （价格、品牌、规格） │
            │                 └─────────────────────┘
            │                           │
            └─────────────┬─────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: 调用 unified_search                            │
│  搜索 → 排序 → 转链（一步完成）                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: 格式化结果返回给用户                            │
│  商品名称为超链接，点击即可跳转购买                       │
└─────────────────────────────────────────────────────────┘
```

**关键点**：
- ✅ 必须先调用 `analyze_shopping_need`
- ✅ 如果需求不明确，与用户沟通确认
- ✅ 需求明确后，调用 `unified_search`

---

## MCP 工具列表

| 工具 | 功能 | 调用时机 |
|-----|------|---------|
| `unified_search` | 搜索+排序+转链（一键完成） | **需求明确后调用** |
| `analyze_shopping_need` | 分析用户需求 | **必须首先调用** |
| `complete_shopping` | 完整购物流程（含自动分析） | 可替代上述两步 |
| `search_products` | 仅搜索商品 | 不推荐（不含转链） |

---

## unified_search 参数

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| keyword | string | ✅ | 搜索关键词 |
| minPrice | number | ❌ | 最低价格 |
| maxPrice | number | ❌ | 最高价格 |
| pageSize | number | ❌ | 每平台结果数（默认10） |
| sortBy | string | ❌ | 排序方式（默认销量） |

**排序选项**：
- `sales` - 按销量排序（默认）
- `price_asc` - 按价格升序
- `price_desc` - 按价格降序
- `rating` - 按评分排序

---

## 技术说明

- **MCP Server**: `http://81.70.235.20:3001/mcp`
- **协议版本**: MCP 2024-11-05 (Streamable HTTP + SSE)
- **支持平台**: 京东（仅自营）、淘宝（仅天猫）
- **无需认证**: 公开服务，直接调用
- **能力**: 流式输出、SSE

---

## 注意事项

- ⚠️ **佣金信息不对外展示**
- ⚠️ 商品名称已包含推广链接，用户点击即可跳转
- ⚠️ 默认只搜京东自营和天猫商品（品质优先）

---

*版本：1.2.0*
