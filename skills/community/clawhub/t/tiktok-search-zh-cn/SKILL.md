---
name: tiktok-search
description: 通过 Gecho Bridge MCP 搜索 TikTok 视频、采集创作者视频、获取指定视频详情与评论，并开展商品、趋势、竞品与内容洞察。需要安装 Gecho Chrome 扩展、保持有效的 TikTok 登录会话，并配置 Gecho Bridge MCP 服务。
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, search, insight, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# Gecho TikTok 搜索与洞察

在 AI 对话中搜索 TikTok、采集结构化视频元数据，并通过官方 Gecho Bridge MCP 工作流发起异步的商品或趋势洞察任务。

这是 Gecho 默认的 TikTok 聚合 Skill，涵盖 TikTok 视频搜索、创作者视频采集、单条视频详情与评论采集及 TikTok 洞察。为便于分发和搜索流量，也可能提供单工具 TikTok Skill；但对于需要完整 TikTok 调研工作流的用户，本 Skill 是推荐的默认选择。

## 重要前提：使用前请阅读

Gecho Skill 必须与 Gecho Chrome 扩展配合使用。你必须同时在扩展中登录 Gecho 账号，并在 Chrome 网页版中登录 TikTok。即使已经安装本 Skill，只要任一登录缺失，所有 TikTok 搜索和洞察功能都可能失败。

## 三步快速开始

### 第 1 步：安装 Gecho Chrome 扩展

