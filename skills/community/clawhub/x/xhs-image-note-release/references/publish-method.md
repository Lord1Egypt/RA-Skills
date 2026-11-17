# 小红书图文笔记自动发布方法（技术原理）

> 通过 ego-browser 发布小红书笔记的方法论文档。
>
> ⚠️ **本文件写于 v1.x，部分结论已被后续实测推翻。** 下面 4 处已就地修正并标注；
> **与 `SKILL.md` 冲突时一律以 SKILL.md 为准**。日常执行不要读本文件，
> 它只用于理解 `_onPublish` / `_onSave` 这类底层机制。

## 一、整体流程（9 步）

```
创建 task space → 打开创作平台 → 等待 SPA 渲染
→ 上传图片（uploadFile 逐张）→ 填标题 → 填正文 → 关闭弹窗
→ 调用 _onPublish() 发布 → 等待 published=true → 清理 task space
```

## 二、各步骤技术要点

### 1. 环境准备

- ego-lite 必须在前台运行
- WorkBuddy 沙箱必须关闭（沙箱会导致 ego-browser 进程被 SIGKILL，exit 137）
- ego-browser 继承用户登录态，小红书需已在 ego-lite 中登录
- 检测沙箱：如果报错包含 `from the default agent sandbox`，说明沙箱未关闭

### 2. 打开创作平台

```
URL: https://creator.xiaohongshu.com/publish/publish
```

小红书创作平台是 **Vue SPA**，`<div id="app">` 初始为空，需要等待 **15 秒** 才能完成渲染。

- `waitForNetworkIdle(5)` 不够：网络空闲时 DOM 可能还没渲染
- 必须显式 `await wait(15)` 
- 然后用 `js()` 检查 `document.getElementById('app').childElementCount` 确认渲染完成

### 3. 进入图文发布页

页面加载后显示「发布笔记」下拉按钮。需要两步点击：

1. 点击「发布笔记」展开下拉菜单
2. 点击「上传图文」进入图文编辑器

用 `snapshotText()` 获取语义快照，正则匹配 ref 编号后 `click('@N')`。

### 4. 上传图片（关键坑点）

小红书的图片上传 `<input type="file">` 的 class 是 `upload-input`。

**不能用** `uploadFile()` 传逗号分隔的多文件路径（不生效，只上传第一张或无反应）。

> 🔴 **【已推翻，2026-08 实测】** 原文推荐「CDP `DOM.setFileInputFiles` 批量设置 + 手动触发
> `input`/`change`」，实测这条路**走不通**：编辑器会显示「图片编辑 10/18」，但缩略图全是空占位符，
> 存草稿后图片为空。**正确做法是 `uploadFile()` 逐张上传**（每张等 6s，全部传完再等 4s），
> 每次调用都会触发真实的文件选择事件。当前 `publish_note.mjs` 已按逐张实现。
>
> 下面这段 CDP 批量代码**仅作历史记录，不要照用**。

```js
const doc = await cdp('DOM.getDocument', {})
const inputNode = await cdp('DOM.querySelector', {
  nodeId: doc.root.nodeId,
  selector: 'input.upload-input'
})
await cdp('DOM.setFileInputFiles', {
  files: ['/path/to/card_01.png', '/path/to/card_02.png', ...],
  nodeId: inputNode.nodeId
})

// 关键：触发事件，让前端开始上传
const input = document.querySelector('input.upload-input')
input.dispatchEvent(new Event('input', { bubbles: true }))
input.dispatchEvent(new Event('change', { bubbles: true }))

await wait(12)  // 等待图片上传到 CDN 并生成预览
```

**上传校验**：统计小红书 CDN 预览图数量，确认图片真的上传成功：

```js
const cdnCount = [...document.querySelectorAll('img')].filter(i =>
  (i.src || '').includes('xhscdn.com') || (i.src || '').includes('spectrum/')
).length
if (cdnCount < filePaths.length) {
  throw new Error('图片未正确上传到小红书，可能只留下了空占位符')
}
```

- 图片推荐尺寸：1080x1440（3:4 竖屏）
- 最多 18 张
- 文件路径必须是绝对路径

