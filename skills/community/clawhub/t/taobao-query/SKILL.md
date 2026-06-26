---
name: taobao-query
description: Query Taobao product prices and information through MCP (Model Context Protocol). Use when the user asks about product prices, searches for items on Taobao, compares prices, or wants to find the best deals on specific products. Triggers on phrases like "淘宝价格", "多少钱", "查一下价格", "销量", "店铺" or any product-related price inquiries. Can also perform other Taobao operations like viewing cart, checking orders, chatting with customer service, etc. - but NEVER payment or financial operations.
---

# Taobao Query Skill

This skill enables interacting with Taobao through an MCP (Model Context Protocol) server to query products, manage cart/orders, and communicate with sellers.

## ⚠️ Prerequisites - IMPORTANT

**This skill requires a running Taobao MCP server.**

### Setup Required

1. **Install Taobao Desktop Client** (淘宝桌面版) on your local machine
2. **Enable MCP service** in the client settings
3. **Configure MCP URL** in your OpenClaw config (see below)

### Default Configuration

**Default MCP Server:** `http://127.0.0.1:3654/mcp`

If your MCP server runs on a different address, configure it via environment variable:

```bash
# Add to your OpenClaw environment or shell profile
export TAOBAO_MCP_URL="http://your-server-ip:3654/mcp"
```

Or set it in OpenClaw config:
```json
{
  "env": {
    "TAOBAO_MCP_URL": "http://192.168.100.20:3654/mcp"
  }
}
```

## When to Use This Skill

Use this skill when the user:
- Asks about product prices on Taobao (e.g., "iPhone 16 淘宝价格")
- Wants to search for items and compare prices
- Asks to view shopping cart contents
- Wants to check order status or history
- Needs to contact seller/customer service via 旺旺
- Requests product links from Taobao
- Mentions "销量" (sales volume), "店铺" (shop), "价格" (price), "购物车" (cart), "订单" (order)

## 🔴 RESTRICTION - IMPORTANT

**NEVER perform the following operations:**
- Payment or checkout operations
- Confirming orders
- Any financial transactions
- Authorizing payments
- Auto-buying with stored payment methods

**Permitted operations:**
- Search products
- View cart/orders (read-only)
- Add items to cart
- Browse products
- Chat with customer service
- Navigate pages

## Query Strategy Based on User Input

### Case 1: Specific Product Model Given

When user provides a **specific model** (e.g., "iPhone 16 Pro Max 256GB", "MacBook Air M4 13寸 16GB+512GB", "AirPods Pro 2"):

1. **Search with exact keywords** provided by user
2. **Filter results:**
   - Remove accessories, cases, protective films
   - Remove single-ear replacements, charging case only listings
   - Remove second-hand items (二手)
   - Remove suspiciously low prices (e.g., iPhone for ¥1000)
3. **Sort by price** (ascending)
4. **Return top 5-8 results** showing:
   - Different stores and their prices
   - Any subsidies (政府补贴, 百亿补贴) applied
   - Official store for reference

### Case 2: General Product Category Only

When user asks about a **general category** without specific model (e.g., "iPhone", "MacBook Air", "蓝牙耳机", "机械键盘"):

1. **Search with broad keywords**
2. **Analyze all results** to identify:
   - Different models/variants available
   - Different specifications (storage, color, size, etc.)
   - Price distribution across variants
3. **Categorize by specifications:**
   - Group similar products together
   - Identify entry-level, mid-range, high-end variants
4. **Provide comprehensive report:**
   - Price range for each specification tier
   - Popular/recommended variants
   - Purchase advice based on use case

## MCP Configuration

**Server URL:** `${TAOBAO_MCP_URL:-http://127.0.0.1:3654/mcp}`  
**Transport:** `streamableHttp`  
**Server Name:** `taobao-native`

## MCP Call Process

The MCP server uses streamable HTTP transport. Standard call process:

1. **Initialize connection** to get session ID:
```bash
curl -X POST ${TAOBAO_MCP_URL:-http://127.0.0.1:3654/mcp} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {
        "name": "openclaw-agent",
        "version": "1.0.0"
      }
    }
  }'
```

2. **Extract session ID** from response headers: `mcp-session-id: <uuid>`

3. **Call tools** with session ID in header: `mcp-session-id: <session-id>`

## Available Tools

### Product Search & Browsing
- **search_products** - Search products by keyword
- **navigate** - Navigate to Taobao pages (home, cart, order, tmall, my, etc.)
- **navigate_to_url** - Open any URL
- **read_page_content** - Read visible page text
- **scroll_page** - Scroll page
- **scan_page_elements** - Scan interactive elements
- **click_element** - Click page element
- **input_text** - Input text to fields

### Cart & Orders (Read-Only)
- **navigate** with `page: cart` or `page: order`
- **read_page_content** - View cart/order details
- **add_to_cart** - Add items to cart (safe, no payment)

### Customer Service
- **open_chat** - Open Wangwang chat and send message
- **send_chat_message** - Send additional messages in chat

### Utility
- **get_browse_history** - Get browsing history (product/search/shop)
- **get_current_tab** - Get current page info
- **close_page** - Close current page
- **inspect_page** - Diagnose page DOM state

## Output Formats

### Format A: Specific Model Search Results

Use when user provided specific model:

```
## 🛍️ [Product Model] 价格查询结果

### 价格对比（从低到高）

| 排名 | 店铺 | 价格 | 优惠/补贴 | 链接 |
|:---:|:---|:---:|:---|:---:|
| 1 | [店铺名] | **¥XXXX** | 政府补贴15% | [查看](URL) |
| 2 | [店铺名] | **¥XXXX** | 百亿补贴 | [查看](URL) |
| 3 | [店铺名] | **¥XXXX** | 无 | [查看](URL) |

### 购买建议
- **最优惠**: [店铺名] ¥XXXX（有政府补贴，需确认资格）
- **官方保障**: Apple Store 官方旗舰店 ¥XXXX
- **注意事项**: [任何需要提醒的事项]
```

### Format B: General Category Analysis

Use when user asked about a category without specific model:

```
## 🛍️ [Product Category] 价格分析

查询到 [N] 款在售商品，按规格分类如下：

### 📱 规格分类与价格区间

| 规格/型号 | 价格区间 | 推荐入手价 | 说明 |
|:---------|:---:|:---:|:---|
| 入门款/基础版 | ¥X,XXX - ¥X,XXX | **¥X,XXX** | 适合日常使用 |
| 中端款/Pro版 | ¥X,XXX - ¥X,XXX | **¥X,XXX** | 性价比最高 |
| 旗舰款/Max版 | ¥X,XXX - ¥X,XXX | **¥X,XXX** | 专业需求 |

### 💰 具体价格参考

**[规格A]**
- 最低价：¥XXXX（[店铺名]）
- 官方价：¥XXXX（官方旗舰店）
- 百亿补贴价：¥XXXX（如适用）

**[规格B]**
- ...

### 🎯 购买建议

**预算有限**: 选择 [规格A]，推荐 [店铺] ¥XXXX
**追求性价比**: 选择 [规格B]，推荐 [店铺] ¥XXXX  
**要官方保障**: 选择官方旗舰店 [规格] ¥XXXX

**注意事项**:
- [提醒1: 如政府补贴需要资格]
- [提醒2: 如百亿补贴库存有限]
- [提醒3: 如新品即将发布等]
```

## Filtering Rules

**Always filter out:**
- Price = 0 or null
- Missing shop name
- Clearly mismatched products (e.g., searching for iPhone but getting cases)
- Used/second-hand items (二手, 翻新) unless specifically requested
- Accessories when searching for main product (cases, chargers, etc.)
- Suspiciously low prices (e.g., MacBook for ¥2000)
- Service listings (安装系统, 数据恢复, 租赁)

**Link format:**
- Extract itemId from productUrl
- Tmall: `https://detail.tmall.com/item.htm?id=<itemId>`
- Taobao: `https://item.taobao.com/item.htm?id=<itemId>`

## Connection Health Detection

MCP service may disconnect. Detect and handle connection issues:

### Connection Error Patterns

**Connection failed indicators:**
- `Connection failed` or `Connection refused` errors
- Timeout errors (no response after 10+ seconds)
- `mcp-session-id` header missing from initialize response
- Empty or malformed JSON responses
- HTTP status codes: 500, 502, 503, 504

**Session expired indicators:**
- Error message: "未提供有效的会话ID" (invalid session ID)
- Error code: `-32000` with session-related message
- Previously working session suddenly returns auth errors

### Connection Recovery Steps

When connection fails:

1. **First failure:**
   ```
   ⚠️ MCP 服务连接失败，正在尝试重新连接...
   ```
   - Retry initialize with new session
   - If succeeds, continue with operation

2. **Second failure (persistent):**
   ```
   ❌ MCP 服务暂时不可用

   可能原因：
   - 淘宝桌面客户端未运行
   - 网络连接问题
   - MCP 服务需要重启

   建议操作：
   1. 检查淘宝桌面客户端是否已打开
   2. 确认电脑网络连接正常
   3. 重启淘宝桌面客户端后重试
   
   当前配置的 MCP 地址: ${TAOBAO_MCP_URL:-http://127.0.0.1:3654/mcp}
   ```
   - Stop attempting further MCP calls
   - Inform user clearly about the issue
   - Provide actionable troubleshooting steps

3. **Session expired mid-operation:**
   - Detect "invalid session" errors
   - Automatically re-initialize with new session
   - Retry the failed operation once
   - If still fails, treat as connection failure (step 2)

### Proactive Health Check

Before major operations (e.g., viewing cart with many items), optionally verify connection:
```bash
# Quick health check - try to get current tab
curl -X POST ${TAOBAO_MCP_URL:-http://127.0.0.1:3654/mcp} \
  -H "mcp-session-id: <session-id>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_current_tab"}}'
```

## Error Handling

If the MCP server is unreachable or returns an error:
1. **Detect error type** (connection vs. session vs. operational)
2. **For connection errors:** Follow Connection Recovery Steps above
3. **For session errors:** Attempt re-initialization once, then follow recovery steps
4. **For operational errors:** Inform user of specific error, suggest alternatives
5. **Never** make up fake product data or pretend operation succeeded

## Safety Reminders

- **Never** proceed to payment or checkout
- **Never** click "立即购买" (Buy Now) if it leads to payment
- **Never** confirm orders on behalf of the user
- Cart operations (add/view) are safe - payment is the red line

## Example Interactions

**User:** "iPhone 16 Pro Max 256GB 多少钱"
→ Specific model given → Search exact keywords → Filter accessories → Return top 5-8 prices

**User:** "MacBook Air 推荐"
→ Category only → Search broadly → Analyze all M3/M4/M5 variants → Provide price ranges for each spec → Give purchase advice

**User:** "看看我的购物车"
→ Use `navigate` to cart → `read_page_content` → Show items
