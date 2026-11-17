# 流程实现细节（`publish_note.mjs` 镜像）

> **什么时候读这个文件**：改选择器、新增步骤、排查 DOM 结构、或要理解某个失败的确切成因时读。
> **日常发布不要读** —— `scripts/publish_note.mjs` 已经实现了下面全部逻辑，运行时不需要照着抄。
>
> 本文件里的 JS 片段是 `publish_note.mjs`（854 行）的**节选与注释版**，不是可直接执行的文件；
> 与代码冲突时以代码为准。选择器常量集中在 `publish_note.mjs` 顶部的 `SEL` / `T` 两张表。

## 流程链总览

```
[sh] 判断媒体类型(按扩展名) + 全部参数校验
→ [mjs] open-publish-page  创建 task space + 打开创作平台 + 等 SPA
→ auth                     登录态检查
→ ensure-upload-tab        切到对应上传 tab(自动兼容 tab/下拉)
→ upload-media             上传素材(图文=uploadFile 循环；视频=单文件+转码轮询)
→ set-cover                自定义封面(仅视频且传了 COVER_IMAGE，可选)
→ fill-title / fill-body   填标题、正文(带回读校验)
→ add-topics               逐个话题从下拉列表选择(失败重试一次)
→ submit                   调用 _onPublish() / _onSave()（由 MODE 决定）
→ 校验结果 → 清理 task space(失败时保留现场)
```

**收尾模式（MODE）**：
- `publish`（默认）：调用 `_onPublish()` 直接发布，等待跳转 `note-manage` 确认。
- `draft`：调用 `_onSave()` 存草稿箱，校验左侧「草稿箱(N)」计数 +1（草稿箱按钮文本是「暂存离开」，不是「存草稿」）。
- `stage`：填完标题/正文/话题后停在页面，**不提交、也不关闭 task space**；收尾要手动 `ego-browser nodejs -e "await completeTaskSpace(<id>,{keep:false})"`，否则每跑一次就多一个常驻空间。
用户说「存草稿 / 推到草稿箱 / 自己点发布」时走 `draft` 模式；说「发小红书 / 发布」走 `publish`。

## 图文 vs 视频的差异

v1.7.2 之前只支持图文，根因就在这张表——两条路径的落地面和完成判据完全不同。

| 环节 | 图文 | 视频 |
|------|------|------|
| 落地页 | `/publish/publish` 默认是视频页，需切「上传图文」 | 默认就是，无需切换 |
| 上传方式 | 逐个 `uploadFile()`，批量只留空占位 | 单文件 `uploadFile()` |
| 完成判定 | CDN 缩略图数 ≥ 文件数 或「图片编辑 N/18」 | 出现「重新上传」+ 标题输入框 |
| 等待时长 | 每张 6s + 汇总 10s | 转码轮询，最多 40×3s（约 2 分钟） |
| 封面 | 无 | 默认第一帧；可用 `COVER_IMAGE` 指定图片 |

## 1. 创建 task space 并打开创作平台

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('publish xhs note')
await openOrReuseTab('https://creator.xiaohongshu.com/publish/publish', { wait: true, timeout: 25 })
// Vue SPA，必须等待 15 秒渲染
await wait(15)
EOF
```

**关键点**：小红书创作平台是 Vue SPA，`<div id="app">` 初始为空，`waitForNetworkIdle` 不够，必须 `await wait(15)`。

## 2. 切换到对应上传 tab

`/publish/publish` 落地时**默认就是「上传视频」页**，所以视频不用切换，图文要切。判断依据是目标 file input 是否已存在，不要靠页面文案猜。

支持两种入口，脚本**自动兼容**：

- **方式 A（顶部 tab）**：页面顶部有「上传视频 / 上传图文 / 写长文」tab 导航
- **方式 B（下拉菜单）**：页面有「发布笔记」下拉按钮，点击展开后选对应项

脚本逻辑：先检测 `input[type="file"][accept*=".mp4"]`（视频）或 `[accept*=".png"]`（图文）是否已存在；不存在则试方式 A（按文本遍历点击）；仍未出现再回退方式 B（snapshotText 匹配 ref 点击）。

```js
// 方式 A：点击顶部「上传图文」tab
const tabClicked = await js(`(() => {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false)
  let node
  while (node = walker.nextNode()) {
    if (node.textContent.trim() === '上传图文') {
      let element = node.parentElement
      for (let i = 0; i < 4; i++) {
        if (!element) break
        element.click()
        element.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }))
        element = element.parentElement
      }
      return true
    }
  }
  return false
})()`)
await wait(3)

