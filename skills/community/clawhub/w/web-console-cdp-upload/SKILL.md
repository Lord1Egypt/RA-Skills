---
name: web-console-cdp-upload
description: 平台只有网页后台、没有上传 API 时，用本机已装的 Chrome/Edge + CDP 自动化走完上传/发布/填表流程——复用真实登录态、零安装（不下载 500MB Chromium）、能给文件选择框塞文件；并实测富文本编辑器（公众号 / CMS / 邮件模板）里到底哪些 CSS 能活下来，以及在决定是否接入平台自带的「一键排版 / AI 美化」前先抓它输出做结构化 diff。当用户说「只能网页上传」「后台发布」「网页填表自动提交」「发布到技能市场/各平台控制台」「复用已登录的浏览器」「公众号排版样式不生效/保存后样式没了」「一键排版要不要用」「点了按钮没反应/提交没成功也没报错」时使用。
category: dev-programming
subCategories: [dev-script]
platforms: [WorkBuddy, Claude Code, Codex]
license: MIT
agent_created: true
slug: web-console-cdp-upload
version: 1.3.0
displayName: 网页后台上传自动化（免安装浏览器）
---

# 网页后台上传 / 发布 / 填表自动化

## 这个技能解决什么

有些平台**只给网页入口**：没有 CLI、没有可用的 API（或 API 没 token 直接 401），
还必须带着登录态才能走完。典型如 SkillHub 发布页、各类云控制台、内容后台的上传表单。

本技能的做法：**不装任何浏览器**，直接遥控用户机器上已有的 Chrome / Edge
（用 Chrome DevTools Protocol）。对比 `agent-browser` / Playwright 方案：

| | 本技能 | agent-browser / Playwright |
|---|---|---|
| 下载体积 | 0（只依赖 `websocket-client`，几十 KB） | Chromium 约 500MB |
| 登录态 | **复用用户日常浏览器的登录态** | 全新 profile，通常要重新登录 |
| 适用 | 有头、需登录的后台操作 | 无头采集、批量自动化 |

依赖：`pip install websocket-client`（多数环境已具备）。

## 流程

### 1. 探测浏览器

```bash
python scripts/cdp.py chrome-path
```
按 Windows / macOS / Linux 依次探测 Chrome、Edge、Chromium，打印可执行文件路径；找不到输出 `NOT_FOUND`。

### 2. 带调试端口启动 —— 必须用「常驻后台任务」

**这一步最容易卡住：浏览器会随启动它的 shell 一起被回收。**

| 启动方式 | 结果 |
|---|---|
| 普通 shell 调用 + `&` | ❌ shell 退出即死，调试端口立刻不通 |
| `cmd //c start`（Git Bash） | ❌ MSYS 路径转换会把 `C:\Program Files\...` 拆坏，报 `'hrome' not recognized` |
| `Start-Process`（PowerShell） | ❌ 进程起来了但端口不监听 |
| **后台常驻任务**（Bash 工具 `run_in_background=true`） | ✅ 稳定常驻 |

```bash
"<上一步探测到的路径>" --remote-debugging-port=9222 \
  --user-data-dir="<临时目录，建议新建，别污染日常 profile>" \
  --no-first-run --no-default-browser-check "https://目标页"
```

想长期省事，可在启动参数里加 `--remote-allow-origins=*`，这样第 3 步就不必抑制 Origin。

### 3. 连通性自检（两条都要做）

```bash
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy   # 本机代理会拦 localhost
curl -s --noproxy '*' http://127.0.0.1:9222/json/version                  # 能返回即通
```

连 WebSocket 时（脚本已处理）：Chrome 新版校验握手来源，需
`websocket.create_connection(ws_url, suppress_origin=True)`，否则 `Handshake status 403 Forbidden`。

### 4. 读页面 → 判断状态

```bash
python scripts/cdp.py eval "document.body.innerText.slice(0,1500)"
```
用正文判断「是否已登录 / 列表里有没有这条 / 当前什么状态」，比截图快得多。
需要换页面时用 `CDP_MATCH` 环境变量指定 URL 片段；留空则取第一个页面标签。

**更进一步：直接读后端接口**（比读 DOM 可靠一个量级，2026-09-21 新增）。
后台页面里发同步 XHR，走浏览器自己的登录态 cookie，零额外鉴权：

```js
(function(){var x=new XMLHttpRequest();
 x.open('GET','/cgi-bin/appmsg?action=list_ex&type=77&sub=all&begin=0&count=30&token=X&lang=zh_CN&f=json&ajax=1&random=0.7',false);
 x.send(null);return x.responseText;})()
```

