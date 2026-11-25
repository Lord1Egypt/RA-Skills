---
name: xiaohongshu-post
description: "Publish image-and-text notes to Xiaohongshu (RED) from a logged-in Chrome profile via Playwright over CDP. Covers browser bootstrap that keeps the login alive across agent turn boundaries by persisting the Chrome profile (the browser process itself gets reaped), multi-image upload, title/body filling, insertion of REAL topic tags through the Tiptap suggestion dropdown, pre-publish draft approval, note-id / xsec_token / short-link extraction, and logged-out public-visibility verification. Use when the user asks to post or publish to 小红书 / RED, says 发小红书 / 上传小红书 / 帮我发笔记 / 发个笔记, or wants a note published to a Xiaohongshu account automatically."
license: MIT
compatibility: "Windows 10/11 with Google Chrome or Edge installed; Node.js 18+ for the bundled scripts; Python 3.8+ optional. Needs network access to xiaohongshu.com. The account must already be logged in (SMS login on creator.rednote.com)."
metadata:
  version: "1.0.0"
  language: zh-CN
  tags: xiaohongshu, rednote, social-publishing, playwright, cdp, browser-automation, content-publishing
  agent_created: "true"
---

# 自动发小红书图文笔记（Playwright + CDP）

**核心难点不是"怎么点发布"，是"怎么让浏览器活过对话轮次"以及"怎么拿到能长期有效的公开链接"。** 本 skill 只提供这两处的确定做法与判据，检索/写作/审美的部分由模型自己负责。

---

## 何时用

- 用户要求把内容发到**小红书 / RED**，发图文笔记、发作品推广
- 用户已经备好配图与文案，要求代发
- ⛔ **不适用**：小红书**视频**笔记、直播、评论互动、批量矩阵号（多号发布请逐个确认账号归属）

---

## ⛔⛔ 三条不可跳过的前置判据（先验后做，别先动手）

### 判据 1：账号必须是用户本人的，且要用户亲自完成登录

- 创作服务平台（`creator.rednote.com`）**只有短信登录，没有扫码登录**（2026-10-23 实测）。
- ⛔ **不要让用户把手机号和验证码发到对话里**。正确做法：把浏览器窗口开在用户屏幕上，让**用户自己在窗口里输**。
- ⛔ 绝不代替用户登录他人账号。发布动作使用用户的身份、用户的账号。

### 判据 2：发布前必须给用户看草稿并等到明确点头

流程固定为：**填完 → 截图 → 给用户看 → 等"发/可以/发布" → 才点发布按钮 → 校验 `?published=true`**。
不要把"截图给用户看"和"点发布"合并成一次动作。

### 判据 3：发布后必须验证"公开可访问"，不能只看"发布成功"

`?published=true` 只代表提交成功；笔记可能仍在**审核中**（`tab_status=1`），也可能因任何原因对外不可见。
必须用**全新无痕上下文**打开链接、确认标题与正文真的渲染出来，才算完成（做法见下）。

---

## 一、浏览器启动：持久的是 **profile 目录**，不是浏览器进程

### ⛔⛔ 实测结论（2026-10-23，两种方式都试过）

| 启动方式 | 跨命令存活 | 跨对话轮次存活 |
|---|---|---|
| `playwright-cli open --headed` | 同轮内勉强，跨命令常挂 | ❌ |
| 自己起 Chrome + `--remote-debugging-port` + 挂成后台任务 | ✅ | ❌ **同样被回收** |

**两个后台任务都会被 harness 在轮次结束时清掉**（`TaskOutput` 报 `No task found`）。
⇒ **浏览器进程跨轮次活不下来**。这是本 skill 最容易踩空的一点，别再写"用后台任务常驻"。

### ✅ 真正持久的：`--user-data-dir` 指向的 profile 目录

登录态（小红书的 `id_token` 等 34 条 cookie）写在 profile 里，**进程被回收也不影响**。
⇒ **正确工作模型：每轮用同一个 profile 重新启动 Chrome → 登录态自动恢复 → CDP 挂载 → 干活。**

