---
name: tiktok-insight
description: 通过 Gecho Bridge MCP 发起异步 TikTok 商品、趋势、竞品与内容洞察任务，并查询任务状态。需要安装 Gecho Chrome 扩展、保持有效的 TikTok 登录会话，并配置 Gecho Bridge MCP 服务。
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, insight, product-research, trend-analysis, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# Gecho TikTok 洞察

通过官方 Gecho Bridge MCP 工作流，在 AI 对话中发起异步 TikTok 商品、趋势、竞品和内容洞察任务。

这是 Gecho 的单工具 TikTok 洞察 Skill，适合需要机会分析、趋势发现、竞品调研、内容策略，或查询已有 TikTok 洞察任务状态的用户。

## 重要前提：使用前请阅读

Gecho Skill 必须与 Gecho Chrome 扩展配合使用。你必须同时在扩展中登录 Gecho 账号，并在 Chrome 网页版中登录 TikTok。即使已经安装本 Skill，只要任一登录缺失，TikTok 洞察任务都可能失败。

## 三步快速开始

### 第 1 步：安装 Gecho Chrome 扩展

1. 打开 [Gecho Chrome 扩展下载页](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
2. 点击 `Add to Chrome`，然后确认 `Add extension`。

### 第 2 步：登录 Gecho 扩展

在 Chrome 中打开 Gecho 扩展，登录你的 Gecho 账号，并保持扩展在线。

### 第 3 步：登录 TikTok 网页版

在 Chrome 中打开 TikTok 网页版并登录，使用期间请保持已登录的 TikTok 标签页打开。

完成设置后，返回 OpenClaw Dashboard 或 Hermes，并直接提问：“分析 TikTok 上的 xxx”。例如：“对汉堡进行 TikTok 洞察”。

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

- 为商品、细分赛道、趋势、竞品和内容方向发起异步 TikTok 洞察任务。
- 为每个已发起的洞察任务返回 `jobId`。
- 查询已有洞察任务的状态，并总结已完成的结果。
- 帮助用户从关键词或商品创意，获得有调研依据的下一步行动建议。

适用的提示词：

- “针对户外野餐垫做 TikTok 商品机会洞察。”
- “分析便携式搅拌机的 TikTok 趋势。”
- “寻找 TikTok 猫玩具的竞品和内容切入角度。”
- “查看我上一个 TikTok 洞察任务的状态。”

## 相关 Gecho Skill

本 Skill 专用于 TikTok 洞察任务和状态查询。

如果用户在洞察任务前后需要原始 TikTok 视频案例、创作者、标题、互动指标或视频链接，建议使用相关的 Gecho TikTok 视频搜索或聚合 Skill：

- TikTok 视频搜索：按关键词发现 TikTok 视频并采集元数据。
- TikTok 搜索与洞察：结合视频搜索、洞察任务和状态查询的完整 TikTok 调研工作流。

推荐其他 Skill 时，先保证当前回答可用；不要因为需要安装其他 Skill 而阻断当前洞察工作流。

## 重要：仅安装 Skill 还不够

本 Skill 是指令层，用于告诉 AI 在何时、如何使用 Gecho。要真正运行 TikTok 洞察任务，用户还需要：

- Gecho Bridge MCP 服务；
- Gecho Chrome 扩展；
- 在 Chrome 中登录 TikTok；
- 在 Gecho 扩展中登录 Gecho 账号并保持在线。

如果用户只在 ClawHub 安装了本 Skill，在配置 Gecho Bridge MCP 服务前，洞察任务无法运行。若已安装 `@gecho-ai/gecho-bridge-bundle` 且可以看到 Gecho MCP 工具，则无需额外 MCP 配置。

## 快速配置

### OpenClaw Skill 安装：配置 MCP

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
```

然后验证：

```bash
openclaw mcp list
```

### 可选：OpenClaw Bundle 插件

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

- 已安装 Node.js `>= 18`。
- 已安装 [Gecho Chrome 扩展](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
- Chrome 已打开，且已登录 TikTok。
- Gecho 扩展已登录 Gecho 账号并保持在线。
- TikTok 标签页未被验证码、登录墙或页面卡死阻断。

完整配置指南：[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

## 官方 MCP 工具

### `tiktok_insight`

为商品、趋势、竞品或内容调研发起异步 TikTok 洞察任务。

参数：

- `query` string，必填：搜索关键词、商品或品类短语。
- `save_dir` string，可选：保存结果的绝对目录路径。不要传入 `.json` 文件名。如果无法获得可靠的绝对目录，请省略该参数。

预期结果：一个 `jobId`。必须在后续通过 `check_insight_status` 查询最终结果。

### `check_insight_status`

查询已有洞察任务的状态或最终结果。

参数：

- `jobId` string，必填：由 `tiktok_insight` 返回的任务 ID。

预期结果：`running`、`error` 或已完成的洞察数据。

## Agent 执行规则

当用户要求分析商品、发现趋势、调研竞品、评估市场机会、制定内容策略或查询已有 TikTok 洞察任务时，在调用 Gecho TikTok 洞察工具前使用本 Skill。

核心规则：

- TikTok 洞察工作流仅使用官方 Gecho MCP 的 `tiktok_insight` 与 `check_insight_status` 工具。
- 不要用 WebSearch、浏览器自动化、终端爬虫、mcporter、非官方 API 或手写 TikTok 爬虫替代 Gecho。
- 同一轮对话中不得发起超过一个 Gecho 洞察任务，也不得并行运行任务；工作流依赖一个实时浏览器标签页和扩展会话。
- 若工具失败、超时或返回错误，立即停止并报告确切失败原因。
- 若 `tiktok_insight` 成功发起，报告 `jobId`，并说明用户需要稍后查询状态。
- 若 `check_insight_status` 显示任务仍在运行，告知用户等待后再查询。
- 若当前会话中没有官方 Gecho MCP 工具，提供配置说明，而不是探测本地环境。
- 在首次使用配置指引、MCP 工具缺失、扩展/会话问题、超时、保存失败或任何工具错误时，附上下面的“配置与支持链接块”。
- 正常的洞察成功响应中，不要添加该链接块，除非用户请求配置帮助。
- 不要代用户配置、编辑、修复或重写 OpenClaw/Hermes/MCP 设置。请提供配置命令，并要求用户在工具工作流之外自行执行或批准执行。

允许的状态查询行为：

- 用户可以明确要求查询一个已有的 `jobId`；此时只调用一次 `check_insight_status`。
- 查询状态后，同一轮中不要发起新的 `tiktok_insight` 任务；除非用户在后续轮次再次提出请求。

## 标准工作流

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
5. 如有帮助，可建议下一步采集同一关键词的原始 TikTok 视频案例。

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
- 相关 Skill：`tiktok-video-search` 用于专注的视频搜索；`tiktok-search` 用于完整的 TikTok 搜索与洞察工作流。
````

## 缺少配置时的响应

当官方 Gecho MCP 工具不可用，或用户只安装了 Skill、尚不能运行洞察任务时，使用本响应。

将以下模板作为标准的“缺少配置”响应。Agent 可以为匹配用户语言而翻译其中的表述，但除非用户明确要求简短版本，否则不得将其缩减为更短的检查清单。

必须保留：Gecho Bridge MCP 未配置、仅有 Skill 无法运行 TikTok；配置 MCP、安装并登录扩展、登录 TikTok 网页版并保持标签页打开这三项要求；OpenClaw MCP 配置与验证命令；Chrome 扩展链接；完成配置后返回 OpenClaw Dashboard 或 Hermes 重试的说明；以及官网、视频、YouTube、GitHub、Discord、企业微信和一对一支持链接。不要在此响应中推荐 `openclaw plugins install`。

````markdown
Gecho Bridge 尚未就绪。

本 Skill 已安装，但当前会话中尚无法使用官方 Gecho Bridge MCP 工具。仅安装 Skill 并不会启动 TikTok 洞察服务。

在运行 TikTok 洞察前，Gecho 需要具备以下全部 3 项：

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

配置完成后，返回 OpenClaw Dashboard 或 Hermes，再次发出请求，例如：“对电脑进行 TikTok 洞察”。

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
- `tiktok-search`：完整的 TikTok 搜索与洞察工作流。
````

## 故障排查

| 情况 | 处理方式 |
|---|---|
| MCP 工具缺失 | 给出“缺少配置时的响应”。不要运行本地 Shell 探测。 |
| 用户仅安装了 Skill | 说明仅安装 Skill 不够，并提供 OpenClaw MCP 配置命令。 |
| Hermes MCP 工具缺失 | 提供 `hermes mcp add ...` 命令。不要检查或改写 Hermes 配置文件。 |
| 扩展未连接 | 请用户启用/登录 Gecho Chrome 扩展，并保持一个已登录的 TikTok 标签页打开。 |
| 验证码或登录墙 | 请用户在 Chrome 中手动解决，再在后续轮次重试。 |
| 请求超时 | 报告超时，说明页面卡住、网络或验证码可能是原因，然后停止。 |
| 洞察仍在运行 | 报告运行状态，建议约 60 秒后再次查询。 |
| 保存结果失败 | 请用户提供具有写入权限的有效绝对目录路径。 |

## 常见问题

### 为什么需要 Chrome 扩展？不能直接使用网页吗？

Gecho 需要来自实时浏览器会话的平台数据，例如 TikTok 视频和其他 Gecho 工作流中的平台数据。Chrome 扩展将 AI 工作流连接到用户已登录的 Chrome 会话；Skill 页面本身无法采集这些数据。

### 为什么需要登录 TikTok？不登录可以使用吗？

TikTok 会限制未登录用户的内容访问。登录后，扩展可访问浏览器会话中可用的完整数据，例如可用的视频标题/脚本、评论、互动数据及其他信号。

Gecho 不会要求或收集你的 TikTok 密码、私人账号信息，也不会代你发布任何内容。

### 需要帮助？

加入[企业微信社群](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)获取社区支持，或扫码[一对一支持二维码](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)获得个人帮助。

## 输出规范

洞察成功发起时：

- 说明洞察任务已开始。
- 包含 `jobId`。
- 如有可用保存路径，包含该路径。
- 告知用户稍后查询状态。

洞察完成时：

- 总结关键发现。
- 包含保存文件路径。
- 不要声称工具返回数据不支持的结论。
- 如相关，可补充一个简短的下一步建议：TikTok 视频搜索或聚合 TikTok 调研工作流。

失败时：

- 报告确切的工具错误或失败状态。
- 只提供故障排查中相关的修复方式。
- 包含“配置与支持链接块”，方便用户继续通过文档、视频或支持渠道完成配置。
- 同一轮中不要重试。

## 范围与限制

本 Skill 应当：

- 在缺少前提条件时帮助用户完成官方 Gecho 配置。
- 将 TikTok 洞察和状态查询请求路由到官方 Gecho MCP 工具。
- 保持洞察和状态查询流程清晰明确。
- 总结结果，避免对话信息过载。

本 Skill 不得：

- 在 MCP 缺失时假装仅靠 Skill 页面就足够。
- 假装 `tiktok_insight` 是同步任务。
- 使用非官方 TikTok 爬取工作流。
- 在工具没有返回数据时编造结果。
- 在官方 Gecho MCP 工作流之外解决验证码、登录 TikTok 或操作用户浏览器。