### 5. 填写标题

```js
await fillInput('css:input[placeholder="填写标题会有更多赞哦"]', '标题内容')
```

标题限制 20 字符，超出会被截断。

### 6. 填写正文

正文区域是 `contenteditable="true"` 的富文本编辑器，不是 `<textarea>` 或 `<input>`：

```js
// 先 focus 编辑器
await js(`document.querySelector('[contenteditable="true"]').focus()`)
// 再用 typeText 输入（支持 \n 换行和 #话题标签）
await typeText('正文内容...\n\n#话题1 #话题2')
```

输入完成后按 `Escape` 关闭话题建议弹窗（输入 `#` 后小红书会弹出话题建议列表）。

### 7. 点击发布按钮（最关键的坑点）

#### 问题分析

小红书的「发布」按钮被封装在 **`<xhs-publish-btn>`** 自定义 Web Component 中，该组件使用 **closed Shadow DOM**：

```html
<xhs-publish-btn submit-text="发布" submit-disabled="false" submit-loading="false">
  #shadow-root (closed)    ← closed 意味着 host.shadowRoot 返回 null
    <div class="publish-page-publish-btn">
      <button class="ce-btn bg-red">发布</button>
    </div>
</xhs-publish-btn>
```

#### 失败的方法（全部无效）

| 方法 | 结果 | 原因 |
|---|---|---|
| `document.querySelector('button.ce-btn.bg-red')` | 找不到 | 按钮在 shadow DOM 内，主文档查询不到 |
| `host.shadowRoot.querySelector(...)` | `shadowRoot` 为 `null` | closed shadow DOM 不暴露 shadowRoot 属性 |
| `click('@N')` via snapshotText | 无 ref 可用 | snapshotText 不穿透 shadow DOM |
| `cdp('DOM.performSearch', {includeUserAgentShadowDOM: true})` | 找到节点但 nodeId=0 | closed shadow DOM 的节点无法被 CDP 操作 |
| `cdp('DOM.enable') + DOM.performSearch` | 同上 | 即使启用 DOM agent 也无法穿透 closed shadow |
| `cdp('Input.dispatchMouseEvent', {x, y})` | 不触发 Vue 事件 | 坐标点击不触发 Vue 的事件绑定 |
| `host.click()` | 点击的是宿主元素 | 宿主没有绑定 click 事件，内部按钮未触发 |

#### 成功的方法

**直接调用组件暴露的内部方法 `_onPublish()`**：

```js
const host = document.querySelector('xhs-publish-btn')

// 检查按钮状态
const submitDisabled = host.getAttribute('submit-disabled')  // 'false' = 可点
const submitLoading = host.getAttribute('submit-loading')     // 'false' = 未在加载

if (submitDisabled === 'true') {
  // 按钮被禁用，可能标题或正文为空
  throw new Error('Publish button is disabled')
}

// 直接调用内部发布方法
host._onPublish()
```

**原理**：`<xhs-publish-btn>` 是一个 Web Component（自定义元素），其原型链上暴露了 `_onPublish` 和 `_onSave` 方法。这些方法绑定在组件实例上，通过 `host._onPublish()` 可以直接调用，绕过 Shadow DOM 的封装。

**发现方法**：通过 `Object.getOwnPropertyNames(Object.getPrototypeOf(host))` 列出组件原型上的所有方法名，发现 `_onPublish`、`_onSave` 等内部方法。**`_onPublish` 与 `_onSave` 是同一个 `<xhs-publish-btn>` 组件上的兄弟方法**——发布和存草稿共用这一个按钮组件，只是触发的不同方法。

#### 验证发布状态

- 按钮进入 loading：`host.getAttribute('submit-loading')` 变为 `'true'`
- **发布成功（主判据）**：页面约 5-10 秒后 URL 出现 `published=true`
- 检查方式：`pageInfo().url.includes('published=true')`

> 🔴 **【已修正，2026-11-02】** 原文写的判据是跳转 `note-manage`。
> 现在直接访问 `/publish/note-manage` 已 **404**，该路径只作旧行为兜底；
> 主判据是 `published=true`。确认发布结果请走侧栏「笔记管理」入口，别手工拼 URL。