```bash
# 1) 固定一个 profile 目录（跨轮复用，别每次新建）
mkdir -p <workdir>/.tmp/xhs-cdp

# 2) 每轮启动 Chrome（挂后台任务，只管本轮）
chrome.exe --remote-debugging-port=9222 \
  --user-data-dir="<abs>/.tmp/xhs-cdp" \
  --no-first-run --no-default-browser-check \
  --window-size=1360,900 --window-position=60,40 \
  "https://creator.rednote.com/publish/publish"

# 3) 挂载
playwright-cli -s=xhs attach --cdp http://127.0.0.1:9222
```

> ⚠️ **Chrome ≥136 硬限制**：`--remote-debugging-port` **必须**搭配**非默认** `--user-data-dir` 才生效，
> 否则静默忽略（表现为"CDP 连不上"）。

### 判定登录态是否恢复

```js
// 落在 /login → 登录态没了，需要用户重新登录
// 落在 /publish/publish → profile 里的登录态还在
location.href
```

### 登录怎么做（当确实需要重新登录时）

创作服务平台（`creator.rednote.com`）**只有短信登录，没有扫码登录**。
⛔ **不要让用户把手机号和验证码发到对话里**——把窗口开在用户屏幕上，让**用户自己在窗口里输**。
⛔ 绝不代替用户登录他人账号。

> 附：想抄别人浏览器的登录态去读 cookie 也不行——运行中的浏览器把 Cookies 库锁着
> （`Device or resource busy`），而且**没有小紅書桌面登录态也一样能发**：
> 用全新 profile 短信登录一次即可，之后 profile 自己会记住。

---

## 二、发布流程（图文）

### 2.1 切标签（有个 DOM 陷阱）

`creator.rednote.com/publish/publish` 默认是**上传视频**。要切到「上传图文」。

⛔ **DOM 里有两份同名 tab**：一份 `aria-hidden="true"` 的无障碍镜像，和真标签**尺寸相同、叠在同一坐标**。
普通 `click()` 的命中检测永远被镜像挡住，报 `subtree intercepts pointer events`。

✅ 对**非 aria-hidden 的真元素**直接派发 click：

```js
const switched = await page.evaluate(() => {
  const tabs = Array.from(document.querySelectorAll("div.creator-tab"));
  const real = tabs.filter(e =>
    (e.textContent || "").trim() === "上传图文" && e.getAttribute("aria-hidden") === null);
  if (!real.length) return false;
  real[real.length - 1].click();
  return true;
});
```

切完确认：页面上出现 `input[type=file]`（视频页没有它）。

### 2.2 传图

发布页只有一个 file input，**带 `multiple`**，accept `.jpg,.jpeg,.png,.webp`：

```js
await page.locator('input[type=file]').first()
         .setInputFiles([cover, img2, img3]);   // 第一张 = 封面
```

⛔ 不要用 `upload` 命令（依赖文件选择器弹窗，headed 场景容易卡）。
✅ 传完校验：`document.querySelectorAll('img')` 里应出现对应数量的 200×267 缩略图。

### 2.3 填标题与正文

| 字段 | 选择器 | 限制 |
|---|---|---|
| 标题 | `input[placeholder*="标题"]` | **≤20 字**（含空格与标点） |
| 正文 | `div[contenteditable=true]` | **≤1000 字** |

- 正文编辑器是 **Tiptap**：段落是 `<p>`，换行是独立的 `<p>`。
- 中文正文用 `page.keyboard.insertText(text)` 写入（`fill` 对富文本容易丢换行）。
- ⛔ **不要直接改 `innerHTML`**：Tiptap 会用自己的模型把 DOM 改回去。

### 2.4 ⭐ 插入真话题标签（本流程最容易做错的一步）

小红书的话题必须是由**建议下拉选中**产生的 `a.tiptap-topic` 节点。**纯文本 `#xxx` 不算话题**（不进话题广场、检索不到）。

正确动作序列：

