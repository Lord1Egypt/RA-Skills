# 工具参考（11 个）

与 `https://www.wwzu.com/mcp` 的 MCP 服务完全同构。内容层 5 个受每日额度约束（普通 100 次/Key、
VIP 300 次，次日自动恢复），计费层 6 个免费且不占额度。`comic_id` 对外统一为官网 htmlname
（如 `17763369151688`），入参亦兼容内部数字 ID。

---

## 内容层（5）

### get_site_overview()

站点统计 + 全部标签目录，无参数。统计缓存 5 分钟。

返回：`comics`（连环画部数）、`pages`、`characters`、`chat_characters`（可对话角色数）、
`ai_character_images`、`tags`（标签数）、`tag_list[]`（`{name, comic_count}`，按数量降序——
`tag_list[].name` 即 `browse_comics` 的合法 `tag` 值）。

### browse_comics(query, tag, ranking, related_to, sort, order, limit, offset)

统一浏览入口。**四种模式互斥，一次只传一个**，同时传多个会返回错误：

| 模式 | 参数 | 说明 |
|---|---|---|
| 搜索 | `query` | 标题关键词，空格分隔多词 OR 匹配（≤5 词）；排序：精确匹配 > 前缀 > 命中词数 > 热度 |
| 标签 | `tag` | 标签名见 `get_site_overview` 的 `tag_list`；`sort` 白名单 hits/wwwid/rating/jishu（默认 hits）；配合 `offset`/`total` 翻页 |
| 榜单 | `ranking` | `favorites` 收藏 / `rating` 评分 / `hot` 综合热度（≤50 条） |
| 相关 | `related_to` | 锚点书的 comic_id，随机抽样 ≤10 条 |

`limit` 默认 20，`order` 默认 desc。

返回：`{mode, total, limit, offset, comics[], unlock_hint}`。条目字段同构：
`comic_id`（官网 htmlname）、`web_url`、`title`、`cover`（800×600）、`page_count`、`tags[]`、
`collection`（丛书）、`year`、`publisher`、`author`、`rating`、`rating_count`、
`unlock_points`（按页数档位估算的积分解锁价，仅 VIP 可用积分解锁）、`download_available`；
ranking 模式额外有 `favorite_count` 与 `ranking_note`。

### get_comic(comic_id, page=0, page_start=1, page_limit=0)

书详情一步到位，**解锁态自适应**——未解锁不报错，降级返回并附引导。`page`（单页模式）与
`page_start/page_limit`（列表模式）互斥。

- 未解锁：基础信息 + 前 20 页图预览（`preview_limited=true`）+ `unlock_quote` 解锁报价块 +
  `description_tts_url` 整书梗概语音 + `preview_note` + `how_to_unlock`
- 已解锁：全量页图（默认 50、上限 200/次，`page_start = 上次 page_start + returned` 翻页，
  `page_start + returned - 1 >= pages.total` 即取完整本）+ 逐页 `audio_url` 朗读 + 逐页 `text`
  + `story` AI 故事资料 + `reading_guide`（漫剧模式播放指引）

返回（基础块）：`comic_id, web_url, title, cover, page_count, tags, collection, year, publisher,
author, rating, rating_count, download_available, colored, has_audio, has_story_analysis,
unlocked, description_tts_url`；列表模式加 `pages: {total, returned, page_start, page_limit,
preview_limited, items[]}`（页条目 `page_number, image_url, width, height`，解锁后加
`audio_url, text`）；单页模式加 `page: {...}`。

`unlock_quote` 结构：`tier`（A/B/C 档）、`points_price`、`yuan_price`、`points_balance`、
`affordable_by_points`、`points_unlock_vip_only`、`unlock_perks[]`、`nudge{progress,
unit_price, value_anchor, recommended_method, instant}`、`how_to_unlock`、`[resource_pack]`、
`[social_proof]`、`[pending_order]`（有同书未付订单时提示）。

### search_characters(query, character_ids, comic_id, random, include_ai_images, ai_images_limit=20, limit=20)

角色查询五合一。`query`（姓名关键词，≤5 词 OR）/ `character_ids`（≤50 个）/ `comic_id`（该书全部
角色）/ `random`（随机一个可对话角色）互斥。

返回：`{requested, total, full_profile_count, basic_only_count, not_found[], characters[], hint?}`。
角色条目：`character_id`、`name`、`role_type`、`avatar`、`can_chat`（是否可 AI 对话）、`hits`、
`comic_id`、`web_url`、`comic_title`、`book_unlocked`、`description`；所属书已解锁时额外有
`appearance`/`personality` 完整档案与 `ai_images[]` 图集，未解锁自动降级并附 `hint` 引导。

### chat_with_character(character_id, message)

