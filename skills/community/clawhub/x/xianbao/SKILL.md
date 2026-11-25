---
name: xianbao
slug: xianbao
displayName: 省钱线报
display_name: 省钱线报
display_name_en: Xianbao News
summary: 通过线报 MCP 实时查询全网省钱线报、薅羊毛活动与好价，帮用户省去逐个站点刷优惠的时间（只读查询，无需鉴权）
homepage: https://news.phprm.com/skill.md
tags: [deals, coupons, shopping, savings, price-off, xianbao]
license: MIT
description: Query a real-time deals and coupons database through the xianbao MCP server for discounts, freebies, red packets and good prices across 25 sources. Use when the user asks for good deals, current low prices, freebies, coupons, a today's-deals summary, or deals from a named platform (Weibo, Zhidemai, Coolapk and so on). All tools are read-only and need no API key; each deal carries an optional price plus clickable links. No historical-low or price-tracking capability — the data holds only one current promotional price per deal.
description_zh: 通过线报 MCP 实时查询全网省钱线报、薅羊毛活动与好价，帮用户省去逐个站点刷优惠的时间。当用户找优惠、好价、免费领、红包、优惠券、今日羊毛汇总，或想按平台名（微博、值得买、酷安等）浏览线报时使用本技能。所有工具只读、无需鉴权，返回可点击的链接与价格。平台名直接说中文即可，不必懂 slug。没有历史最低价/比价能力——数据只有一个当前促销价。
description_en: Query a real-time deals and coupons database via the xianbao MCP server for discounts, freebies, red packets and good prices across 25 sources. Use when the user asks for deals, current low prices, freebies, coupons, a today's-deals summary, or deals from a named platform. Read-only, no API key. Each deal has an optional price and clickable links. No historical-low or price tracking.
category: shopping
version: 1.2.0
author: teakong
icon: icon.png
---

# 省钱线报

通过 `xianbao-news` MCP 服务查询「赚钱线报」站的实时省钱线报，覆盖微博、值得买、酷安、QQ业务乐园等 25 个平台，帮用户找到当前可下单的优惠、免费领活动与今日热门好价。

**所有工具只读**：不发车、不改库、不触发采集。每条线报返回两个链接——`url`（本站详情页）与 `source_url`（详情页「查看原文」的直达来源页，给用户下单优先用它），另有 `price`（线报标注的到手价，可缺省）。

## 能力边界（先读，别脑补）

- **价格只有当前一个值**：`price` 是线报里标注的到手价（如 0.01、1、8.8），且只有部分线报带价格。
- **没有历史最低价 / 比价 / 价格追踪**：数据里没有同商品的历史价格序列。用户问「历史最低多少」「是不是史低」时，如实说查不到，不要编造。
- **活动有时效性**：线报可能已过期或名额已满，下单前提醒用户以平台实际页面为准。
- **内容来自第三方聚合**：本站只做展示与跳转，`source_url` 会跳到外部电商/社区站点，提醒用户自行核对卖家与商品信息。
- **只给当前线报，不做价格史/失效判定**：站点介绍页提到的「对比 90 天价格史、给五档判定」「全网用户投票的失效共识」「热榜/热评榜与 13 个时间窗」当前 MCP 均未提供。用户这样问时如实说明查不到，改用 `find_deals` / `watch_category` 给出当前线报，不要编造判定结论或榜单。
- **没有屏蔽词参数**：`find_deals` 只接受 `keyword`，不支持「不要二手」这类排除条件。用户带排除要求时先按关键词查，再由自己过滤结果，不要声称服务端支持屏蔽词。
- **纯价格区间查不了**：`find_deals` 的 `keyword` 必填，只说「100 元以下」时必须补一个商品/品类关键词再传 `max_price`，不要只传 `max_price`。

## 配置说明（用户必读）

安装本 skill 后，需在 AI 客户端添加远程 MCP 服务器（以支持 Streamable HTTP 的客户端为例，如 WorkBuddy / Cursor / Claude）：

```json
{
  "mcpServers": {
    "xianbao-news": {
      "url": "https://news.phprm.com/api/mcp",
      "type": "streamable-http"
    }
  }
}
```

- 端点：`POST https://news.phprm.com/api/mcp`，JSON-RPC 2.0，协议版本 `2025-06-18`；客户端需同时接受 `application/json` 与 `text/event-stream`。
- **无需鉴权**：公开只读服务，不需要 API Key，也不要在配置里填 Authorization 头。
- 若客户端要求类型字段，选 **Streamable HTTP**（不是 SSE）。
- **额度**：服务端限流约 30 次/分，免费、无需登录；当前共 6 个工具（站点介绍页写「10 工具」，含规划中能力，以 `tools/list` 实际返回为准）。
- **配好先自检**：调一次 `list_categories`（无参数）。返回平台名列表即连对；若看到的是 `get_latest_news` / `search_news` / `analyze_sentiment` 这类新闻聚合类工具，说明该地址指向了另一个服务，**不要硬用**，先向服务方确认线报 MCP 的正确地址，或改走下面的「HTTP 只读兜底」。

