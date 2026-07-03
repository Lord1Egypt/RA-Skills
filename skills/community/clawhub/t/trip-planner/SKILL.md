---
name: trip-planner
description: Plan trips and build day-by-day travel itineraries, delivered as one polished, standalone HTML page. Use this skill PROACTIVELY for any travel-planning request — trigger on "帮我规划行程 / 旅游攻略 / X日游 / 安排去XX玩 / 做旅行计划 / 行程安排 / 帮我排个行程", on "plan a trip / make an itinerary / X-day trip to a city / things to do in a place", and whenever the user gives a destination plus dates or a duration (e.g. "6月去东京玩5天", "国庆想去成都4天", "trip to Kyoto next month", "下周末杭州两日游"). Always gather requirements first (never jump straight to an itinerary), research transport/weather/opening-hours via web search (query-only — it never books or pays), then output ONE self-contained HTML file with an embedded Leaflet + OpenStreetMap map, per-day timeline cards, transport-segment cards, a budget table, a pre-departure checklist, collapsible sections, hierarchical navigation, scroll-memory, and 注意/必订/避雷 callouts. Do NOT use for academic study notes (use study-notes) or generic business reports (use visual-report).
---

# Trip Planner Skill

Produces a detailed, realistic, **day-by-day travel plan** as a single polished HTML file —
geographically sensible routing, honest time budgets, verified opening hours and prices, an embedded
interactive map, and a pre-trip checklist. The visual design reuses the `study-notes` HTML output
spec (collapsible blocks, hierarchical nav, colored callouts, dark-mode theme, scroll-position
memory), retargeted to travel and documented in **`references/design-system.md`**.

**Audience assumption**: the reader is the traveler. Write so they can follow the plan on their phone
during the trip — concrete times, addresses, prices, "how to get there", and what to do if it rains.

**Environment (Windows / Claude Code).** There is **no** `places_search`, `places_map_display_v0`, or
`weather_fetch` tool here. Do research with **`web_search`**; render the map by embedding
**Leaflet + OpenStreetMap** in the output HTML (OSM tiles need no API key). For requirements
gathering use the **`AskUserQuestion`** structured-question tool if available, otherwise ask in plain
text — batched by dependency layer, each question carrying a recommended answer (see Step 1).

**Browser scraping — read the DOM with `javascript_tool`, don't screenshot-and-eyeball.** 查机票/酒店价、
携程/高德评论时，**优先用 `javascript_tool` 抓 DOM 取结构化 JSON**（省 token，且绕开高德 canvas 截图报错——
评价在 HTML 面板里，JS 抓得到）。探测脚本 + 各站点已复验选择器模板见 **`references/scraping-method.md`**；
只在确认加载/需要视觉/canvas 内容时才截图。**保存的选择器只是"自检缓存"、会过期——取到 0 条就按该文档
§八 自愈降级（探测脚本 → 锚定内容模式 ¥/HH:MM/日期 → 语义兜底），别干等、别放弃；自愈失败仍取不到，就如实
标「未读到 · 以官网为准」，绝不编。**

**Output path.** Write the final HTML to the current working directory (or a directory the user
names). Filename: `<目的地><N>日游行程.html` (e.g. `东京5日游行程.html`).

---

## 数据诚信契约（DATA INTEGRITY — 凌驾本文件一切其它规则）

**这个 skill 唯一不能破的底线：页面上每一个具体数字/事实，要么本会话真的查到了，要么就别写成具体值。
宁可不写，绝不编。** 一次编造的营业时间能把游客送到闭馆的门口，一张编造的"4.8 分 3,201 条点评（已核）"
能让整份行程的可信度归零。这条契约的违反，比任何排版/组件缺失都严重。

**浏览器优先，不是浏览器可选。** 机票、酒店（价格+评论）都是**强制要主动尝试浏览器**的项——
先去连/去查，连不上或用户跳过才退到估价。**不许因为"这趟没机票"或图省事，跳过尝试直接走 web_search 估价。**

**两类来源，泾渭分明：**

- **实查（可写具体值）**：本会话真的用浏览器（携程/飞猪/航司官网/高德）或 `web_search` 读到了，
  且**就近标了来源**——浏览器读的标「实查于 YYYY-MM-DD」/「浏览器实读点评区」/「高德实测」，
  web_search 读的标「web_search · 未浏览器核实」，火车标「以 12306 为准」。
  **注意：`web_search` 只能给价格区间和事实概要，给不了真实评论区——评论结论与评分只有浏览器读得到，
  web_search 写评论=编造。**