这一次直接看到了**服务端字段**（列表项缩略图读的是 `cover`，而它一直是空串），
2 分钟定位到「编辑器里看着有图、服务端其实没落库」。只在 DOM 里绕很容易
误判——页面上的预览节点和真正决定展示的字段可以完全无关。

⚠️ 接口名和参数是**逆向来的，别当文档**：`type=10` 拿不到图文草稿、
`type=77` 才有（本次实测），带 `random=` 的防抖参数照抄页面格式即可。
换版本先 dump 一次响应看结构，别照着记忆硬写。

### 5. 点击

先按 `textContent.trim()` 精确匹配元素再 `el.click()`：

```js
var spans=[].slice.call(document.querySelectorAll('span,button,a'));
for (var i=0;i<spans.length;i++){
  var s=spans[i];
  if((s.textContent||'').trim()!=='更新') continue;
  var box=s, hit=null;
  for(var k=0;k<5 && box;k++){ box=box.parentElement;
    if(box && (box.textContent||'').indexOf('slug: 唯一标识')>=0){ hit=box; break; } }
  if(hit){ s.click(); return 'clicked'; }
}
```
⚠️ 别用 `closest('div')` 直接找卡片——按钮常在更外层的兄弟容器里，
要**向上逐层找包含唯一标识文本的那一层**再定位。

#### 5.1 「点了没反应」的两大真凶（2026-09-21，各踩一次）

**真凶 A：可见性只看了元素自己，没看祖先链。**
框架常把按钮包在主控显示/隐藏的 `<span class="btn ...">` 里，
按钮本身的 `display` 永远是 `block` —— 于是「元素可见」判定通过，
你去点一个**父级 display:none** 的按钮，`.click()` 毫无反应且**不报错**
（症状：走完了全流程、代码全绿、结果什么都没有）。

```js
// ✅ 沿祖先链判，直到 body
function vis(e){ var n=e;
  while(n && n!==document.body){ var cs=getComputedStyle(n);
    if(cs.display==='none'||cs.visibility==='hidden') return false;
    n=n.parentElement; }
  return true; }
```
顺带：**步骤条的容器 id 不等于按钮的容器**。多步弹窗（`#step1Desc` / `#step2Desc`）
的「下一步 / 上一步 / 确定」往往全在**弹窗 footer**，三个都常驻 DOM、
靠各自父 `span` 的 display 切换。用 `#step1Desc button` 找按钮会**找不到**。

**真凶 B：框架按钮不响应合成 click。**
edui（百度 UEditor）/ weui 一类按钮只认真实鼠标事件。判据：`el.click()`
返回成功但页面状态一点没变。改用：

```python
def mouse_click(cdp, x, y):            # x/y = getBoundingClientRect 中心
    for t, b in (("mouseMoved", 0), ("mousePressed", 1), ("mouseReleased", 0)):
        cdp.send("Input.dispatchMouseEvent",
                 {"type": t, "x": x, "y": y, "button": "left",
                  "clickCount": 1, "buttons": b})
        time.sleep(0.05)
```
配套纪律：**每次点击前重新取坐标**（布局会变，尤其是分步弹窗切页后）。

**这两个真凶会叠加**：一次「上传头像」两步弹窗，A 让它点了不可见按钮、
B 让它即使可见也没反应 —— 现象都是「没有成功、没有报错、什么都没有」。
遇到这种描述，按 A → B 顺序排。

**真凶 C：按文本找按钮，却在全文档里找 —— 被正文里的同名字「抢答」。**
（2026-09-21，一次批量发布里废掉 3 篇。）

用 `querySelectorAll('a,button,span,div')` + `textContent.indexOf(按钮文字)` 找按钮时，
**搜索范围是整个文档**、判定是**包含**、取的是**DOM 顺序第一个**。只要被填的正文里
出现这两个字，正文段落就会先被命中：

```python
# ❌ 点封面的「确认」——正文里写了「外部无法确认哪个是当前值」，
#    结果点到正文段落 @y=-1345（视口外），弹窗按钮根本没点到
r = _click_visible(cdp, "a,button,span,div", "确认")
```

判据：一次「全都一样」的操作里**只有少数几条失败**，且失败的正文里恰好含按钮文字
（本例 3 篇含「确认」全废、另 27 篇零失败）。**这种"个别失败"不要当偶发重试了事。**

