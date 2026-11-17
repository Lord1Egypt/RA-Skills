# Web Publisher Skill

将任意网页文章 / 本地文档（PDF / DOCX / PPTX / XLSX / EPUB / 图片 / 音频）自动提取、改写、发布到内容平台（目前支持微信公众号）的 OpenClaw Skill。
**纯 HTTP 调用，CLI 自身不装任何 npm 依赖**——抓取、文档转换 (markitdown)、图片下载、AI 改写、发布全部由服务端完成。

> **可选安装 [`news-to-markdown`](https://www.npmjs.com/package/news-to-markdown) skill。** 服务端 pipeline 走云端固定 IP，**对小红书、部分知乎专栏、登录墙文章、海外站点等容易被反爬挡掉**；这种情况下用 `news-to-markdown` 在本地（你的家庭 IP / 真实浏览器）抓取兜底，是一种可选回退方式。可选再装 `browser-web-search` 用于「先搜索再批量发布」。

## 功能

- **网页 → 公众号一键发布**：交给一个 URL，剩下交给服务端
- **PPT/PDF → 公众号一键发布**：`ppt draft|publish <file>` 或 `draft|publish <file>`（PDF/PPTX 自动走 `POST /ppt/jobs`：解析→Markdown→公众号草稿/发布，返回 `mediaId` / `publishId`）
- **其他本地文档 → 公众号**：DOCX / XLSX 等仍走 `/pipeline`
- **任意文档 → markdown**：`convert` 命令把文档转成 markdown 文本（不发布），可加 `--out` 写文件，大文件加 `--async` 走后台任务避免 CDN 60s 超时
- **平台适配**：微信、知乎、36kr、CSDN、今日头条、小红书、人人都是产品经理 + 通用回退
- **图片处理**：服务端下载文章图片并自动上传到微信媒体库
- **AI 改写**（可选）：Minimax 驱动的分段改写，多种风格
- **对话式接入**：登录、绑定公众号都通过浏览器一次性短链完成，**AppSecret 永不进入对话**
- **抓不到的站点有兜底**：服务端 IP 被站点挡掉时，改用本地 `news-to-markdown` 抓取，再走发布流程

## 推荐配套 skill

| skill | 作用 | 安装 | 何时需要 |
|---|---|---|---|
| [`news-to-markdown`](https://www.npmjs.com/package/news-to-markdown) | 在你本地把 URL 抓成 Markdown（17 个平台专项适配 + 通用回退） | `npm install --ignore-scripts --save-exact news-to-markdown@3.3.1` | **服务端抓取失败时可选**：小红书、部分知乎专栏、登录墙文章、海外站点 |
| `browser-web-search` | 关键词 → URL 列表 | 见 skill 文档 | 你只有话题没有具体 URL 时 |

> 本 skill 自身依然零依赖；上面两个是 **配套** 而非硬依赖。但实际使用中，没装 news-to-markdown 时，遇到反爬站点 `draft / publish` 会直接报 `抓取失败`，可请用户提供已提取的正文。

## 快速开始

只需两步浏览器跳转，全部在对话里完成：

### 1) 在对话里说「帮我登录」

AI 会执行 `scripts/run.js login`，CLI 会打印一条一次性短链：

```
请在浏览器中打开以下链接，确认绑定到你的账号：
  https://tools.siping.me/skill/bind?code=ABCD-EFGH
  绑定码: ABCD-EFGH
  有效期: 5 分钟
```

在浏览器完成注册/登录 + 点「确认绑定」，凭证会自动写入 `~/.web-publisher/credentials.json`（mode 0600，仅当前用户可读）。

### 2) 在对话里说「帮我配置公众号」

AI 调用 `scripts/run.js wechat config`，CLI 同样打印短链。在浏览器表单里填 AppID/AppSecret 即可，**AppSecret 直接 POST 到服务端 AES-256-GCM 加密落库，永不进入对话上下文**。

> Agent 必须把 CLI 输出里的完整裸 URL 原样发给用户，例如 `https://tools.siping.me/skill/wechat?t=...`，不要只回复「点击填写 AppID/AppSecret」这种没有 href 的文字。

同一页面会展示需要在 mp.weixin.qq.com 后台加入 IP 白名单的服务器 IP——这一步只能你自己去公众号后台操作。

### 3)（专业版及以上可选）让每篇文章自动加页眉页脚

> 帮我配置文章页眉和文末二维码

AI 会执行 `scripts/run.js wrapper config`，再次给一条短链。在浏览器表单里写 Markdown 内容（图片、加粗、引用、二维码图片都行），保存后默认启用，下一次发布或存草稿时 pipeline 会**自动**把页眉拼到正文最前、页脚拼到正文最后；如果开了 `--rewrite`，页眉页脚内容**不会**被 AI 改写。

随时 `wrapper off` 暂停、`wrapper on` 恢复，内容保留不删；`wrapper status` 看当前字数和是否启用。

完成。直接说「把这篇文章发到公众号草稿 https://...」就能用了。

### 环境变量（可选，CI 使用）

凭证文件优先（0.9.4 起）；env vars 仅在没有 `~/.web-publisher/credentials.json` 时生效：

| 变量 | 说明 |
|---|---|
| `WEB_PUBLISHER_TOOLS_URL` | 账号 API 地址（仅允许 `https://tools.siping.me/api`） |
| `WEB_PUBLISHER_API_URL` | pipeline API 地址（仅允许 `https://api.siping.me`，兼容 `/api` 前缀） |
| `WEB_PUBLISHER_USER_ID` | 用户 ID |
| `WEB_PUBLISHER_API_KEY` | API Key |

> 想强制走 env：先 `web-publisher logout` 删除本地凭证。两者同时存在时 CLI 会在 stderr 打一条 `[warn]` 提示 file 正在覆盖 env，避免静默踩坑。

## 使用示例

在 OpenClaw 中与 AI 对话即可：

> 帮我登录

> 帮我配置一下公众号

> 帮我把这篇文章存到公众号草稿 https://mp.weixin.qq.com/s/xxxxx

> 把这篇文章改写成轻松的风格，存到草稿 https://example.com/article

> 把这篇文章直接发布到公众号 https://example.com/article

> 把这个 PDF 存到公众号草稿 ./drafts/2025-q4-report.pdf

> 把这个 PPT 发到公众号 ./deck.pptx

> 把 ~/Downloads/slide.pptx 改写后存草稿（自动走 /ppt/jobs）

> 帮我把这个 PDF 转成 markdown 存到 paper.md：./papers/whitepaper.pdf

## 可用选项

发布命令（`draft` / `publish` / `ppt draft|publish`）：

| 命令 | 说明 |
|---|---|
| `ppt draft <file>` | PDF/PPTX 专用，POST `/ppt/jobs` → 公众号草稿 |
| `ppt publish <file>` | PDF/PPTX 专用，POST `/ppt/jobs` → 直接发布 |
| `draft <file>` | PDF/PPTX 同样自动走 `/ppt/jobs`；DOCX 等走 `/pipeline` |

| 选项 | 说明 | 默认值 |
|---|---|---|
| `--theme <name>` | 发布主题 | `blackink` |
| `--rewrite` | 启用 AI 改写（`/ppt/jobs` 仅支持布尔开关） | 关闭 |
| `--style <style>` | 改写风格；PDF/PPTX 带此选项时改走 `/pipeline` | `casual` |
| `--prompt <text>` | 自定义改写提示 | - |

`convert` 命令（文档 → markdown，不发布）：

| 选项 | 说明 | 默认值 |
|---|---|---|
| `--out <file>` | 把 markdown 写到文件（stdout 只回 JSON 摘要，避免大段正文撑爆 AI 上下文） | 无（直接 stdout） |
| `--async` | 走 `/convert/async` 异步任务；学术 PDF / 扫描件 / 音频转录建议加 | 同步 |
| `--timeout <ms>` | 单次转换超时；服务端封顶 600000 (10min) | 服务端 5min |

**可用主题（服务端 0.8.0+）**：

| ID | 中文名 | 配色 |
|---|---|---|
| `astranotes` | 暖纸叙事 | 米白纸面、蓝灰强调 |
| `blackink` | 墨黑（默认） | 深色靛蓝 |
| `fieldnotes` | 蓝图笔记 | 深蓝底、浅蓝强调 |
| `clinical` | 青禾医学 | 白底深绿 |
| `default` | 默认 | 清爽蓝色 |
| `orangesun` | 橙日 | 暖橙色 |
| `redruby` | 红宝石 | 克制酒红 |
| `greenmint` | 薄荷绿 | 清新绿色 |
| `purplerain` | 紫雨 | 柔和紫色 |
| `paperjournal` | 纸上刊物 | 黑白刊物 |
| `clearguide` | 清晰指南 | 白底深绿 |
| `intelligence` | 智序 | 冷白靛蓝 |

> 在自然语言中说"墨黑 / 橙日 / 紫雨"等中文名，AI 会自动映射到对应 ID 传给 `--theme`。

## 支持平台

**发布目标**：

| 平台 | 提取 | 发布 | 状态 |
|---|---|---|---|
| 微信公众号 | ✅ | ✅ | 已支持 |
| 今日头条 | ✅ | — | 计划中 |
| 小红书 | ✅ | — | 计划中 |

**内容来源**（任意 URL 都可以丢进来，服务端会选最合适的适配器）：
微信文章、知乎专栏、36kr、CSDN、今日头条、小红书、人人都是产品经理，以及任何标准网页（通用 readability 模式）。

## 工作原理

```
draft / publish (URL):
  URL ──▶ /pipeline (JSON) → 抓取 → 可选改写 → 公众号

draft / publish / ppt (本地 PDF|PPTX):
  文件 ──▶ /ppt/jobs (multipart) → markitdown → 可选 --rewrite → 公众号
         （带 --style / --cover 等高级选项时改走 /pipeline）
  完成：mediaId（草稿）或 publishId（发布），不返回 PPT 下载链接

draft / publish (其他本地文档):
  DOCX / XLSX / ... ──▶ /pipeline (multipart)

convert:
  URL 或本地文件 ──▶ /convert (sync)  或  /convert/async (--async)
                       └─ 只返回 markdown，不推公众号
```

CLI 自身只负责凭证管理 + HTTP 调用 + 本地文件读字节并 multipart 上传，**没有本地依赖**；推荐另装 `news-to-markdown` 应对服务端抓不到的站点，但不是硬依赖。

## License

MIT


## 主题与 Markdown 扩展（0.10.1）

`node scripts/run.js themes` 离线列出 12 个主题，不读取凭证、不联网。`--theme` 支持上表中文名或 ID；旧的 `warmeditorial` / 暖调手记自动映射到 `astranotes`。未指定仍为 `blackink`，未知 ID 交由服务器明确报错，不静默替换。

所有主题统一暖纸叙事布局（16px / 350 正文，26 / 21 / 18px 标题），仅保留各自配色。主题不会改写正文，不自动添加插画或重组结构。完整扩展语法及转换边界见 [references/markdown-themes.md](references/markdown-themes.md)。用户提供的 Markdown 扩展应原样上传，不预先剥除。

```bash
node scripts/run.js draft ./article.md --theme astranotes
node scripts/run.js draft ./article.md --theme 青禾医学
```

PDF/PPTX 每页成图模式下，主题影响导读和图文容器，不会改变页面截图里的字体或原版式。想让主题作用于正文，需要用户选择原有的文字转换模式。旧服务器可能不支持新主题与扩展；部署 API 0.8.0+ 后使用。


### 0.10.1 安全边界

仅向 `https://tools.siping.me/api`（账号服务）和 `https://api.siping.me`（转换服务，兼容 `/api` 前缀）发送请求；环境变量和登录响应不能扩展该白名单。已知旧 HTTP IP 地址只在本地映射到 HTTPS，不向 HTTP 发送请求。所有请求禁止重定向。凭证保存失败时修复本地权限或空间后重新登录，不通过终端提供临时密钥；whoami 仅显示脱敏占位符。


0.10.2：本地文件读取前强制检查 50 MiB 上限，拒绝读取时变动的文件。可选抓取工具采用固定版本的项目本地安装，禁用安装脚本；请在独立目录安装并保留锁文件，后续使用 `npm ci --ignore-scripts`。第三方工具须单独评估，不会自动安装；也可直接提供正文。开发测试不包含在 ClawHub 运行包中。