- **没查到（禁止写具体值）**：没读到就**不许填一个看起来合理的数**。用不含杜撰细节的 hedge 占位，
  例如「营业时间以官网为准」「评分以 App 为准」「打车费用以高德为准」「车次时刻以 12306 实时为准」。

**受控『已验证』词表——只有真查到才能用：**
`已核 / 已核实 / 可信 / 实测 / 实测数据 / 浏览器实读 / 浏览器实查 / 高德实测 / 分布正常 / 不像刷分 /
好评集中在X / 口碑稳 / 活跃真实`。这些词**只有当本会话确实读到对应内容、且同一处带了来源+日期标记**时
才允许出现。**同一张卡/同一段里，价格标了「未核实/估价」，就绝不能在别处出现这些词**——那是自相矛盾，
是最恶劣的"伪装成已核实"。也不要用同义词（口碑扎实/水分不大/可放心订/评分稳）绕开——**任何关于评论区
的结论性判断，没有就近来源标记，一律不写。**

**按面分项的硬规矩（每一面都管，不只是酒店）：**

| 数据 | 实查到 → 可写 | 没查到 → 只能写 |
|---|---|---|
| 酒店评分/点评数 | 具体分+条数+「实查于 日期」 | 留空，或「评分以 App 为准」（**禁止**任何分数/条数） |
| 评论体检结论 | 读到的真实复发主题+来源标记 | 只写"为什么选它/订前自查"这类连锁常识推荐理由 |
| 酒店/机票比价 | 现役平台（携程/飞猪/官网）真实价 | 现役平台估价并标「（估）」；**已废平台（去哪儿/美团/同程/艺龙）禁止出现**；估价行不得打「✓最低」 |
| 门票¥/营业时间/地址 | 实查值 | 就近标「以官网为准」（**禁止**编逐项联票价并做"单买超¥X"的派生算术） |
| 车次号/分钟级时刻/票价 | 实查值+「以12306为准」 | 不写具体车次号与到发分钟，只写「高铁直达约 Nh · 班次票价以12306实时为准」 |
| 预约配额/放号时刻 | 实查值 | 「名额有限 · 配额与放号以官方公众号当日为准」（**禁止**编"每日2000人/8:00放号"） |
| 打车¥/分钟/里程 | 高德路线规划值+「（高德实测）」 | 「打车可达 · 费用时长以高德为准」（短步行腿 ≤2km 可按 70–80 m/min 估距离+步行 min，但一旦出现¥或"打车"就必须高德来源；**禁止**"步行或打车 N min"这种混写偷渡打车分钟） |
| 步数 | 由实测里程换算（≈1,300 步/km） | 不标具体步数 |
| 天气（>14 天外） | —— | 「X月气候典型 约A°/B°（非当日预报，出行前再查）」，**不得对多日复制同一具体温度串当各日预报** |
| 地图坐标 | 知名点的已知坐标 | 定位不到就降到城区级并注明近似，**禁止**给定位不到的点编 4 位小数精确坐标 |
| 预算派生 | 各项来自上面的实查/估价 | 不得把编造的单价滚成"精确"日小计/总计；header 总价与预算表必须一致 |

**逃生门（"你直接安排就行"）只放宽提问，不放宽这条契约**：缺的偏好按推荐值填、写进顶部假设 callout；
但任何**事实**仍然遵守上表——没查到就 hedge，绝不因为是非交互模式就开始编数字。

`scripts/check_html.py` 的第 8–10 检查是这条契约的**兜底**（抓最常见的编造：无凭据的酒店评分/评论结论、
假"最低"比价、复制粘贴的假天气）。但校验器只是结构兜底、挡不住刻意绕过——**真正的防线是你自己守住"宁可
不写绝不编"**。

---

## Run it as a workflow (plan → research → verify → assemble)

Don't free-write a plan in one pass. The quality comes from the structure:

1. **Plan** — gather requirements (Step 1), then sketch the day count, geographic clusters, and which
   stops need booking. Nothing is researched yet; this is the skeleton.