改法两条一起上：
1. **把范围钉死在可见弹窗里**（`dlg.querySelectorAll(...)`，按
   `getBoundingClientRect().width>300 && height>100` 挑可见弹窗）；
2. 优先级 **文本完全相等 > 包含**，且要求**是叶子节点**（`children.length===0`）、
   尺寸 ≥5px、坐标在视口内（`left/top >= 0`）。正文段落是容器、文字长，三道都过不了。

```python
def pick_dialog_button(cands, text):        # 纯函数，可单测
    usable = lambda c: (c["disp"]!="none" and c["vis"]!="hidden"
                        and c["w"]>=5 and c["h"]>=5
                        and c["left"]>=0 and c["top"]>=0)
    for exact, leaf_only in ((True,True),(True,False),(False,True),(False,False)):
        for c in cands:
            if usable(c) and ((c["t"]==text) if exact else (text in c["t"])) \
               and (not leaf_only or c["leaf"]):
                return c
    return None
```

**连带伤害要一起处理**：错点还让「编辑封面」弹窗留在页面上，紧接着的原创声明
取可见弹窗时拿到了**它**（里面没有作者输入框）→ 误报「作者框没找到」。
所以**一个错点会伪装成两个不相关的故障**。凡是「上一步失败 + 下一步也说找不到元素」
的描述，先怀疑上一步留了个没关的弹窗：失败路径上补 `close_dialog()` 收场。

#### 5.2 结果一定要用服务端真值验，别信前端信号
弹窗关闭 ≠ 成功。验证要走「重新加载页面 → 读服务端返回」，
并且**量化比对**而不是肉眼扫一眼：

```js
// 在页面上下文里同步取二进制（responseType=arraybuffer 在同步 XHR 里被禁，
// 必须走 overrideMimeType + responseText 逐字节 &0xff）
var x=new XMLHttpRequest(); x.open('GET',url,false);
x.overrideMimeType('text/plain; charset=x-user-defined'); x.send(null);
var s=x.responseText,o=''; for(var i=0;i<s.length;i++) o+=String.fromCharCode(s.charCodeAt(i)&0xff);
return btoa(o);
```
坑：**别用异步 XHR + 忙等**（`while(!done){}`）—— 阻塞主线程，`onload` 永不触发。

拿到图之后怎么比：服务端常把 PNG 转成 JPEG（零依赖 PNG 解码器用不了），
**把 JPEG 丢给浏览器** `drawImage` + `getImageData` 算统计量（暗/白/主色占比），
比自己写 JPEG 解码器省事。占比对得上（如源图 暗81.9%/白17.5% vs
服务端 暗81.2%/白16.9%）就能确认是同一张图。

### 6. 填表（React / Vue 受控组件）

直接改 `.value` 不生效，必须走原生 setter：

```js
var proto = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, v);
el.dispatchEvent(new Event('input', {bubbles: true}));
```

⚠️ **但带异步后端校验的字段（如「slug 是否可用」）光这样还不够**：
合成事件常常不触发它的防抖校验，界面会一直挂着上一次的报错（如 `Slug 不可用`、
输入框 `aria-invalid="true"`），改了值也不重算，于是提交必然失败。
必须用**真实输入事件**再补一次 blur：

```python
c.call('DOM.focus', nodeId=nid)
c.eval("var e=document.querySelector('#skill-slug'); e.focus(); e.setSelectionRange(0,e.value.length);")
c.call('Input.insertText', text='目标值')
c.eval("var e=document.querySelector('#skill-slug'); e.blur();")
# 等 5~6 秒后检查 aria-invalid 是否为 false，再提交
```

判据：提交前确认目标输入框的 `aria-invalid` 是 `false`、页面里没有残留报错文本。
「改完值但报错不消失」≠ 值真的不可用——先怀疑校验没被触发（真被占用时
重新输入后仍会报，可据此区分）。

### 7. 上传文件

```bash
python scripts/cdp.py file 'input[accept=".zip,application/zip"]' /abs/path/file.zip
```
然后补发一次 change 事件让前端解析：

```js
inp.dispatchEvent(new Event('change', {bubbles:true}));
```
解析成功的标志是界面出现「已选择 N 个文件，总大小 X KB」——**以这条为准**。

### 8. 提交与复核

点提交按钮后对话框通常自动关闭。复核要 `location.reload()` 再读列表状态
（如「安全审核中 / V 1.0.1」）。最后连 `/json/version` 的 `webSocketDebuggerUrl`
发 `Browser.close` 收尾，别留僵尸浏览器。

