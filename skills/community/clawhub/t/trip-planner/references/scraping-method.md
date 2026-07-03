# 高效网页抓取方法（Claude in Chrome）

> 适用：携程/飞猪机票、酒店价格，携程/高德酒店与民宿评论等动态网页。
> 核心目标：用 **DOM/JS 提取** 替代 **截图认图**，把每次提取的 token 成本压到接近零，并拿到可直接落表的结构化数据。
> 方法由用户用 Cowork 研究产出，本文档基于 4 个真实页面实测验证。

> **复验记录（2026-06-13，本 skill 实机重测，结论：可行、采用）：**
> - ✅ **携程机票** `.flight-box` + 字段选择器（`.flight-airline`/`.plane-No`/`.depart-box .time`/`.price`）——
>   一次取 12 航班结构化 JSON，零截图。**唯一坑：首个 `.flight-box` 常是"X→Y 推荐位"广告，无航班字段；
>   用 `.filter(f=>f.dep&&f.price)` 滤掉即可**（本文档模板已含该过滤）。
> - ✅ **高德 POI 评价** `[class*="ReviewList_reviewItem__"]`——取 30 条带作者+日期+正文，**纯 JS、零 canvas
>   报错**。这直接解决了之前几轮高德"截图报参数错/SSR 不渲染"的痛点：**评价在 HTML 面板里、JS 抓得到，
>   只有背景地图是 canvas**。以后高德评论一律走 JS，不要再靠截图认图、更不要因截图失败就下"没评价"结论。
> - ✅ **携程酒店点评** `[class*="reviewSwiper_reviewSwiper-item"]` 选择器命中；评分/点评数可用
>   `innerText.match(/[1-5]\.\d/)` 与 `/\d[\d,]+\s*条点评/` 取（注意区分总分 vs 分项分，必要时定位到顶部评分块）。
> - ⚠️ **飞猪机票** `tr.flight-item-tr` 沿用 Cowork 实测（本轮飞猪站点不可达未复验）；站点能开时按模板抓。

---

## 一、核心原则

**能用 JS 读 DOM，就别截图。**

截图（`computer` 的 screenshot）一张约 1000+ token，而且会一直留在上下文里，多翻几页就「上下文爆炸」。相比之下，`javascript_tool` 只返回你提取的那几个字段，成本极低，数据还是结构化的。

工具优先级（成本由低到高）：

1. **`javascript_tool`** —— 知道选择器时首选，`querySelector` 精确取数，返回 JSON。
2. **`get_page_text`** —— 只要正文文本（文章类）时用。
3. **`read_page`** —— 需要理解页面结构 / 拿元素引用时用（无障碍树，约 800 token，复杂页可能上万，慎用）。
4. **`find`** —— 自然语言定位某个按钮/输入框。
5. **`computer` 截图** —— 只在以下情况用：① 确认页面是否加载完；② DOM 取不到、需要看视觉；③ canvas 渲染的内容（如地图）。

---

## 二、标准三步工作流

任何一个新页面，都按这三步走，**全程通常只截 1 张图**：

### 步骤 1 — 导航 + 1 张图确认加载

```
navigate → wait(5s) → screenshot   ← 用 browser_batch 合并成一次调用
```

只截这一张，确认页面渲染出来了、是否需要登录、数据大概在哪。

### 步骤 2 — 探测结构（关键）

不要靠猜类名。用一段「探测脚本」自动找出重复卡片的容器类名：

```javascript
(() => {
  const all = Array.from(document.querySelectorAll('div,li,tr,p'));

  // A. 从一个已知文本（如某航班号/某句评论）回溯父级，看它在什么容器里
  const el = all.find(e => e.children.length === 0 && /已知关键词/.test(e.textContent));
  let node = el, path = [];
  for (let i=0; i<7 && node; i++){ path.push((node.className||'').toString().slice(0,55)); node = node.parentElement; }

  // B. 统计「出现 N 次」的可疑列表类名（重复 = 列表项）
  const counts = {};
  all.forEach(e => (e.className||'').toString().split(/\s+/).forEach(k => {
    if (/flight|item|row|list|card|review|comment|content|user/i.test(k)) counts[k] = (counts[k]||0)+1;
  }));
  const candidates = Object.entries(counts).filter(([,n]) => n>=3 && n<80).sort((a,b)=>b[1]-a[1]).slice(0,15);

  return JSON.stringify({ path, candidates }, null, 1);
})()
```

出现次数稳定（如 6 次、16 次、111 次）且语义相关的类名，就是「每条记录」的容器。

### 步骤 3 — 批量提取成 JSON