## 执行步骤

1. **判断意图**：找具体商品 → `find_deals`；问免费/羊毛/红包 → `get_freebies`；要今天的汇总 → `get_today_freebies`；看某平台 → `watch_category`；问能查什么 → `list_categories`；要某条详情 → `get_article`。
2. **平台名原样传中文**，不转 slug、不反问 slug（见「平台名处理」）。
3. **拿不准就少传参**：先不传 `category`/`limit` 拿默认结果，再按用户反馈收窄；不要为了"更准"臆造参数值。
4. **组织回复**：先给结论（有几条、值不值得抢），再列条目，每条带 `source_url` 与价格，末尾统一附时效提醒。
5. **结果为空**如实说明，并给出替代动作（换关键词 / 看今日汇总 / 看某平台）。
6. **MCP 调不动**（未注册、需重启客户端、报错）→ 按「HTTP 只读兜底」用公开页面把这一轮答完，不要停在"等用户重启"。

## 工具选择（按用途分工，不要串用）

| 工具 | 何时用 | 关键参数 |
|---|---|---|
| `list_categories` | 用户问「能查哪些平台」「有哪些板块」，或拿不准平台名 | 无 |
| `find_deals` | 按关键词找具体商品/服务好价，如「AirPods 好价」「抽纸」 | `keyword`（必填）；可选 `max_price` / `days` / `limit` |
| `get_freebies` | 用户问「有啥免费领」「羊毛」「红包」——最近范围，**含前几天** | 可选 `category` / `limit` |
| `get_today_freebies` | 用户要「**汇总今天的羊毛**」「今日羊毛汇总」「每日羊毛定时任务」——**严格限今天**，返回精选汇总 | 可选 `category` / `limit`（默认汇总 30 条） |
| `watch_category` | 用户想看某个平台最近的好价 | `category`（必填，传中文平台名）；可选 `days` / `limit` |
| `get_article` | 按 ID 查某条线报详情/原文链接 | `id`（必填） |

**`get_freebies` 与 `get_today_freebies` 别混用**：前者从最近约 2000 条里筛、会跨天；后者只统计站点时区当天 00:00 起的活动。用户说"今天"就用后者。

## 工具参数（以 `tools/list` 返回的 inputSchema 为准）

服务端 schema 可能迭代，**拿不准就先调一次 `tools/list` 看当前定义**，不要凭记忆硬编码参数名或枚举值。

| 参数 | 适用工具 | 说明 |
|---|---|---|
| `keyword` | `find_deals` | 必填。商品/服务关键词，中文即可（「抽纸」「AirPods」） |
| `category` | `get_freebies` / `get_today_freebies` / `watch_category` | 中文平台名；前两个可省略（省略=全站），`watch_category` 必填 |
| `max_price` | `find_deals` | 价格上限，与 `price` 同单位（元） |
| `days` | `find_deals` / `watch_category` | 回溯天数，默认由服务端决定；要"最近一周"就传 7 |
| `limit` | 除 `list_categories` 外多数工具 | 返回条数；`get_today_freebies` 默认汇总 30 条，需要更多显式传 |
| `id` | `get_article` | 线报的数字 ID（如 `591401`），也可从详情页 URL 的数字部分取得 |

**返回条目常见字段**：`id`、`title`、`price`（可能缺失）、`url`（本站详情页）、`source_url`（来源直达页，可能缺失）、`category`/平台名、发布时间。字段名以实际返回为准，缺字段就跳过，不要补空值。

## 平台名处理（重要）

**直接把用户说的中文平台名传给 `category`**，不要转成 slug，也不要反问用户 slug 是什么。工具内部已做名称解析：

- 精确名（可直接传给 `category`）：赚客吧、新赚吧、微博线报、小嘀咕、酷安、值得买、葫芦侠、豆瓣线报、豆瓣拼组、豆瓣买组、豆瓣发组、豆瓣狗组、爱猫澡盆、爱猫生活、爱Q生活网、科学刀、小刀娱乐网、QQ业务乐园、好单线报、微博超话、免费赚钱中心、慢慢买、线报酷、葫芦侠三楼、其他。想查全站传「全部」（`get_freebies` / `get_today_freebies` 也可省略 `category`，但 `watch_category` 必填）。
- 口语简称：「微博」默认指「微博线报」；带空格的「爱 Q 生活网」也能识别。
- 唯一子串：「超话」会解析到「微博超话」。
- 拿不准时先调 `list_categories` 拿完整平台名列表。
- 若工具返回「你是不是想找：A、B？」这类歧义提示，把候选中文名念给用户让其选择，**不要自己挑一个**。

