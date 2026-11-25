# 发布或更新文本/HTML 页面

当用户要发布对话、大段文本、代码、HTML、Markdown 或纯文本时读取本文件。发布前必须已经完成 `environment-and-credentials.md`。

适用文件类型：`.html`、`.md`、`.txt`。

不适用文件类型：`.ppt`、`.pptx`、`.pdf`、`.doc`、`.docx`。遇到这些文件时，停止本 workflow，改读 `publish-binary-file.md`（那里的命令同样是 `publish.js`，但规则不同）。即使误判了类型，`publish.js` 也会自动把支持的二进制文档分发到正确的上传通道，不会发错接口。

## 视口应用的来源页脚

编写或修改占满 iframe 视口的 HTML 应用时，在源 HTML 的 `body` 上声明 `data-shareone-layout="viewport"`。绑定外部 `remote_url` 后，ShareOne 的来源链接使用约 23px 的单行紧凑页脚；长 URL 省略显示，链接和悬停提示仍保留完整 URL。应用主体应随剩余高度收缩，例如纵向 flex 容器内的 `flex:1; min-height:0`，不要把主体另设成完整 `100vh` 再叠加页脚。

普通文章保留文档间距；`data-shareone-layout="document"` 可显式指定。未声明时仅自动识别固定视口高度、纵向 flex、垂直 overflow 为 hidden/clip 的现有 `body`。窗口缩放和评论侧栏开关改变 iframe 视口时会重新判断。内部 ShareOne 指针不显示来源页脚。此声明只控制页脚展示，不改持久内容或 iframe 高度；不要仅为添加声明重写用户已有文件，仍按下方原格式规则发布。

验收 HTML 应用时检查桌面、手机、评论侧栏开/关和窗口缩放：来源链接可见且可点击，应用主体使用剩余高度，页脚不额外产生横向或空白滚动区。Git 源修改仍按 [git-backed-versions.md](git-backed-versions.md) 更新并同步原分享。

## iframe 应用的文字测量

图表、编辑器等会缓存文字尺寸的应用，需要分别处理文档加载、几何可测量和字体就绪。`load` 不代表字体或应用布局已经完成。首次布局等待 `document.fonts.ready`，并确认实际测量容器的 `getBoundingClientRect()` 宽高都大于零；尺寸不可用时保留待布局状态，通过原生 `ResizeObserver` 或实际 `resize` 后重新检查。不要把零尺寸加上 padding 后当作有效文字高度缓存。

隐藏 iframe 的标准测量结果可能为零，子 frame 的回调也可能暂停。应用仍需自己的测量保护；ShareOne SDK 没有通用的“应用布局完成”信号。字体、可读内容和真实视口变化时更新必要的布局，纯相机平移或缩放不应触发全量文字测量。验收包含冷启动、缓存刷新、隐藏后恢复和字体延迟加载，并检查实际文字边界。

## 1. 识别目标内容与格式保持规则

格式保持是硬规则，优先于一切“展示更美观”的考虑：

- **凡是磁盘上已存在的 `.md`、`.txt`、`.html` 文件——无论是用户指定的，还是本会话中 AI 刚生成的——一律按原文件、原格式发布**。不要生成 `.html` 副本，不要转换格式。`.md` 文件中包含表格、流程描述、mermaid 代码块等可视化内容，也不构成转换成 HTML 的理由。
- 只有当用户**明确表达美化意图**（例如“美化一下”、“做成网页/页面”、“排个版再发”）时，才可以把内容包装为带基础样式的 HTML。除此之外的任何情况都不允许格式转换。
- 如果用户要求分享对话、大段文本或代码（内容尚未落盘）：从对话历史中提取完整文本或代码块，**默认保存为 `.md` 临时文件发布**（纯文本可用 `.txt`），例如 `share_note.md`；同样只有用户明确要求美化时才包装成 `.html`。
- 如果用户没有指定文件：根据上下文寻找最近一次生成或编辑的文本/HTML 文件，例如 `.html`、`.md`、`.txt`，并按上面的格式保持规则原样发布。
- 如果锁定的文件不存在，停止并告知用户。
- 如果锁定的文件是 `.ppt`、`.pptx`、`.pdf`、`.doc`、`.docx`，停止本 workflow，改读 `publish-binary-file.md`。
- 提取用户可能要求的密码 (`password`)、水印 (`watermark`) 和自定义短链接后缀 (`slug`)。服务端会根据文件名自动生成可读的 slug，客户端无需主动设置。只有用户明确说”链接叫 xxx / 自定义短链接 xxx / URL 后缀 xxx”时才用 `--slug` 覆盖。