1. 光标移到正文末尾：`Control+End`
2. 逐字符输入 `#` + 关键词（`page.keyboard.type('#WorkBuddy', {delay:120})`）
3. 等 **2.5~3 秒**让建议框弹出（它是 `tippy` 浮层）
4. 在 `.tippy-box` 里点**精确匹配**的那一条

```js
const opt = page.locator('.tippy-box *')
             .filter({ hasText: /^#WorkBuddy$/ }).first();
await opt.click();
```

节点长这样（注意 `[话题]#` 是隐藏的辅助文本，不要拿它做精确匹配）：

```html
<a class="tiptap-topic" data-topic='{"id":"...","name":"WorkBuddy",...}' contenteditable="false">
  #WorkBuddy<span class="content-hide">[话题]#</span>
</a>
```

⭐ **校验话题是否真插入**：读 `data-topic` 里的 `name`，不要读 `innerText`：

```js
Array.from(ed.querySelectorAll('a.tiptap-topic'))
     .map(c => JSON.parse(c.getAttribute('data-topic')).name)
```

⚠️ 页面右侧**手机预览面板会镜像同样的节点**，`querySelectorAll` 会数出 2 倍。校验时必须限定在编辑器容器内：
`ed.querySelectorAll('a.tiptap-topic')`（`ed` = 正文 contenteditable 根节点）。

### 2.5 在话题前断行（想让话题单独成段时）

用**真实选区 + 真实按键**，让 Tiptap 自己去拆段落：

```js
await page.evaluate(() => {
  const ed = document.querySelector('div[contenteditable=true]');
  const chip = ed.querySelector('a.tiptap-topic');       // 第一个话题节点
  const r = document.createRange();
  r.setStartBefore(chip); r.collapse(true);
  const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
});
await page.keyboard.press('Enter');
```

⛔ 直接 `insertBefore` 一个 `<p>` 会被 Tiptap 回滚。

### 2.6 草稿截图给用户确认

- 页面用**内层滚动容器**，不是 window 滚动 → `page.screenshot({fullPage:true})` 只能拍到当前视口。
- 拍顶部：先 `await page.locator('input[placeholder*="标题"]').scrollIntoViewIfNeeded()` 再截图。
- 把两张图（顶部 + 正文）都交给用户看，同时口头列出：标题/字数/图片数/话题名/链接。

---

## 三、发布后：拿到链接并验证公开可见

### 3.1 笔记元数据（⛔ 不要自己 fetch）

⛔ 该接口带**签名头**（`x-s` / `x-t` / `x-s-common`），自己 `fetch` 会拿到 **HTTP 406**；
即便 URL 少了 `?tab=0&page=0` 也会返回空 `notes`。

✅ 正确做法：**拦截页面自己发出的请求**，读它的响应体：

```js
let body = null;
const onResp = async r => { if (/note\/user\/posted/.test(r.url())) { try { body = await r.text(); } catch (_) {} } };
page.on("response", onResp);
await page.goto("https://creator.rednote.com/new/note-manager", { waitUntil: "domcontentloaded" });
for (let i = 0; i < 20 && !body; i++) await page.waitForTimeout(500);
page.off("response", onResp);
const note = JSON.parse(body).data.notes[0];
```

关键字段：`id`（笔记 ID）、`xsec_token`、`xsec_source`、`display_title`、`tab_status`（**1 = 审核中**）、`visible_time`。
⛔ `notes[0]` 是**最新一条**——如果要确认某条特定笔记，遍历比对 `display_title`。

### 3.2 公开链接

```
https://www.xiaohongshu.com/explore/<id>?xsec_token=<urlencoded token>&xsec_source=pc_creatormng
```

⛔ **不带 token 的裸链接（`/explore/<id>` 或 `/discovery/item/<id>`）实测一律 302 到 404**，必须带 token。

短链（更利于分享，需 www 域有登录态）：

```
POST https://edith.xiaohongshu.com/api/sns/web/share/code   →  {"data":"<15位key>"}
→  https://xhslink.com/<key>
```

### 3.3 ⭐ 公开可访问性验证（curl 做不到，必须用无痕上下文）

