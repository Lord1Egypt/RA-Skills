# 发布或更新文本/HTML 页面

当用户要发布对话、大段文本、代码、HTML、Markdown 或纯文本时读取本文件。发布前必须已经完成 `environment-and-credentials.md`。

适用文件类型：`.html`、`.md`、`.txt`。

不适用文件类型：`.ppt`、`.pptx`、`.pdf`、`.doc`、`.docx`、图片、zip 或其他二进制文件。遇到这些文件时，停止本 workflow，改读 `publish-binary-file.md`（那里的命令同样是 `publish.js`，但规则不同）。即使误判了类型，`publish.js` 也会自动把二进制文件分发到正确的上传通道，不会发错接口。

## 1. 识别目标内容与格式保持规则

格式保持是硬规则，优先于一切“展示更美观”的考虑：

- **凡是磁盘上已存在的 `.md`、`.txt`、`.html` 文件——无论是用户指定的，还是本会话中 AI 刚生成的——一律按原文件、原格式发布**。不要生成 `.html` 副本，不要转换格式。`.md` 文件中包含表格、流程描述、mermaid 代码块等可视化内容，也不构成转换成 HTML 的理由。
- 只有当用户**明确表达美化意图**（例如“美化一下”、“做成网页/页面”、“排个版再发”）时，才可以把内容包装为带基础样式的 HTML。除此之外的任何情况都不允许格式转换。
- 如果用户要求分享对话、大段文本或代码（内容尚未落盘）：从对话历史中提取完整文本或代码块，**默认保存为 `.md` 临时文件发布**（纯文本可用 `.txt`），例如 `share_note.md`；同样只有用户明确要求美化时才包装成 `.html`。
- 如果用户没有指定文件：根据上下文寻找最近一次生成或编辑的文本/HTML 文件，例如 `.html`、`.md`、`.txt`，并按上面的格式保持规则原样发布。
- 如果锁定的文件不存在，停止并告知用户。
- 如果锁定的文件是 `.ppt`、`.pptx`、`.pdf`、`.doc`、`.docx`、图片、zip 或其他二进制文件，停止本 workflow，改读 `publish-binary-file.md`。
- 提取用户可能要求的密码 (`password`)、水印 (`watermark`) 和自定义短链接后缀 (`slug`)。服务端会根据文件名自动生成可读的 slug，客户端无需主动设置。只有用户明确说”链接叫 xxx / 自定义短链接 xxx / URL 后缀 xxx”时才用 `--slug` 覆盖。

## 2. 发布前安全确认

发布前安全提示由入口 `SKILL.md` 统一描述：**首次创建新分享链接（POST）**前必须展示安全提示并获得用户明确回复“同意”或 `agree`；对本会话中已确认链接的 PUT 更新（含评论处理闭环中的重新发布）不需要重复确认。

## 3. 判断创建还是更新

检查对话上下文。如果当前会话中已经为同一个文件生成过 ShareOne 链接，提取之前的 `share_id`（16 位字符串）并执行 PUT 更新。

- 有 `share_id`：执行更新。
- 没有 `share_id`：执行首次创建。
- **例外（优先于上面两条）**：如果当前处于评论处理流程（`comments-process.md`），或当前目录存在 `.shareone_active_task` 文件，说明目标 share 已经确定——必须读取该文件内容作为 `share_id` 执行 PUT 更新，**禁止走首次创建**。“想不起 share_id”不等于“没有 share_id”。

脚本另有两道磁盘防线兜底，触发时按提示修正命令，不要绕过：

- `ERROR:ACTIVE_SHARE_TASK`：存在进行中的评论处理任务，必须用错误提示中的 `--share-id` 执行更新。
- `ERROR:FILE_PREVIOUSLY_PUBLISHED`：该文件此前发布过（记录在 `.shareone_history.json`），错误提示中带有原 `share_id`。默认用 `--share-id` 更新原链接；只有用户明确要求为同一文件再发一个新链接时才加 `--force-new`。

## 4. 文本页面发布规则

发布与更新统一使用 `publish.js`。脚本会按文件类型自动选择上传通道（文本走 pages JSON 接口，二进制走 `/api/v1/files` 直传），并在 stderr 输出 `INFO:CHANNEL:text|binary` 说明走了哪条通道——不需要自行判断，也不要直接调用底层的 `upload_page.js` / `shareone_upload.js`。

