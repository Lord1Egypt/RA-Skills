---
name: webclaw3
slug: webclaw3
displayName: 浏览器自动化 · Browser Automation · 用你自己的 Chrome 登录态
version: 1.0.5
summary: 浏览器自动化 / 网页数据采集：让 AI 直接用你已登录的 Chrome 搜索、抓数据、填表单、发内容，跑通一次即可提炼成零 token、可定时运行的本地 skill。
license: MIT
github: https://github.com/fatmind/webclaw3
description: 浏览器自动化 / 网页数据采集 / 爬虫抓取——用你自己的 Chrome 和已登录状态干活，不用重新登录、不用交账号密码、不怕反爬。搜东西、看网页、抓列表、导表格、下载内容、点按钮、填表单、发内容都能干；必须登录才能看的页面（xhs、抖音、微博、推特(X)、知乎、B站、公众号、淘宝、拼多多、Shopify 后台等）也能抓。跑通一次即可提炼成零 token、可定时自动运行的本地 skill，网站改版也能本地修。当用户提出任何需要操作浏览器或抓取网页数据的联网任务时使用。
---

# webclaw3 — 浏览器自动化 · 用你自己的 Chrome 登录态

> 让 AI 用你**已经登录**的 Chrome 干活：搜索、抓数据、点按钮、发内容都行。跑通一次后说一句"帮我提炼"，它就变成零 token、每天能自动跑的本地 skill。

**能干什么（三个真实例子）**

- 「把xhs搜索『显瘦连衣裙』前 50 条笔记的标题、点赞数、作者导成表格」——需要登录才能看的页面照样抓。
- 「每天早上 8 点把 SkillHub 下载热榜前 10 拉下来发我」——提炼成 skill 之后定时跑，零 token、毫秒级返回。
- 「打开我的 Shopify 后台，把昨天的订单整理成日报」——直接操作你已登录的后台，账号密码不用交给任何人。

