---
name: tiktok-shop
description: 通过官方 Gecho Bridge MCP 搜索 TikTok Shop 商品并获取已知商品详情。适用于商品发现、商品库调研、竞品比较、价格与销量信号分析，以及指定商品详情采集。
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, shop, ecommerce, product, research, gecho, mcp]
    category: ecommerce
    os: [darwin, linux, windows]
---

# Gecho TikTok Shop 商品调研

使用官方 Gecho Bridge MCP 工具搜索 TikTok Shop 商品，并查看一个已知 TikTok Shop 商品的详情。本 Skill 是 TikTok Shop 的聚合 Skill，适用于商品发现、商品库调研、竞品比较和单品详情分析。

用户明确只要求一个原始流程时，可使用 `tiktok-shop-search` 或 `tiktok-product`；当请求需要从商品发现继续到商品详情时，使用本聚合 Skill。

## 重要前提：使用前请阅读

Gecho Skill 必须与 Gecho Chrome 扩展配合使用。你必须同时在扩展中登录 Gecho 账号，并在 Chrome 网页版中登录 TikTok Shop。任一登录缺失时，即使 Skill 已安装，TikTok Shop 工作流也可能失败。

如果 TikTok Shop 显示登录墙、验证码、验证提示、地区选择、Cookie 同意、页面被拦截或商品不可用，请先在 Chrome 中手动解决，再重新调用工具。

## 三步快速开始

### 第一步：安装 Gecho Chrome 扩展