### 7b. 存草稿模式（_onSave 方法）

#### 需求场景

用户要求「存草稿 / 推到草稿箱 / 自己点发布」时走此模式：笔记进入小红书草稿箱，由用户自行检查后点发布。多笔记批量发布前应全部存草稿，再手动间隔 ≥5 分钟逐一发布，避风控。

#### ⚠️ 关键坑点：根本没有「存草稿」按钮

- 发布页右下角的按钮**文本不是「存草稿」，而是「暂存离开」**（组件属性为 `save-text="暂存离开"`、`is-save-draft="true"`、`save-disabled="false"`）。
- 这个按钮同样在 `<xhs-publish-btn>` 的 **closed Shadow DOM** 内：DOM 遍历、`snapshotText` 正则匹配、`click('@N')`、坐标点击全部抓不到文本/节点。
- 若按"存草稿"文本去搜索点击，永远找不到，页面也不会有任何变化。
- **正确做法**：直接调组件实例方法 `host._onSave()`（发布用 `host._onPublish()`）。

```js
const host = document.querySelector('xhs-publish-btn')

// 检查存草稿按钮状态
const saveDisabled = host.getAttribute('save-disabled')  // 'false' = 可存
if (saveDisabled === 'true') {
  throw new Error('Save-draft button is disabled')
}

// 直接调用内部存草稿方法（不是找按钮点）
host._onSave()
```

**发现方法**：与 `_onPublish` 同源——`Object.getOwnPropertyNames(Object.getPrototypeOf(host))` 列出原型方法，其中既有 `_onPublish` 也有 `_onSave`；进一步用 `Object.getOwnPropertyNames(host)` 可查实例自有方法，确认 `_onSave` 绑定在组件实例上。

#### 校验存草稿状态（页面不跳转）

调用 `_onSave()` 后页面**不会跳转**，而是把笔记存入**当前浏览器本地**（页面会提示"草稿存储于当前使用的浏览器本地"）。不能用 URL 变化验证，必须靠「草稿箱(N)」计数 +1：

- 读取左侧导航文案，正则 `草稿箱\((\d+)\)`
- 调用前后比较，计数 +1 即成功

```js
await wait(6)
const draftN = await js(`(() => {
  const m = document.body.innerText.match(/草稿箱\\((\\d+)\\)/)
  return m ? m[1] : 'n/a'
})()`)
// draftN 与调用前相比 +1 即校验通过
```

#### _onPublish vs _onSave 失败方案对比（合并）

| 方法 | 发布 `_onPublish` | 存草稿 `_onSave` |
|---|---|---|
| 按文本找按钮（"发布"/"存草稿"） | 无文本节点可匹配 | ❌ 连文字都是「暂存离开」，更找不到 |
| `host.shadowRoot.querySelector(...)` | `null`（closed shadow） | 同左 |
| `click('@N')` via snapshotText | 无 ref | 同左 |
| 坐标 `Input.dispatchMouseEvent` | 不触发 Vue 事件 | 同左 |
| **直接调实例方法** | ✅ `host._onPublish()` | ✅ `host._onSave()` |

### 8. 清理

```js
await completeTaskSpace(task.id, { keep: false })
```

## 三、注意事项

1. **沙箱限制**：WorkBuddy 的 Bash 工具即使在"完全访问"模式下，ego-browser 仍可能检测到 macOS sandbox。如果报错 `from the default agent sandbox`，需要在 WorkBuddy 设置中关闭沙箱。
2. **SPA 渲染**：小红书创作平台首次加载需要 15 秒，不要用 `waitForNetworkIdle` 代替。
3. **话题标签**：输 `#` 会弹建议列表，**必须从列表里点选才算挂上**。直接粘贴 `#话题1 #话题2` 只生成纯文本，不会挂载。选完后按 `Escape` 关弹窗。
4. **图片尺寸**：推荐 1080x1440（3:4 竖屏），最多 18 张。
5. **发布频率**：不要短时间内连续发布多篇，可能触发风控。
6. **标题字数**：小红书标题限制 20 字符。
7. **正文字数**：小红书正文限制 1000 字符。