### 9. 富文本编辑器的样式能力：**实测，别猜**（2026-09-21 新增）

症状：往富文本编辑器（公众号、各类 CMS、邮件模板）注入 HTML 后，
样式**静默消失**——不报错、不警告，只是保存完跟没写一样。
此时最容易犯的错是「凭印象拉一份黑名单」，把一堆其实能用的属性禁掉，
于是排版只能用最土的办法凑（比如拿 `······` 点线去凑左右对齐）。

**正确做法：写一个样式探针，让平台自己回答。**

```
注入带标号的候选 HTML（V1/V2/V3…，每组长短一致便于定位）
  → 保存
  → 在**保存前**读一次编辑器内部 HTML（= 编辑器 schema 解析结果）
  → reload 后再读一次（= 服务端存储结果）
  → 逐属性判定存活，打印对照表
```

探针四个关键点（缺一个结论就是错的）：

1. **送原始 HTML，绕过自己的清洗层。** 否则你测的是自己的白名单，不是平台的。
2. **保存前 / 重载后各读一次。** 两处一致说明清洗只有一层；不一致说明服务端还洗了一遍。
3. **按属性名判定，别按字符串原样匹配。** 富文本编辑器会重建 DOM ——
   ProseMirror 会给每个文本节点包一层 `<span leaf="">`，属性顺序也会被重排。
4. **正则判定要防误报**：`height\s*:` 会命中 `line-height:`，得写 `(?<!line-)height\s*:`。
   这一条踩过，会让「进度条能不能用」的结论整个反过来。

实测出来的通用规律（微信编辑器，2026-09-21）：

| 结论 | 具体 |
|---|---|
| 布局属性**能用** | `display:flex` / `justify-content:space-between` / `float:right` / `display:inline-block` + `width` / `border-radius` / `clear` / `opacity` / `vertical-align` 全部原样保留 |
| **空元素会被剔除** | 里面没有文字的 `<span>` 整块消失（连 `width`/`background` 一起），**塞零宽字符 U+200B 也救不回** → 进度条、色块刻度这类「空盒子」方案不可行，要画刻度只能用字符（`●●●○○`） |
| 定位/装饰类确实留不住 | `position` / `transform` / `box-shadow` / `linear-gradient` / `overflow` |
| 属性值也要设白名单 | 放开 `display` 时必须拦 `display:none`（会把内容藏掉且不报错），`float` 只放 left/right/none |
| **`white-space` 会被平台覆盖** | 平台把 `white-space` 覆写成 `break-spaces`（你自己写的 `nowrap` 被吃掉）→ 任何「靠 `nowrap` 钉住宽度防压缩」的方案**一律失效**。flex 两端对齐里，长值会把标签列挤到只有一个字宽（标签竖排）。正确做法是**按内容长度分流版式**，别跟 `white-space` 较劲 |

窄屏必须单独验：编辑器常在 470px 宽下渲染，手机只有 343px。
用本地 `file://` 页面 + 固定宽度容器截图，比改浏览器窗口可靠（也要跑一次
`Emulation.setDeviceMetricsOverride` 双保险）。重点看**长内容行**会不会把定宽栏挤扁——
⚠ 给标签加 `white-space:nowrap` **救不了**（平台会覆盖它，见上表）。正解是**按内容
长度分流**：估算整行宽度（全角记 1、其余约 0.55em），超阈值就走「标签：正文」单栏
左对齐、**不套 flex**（无 flex 就无收缩）；没超才用两端对齐。判定代码要进测试。

最后一步别省：把「白名单的方向」写进测试。**放宽会静默失效，收紧会静默变丑**，
两种都不报错，只有测试能拦住。

### 10. 平台自带的「一键排版 / AI 美化」要不要纳入流程：抓输出做结构化 diff
（2026-09-21 新增）

平台后台常有「一键排版 / AI 排版 / 智能美化」这类按钮，看着像白捡的质量提升。
但它会**整篇重写样式**，而你的产物往往已经有了自己的设计。**别靠试看，靠 diff。**

这类功能通常是「异步任务 + 结果预览页」，抓链路：

```
点按钮 → 前端发请求拿到 taskid
        → 打开结果预览页 /cgi-bin/xxxstruct?taskid=...&token=...
        → 预览页本身就是一个可读的 ProseMirror（含重排后的完整正文）
        → 底部有「使用此排版 / 取消」
```

**关键：还没点「使用此排版」时，预览页里的正文就是"如果应用会变成什么样"** ——
不用真的应用就能拿到完整物料。取 `document.querySelector('.ProseMirror').innerHTML`
即为重排后正文，和改前备份做 diff 即可判断，草稿零风险。