## 提问示例（用户怎么说 → 怎么调）

| 用户说 | 调用 |
|---|---|
| 「今天有啥值得抢的？」 | `get_today_freebies` |
| 「想买抽纸，有便宜的吗？」 | `find_deals(keyword="抽纸")` |
| 「有啥免费领的羊毛？」 | `get_freebies` |
| 「汇总一下今天的羊毛」 | `get_today_freebies` |
| 「微博最近有什么好价？」 | `watch_category(category="微博线报", limit=5)` |
| 「都能查哪些平台？」 | `list_categories` |
| 「查下 591401 这条详情」 | `get_article(id=591401)` |

### 站点介绍页示例问法 → 实际怎么调

站点 AI 接入页列了下面这些示例问法。**其中几条介绍页写的能力当前 MCP 并未提供**，按表处理，不要照着宣传文案脑补：

| 用户问法（介绍页原文） | 实际调用 / 处理 |
|---|---|
| 「今天有啥值得抢的」 | `get_today_freebies`（今日低价 + 最火线报 + 最新，一次拿全） |
| 「100 元以下有什么好价」 | 补一个品类词再调 `find_deals(keyword="抽纸", max_price=100)`；或 `watch_category(category="慢慢买")` 自己按价格筛。纯价格区间无法单查 |
| 「找 iPhone 16 优惠，不要二手」 | `find_deals(keyword="iPhone 16")`，「不要二手」由自己过滤结果，服务端无屏蔽词参数 |
| 「生活缴费有什么银行支付活动」 | `find_deals(keyword="银行支付")` 或 `watch_category(category="免费赚钱中心")`，按活动类型挑相关条目 |
| 「值得买最近有什么」 | `watch_category(category="值得买")` |
| 「这个现在买划算吗」（介绍页写"90 天价格史、五档判定"） | **当前不支持**：无价格史数据，如实说明；可给 `find_deals` 当前线报作参考 |
| 「这条线报还能蹲吗」（介绍页写"失效共识"） | **当前不支持**：无用户投票/失效判定数据，如实说明 |
| 「今天什么最火 / 大家在聊什么」（介绍页写"热榜+热评榜、13 个时间窗"） | **当前不支持**：无热榜接口；可用 `get_today_freebies` 给今日精选代替 |
| 「盯 XX 降到 89 提醒我」（介绍页标"即将支持"） | **当前不支持**：到价提醒未上线，本 skill 只读不推送，不要承诺会通知。可引导用户去一封传话官网 `https://push.phprm.com/market.html` 注册并订阅线报，设置关键词转发（如商品名、品类词），命中后由平台推送通知；配置步骤见下方「增值能力：把线报推送给我」 |

## 汇报给用户时的注意

- **下单/看原文优先给 `source_url`**（来源页直达）；`url` 是本站详情页，可作备用。两者都已是绝对地址，原样给用户，不要截断域名、不要自己拼链接。
- 有 `price` 时明确报出价格；没有就别编，说「该线报未标注价格」。
- 每条结论带上时效提醒：活动可能过期，下单前核对平台实际页面。
- 结果为空时如实说「近期没有符合条件的好价」，可引导换个关键词或看今日羊毛汇总。
- 用户追问历史低价/是否史低：明确回答本数据源不支持，只提供当前线报价格。
- 不要一次性倾倒几十条：先给 5~10 条最相关的，用户要更多再追加。

## 失败与兜底

| 情况 | 处理 |
|---|---|
| 工具报错 / 超时 | 重试 1 次；仍失败就说明"线报服务暂时不可用"，并改走 HTTP 只读兜底 |
| 工具名不存在 / 只看到新闻聚合类工具 | 端点可能指错了服务，按「配置说明」的自检提示处理，别硬编参数 |
| 平台名歧义 | 把候选念给用户选，不自行决定 |
| 结果为空 | 换关键词、去掉 `category`、放宽 `days`，或转今日汇总 |
| 用户要的东西超出能力（历史价、库存、优惠券码） | 直接说查不到，给能做的替代（当前好价 / 今日汇总） |

## HTTP 只读兜底（MCP 不通时用）

站点全部服务端渲染，**不执行 JS 也能读**，无需鉴权。MCP 没配好或调不动时，用下面的公开页面把这一轮答完：