锁定容器后，对每个容器内部 `querySelector` 取字段，返回数组。见下方各站点模板。

---

## 三、两个最重要的技巧

### 技巧 1：CSS-modules 哈希类名 → 用「前缀/包含匹配」

携程酒店点评、高德评价用的是构建工具生成的哈希类名，例如：

```
ReviewList_reviewItem__KQ37n      高德
reviewSwiper_reviewItem-content__HB2hC   携程
```

`__KQ37n` 这种后缀**每次发版都会变**，写死必废。用属性包含选择器只匹配稳定的前缀：

```javascript
// ✅ 稳定
document.querySelectorAll('[class*="ReviewList_reviewItem__"]')
document.querySelectorAll('[class*="reviewItem-content"]')

// ❌ 易碎
document.querySelectorAll('.ReviewList_reviewItem__KQ37n')
```

> 经验：携程机票（`.flight-box`）、飞猪机票（`.flight-item-tr`）用的是**普通稳定类名**，可直接写；
> 携程酒店点评、高德评价是 **CSS-modules 哈希**，必须前缀匹配。

### 技巧 2：懒加载 / 虚拟滚动 → 用 JS 滚动循环触发

有的页面一次性把全部数据塞进 DOM，有的边滚边加载。先判断，再决定要不要滚：

```javascript
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  let last = 0;
  for (let i=0; i<15; i++){
    window.scrollTo(0, document.body.scrollHeight);
    await sleep(700);
    const n = document.querySelectorAll('选择器').length;
    if (n === last && i > 2) break;   // 数量不再增长 → 加载完
    last = n;
  }
  window.scrollTo(0, 0);
  return last;
})()
```

> 实测：**携程机票**虚拟滚动，初始只 6 条，需滚动加载；**飞猪机票**一次性渲染全部 111 条，无需滚动。

---

## 四、各站点实测模板（可直接复用）

### 1. 携程机票列表

- 容器：`.flight-box`（稳定类名）
- 需要滚动懒加载
- 内部字段：`.flight-airline` / `.plane-No` / `.depart-box .time` / `.depart-box .airport` / `.arrive-box .time` / `.arrive-box .airport` / `.price` / `.flight-tag`

```javascript
Array.from(document.querySelectorAll('.flight-box')).map(b => ({
  airline:    b.querySelector('.flight-airline')?.textContent.trim(),
  flightNo:   b.querySelector('.plane-No')?.textContent.trim(),
  dep:        b.querySelector('.depart-box .time')?.textContent.trim(),
  depAirport: b.querySelector('.depart-box .airport')?.textContent.trim(),
  arr:        b.querySelector('.arrive-box .time')?.textContent.trim(),
  arrAirport: b.querySelector('.arrive-box .airport')?.textContent.trim(),
  price:     (b.querySelector('.price')?.textContent || '').replace(/起|\s/g,''),
  tags: Array.from(b.querySelectorAll('.flight-tag, .tag')).map(e=>e.textContent.trim())
}));
```

### 2. 飞猪机票列表

- 容器：`tr.flight-item-tr`（稳定类名），**一次性全部渲染，无需滚动**
- 单元格：`.flight-line`（航司+航班号+机型）/ `.flight-time`（含起降，正则抓 `\d{1,2}:\d{2}`）/ `.flight-port`（起降机场）/ `.flight-price`
- 注意：飞猪价格是**不含税费**的起价；行有隐藏副本，用 `offsetParent!==null` 过滤可见行 + 按航班号去重

```javascript
(() => {
  const rows = Array.from(document.querySelectorAll('tr.flight-item-tr')).filter(r => r.offsetParent !== null);
  const seen = new Set();
  return rows.map(r => {
    const line  = (r.querySelector('.flight-line')?.textContent || '').replace(/\s+/g,' ').trim();
    const times = (r.querySelector('.flight-time')?.textContent || '').match(/\d{1,2}:\d{2}/g) || [];
    const ports = (r.querySelector('.flight-port')?.textContent || '').replace(/\s+/g,' ').trim()
                    .split(/\s+(?=白云|虹桥|浦东|宝安)/);
    return {
      info: line,                                   // 例 "春秋9C8930 中型机 321"
      dep: times[0], arr: times[1],
      depAirport: ports[0], arrAirport: ports[1],
      price:    (r.textContent.match(/¥\s*\d+/) || [])[0],
      discount: (r.textContent.match(/[\d.]+折/) || [])[0]
    };
  }).filter(f => { const k = f.info + f.dep; if (seen.has(k)) return false; seen.add(k); return true; });
})();
```