小红书笔记页是**客户端渲染**，SSR HTML 里没有笔记内容，标题也只有通用文案 → **curl 永远验不出来**。

```js
const ctx = await page.context().browser().newContext();   // 全新无痕 = 未登录
const p2 = await ctx.newPage();
await p2.goto(publicUrl, { waitUntil: 'domcontentloaded' });
await p2.waitForTimeout(4000);
const ok = await p2.evaluate(() => ({
  title: document.title,                                  // 期望含笔记标题
  hit: document.body.innerText.includes('笔记标题前几个字'),
}));
await ctx.close();
```

判据：
- `document.title` 含笔记标题 + `hit === true` → **公开可见**（浮一层登录弹窗是正常的，右上角有 X 可关）
- 跳到 `/404` 或 title 是「你访问的页面不见了」→ **不可见**（多半是缺 token 或笔记未过审）

---

## 四、脚本

| 文件 | 作用 |
|---|---|
| `scripts/bootstrap_browser.sh` | 起带调试端口的 Chrome 并挂载 playwright-cli，幂等 |
| `scripts/publish_note.js` | 填标题/正文/话题/传图，**默认不点发布**（`--publish` 才点） |
| `scripts/verify_note.js` | 取 id/token/短链 + 无痕上下文验证公开可见 |
| `references/selectors.md` | 全部选择器、API、字段、踩坑清单 |
| `references/copy-guide.md` | 小红书文案与配图规格（标题字数、正文字数、封面比例、话题双写） |

脚本只用 `playwright` / `playwright-core`（会自动去找全局 `@playwright/cli` 自带的 `playwright-core`），零第三方依赖。

---

## 五、已知坑速查

| 现象 | 真因 | 处置 |
|---|---|---|
| 浏览器莫名消失（无论 playwright-cli 起还是后台任务起） | 随对话轮次被回收 | **认了**：持久的是 profile 目录，每轮用同一个 profile 重启（第一节） |
| 换了 profile 后要重新登录 | 登录态存在 profile 里 | 复用固定 profile 目录，别每次新建 |
| `--remote-debugging-port` 无效 | Chrome ≥136 要求非默认 `--user-data-dir` | 加 `--user-data-dir=<固定目录>` |
| 点「上传图文」报 intercepts pointer events | 有一份同尺寸的 aria-hidden 镜像盖在上面 | 对非 aria-hidden 的真元素派发 click（2.1） |
| `snapshot` 没输出到 stdout | 默认写 `.playwright-cli/page-*.yml` | 用 `--filename=` 指定后读文件 |
| `strings` 命令不存在 | Git Bash 无该工具 | 用 `grep -a` 或 Python 读二进制 |
| 浏览器的 Cookies 读不出来 | 运行中文件被锁（`Device or resource busy`） | 要读就先关浏览器；发笔记用全新 profile 即可 |
| 话题输成纯文本 | 没点建议下拉 | 走 2.4 的 tippy 流程，校验 `data-topic` |
| 话题数了 2 倍 | 右侧手机预览镜像了同一批节点 | 校验时限定在编辑器容器内 |
| 改 innerHTML 后被回滚 | Tiptap 用自己的文档模型 | 用真实选区 + 真实按键 |
| fetch 笔记接口拿到 406 | 接口要签名头 | 拦截页面自己的请求读响应体（3.1） |
| curl 验不出公开可见 | 页面客户端渲染 | 用无痕上下文断言 `document.title` |
| 裸链接 404 | 缺 `xsec_token` | 用带 token 的 explore 链接 |
| 笔记管理 goto 被弹回 | 路由守卫 | 点侧边栏「笔记管理」 |

---

## 六、边界

- 只发**图文**笔记；视频、直播、评论不在本 skill 范围。
- 不代用户登录、不保管账号凭证、不绕验证码。
- 发布前必须等用户明确点头；发布后必须验公开可见。
- 平台规则以小红书官方为准；本 skill 记录的是 2026-10-23 实测行为，平台改版后需重新核对 `references/selectors.md`。
