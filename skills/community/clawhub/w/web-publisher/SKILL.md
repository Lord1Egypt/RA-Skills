---
name: web-publisher
version: 0.9.18
description: 输入文章 URL **或本地文档（PDF/DOCX/PPTX/XLSX/EPUB/图片/音频/...）**，自动提取正文、可选 AI 改写、并发布到微信公众号；也可只把任意文档转成 Markdown 文本（不发布）。抓取 / 转换 / 改写 / 发布都在服务端 (tools.siping.me) 完成，CLI 不装任何 npm 依赖；登录、公众号配置全部通过对话 + 一次性浏览器跳转完成。⚠️ 服务端走云端固定 IP，**对小红书、部分知乎专栏、登录墙文章、海外站点经常被反爬挡掉**——此时由 AI Agent（Hermes / Cursor / OpenClaw 等）改调用**用户本地安装的 `news-to-markdown-skill`** 把 URL 抓成 Markdown，然后人工复核 / 归档。也可配合 `browser-web-search` 先搜索拿到 URL 再批量发布。
author: Ping Si <sipingme@gmail.com>
tags: [publish, wechat, article, content, onboarding, pdf, docx, markitdown]
---

# Web Publisher

输入文章 URL **或本地文档（PDF / DOCX / PPTX / XLSX / EPUB / 图片 / 音频 / ...）**，自动提取正文、可选 AI 改写、并发布到微信公众号；也支持只把文档转成 Markdown（不发布）。**纯 HTTP 调用，无本地依赖**——抓取、文档转换、图片处理、AI 改写、发布全部由服务端完成。

## 用户怎么说（复制给机器人）

下面这些话可以直接对 Cursor / OpenClaw / 其他 Agent 说。**带上文件路径或 URL**，机器人会调用本 skill，不需要你自己敲命令。

### 第一次用（登录 + 配公众号）

```text
帮我登录 web-publisher
```

```text
我点完确认了，继续绑定
```

```text
帮我配置微信公众号
```

### 网页文章 → 公众号草稿

```text
把这篇文章存到公众号草稿：https://mp.weixin.qq.com/s/xxxxx
```

```text
用橙日主题，改写后存草稿：https://36kr.com/p/xxx
```

### PDF → 公众号（默认：每页成图，保留视觉版式）

**最常见说法**——默认会把 PDF **每页渲染成图片**发公众号，保留原排版、图表、扫描件效果：

```text
把这个 PDF 发到公众号草稿：~/Downloads/报告.pdf
```

```text
帮我把 手册.pdf 存到公众号草稿
```

### PDF → 公众号（PPTX 抽可编辑文字）

当你**要可搜索、可编辑的文字文章**（不是整页截图），应说明「提取文字 / 抽文字」：

```text
把这个 PDF 提取文字后存到公众号草稿：report.pdf
```

```text
把 report.pdf 发公众号，要可编辑文字，不要按页截图
```

Agent 应加 **`--extract-text`**（`mode=convert_only`）。

### PDF → 公众号（每页成图，显式指定）

与默认相同；用户明确说「每页成图」时可加 **`--page-images`**（`mode=page_images`），一般不必加。

### PDF → 公众号（直接从 PDF 抽文字）

```text
先把这份 PDF 转成 Markdown 文字，再存到公众号草稿：report.pdf
```

```text
提取 report.pdf 的文字，改写后发到公众号
```

```text
把 report.pdf 当文字文章发公众号，不要按页截图
```

### PPT/PPTX → 公众号（默认：导读 + 每页成图，与 PDF 相同）

```text
把这个 PPT 存到公众号草稿：~/Downloads/deck.pptx
```

默认与 PDF 一样：**文首 LLM 导读 + 每页截图**。要纯文字文章时加 **`--as-markdown`**。

### 直接发布（慎用）

只有明确说「发布 / 直接发出去」时机器人才会用 publish：

```text
把 report.pdf 直接发布到公众号
```

```text
发布到公众号（不要只存草稿）：https://example.com/article
```

### 只转 Markdown，不发布

```text
把这个 PDF 转成 markdown，保存到 report.md
```

```text
提取 ~/Downloads/paper.pdf 的文字，不要发公众号
```

### 和 fast-ppt 区分（不要说混了）

| 你想做什么 | 对机器人说 | 用什么 skill |
|---|---|---|
| PDF **发到公众号** | 「存到公众号草稿 / 发到公众号」 | **web-publisher** |
| PDF **做成可下载 PPT** | 「仅转换成 PPT / 做成幻灯片」 | **fast-ppt** |
| PDF **只要文字、不发也不做 PPT** | 「转成 markdown」 | **web-publisher** `convert` |

❌ 容易混淆的说法：

- 「把这个 PDF 做成 PPT 并发公众号」→ 机器人应**先问**：要公众号图文（web-publisher）还是 PPT 下载（fast-ppt）？
- 「发 PDF」且没说是公众号 → 默认按 **web-publisher 发公众号** 理解；若用户其实要 PPT 文件，需澄清。

### 关键词速查（Agent 用来选模式）

| 用户关键词 | Agent 应选 |
|---|---|
| 发公众号 / 存草稿（PDF/PPTX，未特指） | 默认 **`page_images`**（导读 + 每页成图） |
| **提取文字 / 可编辑文字 / PPTX 抽字** | **`--extract-text`**（`convert_only`） |
| **每页成图 / 按页截图 / 保留版式** | 默认已是；可显式 **`--page-images`** |
| 直接从 PDF 转 markdown / 提取文字 | **`--as-markdown`** |
| 改写 / 润色 | **`--rewrite`**（自动 markdown 模式） |
| 仅转换 / 做成 PPT / 下载幻灯片 | **不是本 skill** → 转 **fast-ppt** |
| 只转 markdown、不发布 | `convert` |

---

## 给 AI 的使用说明（核心）

### 用户意图 → 命令