## 2. 发布前安全自检

发布前安全自检由入口 `SKILL.md` 统一描述：**首次创建新分享链接（POST）**前由 Agent 自行检查内容是否明显违规；自检通过后直接继续发布，不要展示安全提示，也不要等待用户回复“同意”或 `agree`。自检只基于当前已知内容或发布所需读取的文本内容，不要增加额外转换步骤。PUT 更新（含评论处理闭环中的重新发布）按对应规则直接执行。

## 3. 判断创建还是更新

检查对话上下文。如果当前会话中已经为同一个文件生成过 ShareOne 链接，提取之前的 `share_id`（16 位字符串）并执行 PUT 更新。

- 有 `share_id`：执行更新。
- 没有 `share_id`：执行首次创建。
- **例外（优先于上面两条）**：如果当前处于评论处理流程（`comments-process.md`），或当前目录存在 `.shareone_active_task` 文件，说明目标 share 已经确定——读取该文件锁定原分享，按内容来源执行 PUT 更新或修改源头后刷新，**禁止走首次创建**。“想不起 share_id”不等于“没有 share_id”。

脚本另有两道磁盘防线兜底，触发时按提示修正命令，不要绕过：

- `ERROR:ACTIVE_SHARE_TASK`：存在进行中的评论处理任务，必须用错误提示中的 `--share-id` 执行更新。
- `ERROR:FILE_PREVIOUSLY_PUBLISHED`：该文件此前发布过（记录在 `.shareone_history.json`），错误提示中带有原 `share_id`。默认用 `--share-id` 更新原链接；只有用户明确要求为同一文件再发一个新链接时才加 `--force-new`。

## 4. 文本页面发布规则

发布与更新统一使用 `publish.js`。脚本会按文件类型自动选择上传通道（文本走 pages JSON 接口，二进制走 `/api/v1/files` 直传），并在 stderr 输出 `INFO:CHANNEL:text|binary` 说明走了哪条通道——不需要自行判断，也不要直接调用底层的 `upload_page.js` / `shareone_upload.js`。

## 5. 首次创建 (POST)

本地文件与远程 URL 创建均默认关闭评论，脚本在 POST 中显式发送 `allow_comments: false`。只有用户明确要求评论或协同时，才传 `--allow-comments true`。

### 5a. 从本地文件创建

执行：

```bash
node scripts/publish.js "<YOUR_FILE_PATH>" --filename "YOUR_FILE_NAME" [--password "OPTIONAL_PASSWORD"] [--watermark "OPTIONAL_WATERMARK"] [--slug "OPTIONAL_SLUG"] [--allow-comments true] [--allow-data true]
```

### 5b. 从远程 URL 创建

当用户要求从 GitHub 等远程 URL 发布内容时，使用 `upload_page.js`（不是 `publish.js`，因为没有本地文件供类型检测）的 `--remote-url` 参数。服务端自动拉取内容并存储快照，后续访问时自动检查更新。

Git 源的版本选择、更新和回退先读 [git-backed-versions.md](git-backed-versions.md)：历史由源仓库维护。GitHub 可跟随分支，GitLab 只接受完整 commit 的 raw 产物；私库需运营方配置项目/文件/发布者凭据，默认仅所有者和协作者可读。

远程 URL 发布的安全自检只基于用户请求、URL、文件名和显式参数；除非远程内容已经在当前上下文中，不要为了自检主动 fetch、下载、解析或转换远程内容。深度内容检查由服务端拉取后的审核负责。

```bash
node scripts/upload_page.js --remote-url "https://github.com/org/repo/blob/main/docs/report.html" [--filename "OPTIONAL_NAME"] [--password "OPTIONAL_PASSWORD"] [--slug "OPTIONAL_SLUG"]
```

规则：