2. **Research (fan-out)** — for each day/cluster, look up transport, weather, opening hours, closure
   days, and prices with `web_search` (Steps 2–3). For a big trip you may run parallel subagents, one
   per day or per city.
3. **Verify (the decisive step)** — enforce the **数据诚信契约 above**: every specific number/fact is
   either actually verified this session (with a source marker) or written as a hedge that carries **no
   invented specifics** — never a plausible-looking number. This applies to **every surface**, not just
   hotels: 票价/营业时间/地址/车次/时刻/船票/打车费/里程/步数/预约配额/坐标/天气. Re-check that no stop
   is scheduled on its closing day and that intercity connections leave realistic buffers.
4. **Assemble** — build the HTML per `references/design-system.md`, then run the checker
   (`scripts/check_html.py`).

The six steps below are mandatory and **in order**. Do not skip Step 1.

---

## Step 1 — 需求采集（GRILL，问透为止 — never skip, never jump straight to an itinerary）

**This is the most common failure mode: producing a generic itinerary before knowing who's traveling
and what they want. Don't.** 需求采集采用 **grill 式访谈**（方法源自 [grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md)）：
**沿着决策树把每一个分支问到底，直到没有任何一项需求是靠猜的**。四条铁律：

1. **问透为止，不设问题数上限。** 下面清单里的每一项，要么用户答了，要么用户明确同意用推荐值——
   没有第三种状态。一轮 3–4 问、按依赖顺序分多轮（用 `AskUserQuestion`，没有就纯文本编号提问），
   问完一层再问下一层，直到清单清零。
2. **每问必附推荐答案。** 每个问题给出你基于已知信息的推荐选项和一句理由（放在选项第一位），
   用户嫌烦可以整轮"都按推荐"。
3. **能查的绝不问。** 凡是 web_search/浏览器能查到的（天气、闭馆日、签证政策、有没有直达高铁），
   自己查；只问存在于用户脑子里的事（偏好、约束、已订了什么）。
4. **先读 prompt，绝不重问已知。** 开场先把用户已给的信息抽出来打勾，只 grill 缺口。

### 需求决策树（按依赖顺序分层 grill）

**第 1 层 · 骨架（决定一切的硬事实）**
- **目的地 + 出发地**（精确到城市/机场）
- **日期 / 天数**（精确日期；驱动天气、节庆、闭馆、票价）
- **大交通是否已订？** 已订 → 拿到具体班次/车次时刻，行程以它为锚，Step 2 只做接驳；
  未订 → Step 2 全流程实查比价
- **城际出行方式偏好** — 飞机 / 高铁 / 自驾 / 不限（价格 vs 时间怎么权衡；红眼/早班能不能接受）
- **时间硬约束** — 出发日最早几点能出门？返程当天必须几点前到家？行程中间有无固定事项（会议/探亲/复诊）
- **证件** — 身份证/护照在不在有效期？出境/港澳台需要的签证签注办了吗（政策本身自己查，证件状态问用户）

**第 2 层 · 人和钱（决定行程形态）**
- **同行构成** — 人数；亲子（孩子年龄）/ 银发（体力、无障碍）/ 情侣 / 朋友 / 独行 / 商务+休闲
- **健康与体力** — 每天能走多少步？爬山/楼梯行不行？需不需要午休？晕车船/高反史？常用药？
- **预算口径** — 总预算还是人均/天？机酒大头含不含在内？有没有不能破的硬上限？
- **节奏** — 暴走 / 适中 / 悠闲（每天少而精）
- **兴趣偏好** — 自然 / 历史人文 / 美食 / 购物 / 艺术展馆 / 夜生活 / 亲子乐园 / 摄影出片
- **必去 / 避雷清单** — 点名要去的，和明确不想要的类型

**第 3 层 · 落地细节（决定每张卡片怎么填）**
- **住宿** — 已订（给地址）还是待选？几间房、什么床型？品牌偏好/忌讳？要不要含早？位置偏好
  （市中心 / 枢纽旁 / 景区附近）
- **市内交通方式** — 地铁公交 / 打车 / 自驾租车 / 步行为主
- **行李** — 有无托运需求（廉航是否适配）？婴儿车 / 轮椅？
- **餐饮** — 忌口、过敏、清真/素食？辣度接受度？有没有必吃清单？
- **天气与弹性** — 雨天还出门吗？高温耐受？行程有变数吗（要不要退改弹性/保险提醒）？