// 检查是否已进入图文编辑页
if (!await js(`!!document.querySelector('input[type="file"][accept*=".png"]')`)) {
  // 方式 B：回退到「发布笔记」下拉菜单
  const pageText = await snapshotText()
  const matchPublish = pageText.match(/发布笔记.*?\[ref=(\d+)/)
  if (matchPublish) {
    await click('@' + matchPublish[1])
    await wait(2)
    const text2 = await snapshotText()
    const matchUpload = text2.match(/上传图文.*?\[ref=(\d+)/)
    if (matchUpload) {
      await click('@' + matchUpload[1])
      await waitForNetworkIdle(5)
      await wait(3)
    }
  }
}
```

> **注意**：两种 UI 可能同时存在或随版本切换，脚本以图片 file input 是否出现为判断标准，自动选择可用入口。

## 3. 上传素材

### 3a. 图文（`uploadFile` 单文件循环）

小红书 Web 端对批量 `DOM.setFileInputFiles` 只创建空占位、不真正上传图片，因此改用 **`uploadFile()` 逐个上传**，每次调用都会触发真实的文件选择/change 事件，图片能真正落到 CDN。

```js
for (let i = 0; i < filePaths.length; i++) {
  const fp = filePaths[i]
  cliLog('Uploading file ' + (i + 1) + '/' + filePaths.length + ': ' + fp)
  await uploadFile('input[type="file"][accept*=".png"]', fp)
  await wait(6)  // 等待单张图上传处理
}
await wait(10)   // 最后批量等待 CDN 缩略图
```

- 图片推荐尺寸：1080x1440（3:4 竖屏）
- 最多 18 张
- 文件路径必须是绝对路径

> ⚠️ **踩坑记录（已验证，2026-08-18）**：
> - 用 `DOM.setFileInputFiles` 批量设置 10 张文件并手动触发 `input`/`change` 事件，编辑器会显示「图片编辑 10/18」，但缩略图是空占位符，保存草稿后图片为空。
> - 用 `uploadFile()` 单文件循环上传，每次只传 1 张，可确保每张图真正上传到小红书 CDN。
> - 校验时以「图片编辑 N/18」的 **N**（`editCount`）为准，并辅以 `img[src*="xhscdn.com"]` / `spectrum/` 预览图数量判断。

### 3b. 视频（单文件 + 转码轮询）

视频页的 file input 是 `input[type="file"][accept*=".mp4"]`（accept 为 `.mp4,.mov,.flv,.f4v,.mkv,.rm,.rmvb,.m4v,.mpg,.mpeg,.ts`），**只有一个 input，无 multiple**，`uploadFile()` 一次传完即可。

视频上传后要等服务端转码，不能只看瞬时状态。判定完成的信号是**同时出现「重新上传」文案和标题输入框**：

```js
await uploadFile('input[type="file"][accept*=".mp4"]', filePath)
await wait(5)

let videoOk = false
for (let attempt = 0; attempt < 40; attempt++) {   // 最多约 2 分钟
  await wait(3)
  const v = await js(`(() => {
    const text = document.body.innerText
    return {
      hasReupload: text.includes('重新上传'),
      hasTitleInput: !!document.querySelector('input[placeholder="填写标题会有更多赞哦"]'),
      hasSetCover: text.includes('设置封面'),
      videoCount: document.querySelectorAll('video').length,
      readyState: Math.max(0, ...[...document.querySelectorAll('video')].map(el => el.readyState || 0))
    }
  })()`)
  if (v.hasReupload && v.hasTitleInput) { videoOk = true; break }
}
```

> 实测：10MB / 22.8s 的 mp4，第 0 次轮询（上传后 8 秒）就已 `readyState: 4` 且「重新上传」出现，基本不需要等。
>
> 封面默认截取视频第一帧，**不传 `COVER_IMAGE` 就完全不碰**。传了图就走下面 §3c 的四步替换链路。
>
> 注意 `video` 元素在页面上可能有 4 个（预览、封面候选等），不要用 `videoCount === 1` 做判定。

### 3c. 设置视频封面（可选，`COVER_IMAGE`）

默认封面是视频第一帧，留空就什么都不做。要用自己的图片当封面时传绝对路径：

```bash
COVER_IMAGE=/absolute/path/cover.png   # 建议 3:4 竖图，1080x1440 及以上
```

真实交互链路，四步缺一不可：

```js
// 1. 用 CDP 派发真实鼠标悬停 —— 「编辑封面」按钮平时 boundingRect 是 0×0，
//    只有 CSS :hover 生效才渲染出来，js 的 el.click() 和 scrollIntoView 都无效
await cdp('Input.dispatchMouseEvent', {
  type: 'mouseMoved',
  x: rect.x + 65,                       // 缩略图在 .cover 左侧约 130px 宽，右侧是智能推荐区
  y: rect.y + Math.round(rect.h / 2),
  button: 'none'
})
await wait(1.5)

// 2. 点「编辑封面」，打开封面编辑器
await click('.cover-edit-entry', { label: 'open cover editor', timeout: 8000 })
await wait(4)

// 3. 编辑器打开后页面会多出一个 accept 含 image 的 file input，直接上传即可
await uploadFile('input[type="file"][accept*="image/png"]', coverPath)
await wait(5)

// 4. 点「完成」——按钮在视口外右侧（innerWidth 900 时 x≈1128），必须先滚动再点
await js(`(() => {
  const el = [...document.querySelectorAll('span')].find(e =>
    e.textContent.trim() === '完成' && String(e.className).includes('circle-button'))
  if (!el) return false
  el.scrollIntoView({ block: 'center', inline: 'center' })
  el.click()
  return true
})()`)
await wait(4)
```

关键选择器与坑：

| 元素 | 选择器 | 说明 |
|---|---|---|
| 封面预览容器 | `.cover` | 632×160，左侧缩略图 + 右侧「智能推荐封面」 |
| 编辑入口 | `.cover-edit-entry` | 文本「编辑封面」，**平时 0×0，必须 hover 才出现** |
| 封面图片 input | `input[type="file"][accept*="image/png"]` | 编辑器打开后才存在（页面此时有 2 个 file input） |
| 完成按钮 | `span.circle-button-content`（文本「完成」） | 在视口外，需 `scrollIntoView` |
| 编辑器容器 | `.d-modal.cover-modal` | 关闭判定：`!m \|\| m.offsetParent === null` |

- **不要点「上传」按钮**：编辑器打开后 image input 已在 DOM 里，直接 `uploadFile` 就能替换封面，省一步。
- **PK 封面引导气泡会遮挡**：`.pk-cover-guide-tooltip` / `.pk-cover-guide` 首屏可能自动弹出，先 `display: none` 掉（纯视觉层，不影响提交数据）。
- **不要用「智能推荐封面/一键生成」**：那是 AI 生成封面，会消耗 HeyGen 类额度且不可控，本技能只做「上传自己的图」。
- **校验信号**：完成回到编辑页后，页面出现「✅ 封面效果评估通过，未发现封面质量问题」即封面已被服务端接受。
- **失败即中止**：任一环节失败（悬停没出按钮 / 编辑器没开 / 找不到完成按钮 / 弹窗没关 / URL 没变）
  `setVideoCover()` 返回 `{ok:false, code:'E_COVER_*'}`，上层 `publish_note.mjs:586`
  调 `fail('set-cover', r.code, EXIT.COVER, ...)`，**`exit 60` 中止整条流程**，
  不会带着错误封面继续发。`what_now` 按 code 给分级提示（见 `error-handling.md`）。
  > 注意：`video-multi-release` 的 `scripts/xhs.mjs` 对同一件事是「只告警、继续发布」——
  > 那是另一个脚本的有意设计，别把两者行为互相套用。

## 4. 填写标题

```js
await fillInput('css:input[placeholder="填写标题会有更多赞哦"]', '标题内容')
```

## 5. 填写正文与话题标签

正文区域是 `contenteditable="true"` 的富文本编辑器。**2026-11 起图文页与视频页的编辑器都已换成 tiptap ProseMirror**（外层 `div.tiptap`，内层仍有 `contenteditable="true"`），建议按下面的顺序探测，别写死：

```js
const editorSel = await js(`(() => {
  if (document.querySelector('div.tiptap')) return 'div.tiptap'
  if (document.querySelector('[contenteditable="true"]')) return '[contenteditable="true"]'
  return ''
})()`)
```

```js
// 先 focus 编辑器并输入正文（不带 #话题）
// 注意：用 js 里的 focus()，不要用 click()——发布按钮浮层会拦截指针事件
await js(`document.querySelector('${editorSel}').focus()`)
await typeText('正文内容...')
await wait(1)

// 逐个话题从下拉列表选择，确保生成真正可点击的话题标签
const topics = ['话题1', '话题2']
for (const topic of topics) {
  await moveCaretToEnd()   // 见下方「tiptap 光标定位」，每次都要重置光标
  await typeText('#' + topic, { label: 'type topic' })
  await wait(4)  // 等待下拉列表返回

  await js(`((topic) => {
    const container = document.getElementById('creator-editor-topic-container')
    if (!container) return
    const items = [...container.querySelectorAll('.item')]
    // 优先精确匹配（名称首行等于 #话题），否则退到第一个
    const exact = items.find(el => {
      const nameEl = el.querySelector('.name')
      return nameEl && nameEl.innerText.trim().split('\n')[0] === '#' + topic
    })
    const item = exact || items[0]
    if (!item) return
    ;(item.querySelector('.name') || item).click()
  })('${topic}')`)

  await wait(1.5)
  await pressKey('Escape')
  await typeText(' ')
}
```

> **注意**：直接粘贴 `#话题1 #话题2` 只会生成纯文本，不会真正挂载到话题词条。必须从 `#` 触发下拉列表后点击选中。
>
> ⚠️ **tiptap 光标定位（2026-11-02 实测）**：tiptap 不认 `Control+End`，按了之后光标不会到末尾，后续 `#话题` 会被插进正文中间（表现为「给同#人生感悟样走在这段路上的人」）。不要用快捷键，用 Selection API 显式收敛光标：
>
> ```js
> await js(`(() => {
>   const el = document.querySelector('div.tiptap')
>   el.focus()
>   const r = document.createRange()
>   r.selectNodeContents(el)
>   r.collapse(false)          // false = 折叠到末尾
>   const s = window.getSelection()
>   s.removeAllRanges()
>   s.addRange(r)
> })()`)
> ```
>
> 每次 `typeText('#话题')` 前都要重新定位一次光标。写错了用 `pressKey('Control+z')` 可以整段撤销上一次 `typeText`。
>
> ⚠️ **点编辑器会被发布按钮挡住**：`click('div.tiptap')` 报 `ElementResolutionError: <xhs-publish-btn> intercepts pointer events`。**用 `js()` 里的 `el.focus()` 或 `page.focus()`，不要用 click。**

## 6. 触发发布 / 存草稿

小红书的「发布 / 存草稿」按钮封装为同一个自定义 Web Component（`<xhs-publish-btn>`），常规选择器或坐标点击无法命中，需直接调用其内部方法。**两种收尾模式共用这一个组件**：

```js
const host = document.querySelector('xhs-publish-btn')
// 检查状态
const disabled = host.getAttribute('submit-disabled')   // 'false' = 可点
const loading = host.getAttribute('submit-loading')     // 'false' = 未加载
const saveDisabled = host.getAttribute('save-disabled')  // 'false' = 可存草稿

if (MODE === 'draft') {
  // 存草稿模式：调用 _onSave()，不要找「存草稿」按钮——它根本不存在
  host._onSave()
} else {
  // 发布模式：调用 _onPublish()
  host._onPublish()
}
```

> ⚠️ **踩坑记录（已验证，2026-08-18）**：小红书根本没有名为「存草稿」的按钮。发布页右下角的按钮文本是**「暂存离开」**（组件属性 `save-text="暂存离开"`、`is-save-draft="true"`），且同样藏在 `<xhs-publish-btn>` 的 **closed Shadow DOM** 内，DOM 遍历、坐标点击、`snapshotText` 全部抓不到文本。正确做法是直接调 `host._onSave()`（发布用 `host._onPublish()`）。若按"存草稿"文本找按钮会永远找不到，页面也不会变化。

**存草稿校验**：调用 `_onSave()` 后页面不会跳转，而是把笔记存入**当前浏览器本地**（页面提示"草稿存储于当前使用的浏览器本地"）。校验方式——读取左侧导航的「草稿箱(N)」计数，正则 `草稿箱\((\d+)\)` 比较调用前后是否 +1。

**发布校验**：调用 `_onPublish()` 后按钮进入 loading，约 5-10 秒后 URL 出现 `published=true`（脚本主判据）。`note-manage` 只作旧行为兜底——直接访问 `/publish/note-manage` 已 404（见注意事项 19），**别手工拼这个 URL 去确认**，走侧栏「笔记管理」入口。

> 若需了解完整的失败方案对比与 `_onPublish`/`_onSave` 技术细节，参见 `references/publish-method.md`。

## 7. 等待完成并校验

按 MODE 不同校验方式不同：

**发布模式**：调用 `_onPublish()` 后按钮进入 loading，约 5-10 秒后页面重置并出现 `published=true` URL 参数或跳转 `note-manage`。

```js
const info = await pageInfo()
if (info.url.includes('published=true') || info.url.includes('note-manage')) {
  cliLog('SUCCESS: 发布成功！')
}
```

**存草稿模式**：调用 `_onSave()` 后页面**不跳转**（只是存入当前浏览器本地草稿箱），需靠「草稿箱(N)」计数 +1 来验证。

```js
await wait(6)
const draftN = await js(`(() => {
  const m = document.body.innerText.match(/草稿箱\\((\\d+)\\)/)
  return m ? m[1] : 'n/a'
})()`)
cliLog('草稿箱 count: ' + draftN)  // 与调用前对比，+1 即成功
```

## 8. 清理

```js
await completeTaskSpace(task.id, { keep: false })
```

---

## 附：注意事项里的技术细节

下面几条在 SKILL.md 里只留了结论，这里保留完整成因与排查口径。

11. **重复发布会累积「暂无笔记标题」废草稿**：小红书创作平台在每次进入图文编辑页并发生导航/重渲染时，会自动存若干标题为「暂无笔记标题」的空草稿。用 `draft` 模式重跑多篇后，草稿箱会堆积大量废草稿。清理方法：进「草稿箱」→ 切「图文笔记」tab → 对每个废草稿点 `.draft-actions` 里**最后一个 `.btn`**（编辑/删除中的删除）→ 确认弹窗。⚠️ 确认弹窗的删除按钮是真实 `<button class="...model-footer-confirm-btn draft-delete-popconfirm-btn-footer-confirm">删除</button>`，**必须点这个 `<button>`**；点 footer 容器 `<div class="modal-footer-buttons">`（文本也是「取消\n删除」）是空操作，不会删。弹窗文案含「草稿删除后不可找回」。

12. **发布后的事后验证（2026-09-09 踩坑）**：发布脚本结束时 `completeTaskSpace({ keep: false })` 会销毁 space 连同小红书登录态 cookie。**之后新建的 task space 不继承登录态**（打开 creator.xiaohongshu.com / www.xiaohongshu.com 都会跳登录墙，公开搜索页未登录也全被拦截）。因此**事后独立远程验证不可行**——如需登录态验证（如查「已发布」列表），必须在发布脚本同一 space 内、`completeTaskSpace` 之前完成。发布成功本身以业务级证据为准：图片 CDN 落盘（`cdnImages`≥N、`editCount`=N）+ 话题全部 `clicked:true` + URL 跳转含 `published=true`（发布端点真实处理后的跳转，非 HTTP 200 假成功）。最终视觉确认建议用户在 App 内查看。

13. **登录检测必须用 URL 判定，不能只扫页面文字（2026-10-09 踩坑）**：小红书登录态过期时，创作平台会 302 到 `creator.xiaohongshu.com/login?source=&redirectReason=401&lastUrl=...`。**登录页导航里同样含「发布」「上传图文」等字样**，早期版本用 `text.includes('登录') && !text.includes('发布')` 判断，会把 401 误判成「已登录」，然后在 `uploadFile()` 阶段抛 `ElementResolutionError: input[type="file"][accept*=".png"] not found`——真实原因被掩盖，排查绕远路。
    正确判定（已内置于 `publish_note.mjs` 的 auth 步骤）：
    ```js
    const href = location.href || ''
    if (href.includes('/login')) return { loggedIn: false, reason: 'redirected_to_login', url: href }
    const text = document.body ? document.body.innerText : ''
    if (!text.includes('笔记管理') && !text.includes('草稿箱')) {
      return { loggedIn: false, reason: 'no_manage_entry', url: href }
    }
    return { loggedIn: true, url: href }
    ```
    双重判据（URL + 侧栏「笔记管理/草稿箱」入口）比单看文字稳。**发布前先在 ego-lite 手动登录**，别指望脚本能自动过登录墙。

14. **用户手动登录会触发「用户接管 task space」硬停止**：登录是用户在 ego-lite 窗口手动完成的，这会把 task space 的控制权切给用户（ownership 变为 `user`），之后所有 agent 浏览器命令直接报 `The user has taken control of this task space, so browser commands are paused`。这是**硬停止，不可自行绕过**：不要重试、不要自行夺回，必须让用户回复「继续」，再用 `claimTaskSpace(spaceId)` 认领（控制权已在用户手里，`claimTaskSpace` 才生效；`takeOverTaskSpace` 只适用于 agent 自己结束、ownership 仍为 agent 的空间）。完整流程：脚本因 401 退出 → 提示用户去 ego-lite 登录 → 用户登录并回复 continue → `claimTaskSpace(原 spaceId)` → 重跑发布脚本。

22. **图片上传完成判定有三个信号，别再只看 CDN 计数（v2.0.1 修正）**：v2.0.0 及更早版本的判定有两个硬伤，2026-11-08/09 连续三次误报 `E_IMAGE_UPLOAD_TIMEOUT`（明细 `cdnImages:6 / editCount:"" / expected:8`），而页面上 8 张图其实全部上传成功。
    - **硬伤一（根因）**：`editCount` 的解析写的是「按行找含'图片编辑'的行 → `split('/')[0]` → 滤数字」。但小红书把**标签和数字渲染在两行**（`图片编辑\n8/18`），该行只剩标签本身，滤完是空串，`parseInt("") = NaN`，主判据等于不存在，只能靠 CDN 计数兜底。
    - **硬伤二**：CDN 计数用 `img[src*=xhscdn.com]` 扫全页，会把**用户头像**（`sns-avatar-qc.xhscdn.com`）、UI 图（`fe-img-qc` / `growth-img`）一起数进去，数字既可能虚高也可能永远凑不满——实测 3 张图时只数到 2。
    - **现行判定**：①「图片编辑 N/18」用跨行正则 `/图片编辑[\s:：]{0,6}(\d{1,2})\s*\/\s*(\d{1,2})/`；② 结构判据，数编辑区里 `textContent === '编辑'` 的叶子节点；③ CDN 计数但排除 `avatar`。任一 ≥ 张数即通过。
    - **排查口径**：失败块里 `detail.editCount` 若已是 `N/18` 且 N ≥ expected，说明只是判定逻辑又跟不上改版，**图其实传好了**，直接按 space 接管页面手动填表收尾，不要重跑。