- `--remote-url` 与本地文件路径互斥，不能同时使用。
- 支持的域名：GitHub（blob URL 自动转 raw）和 **ShareOne 内链**（如 `https://s.shareone.vip/s/my-source-page`）。其他域名返回 400。
- `--filename` 可选：未提供时服务端从 URL 路径自动提取。
- 创建时服务端必须成功 fetch 远程内容，失败返回 400。
- 新内容是否执行 AI 审核由服务端统一配置；当前默认暂停，普通发布接口保持可用。
- 远程源必须是 UTF-8 文本，最大 16 MiB；大小按字节计算。原生 HTML 可直接托管，包含完整数据的文件不需要删记录或包装成自行重写 document 的解码页。
- 已有审核阻断仍有效。实际返回 `CONTENT_REVIEW_REQUIRED` 时保持原分享不变，按 [content-review.md](content-review.md) 处理同一记录；`CONTENT_REVIEW_DISABLED` 表示新自动复核申请暂停。发布后核对原链接与完整下载字节，不能把提交复核当成已发布。
- 服务端根据文件名自动生成 slug，无需手动设置。只有当用户明确要求自定义短链接时，才加 `--slug` 覆盖。

### ShareOne 内链 pointer 模式（多份定制分享）

当 `--remote-url` 指向另一个 ShareOne 链接时，创建的是一个 pointer share：内容从源 share 同步，但有自己的密码、水印和短链接。典型用途：一份源文档 + N 个定制分享；这些分享跟随同一份内容，不保存历史版本。

```bash
# 源文档已存在：https://s.shareone.vip/s/sudowork-bp
# 创建带独立密码和水印的 pointer
node scripts/upload_page.js --remote-url "https://s.shareone.vip/s/sudowork-bp" --password "abc123" --watermark "仅供某机构参考" --slug "sudowork-bp-xxx"
```

- 源 share **不需要开 allow_download**——内链 pointer 走 DB 直读，不走 HTTP。
- 源内容更新后，pointer share 在下次被访问时自动同步最新内容。
- pointer share 不能用 `html_content` 直接更新（返回 `409 REMOTE_SOURCE_BOUND`），必须改源头或先解绑（PUT `remote_url: ""`）。
- 也可以对已有链接 PUT 绑定 `remote_url`，将独立副本转为 pointer：

```bash
node scripts/upload_page.js --remote-url "https://s.shareone.vip/s/sudowork-bp" --share-id <已有的share_id>
```

## 6. 更新已有链接 (PUT)

本节上传本地正文只适用于未绑定远程源的页面。遇到 `INFO:REMOTE_SOURCE` / `HINT:EDIT_AT_SOURCE` 或 `REMOTE_SOURCE_BOUND`，先按 [git-backed-versions.md](git-backed-versions.md) 修改 Git 源并刷新；ShareOne 内链则修改源 share 再刷新。不要自动解绑或另建分享。

如果用户只要求修改已有链接的水印、访问密码、自定义短链接或评论开关，不要执行本节，不要下载原文件；改读 `update-share-settings.md`，使用 `update_share_settings.js` 只更新元数据。

执行：

```bash
node scripts/publish.js "<YOUR_FILE_PATH>" --filename "YOUR_FILE_NAME" --share-id <YOUR_SHARE_ID> [--password "OPTIONAL_PASSWORD"] [--watermark "OPTIONAL_WATERMARK"] [--slug "OPTIONAL_SLUG"] [--allow-comments true/false] [--allow-data true/false]
```

规则：

- Sudowork 环境不要传 `--api-key`。
- 未传 `--allow-comments` 时保留原评论开关；创建的默认值不应用到 PUT 更新。
- 如果用户要求关闭评论协同或开启评论协同，可以在 PUT 更新时传入 `--allow-comments false` 或 `--allow-comments true`。
- 如果用户要求页面持久化数据（游戏分数、表单状态等），传入 `--allow-data true`。
- 如果用户要求修改或清除密码/水印，可以传入 `--password` 或 `--watermark`。
- 如果用户要求修改自定义短链接，可以传入 `--slug`。
- 空字符串 `""` 表示清除对应设置。

## 6b. 就地升级 content-type（md ↔ html ↔ txt），URL 与评论都不变

文本页的 content-type 由文件名后缀决定，可以在**同一个 share 上就地更换**——最常见的是「先用 `.md` 快速起草 → 之后升级成带样式 / Mermaid 的 `.html`」（例如把 md 里的 ASCII 流程图升级成 Mermaid 渲染图）。