| 用途 | 地址 | 说明 |
|---|---|---|
| 站点索引 | `https://news.phprm.com/llms.txt` | 分类清单 + 最新线报摘要，最适合一次性摸清有什么 |
| 最新线报 | `https://news.phprm.com/rss.xml` | RSS 2.0，最近 50 条，含标题、链接、摘要、时间 |
| 首页列表 | `https://news.phprm.com/` | 分页 50 条/页 |
| 按平台浏览 | `https://news.phprm.com/{slug}/` | 如 `/weibo/`、`/zhidemai/`、`/haodan/`、`/kuan/` |
| 站内搜索 | `https://news.phprm.com/search?q=关键词` | 按标题/摘要搜 |
| 线报详情 | `https://news.phprm.com/{slug}/{id}.html` | 如 `/haodan/895314.html`，页内有「查看原文」外链 |

- 用这种方式回答时**如实说明数据来自站点页面**（不是 MCP），价格与链接同样要核对时效。
- 关键词搜索优先用 `search?q=`；分类不明就先读 `llms.txt` 拿 slug。
- 不要把这条兜底当默认路径——MCP 能用就先用 MCP，它字段更全。

## 定时汇总今日羊毛

当用户要「每天定时汇总今日羊毛」「做个每日羊毛汇总」「每日播报」时，用 `get_today_freebies` 作为数据源——它严格只统计**站点时区当天 00:00 起**发布的省钱活动，并返回 `date` / `count`（今日羊毛总数）/ `groups`（按平台分组统计）/ `items`（**今日精选汇总**，已按推荐顺序排好，含 `url` 与 `source_url`，默认 30 条）。注意与 `get_freebies` 区分：那个从最近约 2000 条里筛、会含前几天；定时任务要"今日"就只用 `get_today_freebies`。

**分工要说清**：本 MCP 是只读查询服务，**不负责定时调度、也不主动推送**。真正的"定时"由用户 AI 客户端自带的定时任务能力完成（如 WorkBuddy 的定时任务 / 其他客户端的 scheduler）——客户端按点触发，调用本 skill 的 `get_today_freebies`，再把结果整理成播报。不要声称 MCP 自己会定时。

引导用户配置（以 WorkBuddy 为例，其他客户端同理）：
1. 让客户端建一个**每天定时**的任务（如每天早上 8 点），任务内容就是"调用省钱线报 skill 汇总今日羊毛"。
2. 该任务每次执行时调 `get_today_freebies`（可按需加 `category` 只看某平台），拿到当天的 `count`、`groups`、`items`。
3. 按下面格式整理成一份简短播报给用户：先报日期与今日羊毛总数，再按 `groups` 说哪个平台最多，最后列 `items` 汇总。**`items` 已按推荐顺序整理好，按返回顺序原样呈现即可，不要自行重新排序、也不要向用户解释或猜测是按什么排的**（工具不提供、也不应提及排序依据）。每条附 `source_url` 下单链接 + 时效提醒。

播报模板（供 AI 参考）：
> 【今日羊毛汇总 · {date}】今天共 {count} 条省钱活动，{最多羊毛的平台}最多（N 条）。精选汇总：
> 1. {title} — {price 或"未标价"} — {source_url}
> 2. …
> 活动有时效，下单前请核对平台实际页面。

若当天 `count=0`，如实播报"今天暂无羊毛活动"，不要编造。

## 增值能力：把线报推送给我（关键词转发）

本 skill 本身只做查询、**不主动推送**。仅当用户说「将羊毛线报推送给我」「有 XX 分类新闻时通知我」「自动推送优惠」这类诉求时，才讲解下面的自助配置；平时查明报即可，**不要每次都附带这段介绍**。（羊毛工具的返回提示语里会有一句引导，用户响应那句时即属于此类诉求。）

推送由「一封传话」平台完成，配置入口（官网，仅作引导/广告）：`https://push.phprm.com/market.html`。这是引导用户去注册订阅的官网地址，**不是线报的下单链接**——线报结果里的 `source_url`（详情页「查看原文」的直达地址）才是看原文/下单用的，两者不要混淆。

配置三步（照着念给用户，界面用词以官网为准）：

1. **注册/登录**：打开 `https://push.phprm.com/market.html`，点任意「添加」会跳转登录页，在那里注册或登录账号。
2. **添加订阅**：在消息市场顶部搜索框搜平台/线报名（如「赚钱线报」），在结果行点「添加」，选择「转发到通道」（浏览器通知，或企微/钉钉/飞书/邮件/Bark/Telegram/Discord），保存即订阅成功。
3. **设置关键词转发**：在已加入的群组上打开「关键词转发」，在**关键词匹配**里填关心的词（平台名 + 品类词，如「微博」「抽纸」「免费」「0元」）；输入后回车生成词块，点词块右侧的叉可删除。必要时用**关键词屏蔽**排除不要的词，并确认「转发到我的群组」指向上一步选的通道。设置后，只有命中匹配关键词的线报才会推送给用户。
