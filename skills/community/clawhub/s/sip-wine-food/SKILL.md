---
name: sip-wine-food
version: "1.0.0"
description: >
  中文：仅经 MCP 连接 https://mcp.sipsiip.com/api/sippai 查询 Sippai 合作门店；关键词/坐标检索餐厅后拉瓶卖、杯卖酒单与按菜单排序的在售菜式，用于酒与主推菜推荐；多店须用户选择；禁止编造。
  English: Use MCP only (https://mcp.sipsiip.com/api/sippai) to search Sippai restaurants, then fetch bottle/glass wine menus and menu-sorted dishes for wine and featured-dish suggestions; require user disambiguation when multiple stores match; never fabricate prices or items.
license: MIT
homepage: https://sipsiip.com/ai/getwinefood
author: sipsiip
requires_api_key: conditional
category: productivity
tags: [wine, food, restaurant, sippai, mcp, api-mcp-only, featured-dish, bottle, glass, wine-list, sipsiip]
---

# Sippai 门店美酒与菜式

**一句话**：智能体**只**通过 **MCP** 工具完成「找店 → 瓶卖 / 杯卖酒单 → 菜式排序 → **酒 + 主推菜**推荐」；**对外只使用下文唯一网关**。门店检索、酒单与菜式等业务能力由 **Sippai 后端工程 `api/sippai`** 实现，经 MCP 网关对外暴露工具。

## 对外地址（唯一）

| 用途 | URL |
|------|-----|
| **聚合网关前缀（本 skill 语境下唯一对外 API 域）** | **`https://mcp.sipsiip.com/api`** |
| **本 skill 默认 MCP 会话入口（与网关 `MCP_HTTP_MOUNT_PATH=/api/sippai` 一致）** | **`https://mcp.sipsiip.com/api/sippai`** |

- **远程宿主（HTTP / Streamable MCP）**：只配置、只告知 **`https://mcp.sipsiip.com/api/sippai`**（及其文档约定的子路径）；**不要**在 skill 或用户可见说明里再写其它域名或直连业务网关 URL。
- **本地调试**：可选用与线上一致的网关 URL；若在本机启动 MCP stdin/stdout 子进程联调仍须设置 `SIPPAI_BASE_URL` 与环境变量。**不要把**局域网或自建端口作为对外文档中的「官方数据入口」。

## 唯一入口（必读）

- **必须使用**：MCP 工具 `sippai_search_restaurants`、`sippai_get_restaurant_menus`（会话入口见上表）。
- **禁止**：在未经由 **`https://mcp.sipsiip.com/api`** 托管的 MCP、或未使用本 skill 所列工具的前提下，用其它 HTTP 入口获取同一批数据；禁止混用与本链路不一致的门店标识或解析方式。禁止向终端用户暴露「第二条」业务 API 基址。

## 能力概览

| 项目 | 说明 |
|------|------|
| 覆盖范围 | 已录入 Sippai 且状态正常的门店 |
| 数据内容 | 当前「正在使用」酒单下的瓶卖/杯卖酒款；在售菜品（`sort_order` 靠前可作主推候选） |
| **业务实现所在**（单仓后端） | **`api/sippai`**：检索餐厅、门店酒单、`/v1/c/restaurants/...` 菜品等均由该工程承载 |
| 对外接入形态 | MCP：`https://mcp.sipsiip.com/api/sippai` |
| 实时性 | 与门店生效酒单一致；以工具返回值为准 |
| 密钥 | 检索门店时后端可能校验集成密钥（与 **Sippai** 应用集成配置、`SIPPAI_MCP_API_KEYS` 等一致） |

## 工作流

```
用户：「半山腰有什么杯卖？再给几道主推菜。」
       ↓
Step 1: sippai_search_restaurants(keyword="半山腰")
       ↓
若 records 多条 → 列出 name/address，请用户选一个 restaurantId（UUID）
若仅一条 → 直接取 restaurantId
       ↓
Step 2: sippai_get_restaurant_menus(restaurantId=<选定 UUID>)
       ↓
从返回 JSON 中取：
  bottleWineMenu.records[]  —— 瓶卖
  glassWineMenu.records[]   —— 杯卖
  dishesSoldOrderedByRestaurantMenuSort.records[] —— 主推菜候选（仅用返回字段做搭配话术）
```

### 行为规则

1. **`restaurantId`（UUID）** 仅能通过 **`sippai_search_restaurants`** 取得后再调 `sippai_get_restaurant_menus`。禁止用其它体系的门店编号、租户类标识或非 MCP 提供的解析接口顶替。
2. **检索命中多家店** → 必须让用户选一。
3. **回答**只用工具返回字段；缺的写「接口未返回」；**绝不编造**。
4. **杯卖 / 瓶卖** 分别从 `glassWineMenu` / `bottleWineMenu` 读取。
5. **主推菜**：优先 `sort_order` 较小的在售菜；勿夸大未在数据中的背书。
6. **酒 + 菜**：搭配话术必须锚定在已返回的菜名与酒款上。

## 工具约定

宿主通过 **Model Context Protocol** 连接 **`https://mcp.sipsiip.com/api/sippai`**（或本机等价联调会话）。工具行为应与 **`api/sippai`** 已实现接口一致：**门店检索**与 **酒单、菜式**数据来源均为该后端；网关按 MCP 协议封装，宿主不要用 curl 绕过 MCP 自行拼 REST。

**运维与密钥**：`sip.sippai.integration`、`SIPPAI_MCP_API_KEYS`、`SIPPAI_BASE_URL` 等以服务部署与 **`api/sippai`** 应用配置为准，**不属于**向终端读者展开的 skill 正文。

## 宿主侧配置要点（远程）

- **MCP URL**：`https://mcp.sipsiip.com/api/sippai`（认证方式以服务交付说明为准）。
- **不要**在 Cursor / SkillHub / 其它宿主配置里填写其它 API 根路径来获取同一批数据。

**本机 stdio（仅开发）**：须 `MCP_TRANSPORT=stdio`，并为本机 MCP 网关进程配置与后端可互通的 **`SIPPAI_BASE_URL`**；勿把该类地址当作对外公开的「官方数据入口」写入用户文档。

## 使用示例（上架与检索所需）

以下示例说明**工具调用顺序**；宿主须已配置 MCP 指向 `https://mcp.sipsiip.com/api/sippai`（或等价），并按交付方要求配置检索密钥（若启用）。

### 示例 1：店名 → 杯卖 + 主推菜

1. 用户：「XX 餐厅有什么杯卖？推荐几道你们的主打菜。」
2. 调用 `sippai_search_restaurants`，`keyword` 填用户说的店名（或地址关键词）。
3. 若返回多条记录：列出 `name`、`address`，请用户选定一家，取得其 `restaurantId`（UUID）。
4. 调用 `sippai_get_restaurant_menus`，`restaurantId` 为上一部选定值。
5. 回答：从 `glassWineMenu` 概括杯卖；从 `dishesSoldOrderedByRestaurantMenuSort` 取排序靠前若干道作为主推候选；**仅使用返回字段**，缺项写「接口未返回」。

### 示例 2：仅问瓶卖

1. 用户：「这家店瓶卖酒单有哪些？」（已能确定唯一门店时仍须先有 `restaurantId`。）
2. `sippai_search_restaurants` → 必要时让用户选店 → `sippai_get_restaurant_menus`。
3. 从 `bottleWineMenu` 组织回答。

## 仓库与实现

| 路径 | 说明 |
|------|------|
| **`api/sippai`** | **Sippai 后端**。本 skill 用到的能力在此实现：例如 **`/v1/sippai/restaurants/search`**（供集成/MCP 先检索门店）、**`/v1/c/restaurants/{id}/wine-list`、`/dishes`** 等菜品与酒单数据。宿主侧仍 **只经由** **`https://mcp.sipsiip.com/api/sippai`** 的 MCP 工具访问，不向用户暴露直连后端的拼装 URL。