做法就是一次普通的 PUT 更新（§6）：传新内容 + 新后缀的 `--filename`，并带上原 `--share-id`：

```bash
node scripts/publish.js "<NEW_HTML_FILE>" --filename "report.html" --share-id <YOUR_SHARE_ID>
```

关键保证（这些是可依赖的特性，不是巧合）：

- **分享 URL 一字不变。** ShareOne 的浏览路由按 ref（slug/share_id）解析 share、按 share 真实的 content-type 渲染，**URL 前缀不参与内容决定**。所以 `/s/<ref>` 与 `/md/<ref>` 完全等价、指向同一个 share、服务同一份内容——升级成 html 后，**老的 `/md/<slug>` 链接继续有效、直接渲染新 html**，不用改前缀，也不会重定向。
- **评论全部保留（open + resolved）。** 评论按 `share_id` 存储、与内容格式无关，就地升级不丢任何评论。
- **就地升级禁止 `--force-new`。** `--force-new` 会新建一个 share（新 URL、新 `share_id`），**丢掉原链接和其上所有评论**。要升级 content-type 时永远用 `--share-id` 更新，绝不 `--force-new`。

> 反面教训：一个没有上下文的 agent 看到「把 md 换成 html」，可能误以为要重新发布而加 `--force-new`——那会另起一条链接、丢掉原 URL 和评论。正确做法是 `--share-id` 就地更新。

### 动态页面与文字评论

生成或修改启用评论的 HTML 页面时，正文保留用户可阅读的文字。SCRIPT、STYLE、NOSCRIPT、TEMPLATE 和 ShareOne 标注浮层不参与文字锚点捕获、上下文或重定位；普通高亮 span 中的原文仍参与。不要依靠代码或数据脚本里的同名字符串恢复评论。

- 大体积数据快照保留完整，适合放在 `<head>` 的 `<script type="application/json">` 中，运行逻辑读取该数据。无需为了评论删记录、另建分享或关闭评论。普通发布保持文件格式和内容；只有用户授权修改页面时才调整结构。
- 文字或 DOM 结构变化会重新定位，等长文字替换也算变化；代码更新、标注自身变化和纯坐标移动不应触发全量文字扫描。ShareOne 在一轮重定位中共用内存索引，不把索引或当前可见性写入评论。
- 普通 DOM 区域评论可用稳定元素属性。命名对象上的新文字评论若需跨呈现方式保持身份，在选中文字的容器上写 `data-shareone-anchor-id="<编译器/数据模型的稳定ID>"`，并按下方契约报告同一个 ID；不要用翻译后的显示名或 DOM 序号充当 ID。
- 修改后保持评论开启，用真实浏览器实际展开/收起、滚轮缩放和拖动，检查评论卡片、恢复后的高亮及输入响应。CPU 采样累计值和一次交互墙钟时间分别报告，不把某台设备的结果写成性能承诺。

旧文字锚点的偏移可能含非阅读内容，ShareOne 会校验引用文字并尝试内容重定位。失败时评论卡片仍保留，可阅读和回复；不要据此推断原文删除或自动关闭评论。

#### 稳定对象的评论契约

页面从加载开始可读取 `window.__SHAREONE__?.anchors`；独立文件中没有 SDK，调用前检查是否存在。

```javascript
const A = window.__SHAREONE__?.anchors;
// 只在用户明确选择评论目标时调用；普通检查/浏览点击不调用。
A?.select({id: object.id, label: object.label, context: object.context}, rectOf(object));
A?.on("resync", ids => reportRequestedIds(ids));
A?.on("reveal", ids => { revealKnownIds(ids); redraw(); });
// 在自身布局、分页、语言和视图变化时报告，不另起指针帧轮询。
A?.report([
  {id: "source/Products", state: "visible", rect: rectOf(products)},
  {id: "source/Products/ProductName", state: "hidden"}, // 已知存在，此视图未画
  {id: "source/deleted-object", state: "missing"},     // 当前完整模型确认不存在
  {id: "source/loading-object", state: "pending"},    // 尚未确认；清除旧坐标
]);
```

`data-shareone-anchor-id` 只为**新选择**指定身份；该标记本身不提供位置、可见性或恢复操作，仍需上述回调和报告。整个选择位于一个标记容器中时，使用最近的共同标记容器的 ID，并保留引用文字与上下文；没有共同标记容器时保留普通文字语义。`select` 打开草稿，提交才落库；取消不创建评论。ID 可表示源对象或字段，不能从相同显示名猜测。