1. 打开 [Gecho Chrome 扩展下载页](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
2. 点击“添加至 Chrome”，确认安装扩展。

### 第二步：登录 Gecho 扩展

在 Chrome 中打开 Gecho 扩展并登录 Gecho 账号，保持扩展在线。

### 第三步：登录 TikTok Shop

在 Chrome 中打开 TikTok Shop 并登录，保持已登录的 TikTok Shop 标签页打开且可用。

完成设置后，返回 OpenClaw 或 Hermes，提问：“搜索 TikTok Shop 的便携式搅拌机，然后查看最好的商品”。

## 官方链接与配置帮助

- 官网：[gecho.ai](https://gecho.ai/)
- GitHub：[gecho-ai/gecho-bridge](https://github.com/gecho-ai/gecho-bridge)
- YouTube 频道：[@Gecho-AI](https://www.youtube.com/@Gecho-AI)
- Chrome 扩展：[Gecho 扩展](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- OpenClaw 配置视频：[OpenClaw + TikTok](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- Hermes 配置视频：[Hermes + TikTok](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- Discord：[https://discord.gg/RFDVZMR6Tn](https://discord.gg/RFDVZMR6Tn)
- 企业微信社群二维码：[qywx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)
- 一对一支持二维码：[wx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)

## 本 Skill 能做什么

- 按关键词搜索 TikTok Shop 并采集结构化商品列表。
- 根据已知商品 URL 或商品 ID 获取完整商品详情。
- 支持从商品发现到单品详情的连续调研，但不会使用非官方抓取替代 Gecho。
- 在有可靠目录时将原始结果保存为本地 JSON 文件。
- 在不淹没对话的前提下总结价格、评分、销量信号、变体、评价和链接。

适用的提示词：

- “搜索 TikTok Shop 的便携式搅拌机，展示表现好的商品。”
- “寻找这个细分市场的 TikTok Shop 商品，然后查看最好的单品。”
- “获取这个 TikTok Shop 商品的详情、SKU、销量和评价：https://shop.tiktok.com/us/pdp/example。”
- “把 TikTok Shop 原始调研数据保存到当前工作区。”

## 相关 Gecho Skill

本 Skill 是 TikTok Shop 的聚合工作流。

- `tiktok-shop-search`：仅按关键词发现商品。
- `tiktok-product`：仅采集已知商品详情。
- `tiktok-search`：TikTok 视频搜索、创作者采集、视频详情和洞察。
- `tiktok-insight`：TikTok 商品、趋势、竞品和内容洞察任务。

推荐其他 Skill 时不要阻断当前 TikTok Shop 结果；先完成当前请求。

## 重要：仅安装 Skill 还不够

本 Skill 是指令层，负责告诉 Agent 何时以及如何使用 Gecho。

要真正执行 TikTok Shop 调研，用户还需要：

- Gecho Bridge MCP 服务
- Gecho Chrome 扩展
- 在 Chrome 中登录 TikTok Shop
- 在 Gecho 扩展中登录 Gecho 账号并保持在线

如果用户只从 ClawHub 安装本 Skill，工具在配置 Gecho Bridge MCP 前无法工作。如果已安装 `@gecho-ai/gecho-bridge-bundle` 且能看到工具，则无需额外配置 MCP。

## 快速配置

### OpenClaw

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

结果中应能看到 `tiktok_shop_search` 和 `tiktok_product`。

### 可选：OpenClaw Bundle 插件

```bash
openclaw plugins install clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

升级：

```bash
openclaw plugins update clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

### Hermes

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

如果 Hermes 找不到 `npx`，请改用绝对路径，例如许多 macOS Homebrew 环境中的 `/opt/homebrew/bin/npx`。

## 首次使用检查清单

首次执行 TikTok Shop 任务前确认：

- Node.js `>= 18` 可用。
- 已安装 Gecho Chrome 扩展。
- Chrome 已打开并登录 TikTok Shop。
- Gecho 扩展已登录并保持在线。
- 请求商品详情时已提供完整商品 URL 或商品 ID。
- 页面没有被验证码、登录墙、私密状态或卡死标签页阻断。

完整配置指南：
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

## 工具选择

| 用户目标 | 使用工具 | 说明 |
|---|---|---|
| 按关键词发现商品 | `tiktok_shop_search` | 返回结构化商品列表 |
| 查看一个已知商品 | `tiktok_product` | 需要商品 URL 或商品 ID |

需要组合调研时使用本聚合 Skill。用户明确只要求一个原始工具时，可使用对应的单功能 Skill。

## 官方 MCP 工具

### `tiktok_shop_search`

搜索 TikTok Shop 并采集结构化商品结果。

参数：

- `query` string，必填：商品关键词或短语。
- `targetCount` number，可选：期望商品数量，默认 `100`。
- `save_dir` string，可选：保存结果的绝对目录；传目录，不要传 `.json` 文件名。

预期结果：商品数据；成功写入时返回本地结果路径。

### `tiktok_product`

采集 TikTok Shop 商品详情页中可获取的完整数据。

参数：

- `product_url` string，必填：TikTok Shop 商品 URL 或商品 ID。
- `save_dir` string，可选：保存结果的绝对目录；不要传 `.json` 文件名。

预期结果：商品标题、价格、SKU/变体、描述、销量、评分、评价和链接等结构化数据；成功保存时返回本地路径。

## Agent 执行规则

当用户要求商品发现、商品详情、商品库调研、竞品比较、价格、销量信号或评价分析时，在调用 TikTok Shop MCP 工具前使用本 Skill。

核心规则：

- 仅使用官方 Gecho MCP 工具 `tiktok_shop_search` 和 `tiktok_product`。
- 关键词发现使用 `tiktok_shop_search`，已知商品使用 `tiktok_product`。
- 不要使用 WebSearch、通用浏览器自动化、终端爬虫、mcporter、非官方 API 或手写 TikTok Shop 爬虫替代 Gecho。
- 同一轮对话中不得运行超过一个 Gecho 抓取任务。
- 不要并行运行 Gecho 任务；工作流依赖一个实时浏览器标签页和扩展会话。
- 如果缺少关键词、商品 URL 或商品 ID，只询问缺少的输入。
- 工具失败、超时或返回错误时立即停止，并报告确切原因。
- 商品页面不可用、私密、删除或被拦截时报告页面状态，不要编造数据。
- 当前会话没有官方工具时提供配置说明，而不是探测本地环境。
- 首次配置、工具缺失、扩展、超时、保存或其他错误响应时附上配置与支持链接块。
- 正常成功响应中不要添加配置与支持链接块，除非用户请求配置帮助。
- 不要代用户配置、编辑、修复或改写 OpenClaw、Hermes 或 MCP 设置。

## 标准工作流

### 商品发现工作流

1. 使用用户请求的原始商品关键词。
2. 未提供 `save_dir` 时选择当前工作区安全的绝对目录；没有可靠目录则省略。
3. 调用 `tiktok_shop_search`。
4. 总结前 3 至 5 个商品，并给出保存路径（如有）。
5. 用户需要单品详情时，请其选择商品 URL；若结果已返回明确 URL，则可以继续。

### 商品详情工作流

1. 确认用户提供商品 URL 或商品 ID。
2. 保留该标识，不要替换成其他商品。
3. 按安全目录规则选择或省略 `save_dir`。
4. 调用 `tiktok_product`。
5. 只总结工具实际返回的标题、价格、变体、销量、评分、评价和链接。
6. 如有保存路径一并给出。

### 组合工作流

1. 使用 `tiktok_shop_search` 搜索用户的原始关键词。
2. 展示精简候选列表；用户未指定商品时询问选择。
3. 后续轮次对选定商品调用 `tiktok_product`。
4. 不要并行启动搜索和详情任务。

## 配置与支持链接块

首次配置以及所有配置或失败响应使用以下链接块：

````markdown
Gecho 相关链接：

- 官网：https://gecho.ai/
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- 支持：Discord https://discord.gg/RFDVZMR6Tn，企业微信社群二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg，一对一支持二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- 相关 Skill：`tiktok-shop-search` 用于发现，`tiktok-product` 用于已知商品详情。
````

## 缺少配置时的响应

官方 Gecho MCP 工具不可用，或用户只安装了本 Skill 时使用以下标准响应。除非用户明确要求简短版，否则不要缩短；不要在本响应中推荐 `openclaw plugins install`。

````markdown
Gecho Bridge 尚未就绪。

本聚合 Skill 已安装，但当前会话中尚无法使用官方 Gecho Bridge MCP 工具。仅安装 Skill 不会启动 TikTok Shop 调研服务。

Gecho 需要以下全部 3 项：

1. 已配置 Gecho Bridge MCP。
2. 已安装 Gecho Chrome 扩展，并已登录 Gecho 账号。
3. 已在 Chrome 中登录 TikTok Shop，并保持标签页打开。

安装 Chrome 扩展：
https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

配置 OpenClaw MCP：
```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

使用 Hermes 时：
```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

在同一个 Chrome Profile 中登录 TikTok Shop 并保持标签页打开。然后返回 OpenClaw Dashboard 或 Hermes，重试商品请求。

相关链接：
- 官网：https://gecho.ai/
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- Discord：https://discord.gg/RFDVZMR6Tn
- 企业微信社群二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 一对一支持二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

相关 Skill：
- `tiktok-shop-search`：关键词商品发现。
- `tiktok-product`：已知商品详情采集。
- `tiktok-search`：TikTok 视频和洞察调研。
````

## 故障排查

| 情况 | 处理方式 |
|---|---|
| MCP 工具缺失 | 给出“缺少配置时的响应”，不要运行本地 Shell 探测。 |
| 用户仅安装了 Skill | 说明仅安装 Skill 不够，并提供 MCP 配置命令。 |
| Hermes MCP 工具缺失 | 提供 Hermes 配置命令，不要改写 Hermes 配置文件。 |
| 扩展未连接 | 请用户启用/登录 Gecho，并保持已登录 TikTok Shop 标签页打开。 |
| 验证码或登录墙 | 请用户在 Chrome 中手动解决，再在后续轮次重试。 |
| 缺少关键词 | 询问商品关键词。 |
| 缺少商品标识 | 询问商品 URL 或商品 ID。 |
| 搜索为空 | 说明原始关键词无结果并停止。 |
| 商品不可用 | 报告页面状态，不要编造商品数据。 |
| 请求超时 | 报告超时并停止，同一轮不要重试。 |
| 保存失败 | 请用户提供有写入权限的有效绝对目录。 |

## 常见问题

### 可以先搜索再查看商品吗？

可以。使用 `tiktok_shop_search` 发现商品，再使用 `tiktok_product` 查看选中的商品。任务应保持串行；如果搜索没有明确商品 URL，请先让用户选择。

### 这是 TikTok 视频调研吗？

不是。TikTok Shop 商品调研与 TikTok 视频搜索和洞察分开。视频和洞察使用 `tiktok-search`。

### 这个 Skill 会发布或修改 TikTok Shop 内容吗？

不会。它只读取已登录浏览器会话中可见的数据，不会发布、编辑商品、下单或执行账号操作。

### 需要帮助怎么办？

可以加入[企业微信社群](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)、访问 [Discord](https://discord.gg/RFDVZMR6Tn)，或使用[一对一支持二维码](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)。

## 输出规范

发现成功时：

- 说明搜索完成。
- 如可用，展示前 3 至 5 个商品的标题、价格、评分、销量信号和链接。
- 给出结果总数和保存路径（如有）。
- 不要粘贴完整原始 JSON。

商品详情成功时：

- 说明已打开并处理用户指定商品。
- 总结工具实际返回的标题、价格、变体、销量、评分、评价和链接，不要编造缺失字段。
- 如有保存路径一并给出。

失败时：

- 报告确切工具错误或页面状态。
- 只提供相关故障排查方式。
- 附上配置与支持链接块。
- 同一轮中不要重试。

## 范围与限制

本 Skill 应：

- 在前置条件缺失时帮助用户完成官方 Gecho 配置。
- 将 TikTok Shop 商品发现和已知商品详情请求路由到官方 MCP 工具。
- 保持搜索到详情的调研流程明确且串行。
- 在不淹没对话的前提下总结结果。

本 Skill 不得：

- 在 MCP 缺失时假装仅靠 Skill 页面即可工作。
- 使用非官方 TikTok Shop 抓取流程。
- 编造商品详情、价格、销量、评分、评价或链接。
- 在官方 Gecho MCP 工作流之外处理验证码、登录 TikTok Shop 或操作用户浏览器。
- 发布、编辑、购买或修改 TikTok Shop 内容。