diff 要覆盖五个维度（少一个都会误判）：

| 维度 | 怎么比 | 判读 |
|---|---|---|
| **纯文本是否一致** | 各自 `re.sub(r"<[^>]+>","",h)` 后压掉空白再比 | 一致 ⇒ 只改样式没动字（可接受的前提）；不一致 ⇒ 它**改了内容**，风险升级 |
| **自定义结构存活** | 数你自己的「指纹属性」：`display:flex` / `justify-content` / `border-radius` / 你的强调色 / `border-top` 分隔线 | 归零 ⇒ 你的自定义结构被拍平 |
| **结构标签迁移** | `Counter(</?tagname)` 比 tag 分布 | `h2→h1`、`p→section`、`strong→0` 是典型「模板接管」信号 |
| **配色是否被替换** | 提全部 `#hex` + `rgb()`，看你的强调色是否归零、新增了哪些主题色 | 主题色会覆盖你的品牌色 |
| **越界属性** | 改后样式里出现你白名单外的属性（`transform` 等） | 这些到客户端会**静默失效**，等于改后反而更差 |

再补一条「白字陷阱」检查：改后若新增 `color:#FFFFFF`，一定要确认它配的是
**实心 `background-color`**（能留）而不是 gradient/图片底（留不住 → 白底白字，字全没了）。

**结论通常是不纳入**，但一定会捡到一两条真优点（例如「给正文段落加统一
`font-size` / `line-height` / `color` 基线」）—— 把它单独搬进自己的模板，
而不是引入整个重排器。

可视对比：把改前/改后两份正文塞进同一个本地页面，**两个固定宽度列并排**
（`display:flex` + 每列 `flex:0 0 343px`），按「文本标记」切出同几个区块再截图。
用文本标记定位区块边界时，取 marker 前面最近的一个块级标签起点：

```python
def block_start(h, marker):
    i = h.find(marker); best = 0
    for tag in ("<h1","<h2","<h3","<section","<blockquote","<p ","<p>"):
        j = h.rfind(tag, 0, i)
        if j > best: best = j
    return best
```
两份正文 tag 不同（`h2` vs `h1`）也能切在同一段内容上——**按文字切，别按标签切**。

## 11. 长批次自动化：单篇隔离 + 断点续完（2026-09-21 新增）

一次要跑几十条、单条几分钟的任务（批量建草稿 / 批量上传），最大的风险不是"某一条失败"，
而是**一条失败把整批带走**。真实事故：29 条跑到第 13 条，那一条的草稿**已经成功建好**，
紧接着的操作遇上页面 WebSocket 偶发断开（`ws closed`），异常一路冒到主循环，
进程当场退出，**后面 16 条一条没发**，而且已经建好的那条**没记账**，下次重跑还会再建一遍
→ 草稿箱堆重复。

三条硬规则：

**① 每一层收尾都要"降级返回"，不许往上抛。** 主流程里"已经产生了外部副作用"的那一段
（草稿已建、文件已传），要包在 `try/except` 里，出错就返回带状态的半成品标记
（`{"status": "partial", "remote_id": ...}`），而不是抛异常。

**② 记账要逐条落盘，且带远端 id 与状态。** 只在结尾写一次的话，中途被 kill / 断电
就会出现"远端有、本地没有"的孤儿对象。记录里必须存 `remote_id` + `status`，
这是能"就地续完"的前提。

**③ 重跑时按 remote_id 就地续，别新建。** 收尾动作（声明/开关/保存）通常**幂等**
——先查一次"已经是目标状态了吗"，是就跳过。于是重跑 = 打开已有对象补完，
天然不会产生重复。

两个反复踩到的配套坑：

- **待办列表要自己重建，别复用"未处理队列"函数。** 这类函数通常会把"已记录"的整条
  剔掉，**包括半成品** → 半成品被永远当成"已完成"跳过（实测漏了一整轮）。
  待办 = 未处理的 **+ 状态为 partial 的**，顺序仍按主列表来。
- **别用 shell `timeout` 包这种命令。** 单条 4~6 分钟，随手写个 `timeout 400`
  会把它砍在"做了前一半、后一半没做"的位置，**自己又造出一个半成品**。
  要跑就丢后台 + 写日志文件，跑完再读日志。

顺手把连接层也加固：CDP 客户端记住当前 target id，发包遇 `ConnectionError` 时
**重连同一个 target 再试一次**（页面 ws 被偶发断开很常见，重连就能继续，不必丢整条）。

