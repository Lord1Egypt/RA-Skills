---
name: shareone
description: Host HTML/Markdown pages and share PDF, Word, or PowerPoint docs as ShareOne short links. Use for publishing, passwords/watermarks, comments, downloads, updates, or Git-backed remote sources for ShareOne content.
license: MIT
metadata:
  slug: shareone
  display-name: ShareOne
  version: 1.11.1
  summary: Host HTML pages and share PDF/Word/PPT docs with short links
  tags:
    - shareone
    - publish
    - sharing
    - hosting
    - html
    - upload
---

# AI Agent 技能：发布到 ShareOne (shareone)

Host HTML/Markdown pages and share PDF, Word, and PowerPoint documents with ShareOne public short links. Covers page publishing, document sharing, password protection, watermarks, review comments, downloads, and updates to existing shares.

这个 Skill 允许 AI Agent 将当前生成的历史会话以及 HTML/Markdown/TXT/PDF/PPT 等文件发布到 ShareOne 线上托管服务，并为用户生成一个持久化的公网分享链接；也可以对已有 ShareOne 链接执行下载、内容更新、设置修改和评论处理。

## 内容版本管理决策

ShareOne 复用 **GitHub / GitLab 的内容版本管理**：历史、diff、分支、评审和回退在源仓库完成，ShareOne 负责展示、分享、访问控制和评论协作。`remote_url` 的 snapshot 是当前缓存，ShareOne 不维护独立的文件版本库。

评论目标重新绑定是独立的协作记录，不是文件版本管理。原始 `quote` / `highlighter_data` 保留；有 `anchor_binding` 时，其目标才是当前有效绑定。查看或处理评论先读对应评论工作流；用户明确要求重绑时再读 [workflows/comment-reattachment.md](workflows/comment-reattachment.md)。不要猜测未记录的历史选区，也不要自动迁移旧评论。

远程文本源支持完整 UTF-8 原生 HTML，下载上限为 **16 MiB（16,777,216 字节）**。发布前 AI 审核当前默认暂停，普通新内容沿原发布接口完成；是否启用以服务端为准。已有复核记录和最终决定继续有效。实际返回 `CONTENT_REVIEW_REQUIRED` 或内容拒绝时，保留原链接和记录，并读取 [workflows/content-review.md](workflows/content-review.md)。不要为解除已有候选的阻断改内容包装、MIME、门禁、身份或上传入口。

涉及 ShareOne 内容的 Git 源、版本选择、历史或回退时，先读 [workflows/git-backed-versions.md](workflows/git-backed-versions.md)，再按下方路由执行发布、刷新或评论处理。该工作流包含跟随分支、固定 commit、切换版本与验收命令。**当前可直接使用公开 GitHub 文本文件；GitLab 和私有仓库认证仍需接入，不能把产品方向当作已支持能力。** 普通本地文件上传仍按原流程执行，不自行迁移到 Git。

## 脚本执行基准

本文档中所有 `node scripts/xxx.js` 命令的路径都以 **本 skill 的安装目录**（即本 `SKILL.md` 所在目录）为基准。当前工作目录通常是用户的项目目录，直接执行相对路径会失败。执行前先确定 skill 目录，使用绝对路径或先 `cd` 到 skill 目录，例如：

```bash
node /path/to/shareone-skill/scripts/ensure_credentials.js
```

## 入口隔离规则

本 skill 和用户本机可能安装的 `shareone` CLI 是两个独立入口。除非用户明确要求”使用 CLI”或指定执行 `shareone ...` 命令，否则不要调用系统 PATH 中的 `shareone` 命令。即使 `which shareone` 能找到 CLI，也不要把自然语言的发布、下载、评论处理任务改走 CLI。所有 ShareOne 操作都必须调用本 skill 目录内 `scripts/` 下的脚本。

## 使用说明与触发条件

当用户表达出以下意图时，应主动使用此技能：