对象内文字选择还保存 `text: {exact, prefix, suffix, position: {start,end}, version?}`。
偏移是该对象**可阅读文字**的 UTF-16 偏移，排除代码、样式与标注浮层；原文及上下文
是选择时的事实，不能由今天的对象标题重建。DOM 容器可写
`data-shareone-anchor-version="en@content-revision"`，由 ShareOne 捕获；内容或语言变化
时必须更新它。版本未知时，只允许原文和两侧上下文唯一命中，重复句子不能猜。

页面接入常驻文字恢复，无需在每次手势中下载评论。对象可见并不代表该对象上的
选中文字已定位；实现下面的被动回调，用户提交后即可恢复当前可见文字：

```javascript
A?.configure({marks: "page"});
A?.on("resync-text", async passages => {
  // 每批是当前所有单对象文字评论；移除不再存在的旧 Range。
  retainPassageMarks(new Set(passages.map(p => p.commentId)));
  return Promise.all(passages.filter(p => p.changed).map(async p => {
    clearPassageMark(p.commentId);
    if (!p.visible || !readableSurfaceIsVisible(p.id))
      return {commentId: p.commentId, state: "pending"};
    const span = A.resolveText(readableTextOf(p.id), p.text, contentLanguageVersionOf(p.id));
    if (p.signal.aborted) return {commentId: p.commentId, state: "pending"};
    if (!span) return {commentId: p.commentId, state: "unresolved"};
    // 页面自身的可阅读表面；使用 Range/CSS.highlights，不覆盖输入区域。
    const mark = markPassageWithoutInterceptingInput(p.id, span, p.commentId);
    p.signal.addEventListener("abort", () => clearThisPassageMark(p.commentId, mark), {once: true});
    return {commentId: p.commentId, state: "resolved"};
  }));
});
A?.on("marks", ({text, point}) => {
  setNativePassageMarksVisible(text);
  setObjectMarksVisible(point);
});
// 自绘某一条文字批注被点击时，精确打开该线程。activate(objectId) 仍用于对象。
A?.activateComment(commentId);
// 文字表面挂载、内容/语言切换后合并调用一次；平移、缩放不调用。
A?.resyncText();
```

此示例中的读取、绘制和清理函数由页面实现，必须与捕获使用同一份可阅读文字序列。
`resync-text` 收到 `{commentId, id, text, visible, changed, signal?}` 数组；`changed: false`
的条目只用于保留缓存，不重复扫描，只有变化条目带取消信号。回调返回
`{commentId, state}` 数组，状态为 `pending`、`resolved`、`unresolved` 或 `unsupported`。
被动恢复不打开面板、不切视图、不导航或移动相机。隐藏表面保持 `pending`；已显示但
版本不符或匹配有歧义才报 `unresolved`。十秒超时或回调失败会取消本批变化条目，
新选择、重新绑定、删除和下一次恢复也会取消旧请求；取消时只清除该请求自己的 Range。
可见性、Range、索引、取消信号和标记开关都只存在于浏览器内存。

独立的显式“显示目标”操作允许导航并恢复：

```javascript
A?.on("reveal-text", async ({commentId, id, text, signal}) => {
  await revealAndRenderObject(id);
  if (signal.aborted) return "unresolved"; // 旧异步请求不再绘制标记
  const content = readableTextOf(id); // 与捕获使用同一份文字序列
  const span = A.resolveText(content, text, contentLanguageVersionOf(id));
  if (!span) { clearPassageMark(commentId); return "unresolved"; }
  markPassageWithoutInterceptingInput(id, span, commentId);
  return "resolved";
});
// 版本或语言切换时失效旧定位；这是浏览器状态，不落库。
A?.reportText([{commentId, state: "pending"}]);
```

`reveal` 仍接收稳定 ID 数组；`reveal-text` 接收原始文字 selector 和取消信号，可异步恢复并返回
`pending`、`resolved`、`unresolved` 或 `unsupported`。只实现 `reveal-text` 的页面仍需
读者显式定位才恢复；缺少该回调时显式定位报告尚未支持。旧对象评论显示未捕获文字范围，
不把 label 当 selector。重新绑定目标是可选的修改操作，不表示刚提交的评论失去目标。
页面自绘标记保持不拦截输入；平移、缩放和位置报告不触发文字扫描或网络请求。

