# Research Playbook & Itinerary Logic (deep dive)

Companion to `SKILL.md`. Read this when researching transport/weather/places and when sequencing a
day. The golden rule throughout: **only state facts you actually found; never fabricate hours, prices,
addresses, or schedules.** A confidently wrong opening time is worse than an honest "以官网为准".

---

## 1. Web search patterns (the fast default)

Run focused searches and read 2–3 sources before asserting a fact. Useful query shapes:

**Transport (查询，不下单):**
- `"<出发地> 到 <目的地> 高铁 时刻表 票价"` · `"<出发地> <目的地> 火车 二等座 多少钱"`
- `"<from> to <to> flights <month> price"` · `"<航司> <航线> 直飞 时长"`
- airport ↔ city: `"<机场> 到 市区 怎么走 时间 价格"` (机场快线/大巴/打车)

**Flights — MANDATORY browser price check (机票必须用浏览器实查多平台).** web_search prices for flights
are stale/indicative; for every air leg you must read **live** fares in a browser. Procedure:

1. **First pass (web_search):** identify the target flight(s) — date, flight number, rough range.
2. **Browser pass (required):** with whichever browser tool is connected — **Claude in Chrome**,
   **Windows-MCP**, or **Desktop Commander** — open each platform's results page for that flight/date
   and **read** the fare:
   - 国内（**2026-06 实测平台真值表，省时间，别去碰已废的**）:
     - ✅ **携程** (`flights.ctrip.com` / `hotels.ctrip.com`) — 机票酒店免登录可读，台面价为裸价。
     - ✅ **飞猪** — 机票/酒店 web 均可用（需淘宝登录态；连续查询可能触发验证码 → 走登录墙协议）。
       机票 URL **必须带全参数**，缺 `depDate`/城市三字码会报「入参校验失败」——别误判成已废；模板见下方 URL 模板库。
       列表价均为**裸价**（机票表头自标「不含税费」）。
     - ✅ **航司官网**（**必查**，东航/国航/南航实测可查价，吉祥/春秋等多数也可）— 价值在于：会显示 OTA
       未售的独家班次、有券时可能更低、改签直连。**官网列表价同样是裸价**——吉祥官网页头标「含税票价总价」
       但订单页实测仍另加机建+燃油 ¥200/段，别被页头骗了。
     - ✅ **高德地图** — 查不了酒店价格，但 **POI 评价真实可靠**（可作酒店评论信源），且路线规划给出
       **打车费/时长估算**（市内交通数字必须从这里来，不许拍脑袋）。
     - ❌ 已废，不要再查：**去哪儿**（机票+酒店桌面端均已下线）、**美团**（web 403）、**同程/艺龙**（基本残废）、
       **华住会官网**（查不到价）。
   - 国际: **Google Flights**、**Skyscanner**、航司官网 — these need no login, so prefer them and they
     rarely hit a wall.

   **燃油附加费 + 机场建设费（国内机票绝不可漏，且必须现查）：** 国内**全平台列表价均为裸价，无一例外**
   ——OTA、航司官网都不含燃油附加费与机建费（实测吉祥官网订单页：票面 ¥1,150 + 机建燃油 ¥200 = 总计 ¥1,350，
   尽管其列表页头标着「含税总价」）。预算表必须用**含税总价 = 裸价 + 机建费 + 燃油附加费**。折算时，
   **燃油附加费随油价频繁调价（一年多次），绝不许用记忆值** — 先 `web_search "国内 燃油附加费 最新 调整"`
   拿当前标准再算（例：2026-06-05 起 >800km ¥150/段、≤800km ¥80/段，机建费 ¥50/段——仅作记录，下次仍要现查），
   并在页面上注明「按 YYYY-MM-DD 起执行标准」；真实税费也可在订单第一步的价格明细页核对（只读不提交）。
   查不到就标「票面价 · 燃油/机建另计，以出票页为准」，**绝不能自己编一个税费数**。

   **URL 模板库（实测可用 · 直接套用，省点击省 token；坏了就更新这里）：**
   | 平台/用途 | 模板 | 实测注意（碰过的壁） |
   |---|---|---|
   | 携程机票（单程列表） | `https://flights.ctrip.com/online/list/oneway-{出发IATA小写}-{到达IATA小写}?_=1&depdate=YYYY-MM-DD&cabin=Y_S_C_F` | **用户实测的稳定格式**：`?_=1&` 缓存破坏 + `cabin=Y_S_C_F`（全舱）。例：广州→三亚 `oneway-can-syx?_=1&depdate=2026-10-14&cabin=Y_S_C_F`。旧写法 `?depdate=...&cabin=y_s` 常渲染不出、得手动点，**别再用** |
   | 携程酒店（城市列表+日期） | `https://hotels.ctrip.com/hotels/list?city={城市数字id}&checkin=YYYY/MM/DD&checkout=YYYY/MM/DD` | **city id 用错会静默返回「找到0家」**（曾把厦门错填 18→0 家）。常见 id：北京1·上海2·厦门25·成都28·杭州17·广州32·深圳30·西安10；**不确定就先在框里输城市名让它解析**。**keyword 参数不过滤**——酒店名一律在页内搜索框输入 |
   | 飞猪机票（单程列表） | `https://sjipiao.fliggy.com/flight_search_result.htm?tripType=0&depCity={dep3字码}&arrCity={arr3字码}&depDate=YYYY-MM-DD&depCityName={中文}&arrCityName={中文}` | 缺 depDate/三字码报「入参校验失败」（≠已废） |
   | 飞猪酒店（关键词+日期） | `https://hotel.fliggy.com/hotel_list3.htm?cityName={中文城市}&checkIn=YYYY-MM-DD&checkOut=YYYY-MM-DD&keywords={酒店名}` | 连续查可能触发验证码墙 |
   | 吉祥官网（航班查询） | `https://www.juneyaoair.com/flightQuery?depCity={中文}-{3字码}&arrCity={中文}-{3字码}&depDate=YYYY-MM-DD&routeType=OW` | 其余航司官网结构各异，首次 UI 搜索后**记下结果页 URL 进表** |
   | 高德 POI 搜索（看评价/坐标） | `https://www.amap.com/search?query={城市名}{POI名}` | **城市塞进 query，别用 `&city=中文`（不过滤）**；**导航后 URL 不自动执行，必须点搜索按钮(放大镜)才出结果**，之后它自动把 city 解析成 adcode（如厦门350200）。**点 POI 后评价区是懒加载——必须 wait 3–5s 再读，常需在详情面板内向下滚一下；「没返回评价」十有八九是没等够，不是真没有（实测三亚喜来登有 1.5万 评价）。若搜索默认跳了北京 = 没解析到城市，把城市名加进 query 重搜+点按钮。** |
   | 高德路线（起终点要 UI 选点） | 搜起点 POI → 点「路线」→ 改终点 → 切驾车/公交 | 结果含驾车里程/时长/过路费、公交方案+票价；无打车价，用里程×当地计价标准折算并注明来源 |

   **碰壁即记录（用户硬性要求）：** 任何一次"直接 navigate 没出结果、得手动点击/改参数才成"的情况，
   **当场把真正可用的 URL 格式或操作序列回填到上表的「实测注意」列**——目标是让"直接输 URL 就能用"的状态
   尽量保持。下次同平台直接套，不再重复踩同一个坑、不再重复点击流程（省 token）。
