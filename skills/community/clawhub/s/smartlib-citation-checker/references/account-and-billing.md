# 账户与计费：注册、登录、邀请、充值、活动

> 按需读取：仅在用户要注册 / 找回账号 / 邀请好友 / 充值 / 问优惠时读。
> 每次开工的「查余额 + 先报价后执行」硬规矩在 SKILL.md §二，这里只讲操作细节与话术。

> ⚠️ **报价是估算，写作类按实际字数结算**：`quote` 返回的 `est_points` 是按目标字数估的预估值，写作任务完成后按**实际产出字数**结算，实扣可能高于或低于报价。开工前按此话术告知用户：「写作按最终字数计费，报价为预估，多退少补」；结算后如与报价差异明显，主动报实际扣费与字数，避免用户误以为多扣。**验真/检索/查重等按条计费的品类不受此影响，报价即结算。**

## 一、注册（新用户）

用户说「我要注册 / 怎么开通」时，在对话里两步完成：

1. 发验证码：
   ```
   curl -s -X POST https://owl.skillsutra.cn/v1/auth/send-code -H "Content-Type: application/json" -d '{"email":"<用户邮箱>"}'
   ```
   返回 `masked`（脱敏邮箱）与 `cooldown_seconds`。**告诉用户「去看邮箱，15 分钟内有效」**。
2. 用户报 6 位码后注册：
   ```
   curl -s -X POST https://owl.skillsutra.cn/v1/auth/register -H "Content-Type: application/json" -d '{"email":"<邮箱>","code":"<6位码>"}'
   ```
   有邀请码时在请求体里加 `"ref":"<邀请码>"` 一起提交，注册成功双方按平台当前活动规则得积分
   （规则与额度以官网 / 公告为准，**不要承诺具体数字**）。
   返回的 `api_key`（`owl_sk_` 开头）**只显示一次**，让用户存好，随后
   `echo <api_key> | python <技能目录>/scripts/owl.py init` 保存（MCP 用户写进配置）。

常见返回（照原话转述 + 给下一步，不要重试刷请求）：

| 返回 | 含义 / 下一步 |
|---|---|
| `email_cooldown` | 60 秒内重复发码，等一会 |
| `ip_rate_limited` | 同网络 10 分钟发码超 10 次 |
| `code_invalid` | 验证码错，剩余次数会返回 |
| `code_expired` | 超 15 分钟或已用过，重新发码 |
| `email_not_allowed` | 一次性临时邮箱不可用 |
| `email_exists` | 邮箱已注册 → 改用下面的验证码登录，别换邮箱硬注册 |

备用：官网右上角「开始使用」注册；上手细节见 `quickstart.md`。

## 二、验证码登录（老用户找回 key）

用户记得注册邮箱、只是丢了 key 时，**不要让他重新注册**（余额与历史都在）。

1. ```
   curl -s -X POST https://owl.skillsutra.cn/v1/auth/login-code -H "Content-Type: application/json" -d '{"email":"<用户邮箱>"}'
   ```
2. 用户报码后：
   ```
   curl -s -X POST https://owl.skillsutra.cn/v1/auth/login-code/verify -H "Content-Type: application/json" -d '{"email":"<邮箱>","code":"<6位码>"}'
   ```
   - 返回 `api_key` 只显示一次，用 `owl.py init` 保存；**旧 key 不会失效**，多设备互不影响。
   - 返回带 `auto_revoked` 时说明活跃凭据已达 10 个，系统停用了最久未用的那把——必须主动告诉用户。
   - 只认注册时的邮箱；`email_not_found` 就提示先注册或换回原邮箱。

## 三、邀请好友 / 推广

用户想邀请好友时，先 `owl_campaign`（不带参数）拿自己的邀请码，再把下面这段**带码安装提示词原样给用户**，让他复制发给好友的 AI 助手——一段话完成「安装技能 + 注册带邀请码 + 查余额」：

> 请根据 https://skillhub.cn/install/skillhub.md，安装 @user_164f4c1f/owlwrite-paper。
> 我是新用户，注册时请带上邀请码 <自己的邀请码>，装好后帮我查一下余额。