- "帮我把 `index.html` 发布到 ShareOne"
- "把我刚才生成的网页发布，给我个链接"
- "生成一个可分享的链接给我的团队看"
- "Upload this presentation to ShareOne and protect it with password 'secret'"
- "发布这个 PDF 到 ShareOne，并加上密码 1234"
- "把这个网页发布到 ShareOne，加上水印 '内部绝密'"
- "把这个网页发布到 ShareOne，链接叫 product-demo"
- "发布这份设计稿并开启协同评论模式"
- "用 shareone 分享上一轮对话"
- "把我刚才写的代码/大段文字分享出去"
- "Share your last response as a note"
- "帮我下载这个 ShareOne 链接的文件：https://s.shareone.vip/s/xxx"
- "拉取一下这个链接的评论：https://s.shareone.vip/s/xxx"
- "删掉/删除这个 ShareOne 链接：https://s.shareone.vip/s/xxx"
- "我 push 了，刷新一下这个 ShareOne 远程链接的内容：https://s.shareone.vip/s/xxx"
- "给这个 ShareOne 链接加水印：https://s.shareone.vip/s/xxx"
- "根据这个链接的评论修改页面：https://s.shareone.vip/s/xxx"
- "修改这个 ShareOne 链接的内容：https://s.shareone.vip/s/xxx"
- "把这个 GitHub 文件发布到 ShareOne：https://github.com/org/repo/blob/main/report.html"
- "用远程 URL 发布这个页面"
- "Publish this GitHub raw URL to ShareOne"

## 路由判定顺序（唯一路由依据）

入口文件只负责判断用户意图、选择需要阅读的 workflow。不要一次性读取所有 `workflows/*.md`；只读取当前任务命中的子文件。

持续监听评论、接收持久通知或唤醒 scode / 其他 Agent：先读 `workflows/environment-and-credentials.md`，再读 `workflows/agent-notifications.md`，使用 `scripts/agent_watch.js`。普通评论查看和单次处理按以下路由执行，不启动常驻监听。

按以下顺序从上到下判断，**命中第一条即停止**，按该条给出的阅读顺序执行：

1. **删除/清除/移除/重置 ShareOne API Key**
   → 读 `workflows/delete-api-key.md`。无需凭据检查。

2. **删除/移除 ShareOne 分享链接本身（用户明确要求“删掉/删除/移除”某个 share_id、slug 或链接）**
   → 先读 `workflows/environment-and-credentials.md`，再读 `workflows/delete-share.md`。删除是 owner-only 操作，执行前须与用户确认（软删除后公开链接立即失效）。对 HTML/文本页和二进制文件链接（`/pdf/`、`/ppt/`、`/word/`）通用。注意与第 6 条区分：本条是删除整个 share，不是改设置。

3. **刷新 remote-url auto-follow 分享的源内容（用户说“我 push 了”“拉一下最新源”“刷新这个远程链接”）**
   → 先读 `workflows/environment-and-credentials.md`，再读 `workflows/refresh-remote.md`。remote 页面刷新是懒的、只在打开渲染页时触发，下载/`/file` 只服务缓存；本条用 `refresh_share.js` 显式强制 refetch。仅对绑定了远程 URL 的分享有效；非 remote-bound 返回 `NOT_REMOTE_BOUND`，此时应改走第 6 或第 10 条（改设置 / 重新发布内容）。

4. **绑定账号、注册、升级 guest、绑定邮箱**
   → 先读 `workflows/environment-and-credentials.md`，再读 `workflows/bind-account.md`。

5. **让别人一起编辑、分享编辑权限、添加/移除/查看协作者、对方怎么拿 API Key**
   → 先读 `workflows/environment-and-credentials.md`，再读 `workflows/manage-collaborators.md`，最后读 `workflows/result-and-errors.md`。

6. **用户提供已有 ShareOne 链接、`share_id` 或 slug，且只要求修改水印、访问密码、自定义短链接、评论开关或数据存储开关（不改内容本身）**
   → 先读 `workflows/environment-and-credentials.md`，再读 `workflows/update-share-settings.md`，最后读 `workflows/result-and-errors.md`。
   这是元数据更新：不要按文件类型路由，不要下载源文件，不要使用 `publish.js`，不要重新上传内容。对二进制文件链接（`/pdf/`、`/ppt/`、`/word/`）同样适用本条。

7. **下载 ShareOne 链接的文件或取回源内容**
   → 读 `workflows/download-file.md`。下载脚本会在已有凭据时优先尝试 owner 下载，没有凭据时自动走公开下载；不要为了普通下载强制配置 API Key。