| 用户说什么 | 调用 | 然后做什么 |
|---|---|---|
| 帮我登录 / 注册 / 绑定账号 | `scripts/run.js login` | **fire-and-forget (checkpoint 模型)**：命令 ~0.3s 返回，写 `~/.web-publisher/login-pending.json` 等待用户在浏览器授权。把 stdout JSON 里的 `verifyUrl` **原文**交给用户，附上 `userCode`。**不要 await login** 它已经退出了。等用户说"点完了"再调 `scripts/run.js login-status` 把凭证拉下来 |
| 检查登录是否完成 / 我登上没 / 完成登录第二步 | `scripts/run.js login-status` | 一次性向服务端查 device-code 状态并写凭证。`state`：`logged-in` = 已登录 **且** 公众号已配置（可以发文章了）；`logged-in-no-wechat` = 账号绑好了但公众号 AppID/AppSecret 还没填齐，**AI 必须自己接着调用 `wechat config`**（不要把命令贴给用户让他敲）然后只把生成的 URL 原文给用户，否则 draft / publish 会失败；`awaiting-browser-confirm` = 用户还没在浏览器点确认（催用户去点，再隔几秒重试本命令）；`expired-pending` = device-code 5 分钟过期了，重跑 `login`；`invalid-credentials` = apiKey 已失效，建议 `login --force`；`polling-failed` = 网络/服务端临时错，可重试本命令；`persist-failed` = 服务端绑定成功但本地写盘失败（看 `note` 里的 fallback 环境变量）；`not-logged-in` = 没启动过 login |
| 配置/绑定公众号 / 配 AppID | `scripts/run.js wechat config` | **两件事必须一并交付，缺一不可**：(1) 把 stdout JSON 里 `url` 字段的完整 URL **原文粘贴**给用户（不包装 Markdown 链接、不用"点击此处"替代）；(2) 把 stdout JSON 里 `serverIps` 数组里的所有 IP 也告诉用户，并明确指引"到 mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单 加入"。漏掉 IP 白名单会让发布时被微信以 invalid IP 拒绝，所以**不能省**。`instruction` 字段已经把这两件事写在一起了，照念即可 |
| 我现在是谁 / 看看账号 / 余额 / 我是哪一档 | `scripts/run.js whoami` | 报告账号、apiKey 脱敏摘要、微信配置、`plan.{role,label,rewriteEngine}`（用户等级 + 当前 rewrite 引擎；专业版及以上走 `creator` 原创合成，其它走 `rewriter` 伪改写） |
| 公众号配好了吗 | `scripts/run.js wechat status` | 报告 `configured` 与当前 AppID |
| 退出登录 / 注销 | `scripts/run.js logout` | 报告"已清除本地凭证" |
| 配置页眉页脚 / 关注引导 / 文末二维码 | `scripts/run.js wrapper config` | 专业版及以上可用；读取 stdout JSON `url` 字段，把完整 URL **原文粘贴**给用户（同 wechat config 规则，不包装 Markdown 链接）；AI **不要替用户编 Markdown 内容** |
| 我的 wrapper 配好了吗 / 现在还启用吗 | `scripts/run.js wrapper status` | 报告 `configured` / `enabled` / 字符数 |
| 关掉页眉页脚 / 暂停 wrapper | `scripts/run.js wrapper off` | 报告"已关闭，下次开启即恢复" |
| 重新启用页眉页脚 | `scripts/run.js wrapper on` | 若返回 409 提示先运行 `wrapper config` 填内容 |
| 把这篇文章存到草稿 `<url>` | `scripts/run.js draft <url>` | 等待返回，转告标题与 mediaId |
| 把这个 PDF / DOCX 存到草稿 `<file>` | `scripts/run.js draft <path>` | **PDF 默认** `page_images`（每页成图）；**抽可编辑文字**加 `--extract-text`；**直接抽 PDF 文字**加 `--as-markdown` |
| 把这个 PPT / PDF 发到公众号草稿 `<file>` | `scripts/run.js ppt draft <path>` | 同 `draft <path>` |
| 把 PDF **抽 PPTX 文字**发公众号 `<file>` | `scripts/run.js draft <path> --extract-text` | `mode=convert_only`，经 pingPPT |
| 把这个 PPT / PDF 直接发布 `<file>` | `scripts/run.js ppt publish <path>` | 仅当用户**明确说"发布"**；PDF 默认每页成图 |
| 把这篇文章发布到公众号 `<url>` | `scripts/run.js publish <url>` | 仅当用户**明确说"发布"** 才用 publish；默认走 draft |
| 把这个 PDF 直接发布到公众号 `<file>` | `scripts/run.js publish <path>` | 同上；PDF 默认每页成图 |
| 把 PDF 当**文字文章**发公众号 `<file>` | `scripts/run.js draft <path> --as-markdown` | 用户说了「转 markdown / 提取文字 / 不要截图」时用 |
| 改写后存草稿 / 发布 | `... draft <input> --rewrite [--style casual]` | PDF 加 `--rewrite` 会自动切 markdown 模式 |
| 把这个文档转成 markdown / 提取这个 PDF 的文字 | `scripts/run.js convert <input>` | 默认同步返回 `markdown / byteLength / durationMs`；想保存成文件加 `--out path.md`；大文件 / 学术 PDF 加 `--async`，CLI 自动轮询 |
| 上次那个任务完成了吗 | `scripts/run.js status <jobId>` | 转告 status / progress / result |

### PDF/PPTX 上传提示（Agent 必看）

用户给 **本地 PDF / PPTX** 要发公众号时，CLI 走 **`POST /ppt/jobs`**（完整 URL 为 `{apiUrl}/ppt/jobs`）。

#### PDF 三种处理方式

| 模式 | 何时使用 | 服务端流程 | 公众号效果 |
|---|---|---|---|
| **`page_images`（默认）** | PDF/PPTX，只说「发公众号」 | 导读 + 每页 PNG → 公众号（PPTX 经 LibreOffice 转 PDF 后成图） | **图文**，文首主题样式导读 + 每页一张图 |
| **`convert_only`** | PDF，「提取文字 / PPTX 抽字」 | pingPPT → PPTX → markitdown 抽文字 | **可编辑文字文章** |
| **`markdown`** | `--as-markdown` / `--rewrite` | 原文件直接 markitdown | **文字文章** |

**PPTX** 没有 `convert_only`；默认已是 `page_images`。

#### 1. 执行前 — 告诉用户（推荐话术）

**PDF 默认（每页成图）：**

> 我会把 PDF 每一页渲染成图片，文首自动生成一段 100–150 字的导读摘要，再按原排版存入微信公众号草稿（图表、扫描件都能保留）。

**用户明确要 PPTX 抽可编辑文字：**

> 我会先用 pingPPT 把 PDF 转成带可编辑文字的 PPTX，再提取文字存入公众号草稿。

**用户明确要 markdown 文字：**