旧文字评论不会自动转成对象评论；同名文字、未回答的 ID 和明确缺失分别处理。区域评论保存一组 ID，侧栏保留可见、隐藏、缺失和等待各部分的数量。恢复已知隐藏目标用“显示目标”；等待或文字未定位可“重新定位”。绑定公开 GitHub 文件时可查看该文件的 Git 历史；本地上传和内部 ShareOne 指针不新增版本库，不公开内部源地址。GitLab 版本与私库使用方式见 [git-backed-versions.md](git-backed-versions.md)。

## 7. 使用 Mermaid.js 绘制图表

**适用前提**：本章节只适用于目标内容本来就是 HTML 页面的场景——即用户提供的就是 HTML 文件，或用户明确要求美化/做成网页而新生成 HTML。**不要为了使用 Mermaid 而把 `.md`/`.txt` 文件转换成 HTML**；`.md` 里的图表内容按第 1 节的格式保持规则原文发布。

当 HTML 页面需要包含图表、流程图、时序图、思维导图等可视化内容时，优先使用 Mermaid.js：用文本维护节点与关系，渲染为可缩放的 SVG。复杂图表可结合原生 HTML/CSS/JavaScript 实现展开、缩放和拖动。

### 引入方式

在 HTML 的 `<style>` 中添加防闪烁 CSS，在 `<body>` 末尾通过 ESM 模块加载：

```css
/* 防止 Mermaid 加载前显示原始语法文本 */
pre.mermaid { background: none; border: none; text-align: center; padding: 20px 0; visibility: hidden; }
pre.mermaid[data-processed] { visibility: visible; }
```

```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.12.1/dist/mermaid.esm.min.mjs';
  import elkLayouts from 'https://cdn.jsdelivr.net/npm/@mermaid-js/layout-elk@0.2.0/dist/mermaid-layout-elk.esm.min.mjs';
  mermaid.registerLayoutLoaders(elkLayouts);
  mermaid.initialize({ startOnLoad: true, securityLevel: 'strict', theme: 'default' });
</script>
```

### 语法

在 HTML 中用 `<pre class="mermaid">` 包裹 Mermaid 语法：

