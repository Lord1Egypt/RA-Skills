# 选择器 / API / 字段 / 踩坑 全清单

> 记录时间：**2026-10-23 实测**（小红书 web 创作服务平台，Chrome 156）
> 平台改版后请以本文件为准重新核对；发现差异请更新本文件再发布。

---

## 一、页面与路由

| 用途 | URL | 备注 |
|---|---|---|
| 创作中心发布页 | `https://creator.rednote.com/publish/publish` | 登录后会自动从 `creator.xiaohongshu.com` 跳到 `rednote.com` |
| 登录页 | `https://creator.rednote.com/login?source=&redirectReason=401&lastUrl=%252Fpublish%252Fpublish` | **只有短信登录** |
| 笔记管理 | `https://creator.rednote.com/new/note-manager` | 直接 goto 会被弹回发布页，**必须点侧边栏「笔记管理」** |
| 公开笔记页 | `https://www.xiaohongshu.com/explore/<id>?xsec_token=<enc>&xsec_source=pc_creatormng` | 缺 token → 302 到 `/404` |
| 短链 | `https://xhslink.com/<key>` | key 来自 `share/code` 接口 |

---

## 二、选择器

### 发布页（图文）

| 元素 | 选择器 | 说明 |
|---|---|---|
| 视频标签 | `div.creator-tab`（含「上传视频」） | 默认选中，要点掉 |
| 图文标签 | `div.creator-tab`（含「上传图文」）**且 `aria-hidden` 为 null** | ⛔ 见下方「双份同名 tab」 |
| 文件输入 | `input[type=file]` | 页面**只有一个**，带 `multiple`，accept `.jpg,.jpeg,.png,.webp` |
| 标题 | `input[placeholder*="标题"]` | placeholder 是「填写标题会有更多赞哦」；≤20 字 |
| 正文 | `div[contenteditable=true]` | Tiptap 富文本；≤1000 字 |
| 话题建议框 | `.tippy-box` | 浮层，出现在编辑器上方 |
| 话题节点 | `a.tiptap-topic` | `data-topic` JSON 里 `name` 是真名；`innerText` 带隐藏的「[话题]#」 |
| 发布按钮 | `getByText('发布', {exact:true}).last()` | 旁边还有「暂存离开」，别点错 |
| 原创声明 | 开关控件 | 默认关闭；开不开由用户定 |

### ⛔ 双份同名 tab（命中检测陷阱）

DOM 里「上传图文」有**两份**：

```html
<div class="creator-tab" aria-hidden="true">  <!-- 无障碍镜像，96×40，叠在真标签同一坐标 -->
  <span class="title">上传图文</span>          <!-- 80×22 -->
</div>
<div class="creator-tab">                      <!-- 真标签，96×40 -->
  <span class="title">上传图文</span>          <!-- 64×24 -->
</div>
```

`getByText('上传图文').first()` / `.click()` → Playwright 报
`subtree intercepts pointer events`，**点不动**。

✅ 对真元素直接派发 click：

```js
const real = Array.from(document.querySelectorAll('div.creator-tab'))
  .filter(e => e.textContent.trim() === '上传图文' && e.getAttribute('aria-hidden') === null);
real[real.length - 1].click();
```

### 正文编辑器（Tiptap）结构

```html
<div contenteditable="true" class="tiptap ProseMirror">
  <p>第一段</p>
  <p>\n</p>            <!-- 段落分隔用的空 p -->
  <p>第二段</p>
  <a class="tiptap-topic" data-topic='{"id":"...","name":"WorkBuddy","link":"..."}' contenteditable="false">
    #WorkBuddy<span class="content-hide">[话题]#</span>
  </a>
</div>
```

⭐ `insertText` 传含 `\n` 的长文本 → 自动拆成多个 `<p>`（已实测）。
⭐ 直接改 `innerHTML` → Tiptap 用自己的文档模型**回滚**。要断行就用真实选区 + 真实 Enter。

---

## 三、接口

### 笔记列表（拿 id / token）

⛔ **自己 fetch 会 406**（接口要签名头 `x-s` / `x-t` / `x-s-common`）；
⛔ 少了 `?tab=0&page=0` 也会返回空 `notes`。

✅ **拦截页面自己的请求**读响应体：

```js
let body = null;
const onResp = async r => { if (/note\/user\/posted/.test(r.url())) { try { body = await r.text(); } catch (_) {} } };
page.on('response', onResp);
await page.goto('https://creator.rednote.com/new/note-manager', { waitUntil: 'domcontentloaded' });
for (let i = 0; i < 20 && !body; i++) await page.waitForTimeout(500);
page.off('response', onResp);
const note = JSON.parse(body).data.notes[0];
```