> 我会先把 PDF 提取成 Markdown 文字，再存入公众号草稿。

#### 2. 选命令

| 场景 | 命令 |
|---|---|
| PDF → 公众号（**默认每页成图**） | `draft report.pdf` |
| PDF → PPTX 抽可编辑文字 | `draft report.pdf --extract-text` |
| PDF → 每页成图（显式） | `draft report.pdf --page-images` |
| PDF → 直接 markitdown | `draft report.pdf --as-markdown` |
| PDF + AI 改写 | `draft report.pdf --rewrite`（自动改 markdown 模式） |
| 高级改写 `--style` / `--cover` | `draft report.pdf --rewrite --style ...` → 改走 **`/pipeline`** |
| PPTX → 公众号（**默认导读+每页成图**） | `draft deck.pptx` |
| PPTX → 纯文字 | `draft deck.pptx --as-markdown` |

#### 3. 执行中 — 读 stderr 确认路由

每页成图（**默认**）：

```
[server] PDF → 每页成图 → 公众号 (/ppt/jobs): report.pdf (1234567 bytes)
```

PPTX 抽文字（`--extract-text`）：

```
[server] PDF → 仅转换 (PPTX 提取文字) → 公众号 (/ppt/jobs): report.pdf (1234567 bytes)
```

```
[server] PDF → Markdown → 公众号 (/ppt/jobs): report.pdf (1234567 bytes)
```

#### 4. 完成后 — 读 stdout JSON

每页成图（默认）：

```json
{
  "endpoint": "/ppt/jobs",
  "mode": "page_images",
  "flow": "pdf-page-images-wechat",
  "mediaId": "..."
}
```

PPTX 抽文字（`--extract-text`）：

```json
{
  "endpoint": "/ppt/jobs",
  "mode": "convert_only",
  "flow": "pdf-pptx-text-wechat",
  "mediaId": "..."
}
```

Markdown 模式：

```json
{
  "endpoint": "/ppt/jobs",
  "mode": "markdown",
  "flow": "ppt-markdown-wechat",
  "mediaId": "..."
}
```

#### 5. 与 fast-ppt 区分

| | **web-publisher** | **fast-ppt** |
|---|---|---|
| 用途 | PDF/PPTX → **公众号** | 生成 **PPT 下载文件** |
| PDF 默认 | 每页成图 → 公众号图文 | 可编辑 PPTX 下载 |
| 结果 | `mediaId` / `publishId` | `ppt.siping.me/.../download` |

### 登录流程（AI 必看，0.9.0 切换成 checkpoint 模型）

历史变迁：
- 0.7.x：`login` 在前台阻塞 5 分钟轮询。被 IDE / agent shell wrapper（Cursor / Claude / OpenClaw 等）包起来时，wrapper 把长任务标成已完成 / 转后台，输出全部丢失，用户以为失败。
- 0.8.x：`login` 改成 fire-and-forget + 后台 daemon。前台 ~1s 退出，daemon 自动写凭证；后台进程难以审计，已弃用。
- **0.9.0：checkpoint-file 模型。** 没有后台进程，没有 child_process。`login` 写 pending 文件就退出；`login-status` 读 pending → 一次性 poll → 写凭证。流程更简单、可审计。

AI 必须按这两步走：

1. **第一步：`login` → 把链接给用户。**

   ```bash
   scripts/run.js login   # ~0.3 秒内返回，stdout 是 JSON
   ```

   stdout 形如：

   ```json
   {
     "success": true,
     "pendingCheckpoint": true,
     "verifyUrl": "https://tools.siping.me/skill/bind?code=ABCD-1234",
     "userCode": "ABCD-1234",
     "expiresInSec": 300,
     "expiresAt": 1746336789012,
     "pendingPath": "/Users/.../.web-publisher/login-pending.json",
     "credentialsPath": "/Users/.../.web-publisher/credentials.json",
     "instruction": "[AI必读] ..."
   }
   ```

   AI 必须做的事：

   - 把 `verifyUrl` **完整 URL 原文**贴给用户（同 `wechat config` 规则：不要包成 Markdown 链接、不要用"点击此处"代替），并附上 `userCode`。
   - 告诉用户："点完确认后回来跟我说一声，我帮你完成绑定"。
   - **绝对不要再 await `login` 命令**——它已经退出，没有任何后台进程在轮询。device-code 写在了 `pendingPath` 那个文件里等你下一条命令处理。

2. **第二步：用户回来说"点完了" → `login-status` 真正完成绑定。**

   ```bash
   scripts/run.js login-status   # 也是 ~1s 内返回
   ```

   这条命令会做一次性 POST `/skill/device/poll`，bound 时把凭证写进 `credentials.json` 并删掉 pending 文件。读 stdout JSON 的 `state` 字段决定下一步：

   | state | 含义 | AI 该做什么 |
   |---|---|---|
   | `logged-in` | 凭证有效 **且** 微信公众号 AppID/AppSecret 已配置 | 报"已登录，账号 = `<name>`，公众号已就绪，可以使用 draft / publish / convert 了"。stdout JSON 的 `wechat.appId` 可以告诉用户绑定的是哪个公众号 |
   | `logged-in-no-wechat` | 凭证有效，但 `wechat.configured == false`——账号绑好了但公众号 AppID/AppSecret 还没填齐（stdout 的 `wechat.appId` 非 null 表示 AppID 已留过，仅缺 AppSecret） | **四件事，按顺序做完**：①不要说"可以直接用了"；②告诉用户"登录成功，但公众号配置还差一步"，措辞按 `wechat.appId` 是否为 null 区分（"AppID 已留过、缺 AppSecret" vs "AppID/AppSecret 都还没填"）；③**AI 自己**立即调用 `scripts/run.js wechat config`，把它返回的 stdout JSON 里 `url` **完整原文**呈现给用户；④**同时**把 `wechat config` 输出里 `serverIps` 数组的所有 IP 也告诉用户，附上"到 mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单 加入"的明确步骤。漏掉 ④ 用户填完 AppID/AppSecret 也发不了文章——微信会以 invalid IP 拒绝。**不要**给用户贴 `cd ... && node scripts/run.js wechat config` 这种 shell 命令——AI 该自己跑的命令绝不外推给用户。 |
   | `awaiting-browser-confirm` | pending 文件存在、device-code 还在 TTL 内、但用户还没在浏览器点确认 | 催用户去浏览器点击"确认绑定"；用户说点完了之后再调一次 `login-status`。**不要立刻轮询本命令**——服务端状态只有用户点了才会变 |
   | `expired-pending` | device-code 5 分钟过期了 | 让用户重跑 `login` |
   | `not-logged-in` | 既没凭证也没 pending checkpoint | 让用户从 `login` 开始 |
   | `invalid-credentials` | 本地有凭证但服务端拒绝（apiKey 已被换 / 撤销） | 让用户跑 `scripts/run.js login --force` |
   | `polling-failed` | 网络或服务端 5xx 临时失败，pending 文件保留 | 几秒后再调一次 `login-status` |
   | `persist-failed` | 服务端已绑定但本地写盘失败（磁盘满 / 权限） | 把 stdout `note` 字段里给的 `WEB_PUBLISHER_*` 临时环境变量交给用户，并提示用户修磁盘问题后再 `login --force` |
   | `logged-in-unverified` | 有凭证但 whoami 当下连不通；微信状态也未知 | 当已登录处理，但提示"网络不稳定，未做服务端校验，公众号配置状态未知"。等网络恢复后建议跑一次 `wechat status` 确认 |