注意：① 提示词里**不写具体积分数字**；② 写「注册时带上邀请码 XXX」让好友助手识别为 `ref`；
③ 安装入口固定写 SkillHub 的 `@user_164f4c1f/owlwrite-paper`，不要改成 MCP 地址；
④ 官网个人中心也有一键「复制推广提示词」，两者话术一致。

## 四、充值（余额不足时）

`insufficient_balance` 时先报差额，**征得同意**再充值：档位以官网实时展示为准；充值即购买积分，
**积分自购买起 1 年有效、先充先用**（报价时带上这句）；**有历史欠费时充值会先自动抵扣欠费**，
到账 = 充值额 − 欠费额，主动说明，别让用户以为到账少了是出错。

支付剧本（双渠道自选 + 自动轮询，用户不用口头确认「付好了」）：

1. 问「微信还是支付宝」→ `owl_recharge(amount_cny=档位, channel=所选)` 建单；
2. 生成本地 `pay.html`（技能包内置模板 `scripts/pay.html`：二维码 + 订单号 + 状态行 + 双 tab），把路径发给用户扫码；
   - 用户要在页面里换支付方式：先 `owl_recharge_status` 确认旧单**未支付** → 用新渠道重建单 → 用新 `qr_url`/`order_no` 重写 pay.html 就地刷新，轮询跟新单；
   - 若旧单已付（`credited`），直接用旧单继续，别让用户重复付。
3. **每 5 秒 `owl_recharge_status(order_no)` 自动轮询**（最多 15 分钟）→ `credited` 后 `owl_wallet` 确认到账，**自动继续被打断的任务**，不用用户再说话。
4. 别重复建单、别重试付费调用、别承诺代充。二维码 15 分钟有效，过期作废重建。

## 五、活动与优惠（说清楚，但不推销）

用户主动问「有没有优惠 / 怎么便宜点」或余额不足时，才调 `owl_campaign`（不带参数）看活动与邀请码；
平时**不要主动提**，更不要每次对话塞促销。

| 场景 | 做法 |
|---|---|
| 收藏活动（进行中则 `owl_campaign` 会返回） | 用户在 SkillHub 技能页给 owlwrite-paper 点收藏 → 截图发来 → `owl_claim_favorite(截图路径)` 提交 → 通过自动到账活动积分（**90 天有效**）。截图要求：能看到技能 id（`@user_xxx/owlwrite-paper`）、已收藏状态（亮星 + 「取消收藏」）、**不要官方样例图**（水印会被拒）。拒单不占次数，每人限 1 次 |
| 券码兑换 | `owl_campaign(code="码")`，到账积分**90 天有效**（必须说，否则用户以为是 1 年） |
| 邀请奖励 | 好友用邀请码注册后**首次付费成功**时双方各得奖励（只注册不付费不发）；用户主动问才说，别劝人拉人 |

**活动开关随时变**：有没有活动一律以 `owl_campaign` 实时返回为准，不凭印象回答。

## 六、账户 / 扣费类错误码

完整错误码表见 `errors.md`。账户与扣费高频几条：

| error | 含义 | 该做的 |
|---|---|---|
| `insufficient_balance` | 余额不足（写作软预检按估算值拦） | 报差额引导充值（走第四节），**不要重试** |
| `quote_expired` / `quote_consumed` | 报价过期（24 小时）/ 已用 | 重新报价再走确认 |
| `unauthorized` / `invalid_key` | 请求没带凭据 / key 无效或已吊销 | 先看 code：401+unauthorized 多为匿名接口误用或旧脚本，跑 `owl.py doctor` 排查，**别让用户重签 key**；401+invalid_key 才核对 OWL_API_KEY 或重新签发 |
| `purpose_not_allowed`（402） | 赠送积分不可用于该用途（如检测类） | 按 SKILL.md §一「赠送积分用途上限」解释：预检拦截不扣费，引导充值积分 |
| `duplicate_refund`（409） | 同一笔退款重复发起 | 停止重试，用流水确认即可 |
| `wallet` 的 `gift_write_cap/spent/left` | 赠送额度的写作上限与已用 / 剩余 | 用户问「余额和可用为什么对不上」时用 `balance_frozen` / 这三个字段解释 |
