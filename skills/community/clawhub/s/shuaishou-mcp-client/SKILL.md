---
name: htyd-mcp-client-streamable
description: Builds and uses an MCP client (Streamable HTTP transport) to connect to the htyd MCP server and invoke all available tools (including login). Use when connecting to a Streamable HTTP MCP endpoint like https://dz.shuaishou.com/mcp. This is the production version.
---

# HTYD MCP Client (Streamable HTTP) - Production

## Goal

Provide an **MCP client-first** wrapper for MCP servers exposed via **Streamable HTTP** transport (`/mcp`). This is intended for hosts (e.g. OpenClaw) that **do not support MCP connections natively**: install a tiny Node client and use it to **list/call all MCP tools**, including **login**.

**这是正式生产环境版本**，连接 `https://dz.shuaishou.com/mcp`。

Default endpoint:

- `MCP_URL=https://dz.shuaishou.com/mcp`
- `MCP_APP_KEY=<your_app_key>` (sent as `Authorization: Bearer ...`)

## Quick start (OpenClaw / any shell)

1) 确保 MCP 服务可访问（生产环境：`https://dz.shuaishou.com/mcp`）。

2) 安装依赖（如需要）:

```bash
cd "%USERPROFILE%\.agents\skills\htyd-mcp-client-streamable-0.1.0\scripts"
npm install
```

3) 列出工具：

```bash
node htyd-mcp.mjs tools
```

4) 调用工具：

```bash
node htyd-mcp.mjs call list_shops "{}"
node htyd-mcp.mjs call list_collected_goods "{\"claimStatus\":0,\"pageNo\":1,\"pageSize\":50}"
```

5) 登录（部分流程需要）:

```bash
node htyd-mcp.mjs login_shuashou --username "YOUR_USER" --password "YOUR_PASS" --loginType "pd"
```

6) 采集商品：

```bash
node htyd-mcp.mjs collect_goods --originList "https://detail.1688.com/offer/xxx.html"
```

7) 认领商品到店铺：

```bash
node htyd-mcp.mjs claim_goods --itemIds 35476703,35476704 --platId 68 --merchantIds 2025050918
```

**推荐使用 `--originList` 替代 `--itemIds`**，客户端会自动从已采集商品中筛选可认领的（采集成功、非重复采集、非采集中）。

示例（推荐）：

```bash
node htyd-mcp.mjs claim_goods --originList "https://detail.1688.com/offer/xxx.html" --platId 68 --merchantIds 2025050918
```

8) 一键采集+认领+发布：

```bash
node htyd-mcp.mjs collect_and_publish --originList "https://detail.1688.com/offer/xxx.html" --platId 68 --merchantIds 2025050918 --pubShops 2025050918
```

此命令执行：采集 → 认领 → 查询草稿 → 发布。

**默认会跟踪发布结果**，通过 `list_publish_records` 轮询直到 SUCCESS/FAIL：

```bash
node htyd-mcp.mjs collect_and_publish --originList "https://detail.1688.com/offer/xxx.html" --platId 68 --merchantIds 2025050918 --pubShops 2025050918 --timeoutSec 180 --intervalSec 3
```

跳过结果跟踪（仅发送发布请求）：

```bash
node htyd-mcp.mjs collect_and_publish --originList "https://detail.1688.com/offer/xxx.html" --platId 68 --merchantIds 2025050918 --pubShops 2025050918 --track false
```

如果发布失败，客户端会打印**错误信息**，并建议到**甩手店长**后台修正商品信息后重新发布。

8.1) 仅发布并跟踪（适用于已有草稿 itemIds）：

```bash
node htyd-mcp.mjs publish_and_track --itemIds 1306795 --pubShops 2025050918 --timeoutSec 180 --intervalSec 3
```

## 业务流程说明

### 闭环1：采集 → 认领（到草稿箱）

仅完成商品采集并认领到指定店铺，停留在草稿箱状态，不自动发布。

```bash
# Step 1: 采集
node htyd-mcp.mjs collect_goods --originList "https://detail.1688.com/offer/xxx.html"

# Step 2: 认领（认领到草稿箱）
node htyd-mcp.mjs claim_goods --originList "https://detail.1688.com/offer/xxx.html" --platId 68 --merchantIds 2025050918
```

### 闭环2：采集 → 认领 → 发布（一站式）

用户提供一个链接，完成采集、认领、发布的完整闭环，**默认会跟踪发布结果**。

```bash
node htyd-mcp.mjs collect_and_publish \
  --originList "https://detail.1688.com/offer/730708656407.html" \
  --platId 68 \
  --merchantIds 2025050918 \
  --pubShops 2025050918
```

#### 参数说明

- `--originList` (必填) - 商品链接，支持多个
- `--platId` (必填) - 平台ID，如 68 代表 Temu
- `--merchantIds` (必填) - 认领目标店铺ID列表
- `--pubShops` (可选) - 发布店铺ID列表，不传则默认使用 merchantIds 第一个
- `--track` (可选) - 是否跟踪发布结果，默认 `true`
- `--timeoutSec` (可选) - 跟踪超时时间（秒），默认 180 秒
- `--intervalSec` (可选) - 轮询间隔（秒），默认 3 秒

