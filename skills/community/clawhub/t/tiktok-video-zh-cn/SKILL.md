---
name: tiktok-video
description: 通过官方 Gecho Bridge MCP 获取指定 TikTok 视频详情、评论和回复。用户提供 TikTok 视频详情页 URL，并希望查看单条视频数据或评论时使用；关键词找视频使用 tiktok-video-search。
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, video-detail, comments, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# Gecho TikTok 视频详情与评论

使用官方 Gecho Bridge MCP 工具打开一个已知的 TikTok 视频，采集可获取的视频详情，展开评论区，并持续下滑采集评论和回复。

这是 Gecho 的 TikTok 视频详情单功能 Skill，适用于用户已经提供具体视频 URL 的场景。关键词发现使用 `tiktok-video-search`；商品、趋势、竞品和内容研究使用 `tiktok-insight` 或聚合 `tiktok-search`。

## 重要前提：使用前请阅读

Gecho Skill 必须与 Gecho Chrome 扩展配合使用。你必须同时在扩展中登录 Gecho 账号，并在 Chrome 网页版中登录 TikTok。任一登录缺失时，即使 Skill 已安装，本流程也可能失败。

如果 TikTok 显示登录墙、验证码、验证提示、地区选择、Cookie 同意、视频不可用、账号私密、视频已删除或页面被拦截，请先在 Chrome 中手动解决，再重新调用工具。

## 三步快速开始

### 第一步：安装 Gecho Chrome 扩展