8. **只查看、拉取、总结 ShareOne 链接评论（用户没有要求修改）**
   → 读 `workflows/comments-view.md`。单次查看用 `comment_list.js`，走公开接口，无需凭据检查；维护评论缓存时使用该 workflow 的增量查询步骤。

9. **处理评论、根据评论修改页面、修复 ShareOne 链接内容**
   → 先读 `workflows/environment-and-credentials.md`，再读 `workflows/comments-process.md`（其中的重新发布步骤会引用 `workflows/publish-text-page.md`），最后读 `workflows/result-and-errors.md`。

10. **发布、分享、生成链接、上线（创建新链接或更新已有链接的内容）**
   → 先读 `workflows/environment-and-credentials.md`，再按目标文件类型二选一，最后读 `workflows/result-and-errors.md`：
   - `.ppt`、`.pptx`、`.pdf`、`.doc`、`.docx` → `workflows/publish-binary-file.md`
   - `.html`、`.md`、`.txt`、对话内容、大段文本、代码块、已包装成 HTML 的内容 → `workflows/publish-text-page.md`。注意：`.md`/`.txt` 一律按原格式发布，不要因为内容包含图表就转成 HTML；只有目标本来就是 HTML 页面时才参考其中的 Mermaid.js 章节。

所有需要 ShareOne API 的操作（上面第 2、3、4、5、6、7、9、10 条），都先运行 `node scripts/ensure_credentials.js`，输出 token 含义与处理流程见 `workflows/environment-and-credentials.md`，这里不重复。

## ShareOne 链接与 share_id

- 用户提供的目标可以是完整链接、`/s/<ref>` 等路径、裸 `share_id`（16 位字符串）或自定义短链 slug。服务端接口同时接受 `share_id` 和 slug，无需自行区分两者。
- `/s/<share_id>` 是最终给用户访问的分享链接，**不是上传 API endpoint**。不要把 `/s/<share_id>` 当作发布地址，也不要直接向 `/s/<share_id>` PUT/POST 文件。
- 路径前缀与内容类型的对应关系：`/s/`、`/md/` 是文本/HTML/Markdown 页面；`/pdf/`、`/ppt/`、`/word/` 是二进制文件。元数据更新时 `update_share_settings.js` 会按此前缀自动选择 endpoint，裸 `share_id` 或 slug 由脚本先试页面 endpoint、必要时回退文件 endpoint，整个过程不下载源文件。
- 文本页里 `/s/<ref>` 与 `/md/<ref>` **等价**：前缀不绑定、也不校验内容类型，浏览路由一律按 ref 解析 share、按 share 真实 content-type 渲染。因此文本页可以就地把 content-type 从 md 升级成 html（`.md → .html`，如把 ASCII 图升级成 Mermaid），URL（含老的 `/md/<slug>`）一字不变、评论保留——见 `workflows/publish-text-page.md` §6b。升级用 `--share-id` 更新，**绝不 `--force-new`**。
- 本地文件发布与更新统一使用 `publish.js`，脚本按文件类型自动分发（stderr 输出 `INFO:CHANNEL:text|binary`）。远程源例外：使用 `upload_page.js --remote-url` 创建或更换源 URL，`refresh_share.js` 刷新已有源。不要因为会话里存在旧的 `/s/<share_id>` 就把二进制文件改走文本页面 PUT；二进制文件传 `--share-id` 会被脚本拒绝（`ERROR:BINARY_NO_SHARE_ID`）。
- 如果当前会话中已经为同一个文本/HTML 文件生成过 ShareOne 链接，可复用之前的 `share_id` 执行文本页面 PUT 更新；否则执行首次创建。
- 非 owner 下载要求链接已开启允许下载；若脚本输出 `ERROR:DOWNLOAD_NOT_ALLOWED`，直接提示用户让链接 owner 先开启允许下载。

## 发布前安全自检（非阻塞）