**第 4 层 · 收口**
- 最后一问固定是：**「还有什么硬要求是我没问到的？」** 答"没有"才算 grill 结束。
- 结束后**回读一遍完整需求清单**（含所有推荐值的采纳情况）让用户确认，再进 Step 2。

Escape hatch：用户说"你直接安排就行 / just decide for me"时不再追问，全部缺口按推荐值填——但
**整张假设清单必须原样写进 HTML 顶部的 info callout**（已有机制），并在回复里提醒"按这些假设排的，
不符再说"。

---

## Step 2 — 机票 / 火车票查询（只查询，不下单）

Fit the itinerary to real arrival/departure times — but **only read, never book.**

1. **First pass — `web_search`.** Find candidate 班次/航班 (times, duration, rough price range,
   train/flight number). Examples: "上海 到 成都 航班 时刻", "北京 西安 高铁 时刻表 票价". Capture 2–3
   candidates. For **trains**, a fare/区间 from web_search or 12306 is enough — stop here (12306 is the
   single source of truth; use a browser only if you need live 余票/具体车次).
2. **Flights — browser price check is MANDATORY (机票必须用浏览器查一遍).** A flight fare moves too much
   for a web_search number to be trusted, so for **every air leg** you must open the booking sites in a
   browser — **Claude in Chrome / Windows-MCP / Desktop Commander**, whichever is connected — and read
   the **live** fare for the chosen flight/date on **several** platforms: **携程 / 飞猪 / 航司官网（必查：
   东航/国航/南航等实测可查，官网有券时更低）**（去哪儿/美团/同程/艺龙已废，别浪费时间——平台真值表见
   `references/research-playbook.md`）。International: add **Google Flights / Skyscanner** (no login).
   **国内机票全平台列表价均为裸价——无一例外，航司官网也是**（个别官网页面标着「含税总价」，订单页实测
   仍另加机建+燃油，别被页头骗了）。预算必须用**含税总价 = 裸价 + 机建费 + 燃油附加费**；燃油费率随油价
   频繁调价，先 web_search 最新标准再折算并注明执行日期；要看真实税费可进订单第一步的价格明细页（只读，
   绝不提交）。读不到就标「票面价 · 燃油/机建另计，以出票页为准」，不许编税费。 Put those real, same-session prices + the exact query time into the `.price-compare` block,
   cheapest tagged. This is **query-only** — obey the prohibitions below.
   - **At a login wall / captcha — defer it, don't block; batch all logins into ONE prompt.** You never
     enter passwords or solve captchas yourself. When a platform throws a login/captcha wall, **don't
     stop and wait there.** Instead: read whatever shows *without* logging in (e.g. a price-calendar
     lowest), leave that tab open and **navigate it to its login page** so it's ready for the user, add
     it to a **"needs-login" list**, and **move on** — open and read every other platform (incl.
     login-free ones like Google Flights) first. **Only after all platforms are queried**, if the
     needs-login list is non-empty, ask the user **once**, listing them, e.g.: *"这几个要登录才能看完整价：
     飞猪、某航司官网。我已把每个标签页都停在登录页了——请你一次性全部登录（我不会替你输密码或过验证码），都登好
     告诉我，我再回去逐个读价。"* **Wait** for one confirmation, then go back and **read the now-accessible
     fares on each** previously-walled tab. (Batching beats pausing per-platform — the user logs in once,
     not N times.)
   - **Fall back per-platform as a last resort** — no browser connected, or the user skips / can't log
     into a given site. For just those, use web_search ranges and **label them** "web_search 估价 · 未浏览器
     核实，请在购票平台确认". Never present an estimate as a browser-verified price; keep the platforms you
     *did* read live as the real comparison.
3. **Hard prohibitions — what YOU never do (the user may do these manually):**
   - ❌ **You** never log in or type passwords. (If login helps, the **user** logs in manually, then you
     resume reading — see the login-wall step above.)
   - ❌ **You** never read, solve, or bypass CAPTCHAs / 验证码 / 滑块. (The user clears it themselves.)
   - ❌ Never place an order, reserve, or pay — booking is always the user's, not yours.
