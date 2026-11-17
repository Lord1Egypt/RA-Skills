# 业务流程与对客话术

按用户旅程组织。所有流程都基于 11 个工具（见 `tools.md`）；涉及金钱的动作（解锁/充值/开通 VIP）
一律走支付宝订单码 + `check_payment` 轮询，全程不离开对话。

---

## A. 开通 API Key（新用户第一关）

### A1. 对话内开通（首选，约 60 秒）

适用：用户没有 `XIANMU_API_KEY`，且 `https://www.wwzu.com/api/mcp/keys` 可用。

1. 向用户说明："需要一把免费 API Key，您提供一个邮箱，验证码来了念给我，我帮您开通，
   全程不用离开对话。"
2. 用户给出邮箱后调用：
   ```
   POST https://www.wwzu.com/api/auth/send-code
   Content-Type: application/json
   {"email": "用户邮箱"}
   ```
   成功返回 `{"success":true,...,"message":"验证码已发送"}`。同邮箱 60 秒冷却、每日 10 次。
3. 请用户把邮箱里收到的 **6 位验证码** 念出来（10 分钟有效）。
4. 验证码登录（邮箱不存在会自动注册并送 30 积分）：
   ```
   POST https://www.wwzu.com/api/auth/login
   {"email": "用户邮箱", "code": "6位验证码"}
   ```
   从 `data.token` 取出 **remember_token**。