#### 执行流程（6步闭环）

```
[1/6] collect_goods                    → 调用采集接口
[2/6] list_collected_goods             → 查询采集结果，获取 itemId
[3/6] claim_goods                      → 认领到指定店铺
[4/6] list_temu_drafts                 → 查询草稿箱定位商品
[5/6] publish_temu                     → 调用发布接口
[6/6] list_publish_records_by_item_id  → 轮询查询发布结果
```

#### 草稿箱商品定位策略

1. 店铺限定：只查询目标店铺
2. 状态限定：只查未发布状态（`status=UNPUBLISH`）
3. 时间排序：按认领时间倒序
4. 链接匹配：匹配原始 URL

#### 重要说明

- **一个商品可多次发布**：同一 itemId 可能有多条发布记录，系统自动取**最新**的那条判断状态
- 如需跳过结果查询，添加 `--track false`

#### ⚠️ 平台限制说明

**当前发布功能（publish_temu）仅支持 Temu（拼多多）店铺，不支持其他平台！**

| 工具/命令 | 支持的平台 |
|-----------|-----------|
| `collect_goods` | 1688、淘宝、天猫等（采集） |
| `claim_goods` | 所有支持的目标店铺（认领到草稿箱） |
| `list_temu_drafts` | **仅 Temu** |
| `publish_temu` | **仅 Temu** |
| `collect_and_publish` | **仅 Temu**（一键发布） |
| `publish_and_track` | **仅 Temu** |

**如果用户要求发布到天猫、京东、抖音等其他平台**：
- ❌ 不要使用 `publish_temu` / `collect_and_publish` / `publish_and_track`
- ✅ 只执行到 `claim_goods` 步骤（认领到目标店铺的草稿箱）
- ✅ 告知用户：目前自动发布功能仅支持 Temu 店铺，其他平台需要手动在**甩手店长**后台发布

**platId 参考**：
- `68` = Temu（目前唯一支持自动发布的平台）

**默认发布设置**（用户未指定时自动生效）：
- `isTitleCut=true` - 自动截取标题（避免超长导致失败）
- `titleCutType=0` - 取标题最前面的部分（含核心关键词）
- `isFilterPsoriasisImg=true` - 自动过滤牛皮癣图片
- `uploadDetail=true` - 上传详情信息
- `bindWordRule=IGNORE` - 忽略敏感词直接发布
- `randomImage=false` - 不打乱图片顺序
- `videoUpload=false` - 不上传视频
- `scheduledPublish=false` - 立即发布（非定时）

9) Query publish records by itemId (根据商品itemId查询发布记录，对应接口 `/api/pdd/record/list_by_item_id`):

```bash
node htyd-mcp.mjs call list_publish_records_by_item_id "{\"ids\":[1306795,1306796]}"
```

- `ids` (required): 商品ID列表，支持多个itemId，返回结果按itemId顺序排列
- **一个商品可多次发布**：同一 itemId 可能对应多条发布记录（例如重复发布），系统会自动取**发布时间最新**的那条记录
- 返回字段: `id`, `itemId`, `title`, `status`, `productId`
- `status` 可能值: `SUCCESS`/`FAIL`/`PUBLISHING`

## Tool coverage (current `user-htyd-mcp`)

This wrapper is expected to expose **all current tools**:

- `login_shuashou` (required)
- `list_shops`
- `collect_goods`
- `list_collected_goods`
- `claim_goods`
- `list_temu_drafts` (new)
- `publish_temu` (new)
- `list_publish_records_by_item_id` (根据itemId查询发布记录，对应接口 POST /api/pdd/record/list_by_item_id。一个商品可多次发布，取最新记录)

Convenience command:
- `collect_and_publish` - One-step collect → claim → publish workflow

If new tools are added server-side later, use `tools` to discover them and call them via `call`.

## Configuration

Environment variables:

- `MCP_URL` (optional): MCP endpoint URL. Default `https://dz.shuaishou.com/mcp`.
- `MCP_APP_KEY` (optional): AppKey (sent as `Authorization: Bearer ...`).
- `MCP_AUTHORIZATION` (optional): Full Authorization header value; overrides `MCP_APP_KEY`.

首次运行 / 缺少 API Key：

- 如果未设置 `MCP_APP_KEY`/`MCP_AUTHORIZATION`（或加载失败返回 401/403），客户端会交互式提示输入
- 配置值会保存到 `~/.htyd-mcp-client-streamable.json`，下次自动复用

## 环境配置

环境变量：

- `MCP_URL`（可选）：MCP 端点 URL。默认 `https://dz.shuaishou.com/mcp`
- `MCP_APP_KEY`（可选）：AppKey（作为 `Authorization: Bearer ...` 发送）
- `MCP_AUTHORIZATION`（可选）：完整的 Authorization header 值；优先级高于 `MCP_APP_KEY`

临时覆盖 endpoint：

```bash
# 连接其他环境
MCP_URL=https://other-server.com/mcp node htyd-mcp.mjs tools
```

## 操作流程

使用 MCP 工具时：

1. 运行 `tools` 验证连接
2. 如需认证，先调用 `login_shuashou`
3. 然后调用业务工具（`list_shops`、`collect_goods`、`list_collected_goods`、`claim_goods`）