### 3. 携程酒店点评

- 详情页向下滚动加载点评区
- 容器：`[class*="reviewSwiper_reviewSwiper-item__"]`（**CSS-modules 哈希，前缀匹配**）
- 字段前缀：`reviewItem-userName` / `reviewItem-userReviewTime` / `reviewItem-content`
- **坑**：① 用户名里被插入**零宽字符**（`​`/`‍` 等），需 strip；② 轮播 + 列表有重复，需**去重**；③ 长评论尾部有「全文」按钮，需展开取全文
- 抓全部 1465 条：点「显示所有点评」展开弹层，弹层内翻页/滚动，选择器策略相同

```javascript
(() => {
  const strip = s => (s || '').replace(/[​-‏‪-‮⁠﻿]/g, '').trim();
  const items = [...new Set(
    Array.from(document.querySelectorAll('[class*="reviewSwiper_reviewSwiper-item__"]'))
  )];
  const pick = (it, frag) => it.querySelector(`[class*="${frag}"]`)?.textContent.trim().replace(/\s+/g,' ');
  const seen = new Set();
  return items.map(it => ({
    user:    strip(pick(it, 'reviewItem-userName')),
    time:    pick(it, 'reviewItem-userReviewTime'),
    content: pick(it, 'reviewItem-content')
  })).filter(r => r.content && !seen.has(r.content) && seen.add(r.content));
})();
```

### 4. 高德地图 POI 评价

- POI 详情面板是 **HTML 可抓**；背景地图是 **canvas，读不出**（要地图视觉信息才截图）
- 容器：`[class*="ReviewList_reviewItem__"]`（**CSS-modules 哈希，前缀匹配**）
- 字段前缀：`ReviewList_authorName` / `ReviewList_reviewTime` / `ReviewList_reviewText`
- 长评价尾部同样有「全文」

```javascript
Array.from(document.querySelectorAll('[class*="ReviewList_reviewItem__"]')).map(it => {
  const pick = frag => it.querySelector(`[class*="${frag}"]`)?.textContent.trim().replace(/\s+/g,' ');
  return {
    author: pick('ReviewList_authorName'),
    time:   pick('ReviewList_reviewTime'),
    text:   pick('ReviewList_reviewText'),
    images: it.querySelectorAll('[class*="imageWrapper"] img').length
  };
});
```

---

## 五、通用注意事项 / 反爬坑

- **登录态**：用的是用户本地已登录的 Chrome 会话，所以能拿到价格、评价等需登录内容。飞猪反爬比携程严，更依赖登录态。
- **零宽字符**：携程用户名等字段插入不可见字符干扰，统一用 `replace(/[​-‏‪-‮⁠﻿]/g,'')` 清洗。
- **「全文」截断**：长评论默认折叠，文本尾部带「全文」。需完整内容时先用 JS 点击所有展开按钮再提取。
- **去重**：轮播区 + 完整列表常有重复，按内容或唯一 id 去重。
- **canvas 内容读不出**：地图、部分图表是 canvas 绘制，DOM 里没有文字 —— 这类只能截图，但其旁边的 HTML 信息面板照常 JS 抓。
- **哈希类名优先前缀匹配**；普通类名可直接写。
- **判断是否懒加载**：先取一次数量，滚动后再取，数量变了就是懒加载。
- **价格口径**：注意「起价 / 含税 / 不含税」差异（飞猪显示不含税费）。

---

## 六、给 Skill 的提示词建议

把下面这段写进 skill 的指令，让它默认走高效路径：

```
抓取网页数据时优先用 javascript_tool 读 DOM，不要用截图认图。
流程：① navigate + wait + 1 张截图确认加载（用 browser_batch 合并）；
② 先跑一段探测脚本，统计重复出现的列表项类名，定位记录容器；
③ 对容器内部用 querySelector 批量提取成 JSON 返回。
遇到形如 Name_part__hash 的 CSS-modules 哈希类名，一律用 [class*="稳定前缀"] 包含匹配，不要写死哈希后缀。
列表若懒加载，用 JS 滚动循环触发直到数量不再增长。
清洗零宽字符，处理「全文/加载更多」展开，按内容去重。
只有 canvas 内容或确需视觉确认时才截图。
能两步以上预判的操作，用 browser_batch 合并成一次调用减少往返。
```

---

## 六点五、小红书（旅游攻略）——同方法可用，但反爬最重

同一套「JS 读 DOM」对小红书一样有效，但约束最多。**本 skill 用它做攻略佐证**：搜 `<目的地> 攻略`，抓
搜索列表的标题/作者/点赞，**跨多篇独立笔记互证**经验、并按软广规则过滤（见 SKILL.md Step 3）。