5. 创建 Key（明文仅此一次）：
   ```
   POST https://www.wwzu.com/api/mcp/keys
   Authorization: Bearer <data.token>
   Content-Type: application/json
   {"key_name": "skill"}
   ```
   返回 201，`key` 字段即 `xm-` 明文 Key；若返回 409 `keys_limit`，说明该账号已有 Key——
   请用户到 [wwzu.com/mcp-keys.php](https://www.wwzu.com/mcp-keys.php) 用"更换 Key"
   （旧 Key 会失效，需向用户确认）或直接粘贴已有 Key。
6. 征得用户同意后写入环境变量，并**绝不回显完整 Key**：
   - macOS/Linux：追加 `export XIANMU_API_KEY="xm-…"` 到 `~/.bashrc`（或 `~/.zshrc`）
   - Windows：`setx XIANMU_API_KEY "xm-…"`，提醒**重开终端**生效；当前会话可临时 `set` 生效
7. 提醒用户两点：若该邮箱此前在官网登录过，本次对话内登录会使旧网页登录态失效；
   Key 已保存进环境变量，今后无需重复提供。
8. 立即用 `get_site_overview` 跑通一次验证，然后推荐一条免费演示提示词（见 E 节）。

### A2. 浏览器兜底（端点未部署 / 用户偏好网页）

1. 请用户打开 [wwzu.com/login.html](https://www.wwzu.com/login.html)：输入邮箱 → 收验证码 →
   登录（即注册，自动送 30 积分）。
2. 打开 [wwzu.com/mcp-keys.php](https://www.wwzu.com/mcp-keys.php) → 点"创建 Key" →
   页面直接显示明文 Key。**提醒：明文仅展示这一次，当次复制保存。**
3. 用户把 Key 粘贴到对话里后，按 A1 第 6 步写入环境变量。

### A3. Key 异常的再入口

- 退出码 1 + HTTP 401：Key 无效/已撤销 → 引导 A1（若用户已有账号直接走 A2 的 keys 页"更换 Key"）
- 用户说"忘了 Key / 找不到了"：明文无法找回 → 引导 keys 页"更换 Key"（旧 Key 失效）
- 额度 429：见 F 节错误处理

---

## B. 找书与阅读（免费体验主路径）

1. 明确意图：找题材 → `get_site_overview`（拿真实标签）→ `browse_comics(tag=…)`；
   找具体书 → `browse_comics(query=…)`；"随便推荐" → `browse_comics(ranking='hot')`；
   "和这本类似的" → `browse_comics(related_to=comic_id)`。
2. 展示结果：挑 3–5 部，给出 `title`/`page_count`/`rating`/`collection` 与 `web_url`，
   不要整页照搬。
3. 用户选中后 `get_comic(comic_id)`：
   - 未解锁：讲基础信息与梗概，`<audio>` 播放 `description_tts_url`，展示前 20 页预览图，
     并转述 `unlock_quote` 的价格与权益（见 D 节话术）
   - 已解锁：进入**漫剧模式**——按 `reading_guide` 逐页展示 `image_url`、自动播放
     `audio_url` 朗读，配合 `text` 字幕；长书用 `page_start` 翻页，讲完一页再翻下一页
4. 单页细看：`get_comic(comic_id, page=N)` 返回该页图+音频+文字三件套。

---

## C. AI 角色对话

1. 找角色：`search_characters(query="角色名")`；"来个能聊天的" → `random=true`；
   "这本书里有哪些角色" → `comic_id=comic_id`。
2. 确认 `can_chat=true` 后 `chat_with_character(character_id, message)`。
3. 计费透明：告诉用户 1 积分/条、免解锁；返回的 `billing.points_left` 余额较低时主动提醒充值。
4. 提示词建议引导用户用角色口吻对话，例如："让聂小倩用她自己的口吻，讲讲兰若寺的那段往事。"

---

## D. 解锁支付（对话内闭环）

1. 用户表达想看完整内容 → `unlock_comic(comic_id, method='alipay')`（免费会员唯一通道；
   VIP 用户可选 `method='points'` 扣积分解锁，零跳转）。
2. 把 `qr_code_image` 以 `<img src="…">` 直嵌展示（PNG data URI，正方形 1:1），
   辅以 `amount` 金额与 `unlock_perks` 权益说明；`qr_code` 码串仅在用户想用浏览器打开时给。
3. 主动轮询 `check_payment(order_no=…)`（数秒一次，通常立即到账）：
   - `paid=true, unlocked=true`：恭喜 + 转 `next_step`（回 `get_comic` 看全书 / 资源包下载指引）
   - `paid=false`：告知"扫码后数秒内到账，我再查一次"，继续轮询或等用户回复后重查
4. 有同书未付订单时响应会带 `pending_order`——直接提示继续支付该单，不要重复下单。
5. VIP 用户积分不足走 `unlock_comic(method='points')` 会返回 `shortfall` 与套餐引导 →
   转 E/F 节充值流程。

**对客话术基线**（照 `unlock_quote` 字段转述，勿编造）：
"这本书共 N 页，未读部分按部买断 ¥X.X（一次性买断、解锁后永久可读，无订阅）；
您已免费看到前 20 页。扫码支付后我立即帮您解锁全书并开启逐页朗读。"

---

## E. 积分充值

1. `get_account` 看 `packages[]`（p100=100分/¥1 … p5000）与余额；VIP 充值有 `vip_bonus` 加赠 10%。
2. `recharge_points(package_key='p100')` → 展示 `qr_code_image` + 金额。
3. `check_payment(order_no=…)` 轮询 → `paid=true` 后报 `credited_points` 与新余额。

---

## F. VIP 开通 / 续费

1. 用户问 VIP → `get_account` 读 `vip_plans`/`vip_perks`/`how_to_vip`，如实转述：
   月卡 ¥9.9（赠 1200 积分）/ 季卡 ¥29.7（赠 3600 积分）；每日额度 300 次、每月赠 1200 积分、
   充值加赠 10%、积分解锁/下载专享、签到双倍；**无自动续费**，到期前随时续费顺延。
2. `purchase_vip(plan_key='monthly'|'quarterly')` → 展示二维码 → `check_payment(order_no=…)`。
3. `paid=true`：报 `months`、新 `vip_expired_at`、`granted_points`（赠分已到账）、
   `renewal`（是否为续期）；引导用户重新查看权益生效（如查询额度升到 300 次/日）。

---

## G. 免费演示提示词（开通后立刻跑一条，建立价值感）

题材多样、均可在真实内容上命中：

- "帮我找几本聊斋志异题材的连环画，挑一本讲讲梗概，再放一段梗概语音"
- "《画皮》讲的是什么？先给我看前几页"（comic_id=17763369151688）
- "我想和聂小倩聊聊她的故事"（character_id=9574）
- "找评分最高的岳飞题材连环画，让岳飞给我讲讲精忠报国"（岳飞 character_id=68）
- "白蛇传这本书值不值得解锁？给我看看预览和报价"
- "你们一共有多少部连环画？收藏榜前十是哪些？"

---

## H. 错误处理手册

| 情况 | 判别 | 处理 |
|---|---|---|
| Key 无效 | 脚本退出码 1，stderr 含 HTTP 401 | 引导 A1/A2 重建 Key，更新环境变量后重试 |
| 额度用尽 | 退出码 1，stderr 含 HTTP 429 | 说明"4 个查询工具每日 100 次（VIP 300）"；提供 `reset_daily_quota`（扣 100 积分立即重置）或次日再用 |
| 会话失效 | 脚本已自动重握手重试一次；仍 404 时 stderr 提示 | 检查 `XIANMU_MCP_URL` 是否被改动；重跑即可 |
| 业务错误 | 退出码 2（isError） | 常见：参数不合法（如 browse_comics 模式互斥）、无效套餐、积分不足——服务端已给原因与引导，照转述 |
| 支付未到账 | `check_payment` 反复 `paid=false` | 确认用户确实扫了码；提示订单 30 分钟有效，可稍后再查或重新下单 |
| 内容未解锁 | 正常响应含 `preview_note`/`unlock_quote` | 不是错误；走 D 节解锁流程 |