## 5. 首次创建 (POST)

执行：

```bash
node scripts/publish.js "<YOUR_FILE_PATH>" --filename "YOUR_FILE_NAME" [--password "OPTIONAL_PASSWORD"] [--watermark "OPTIONAL_WATERMARK"] [--slug "OPTIONAL_SLUG"] [--allow-comments true]
```

规则：

- Sudowork 环境不要传 `--api-key`。
- 普通 AI Agent 环境可传 `--api-key`，也可以依赖 `SHAREONE_API_KEY` 或本地凭证。
- 只有当用户明确要求“开启评论”、“允许讨论”、“协同模式”等时，才加 `--allow-comments true`。
- 默认不开启评论。
- 服务端根据文件名自动生成 slug，无需手动设置。只有当用户明确要求自定义短链接时，才加 `--slug` 覆盖。

## 6. 更新已有链接 (PUT)

如果用户只要求修改已有链接的水印、访问密码、自定义短链接或评论开关，不要执行本节，不要下载原文件；改读 `update-share-settings.md`，使用 `update_share_settings.js` 只更新元数据。

执行：

```bash
node scripts/publish.js "<YOUR_FILE_PATH>" --filename "YOUR_FILE_NAME" --share-id <YOUR_SHARE_ID> [--password "OPTIONAL_PASSWORD"] [--watermark "OPTIONAL_WATERMARK"] [--slug "OPTIONAL_SLUG"] [--allow-comments true/false]
```

规则：

- Sudowork 环境不要传 `--api-key`。
- 如果用户要求关闭评论协同或开启评论协同，可以在 PUT 更新时传入 `--allow-comments false` 或 `--allow-comments true`。
- 如果用户要求修改或清除密码/水印，可以传入 `--password` 或 `--watermark`。
- 如果用户要求修改自定义短链接，可以传入 `--slug`。
- 空字符串 `""` 表示清除对应设置。

## 7. 使用 Mermaid.js 绘制图表

**适用前提**：本章节只适用于目标内容本来就是 HTML 页面的场景——即用户提供的就是 HTML 文件，或用户明确要求美化/做成网页而新生成 HTML。**不要为了使用 Mermaid 而把 `.md`/`.txt` 文件转换成 HTML**；`.md` 里的图表内容按第 1 节的格式保持规则原文发布。

当 HTML 页面需要包含图表、流程图、时序图、思维导图等可视化内容时，优先使用 Mermaid.js 而非 CSS/字符串拼接的伪图表。Mermaid 渲染的图表响应式更好、更生动。

### 引入方式

在 HTML 的 `<style>` 中添加防闪烁 CSS，在 `<body>` 末尾通过 ESM 模块加载：

```css
/* 防止 Mermaid 加载前显示原始语法文本 */
pre.mermaid { background: none; border: none; text-align: center; padding: 20px 0; visibility: hidden; }
pre.mermaid[data-processed] { visibility: visible; }
```

```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'default', look: 'handDrawn' });
</script>
```

### 语法

在 HTML 中用 `<pre class="mermaid">` 包裹 Mermaid 语法：

```html
<pre class="mermaid">
flowchart LR
    A[开始] --> B{条件判断}
    B -->|是| C[执行]
    B -->|否| D[跳过]
</pre>
```

### 支持的图表类型

- `flowchart` — 流程图
- `sequenceDiagram` — 时序图
- `classDiagram` — 类图
- `stateDiagram-v2` — 状态图
- `erDiagram` — ER 关系图
- `gantt` — 甘特图
- `pie` — 饼图
- `mindmap` — 思维导图
- `timeline` — 时间线

### 使用原则

- 页面中有图表需求时，默认使用 Mermaid 替代 CSS 手工绘制的伪图表。
- 一个页面可以包含多个 `<pre class="mermaid">` 块。
- Mermaid 语法中不要包含 HTML 标签，保持纯文本描述。
- 如果图表极其复杂且 Mermaid 表达力不够，可以退回到 SVG 或 Canvas 方案。

## 8. 下一步

执行完成后读取 `result-and-errors.md`，按返回 JSON 展示结果或错误。