> **复验记录（2026-06-13）：** ✅ 搜索列表 `.note-item` 实测可用——`大理攻略` 取到 **20–22 条**带
> 标题/作者/点赞/图文或视频，已登录、无验证码。⚠️ **xsec_token 的 href 抓不出来**：harness 隐私防护
> 会把含 token 的 query string 拦成 `[BLOCKED: Cookie/query string data]`。所以**别去抽 token URL 再
> 导航**——要看某篇正文/评论，直接**点击该 `.note-item`** 打开浮层（token 在点击里走、不经过你），
> 再按下面浮层模板抓。笔记正文 + 评论沿用用户实测。

**搜索结果列表**（稳定类名，直接抓）
- 容器：`.note-item`（约 20–22 个/页）
- 字段：标题 `[class*="title"]`、作者 `[class*="author"] [class*="name"]`、点赞 `[class*="count"]`、
  是否视频 `[class*="play"]`

```javascript
Array.from(document.querySelectorAll('.note-item')).map(it => ({
  title:  it.querySelector('[class*="title"]')?.textContent.trim(),
  author: it.querySelector('.author .name, [class*="author"] [class*="name"], .name')?.textContent.trim(),
  likes:  it.querySelector('[class*="count"]')?.textContent.trim(),
  type:   it.querySelector('[class*="play"]') ? '视频' : '图文'
})).filter(d => d.title);
// 要读某篇 → 点击对应 .note-item 打开浮层（不要抽 xsec_token URL，会被隐私防护拦）
```

**单篇笔记正文 + 评论**（点开浮层后抓）
- **必须 scope 到浮层容器** `.note-detail-mask` / `[class*="note-detail"]`，否则会窜到背景搜索卡片
- 字段：`#detail-title` / `#detail-desc`（含 `#标签`）/ `.comment-item`

```javascript
const root = document.querySelector('.note-detail-mask, [class*="note-detail"]') || document;
const t = sel => root.querySelector(sel)?.textContent.trim().replace(/\s+/g,' ') || null;
const note = {
  title: t('#detail-title'),
  desc:  t('#detail-desc'),
  tags:  Array.from(root.querySelectorAll('#detail-desc a')).map(e=>e.textContent.trim()).filter(x=>x.startsWith('#'))
};
const comments = Array.from(root.querySelectorAll('.comment-item')).map(c => ({
  user: c.querySelector('[class*="name"]')?.textContent.trim(),
  text: c.querySelector('[class*="content"]')?.textContent.trim().replace(/\s+/g,' '),
  time: c.querySelector('[class*="date"]')?.textContent.trim()
})).filter(c => c.text);
```

**小红书五条硬约束**
1. **必须登录态**：用用户已登录的 Chrome 会话，否则撞登录墙。
2. **xsec_token 是命门、但抓不出**：裸 `.../explore/<id>` 直接导航会被拦成「当前笔记暂时无法浏览」
   （error_code=300031）；而含 token 的 href 又被 harness 隐私防护 BLOCK。**结论：点击 `.note-item` 进，
   别抽 token URL。**
3. **浮层串数据**：笔记以浮层打开时背景列表仍在 DOM → **必须 scope 到浮层容器**。
4. **别高频操作**：连续快速点击/翻页易触发滑块验证码；验证码无法自动通过 → 放慢、小批量分次跑。
5. **视频笔记**正文在视频里，文字仅能拿 desc/标签/评论；图文笔记可拿完整正文。

> 对本 skill，**搜索列表那一层(标题+点赞+作者)通常就够了**——多篇互证 + 看点赞量判断热度 + 标题里
> 鉴别软广，已能支撑攻略佐证；只有特别想要某篇细节时才点进浮层（控制频率防滑块）。

---

## 七、本次实测结果速览

| 场景 | URL 类型 | 容器选择器 | 类名类型 | 加载方式 | 实测条数 |
|---|---|---|---|---|---|
| 携程机票 | flights.ctrip.com | `.flight-box` | 普通稳定 | 虚拟滚动懒加载 | 12（滚动加载更多） |
| 飞猪机票 | sjipiao.fliggy.com | `tr.flight-item-tr` | 普通稳定 | 一次性全渲染 | 111 |
| 携程酒店点评 | hotels.ctrip.com | `[class*="reviewSwiper-item"]` | CSS-modules 哈希 | 滚动加载 | 预览若干（全部需展开弹层） |
| 高德 POI 评价 | amap.com | `[class*="ReviewList_reviewItem__"]` | CSS-modules 哈希 | 面板内 | 16 |
| 小红书搜索 | xiaohongshu.com | `.note-item` | 普通稳定 | 一页 | 20–22 |
| 小红书笔记正文 | xiaohongshu.com | `#detail-title`/`.comment-item` | id + 普通 | 浮层（点击进入） | 正文+评论 |