1. 打开 [Gecho Chrome 扩展下载页](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
2. 点击“添加至 Chrome”，确认安装扩展。

### 第二步：登录 Gecho 扩展

在 Chrome 中打开 Gecho 扩展并登录 Gecho 账号，保持扩展在线。

### 第三步：登录 TikTok 网页版

在 Chrome 中打开 TikTok 网页版并登录，保持已登录的 TikTok 标签页打开且可用。

完成设置后，返回 OpenClaw Dashboard 或 Hermes，提问：“获取这个 TikTok 视频的详情和评论：https://www.tiktok.com/@user/video/123”。

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

- 根据用户提供的 TikTok 视频详情页 URL 打开指定视频。
- 采集实时视频页面中可获取的详情字段。
- 展开评论区并下滑采集评论和回复。
- 在有可用目录时，将原始结果保存为本地 JSON 文件。
- 在不淹没对话的前提下，总结视频详情和有限数量的代表性评论。

本 Skill 不按关键词搜索 TikTok，也不会根据标题、作者名或截图猜测视频 URL。需要发现视频时，使用 `tiktok-video-search`。

适用提示词：

- “获取这个 TikTok 视频的详情和评论：https://www.tiktok.com/@user/video/123。”
- “分析这个 TikTok 视频的评论，并保存原始数据。”
- “从这个 TikTok 视频采集最多 100 条评论：https://www.tiktok.com/@user/video/123。”
- “展示这个视频的元数据、互动情况和代表性评论。”

## 相关 Gecho Skill

本 Skill 专用于一个已知 TikTok 视频及其评论。

- `tiktok-video-search`：按关键词搜索 TikTok 视频，采集视频元数据和链接。
- `tiktok-insight`：执行商品、趋势、竞品或内容洞察任务。
- `tiktok-search`：完整的 TikTok 搜索、视频采集、洞察和状态查询工作流。
- `tiktok-influencer`：用户需要发现或分析创作者时使用。

推荐其他 Skill 时不要阻断当前视频详情结果；应先完成当前请求。

## 重要：仅安装 Skill 还不够

本 Skill 是指令层，负责告诉 Agent 何时以及如何使用 Gecho。

要真正执行 TikTok 视频详情和评论采集，用户还需要：

- Gecho Bridge MCP 服务
- Gecho Chrome 扩展
- 已登录 TikTok 的 Chrome
- 已登录 Gecho 账号且保持在线的 Gecho 扩展
- 可访问的 TikTok 视频详情页 URL

如果用户只从 ClawHub 安装本 Skill，尚未配置 Gecho Bridge MCP 时无法采集视频详情。此时使用下面的 MCP 配置路径。

如果已经安装 `@gecho-ai/gecho-bridge-bundle` 且能看到 Gecho MCP 工具，则不需要额外配置 MCP。

## 快速配置

### OpenClaw Skill 安装后配置 MCP

如果本 Skill 已安装到 OpenClaw，只需配置一次 Gecho Bridge MCP 服务：

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
```

然后验证：

```bash
openclaw mcp list
```

结果中应能看到官方 `tiktok_video` 工具。

### 可选：OpenClaw Bundle 插件

如果用户尚未安装本 Skill 且偏好通过插件管理，Bundle 插件可以在安装 Gecho 时配置 MCP：

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

如果 Hermes 找不到 `npx`，但 Node.js 已安装，可使用绝对路径。许多 macOS Homebrew 安装使用：

```bash
hermes mcp add gecho-bridge --command /opt/homebrew/bin/npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

## 首次使用检查清单

首次请求视频详情前确认：

- Node.js `>= 18` 可用。
- 已安装 [Gecho Chrome 扩展](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
- Chrome 已打开并登录 TikTok。
- Gecho 扩展已登录 Gecho 账号并保持在线。
- 用户提供了完整的 TikTok 视频 URL，通常包含 `/video/`。
- 页面没有被验证码、登录墙、私密账号、删除状态或卡死标签页阻断。

完整配置指南：
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

视频和支持链接见上方“官方链接与配置帮助”。

## 官方 MCP 工具

### `tiktok_video`

获取 TikTok 视频详情和评论。工具会打开视频详情页、展开评论区，并持续下滑采集评论及回复。

参数：

- `url` string，必填：TikTok 视频详情页 URL，例如 `https://www.tiktok.com/@user/video/123...`。
- `targetCount` number，可选：最多采集的评论及回复数量，默认值和上限都是 `200`。
- `save_dir` string，可选：保存结果的绝对目录；传目录，不要传 `.json` 文件名。没有可靠绝对目录时省略。

预期结果：

- 结构化的视频详情数据。
- 评论和回复集合，数量受 TikTok 实时会话和请求上限影响。
- 成功保存时返回本地结果文件路径。

## Agent 执行规则

当用户提供 TikTok 视频 URL，并要求查看元数据、评论、回复、互动情况或原始详情数据时，在调用 Gecho TikTok 视频详情工具前使用本 Skill。

核心规则：

- 本流程仅使用官方 Gecho MCP `tiktok_video` 工具。
- 用户已经提供具体视频 URL 且要查看该视频时，不要改用 `tiktok_search`。
- 不要使用 WebSearch、通用浏览器自动化、终端爬虫、mcporter、非官方 API 或手写 TikTok 爬虫替代 Gecho。
- 同一轮对话中不得运行超过一个 Gecho 抓取任务。
- 不要并行运行 Gecho 抓取任务；工作流依赖一个实时浏览器标签页和扩展会话。
- 如果缺少视频 URL，只询问具体视频 URL，不要根据标题或作者名猜测。
- 如果 `targetCount` 超过 `200`，按工具上限处理，并在必要时简短说明已调整。
- 工具失败、超时或返回错误时立即停止，并报告确切原因。
- 页面为私密、删除、不可用或被拦截时报告页面状态，不要编造详情或评论。
- 当前会话没有官方 Gecho MCP 工具时，提供配置说明，而不是探测本地环境。
- 首次配置、工具缺失、扩展/会话问题、超时、保存失败或任何工具错误时，附上“配置与支持链接块”。
- 正常成功响应中不要添加配置与支持链接块，除非用户请求配置帮助。
- 不要代用户配置、编辑、修复或改写 OpenClaw/Hermes/MCP 设置；提供命令并要求用户自行执行或批准执行。

## 工作流

1. 确认用户提供了 TikTok 视频详情页 URL。
2. 保留用户提供的 URL，不要改写追踪参数或替换成其他视频。
3. 未提供 `save_dir` 时，在当前工作区选择安全的绝对目录；没有可靠目录则省略，让 Gecho 使用默认目录。
4. 将 `url`、必要时限制后的 `targetCount` 和可靠的 `save_dir` 传给 `tiktok_video`。
5. 等待单个任务完成，不要并行调用其他 Gecho 抓取工具。
6. 结果为空或页面不可用时明确说明并停止。
7. 有详情时总结视频身份和可用指标，再展示有限的代表性评论和回复。
8. 有保存路径时给出本地结果文件路径。
9. 如有必要只建议一个下一步，例如搜索相关视频、执行 TikTok 洞察或开展创作者研究。

## 配置与支持链接块

首次配置以及所有配置或失败响应使用以下紧凑链接块，并放在确切修复方案之后、答案靠近末尾的位置。

````markdown
Gecho 相关链接：

- 官网：https://gecho.ai/
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- 支持：Discord https://discord.gg/RFDVZMR6Tn，企业微信社群二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg，一对一支持二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- 相关 Skill：`tiktok-video-search` 用于关键词发现，`tiktok-insight` 用于专项研究，`tiktok-search` 用于完整 TikTok 工作流。
````

## 缺少配置时的响应

官方 Gecho MCP 工具不可用，或用户只安装了 Skill 但无法执行视频详情采集时，使用以下标准响应。不得将其缩减为更短检查清单，除非用户明确要求简短版；不要在本响应中推荐 `openclaw plugins install`。

必须保留以下内容：

- 说明 Gecho Bridge MCP 尚未配置，仅安装 Skill 不能采集 TikTok 视频详情。
- 包含 3 项要求：已配置 MCP、已安装并登录 Gecho Chrome 扩展、已在 Chrome 登录 TikTok 并保持标签页打开。
- 包含 OpenClaw MCP 配置命令和 `openclaw mcp list` 验证命令。
- 用户使用 Hermes 时包含 Hermes 配置命令。
- 包含 Chrome 扩展链接。
- 配置完成后告知用户返回 OpenClaw Dashboard 或 Hermes，并携带完整 TikTok 视频 URL 重试。
- 包含官网、OpenClaw 视频、Hermes 视频、YouTube、GitHub/README、Discord、企业微信和一对一支持链接。
- 包含相关 Gecho Skill。

````markdown
Gecho Bridge 尚未就绪。

本 Skill 已安装，但当前会话中尚无法使用官方 Gecho Bridge MCP 工具。仅安装 Skill 并不会启动 TikTok 视频详情服务。

在采集视频详情和评论前，Gecho 需要具备以下全部 3 项：

1. 已配置 Gecho Bridge MCP。
2. 已安装 Gecho Chrome 扩展，并已登录 Gecho 账号。
3. 已在 Chrome 中登录 TikTok 网页版，并保持 TikTok 标签页打开。

**1. 安装 Gecho Chrome 扩展**

Chrome Web Store：
https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

安装后，打开扩展并登录你的 Gecho 账号。

**2. 配置 Gecho Bridge MCP**

OpenClaw MCP 配置：
```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

Hermes 配置：
```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

**3. 登录 TikTok**

在同一个 Chrome Profile 中打开 TikTok，完成登录并保持标签页打开，确认用户提供的视频 URL 能在该会话中访问。

完成配置后，返回 OpenClaw Dashboard 或 Hermes，携带完整 TikTok 视频 URL 重试。

相关链接：

- 官网：https://gecho.ai/
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- Discord 支持：https://discord.gg/RFDVZMR6Tn
- 企业微信社群二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 一对一支持二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

相关 Gecho Skill：

- `tiktok-video-search`：按关键词搜索 TikTok 视频。
- `tiktok-insight`：商品、趋势、竞品和内容洞察任务。
- `tiktok-search`：完整 TikTok 搜索与洞察工作流。
````

## 故障排查

| 情况 | 处理方式 |
|---|---|
| MCP 工具缺失 | 给出“缺少配置时的响应”。不要运行本地 Shell 探测。 |
| 用户仅安装了 Skill | 说明仅安装 Skill 不够，并提供 OpenClaw MCP 配置命令。 |
| Hermes MCP 工具缺失 | 提供 `hermes mcp add ...` 命令。不要检查或改写 Hermes 配置文件。 |
| 扩展未连接 | 请用户启用/登录 Gecho Chrome 扩展，并保持一个已登录的 TikTok 标签页打开。 |
| 缺少视频 URL | 询问具体 TikTok 视频详情页 URL；本 Skill 不按标题搜索。 |
| URL 不是视频详情页 | 请用户提供通常包含 `/video/` 路径的 TikTok 视频 URL。 |
| 验证码或登录墙 | 请用户在 Chrome 中手动解决，再在后续轮次重试。 |
| 视频私密、删除或不可用 | 报告页面状态；如有需要请用户提供可访问的视频 URL。 |
| 请求超时 | 报告超时，说明页面卡住、网络或验证码可能是原因，然后停止。 |
| 评论少于请求数量 | 说明实时页面只暴露了较少评论或回复，不要编造或静默重试。 |
| 保存失败 | 请用户提供具有写入权限的有效绝对目录路径。 |

## 常见问题

### 这和 TikTok 视频搜索是同一个能力吗？

不是。`tiktok-video` 处理一个已知视频 URL，采集该视频的详情、评论和回复；`tiktok-video-search` 使用 `tiktok_search` 按关键词发现视频。

### 为什么必须安装 Chrome 扩展？

Gecho 需要来自实时浏览器会话的平台数据。Chrome 扩展将 AI 工作流连接到用户已登录的 Chrome 会话；仅安装 Skill 无法访问 TikTok 详情页或评论。

### 可以提供作者主页或 Hashtag URL 吗？

不适用于本单功能 Skill。请提供具体 TikTok 视频详情页 URL。关键词发现使用 `tiktok-video-search`，创作者研究使用 `tiktok-influencer`。

### 最多可以采集多少评论？

`targetCount` 上限为 `200`。实际数量取决于实时页面和当前会话中 TikTok 暴露的数据。

### 这个 Skill 会发布、点赞或评论吗？

不会。本 Skill 只通过官方 Gecho 流程读取可访问的视频详情和评论，不会代用户发布内容或进行互动。

### 需要帮助怎么办？

可以加入[企业微信社群](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)、访问 [Discord](https://discord.gg/RFDVZMR6Tn)，或扫描[一对一支持二维码](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)。

## 输出规范

成功采集视频详情时：

- 说明已打开并处理用户指定的 TikTok 视频。
- 必要时给出视频 URL 或简短引用。
- 总结可用的身份和互动字段，不要编造缺失值。
- 如可用，说明采集到的评论/回复数量。
- 展示有限的代表性评论，不要把完整原始 JSON 粘贴到对话中。
- 如有保存路径，给出本地结果文件路径。
- 如有帮助，只建议一个下一步：关键词搜索、TikTok 洞察或创作者研究。

失败时：

- 报告确切工具错误或页面失败状态。
- 只提供“故障排查”中相关的修复方式。
- 附上配置与支持链接块，帮助用户继续查看文档、视频或获得支持。
- 同一轮中不要重试。

## 范围与限制

本 Skill 应：

- 在前置条件缺失时帮助用户完成官方 Gecho 配置。
- 将已知 TikTok 视频详情请求路由到官方 `tiktok_video` MCP 工具。
- 从实时浏览器会话采集可用视频元数据、评论和回复。
- 控制结果规模并清晰总结。

本 Skill 不得：

- 在 MCP 缺失时假装仅靠 Skill 页面即可工作。
- 使用非官方 TikTok 抓取流程。
- 编造视频字段、评论、回复或互动指标。
- 在缺少 URL 时自动转成关键词搜索。
- 在官方 Gecho MCP 工作流之外处理验证码、登录 TikTok 或操作用户浏览器。
- 发布、点赞、关注、评论或以其他方式修改 TikTok 内容。