```html
<pre class="mermaid">
---
config:
  layout: elk
---
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
- **架构图和流程图默认选择 ELK layered。** 用每张图的 Mermaid YAML 前置配置 `config.layout: elk`；需要 Dagre 时明确写 `layout: dagre`。沿用 Mermaid 的配置语法，不新增 ShareOne 注释协议。上述固定 Mermaid 11 示例必须注册配套 ELK 加载器；浏览器使用包含依赖的 `esm.min.mjs`，`core.mjs` 面向打包器，直接引入会出现裸模块解析错误。自带渲染器的 HTML 页面在自身注册；托管 Markdown 依赖站点渲染器是否支持该布局，不能只改 skill 就宣称已支持。
- 一个页面可以包含多个 `<pre class="mermaid">` 块；编辑已有页面时，在原文位置更新图表，保留其他正文与图表，并按第 6 节更新原分享。
- 节点与连线标注优先用纯文本；需要分行时使用 Mermaid 支持的换行语法，避免在标签中嵌入交互 HTML。
- 如果图表极其复杂且 Mermaid 表达力不够，可以退回到 SVG 或 Canvas 方案。

复杂架构图的推荐实践（用户需要交互阅读时）：

- **保留细节再优化布局。** 对照原图检查节点、部署/信任边界、连线方向和协议标注；两条连线即使连接同一对节点，也可能表示不同职责。全图缩小时用作导航，通过缩放阅读细节；不要为塞进窗口而删节点、合并关系或简写标注。
- **按实际几何比较布局。** ELK layered 适合有方向、分组和层级的图，但不能保证零交叉。比较原布局与 ELK 的文字重叠、连线穿节点、边界和适应窗口比例，再选择方向与间距；平移和缩放不应重跑布局。sudograph 的另一种布局是 Cytoscape 的 fCoSE，适合关系图比较，不能把它当成 Mermaid 的内置布局名。
- **在主文档中展开。** 将图嵌在正文原位置，用浮层扩大画布；建议提供“适应窗口”“100%”、缩放按钮、滚轮缩放、拖动及 Esc 关闭。大型分区图可加分区定位按钮，例如“云端”“盒子”。同一份图源供嵌入和展开视图使用，避免维护另一条内容重复的分享链接。
- **按 SVG 原始尺寸缩放。** 读取渲染结果的 `viewBox`，将 SVG 宽高设为对应的 CSS 像素值，再用容器的 `translate/scale` 平移缩放；“100%”表示该原始尺寸，适应窗口另算比例。若 SVG 已被 `width:100%` 压缩，直接放大仍可能字号过小。画布裁切溢出，浮层随窗口变化重新适配；拖动手势和指针捕获按 `SKILL.md` 的评论交互约束处理。
- **主题与图表一起更新。** 使用固定且验过的 Mermaid 版本；上述示例的 `default` 是静态主题。需要自定义明暗配色时用 `theme:'base'` 与 `themeVariables` 调整文字、连线、节点和分组背景（见 [Mermaid 主题文档](https://mermaid.js.org/config/theming.html)）。ShareOne HTML 页可监听外层的 `message`：`data.source === 'shareone-shell'`、`data.type === 'theme'`，读取 `data.value` 的 `light/dark`；直接打开时以系统主题作为初始值。
- **重绘前保留源文本并恢复未缩放状态。** Mermaid 会将源文本替换为 SVG；手动重绘时设置 `startOnLoad:false`，切换主题时从保存的源码重绘，串行执行并清除旧 `data-processed`。调用 `mermaid.run({ nodes })` 前暂时移除画布的缩放变换，完成后重设 SVG 原始尺寸并恢复视图，避免标签测量受缩放影响而被裁切。其他会自行重建图表 DOM 的页面，也按动态页面要求保留稳定评论身份。
- **看实际页面后再完成验收。** 用可用的真实浏览器工具（如 ai-dev-browser）打开发布后的主链接，查看截图；ShareOne 的 HTML 在 iframe 内，外层页面可打开不代表图已渲染。确认图表加载完成、正文完整、节点/边界/关系与标注无遗漏，实际操作展开/关闭、缩放、拖动、分区定位和窗口变化；在缩放后切换明暗主题，检查文字裁切、标签遮挡及对比度。开启评论的页面还需按上方动态页面要求验证评论交互。

可拖动且可评论的图，还应区分阅读手势：

- **平移、选字、点节点评论互斥。** 当拖动文字标签会触发浏览器选区时，可以提供“移动 / 选择文字 / 评论节点”三个模式。只在移动模式的图区域禁用文字选择，选字模式恢复原生选择；正文始终可以选字。移动模式的 `pointerdown` 才清除旧选区并阻止默认选择，移动超过阈值后才捕获指针。ShareOne 的区域/点评论模式优先，不能被页面平移处理器截走。普通节点点击可打开详情，不应顺便创建评论草稿。
- **模式切换只改变交互。** 复用同一份模型、SVG 和源对象身份，不因模式、布局或主题创建另一组评论对象。选字模式也不能通过重绘恢复文字选择，否则会丢失镜头位置和选区。平移/缩放只更新镜头变换，并用 `requestAnimationFrame` 合并位置报告；不要每次移动重跑布局、重建标签或扫描全文。
- **标记避开可选文字。** 若采用 SDK 的 `marks: 'page'`，页面自行绘制的小评论按钮应放在标签外，调用 `window.__SHAREONE__?.anchors?.activate(id)`，并用 `data-comment-only` 排除按钮文字。不要给整个标签盖一层点击遮罩，也不要重复渲染同一身份和文本版本的可见锚点。`activate(id)` 是对象级入口；一个对象有多条文字评论时，不能宣称它能指定某条评论或还原 SDK 尚未提供的文字范围。
- **用真实手势验收。** 用浏览器原生鼠标/触摸输入，从节点文字上开始拖动，确认不会产生选区或评论请求；切到选字模式选一个词，确认上报的 `exact`、稳定对象 ID 和文本版本正确，镜头未变化。再验证节点评论、ShareOne 区域评论、正文选字、主题切换和手机画布。仅 `dispatchEvent` 或程序设置 Range 不能证明原生拖动没有冲突；验收不需要提交假的测试评论。

## 8. 下一步

执行完成后读取 `result-and-errors.md`，按返回 JSON 展示结果或错误。