**装起来要几步（先说清楚，别踩坑）**：三步、大约 5 分钟。① 装 Chrome 扩展（开发者模式加载一次）；② 到 [webclaw3.com](https://webclaw3.com) 领 Access Key（免费 10 次生成额度）；③ 对你的 Agent 说一句"帮我装 webclaw3 并检查环境"。装完就在对话框里说人话使唤它。

**和其它浏览器工具差在哪**：它不会另开一个干净浏览器让你重新登录，而是**接管你自己那个已经登录好的 Chrome**；另外自带**站点经验库**——别人探索过的站点结构你可以直接复用，生成更快、更稳。

---

> 以上是给人看的介绍。**Agent 从下面这一节开始读。**

## 四环节总览（先读这个）

webclaw3 覆盖「探索 → 提炼 → 日常跑 → 修复」完整动线，四个环节：

| 环节 | 什么时候进入 | 指引在哪 |
|---|---|---|
| ① 安装启动 | 首次使用，或前置检查不通过 | Read `references/setup.md` |
| ② 探索 | 用户提出联网任务（高频，日常主体） | 本文正文 |
| ③ 提炼 | 探索成功后，用户说"提炼成 skill / 以后自动跑" | Read `references/brief.md` |
| ④ 问题修复 | 之前生成的 skill 运行失败 | Read `references/repair.md` |

用户动线：装好通道（①）→ 自然语言探索、拿到用户确认满意的结果（②）→ 一句"帮我提炼"变成可反复跑的 skill（③）→ skill 日常运行，出问题先本地修（④）。

①③④ 低频，对应文件遇到场景时再 Read，不要提前加载。`references/` 目录与本文件同级。

> **和用户说话，永远用大白话（贯穿全程，极重要）**
> 把用户当成一个不懂技术的普通人，不是程序员。无论转达 doctor 的建议、报错、还是进度，都要翻译成简短、口语化的人话，告诉他"下一步点哪、做什么"就够了。**不要**把原始 JSON、日志路径、端口号、tarball / npm / PATH 这类术语甩给用户。一次只说重点，能一句话讲清就别写三句。（文末还有一条同样的提醒。）

## 前置检查

本 skill 的 CLI 就在 skill 目录的 `scripts/` 下，用 node 直接跑——**不需要也不要做任何 PATH / npm link / 全局安装**，也不要向用户提议。下文所有 `webclaw3 <子命令>` 写法均指：

```bash
node <本 skill 目录>/scripts/webclaw3.mjs <子命令>
```

skill 安装完成后、以及每次开始联网操作前，**直接跑下面这条，不用询问用户要不要检查**：

```bash
node <本 skill 目录>/scripts/webclaw3.mjs doctor
# → {"ok":true,...} 即可开始操作
```

doctor 会自动拉起 relay；`ok:false` 时输出里有 advice（Chrome 没开 / 扩展未装 / 被禁用等），需要引导用户人工处理的场景 Read `references/setup.md`。

> 本 skill 的脚本（relay、cdp-proxy、webclaw3 CLI）全部在 skill 目录的 `scripts/` 下，自包含；Chrome 扩展是独立安装的 wc3-chrome（安装方式见 `references/setup.md`）。

## 浏览哲学

**像人一样思考，兼顾高效与适应性的完成任务。**

执行任务时不会过度依赖固有印象所规划的步骤，而是带着目标进入，边看边判断，遇到阻碍就解决，发现内容不够就深入——全程围绕「我要达成什么」做决策。这个 skill 的所有行为都应遵循这个逻辑。

**① 拿到请求** — 先明确用户要做什么，定义成功标准：什么算完成了？需要获取什么信息、执行什么操作、达到什么结果？这是后续所有判断的锚点。

**② 选择起点** — 根据任务性质、平台特征、达成条件，选一个最可能直达的方式作为第一步去验证。一次成功当然最好；不成功则在③中调整。比如，需要操作页面、需要登录态、已知静态方式不可达的平台（xhs、微信公众号等）→ 直接用浏览器中继

**③ 过程校验** — 每一步的结果都是证据，不只是成功或失败的二元信号。用结果对照①的成功标准，更新你对目标的判断：路径在推进吗？结果的整体面貌（质量、相关度、量级）是否指向目标可达？发现方向错了立即调整，不在同一个方式上反复重试——搜索没命中不等于"还没找对方法"，也可能是"目标不存在"；API 报错、页面缺少预期元素、重试无改善，都是在告诉你该重新评估方向。遇到弹窗、登录墙等障碍，判断它是否真的挡住了目标：挡住了就处理，没挡住就绕过——内容可能已在页面 DOM 中，交互只是展示手段。

**条件不可达时重新评估，不死磕：** 当严格筛选条件下数据量确实不足（如"近一周+点赞>500"只有 3 条，目标要求 >=10），这不是技术问题而是数据现实。此时应主动向用户说明实际情况，并建议放宽条件（扩大时间范围、降低阈值），而不是在同一条件下反复翻页、换入口死磕。用户的验收标准是可以协商的，数据的客观存在量不是。

**④ 完成判断** — 对照定义的任务成功标准，确认任务完成后才停止，但也不要过度操作，不为了"完整"而浪费代价。

## 联网工具选择

- **确保信息的真实性，一手信息优于二手信息**：搜索引擎和聚合平台是信息发现入口。当多次搜索尝试后没有质的改进时，升级到更根本的获取方式：定位一手来源（官网、官方平台、原始页面）。

| 场景 | 工具 |
|------|------|
| 搜索摘要或关键词结果，发现信息来源 | **WebSearch** |
| URL 已知，需要从页面定向提取特定信息 | **WebFetch**（拉取网页内容，由模型直接提取，返回结果） |
| URL 已知，需要原始 HTML 源码（meta、JSON-LD 等结构化字段） | **curl** |
| 非公开内容，或已知静态层无效的平台（xhs、微信公众号等公开内容也被反爬限制） | **浏览器**（wc3-chrome 中继，跳过静态层） |
| 需要登录态、交互操作，或需要像人一样在浏览器内自由导航探索 | **浏览器**（wc3-chrome 中继） |

浏览器中继不要求 URL 已知——可从任意入口出发，通过页面内搜索、点击、跳转等方式找到目标内容。WebSearch、WebFetch、curl 均不处理登录态。

> WebSearch / WebFetch 指宿主自带的搜索、网页读取工具。

### 信息核实：定位一手来源

核实的目标是**一手来源**，而非更多的二手报道。多个媒体引用同一个错误会造成循环印证假象。

搜索引擎和聚合平台是**定位**信息的工具，不可用于直接**证明**真伪。找到来源后，直接访问读取原文。同一原则适用于工具能力/用法的调研——官方文档是一手来源，不确定时先查文档或源码，不猜测。

| 信息类型 | 一手来源 |
|----------|---------|
| 政策/法规 | 发布机构官网 |
| 企业公告 | 公司官方新闻页 |
| 学术声明 | 原始论文/机构官网 |
| 工具能力/用法 | 官方文档、源码 |

**找不到官网时**：权威媒体的原创报道（非转载）可作为次级依据，但需向用户说明："未找到官方原文，以下核实来自[媒体名]报道，存在转述误差可能。"单一来源时同样向用户声明。

## 浏览器通道与 API

通过 Chrome 扩展走 WebSocket 中继到用户日常 Chrome，天然携带登录态，零授权弹窗，反检测隐身。

### Relay API

通过 HTTP REST API 与 Relay 服务器交互（Relay 是已运行的 WebSocket 服务器，监听 ws://127.0.0.1:3459，同时暴露 HTTP 端口）：

```bash
# 检查状态
curl -s http://127.0.0.1:3459/api/status
# → {"extensionConnected":true,"wsPort":3459}

# 通用调用格式：POST /api/call，body 为 JSON { "op": "操作名", "params": {...} }
# 返回格式：{ "result": ... } 成功，{ "error": "..." } 失败

# 【硬性要求】任何浏览器操作（tab.create / page.* / site.*）之前，必须先 group.create 建本任务分组，
# 并把返回的 groupId 带到后续所有 tab.create 与 page.* 调用，任务结束 group.close 整组关闭。
# 不建组的 tab 会混进共享默认组，与其他并行任务互相干扰。唯一例外：用户明确说不用分组。
# 记不住 groupId 时用 group.list 按组名找回（组名用任务主题命名）。详见「多任务隔离」一节。

# --- Tab 操作 ---
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.list"}'
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.list","params":{"groupId":GROUP_ID}}'   # 只看某个任务组，隔离多任务
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.create","params":{"url":"https://example.com","active":false}}'
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.create","params":{"url":"https://example.com","active":false,"groupId":GROUP_ID}}'   # 建进指定任务组
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.setStatus","params":{"tabId":TAB_ID,"status":"running"}}'
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.groupInfo"}'
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.groupInfo","params":{"groupId":GROUP_ID}}'
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.close","params":{"tabId":TAB_ID}}'

# --- 任务分组（多任务隔离：每个任务一个分组）---
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"group.create","params":{"name":"skillhub-trending"}}'   # → {"groupId":...}
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"group.list"}'
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"group.setStatus","params":{"groupId":GROUP_ID,"status":"running"}}'
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"group.close","params":{"groupId":GROUP_ID}}'   # 关闭该组所有 tab

# --- 页面操作 ---
# 动态 eval（核心，任意 JS 字符串）。page.* 都可带可选 groupId 做归属校验，防止误操作到别的任务的 tab
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.eval","params":{"tabId":TAB_ID,"code":"document.title","groupId":GROUP_ID}}'

# Aria tree（DOM 遍历，ref_N 寻址）
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.ariaTree","params":{"tabId":TAB_ID,"filter":"interactive"}}'

# 点击/滚动/填表（通过 ref_N 定位元素，React 安全）
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.click","params":{"tabId":TAB_ID,"ref":"ref_3"}}'
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.scrollTo","params":{"tabId":TAB_ID,"ref":"ref_5"}}'
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.fillForm","params":{"tabId":TAB_ID,"ref":"ref_2","value":"搜索内容"}}'

# 关键词搜索页面元素
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.search","params":{"tabId":TAB_ID,"query":"关键词"}}'

# 等待元素出现
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.waitForElement","params":{"tabId":TAB_ID,"selector":".item-card"}}'

# 截图
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.screenshot","params":{"tabId":TAB_ID}}'

# 提取页面正文
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.getText","params":{"tabId":TAB_ID}}'

# 解除调试附加
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"debug.detach","params":{"tabId":TAB_ID}}'
```

Node.js 脚本中用 fetch 封装：

```javascript
const RELAY_URL = 'http://127.0.0.1:3459';

async function relayCall(op, params = {}, timeout = 30000) {
  const res = await fetch(`${RELAY_URL}/api/call`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ op, params, timeout }),
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error);
  return data.result;
}
```

### 上下文集成变量（调用方声明时生效）

调用方可能在上文 `## 上下文变量` 里声明以下变量，从声明取值；未声明则忽略。

- **WC3_OPERATION_LOG**：operation_log 文件绝对路径。声明后，每个浏览器 API 调用都要带上 logFile 参数写入该文件：
  - Extension Relay：POST body 顶层加 `"logFile":"<声明的值>"`
    ```bash
    curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.create","params":{"url":"https://example.com"},"logFile":"<声明的值>"}'
    ```
  - CDP HTTP 兜底：URL query 加 `?logFile=<声明的值>`（示例见 `references/cdp-fallback.md`）
  - 两个通道都会自动追加到同一文件；每条记录含 op / params / result / timestamp / channel / duration_ms。

（站点知识由下文 `## 站点知识` 节 + 声明的 `WC3_SITE_KNOWLEDGE` 覆盖，不在本节重复。）

### 错误处理

- 扩展未加载 → `/api/status` 返回 `extensionConnected: false`，跑 `webclaw3 doctor` 按 advice 引导用户（详见 `references/setup.md`）
- 扩展被禁用/Service Worker 挂掉 → 第一次 op 返回错误，提示用户检查 `chrome://extensions/`
- `page.eval` 抛错 → 直接拿到 JS 异常信息（含 className、message、stack），修复脚本重试

### CDP 兜底通道

默认只用 Extension Relay。仅当 Extension 通道**整体**走不通（扩展未连、Service Worker 挂掉、eval 持续失败）时，回退 CDP HTTP 通道（`:3456`）继续操作——此时 Read `references/cdp-fallback.md`（启动、tab 映射、API、回退判定）。单次 `SyntaxError`、`tab not found` 属脚本问题，不回退。

## 页面理解与数据提取

**`ariaTree` 和 `page.eval` 组合使用**，是理解和提取页面的两个核心能力：

- **Aria 树做地图**：`page.ariaTree` 返回页面的压缩语义结构（role + name，~500 行 vs 原始 DOM ~10000 行）。进入新页面先看一次全貌——有哪些区域、多少数据项、分页结构、可交互元素，一次调用建立页面心智模型。**用于理解页面结构和定位交互元素，不用于提取结构化数据。**
- **eval 做采矿**：`page.eval` 执行任意 JS，**是提取结构化数据的首选方式**——直接从 DOM 返回 JSON（name/href/price/downloads 等），保留完整属性，不受文本布局影响。同时覆盖 Aria 树触达不了的一切——穿透 SPA 框架数据层、操控 DOM 元素、执行复杂交互逻辑。

大多数任务都是 Aria 先看全貌、eval 再提取数据，两者交替推进。**先了解页面结构，再决定下一步动作**，不需要提前规划所有步骤。

### Aria 树的格式与边界

**`ariaTree` 返回格式：**
```
[ref_1] heading "精选 TOP 50 AI Skills 榜单"
[ref_2] list (options=8)
  [ref_3] listitem "Web Access ⭐ 1.4k ↓ 5.2k"
  [ref_4] listitem "DeepSearch ⭐ 892 ↓ 3.1k"
[ref_13] button "下一页"
[ref_14] textbox "搜索"
```

每个节点有 `[ref_N]` 编号，可用于 `page.click(tabId, 'ref_N')` 和 `page.fillForm(tabId, 'ref_N', value)` 精确操作。

**Aria 的边界——什么时候该切 eval：**
- Aria 树只有可见文本的语义摘要，不含 URL、隐藏属性、组件内部数据
- 动态弹出的面板（筛选、下拉菜单、模态框）可能不在 Aria 树中，click 会定位失败
- 展示文本（"31.7万"）和精确值（317000）不同，精确值要从数据层拿

### 数据提取策略（page.eval 优先）

**page.eval 是结构化数据提取的首选方式。** 扩展已通过 declarativeNetRequest 移除页面 CSP 头，page.eval 在绝大多数站点上可正常使用，正常情况下无需兜底到 CDP。直接从 DOM 提取结构化 JSON，不经过纯文本中间层——这样能保留 href、data-* 属性等 DOM 信息，且不受文本布局变化影响。（例外：若 Extension 通道整体不可用/持续失败，按 `references/cdp-fallback.md` 临时走 CDP 摸清页面结构，再切回 Relay。）

`page.eval(code)` 在用户真实 Chrome 中执行任意 JS，用前记牢它的关键约束：

- **支持任意 JS**：表达式、语句、async/await、throw、IIFE 都可以
- **绕过 CSP**：即使页面有 `unsafe-eval` 禁用也能跑
- **返回 JSON 可序列化值**：函数、DOM 节点、循环引用会失败
- **副作用在页面真实世界生效**（点击、表单提交、滚动、导航）

| 层级 | 方法 | 适用场景 |
|------|------|----------|
| L1 | `page.eval` + CSS selector | **首选**——直接从 DOM 提取结构化数据（name/href/price 等），返回 JSON |
| L2 | `page.ariaTree` 直读 | 只需看全貌、确认数据项数量/结构，或信息在可见文本中已足够 |
| L3 | `page.eval` + 穿透框架数据层 | SPA 没有语义化 class，需要从 React fiber、Vue data、全局 store 等拿原始数据对象 |
| L4 | 交互触发（`page.click`、翻页、滚动加载） | 数据需要交互才能出现 |

L3 补充：很多 React/Vue SPA 的 class 是哈希值，DOM 层面无法可靠定位。React 的 `__reactFiber$` → `memoizedProps` 链路、Vue 的 `__vue__.$data`、以及 `window.__NEXT_DATA__` / `window.__INITIAL_STATE__` 等全局变量，都是穿透到原始数据的入口。具体怎么遍历需要根据目标页面的实际结构探索。

**媒体资源**：判断内容在图片里时，用 `page.eval` 从 DOM 直接拿图片 URL，再定向读取——比全页截图精准得多。

### 渐进式提取工作流

面对陌生页面，提取分四步推进——先侦察、再定位、后取值、最后才决定要不要加工：

```
getText 侦察          page.eval 定位           textContent 取值         后处理决策
──────────────── → ──────────────────── → ──────────────────── → ────────────────────
拿整页纯文本          根据侦察结论              拿 DOM 节点原值          判断原值够不够用
理解页面结构          用 eval + DOM 位置定位     保留原始 textContent     ├─ 够用 → 直接输出
找到数据在哪里        锁定目标节点               不做提前格式化            ├─ 需要拆 → split
哪些字段可取                                                            ├─ 需要匹配 → regex
                                                                      └─ 需要理解 → LLM 总结
```

1. **getText 是合法的侦察手段**——面对陌生页面，`page.getText` 拿整页纯文本是最自然的"看一眼"方式，用来理解页面结构、确认数据在哪、有哪些字段可取。**但侦察 ≠ 提取**：侦察清楚后，真正取数据必须切到 `page.eval` 从 DOM 拿结构化 JSON。绝不要用 getText 拿纯文本再正则解析来提取结构化数据——那样丢失了所有 DOM 属性（href、class、data-*），只能靠文本布局匹配，极脆弱。
2. **textContent 原值优先**——`page.eval` 里先拿到原始字符串（如 `"99.7 万"`、`"43"`），再决定要不要进一步处理。不要在提取时就预设格式做转换。
3. **后处理是分层决策**——原值够用就直接输出；需要拆分用 `split`/`trim`；需要模式匹配才上 `regex`；需要"理解"内容（判断、归类、总结）才交给 LLM。不是所有场景都需要 regex。

> 边界提醒：这套工作流描述的是**人工浏览/交互过程**的推进方式。getText 侦察只发生在浏览探查期；**沉淀进可复用提取脚本的代码里只能有 page.eval**，不要把侦察用的 getText 调用抄进脚本。

### 技术事实

- 页面中存在大量已加载但未展示的内容——轮播中非当前帧的图片、折叠区块的文字、懒加载占位元素等，它们存在于 DOM 中但对用户不可见。以数据结构（容器、属性、节点关系）为单位思考，可以直接触达这些内容。
- DOM 中存在选择器不可跨越的边界（Shadow DOM 的 `shadowRoot`、iframe 的 `contentDocument`等）。eval 递归遍历可一次穿透所有层级，返回带标签的结构化内容，适合快速了解未知页面的完整结构。
- `page.eval` 执行滚动到底部会触发懒加载，使未进入视口的图片完成加载。提取图片 URL 前若未滚动，部分图片可能尚未加载。
- 拿到媒体资源 URL 后，公开资源可直接下载到本地后用读取；需要登录态才可获取的资源才需要在浏览器内 navigate + screenshot。
- 短时间内密集打开大量页面（如批量 `tab.create`）可能触发网站的反爬风控。串行逐个处理是最安全的；如需并行，控制在 2-3 个 tab，避免短时间爆发。
- 平台返回的"内容不存在""页面不见了"等提示不一定反映真实状态，也可能是访问方式的问题（如 URL 缺失必要参数、触发反爬）而非内容本身的问题。
- 某些平台的 ID 中编码了时间戳（如xhs note_id 前 8 位是 Unix 时间的十六进制）。当页面不直接展示时间字段时，可尝试从 ID 解码，避免逐个进详情页。
- 现代 Web 应用的输入框很多不是普通 `<textarea>`，而是基于 contenteditable 的富文本编辑器（Twitter/X 的 Draft.js、Notion 的 ProseMirror、Google Docs 等）。这类编辑器有自己的事件系统和内部状态树，直接操作 DOM（如 `textContent` 赋值）会破坏框架状态，导致：输入不被识别、字数统计不更新、提交按钮不激活。面对 contenteditable 输入框，需要通过编辑器能感知的事件方式输入（如逐字符键盘事件），而非直接操作 DOM 文本。

## 页面交互与导航

**交互定位层级：**
- 优先：`page.click` + aria tree ref_N 语义定位，稳定抗改版
- 降级：`page.eval` + CSS selector 定位
- 兜底：`page.eval` 内通过文本内容匹配目标元素后 click——特别适用于 aria tree 找不到的动态面板、模态框内按钮

### 程序化操作与 GUI 交互

浏览器内操作页面有两种方式：

- **程序化方式**（构造 URL 直接导航、eval 操作 DOM）：成功时速度快、精确，但对网站来说不是正常用户行为，更容易触发反爬机制。
- **GUI 交互**（点击按钮、填写输入框、滚动浏览）：GUI 是为人设计的，网站不会限制正常的 UI 操作，确定性最高，但步骤多、速度慢。

根据对目标平台的了解来判断。当程序化方式受阻时，GUI 交互是可靠的兜底。

**站点内 URL 的可靠性**：站点自己生成的链接（DOM 中的 href）天然携带平台所需的完整上下文（含会话相关参数如 token），而手动构造的 URL 可能缺失隐式必要参数，导致被拦截、返回错误页面、甚至触发反爬。提取 URL 时保留完整地址，不要裁剪或省略参数；当构造的 URL 出现异常时，应考虑是否是缺失参数所致。

**页面内打开链接的两种方式**：

- **`page.click`**：在当前 tab 内直接点击，简单直接，串行处理。适合需要在同一页面内连续操作的场景，如点击展开、翻页、进入详情等。
- **`tab.create` + 完整 URL**：从 DOM 提取对象链接的完整地址（包含所有查询参数），在新 tab 中打开。适合需要同时访问多个页面的场景。

### 输入与时序要点

- 写值到 React/Vue 受控组件时，必须用 prototype value setter + InputEvent，**不能直接 `el.value = ...`**：
  ```javascript
  const proto = HTMLInputElement.prototype;
  const desc = Object.getOwnPropertyDescriptor(proto, 'value');
  desc.set.call(el, text);
  el.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: text }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
  ```
- 创建 tab 后 sleep 2-3 秒等加载；切 tab 后 sleep 1-1.5 秒等列表渲染
- 同一时间所有 tab 共享一个扩展连接（first-connection-wins），并发任务需自己排队

### 操作要点

- **关键操作后截图验证**：执行提交、发布、发送等操作后，用 `page.screenshot` 确认操作真正完成了。不要仅从 DOM 状态推断成功——页面上的圆形元素可能是字数统计器而非加载动画，按钮旁的指示器可能是静态 UI 而非操作反馈。同一个名字的按钮在不同上下文含义不同（如 Twitter 的 "Reply" 既是打开回复框的入口，也是提交回复的按钮）。**当操作看起来"卡住"或"没反应"时，先截图看清页面真实状态再判断下一步**，不要在错误假设上继续操作。
- **先 inspect 再写 selector**：面对陌生页面，先用 eval 取一小块 DOM 片段（innerHTML / outerHTML），看清真实的标签嵌套和 class 命名，再写选择器。不要凭想象猜——尤其是 SPA，class 很可能是哈希值或无语义名。
- **弹窗/模态框内操作要限定作用域**：页面上和弹窗里可能存在同名按钮（如都叫"确认"）。在弹窗内操作时，先定位弹窗容器，再在容器内查找目标元素。不加限定 → 可能点到页面上的同名按钮，弹窗没响应，看起来像"点击失效"。
- **多页数据在浏览器内存中累积，最后一次性导出**：翻页抓取时，不要每页都把 JSON 传回 shell——特殊字符（引号、换行、中文）会导致 shell 变量解析失败、数据丢失。正确做法：在浏览器内用全局变量（如 `window.__collected`）累积，全部采集完再一次性 `JSON.stringify` 导出。**避免通过 shell 变量中转大段 JSON。**

## 站点知识

站点知识文件（`{site}.md`）记录了某站点已验证的选择器、URL 模式、页面行为经验，是探索陌生站点时的重要参考。

**来源**：站点知识来自上文声明的 `WC3_SITE_KNOWLEDGE`（声明中已给出可用的站点知识文件清单，文件名即站点关键词，如 `1688.md`、`reddit.md`）。**按当前目标 URL 的域名匹配**对应文件后 Read；匹配不到就不读，不要凭任务描述猜站点。

**使用原则**：
- **历史经验可能过时**——选择器会随站点改版失效，URL 模式可能变化。站点知识是"起点提示"而非"绝对真相"，以实际页面为准；失败时自行 inspect DOM 重新定位
- URL 模式里的查询参数（如 `&type=link&t=month`）直接带进 URL，不要手动点 UI 设过滤器
- 发现新的有效选择器/API/陷阱时，值得回写站点知识（若当前流程允许）

**子 Agent 传递规则（极其重要）**：
子 Agent 运行在 skill 工作目录，**该目录下没有站点知识文件**。若要子 Agent 使用站点知识，必须在子 Agent 的 prompt 中**原文嵌入 Read 指令**，指向站点知识的**绝对路径**（不要改成工作目录、不要改路径）：

> 开始前先 Read `{绝对路径}/{site}.md` 获取站点选择器、URL 模式和页面行为经验。

## 登录判断

用户日常 Chrome 天然携带登录态，大多数常用网站已登录。

登录判断的核心问题只有一个：**目标内容拿到了吗？**

打开页面后先尝试获取目标内容。只有当确认**目标内容无法获取**且判断登录能解决时，才告知用户：
> "当前页面在未登录状态下无法获取[具体内容]，请在你的 Chrome 中登录 [网站名]，完成后告诉我继续。"

登录完成后无需重启任何东西，直接刷新页面继续。

## 多任务隔离：每个任务一个 Tab 分组

多个任务同时跑（主 Agent + 并行子 Agent、多个 skill 同时运行）共享同一个 Chrome 和 relay 时，**每个任务必须开自己的 Tab 分组**，从结构上隔离，避免 tabId 漂移导致误操作。

**为什么**：如果所有任务共用一组 tab，`tab.list` 会返回所有任务的 tab，两个任务访问同一站点（URL 撞车）时按 URL/标题匹配就会选错 tab，对别人的页面做点击/填表/发帖。

**做法（任务开始 → 结束 一套完整动作）**：

```bash
# ① 任务开始：开一个自己的分组，拿到 GROUP_ID
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"group.create","params":{"name":"<任务名，如 skill 名或调研主题>"}}'
# → {"groupId": 123, ...}

# ② 任务中：所有 tab.create 都带自己的 groupId
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.create","params":{"url":"https://...","active":false,"groupId":123}}'

# ③ 列举只限自己组（不会选到别的任务的 tab）
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"tab.list","params":{"groupId":123}}'

# ④ 关键操作（page.*）带 groupId 做归属校验，误传别的组直接报错而不是打错页面
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"page.click","params":{"tabId":TAB_ID,"ref":"ref_3","groupId":123}}'

# ⑤ 任务结束：整组关闭，不残留 tab
curl -s -X POST http://127.0.0.1:3459/api/call -d '{"op":"group.close","params":{"groupId":123}}'
```

要点：
- **`group.create` 每次都是全新分组**（隔离优先），调用方持有 `groupId` 并传给后续操作。
- 任务名用 skill 名或任务主题（如 `skillhub-trending`、子 Agent 的调研主题），标签栏上按任务折叠收纳，用户一眼分清。
- 组状态用 `group.setStatus({groupId, status})` 标记 running/completed/idle（比逐 tab 的 `tab.setStatus` 更适合多 tab 任务）。
- **`group.create` 建组是任务开始的第一步，不是可选项**（唯一例外：用户明确说不用分组）。不传 `groupId` 进默认 `wc3` 组仅是为旧 skill 保留的兼容行为，新任务禁止依赖它。

## 并行调研：子 Agent 分治策略

任务包含多个**独立**调研目标时（如同时调研 N 个项目、N 个来源），鼓励合理分治给子 Agent 并行执行，而非主 Agent 串行处理。

**好处：**
- **速度**：多子 Agent 并行，总耗时约等于单个子任务时长
- **上下文保护**：抓取内容不进入主 Agent 上下文，主 Agent 只接收摘要，节省 token

**并行操作**：每个子 Agent 在当前用户浏览器实例中，**先 `group.create` 开一个属于自己的任务分组**，然后自行创建所需的后台 tab（`tab.create` 带上自己的 `groupId`），自行操作，任务结束**自行 `group.close` 整组关闭**。所有子 Agent 共享一个 Chrome、一个 Relay，各自关在自己的分组里，`tab.list({groupId})` 只看到自己的 tab——即使两个子 Agent 访问同一站点也不会选错 tab、误操作到对方。

**子 Agent Prompt 写法：目标导向，而非步骤指令**
- 必须在子 Agent prompt 中写 `必须加载 webclaw3 skill 并遵循指引` ，子 Agent 会自动加载 skill，无需在 prompt 中复制 skill 内容或指定路径。（注意：这里说的是 **skill 本体**无需路径；若子 Agent 要用**站点知识文件**，则需按下方 `## 站点知识` 节用绝对路径传入，二者不冲突。）
- 子 Agent 有自主判断能力。主 Agent 的职责是说清楚**要什么**，仅在必要与确信时限定**怎么做**。过度指定步骤会剥夺子 Agent 的判断空间，反而引入主 Agent 的假设错误。**避免 prompt 用词对子 Agent 行为的暗示**：「搜索xx」会把子 Agent 锚定到 WebSearch，而实际上有些反爬站点需要浏览器中继直接访问主站才能有效获取内容。主 Agent 写 prompt 时应描述目标（「获取」「调研」「了解」），避免用暗示具体手段的动词（「搜索」「抓取」「爬取」）。
- **超时约束（必写）**：每个子 Agent 的 prompt 中必须包含以下健壮性约束，防止某个环节（如 IM 联系人无法匹配）无限重试拖到全局超时：
  > **超时限制：本任务最多执行 10 分钟。如果某个操作连续失败 5 次，立即停止尝试，记录失败原因并返回已收集到的部分结果。不要死磕。**

**分治判断标准：**

| 适合分治 | 不适合分治 |
|----------|-----------|
| 目标相互独立，结果互不依赖 | 目标有依赖关系，下一个需要上一个的结果 |
| 每个子任务量足够大（多页抓取、多轮搜索） | 简单单页查询，分治开销大于收益 |
| 需要浏览器长时间运行的任务 | 几次 WebSearch / Jina 就能完成的轻量查询 |

## 任务结束

任务若开了自己的分组，用 `group.close({groupId})` 整组关闭（组内所有 tab 一起关）；没开分组的场景用 `tab.close` 关闭自己创建的 tab。必须保留用户原有的 tab 不受影响。

Relay 持续运行，不建议主动停止——重启后需要等扩展重新连接。

---

> **最后再强调一遍：和用户说话用大白话。**
> 用户是不懂技术的普通人。任何时候要把技术输出（doctor 结果、报错、日志、端口）翻译成简短的人话，只告诉他下一步该做什么；别把原始 JSON、日志路径、端口号、npm / PATH 这类术语丢给他。