4. **Integrate the chosen transport into the plan:**
   - The arrival time anchors **Day 1** (don't schedule a 9 AM museum if the flight lands at 13:00).
   - The departure time caps the **last day** (leave time to get to the airport/station + check-in).
   - Between cities, leave a generous **赶车 / 赶飞机 buffer** (airport: arrive ~2–3h before
     international / ~1.5h domestic; train: ~30–45 min at a big station).
   - Put each leg in a **transport-segment card** (times, price range, booking link) — see the design
     system. The link is for the user to book; the skill never books.

More detail and copy-paste search patterns: **`references/research-playbook.md`**.

---

## Step 3 — 天气 + 真实数据

- **Weather**: `web_search` the destination + travel dates — typical seasonal weather and, if the dates
  are within ~10–14 days, the forecast. This drives clothing notes, the energy curve, and rain Plan B.
- **Season-specific facts**: festivals/events on those dates, peak-season crowds, **closure days**
  (many museums close Mondays; some attractions close for holidays), and ticketing windows
  (timed-entry, sells-out-early).
- **Per-place facts — verify, never fabricate**: opening hours, closing day, address, and ticket price
  for every attraction and recommended restaurant. If a fact can't be confirmed, mark it
  "以官网为准" rather than inventing it. Wrong hours that send the traveler to a closed door are the
  worst failure this skill can produce.
- **小红书攻略 — 每趟都搜一遍，不是可选项（用户反复要求，且产物里经常被漏掉）。** 至少跑一次
  `web_search "<目的地> 攻略 小红书"` / `"<目的地> <主题/人群> 避雷 小红书"`，捞本地玩法、出片机位、
  排队/避坑、亲子或银发实操。**但必须鉴别软广**：通篇只夸、出现「合作/赞助/探店/团购券/到店报暗号」、
  统一话术配统一滤镜、引导私信下单的当广告打折；**只采被多篇独立笔记重复印证的具体经验**（如"X点后不排队"），
  单篇热帖不作准，硬事实（票价/时间）仍以官网为准。把采到的写进相关 POI 的 `poi-tip` 或 `tip` callout。
  详见 `references/research-playbook.md` §1 的鉴别清单。

---

## Step 4 — 行程编排逻辑（核心）

This is what separates a real plan from a list of famous places. Apply all of it:

- **地理聚类**: group each day's stops by proximity so the route is a smooth line, not zig-zag
  backtracking. One neighborhood/area per half-day where possible. The embedded map makes bad routing
  obvious — use it as a check.
- **时间预算**: for each stop budget **停留时长 + 点间通勤 + 缓冲**. Be honest about transit time between
  points. Aim for **2–4 主要点 per day** — fewer for 悠闲/银发/亲子, more only for 暴走. Don't cram.
- **点间通勤 + 步数 (标在卡片上)**: between consecutive stops, state the **commute** (mode + distance +
  time, e.g. `🚶 600 m · 步行 8 min` or `🚇 3 站 · 12 min`) as a **transit connector**, and it must match
  the day's route on the map. Sum each day's walking into a **步数估算** (≈ 1,300 步/km) shown in the
  day's overview line. Keep walking legs short for 银发/亲子 and call it out.
  **跨片区/打车腿的里程·时长·过路费必须真的去高德路线规划跑一遍**（浏览器已连时这是强制动作，标「（高德
  实测）」；不是写个「以高德为准」就算完——那只是连不上浏览器时的退路）。纯步行短腿（≤2km）可按 70–80
  m/min 估，但出现打车¥或分钟就必须有高德来源。
- **餐饮卡位**: place 午餐 / 晚餐 at a spot that's **on the route** at the right time, near the stop
  you'll be at — not a detour across town.
- **硬约束**:
  - Skip any stop on its **closing day**; reorder days to fit.
  - Use **日出 / 日落** times for viewpoints, photo spots, night views.
  - Flag every stop that needs **advance booking / 预约 / timed ticket** with a `must` callout and a
    checklist item.
- **体力曲线**: keep the **arrival day** and **departure day** light; put the most demanding day in the
  middle. Don't schedule a dawn hike the morning after a red-eye.
- **天气备选 (Plan B)**: for outdoor-heavy days, give an **indoor alternative** (museum, mall, aquarium,
  café district) in a `weather` callout, so rain doesn't wreck the day.

Deeper heuristics (time-budget rules of thumb, clustering, multi-city pacing):
**`references/research-playbook.md`**.

---

## Step 5 — 住宿备选（选酒店：看评论、偏连锁、多平台比价）

**This step is NOT optional, and it is the one most often silently dropped.** The final HTML must
contain a 住宿备选 section with **at least 3 `.hotel` cards in every plan** — including when the user
never mentioned hotels, and including non-interactive / "你直接安排就行" runs (pick the area from the
itinerary's geographic clusters and state your assumption, e.g. "按 市中心+近地铁 选了3家，已订可忽略").
The **only** exception: the user explicitly says accommodation is already settled (已订酒店 / 住朋友家 /
公司安排). Then replace the section with a single **已订住宿 card** (their hotel's name/address if given,
map pin, transit from it to each day's first stop) and add `data-hotels="user-booked"` on that section
so the checker knows the omission is deliberate. `check_html.py` fails the build if neither is present.

Give the user **at least 3 hotel options (备选), not one** — placed near the itinerary's geographic
clusters / transit and matching their 住宿位置偏好 from Step 1.

**浏览器核实对酒店是强制项，和机票同级——必须主动去连、去查，不是"有机票才连浏览器"。**
（这是真实翻车点：一次纯火车的行程里，agent 以为"机票才是 skill 强制要浏览器的那项"，于是**压根没去连
Chrome**，酒店直接走了 web_search 估价。错。）只要本行程要选酒店（非"已订"），你就**必须主动尝试启动/连接
浏览器**（Claude in Chrome / Windows-MCP / Desktop Commander，哪个连着用哪个），对**价格和评论都**实查——
和 Step 2 机票一字不差的纪律。**有没有机票，与酒店要不要连浏览器，毫无关系。**

- **价格**：浏览器读现役平台（携程/飞猪）实时价。只有在**真的尝试过、确认没有浏览器可用**（没连上 / 用户
  跳过）时，才退到 web_search 区间，并标「web_search 估价 · 未浏览器核实」。**默认就走估价、不去连浏览器 = 违规。**
- **评论**：评论**只能**靠浏览器（携程/高德点评区）——`web_search` 给不了真实评论区，硬写就是编造。
  没浏览器读到评论时，遵守**数据诚信契约**：`.h-rating` 写「评分以 App 为准」（不写任何分数/条数），
  `.review-check` 只写连锁常识推荐理由，**绝不写"可信/已核/分布正常/好评集中在X"这类结论**。
- A missing browser never justifies skipping the section; it only downgrades prices to labeled estimates
  and strips the review verdict — **it never licenses a web_search「估价」shortcut that skips the attempt,
  nor a fabricated rating.**

Selecting a hotel is otherwise the same discipline as flights: **research, don't trust the listing;
compare prices across platforms; read the actual review section; never book.**

- **Read the reviews, NOT the marketing blurb (硬性要求).** A pretty listing and a high headline score
  mean nothing on their own. Open the actual **review section** (大众点评 / 携程 / 去哪儿 / 小红书 /
  Google / Booking) and **read recent and negative reviews**, then judge whether the review area looks
  **normal**:
  - **Healthy signs:** a large review count, **recent** activity (reviews in the last weeks), specific
    praise (mentions 隔音/早餐/前台/床), and a believable mix — **100% 5★ is a red flag, not a green one.**
  - **Avoid / warn (recurring serious complaints):** 卫生差 / 有虫 / 隔音差 / 不安全 / 偷换房型 / 强制消费 /
    前台态度 / 与图片不符. If the same serious complaint repeats across recent reviews → drop it.
  - **Fake-review tells:** a burst of identical, generic, dateless 5★; a score wildly out of line with
    the written complaints; or all reviews old/stale. Treat these as untrustworthy.
  - **评论必须双信源：携程 + 高德，缺一不可。** 单一平台不够可信——携程好评偏光鲜、运营痕迹重，高德 POI
    评价更接近真实住客口碑。流程：携程筛「4.7 分以上」找候选连锁、读携程评论 → **同一家再去高德读一遍**
    （`amap.com/search?query={城市}{酒店名}` → 点搜索按钮 → 点 POI →「评价」）→ 交叉比对，**携程光鲜但
    高德有复发吐槽（旧/吵/窗户/卫生），信高德**。`.review-check` 写清两边各自说了什么。
- **Prefer chains (连锁) when they fit — especially for 银发/亲子** (consistent cleanliness, standards,
  easy recourse): **华住会** (汉庭/全季/桔子/星程/宜必思/美居), **锦江** (锦江之星/7天/维也纳), **首旅如家**
  (如家/和颐). But a chain is **not an auto-pick** — a specific branch with bad recent reviews is still
  out; **reviews override the brand.** A boutique/民宿 is fine if its reviews are strong, specific, and
  authentic and it suits the trip — just flag the higher variance.
- **价格和评论是两套独立的多源要求，都要做——别混为一谈（真实翻车点）。** 一次运行里 agent 把"评论双信源
  携程+高德"当成了"查两家就完事"，于是**只碰了携程和高德，把飞猪价格比价整个丢了**。记牢这张表，三个平台
  都要碰：

  | 维度 | 必查平台 | 为什么不能互替 |
  |---|---|---|
  | **价格比价**（`.price-compare`） | **携程 + 飞猪**（国际加 Booking/Agoda） | 高德**没有房价**，不能当价格源 |
  | **评论核验**（`.review-check`） | **携程 + 高德** | 飞猪评论不顶替高德；高德 POI 口碑更真 |

  → 一张合格的酒店卡 = **携程（价+评）+ 飞猪（价）+ 高德（评）三次浏览器读**。查了携程+高德 ≠ 完成，飞猪价格
  仍要查；只有飞猪真的连不上/验证码墙/未读到，才在那一行如实标「飞猪 · 验证码墙未读」并退到 web_search 估价
  （标「估」），**绝不是默认不查飞猪**。`check_html.py` 会 FAIL 任何「飞猪只写了"订前自己比"却没真查」的酒店卡。
  - **一个源失败，绝不连累另一个（真实翻车点）。** 一次运行里高德评论没加载出来，agent 就写「高德/飞猪我没
    核到」——把价格源飞猪和评论源高德捆在一起一起放弃了。**高德（评论源）失败，与飞猪（价格源）该不该查，
    毫无关系**；反之亦然。一个挂了就单独如实标它挂了，另一个照查。
  - **高德评论是懒加载——别太早下"没评价"的结论。** 点开 POI 后 wait 3–5s、必要时在详情面板内下滚一下再读；
    搜索若默认跳了北京＝没解析到城市，把城市名加进 query 重搜+点搜索按钮。「高德没返回评价」十有八九是没等够。
- **别默认「集团 App 会员价更低」**——实测未必，且华住会官网查不到价；会员价只有真读到才写。**Use the same
  defer-and-batch login handling and the query-only prohibitions from Step 2** (never log in / solve
  captchas yourself, never book). Trains/flights/hotels all share that flow.
- **Output** each option as a **hotel card** (chain badge, 评分 + 点评数, 区域/到地铁/到当天景点群的距离, a
  short **评论体检** note saying what reviews actually say, the multi-platform `.price-compare`, and a
  booking link). Pin the top pick on the map. Mark a 推荐 vs 次选/备选 if helpful. See
  `references/design-system.md` (hotel card) and `references/research-playbook.md` (vetting method).

---

## Step 6 — 输出（沿用 study-notes 的 HTML 规范，按旅行场景改造）

**Read `references/design-system.md` and follow it exactly.** Build ONE standalone HTML file
containing:

- **Themed hero header** (required, on every trip): a gradient banner keyed to the trip's subject
  (`theme-night/ocean/sunset/forest/city/sakura/snow/desert`, optional `deco-stars`/`deco-glow`, or a
  custom gradient from the destination's palette), with the headline facts wrapped as translucent
  `.tag` pills (3–6: 天数 / 核心体验 / 预算档 / 节奏 / 人数). Use `.chip` pills elsewhere to wrap short
  item lists (必吃、亮点、随手鸟点). See "Themed hero header" in the design system.
- **Embedded Leaflet map** (`#map` + the `TRIP` data object) showing each day's stops as numbered
  pins and the day's route as a colored dashed line. Every stop needs `lat`/`lng` (look them up;
  district-level is an acceptable fallback). OSM tiles, no key.
- **Per-day timeline**: one `.sec-COLOR` section per day, opening with a **daily overview line**
  (`.day-meta`: 当日花费 + 步数 + 主要点数). Each stop is a **POI card** showing 名称 / 到达时间 / 停留时长 /
  票价 / 营业时间 + a one-line `poi-tip`, with a collapsible `<details>` for "如何前往 / 周边吃喝". Between
  consecutive cards put a **transit connector** (`.transit`: 步行/地铁/打车 + 距离 + 时间) = the route to
  the next point.
- **Transport-segment cards**: 航班 / 车次, times, price range, booking link. **For flights, include a
  `.price-compare` multi-platform comparison** (去哪儿/携程/飞猪/官网…, cheapest tagged).
- **住宿备选 section** (`.hotel` cards, ≥3 options): chain badge, 评分 + 点评数, 区域/距离, a **评论体检**
  note (what the reviews actually say — not the listing blurb), a multi-platform per-night `.price-compare`,
  and a booking link. Prefer chains; reviews override the brand. Pin the top pick on the map.
- **Budget table** (`.budget`) with **per-day subtotals** (fixed 大项 grouped, then one block per day,
  each day's subtotal = that day's 当日花费 chip) and a grand `.total` row + **pre-departure checklist**
  (`.checklist`, persists ticks in localStorage) covering 订票 / 证件 / 预约 / 必带物.
- **Kept mechanisms**: collapsible sections, hierarchical TOC + floating sub-heading navigator,
  scroll-position memory, dark-mode theme. **Callouts** carry travel meaning:
  `must` = 必订/必约, `warn` = 注意/赶车/闭馆, `avoid` = 避雷, `tip` = 省钱省时, `weather` = 雨天 Plan B,
  `info` = 须知.

### Build + check (before presenting)

After assembling the HTML, run the static checker and fix anything it flags:

```bash
python3 scripts/check_html.py <output>.html
# or on Windows: py scripts\check_html.py <output>.html
```

It verifies `<div>` balance, that the Leaflet CDN + `#map` + a non-empty `TRIP` object are present,
that every map stop has numeric coordinates, that no leftover KaTeX `$$…$$` math slipped in from
the template's study-notes lineage, and that the **travel components actually landed**: ≥3 `.hotel`
cards (or the explicit `data-hotels="user-booked"` marker), a `.budget` table, and the
localStorage-backed `.checklist`. Re-run until clean, then tell the user where the file is.

---

## Output spec summary (the retargeted規范, for quick reference)

The full spec is in `references/design-system.md`. In brief, what changed from study-notes:

| study-notes | trip-planner |
|---|---|
| KaTeX math, `.fbox`/`.big-formula`, math macros, error banner | **removed** |
| (no map) | **Leaflet + OSM map** with per-day numbered pins + route polylines |
| concept section per topic | **day section** per travel day (`.sec-COLOR` cycled by day) |
| worked-example cards | **POI cards** (time / 停留 / 票价 / 营业时间 / tip + collapsible details) |
| — | **transport cards**, **budget table**, **localStorage checklist** |
| callouts: note/tip/warn/exam/mistake/intuition | callouts: **info/tip/warn/must/avoid/weather** |
| collapse, hierarchical TOC+nav, scroll memory, dark mode | **kept verbatim** |

---

## Test prompts

After building the skill, try these (they exercise requirements-gathering, English input, and the
train-query path):

1. **`下个月中旬带爸妈去成都玩4天,从上海出发,预算中等,想看大熊猫、吃地道川菜,老人家走不动太多路,节奏悠闲点,帮我做个行程。`**
   — 银发亲子 + most info given; should confirm only the few missing bits, then plan light-paced days
   with low-walking routing and an indoor Plan B.

2. **`Plan a 5-day Tokyo itinerary for the two of us in early July, flying from Shanghai. We love food and anime (Akihabara), want one day-trip outside the city, mid-range budget, and don't mind a packed schedule.`**
   — English, couple, fast pace; should fit flights to Day 1 / Day 5, cluster by district, and map it.

3. **`9月23到26号去西安,兵马俑、城墙、回民街都想去,顺便帮我看下从北京出发的高铁大概几点有车、大概多少钱。`**
   — destination + dates + a transport-query ask; should still gather missing prefs (同行/预算/节奏),
   `web_search` the 北京→西安 高铁 options into a transport card (query-only), and avoid any closure-day
   clashes.