---

## 八、抗失效设计（selector 会过期，方法不会）

**上面那些选择器一定会过期**——哈希后缀每次发版变，前缀能扛版本号但扛不住组件重命名/重构，连
`.flight-box` 也只活到下次改版。所以**别把保存的选择器当信仰，把它当"每次自检的缓存"**。真正不变的是
**探测脚本 + 锚定内容**。耐久阶梯（从最脆到最稳）：

> 写死哈希 ＜ `[class*="前缀"]` ＜ 稳定语义类 ＜ **运行时探测发现** ＜ **锚定内容模式（¥价/HH:MM/日期/航班号）**
> ＜ **XHR/JSON 拦截** ＜ 截图认图（最稳最贵）

**核心：用户要的是数据（一个 ¥价、一个 HH:MM、一个日期），数据的形状极稳定；会变的是外面那层 CSS。
把提取锚定在内容模式上，而不是类名上。**

### 自愈四层（每次抓取都按这个顺序降级）

1. **快路 = 缓存选择器**：试第四节保存的选择器；取到 **N≥1 条合理记录**（字段非空、价格/时间格式对）就用。
2. **自愈 = 探测 + 内容锚点**：快路取 0 或字段全空 → 跑第二节探测脚本重新定位容器；定位不到就用下面的
   **内容锚定通用提取**（完全不依赖类名）→ 提取成功后**把发现的新选择器写回第四节**（碰壁即记录）。
3. **语义兜底**：仍失败 → `get_page_text` / `read_page` 拿文本/无障碍树，按**内容正则**（价格、时间、日期）解析。
4. **最后手段**：DOM 是 canvas 或全失败 → 截图认图（最稳但最贵）。

### 内容锚定通用提取（不依赖任何保存的类名——选择器全废时的兜底）

```javascript
// 例：机票行。锚点 = 同一元素里同时出现 时间 HH:MM + 价格 ¥N + 航班号 [A-Z]{2}\d{3,4}
(() => {
  const looksLikeRow = t =>
    /\d{1,2}:\d{2}/.test(t) && /¥\s*\d{2,}/.test(t) && /[A-Z]{2}\d{3,4}/.test(t);
  // 找"含一条完整记录的最小元素"：自己像一行、但没有子元素也像一行（即最内层的整行容器）
  let rows = [...document.querySelectorAll('div,li,tr')].filter(e =>
    looksLikeRow(e.textContent) && e.textContent.length < 240 &&
    ![...e.children].some(c => looksLikeRow(c.textContent)));
  const seen = new Set();
  return rows.map(e => {
    const t = e.textContent.replace(/\s+/g, ' ');
    return {
      flightNo: (t.match(/[A-Z]{2}\d{3,4}/) || [])[0],
      times:    t.match(/\d{1,2}:\d{2}/g) || [],
      price:    (t.match(/¥\s*\d[\d,]*/) || [])[0],
    };
  }).filter(r => { const k = r.flightNo + r.times[0]; return r.flightNo && !seen.has(k) && seen.add(k); });
})();
```

同理：**评论**锚点 = 含「日期 `\d{4}-\d{2}-\d{2}` + ≥10 字中文正文」的最小元素；**酒店价**锚点 = 含
`¥\d+` + 房型/「起」字样的最小元素。把锚点换成对应内容模式即可，**类名怎么改都不影响**。

### XHR/JSON 拦截（可选的"黄金耐久"路径）

这些站点多半先用 `fetch`/XHR 取 JSON 再渲染。用 `read_network_requests`（已可用）抓那条接口的响应，
直接拿结构化数据——**接口比 UI 稳得多，UI 改版了接口往往没动**。代价：端点可能要签名/带反爬，未必每站可用。
能用时它最省事也最耐久；不通就回到上面的 DOM 自愈四层。

### 维护纪律

- 第四节每个模板**标"上次复验日期"**；跑测试发现某站点取不到了，就当场重新探测、更新模板、刷新日期。
- **失效是常态，不是事故**——自愈四层保证"选择器过期"只会让这一次慢一点（多跑一段探测脚本），不会让
  数据变假：取不到就如实标「未读到 · 以官网为准」，**绝不编**（数据诚信契约照常生效）。
