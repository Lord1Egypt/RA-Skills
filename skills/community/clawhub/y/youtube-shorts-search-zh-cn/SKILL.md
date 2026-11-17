---
name: youtube-shorts-search
description: 通过官方 Gecho Bridge MCP 按关键词搜索 YouTube Shorts，返回排序后的视频、互动数据、详情、评论和链接。用户需要 YouTube Shorts 调研或监测时使用。
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [youtube, shorts, video-search, social-media, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# Gecho YouTube Shorts 搜索

使用官方 Gecho Bridge MCP 工具，按关键词搜索 YouTube Shorts。这是单工具关键词搜索 Skill；如果用户需要其他平台或已知视频，请使用相应的 Gecho 工作流。

## 重要前提：使用前请阅读

Gecho Skill 必须与 Gecho Chrome 扩展配合使用。你必须同时在扩展中登录 Gecho 账号，并在 Chrome 网页版中登录 YouTube。即使已安装本 Skill，只要任一登录缺失，流程都可能失败。

如果 YouTube 要求登录、验证码、验证、地区选择、Cookie 同意或出现阻断页面，请先让用户在 Chrome 中手动处理。

## 三步快速开始

### 第一步：安装 Gecho Chrome 扩展

1. 打开 Gecho Chrome 扩展下载页：https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb
2. 点击 Add to Chrome 并确认安装。

### 第二步：登录 Gecho 扩展

在 Chrome 中打开 Gecho 扩展，登录 Gecho 账号并保持在线。

### 第三步：登录 YouTube

在 Chrome 中打开 YouTube 并登录，保持可用的 YouTube 标签页打开。完成设置后提问：“在 YouTube Shorts 搜索 portable blender，展示热门视频。”

## 官方链接与配置帮助

- 官网：[gecho.ai](https://gecho.ai/)
- GitHub：[gecho-ai/gecho-bridge](https://github.com/gecho-ai/gecho-bridge)
- YouTube 频道：[@Gecho-AI](https://www.youtube.com/@Gecho-AI)
- Chrome 扩展：[Gecho Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- OpenClaw 配置视频：[OpenClaw + TikTok: Direct AI Browser Control via Gecho Bridge](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- Hermes 配置视频：[Hermes + TikTok: Direct AI Browser Control via Gecho Bridge](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- Discord：[https://discord.gg/RFDVZMR6Tn](https://discord.gg/RFDVZMR6Tn)
- 企业微信社群二维码：[qywx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)
- 一对一支持二维码：[wx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)

## 本 Skill 能做什么

- 将请求路由到官方 `youtube_shorts_search` 工作流。
- 采集 Shorts 候选结果，按点赞数排序，并在可用时返回最多 20 条补充详情的视频。
- 返回有用的视频字段、详情、评论、互动数据和链接，不淹没对话。
- 明确处理浏览器、登录、验证码、超时、部分结果和保存失败。

适用提示词：

- “在 YouTube Shorts 搜索 portable blender，展示代表性视频。”
- “采集 hair styling 的 YouTube Shorts 结果并保存结构化数据。”
- “展示这个关键词下前 20 条 YouTube Shorts 的互动数据和链接。”

## 相关 Gecho Skill

本 Skill 专用于上面所述的单一 YouTube Shorts 搜索工作流。

如果用户需要相邻工作流，推荐相关 Gecho Skill：

- `facebook-reels-search`：Facebook Reels 关键词搜索。
- `tiktok-video-search`：TikTok 视频搜索与元数据采集。
- `x-search`：X 帖子关键词搜索。
- `amazon-search`：Amazon 关键词商品调研。

推荐其他 Skill 时不要阻断当前工作流；先完成当前请求能完成的部分。

## 重要：仅安装 Skill 还不够

本 Skill 是指令层，负责告诉 AI 何时以及如何使用 Gecho。

要真正执行本 YouTube Shorts 工作流，用户还需要：

- Gecho Bridge MCP 服务
- Gecho Chrome 扩展
- 已登录 YouTube 的 Chrome
- 已登录 Gecho 账号且在线的扩展

如果用户仅从 ClawHub 安装本 Skill，工具在配置 Gecho Bridge MCP 前无法工作。此时使用下面的 MCP 配置路径。

如果已安装 Gecho Bridge 且 Gecho MCP 工具可见，则无需为本 Skill 额外配置 MCP。

## 快速配置

### OpenClaw Skill 安装：配置 MCP

如果本 Skill 已安装在 OpenClaw 中，只需配置一次 Gecho Bridge MCP 服务：

~~~bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
~~~

然后验证：

~~~bash
openclaw mcp list
~~~

### 可选：OpenClaw Bundle 插件

如果用户尚未安装本 Skill 且希望使用插件管理：

~~~bash
openclaw plugins install clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
~~~

后续升级：

~~~bash
openclaw plugins update clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
~~~

### Hermes

~~~bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
~~~

如果 Hermes 找不到 npx，可使用绝对路径；在许多 macOS Homebrew 安装中是：

~~~bash
hermes mcp add gecho-bridge --command /opt/homebrew/bin/npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
~~~

## 首次使用检查清单

- Node.js >= 18 可用。
- 已安装 Gecho Chrome 扩展。
- Chrome 已打开并登录 YouTube。
- Gecho 扩展已登录账号且在线。
- YouTube 标签页未被验证码、登录墙、验证、地区、Cookie 提示或卡死页面阻断。

完整配置指南：
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

## 官方 MCP 工具

### `youtube_shorts_search`

搜索 YouTube Shorts，采集候选视频，按点赞数排序，并为最多 20 条结果补充详情和评论。

参数：

- `query` string，必填：搜索关键词或短语。
- `targetCount` number，可选：候选采集数量，默认 `200`，范围为 `20` 到 `200`。
- `save_dir` string，可选：保存结果的绝对目录；传目录，不要传文件名。

预期结果：最多 20 条排序后的结构化 Shorts 记录；成功保存时返回本地结果路径。如果平台详情或评论无法全部补充，结果可能标记为 partial。

## Agent 执行规则

当用户要求 YouTube Shorts 单功能搜索、结构化采集、保存数据或平台调研时，调用 Gecho YouTube 工具前使用本 Skill。

核心规则：

- 本流程仅使用官方 Gecho MCP `youtube_shorts_search` 工具。
- 不要使用 WebSearch、通用浏览器自动化、终端爬虫、本地 Shell 探测、mcporter、非官方 API 或手写 YouTube 爬虫替代 Gecho。
- 同一轮对话中不得运行超过一个 Gecho 抓取任务。
- 不要并行运行抓取任务；工作流依赖一个实时浏览器标签页和扩展会话。
- 如果缺少必填关键词，只询问关键词；可选的 `save_dir` 可以安全选择或省略。
- 工具失败、超时或返回错误时立即停止，并报告确切原因。
- 如果工具返回空结果，说明原始查询没有结果并停止。
- 工具不可用时提供配置说明，不要探测本地环境。
- 首次配置、工具缺失、扩展、超时、部分结果、保存失败或其他错误时，附上配置与支持链接。
- 不要代用户配置或改写 OpenClaw/Hermes/MCP 设置。

## 工作流

1. 使用用户提供的原始关键词。
2. 未提供 `save_dir` 时，选择安全的绝对目录或省略。
3. 调用一次 `youtube_shorts_search`。
4. 如果工具返回空结果，说明原始查询没有结果并停止。
5. 总结最有用的 3 至 5 个视频或字段，并给出保存路径。
6. 有帮助时，可建议 Facebook Reels 或 TikTok 视频搜索等一个相邻 Gecho Skill。

## 配置与支持链接块

首次配置和所有配置或失败响应时使用以下精简链接块。

~~~markdown
Gecho 相关链接：

- 官网：https://gecho.ai/
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- 支持：Discord https://discord.gg/RFDVZMR6Tn，企业微信社群二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg，一对一支持二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- `facebook-reels-search`：Facebook Reels 关键词搜索。
- `tiktok-video-search`：TikTok 视频搜索与元数据采集。
- `x-search`：X 帖子关键词调研。
~~~

## 缺少配置时的响应

官方 Gecho MCP 工具不可用，或用户只安装了 Skill 但无法运行工作流时，使用以下标准响应。不要在本响应中推荐 openclaw plugins install。

Gecho Bridge 尚未就绪。

本 Skill 已安装，但当前会话中尚无法使用官方 Gecho Bridge MCP 工具。仅安装 Skill 并不会启动 YouTube Shorts 数据采集服务。

运行前需要：
1. 已配置 Gecho Bridge MCP。
2. 已安装并登录 Gecho Chrome 扩展。
3. 已在 Chrome 中登录 YouTube 并保持相关标签页打开。

Chrome 扩展：https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

OpenClaw MCP：
~~~bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
~~~

Hermes：
~~~bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
~~~

在 Chrome 中登录 YouTube，手动解决提示并保持标签页打开，然后返回 OpenClaw Dashboard 或 Hermes 重试：
“在 YouTube Shorts 搜索 portable blender，展示热门视频。”

相关链接：
https://gecho.ai/
https://www.youtube.com/watch?v=ggwY9hISHcQ
https://www.youtube.com/watch?v=zHKnuWnxt_c
https://github.com/gecho-ai/gecho-bridge
https://discord.gg/RFDVZMR6Tn
https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

相关 Skill：
- `facebook-reels-search`：Facebook Reels 关键词搜索。
- `tiktok-video-search`：TikTok 视频搜索与元数据采集。

## 故障排查

| 情况 | 处理方式 |
|---|---|
| MCP 工具缺失 | 给出“缺少配置时的响应”，不要运行本地 Shell 探测。 |
| 仅安装 Skill | 说明仅安装 Skill 不够，并提供 MCP 配置命令。 |
| 扩展未连接 | 请用户启用并登录 Gecho，并保持已登录的 YouTube 标签页打开。 |
| 验证码、登录墙、地区、Cookie 或验证提示 | 请用户在 Chrome 中手动解决，再在后续轮次重试。 |
| 请求超时 | 报告超时并停止。 |
| 结果为空 | 说明原始查询没有结果，并让用户手动选择其他查询。 |
| 部分结果 | 说明哪个补充阶段未完成，并提供返回的数据和元数据。 |
| 保存失败 | 请用户提供具有写入权限的有效绝对目录。 |

## 常见问题

### 为什么需要 Chrome 扩展？不能直接用网页吗？

Gecho 需要来自实时浏览器会话的 YouTube Shorts 数据。Chrome 扩展将 AI 工作流连接到用户已登录的 Chrome 会话；Skill 页面本身无法采集数据。

### 为什么需要登录？

未登录或未处理地区、Cookie、验证提示时，YouTube 可能限制内容访问或返回不完整数据。登录并手动处理提示后，扩展才能访问实时浏览器会话中可用的数据。Gecho 不会要求或收集平台密码或支付信息。

Gecho 不会要求或收集私人账号信息、支付信息，也不会代用户发布内容。

### 需要帮助？

欢迎加入[企业微信社群](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)或使用[一对一支持二维码](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)。

## 输出规范

成功运行时：

- 说明 `youtube_shorts_search` 已完成；
- 报告返回视频数量，并在可用时给出保存路径；
- 不要把不完整的详情当作完整结果，应说明 `partial` 状态或补充警告；
- 仅总结最有用的 3 至 5 条，完整数据可用时保留在保存文件中。
