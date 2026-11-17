---
name: xianmu-comics
version: 1.2.0
author: 闲沐（wwzu.com）
display_name: 闲沐连环画
display_name_en: XianMu Comics
description_zh: 把 568 部中国经典连环画（小人书）接入对话：搜书看图、逐页朗读、与书中角色 AI 沉浸式对话，全本逐页可读。
description_en: Bring 568 classic Chinese lianhuanhua (picture-story books, 1960s–1990s) into chat — search & read, page-by-page narration, AI role-play with book characters, full-book reading.
description: >-
  闲沐连环画（XianMu Comics）：把 568 部中国经典连环画（小人书，1960s–1990s）接入对话——书目搜索/
  标签浏览/榜单、书页图片、故事梗概语音、逐页朗读、14171 个角色档案与 5690 个可对话角色的 AI 沉浸式
  角色扮演。当用户想找书、看/读连环画、小人书、老漫画，想和书中角色（聂小倩、岳飞等）聊天，或想阅读
  某本书的完整版时使用；用户提到 闲沐、xianmu、wwzu、连环画、小人书、lianhuanhua、Chinese picture-story
  books 时也应触发——即使用户没有明说"连环画"三个字。
---

# 闲沐连环画（xianmu-comics）

把中国经典连环画（小人书）变成对话里可看、可听、可聊、可付费的内容服务。本技能与
`https://www.wwzu.com/mcp` 的 MCP 服务功能完全一致（同一端点、同一 Key、同一计费），
让没有 MCP 配置能力的智能体也能直接使用全部 11 个工具。

## 服务速览