3. **不要做的事：**

   - ❌ 不要在 `login` 之后立刻紧密循环 `login-status`。`awaiting-browser-confirm` 完全正常，要等用户去浏览器操作；让用户主动告诉你"我点完了"再去查一次。
   - ❌ 不要因为 `login` 返回 `success: true` 就告诉用户"已登录"——`pendingCheckpoint: true` 表示**第二步还没做**，必须 `login-status` 返回 `logged-in` 或 `logged-in-no-wechat` 才算 device-code 流程完成。
   - ❌ **不要看到 `logged-in-no-wechat` 也喊"现在可以用 web-publisher 了 / 可以发文章了"**——这个 state 表示账号绑了但公众号 AppID/AppSecret 还没填齐，draft / publish 必然失败（`convert` 仍可用，因为它不接公众号）。要告诉用户"还差一步：配置公众号"，**然后 AI 自己跑** `wechat config`，把它输出的 URL 原文交给用户。
   - ❌ **绝对不要把 `cd ~/.openclaw/workspace/skills/web-publisher && node scripts/run.js wechat config` 这种 shell 命令贴给用户**。`wechat config` 是 AI 自己执行的命令，用户只该看到执行结果（浏览器短链 + IP 白名单）。同样的规则适用于 `login` / `wrapper config` 等所有产生短链的命令——用户对话里只该出现 URL，不该出现 `cd` / `node` / `scripts/run.js` 之类的东西。
   - ❌ **跑完 `wechat config` 只把短链贴给用户、却不贴 `serverIps` 里的服务器 IP**——这是常见疏忽。AppID/AppSecret 填得再对，没把这些 IP 加到微信公众平台后台 (mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单) 的白名单里，微信调用会直接以 "invalid IP" 拒绝，发布全部失败。`wechat config` 的 stdout JSON 里 `instruction` 字段已经把"URL + IP 白名单"打包成一句话了，原文转达即可。如果 `serverIps` 数组为空，说明服务端没设 `WECHAT_SERVER_IPS`，要提醒用户向管理员索取出口 IP 后再自行加白名单。
   - ❌ 不要用 `--force` 当默认行为；只有 `invalid-credentials` 或用户明确说"切换账号 / 重新绑定"才用。
   - ❌ 不要直接读 `~/.web-publisher/credentials.json` 试图判断登录状态——文件存在不代表 apiKey 还有效，更不代表公众号已配置。永远走 `login-status`。
   - ❌ 不要假定 `login` 之后会自动写凭证——0.9.x 没有后台进程；不调 `login-status`，凭证永远不会被拉下来。

4. **`login --force` / 已登录 fast-path 的同样规则**：当 `login` 看到本地凭证仍然有效时也会走 fast-path 直接退出，stdout JSON 里有 `alreadyLoggedIn: true` + `wechat: { configured, appId }` + `nextStep` 字段。`nextStep == 'wechat-config-required'` 时，AI 也要按 `logged-in-no-wechat` 那条规则处理：自己调 `wechat config` → 给用户 URL 原文，**不要**让用户去敲 shell 命令。

5. **退出码约定**：`login-status` 在 `logged-in` / `logged-in-no-wechat` / `awaiting-browser-confirm` 返回 0（device-code 流程本身没问题）；其余状态返回 1，方便包装脚本用 `set -e` 直接判错。

### 关键约束（必须遵守）

1. **AppSecret 永不进入对话上下文**。`wechat config` 只输出短链，用户在浏览器表单提交，AI 不要询问、不要展示、不要日志化 AppSecret。
   **URL 必须原文输出**：读取 stdout JSON 的 `url` 字段后，必须把完整 URL 原封不动发给用户，例如：
   ```
   请在浏览器中打开以下链接填写 AppID / AppSecret：
   https://tools.siping.me/skill/wechat?t=XXXX
   ```
   ❌ 错误写法（会导致用户拿不到链接）：
   - `[点击填写 AppID/AppSecret](https://...)` ← Markdown 链接，某些 Agent UI 只显示文字
   - `请点击此处填写 AppID/AppSecret` ← 完全丢失 URL
   - 不输出 URL，仅说"已生成配置链接" ← 用户无法打开