## 必坑清单

1. **常驻后台启动**，否则端口永远不通（见第 2 步）。
2. **`suppress_origin=True`**，否则 WS 403。
3. **localhost 也要 bypass 代理**，否则 502。
4. **隐藏 file input 常不止一个**：文件夹那个带 `webkitdirectory`，压缩包那个带
   `accept=".zip,application/zip"`——**按 accept 挑，别按序号猜**。
5. **弹窗会重渲染**：注入文件后原 input 常被移除，`querySelector` 返回 null 不算失败，看界面文本确认。
6. **别用「对话框关了没」判成功**（2026-09-21 实测推翻本技能旧结论）：不少后台点完
   「确定」**弹窗不关也照样提交成功**，而设置区的状态行刷新是滞后的。
   唯一可靠判据是**结果量**：① 先在本页轮询状态行；② 仍不确定就点保存 → **重新加载页面
   再读状态**（只信服务端落库）。本页过程量（弹窗开/关、行文本是否立刻变）都会把成功
   误报成失败。收尾记得自己点「取消」关掉残留弹窗，否则挡住后续按钮点击。
7. **Vue/React 组件必须用真实鼠标事件**：`el.click()` 往往是「看着点上了、状态没进去」。
   用 `Input.dispatchMouseEvent` 发 `mouseMoved → mousePressed → mouseReleased`
   （先 hover 再按；部分组件只认 hover 过的元素），坐标取 `getBoundingClientRect()` 中心。
   JS click 可留作兜底，但不能当主力。
8. **预填字段 = 重复填充陷阱**：弹窗重开/回填时，框架常把已保存的值**预填**进输入框，
   此时再「选一次/打一遍字」会变成 `张三张三` 这种无效值 → 提交**静默失败**。
   正确顺序：**先读值 → 已是目标值就跳过；否则先 `Ctrl+A`+`Delete` 清空（含框架状态）
   再填**，填完断言读回值相等才点确定。
9. 若遇到站点有反爬/WAF，优先复用用户真实 profile（登录态 + 指纹），这是本方案相对无头浏览器的最大优势。
10. **别猜平台支持哪些样式**：失效是**静默**的，凭印象拉黑名单会让你长期用错误的排版
    而不自知（曾因此把能用的 flex / float / 圆角禁了半年）。先跑第 9 节的样式探针。
11. **`scrollIntoView` 和取坐标必须分两次 eval**（2026-09-21 连踩两次）：
    同一次 eval 里先 `scrollIntoView()` 紧接着 `getBoundingClientRect()`，拿到的
    是**滚动前的旧坐标** → `dispatchMouseEvent` 点在视口外 = 点空，且**不报错**。
    症状很好认：坐标停在 `y=3391` 这种远超视口高度的值。
    正确顺序：eval 滚动 → 等 0.6~0.8s 让布局稳定 → 再 eval 取坐标 → 点击。
    （另：`dispatchMouseEvent` 用视口坐标，落在视口外的元素点不到，必须先滚。）
12. **弹层菜单项用 JS click，主按钮用真实鼠标**：展开式弹层对鼠标移出很敏感，
    用坐标点菜单项常常扑空（点下去时弹层已经收了）；而菜单项多半是 `<a>`，
    内部绑的是普通 click handler，`a.click()` 反而稳。
    判断口径：`<a>` 且无复杂状态 → JS click；自定义 div / 开关 / 需要 hover 态 → 真实鼠标。
    本技能第 7 条的「必须真实鼠标」针对的是**表单控件与开关**，不针对弹层里的链接项。
13. **同一信息被拼多遍是「像机器写的」的头号特征**，而且往往不是文案问题、是模板问题
    （2026-09-21：正文里同一句价格出现 4 次，根因是渲染函数 flush 后没清空缓存列表，
    同一批表格行被连打 3 遍）。改文案前先数一遍「这件事在全文出现了几次」，
    再去看渲染代码——直觉会把你引向改措辞，但真正的病灶通常在拼接逻辑。

## 脚本接口

| 子命令 | 作用 |
|---|---|
| `chrome-path` | 探测本机浏览器可执行文件 |
| `eval "<js>"` | 页面上下文求值 |
| `shot <out.png>` | 截图 |
| `file <选择器> <路径>` | 给 `<input type=file>` 塞文件 |

环境变量：`CDP_PORT`（默认 9222）、`CDP_MATCH`（默认取第一个页面标签）。