- 端点：`https://www.wwzu.com/mcp`（Streamable HTTP），认证 `Authorization: Bearer xm-你的Key`
- 内容规模：568 部连环画 / 56073 页 / 14171 个角色（5690 个可 AI 对话）/ 105 个标签
- 门户：[服务介绍](https://www.wwzu.com/mcp-landing.php) ·
  [接入文档](https://www.wwzu.com/mcp-docs.php) ·
  [Key 管理](https://www.wwzu.com/mcp-keys.php) ·
  [计费](https://www.wwzu.com/mcp-billing.php)

## 开始前：确认 API Key

调用任何工具前都需要一把 `xm-` 开头的 API Key（环境变量 `XIANMU_API_KEY`）。检测到没有 Key 时，
按以下顺序引导用户（详细步骤与对客话术见 `references/workflows.md` 第 A 节）：

1. **对话内开通（首选，约 60 秒）**：请用户提供邮箱 → `POST https://www.wwzu.com/api/auth/send-code`
   （`{"email":"…"}`）→ 用户把邮箱里的 6 位验证码告诉你 → `POST https://www.wwzu.com/api/auth/login`
   （`{"email","code"}`，邮箱不存在会自动注册并送 30 积分）→ 用返回的 `data.token` 调
   `POST https://www.wwzu.com/api/mcp/keys` 创建 Key。若该端点返回 404（尚未部署），回落到方式 2。
2. **浏览器兜底**：请用户打开 [wwzu.com/login.html](https://www.wwzu.com/login.html)
   （邮箱验证码一步注册+登录）→ [wwzu.com/mcp-keys.php](https://www.wwzu.com/mcp-keys.php)
   点"创建 Key"→ 把显示的明文 Key 粘贴给你。提醒用户：**Key 明文仅展示这一次**，当次复制保存。
3. **持久化**：拿到 Key 后，征得用户同意再写入环境变量（macOS/Linux 写 `~/.bashrc` 或 `~/.zshrc`
   的 `export XIANMU_API_KEY=xm-…`；Windows 用 `setx XIANMU_API_KEY "xm-…"` 并提醒重开终端生效）。
   **任何时候都不要在回复中回显完整 Key**，展示时只显示前 4 后 4（如 `xm-a1…f3`）。

注意：已有账号走对话内登录会轮换其 `remember_token`（旧网页登录态失效），引导时向用户说明。

## 调用方式（按优先级三选一）

1. **客户端已配置 xianmu-comics MCP**：会话里已有本服务的 MCP 工具（名称形如
   `mcp__xianmu-comics__*`）→ 直接调用，跳过本技能的脚本调用。
2. **本技能脚本（推荐）**：调用本文件所在目录下的 `scripts/xianmu_mcp.py`（纯标准库，无第三方依赖）：

   ```bash
   # 列出全部工具
   python scripts/xianmu_mcp.py tools

   # 调用工具：参数是一个 JSON 对象；参数含引号时建议从 stdin 传入
   python scripts/xianmu_mcp.py call get_site_overview '{}'
   python scripts/xianmu_mcp.py call get_comic '{"comic_id":"17763369151688","page_limit":5}'
   echo '{"comic_id":"17763369151688"}' | python scripts/xianmu_mcp.py call get_comic -
   ```

   脚本自动完成 MCP 握手/会话/响应解析（含 SSE），工具结果文本打印到 stdout，诊断信息走 stderr。
   退出码：0 成功；1 传输/协议/配置错误（stderr 有原因，401/429 已翻译成人话）；2 工具业务错误
   （`isError=true`，stderr/stdout 有服务端原因）。环境变量：`XIANMU_API_KEY`（必填）、
   `XIANMU_MCP_URL`（默认生产端点，勿随意覆盖）。
3. **curl 兜底**（无 Python 环境时）：按 `references/api.md` 手写 JSON-RPC 三步握手。

## 工具路由表（11 个）

内容层 5 个（每日额度内免费：普通 100 次/Key、VIP 300 次）：

| 用户意图 | 工具 | 关键点 |
|---|---|---|
| 站点有什么/有哪些类目 | `get_site_overview` | 无参数；返回统计 + 全部标签目录（105 个） |
| 找书/按标签逛/看榜单/相关推荐 | `browse_comics` | 四模式互斥：`query` 搜索 / `tag` 标签 / `ranking`(favorites\|rating\|hot) / `related_to`，一次只传一个 |
| 看某本书/翻页/看单页 | `get_comic` | `comic_id` 必填；未解锁自动给前 20 页预览+解锁报价+梗概语音；解锁后给全量页图+逐页朗读+文字；`page=N` 单页三件套 |
| 找角色/某书角色表/随机来一个 | `search_characters` | `query`/`character_ids`/`comic_id`/`random` 互斥；基础档案免费 |
| 和角色聊天 | `chat_with_character` | `character_id`+`message`(≤500 字)；免解锁，1 积分/条 |

计费层 6 个（全部免费调用、不占每日额度）：

| 用户意图 | 工具 | 关键点 |
|---|---|---|
| 查积分/VIP/书架/套餐 | `get_account` | 返回 `packages`（积分套餐）、`vip_plans`（VIP 套餐）、`unlocked_comics` |
| 解锁这本书 | `unlock_comic` | `method='alipay'` 返回订单码（免费会员唯一通道）；`method='points'` VIP 专享扣分 |
| 付了吗/到账没 | `check_payment` | 传 `order_no` 轮询；不传查最近一笔待确认单；自动履约 |
| 充积分 | `recharge_points` | `package_key` 如 p100/p500/p1000；返回订单码 |
| 开通/续费 VIP | `purchase_vip` | `plan_key='monthly'`(¥9.9) / `'quarterly'`(¥29.7)；返回订单码 |
| 额度用完了想立刻继续 | `reset_daily_quota` | 扣 100 积分立即清零今日计数 |

工具入参/返回字段的完整说明见 `references/tools.md`；各业务流程的逐步操作与对客话术见
`references/workflows.md`。

## 价格与额度口径（转述给用户时必须准确）

- **免费层**：所有内容工具解锁态自适应——未解锁也能看基础信息、前 20 页预览、听梗概语音；
  4 个查询工具每日 100 次/Key（VIP 300 次），次日自动恢复
- **按部买断**：¥1.9 / ¥2.9 / ¥4.9（按页数分档），解锁后永久可读，**无订阅**
- **AI 角色对话**：1 积分/条，免解锁，与官网同价同账本
- **积分**：100 分 = ¥1 平价直充（p100/p500/p1000/p3000/p5000），VIP 充值额外加赠 10%；
  积分解锁/下载高清资源包为 VIP 专享
- **VIP**：月卡 ¥9.9（赠 1200 积分）/ 季卡 ¥29.7（赠 3600 积分），支付到账即赠分并顺延有效期，
  **无自动续费**；权益：每日额度 300 次、每月赠 1200 积分、充值加赠 10%、积分解锁/下载专享、
  签到双倍积分
- **收款通道**：支付宝订单码是唯一线上收款方式；支付结果一律用 `check_payment` 轮询确认

## 示例提示词（题材多样，均可在真实内容上命中）

把用户的自然表达路由到对应工具组合：

| 示例 | 主工具 |
|---|---|
| "帮我找几本聊斋志异题材的连环画，挑一本讲讲梗概，再放一段梗概语音" | browse_comics → get_comic |
| "《画皮》讲的是什么？先给我看前几页" | get_comic（画皮 comic_id=17763369151688） |
| "我想和聂小倩聊聊她的故事" | search_characters("聂小倩") → chat_with_character（character_id=9574） |
| "找评分最高的岳飞题材连环画，让岳飞给我讲讲精忠报国" | browse_comics → search_characters（岳飞 character_id=68） → chat_with_character |
| "白蛇传这本书值不值得解锁？给我看看前面的预览和报价" | browse_comics(query=白蛇传) → get_comic |
| "你们一共有多少部连环画？收藏榜前十是哪些？" | get_site_overview / browse_comics(ranking=favorites) |
| "《画皮》不错，帮我解锁完整版，我用支付宝扫码付" | unlock_comic(method='alipay') → check_payment |
| "VIP 有什么权益？直接帮我用月卡开通" | get_account（看 vip_plans） → purchase_vip('monthly') → check_payment |

## 智能体行为准则

- **付费引导照转述**：响应里的 `unlock_quote` / `unlock_hint` / `nudge` / `preview_note` /
  `how_to_unlock` / `next_step` / `resource_pack` 字段是给用户看的话术与数字（已读进度、单价锚、
  推荐方式），请转述或按其推荐动作推进，不要丢弃、不要编造替代。
- **二维码必须内嵌显示**：`qr_code_image` 是服务端生成的正方形 PNG data URI，直接放进
  `<img src="…">` 即可 1:1 显示；严禁把它存成本地文件再用路径引用，`qr_code` 链接只作兜底。
- **支付闭环**：下单后主动（或提示用户要求时）用 `check_payment(order_no=…)` 轮询，通常数秒到账；
  `paid=true` 后按返回的 `next_step` 继续（解锁交付/积分入账/VIP 生效）。
- **解锁后进入"漫剧模式"**：已解锁的 `get_comic` 返回逐页 `audio_url` 与 `reading_guide`——
  按指引逐页展示图片并自动播放朗读，翻页播讲，这是本服务最核心的体验。
- **错误处理**：脚本退出码 1 时先读 stderr（401=Key 失效→引导重建；429=额度尽→推荐
  `reset_daily_quota` 或次日再用；404=URL/会话问题）；退出码 2 为工具业务错误（如积分不足，
  服务端已给出差额与套餐引导，照转述即可）。
- **内容合规红线**：书页图片与音频仅供即时展示/播放，禁止批量下载、转存或二次分发；
  给用户展示时使用响应中的站点直链，不要转存代理。
- **comic_id 口径**：对外一律用官网 htmlname（如 `17763369151688`），结果都带 `web_url`
  可引导用户去官网详情页；入参也兼容内部数字 ID。

## 参考文件

- `references/tools.md` — 11 个工具的完整入参/返回字段/互斥规则与示例
- `references/workflows.md` — Key 开通、找书阅读、解锁支付、充值、VIP、角色对话全流程与对客话术
- `references/api.md` — MCP 直连协议细节、curl 兜底、错误语义与排错