AI 角色沉浸式角色扮演。**免解锁、不占每日额度**，1 积分/条（与官网同价同账本）；仅
`can_chat=true` 的角色；`message` 1–500 字符；对话历史与官网互通。

返回：`{comic_id, web_url, character_id, name, comic_title, reply, billing: {charged_points,
points_left}}`。余额不足时返回业务错误，内含差额与充值引导——照转述即可。

---

## 计费层（6，全部免费调用、不占每日额度）

### get_account(unlocked_limit=20)

账户总览：`points_balance`（积分余额）、`is_vip`、`vip_expired_at`、`rate_note`、
`packages[]`（积分充值套餐 `{key, label, points, price, bonus, vip_bonus, total_points}`，
key 如 p100/p500/p1000/p3000/p5000）、`vip_plans[]`（`{key: monthly|quarterly, label, months,
price, grant_points}`）、`vip_perks`、`how_to_recharge`、`how_to_vip`、
`unlocked_comics: {total, has_more, items[]}`（书架，`{comic_id, web_url, title, unlock_points,
unlocked_at}`）。

### unlock_comic(comic_id, method='points')

解锁合一，幂等（重复调用不重复扣/不重复下单）。

- `method='points'`：**VIP 专享**直接扣积分（零跳转）；非 VIP 或积分不足时返回
  `vip_only_points`/`shortfall` 与充值引导，不扣分
- `method='alipay'`：**免费会员唯一解锁方式**，VIP 积分不足时也用它。创建支付宝订单码订单并返回
  `qr_code`（码串/链接兜底）与 `qr_code_image`（正方形 PNG **data URI**，`<img>` 直嵌 1:1 显示，
  严禁落盘后用本地路径引用）、`order_no`、`amount`、`pay_before`（付款前须知）、`unlock_perks`、
  `next_step`、`[resource_pack]`。同书 5 分钟内未付订单自动复用，订单 30 分钟有效

成功（积分路径）返回：`{unlocked, already_unlocked?, method, comic_id, title, tier,
deducted_points, points_balance, order_no, unlock_perks[], next_step[, resource_pack]}`。

### check_payment(order_no='', comic_id='')

支付确认 + 自动履约，免费、可反复轮询。`order_no` 可传解锁单/积分单/VIP 单；**全空参数时查
本人最近一笔待确认订单**（优先级：解锁 > 积分 > VIP）。

- 解锁单：`{paid, order_type:'unlock', unlocked, comic_id, title, order{…}, message, next_step?}`
- 积分单：`{paid, order_type:'points', order_no, credited_points, points_balance, message}`
- VIP 单：`{paid, order_type:'vip', order_no, months, is_vip, vip_expired_at,
  points_balance, message[, granted_points, renewal]}`

`paid=false` 时 `message` 会说明"数秒内到账，请稍后再查"；`paid=true` 后按 `next_step` 推进。

### recharge_points(package_key)

对话内积分充值下单：返回 `order_no`、`amount`、`points`、`package_label`、`vip_bonus`
（VIP 加赠部分）、`next_step`、`fallback`（官网兜底）、`qr_code`、`qr_code_image`（data URI）。

### purchase_vip(plan_key)

VIP 开通/续费下单。`plan_key='monthly'`（月卡 ¥9.9，赠 1200 积分）或 `'quarterly'`（季卡 ¥29.7，
赠 3600 积分）。返回：`{order_no, amount, plan_key, plan_label, months, grant_points, renewal,
vip_perks, next_step, fallback, qr_code, qr_code_image}`。

履约口径：支付到账即赠积分并顺延有效期（未过期从现有到期时间顺延，规范到当日 23:59:59），
**无自动续费**；与官网 vip-subscribe.php 同价同权益。

### reset_daily_quota()

额度自救：扣 100 积分立即清零今日查询计数（重置后按当前身份限额生效，VIP 300）。今日未消耗、
积分不足或无有效 Key 时拒绝并不扣分。返回：`{reset, cost_points, points_balance, daily_used:0,
daily_limit, is_vip, message}`。

---

## 错误语义速查

| 现象 | 含义 | 处理 |
|---|---|---|
| HTTP 401 / 退出码 1 | Key 无效或已撤销 | 引导到 wwzu.com/mcp-keys.php 重建 |
| HTTP 429 / 退出码 1 | 4 个查询工具每日额度用尽 | `reset_daily_quota` 或次日自动恢复 |
| 退出码 2（isError） | 工具业务错误（参数不合法、积分不足、套餐不存在等） | 读服务端返回的原因与引导，转述给用户 |
| 内容"未解锁" | 不是错误 | 响应内含 `unlock_quote`/`preview_note` 等引导字段，照转述 |