3. Record each `platform → price` **with the exact query time**, put them in `.price-compare` (cheapest
   tagged `class="cheapest"`), and set `.tr-price` to "最低 ¥X".

**Login walls — defer and BATCH (don't pause per-platform):**
- *You* never enter passwords, never read/solve/bypass a captcha/验证码, never click 下单/支付.
- When a platform hits a **login/captcha wall, don't stop and wait there.** Read whatever shows without
  logging in (e.g. its price-calendar lowest), leave the tab open and **navigate it to its login page**
  so it's ready, add it to a **needs-login list**, and **move on** to the next platform. Query all the
  login-free / already-open ones first.
- **After all platforms are queried**, if any need login, prompt the user **once** with the whole list:
  *"这几个要登录才能看完整价：去哪儿、飞猪……我已把每个标签页停在登录页了。请你一次性全部登录（我不替你输密码/过
  验证码），都登好告诉我，我再回去逐个读价。"* **Wait** for one confirmation, then revisit each walled tab
  and **read its now-accessible fare**. The user logs in once for all, not once per site.
- **Fall back per-platform** only for sites with no browser / that the user skips: use web_search ranges
  **labeled** "web_search 估价 · 未浏览器核实，请在购票平台确认" — never as verified; keep the live-read
  platforms as the real comparison.

Trains are exempt: a 12306/web_search fare is the source of truth.

**Weather & season:**
- `"<目的地> <月份> 天气 气温 降水"` · `"<destination> weather in <month>"`
- within ~2 weeks: `"<目的地> 未来一周 天气预报"` · `"<destination> 7 day forecast"`
- `"<目的地> <日期> 节庆 活动"` · `"<destination> events <dates>"`

**Per-place facts (verify each):**
- `"<景点> 开放时间 门票 闭馆日"` · `"<attraction> opening hours ticket price"`
- `"<景点> 需要预约 吗 官网 购票"` (timed-entry / 预约 / sells out)
- `"<景点> 经纬度"` or `"<place> latitude longitude"` → for the map's `lat`/`lng`
- `"<餐厅/区域> 营业时间 人均 推荐"` for meal stops

**Tips & avoid-traps:**
- `"<目的地> 避雷 坑 攻略"` · `"<destination> tourist traps avoid"` (corroborate before repeating —
  one ranty post isn't proof; look for repeated, specific complaints).
- **小红书攻略（很有用，但要鉴别软广）。** 两条路：`web_search "<目的地> 攻略 小红书"`，或（浏览器已连时
  更佳）直接抓小红书搜索页 `.note-item` 列表读标题/作者/点赞——**搜索列表那层通常就够佐证**（多篇互证 +
  看点赞量判热度 + 标题鉴别软广），模板与五条反爬约束见 `references/scraping-method.md` §六点五（要点：
  必须登录态、别抽 xsec_token URL 而是点击进浮层、别高频防滑块）。搜 `"<目的地> 攻略"` / `"<目的地> <主题> 避雷"`，
  小红书的本地玩法、出片机位、排队避坑、亲子/银发实操常比官网鲜活。**但要会分辨软广/探店推广**：
  通篇只夸不提缺点、出现「合作/赞助/探店/团购券/到店报暗号」、统一话术配统一滤镜图、引导私信下单的，
  当广告打折看；**只采被多篇独立笔记重复印证的具体经验**（如"X点后不用排队""Y门进人少"），
  单篇热帖不作准，硬事实（票价/时间）仍以官网为准。

Capture for each place: name, address/area, **opening hours + closing day**, ticket price, why-go,
one practical tip, and `lat`/`lng`. If a field is unverifiable, record it as such and surface that in
the HTML rather than guessing.

---

## 2. Browser automation — only when search isn't enough

Use **Claude in Chrome** or **Windows-MCP** (whichever is installed) **only** to read live
availability / exact fares on 携程 / 飞猪 / 航司官网 / 12306. It is a read-only lookup, not a booking flow.

**抓数优先用 `javascript_tool` 读 DOM，别用截图认图（省 token + 解决高德 canvas 报错）。** 完整方法、
探测脚本、各站点实测选择器模板见 **`references/scraping-method.md`**（已 2026-06-13 复验）。三步：① navigate +
wait + **1 张**截图确认加载；② 跑探测脚本定位重复卡片的容器类名；③ 对容器 `querySelector` 批量提取成 JSON。
要点：CSS-modules 哈希类名（携程点评/高德评价）用 `[class*="稳定前缀"]` 包含匹配、别写死哈希后缀；懒加载用
JS 滚动循环；清零宽字符、按内容去重；**高德评价在 HTML 面板里(JS 可抓)，只有背景地图是 canvas(才截图)**。
已验证选择器：携程机票 `.flight-box`（滤掉首个广告位）、高德评价 `[class*="ReviewList_reviewItem__"]`、
携程点评 `[class*="reviewSwiper_reviewSwiper-item"]`。**这些选择器会随发版过期——是"自检缓存"不是信仰；
取到 0 条就按 scraping-method.md §八 自愈（探测脚本 → 锚定内容模式 ¥/HH:MM/日期/航班号 → 语义兜底 → 截图），
并把发现的新选择器写回模板。真正不变的是"锚定内容、不锚定类名"。**

**Stop-and-hand-back triggers (do not cross these):**
- Login / account / password prompt → stop.
- CAPTCHA / 验证码 / 滑块 / 人机验证 → stop (never solve or bypass).
- Any "下单 / 提交订单 / 支付 / 立即预订" step → stop.

When you stop, give the user: the exact query URL, the date/route you searched, and the options you
already read (times, prices, train/flight numbers). They complete the booking. Put a booking link in
the transport card so they can pick up where you left off.

---

## 2.5 Hotels — vet the reviews, prefer chains, compare prices

Pick **≥3 hotel options** near the itinerary's clusters / transit and matching the user's 住宿位置偏好.
Selecting one is the same discipline as flights — **research, don't trust the listing; compare across
platforms; never book.**

**Read the review section, not the marketing blurb (the decisive step).** A polished listing and a high
headline number prove nothing.

**评论必须双信源——携程 + 高德地图，缺一不可（用户硬性要求）。** 单一平台的评论不够可信：携程好评常偏
光鲜、商家运营痕迹重；高德的 POI 评价更接近真实住客口碑。流程：携程筛「4.7 分以上」找候选连锁 → 逐个读
携程评论区 → **同一家再去高德读一遍评论**（URL 模板见上：`amap.com/search?query={城市}{酒店名}` → 点搜索
按钮 → 点 POI → 「评价」，真实带日期）→ **交叉比对**：两边一致才放心；**携程光鲜但高德出现复发吐槽
（旧/吵/窗户/卫生），信高德的警告**。`.review-check` 里写清"两边都读了、各自说了什么"。其它信源（大众
点评 / 小红书 / Google / Booking）可加，但携程+高德是底线。**sort to recent + lowest** so you read fresh
and negative ones, then judge whether the review area looks **normal**:

| Signal | Healthy (pick) | Suspicious (avoid / warn) |
|---|---|---|
| Volume & recency | many reviews, some in the last weeks | few, or all stale/old |
| Score shape | believable mix, mostly good | **100% 5★**, or score clashes with the written complaints |
| Specificity | concrete (隔音/早餐/前台/床/水压) | generic, dateless, copy-paste praise (水军 tell) |
| Negatives | minor/manageable | **recurring serious**: 卫生差/有虫/隔音/不安全/偷换房型/强制消费 |
| Cross-platform (携程↔高德) | both agree | 携程 glows but 高德 surfaces recurring complaints → **trust 高德's warnings** |

If the same serious complaint repeats across recent reviews, **drop the hotel** no matter how nice the
photos are.

**Prefer chains (连锁) when they fit — especially 银发/亲子** (consistent cleanliness, standards, easy
recourse): **华住会** (汉庭 / 全季 / 桔子 / 星程 / 宜必思 / 美居), **锦江** (锦江之星 / 7天 / 维也纳), **首旅
如家** (如家 / 和颐). A chain is **not an auto-pick** — a branch with bad recent reviews is still out
(**reviews override the brand**). Boutique/民宿 is fine if its reviews are strong, specific, authentic,
and it suits the trip — flag the higher variance.

**Multi-platform price (per night) — reuse the flight flow exactly.** Browser-check the same room/date on
**携程 + 飞猪** (+ Booking/Agoda international). **价格的第二家是飞猪，不是高德——高德没有房价。**
**价格(携程+飞猪)和评论(携程+高德)是两套独立要求，别因为评论查了携程+高德就跳过飞猪价格**（真实翻车：
agent 把"双源"当成查两家就完事，丢了飞猪比价）。一张卡 = 携程(价+评)+飞猪(价)+高德(评) 三次读；飞猪只有
真连不上/验证码墙才如实标注并退估价。**不要默认「集团 App 会员价更低」**——实测华住会企业铂金会员价也未必
低于携程，且华住会官网根本查不到价；会员价只有真读到了才能写。Cheapest tagged, query time noted,
`.price-compare` block. **Same defer-and-
batch login handling and query-only prohibitions as §1 flights** — you never log in / solve captchas /
book. Search shapes: `"<酒店名> 大众点评 评价"`, `"<酒店名> 携程 价格 <日期>"`, `"<品牌> <区域> 店 怎么样 测评"`.

---

## 3. Time-budget rules of thumb

Honest time accounting is what makes a plan usable. Rough stay durations (adjust to interest level):

| Stop type | Typical stay |
|---|---|
| 大型博物馆 / 美术馆 | 2–3 h |
| 地标 / 寺庙 / 广场 | 45–90 min |
| 观景台 / 塔 | 45–60 min |
| 公园 / 古镇老街 漫步 | 1.5–3 h |
| 主题乐园 | 大半天–整天 |
| 正餐 | 60–90 min；排队店 +30–45 min |
| 咖啡 / 小吃歇脚 | 30 min |

Add **point-to-point transit** between stops. **跨片区/打车腿的里程·时长·过路费必须真的去高德路线规划
跑一遍**（浏览器已连时这是强制动作，不是写个「以高德为准」就算完——那是连不上浏览器时的退路）。
真实翻车点：一次浏览器已连的运行里，agent 把所有路线都只标了「以高德为准」却没去高德实跑，等于放弃了
本可拿到的真实里程/时长。流程：高德搜起点 POI → 点「路线」→ 改终点 → 读驾车里程/时长/过路费（打车价用
里程×当地出租计价标准折算并注明来源），并在 `.transit`/step 标「（高德实测）」。metro hops are often
20–40 min door-to-door once you count walking + waiting — **plus a 15–20 min buffer** per transition.
A day that looks full on paper with zero buffer will run 1–2 hours late by afternoon — pad it.

**Commute annotation + steps.** Record each inter-stop hop as **mode + distance + time** and put it in
the `.transit` connector between POI cards. Walking pace ≈ **70–80 m/min** (slower for 银发/亲子). Sum
the day's walking distance and convert to a **步数估算** (≈ **1,300 步/km**, e.g. 5 km ≈ 6,500 步) for the
day's overview line. Keep it grounded in the actual legs — don't print a step count you didn't derive.

**Pacing by profile:**
- 悠闲 / 银发 / 亲子（幼童）: 2–3 主要点/天, 早出晚归但中途留休息, 少爬楼梯, 午后留空档.
- 适中: 3 主要点/天 + 1 顺路小点.
- 暴走: 4 主要点/天, 早起, 接受长通勤 — only if the user chose this.

**Arrival/departure days are half-days.** Anchor them to the real flight/train times from Step 2 and
keep them light (drop bags, one nearby easy stop, good dinner).

---

## 4. Geographic clustering

- Plot every candidate stop (mentally or via the map) and **group by area**; assign each cluster to a
  day or half-day so the route reads as one smooth loop, not cross-town ping-pong.
- Order stops within a day to minimise backtracking; end near transit back to the hotel or near
  dinner.
- Use sunrise/sunset: sunrise spots first thing, sunset/night-view spots to close the day.
- Multi-city / day-trips: cluster the out-of-town trip on its own day, account for the round-trip
  transit time, and don't also pack the home city that day.

The embedded Leaflet map is your sanity check — if a day's polyline zig-zags across the whole city,
re-cluster.

---

## 5. Meals, constraints, energy, Plan B

- **Meals on the line**: pick lunch/dinner near the stop you'll physically be at when hungry; note
  hours and rough 人均. Respect dietary needs from Step 1 (清真 / 素食 / 过敏 / 忌口).
- **Hard constraints**: never schedule a stop on its closing day; honor 预约/timed-ticket windows;
  respect 无障碍 needs (elevators, fewer stairs, stroller/wheelchair friendly).
- **Energy curve**: hardest day in the middle; lighter on arrival/departure and after any long
  travel leg.
- **Plan B**: for each outdoor-heavy day give a concrete indoor alternative nearby (museum, mall,
  aquarium, covered market, café street) in a `weather` callout. Tie it to the actual forecast when
  you have one.

---

## 6. Map coordinates

Each map stop needs numeric `lat`/`lng` (decimal degrees, ~4 decimals). Prefer well-known/verified
coordinates; a **district or landmark** coordinate is a fine fallback when a precise one isn't
available — an approximate pin beats no pin. Do **not** fabricate precise-looking coordinates for a
place you couldn't locate; round to district level and say the pin is approximate if needed. Set
`TRIP.center` to the city center and `TRIP.zoom` to 10–12 for a single city.

---

## 7. Honesty & safety recap

The governing rule is the **数据诚信契约 in SKILL.md** — read it; it overrides everything else. Recap:

- **每个具体数字/事实：本会话实查到（带来源标记）或不写成具体值（hedge，无杜撰细节）。宁可不写，绝不编。**
  这条管所有面，不只是酒店：票价/营业时间/地址/车次/时刻/船票/打车费/里程/步数/预约配额/坐标/天气。
- **受控『已验证』词**（已核/可信/实测/实测数据/分布正常/不像刷分/好评集中…及其同义词）只有真查到、且
  就近带来源+日期才能用；同一卡价格标了「未核实/估价」就不得出现这些词（自相矛盾 = 伪造已核实）。
- **没浏览器读到评论区时**：`.h-rating` 留空或「评分以 App 为准」（禁止任何分数/条数），`.review-check`
  只写连锁常识推荐理由（禁止任何评论区结论）。这与"价格回退标估价"是平行的铁律。
- **比价**：已废平台（去哪儿/美团/同程/艺龙，见平台真值表）禁止作价格行；估价行不得打「✓最低」。
- **打车/里程/时长**只能来自高德路线规划并标「（高德实测）」，否则写「以高德为准」。
- Query-only for tickets; never log in, never solve CAPTCHAs, never pay.
- The plan is advisory: end the HTML with a reminder to re-confirm hours and prices before going, and
  to book anything marked `must` early.
- `scripts/check_html.py` checks 8–10 backstop the most common fabrications (no-provenance hotel
  ratings/verdicts, fake 最低, repeated fake forecasts) — a backstop, not a substitute for the contract.