- 创建新分享链接（首次 POST 新页面或首次上传新文件）前，Agent 必须自行做内容安全自检：不得发布明显反动、涉政、暴力、色情、侵权或恶意代码内容。
- 链接保留规则：普通链接在**最后活跃时间**超过 90 天后会被清理（最后活跃 = 创建时间或最后一次被访问时间的较晚者，持续有效访问会一直保持有效，不是发布后 90 天硬删除）；发布到 Explore 公开广场、被知识库引用、或设了 `remote_url` 的内容不参与此无活跃自动清理。
- 自检通过后直接继续发布，不要向用户展示安全提示，也不要等待用户回复“同意”或 `agree`。
- 自检必须轻量：对文本/HTML/Markdown/TXT，只基于当前已知内容或发布所需读取的文本内容判断；对 PDF/PPT/Word 等二进制文件，只基于用户请求、文件名、扩展名和显式参数判断，不要为了自检提取正文、OCR、转换格式或解析文件内部内容。
- 如果内容明显违反上述规则，停止发布并简要说明原因。
- 对已有链接执行后续操作时——包括内容 PUT 更新、评论处理闭环中的重新发布、水印/密码/短链/评论开关等元数据修改——按对应 workflow 直接执行。
- 下载、查看评论、删除 API Key 等不发布内容的操作无需安全自检。

## 不可跳过的阻塞步骤

以下步骤是阻塞性用户通知，不是可选说明。触发后必须先发给用户，再继续后续操作。

- 如果 `ensure_credentials.js --create-guest` 或底层 `create_guest_key.js` 输出 `GUEST_KEY_CREATED:<api_key>`，必须立即向用户发送临时 API Key、绑定账号链接和保存提醒（话术见 `workflows/environment-and-credentials.md`）。即使 key 已经自动保存，也不能省略该通知；发送前不得继续执行原任务的上传、下载、评论处理命令。
- 本会话首次向用户展示生成的 `share_url` 时，必须按 `workflows/result-and-errors.md` 提示所有未使用的高级功能：自定义短链接名称、访问密码、水印。已使用的能力不再提示；三项都已使用则不提示。

## 全局约束