1. 打开 [Gecho Chrome 扩展下载页](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
2. 点击 `Add to Chrome`，然后确认 `Add extension`。

### 第 2 步：登录 Gecho 扩展

在 Chrome 中打开 Gecho 扩展，登录你的 Gecho 账号，并保持扩展在线。

### 第 3 步：登录 TikTok 网页版

在 Chrome 中打开 TikTok 网页版并登录，使用期间请保持已登录的 TikTok 标签页打开。

完成设置后，返回 OpenClaw Dashboard 或 Hermes，并直接提问："在 TikTok 搜索 xxx"。例如："在 TikTok 搜索汉堡"。

## 官方链接与配置帮助

- 官网：[gecho.ai](https://gecho.ai/)
- GitHub：[gecho-ai/gecho-bridge](https://github.com/gecho-ai/gecho-bridge)
- YouTube 频道：[@Gecho-AI](https://www.youtube.com/@Gecho-AI)
- Chrome 扩展：[Gecho 扩展](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- OpenClaw 配置视频：[OpenClaw + TikTok：通过 Gecho Bridge 直接控制 AI 浏览器](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- Hermes 配置视频：[Hermes + TikTok：通过 Gecho Bridge 直接控制 AI 浏览器](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- Discord：[https://discord.gg/RFDVZMR6Tn](https://discord.gg/RFDVZMR6Tn)
- 企业微信社群二维码：[qywx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)
- 一对一支持二维码：[wx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)

## 本 Skill 能做什么

- 查找某个关键词下表现优异的 TikTok 视频。
- 采集标题、作者、互动数据和视频链接。
- 根据已知 TikTok 视频 URL 获取视频详情、评论和回复。
- 将完整原始结果集保存为本地 JSON 文件。
- 为商品调研、竞品分析和趋势发现发起异步洞察任务。

适用的提示词：

- “在 TikTok 搜索便携式搅拌机，展示点赞最高的视频。”
- “寻找猫玩具视频中表现好的开场钩子。”
- “针对户外野餐垫做商品机会洞察。”
- “查看我上一个 TikTok 洞察任务的状态。”
- “获取这个 TikTok 视频的详情和评论：https://www.tiktok.com/@user/video/123。”

## 重要：仅安装 Skill 还不够

本 Skill 是指令层，用于告诉 AI 在何时、如何使用 Gecho。

要真正执行 TikTok 搜索、视频详情采集或洞察任务，用户还需要：

- Gecho Bridge MCP 服务
- Gecho Chrome 扩展
- 在 Chrome 中登录 TikTok
- 在 Gecho 扩展中登录 Gecho 账号并保持在线

如果用户只在 ClawHub 安装了本 Skill，在配置 Gecho Bridge MCP 服务前，搜索无法运行。此时请使用下方的 MCP 配置方式。

已经安装 Gecho Bridge？如果已安装 `@gecho-ai/gecho-bridge-bundle`，且可以看到 Gecho MCP 工具，本 Skill 无需额外配置 MCP。

## 快速配置

### OpenClaw Skill 安装：配置 MCP

若本 Skill 已安装在 OpenClaw 中，请一次性配置 Gecho Bridge MCP 服务：

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
```

然后验证：

```bash
openclaw mcp list
```

### 可选：OpenClaw Bundle 插件

若用户尚未安装本 Skill，且偏好使用插件管理，可通过 Bundle 插件安装已配置 MCP 条目的 Gecho：

```bash
openclaw plugins install clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

后续升级：

```bash
openclaw plugins update clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

### Hermes 配置

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

若 Node.js 已安装但 Hermes 找不到 `npx`，请使用 `npx` 的绝对路径。很多 macOS Homebrew 环境的路径为：

```bash
hermes mcp add gecho-bridge --command /opt/homebrew/bin/npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

## 首次使用检查清单

第一次搜索前，请确认：

- 已安装 Node.js `>= 18`。
- 已安装 [Gecho Chrome 扩展](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
- Chrome 已打开，且已登录 TikTok。
- Gecho 扩展已登录 Gecho 账号并保持在线。
- TikTok 标签页未被验证码、登录墙或页面卡死阻断。

完整配置指南：
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

视频和支持链接请见上方“官方链接与配置帮助”。

## 工具选择

| 用户目标 | 使用工具 | 说明 |
|---|---|---|
| 搜索 TikTok 视频并采集元数据 | `tiktok_search` | 直接返回结果 |
| 获取已知视频的详情、评论和回复 | `tiktok_video` | 需要 TikTok 视频 URL |
| 采集某位 TikTok 创作者的视频 | `tiktok_influencer` | 使用创作者的 `uniqueId` |
| 分析细分赛道、商品、趋势或竞品机会 | `tiktok_insight` | 发起异步任务并返回 `jobId` |
| 查询已有的异步洞察任务 | `check_insight_status` | 使用 `tiktok_insight` 返回的 `jobId` |

对于广泛的 TikTok 调研需求，使用这个聚合 Skill。如果用户明确只要求一个原始工具，例如“运行 tiktok_video”，且对应的单工具分发 Skill 可用，则可以改用该单工具 Skill。

## 官方 MCP 工具

### `tiktok_search`

根据关键词搜索 TikTok，通过 Gecho 浏览器扩展滚动页面，返回结构化元数据，并保存完整结果集。

参数：

- `query` string，必填：搜索关键词或短语。
- `targetCount` number，可选：期望结果数；默认 `100`。
- `save_dir` string，可选：保存结果的绝对目录路径。不要传入 `.json` 文件名。如果无法获得可靠的绝对目录，请省略该参数。

预期结果：

- 视频元数据的 JSON 数组；成功写入结果时还会返回本地保存文件路径。

### `tiktok_video`

获取 TikTok 视频详情和评论。工具会打开视频详情页、展开评论区，并持续下滑采集评论及回复。

参数：

- `url` string，必填：TikTok 视频详情页 URL，例如 `https://www.tiktok.com/@user/video/123...`。
- `targetCount` number，可选：最多采集的评论及回复数量，默认值和上限都是 `200`。
- `save_dir` string，可选：保存结果的绝对目录；不要传 `.json` 文件名。没有可靠绝对目录时省略。

预期结果：

- 结构化视频详情、评论和回复数据；成功保存时还会返回本地结果文件路径。

### `tiktok_influencer`

采集某位 TikTok 创作者发布的视频。

参数：

- `uniqueId` string，必填：创作者的 TikTok `uniqueId`（例如 `zachking`）。
- `targetCount` number，可选：期望视频数；默认 `100`。请求数量请保持在 `500` 及以下。
- `save_dir` string，可选：保存结果的绝对目录路径。不要传入 `.json` 文件名。如果无法获得可靠的绝对目录，请省略该参数。

### `tiktok_insight`

为商品、趋势或竞品调研发起异步 TikTok 洞察任务。

参数：

- `query` string，必填：搜索关键词、商品或品类短语。
- `save_dir` string，可选：保存结果的绝对目录路径。不要传入 `.json` 文件名。如果无法获得可靠的绝对目录，请省略该参数。

预期结果：

- 一个 `jobId`。必须在后续通过 `check_insight_status` 查询最终结果。

### `check_insight_status`

查询已有洞察任务的状态或最终结果。

参数：

- `jobId` string，必填：由 `tiktok_insight` 返回的任务 ID。

预期结果：

- `running`、`error` 或已完成的洞察数据。

## Agent 执行规则

当用户要求搜索 TikTok、查看指定视频、查找热门视频、分析竞品、采集 TikTok 元数据、发现爆款商品或研究关键词趋势时，在调用任何 Gecho TikTok MCP 工具前使用本 Skill。

核心规则：

- 仅使用官方 Gecho MCP 工具：`tiktok_search`、`tiktok_video`、`tiktok_influencer`、`tiktok_insight` 和 `check_insight_status`。
- 不要用 WebSearch、浏览器自动化、终端爬虫、mcporter、非官方 API 或手写 TikTok 爬虫替代 Gecho。
- 同一轮对话中不得发起超过一个 Gecho 抓取或洞察任务。
- 不得并行运行 Gecho 抓取任务，因为该工作流依赖一个实时浏览器标签页和扩展会话。
- 若工具失败、超时或返回错误，立即停止并报告确切失败原因。
- 若 `tiktok_search` 没有返回条目，不得自动改写、翻译、扩展关键词或重试。
- 用户要查看视频详情但未提供视频 URL 时，只询问具体 URL，不要猜测或静默改成关键词搜索。
- 视频为私密、删除、不可用或被拦截时，报告页面状态，不要编造详情或评论。
- 若 `tiktok_insight` 成功发起，报告 `jobId`，并说明用户需要稍后查询状态。
- 若 `check_insight_status` 显示任务仍在运行，告知用户等待后再查询。
- 若当前会话中没有官方 Gecho MCP 工具，提供配置说明，而不是探测本地环境。
- 在首次使用配置指引、MCP 工具缺失、扩展/会话问题、超时、保存失败或任何工具错误时，附上下面的“配置与支持链接块”。
- 正常的搜索或洞察成功响应中，不要添加“配置与支持链接块”，除非用户请求配置帮助。
- 不要代用户配置、编辑、修复或重写 OpenClaw/Hermes/MCP 设置。请提供配置命令，并要求用户在工具工作流之外自行执行或批准执行。
- 不要把本 Skill 用于 TikTok Shop、X/Twitter、Amazon 或其他平台工作流；这些平台应有各自的 Gecho 聚合 Skill。

允许的状态查询行为：

- 用户可以明确要求查询一个已有的 `jobId`；此时只调用一次 `check_insight_status`。
- 查询状态后，同一轮中不要发起新的 `tiktok_search` 或 `tiktok_insight` 任务；除非用户在后续轮次再次提出请求。

## 标准工作流

### 搜索工作流

1. 使用用户请求的原始关键词。
2. 若用户未提供 `save_dir`，在当前工作区选择一个安全的绝对目录路径。若没有可靠的绝对目录，则省略 `save_dir`，让 Gecho 使用默认数据目录。
3. 调用 `tiktok_search`。
4. 若结果为空，说明该原始关键词未返回结果并停止。
5. 若存在结果，仅总结前 3 至 5 条，并给出保存文件路径。

### 视频详情工作流

1. 确认用户提供了 TikTok 视频详情页 URL，通常包含 `/video/`。
2. 保留用户提供的 URL，不要替换成其他视频。
3. 未提供 `save_dir` 时，在当前工作区选择安全的绝对目录；没有可靠目录则省略，让 Gecho 使用默认目录。
4. 将 URL、必要时限制后的 `targetCount` 和可靠的 `save_dir` 传给 `tiktok_video`。
5. 等待单个任务完成，不要并行运行其他 Gecho 抓取任务。
6. 总结视频详情和代表性评论、回复，有保存路径时一并给出。

### 洞察工作流

1. 使用用户请求的原始商品、细分赛道或关键词。
2. 若用户未提供 `save_dir`，在当前工作区选择一个安全的绝对目录路径。若没有可靠的绝对目录，则省略 `save_dir`，让 Gecho 使用默认数据目录。
3. 调用 `tiktok_insight`。
4. 报告返回的 `jobId`。
5. 告知用户任务可能需要数分钟，并应稍后通过 `check_insight_status` 查询。

### 状态查询工作流

1. 使用提供的 `jobId` 调用 `check_insight_status`。
2. 若仍在运行，报告当前状态并建议等待约 60 秒。
3. 若已完成，总结关键发现并给出保存文件路径。
4. 若失败，报告确切错误并停止。

## 配置与支持链接块

在首次使用指引以及所有配置或失败响应中使用此精简区块。将其放在准确修复说明之后、回答末尾附近。

````markdown
Gecho 相关链接：

- 官网：https://gecho.ai/
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- 支持：Discord https://discord.gg/RFDVZMR6Tn，企业微信社群二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg，一对一支持二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
````

## 缺少配置时的响应

当官方 Gecho MCP 工具不可用，或用户只安装了 Skill、尚不能运行搜索时，使用本响应。

将以下模板作为标准的“缺少配置”响应。Agent 可以为匹配用户语言而翻译其中的表述，但除非用户明确要求简短版本，否则不得将其缩减为更短的检查清单。

必须保留的内容：

- 说明 Gecho Bridge MCP 尚未配置，仅有 Skill 无法运行 TikTok。
- 包含全部三项要求：配置 MCP、安装并登录 Gecho Chrome 扩展、登录 TikTok 网页版并保持标签页打开。
- 包含 OpenClaw MCP 配置命令和 `openclaw mcp list` 验证命令。
- 包含 Chrome 扩展链接。
- 包含完成配置后返回 OpenClaw Dashboard 或 Hermes 重试请求的说明。
- 包含所有相关链接：官网、OpenClaw 配置视频、Hermes 配置视频、YouTube 频道、GitHub/README、Discord、企业微信社群二维码和一对一支持二维码。
- 包含模板中列出的相关 Gecho Skill。
- 不要在该“缺少配置”响应中推荐 `openclaw plugins install`。

````markdown
Gecho Bridge 尚未就绪。

本 Skill 已安装，但当前会话中尚无法使用官方 Gecho Bridge MCP 工具。仅安装 Skill 并不会启动 TikTok 搜索服务。

在运行 TikTok 搜索、视频详情采集或洞察前，Gecho 需要具备以下全部 3 项：

1. 已配置 Gecho Bridge MCP。
2. 已安装 Gecho Chrome 扩展，并已登录 Gecho 账号。
3. 已在 Chrome 中登录 TikTok 网页版，并保持 TikTok 标签页打开。

请按以下首次配置步骤操作：

**1. 安装 Gecho Chrome 扩展**

Chrome 网上应用店：
https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

安装后，打开扩展并登录你的 Gecho 账号。

**2. 配置 Gecho Bridge MCP**

OpenClaw MCP 配置：

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
```

然后验证：

```bash
openclaw mcp list
```

Hermes 配置：

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

**3. 登录 TikTok 网页版**

在 Chrome 中打开 TikTok 并登录，使用期间请保持已登录的 TikTok 标签页打开。

配置完成后，返回 OpenClaw Dashboard 或 Hermes，再次发出请求，例如：
“在 TikTok 搜索电脑”，或提供完整 TikTok 视频 URL 获取详情。


**相关链接**

- 官网：https://gecho.ai/
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- Discord 支持：https://discord.gg/RFDVZMR6Tn
- 企业微信社群二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 一对一支持二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

**相关 Gecho Skill**

- `tiktok-video-search`：TikTok 视频搜索和元数据采集。
- `tiktok-video`：已知 TikTok 视频 URL 的详情、评论和回复采集。
- `tiktok-insight`：TikTok 商品、趋势、竞品和内容洞察任务。
- `tiktok-search`：完整的 TikTok 搜索与洞察工作流。
````

## 故障排查

| 情况 | 处理方式 |
|---|---|
| MCP 工具缺失 | 给出“缺少配置时的响应”。不要运行本地 Shell 探测。 |
| 用户仅安装了 Skill | 说明仅安装 Skill 不够，并提供 OpenClaw MCP 配置命令。 |
| Hermes MCP 工具缺失 | 提供 `hermes mcp add ...` 命令。不要检查或改写 Hermes 配置文件。 |
| 扩展未连接 | 请用户启用/登录 Gecho Chrome 扩展，并保持一个已登录的 TikTok 标签页打开。 |
| 缺少视频 URL | 询问具体 TikTok 视频详情页 URL；不要猜测，也不要未经用户要求切换到关键词搜索。 |
| 视频私密、删除或不可用 | 报告页面状态；如有需要请用户提供可访问的视频 URL。 |
| 验证码或登录墙 | 请用户在 Chrome 中手动解决，再在后续轮次重试。 |
| 请求超时 | 报告超时，说明页面卡住、网络或验证码可能是原因，然后停止。 |
| 搜索为空 | 说明原始关键词无结果，并由用户手动选择另一个关键词。 |
| 洞察仍在运行 | 报告运行状态，并建议约 60 秒后再次查询。 |
| 保存失败 | 请用户提供具有写入权限的有效绝对目录路径。 |

## 常见问题

### 为什么必须安装 Chrome 扩展？

Gecho 需要来自实时浏览器会话的平台数据。Chrome 扩展将 AI 工作流连接到用户已登录的 Chrome 会话；仅安装 Skill 无法访问 TikTok 视频、详情页或评论。

### 为什么必须登录 TikTok？可以不登录吗？

TikTok 会限制未登录用户访问。登录后，扩展才能访问当前浏览器会话中可用的视频、评论、互动数据和其他信号。Gecho 不会要求或收集 TikTok 密码、私人账号信息，也不会代用户发布内容。

### 这和 TikTok 视频搜索是同一个能力吗？

不是。`tiktok_search` 按关键词发现视频，`tiktok_video` 处理一个已知视频 URL，采集详情、评论和回复。用户只需要单一流程时，可使用对应的单功能 Skill。

### 需要帮助怎么办？

可以加入[企业微信社群](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)、访问 [Discord](https://discord.gg/RFDVZMR6Tn)，或扫描[一对一支持二维码](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)。

## 输出规范

搜索成功时：

- 说明搜索完成。
- 如可用则给出结果总数和保存路径。
- 仅展示前 3 至 5 条，不要粘贴完整原始 JSON。

视频详情采集成功时：

- 说明已打开并处理用户指定的 TikTok 视频。
- 总结可用的身份和互动字段，不要编造缺失值。
- 如可用，说明采集到的评论和回复数量。
- 展示有限的代表性评论，并给出保存路径（如有）。

洞察成功启动时：

- 说明洞察任务已启动。
- 给出 `jobId`。
- 说明稍后需要通过 `check_insight_status` 查询。

洞察完成时：

- 总结关键发现。
- 给出保存路径。
- 不要声称工具结果没有支持的结论。

失败时：

- 报告确切工具错误或页面失败状态。
- 只提供故障排查中相关的修复方式。
- 附上配置与支持链接块。
- 同一轮中不要重试。

## 范围与限制

本 Skill 应：

- 在前置条件缺失时帮助用户完成官方 Gecho 配置。
- 将 TikTok 搜索、视频详情和洞察请求路由至官方 Gecho MCP 工具。
- 保持搜索、视频详情、洞察和状态查询流程明确。
- 在不淹没对话的前提下总结结果。

本 Skill 不得：

- 在 MCP 缺失时假装仅靠 Skill 页面即可工作。
- 假装 `tiktok_insight` 是同步任务。
- 在缺少视频 URL 时自动改成关键词搜索。
- 使用非官方 TikTok 抓取流程。
- 编造工具没有返回的结果、详情、评论或洞察。
- 在官方 Gecho MCP 工作流之外处理验证码、登录 TikTok 或操作用户浏览器。