2. **默认 draft，不要主动 publish**。除非用户原话里明确说了"发布 / 直接发到公众号 / publish"，否则一律用 `draft`。`convert` 不发布，只把文档转成 markdown，可以放心调。
3. **`<input>` 是 URL 还是本地文件 CLI 自动判断**：以 `http://` / `https://` 开头当 URL；否则当成本地路径。**PDF / PPTX 本地文件**默认走 **`POST /ppt/jobs` + `page_images`**（导读 + 每页成图）；PDF 要 PPTX 抽可编辑文字时加 **`--extract-text`**；要纯 markitdown 或加 **`--as-markdown` / `--rewrite`** 时改 **`markdown`**。带 `--style` / `--cover` 等高级改写选项时改走 `/pipeline`。
4. **本地文件上限 50 MiB**（服务端 `MARKITDOWN_MAX_INPUT_BYTES`）。超过先让用户裁剪 / 压缩；学术 PDF 太大时建议加 `--async` 走异步。
5. **`convert` 输出体积大时务必用 `--out path.md`**：把整个 PDF 的 markdown 塞进 stdout 会撑爆 AI 的上下文窗口；AI 应主动建议用户加 `--out` 然后再读那个文件。
6. **耗时正常**。URL 抓取整体 30–90 秒（带 `--rewrite` 更久），文档转换看体积（学术 PDF 可达 5 分钟）。CLI 每 5 s 打一次进度。**不要超时重试**——重复调用会创建多个草稿；需要更长时间用 `--async`。
7. **错误恢复对照**：

   | CLI 错误 | 正确处置 |
   |---|---|
   | `尚未登录` | 提示用户跑 `scripts/run.js login`；等用户在浏览器点完确认后再调 `scripts/run.js login-status` 验证 |
   | `WeChat credentials not configured` | 提示用户跑 `scripts/run.js wechat config`（仅 draft/publish 需要；`convert` 不需要微信配置） |
   | `发布额度不足 / 余额不足 / insufficient credits` | 提示用户去 [tools.siping.me](https://tools.siping.me) 充值 |
   | `input is not a URL and no file exists at: ...` | 用户给的路径不存在 / 拼错；让用户重确认本地路径 |
   | `Uploaded file exceeds the 52428800-byte server limit` | 超过 50 MiB；让用户压缩 / 拆分 PDF 后重试 |
   | `markitdown 转换失败 (cli_missing)` | 服务端 markitdown 未安装；联系服务方，用户侧无法解决 |
   | 任务 `failed`，error 含 `抓取失败` / `403` / `登录` | 把原 error 转给用户；提示**用本地 `news-to-markdown` 重新抓取**，常见反爬站（小红书 / 知乎 / 海外站）这样能救回来 |

### 与 browser-web-search 配合（搜索 + 发布）

用户只给关键词没有 URL 时，先用 `browser-web-search` 拿 URL 列表，再逐条调本 skill：

```bash
# Step 1：搜索拿 URL（browser-web-search skill）
bws toutiao/search "AI Search" --count 3 --sort time

# Step 2：对每个 URL 调本 skill
scripts/run.js draft <url1>
scripts/run.js draft <url2>
scripts/run.js draft <url3>
```

如果用户已经给了 URL，**跳过 Step 1**。

### 与 news-to-markdown-skill 配合（必看：服务端抓不到时的回退路径）

本 skill 的抓取**只在服务端（tools.siping.me）发生**，CLI 自身不抓任何网页。服务端走云端固定 IP，**以下站点经常拿不到正文**：

- 小红书 `xiaohongshu.com`（全站强反爬）
- 部分知乎专栏 `zhuanlan.zhihu.com`（zse-ck 反爬）
- 登录墙文章（部分公众号 token 链接、内部专栏）
- 海外站点（被云厂商出口 IP 直接 403）

这种站点服务端一律返回 `failed` + `抓取失败 / 403 / 登录 / 内容为空`。**唯一可靠的兜底是用用户本地（家庭 / 办公 IP，可装真实 Chrome）抓取**——这就是为什么强烈要求用户额外安装 [`news-to-markdown-skill`](https://github.com/sipingme/news-to-markdown-skill)。

#### AI Agent (Hermes / Cursor / OpenClaw) 的回退步骤

1. 收到「发到公众号 `<url>`」请求 → 先尝试本 skill：`scripts/run.js draft <url>`。
2. 任务返回 `failed` 且 `error` 含 `抓取失败 / 403 / forbidden / 登录 / 内容为空`，**或**用户预先声明该站反爬严重 → 切到 `news-to-markdown-skill`：

   ```bash
   # news-to-markdown-skill 的标准调用入口（在用户本机）
   node <path-to>/news-to-markdown-skill/scripts/run.js convert \
     --url "<原始 URL>" \
     --download-images \
     --output-dir ./drafts/<safe-slug>
   # 产出：./drafts/<slug>/article.md + ./drafts/<slug>/images/*
   ```

3. 把本地产出（Markdown 路径 + 图片目录）**如实回报给用户**，并明确告知：

   - 服务端为什么抓不到（云 IP 被该站挡了）
   - 已经在本地抓到了正文（路径 + 图片张数）
   - **本 skill 当前 CLI 只接受 URL，不接受本地 Markdown 文件**——所以无法直接把本地稿件再次走 `draft|publish` 上传到公众号；下一步由用户决定（人工复核归档、手动粘贴到公众号后台、或等待服务端开放本地稿件入口）

⚠️ **AI Agent 必须遵守的硬约束**：

- **不要**把本地 markdown 文件路径当作 URL 参数喂给 `scripts/run.js draft|publish`。当前 CLI 只支持 `https?://` URL，传文件路径会让服务端 404 / 抓不到，浪费用户额度。
- **不要**自己重新调用 `draft|publish` 重试同一个失败 URL（多次尝试也会失败，并占额度）。
- **不要**伪装成服务端抓到了——必须明确告诉用户「服务端抓不到，已在本地抓到 X」。

#### 搜索 + 抓取 + 发布（三个 skill 串起来）

```bash
# Step 1：browser-web-search 拿 URL 列表
bws zhihu/search "AI Search" --count 3

# Step 2：先试服务端（多数站能成）
scripts/run.js draft <url1>

# Step 3：服务端失败的 URL，转用本地 news-to-markdown-skill 抓
node <path-to>/news-to-markdown-skill/scripts/run.js convert \
  --url <url-failed> --download-images --output-dir ./drafts/x
```

## 前置要求

本 skill 自身只做凭证管理 + HTTP，对话式两步接入即可（见下面 1 / 2）。但要让 AI Agent 在「服务端抓不到」时能正常回退，**用户必须另外在本机安装 `news-to-markdown-skill`**：

| 配套 skill | 作用 | 安装方式（用户本机） | 是否硬依赖 |
|---|---|---|---|
| [`news-to-markdown-skill`](https://github.com/sipingme/news-to-markdown-skill) | 用本机 IP / 真实 Chrome 把 URL 抓成 Markdown，绕开云端 IP 被反爬挡的问题 | `npm install -g news-to-markdown@3.3.1` + 把 skill 仓库 clone 到本地，由 Hermes / Cursor / OpenClaw 等 AI Agent 直接 `node scripts/run.js convert ...` 调用 | **强烈推荐**（不装则反爬站点完全无法发布） |
| [`browser-web-search`](https://github.com/sipingme/browser-web-search-skill) | 关键词 → URL 列表 | 见 skill 文档 | 可选（用户只有话题没具体 URL 时） |

> AI Agent 注意：`news-to-markdown-skill` 一定要装在 **用户本机**，不能在云端环境里跑——否则就跟 web-publisher 服务端一样被反爬挡。Hermes 之类的本地 Agent 会直接拿到用户家庭 / 办公出口 IP，是这条回退路径的关键。

### 1. 首次登录（0.9.0 checkpoint 流程）

用户说「帮我登录」→ AI 调 `scripts/run.js login` → 命令 ~0.3s 退出，stderr 类似：

```
请在浏览器中打开以下链接，确认绑定到你的账号：
  https://tools.siping.me/skill/bind?code=ABCD-EFGH
  绑定码：ABCD-EFGH
  有效期：5 分钟

等用户在浏览器点完"确认绑定"后，运行下面任意一条命令完成登录：
  web-publisher login-status     ← 推荐。会自动拉取凭证并写入 /Users/.../.web-publisher/credentials.json
  web-publisher whoami           ← 仅在已 login-status 成功后查询账号信息
```

stdout 是机器可读的 JSON（`success / pendingCheckpoint / verifyUrl / userCode / expiresInSec / expiresAt / pendingPath / credentialsPath / instruction`）。

AI 接下来要做：

1. 把 stdout 里的 `verifyUrl` **完整 URL 原文**贴给用户，附上 `userCode`。
2. 等用户回来说"点完了"。
3. 调 `scripts/run.js login-status`：
   - `state == "logged-in"` → 报"已登录，账号 = `<name>`，公众号已就绪，可以使用 draft / publish / convert"
   - `state == "logged-in-no-wechat"` → 看 stdout `wechat.appId`：非 null 时报"已登录，但 AppSecret 还没填好（AppID `<id>` 已留过）"，null 时报"已登录，但还没绑定公众号 AppID/AppSecret"。**两种情况都要 AI 自己立即调用** `scripts/run.js wechat config`，把它返回的 `url` **完整原文**交给用户填写——**不是**把"运行 wechat config 这条命令"作为指令贴给用户。**同时**把 `wechat config` 输出的 `serverIps` 数组里的所有 IP 也告诉用户，明确指引"到 mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单 加入"——漏掉这一步用户填完表单也发不了文章
   - 其他 state 见上面《登录流程（AI 必看）》

   **这一步（login-status）是凭证真正落盘的时机**——0.9.x 没有后台进程，不主动调 login-status，凭证永远不会被拉下来。

> 0.9.x 的 checkpoint 文件在 `~/.web-publisher/login-pending.json` (mode 0600)，5 分钟过期；过期后 `login-status` 会自动清理并返回 `expired-pending`。

### 2. 配置微信公众号

用户说「帮我配置公众号」→ AI 调 `scripts/run.js wechat config`。这一步同时给用户**两份信息**，AI 必须**两份都转达**，不能只发一份：

1. **浏览器短链**（来自 stdout JSON `url` 字段）——用户在该页填 AppID / AppSecret 提交（AppSecret 直接 POST 到服务端 AES-256-GCM 加密落库，永不进入对话上下文）。
2. **服务器 IP 白名单**（来自 stdout JSON `serverIps` 数组）——用户必须登录 [mp.weixin.qq.com](https://mp.weixin.qq.com) → 设置与开发 → 基本配置 → IP 白名单，把上面所有 IP 加进去。**这一步只能在公众号官方后台完成，CLI / 服务端都无法替代**。

漏掉第 ② 步是新手最常见的踩坑：AppID/AppSecret 表单填得再对，调 `draft` / `publish` 也会被微信以 `invalid ip, not in whitelist` 拒绝。`wechat config` 的 stdout JSON `instruction` 字段已经把"短链 + IP 白名单 + 后台路径"打包成一段话，照念即可。

如果 `serverIps` 数组为空，说明服务端的 `WECHAT_SERVER_IPS` 环境变量没设——这是服务端配置缺失，AI 要提醒用户向管理员索取服务器出口 IP，再自行加白名单。

### 3.（专业版及以上可选）配置页眉页脚

用户说「每篇文章末尾自动加我的二维码」「文章开头加关注引导」→ AI 调 `scripts/run.js wrapper config` → 把短链交给用户，让用户在浏览器表单里编辑 **Markdown 格式**的页眉（拼到正文最前）和页脚（拼到正文最后），保存后默认启用。

页眉页脚会在 `--rewrite` **之后**、推送给微信草稿/发布之前由 pipeline 拼接：用户页眉/页脚不会被 AI 改写。`wrapper off` 不删内容，只是临时停用；下次 `wrapper on` 即恢复。

### （可选）环境变量

仅 CI / 无浏览器场景使用：

| 变量 | 说明 |
|---|---|
| `WEB_PUBLISHER_TOOLS_URL` | 账号 API（默认 `https://tools.siping.me/api`） |
| `WEB_PUBLISHER_API_URL` | pipeline API（登录后凭证文件里也会带） |
| `WEB_PUBLISHER_USER_ID` | 用户 ID（如 `usr_xxxx`） |
| `WEB_PUBLISHER_API_KEY` | API Key |

**优先级（0.9.4 起反转）**：`~/.web-publisher/credentials.json` **优先于** 上述环境变量。

- 0.9.3 及之前：env > file，导致老的 `WEB_PUBLISHER_*` 残留（比如 OpenClaw 配置里）会静默盖掉新登录写出来的凭证，新 `login` 看上去"什么也没干"。
- 0.9.4 起：file > env。`web-publisher login → login-status` 写出的凭证立刻生效，env 自动让位。两者同时存在时 CLI 会在 stderr 打一条 `[warn]` 提醒。
- CI 想要 env 生效：先 `web-publisher logout` 删除本地凭证，或确保运行环境里 `~/.web-publisher/credentials.json` 不存在。

## 命令参考

```bash
# 账号
scripts/run.js login              # 第一步：拿短链 + 写 pending checkpoint，~0.3s 退出
scripts/run.js login-status       # 第二步：用户在浏览器点确认后，由本命令拉凭证
scripts/run.js logout             # 撤销 apiKey + 删本地凭证
scripts/run.js whoami             # 当前账号 + 微信配置 + 余额

# 公众号
scripts/run.js wechat config      # 浏览器表单填 AppID/AppSecret
scripts/run.js wechat status      # configured ? appId

# 页眉页脚（每篇文章自动拼接前后内容）
scripts/run.js wrapper config     # 浏览器表单编辑页眉/页脚
scripts/run.js wrapper status     # configured / enabled / 字符数 / 版本
scripts/run.js wrapper on         # 启用页眉页脚
scripts/run.js wrapper off        # 关闭页眉页脚（保留内容）

# 发布（<input> 可以是 URL 或本地文件路径）
scripts/run.js draft   <input> [options]   # 创建草稿（默认）
scripts/run.js publish <input> [options]   # 直接发布
scripts/run.js ppt draft <file> [options]  # PDF/PPTX → Markdown → 公众号草稿
scripts/run.js ppt publish <file> [options] # PDF/PPTX → Markdown → 直接发布
scripts/run.js status  <jobId>             # 查任务进度

# 文档转 Markdown（不发布）
scripts/run.js convert <input> [--out <file>] [--async] [--timeout <ms>]

# 帮助
scripts/run.js help
```

### 发布选项

| 选项 | 默认 | 说明 |
|---|---|---|
| `--theme <id>` | `blackink` | 主题 ID（见下表） |
| `--rewrite` | 关闭 | 启用 AI 改写 / 创作。**按用户等级自动路由引擎**：免费版 / 入门版走 `markdown-ai-rewriter`（minimax 分段伪改写，保结构）；专业版及以上、或 `isAdmin=true` 走 `markdown-ai-creator`（deepseek 原创合成，更贴近"自己写一篇"，会带上 source URL 溯源）。具体当前账号走哪个引擎可以用 `whoami` 看 `plan.rewriteEngine` |
| `--style <name>` | `casual` | 配合 `--rewrite`：`casual` / `formal` / `technical` / `creative`。两种引擎都接受同一组 style，但 creator 引擎里 style 是"语气 hint"而不是硬约束 |
| `--prompt "<text>"` | — | 自定义改写提示，覆盖 `--style` |
| `--cover` | 关闭 | **仅 creator 引擎**：额外生成一张封面图（minimax `image-01`，~ 0.05 元/张），返回字段 `coverImageUrl`。**v0.9.7+ 起 server 自动把 minimax 临时 URL 下载到本地图床**——24h 过期问题解决，调用方拿到的 cover 路径已经是 wechat-md-publisher 能上永久素材的 stable 路径 |
| `--cover-style "<text>"` | — | 配合 `--cover`：封面风格 hint，例如 `"赛博朋克 霓虹 高对比"`；不传走"现代简洁公众号头图"默认 |
| `--regenerate-images` | 关闭 | **仅 creator 引擎**：把分类判定为带水印 / 文字截图 的正文图换成 t2i 重生成版本。每张图同样消耗 minimax image-01 配额。**v0.9.7+ 起同样会本地化转存**。失败自动退化为 `*图：alt*` 注脚 |
| `--no-image-classify` | — | 关闭启发式图片分类（默认开）。开启时：404 / 反爬挡 / 头条等带水印图床 / 过小 icon / 极端比例 banner 都会自动替换为 `*图：alt*` 注脚，不影响 LLM 写作 |
| `--enable-ocr` | 关闭 | 在分类时启用 OCR 增强水印识别（要求服务器装了 `tesseract.js`，目前 optionalDependencies 默认装了；首次模型加载较慢，~30s——server 端 `ENABLE_OCR_WARMUP=true` 时启动期预热可消除）。命中"水印"/"出处"/"今日头条"等关键词、或截图里文字过多会被判 `caption-only` |
| `--lock-title` | 关闭 | **v0.9.7+，仅 creator 引擎**：锁死最终标题。LLM 即使想加副标题 / 改成问句 / 加 emoji，也会被服务端强制改回原 title。适用于热搜稿、SEO 命题作文。要求输入有 title（URL 抓取 / 文档转换会自动提取）。如果输入没 title，server 会忽略此 flag |
| `--append-source-footer auto\|always\|never` | `auto` | **v0.9.7+，仅 creator 引擎**：控制文末"原文：[…](url)" 链接列表追加策略。`auto` = LLM 一份 source 都没引用时才追加（兜底防漏）；`always` = 每次都追加（合规审计）；`never` = 完全关掉（翻译 / 二创场景 footer 太显眼） |

### 改写返回里的诊断字段（v0.9.7+）

`draft` / `publish` 完成后 stdout JSON 会自动包含来自 server `jobs.metadata.dispatch` 的诊断信息（仅 creator 引擎产生）：

```json
{
  "success": true,
  "title": "...",
  "warnings": [
    "lockTitle: H1 mismatch was rewritten to \"我的标题\"",
    "source[0] (https://example.com/long): truncated from 25430 to 12000 chars"
  ],
  "cost": {
    "tokens": { "total": 4521 },
    "imagesGenerated": 1,
    "estimatedRMB": 0.149,
    "trace": [{ "provider": "minimax", "ok": true }]
  },
  "imageStabilize": { "downloaded": 1, "failed": 0, "skipped": 3 },
  "imageClassify": { "safe": 2, "has-watermark": 1, "too-small": 1 }
}
```

- `warnings`：creator 包级告警（标题改写、source 截断、image-stabilize 失败、imageStrategy 失败）；任一不为空时 AI 应转告用户
- `cost.estimatedRMB`：本次预估花费（粗略，仅 LLM tokens + t2i 图片单价；网络/server 成本不计）。**仅作量级提示，不是账单**——真实账单以 minimax / openai 后台为准
- `cost.trace`：哪些 provider 被尝试了（5xx/429 时会切到下一个）。`ok=false` 表示 fallback 命中，应该提醒运维
- `imageStabilize`：临时图床转存结果。`failed > 0` 时图依然能发出去（保留原 URL），但 24h 后会过期
- `imageClassify`：启发式分类摘要

### convert 选项

| 选项 | 默认 | 说明 |
|---|---|---|
| `--out <file>` | — | 把 markdown 写到该文件（stdout 只回 JSON 摘要 `{success, input, out, byteLength, durationMs}`，不灌大段正文） |
| `--async` | 关闭 | 走 `/convert/async`，CLI 自动轮询；适合学术 PDF / 扫描件等可能跑 5–10 分钟的转换 |
| `--timeout <ms>` | 服务端 5min | 单次转换超时；服务端封顶 600000 (10min)，超过仍按 600000 处理 |

**可用主题**（用户说"墨黑/橙日/紫雨"等中文名时，自动映射到对应 ID）：

| ID | 中文名 | 风格 |
|---|---|---|
| `blackink` | 墨黑（默认） | 深色模式，靛蓝点缀，适合夜间 / 科技类 |
| `default` | 默认主题 | 简洁清爽，适合各类文章 |
| `orangesun` | 橙日 | 温暖明亮的橙色阳光主题 |
| `redruby` | 红宝石 | 优雅大气的宝石红主题 |
| `greenmint` | 薄荷绿 | 清新舒缓的薄荷绿主题 |
| `purplerain` | 紫雨 | 梦幻渐变的紫色主题 |

### 调用样例

```bash
# URL → 草稿 / 发布
scripts/run.js draft   https://mp.weixin.qq.com/s/xxxxx
scripts/run.js draft   https://zhuanlan.zhihu.com/p/xxx --theme orangesun
scripts/run.js draft   https://36kr.com/p/xxx --rewrite --style casual
scripts/run.js publish https://example.com/article

# 本地 PDF/PPTX → 公众号
scripts/run.js draft       ~/Downloads/report.pdf              # PDF 默认：每页成图 → 公众号
scripts/run.js draft       ~/Downloads/report.pdf --extract-text  # PPTX 抽可编辑文字
scripts/run.js draft       ~/Downloads/report.pdf --as-markdown   # PDF 直接 markitdown → 公众号
scripts/run.js ppt draft   ./deck.pptx                         # PPTX 默认：导读+每页成图
scripts/run.js draft       ~/Downloads/slide.pptx --as-markdown  # PPTX 纯文字
scripts/run.js draft       ~/Downloads/slide.pptx --rewrite --style technical --cover
                                             # 高级改写 → /pipeline

# 本地其他文档 → 草稿（仍走 /pipeline）
scripts/run.js draft   ./papers/whitepaper.docx

# 任意文档 → markdown（不发布）
scripts/run.js convert ./report.pdf                    # markdown 全文回到 stdout
scripts/run.js convert ./report.pdf --out report.md    # 写文件，stdout 只回摘要
scripts/run.js convert https://arxiv.org/pdf/2401.00001.pdf --async --out paper.md
scripts/run.js convert ./meeting.mp3 --async           # 音频转录（服务端装了对应插件时）

# 查状态
scripts/run.js status  job_abc123
```

## 支持平台

**发布目标**：微信公众号（草稿 / 直接发布）。其他平台规划中。

**内容来源 1：URL**（服务端 news-to-markdown 自动选适配器）：

| 平台 | 适配器 | 配合 `bws <平台>/search` |
|---|---|---|
| 微信公众号 | ✅ | ✅ |
| 今日头条 | ✅ | ✅ |
| 知乎 | ✅ | ✅ |
| 36kr | ✅ | ✅ |
| CSDN | ✅ | ✅ |
| 小红书 | ✅ | ✅（部分内容需登录） |
| 人人都是产品经理 | ✅ | — |
| 任意网页 | ✅ 通用 readability | — |

**内容来源 2：本地文件 / 文档型 URL**（服务端 [Microsoft markitdown](https://github.com/microsoft/markitdown) 处理）：

`.pdf` / `.docx` / `.pptx` / `.xlsx` / `.epub` / `.csv` / `.tsv` / `.html` / `.md` / `.txt` / 常见图片 (`.png` `.jpg` `.webp` `.gif`) / 常见音频 (`.mp3` `.wav` `.m4a`，服务端装了 markitdown 音频插件时)；URL 末尾扩展名命中文档格式时自动走 markitdown 而不是 readability。

## 工作原理

```
draft / publish (URL):              draft / publish / ppt (PDF|PPTX):
  URL ──▶ POST /pipeline              PDF ──▶ POST /ppt/jobs (page_images 默认)
                                              │ 每页 PNG → 公众号
                                              PDF + --extract-text
                                              │ pingPPT → PPTX → markitdown 抽文字
                                              PDF + --as-markdown / --rewrite
                                              PPTX ──▶ POST /ppt/jobs (page_images 默认)
                                                    └─ --as-markdown → markdown
                                              或 POST /pipeline (高级改写选项)
         │                                       │
         ├─ news-to-markdown  (URL)              ├─ markdown: 原 PDF/PPTX 直接 markitdown
         ├─ markitdown        (其他文档)          └─ page_images: PDF 每页成图
         ...                                     wechat draft/publish
                ▼                                       ▼
         返回 jobId；completed 时 mediaId / publishId

convert:
  URL 或文件 ──▶ POST /convert (sync)  或  /convert/async (async)
         └─ 只返回 markdown，不推公众号
```

CLI 端只做**凭证管理 + HTTP 调用 + 本地文件读字节 + multipart 上传**，没有任何抓取 / 解析 / 图片下载 / 文档转换逻辑，也不安装任何 npm 包；本地文件通过 Node 18 内建的 `FormData` / `Blob` 流式上传到服务端，basename 之外的本地路径不会出网络。

## 安全与信任

- **数据流**：
  - URL 模式：CLI 把 `{url, action, theme, rewrite?}` + 你的 API Key 发给服务端；服务端自行抓取目标网页全文与图片，并发布到微信。⚠️ **服务端会接收原始 URL 并下载全文 + 图片**。
  - 本地 PDF/PPTX（`draft|publish|ppt <path>`）：默认 **POST `/ppt/jobs` + page_images**（导读+每页成图）；PDF `--extract-text` 走 pingPPT PPTX 抽文字；`--as-markdown` / `--rewrite` 时走 markitdown 文字路径。完成时返回 `mediaId` / `publishId`，**不返回 PPT 下载链接**。
- **AppSecret**：永不进入对话上下文；浏览器表单直传服务端，AES-256-GCM 加密落库。
- **apiKey**：device_code 在绑定成功后立刻 consumed，一次性下发；`logout` 远端撤销 + 删本地。
- **本地凭证**：`~/.web-publisher/credentials.json`（mode 0600）。
- **IP 白名单**：mp.weixin.qq.com 后台授权远程服务器 IP 直接调微信 API；请确认你信任该 IP 归属方（[tools.siping.me](https://tools.siping.me)）。
- **审计**：所有操作记录可在 tools.siping.me 个人页面查看；源码 [github.com/sipingme/web-publisher-skill](https://github.com/sipingme/web-publisher-skill)。