请求 URL 全貌：`https://creator.rednote.com/api/galaxy/v2/creator/note/user/posted?tab=0&page=0`

响应 `data.notes[0]` 关键字段：

| 字段 | 含义 |
|---|---|
| `id` | 笔记 ID（24 位 hex） |
| `xsec_token` | 公开链接必需的 token |
| `xsec_source` | 通常 `pc_creatormng` |
| `display_title` | 笔记标题 |
| `tab_status` | **0=已发布 1=审核中 2=未通过** |
| `visible_time` | 可见时间（Unix 秒） |
| `images_list[].url` | 配图 CDN 地址 |
| `view_count` / `likes` / `comments_count` / `collected_count` | 数据 |

### 短链

```js
POST https://edith.xiaohongshu.com/api/sns/web/share/code
// 需 www 域有登录态；无登录态返回 {"code":-101,"msg":"无登录信息，或登录信息为空"}
// 成功返回 {"data":"<15位key>"} → https://xhslink.com/<key>
```

### 账号信息

```js
GET https://creator.rednote.com/api/galaxy/user/info
// data.userId / data.userName / data.userAvatar
```

---

## 四、公开可见性验证

⛔ **curl / WebFetch 验不出来**。笔记页客户端渲染，SSR HTML 里：
- `<title>` 是通用文案「小红书 - 你的生活兴趣社区」
- 正文、`WorkBuddy` 等关键词出现 0 次

✅ 唯一可靠做法：**开一个全新无痕 context**（= 未登录视角）打开链接：

```js
const ctx = await browser.newContext();          // 不带任何 cookie
const p2 = await ctx.newPage();
await p2.goto(url, { waitUntil: 'domcontentloaded' });
await p2.waitForTimeout(4000);
const r = await p2.evaluate(() => ({
  url: location.href,
  title: document.title,                            // 期望含笔记标题
  hit: document.body.innerText.includes('标题前几个字')
}));
await ctx.close();
```

判据表：

| 现象 | 结论 |
|---|---|
| `title` 含笔记标题 + `hit=true` | ✅ 公开可见（浮登录弹窗正常，右上角 X 可关） |
| 落地 `/404`，title「你访问的页面不见了」 | ❌ 链接无效（缺 token / 笔记被删） |
| title 通用、`hit=false` | ❌ 未渲染出来（可能未过审或被风控） |

---

## 五、坑与处置

| 现象 | 真因 | 处置 |
|---|---|---|
| headed 浏览器突然消失 | 随对话轮次被回收 | 自起 Chrome + `--remote-debugging-port` + CDP 挂载 |
| 调试端口连不上 | Chrome ≥136 要求非默认 `--user-data-dir` | 加 `--user-data-dir=<新目录>` |
| `playwright-cli` 命令找不到 | 未装 | `npm install -g @playwright/cli@latest` |
| `snapshot` 没打印到 stdout | 默认写 `.playwright-cli/page-*.yml` | `--filename=x.yaml` 后读文件 |
| 浏览器 Cookies 读不出来 | 运行中被锁（`Device or resource busy`） | 要读先关浏览器；发笔记用全新 profile |
| `strings` 不存在 | Git Bash 无此工具 | `grep -a` 或 Python 读二进制 |
| 话题变成纯文本 | 没点建议下拉 | 走 tippy 流程，校验 `data-topic` |
| 话题数出 2 倍 | 右侧手机预览镜像同一批节点 | 校验时限定 `ed.querySelectorAll(...)` |
| 改 innerHTML 被回滚 | Tiptap 文档模型 | 真实选区 + 真实按键 |
| `fetch` 笔记接口拿到空 | 缺 query 参数 | 用页面自身请求的完整 URL |
| 笔记管理 goto 被弹回 | 路由守卫 | 点侧边栏「笔记管理」 |
| Windows 下 bash 路径 | 反斜杠 | 一律用正斜杠 |

---

## 六、平台规格（2026-10 实测）

| 项 | 限制 |
|---|---|
| 标题 | ≤ **20 字**（含空格标点） |
| 正文 | ≤ **1000 字** |
| 图片 | 最多 **18** 张；第一张为封面 |
| 封面比例 | 3:4（1080×1440）官方推荐；2:3 会被裁/补边 |
| 图片格式 | jpg / jpeg / png / webp |
| 话题 | 必须由建议下拉选中，生成 `a.tiptap-topic`；纯文本不算 |
| 原创声明 | 默认关闭，开了会多一层声明流程 |
| 发布后 | 立即进入 `tab_status=1`（审核中），公开可见要等审核过 |