- 发布前必须完成凭据检查和必要的凭据配置。
- 发布成功后必须直接使用脚本返回的 `share_url`，不要自行拼接分享链接；不要展示备用链接。
- 只有当用户明确要求开启评论、允许讨论或协同模式时，才添加 `--allow-comments true`。默认不开启评论。
- 只有当用户明确要求页面持久化数据（如保存游戏分数、表单状态）时，才添加 `--allow-data true`。默认不开启数据存储。
- 页面持久化数据时，页面代码用自动注入的 `window.__SHAREONE__` SDK，**必须按敏感度二选一、无默认**：`putShared(key, value|File)` 存服务器·所有访客可读·跨设备（大文件自动走 blob，≤8MB）；`putPrivate(key, value|File)` 只存这台设备·私有·不上传。命名即风险（Shared=别人能看），敏感/隐私数据一律 `putPrivate`。现成的“公开 vs 敏感”拖拽上传参考页：`templates/page-storage-dropzone.html`；私有数据可留在本机就地推理（模型公开＋数据 `putPrivate`＋页面内计算，字节不出设备）的参考页：`templates/client-side-inference.html`；完整 SDK 见后端 `agent.md` §14。发布时若带 `--allow-data true`，命令行会在成功后打印一行 `HINT:PAGE_DATA_ENABLED` 提示该二选一与本地推理用法。
- 自定义短链接（slug）：服务端会根据文件名自动生成可读的 slug（如 `quarterly-report`），客户端无需额外操作。只有用户明确要求“链接叫 xxx”、“自定义短链接 xxx”、“URL 后缀 xxx”时，才在发布命令添加 `--slug xxx` 覆盖自动生成；slug 冲突时把服务端提示反馈给用户，不要静默改名。
- 页面需要二维码时用 `node scripts/make_qr.js --text "<内容>" --format path`（零依赖，直出 SVG path，贴进页面的 `<path d="...">`；`--format svg` 给完整 `<svg>`，`--ecc L|M|Q|H` 默认 Q）。**不要**引入外部二维码库或 `<img src="https://...qrserver...">` 之类的在线生成服务——发布出去的页面在别人的浏览器里打开，外链会失效、泄露访问者，也印不进 PDF。二维码指向本次发布的链接时，先用 `--slug` 定好链接再生成二维码，顺序反了码会指向不存在的页面。
- 名片/电子名片：用 `templates/business-card.html`（双面设计，一份 HTML 同时产出可发的图片、可扫的链接、90×54mm 印刷 PDF）。改 `data-field="..."` 的文字即可，vCard 和 tel:/mailto: 由页面脚本从卡面读取，不要另写一份联系方式。二维码指向名片页本身而不是公司官网：扫码的人当场要的是把人存进通讯录，名片页能一键存 vCard，且印出去的卡改不了、名片页能随时更新。
- 开启评论的页面**不要用 MutationObserver 监听自己的输出来触发重绘**。ShareOne 会往页面里注入评论桥（样式、覆盖层、高亮包裹），这本身就是 DOM 变化；页面若据此重绘、重绘又改 DOM，会自持成无限循环，页面直接跑飞（实测：关评论 render 1 次，开评论 502 次）。确实需要按变化重绘时，用内容签名门控：先算出这一帧该画什么，和上一帧比，一样就不画。同理，**不要在 `pointerdown` 里无条件 `setPointerCapture`** —— 指针被容器捕获后，`click` 会派发给捕获者而不是被点的元素，页面里所有节点都点不动，而元素还在、`elementFromPoint` 也正常，很难查；平移交互应等 `pointermove` 超过 3–5px 再捕获。
- 评论需要跨折叠、分页、语言或呈现方式追踪命名对象时，用 `window.__SHAREONE__.anchors` 声明稳定 ID，按 [动态页面与文字评论](workflows/publish-text-page.md#动态页面与文字评论) 接入选择、位置报告和恢复；canvas/地图/3D 等没有独立 DOM 的目标也使用它。`hidden` 表示目标确实存在但当前视图没画；`missing` 仅表示当前完整模型确认目标已不存在；未确定时报告 `pending`，不回答的 ID 也处于等待状态。侧栏区分这三种状态、旧文字无法定位和区域部分可用，并保留原文、回复和部分目标的状态。锚点只存稳定 ID 与阅读上下文，坐标和当前状态不落库。参考 `templates/canvas-comments.html`；完整接口见后端 `agent.md` §14b。
- 开启评论且页面会自己重绘（图表、流程图、看板、任何切换视图就重建 DOM 的页面）时，给每个可评论元素加一个稳定的 `data-*` id，例如 `<g class="node" data-node-id="委外cap">`。ShareOne 的区域评论以应用自己给的这个 id 作锚，重绘后评论自动跟回同一个元素；没有 id 时只能退回"第几个同名标签"的结构路径，重绘可能使它失效。id 在同一页内必须唯一（命中多个元素的 id 会被拒绝），且在重绘前后保持不变——用业务含义命名，别用渲染顺序生成。
- 生成或修改启用评论的动态 HTML 时，按 [publish-text-page.md 的动态页面要求](workflows/publish-text-page.md#动态页面与文字评论) 保留可阅读文本与稳定身份。文字锚点不索引 SCRIPT/STYLE/NOSCRIPT/TEMPLATE 或标注浮层；大体积数据保留完整，可放在 head 的非执行数据脚本中。性能验收保留评论，实际展开、缩放和拖动；文本定位失败只表示锚点不可用，不代表评论或原文已删除。
- 评论处理必须形成闭环：认领、修改源内容、同步原分享并验证，然后用 `comment_reply.js --state`（`--state` 必填）**明确表态**——`resolved-agree`（同意收敛）/ `open-disagree`（有异议但保持 open）/ `open-need-input`（需人类澄清）。绑定 Git 源的页面修改仓库后刷新，具体见 `comments-process.md` 和 `git-backed-versions.md`。AI **永不**单方面 dismiss 一条分歧：不同意用 `open-disagree`，`dismiss` 仅用于 owner 确认的无关或垃圾评论；定位失败、权限不足或等待同步时用 `open-need-input`。

## 最终回复前检查清单

在回复用户前，逐项检查：

- 如果本轮创建了临时 API Key，是否已经把 API Key、绑定账号链接和保存提醒发给用户。
- 如果本轮**创建了新分享链接**，是否已完成发布前安全自检；如果内容明显违规，是否已停止发布。
- 如果发布成功，是否直接展示返回的 `share_url`，没有自行拼接链接。
- 如果返回中包含 `custom_slug_warning` 或 `custom_slug_suggestions`，是否展示给用户。
- 如果这是本会话首次展示生成的 `share_url`，是否提示所有未使用的高级功能。
