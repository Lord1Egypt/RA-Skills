# pushplus 开放接口参考

文档版本：**V1.20**（[官方文档](https://www.pushplus.plus/doc/guide/openApi.html)）  
在线调试：https://api.pushplus.plus/doc-6905395

本文件供智能体在需要查询发送结果、管理群组/好友/黑名单/渠道/ClawBot/新消息ClawBot/QQ 机器人、配置设置/消息规则等场景时按需阅读。日常发消息请优先使用 [SKILL.md](SKILL.md) 中的 `/send` 与 `/batchSend`（用户 token，无需 AccessKey）。

## 何时使用开放接口

| 场景 | 用开放接口？ | 说明 |
|------|-------------|------|
| 发通知 / 告警 | 否 | 用 `/send` 或 `/batchSend` + `PUSHPLUS_TOKEN` |
| 查发送是否成功 | 是 | `GET .../message/sendMessageResult` |
| 列消息、删消息 | 是 | 消息接口 |
| 管群组 / 好友 / 黑名单 / webhook | 是 | 对应模块 |
| 绑定 ClawBot | 是 | 微信 ClawBot 接口 |
| 绑定新消息ClawBot | 是 | 新消息ClawBot 接口（`/open/cmcc`） |
| 绑定 QQ 机器人 / 添加自有机器人 / 管群配置 | 是 | QQ 机器人接口 |
| 上传图片 | 是 | 图片服务 |
| 配置消息规则 / 看触发记录 | 是 | 消息规则接口（需会员） |

## 认证（AccessKey）

开放接口权限较高，默认禁用。用户须在开发设置中开启，并配置 `secretKey` 与安全 IP。

### 获取 AccessKey

```bash
curl -s -X POST "https://www.pushplus.plus/api/common/openApi/getAccessKey" \
  -H "Content-Type: application/json" \
  -d '{"token":"USER_TOKEN","secretKey":"SECRET_KEY"}'
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `token` | 是 | **用户 token**（不支持消息 token） |
| `secretKey` | 是 | 用户密钥 |

响应：

```json
{"code":200,"msg":"请求成功","data":{"accessKey":"...","expiresIn":7200}}
```

### 调用规则

1. 后续请求 Header 必须带：`access-key: <accessKey>`
2. 有效期约 7200 秒；重复获取会使旧 key 失效；刷新有约 5 分钟新旧并存窗口
3. 建议中控统一刷新，避免多端互相覆盖
4. 请求 IP 须在安全 IP 列表内，否则 403
5. 凭证获取：优先环境变量 `PUSHPLUS_TOKEN` + `PUSHPLUS_SECRET_KEY`；缺失则询问用户。**禁止**在输出中展示完整 secretKey / accessKey

凭证优先级：
1. 对话中用户提供
2. 环境变量 `PUSHPLUS_TOKEN`、`PUSHPLUS_SECRET_KEY`（可选已有 `PUSHPLUS_ACCESS_KEY`）
3. `.env` 中**仅提取**上述变量行

通用响应：`{"code":200,"msg":"...","data":...}`；`code!=200` 时根据 `msg` 排查。

---

## 一、消息接口

基址：`https://www.pushplus.plus/api/open/message`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 消息列表 | POST | `/list` | body: `current`, `pageSize`（最大 50） |
| 查询发送结果 | GET | `/sendMessageResult` | query: `shortCode`（必填） |
| 删除消息 | DELETE | `/deleteMessage` | query: `shortCode`（必填；不可撤销） |
| 消息详情 HTML | GET | `https://www.pushplus.plus/shortMessage/{shortCode}` | 返回 HTML，无需 access-key |

### 查询发送结果（发消息后常用）

```bash
curl -s "https://www.pushplus.plus/api/open/message/sendMessageResult?shortCode=SHORT_CODE" \
  -H "access-key: ACCESS_KEY"
```

| data 字段 | 说明 |
|-----------|------|
| `status` | `0` 未投递 / `1` 发送中 / `2` 已发送 / `3` 发送失败 |
| `errorMessage` | 失败原因 |
| `updateTime` | 更新时间 |

消息列表项：`shortCode`, `title`, `channel`, `messageType`（1 一对一 / 2 一对多）, `topicName`, `updateTime`。

---

## 二、用户接口

基址：`https://www.pushplus.plus/api/open/user`

| 能力 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 获取用户 token | GET | `/token` | data 为用户 token 字符串 |
| 个人资料 | GET | `/myInfo` | 含积分、实名、会员等 |
| 解封剩余时间 | GET | `/userLimitTime` | `sendLimit`: 1 无限制 / 2 短期 / 3 永久 |
| 当日请求次数 | GET | `/sendCount` | 各渠道当日调用次数，含 `qqBotSendCount`、`cmccSendCount` |

`myInfo` 要点：`verifyStatus`（0 未实名 / 1 已实名）、`points`、`vipInfo.isVip` / `vipInfo.lastDay`、`token`、`phoneNumber`、`email`。

---

## 三、消息 token 接口

基址：`https://www.pushplus.plus/api/open/token`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 列表 | POST | `/list` | `current`, `pageSize` |
| 新增 | POST | `/add` | `name`（必填）, `expireTime`（默认 2999-12-31） |
| 修改 | POST | `/edit` | `id`, `name`, `expireTime` |
| 删除 | DELETE | `/deleteToken` | query: `id` |
| 下拉列表 | GET | `/selectTokenList` | query: `type`：0 全部 / 1 未配默认渠道 |

新增成功时 `data` 为新建的消息 token 字符串。

---

## 四、群组接口

基址：`https://www.pushplus.plus/api/open/topic`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 列表 | POST | `/list` | `params.topicType`：0 我创建的 / 1 我加入的 |
| 我创建的详情 | GET | `/detail` | `topicId` |
| 我加入的详情 | GET | `/joinTopicDetail` | `topicId` |
| 新增 | POST | `/add` | `topicCode`, `topicName`, `contact`, `introduction` 必填 |
| 修改 | POST | `/editTopic` | `topic`（群组编号）, `topicCode`, `topicName` 必填 |
| 二维码 | GET | `/qrCode` | `topicId`；`second` 默认 604800（最长 30 天）；`scanCount` 默认 -1（无限） |
| 退出 | GET | `/exitTopic` | `topicId` |
| 删除 | GET | `/delete` | `topicId` |
| 积分群上下架 | POST | `/isOpen` | `topic`, `isOpen`（1 上架 / 0 下架） |

`topicType`：0 普通 / 1 积分 / 2 公开。列表含 `topicCode`（发送消息时 `topic` 参数用此编码）。

---

## 五、群组用户接口

基址：`https://www.pushplus.plus/api/open/topicUser`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 订阅人列表 | POST | `/subscriberList` | `params.topicId` 必填 |
| 删除用户 | POST | `/deleteTopicUser` | query: `topicRelationId`（订阅人列表中的 `id`） |
| 修改备注 | POST | `/editRemark` | `id`, `remark`（≤20 字） |
| 加入黑名单 | POST | `/addBlacklist` | query: `topicRelationId`（订阅人列表中的 `id`） |
| 黑名单列表 | POST | `/blacklistList` | `params.topicId` 必填；分页 |
| 解除黑名单 | POST | `/removeBlacklist` | query: `id`（**黑名单列表**中的 `id`，不是订阅人 `id`） |

拉黑说明：
- 加入后将该用户**移出群组**，且对方无法再加入该群组
- **积分群组不支持**黑名单
- 不能将自己加入黑名单
- 解除后**不会自动恢复订阅**，对方可重新加入

```bash
# 拉黑（topicRelationId = 订阅人列表 id）
curl -s -X POST "https://www.pushplus.plus/api/open/topicUser/addBlacklist?topicRelationId=1" \
  -H "access-key: ACCESS_KEY"

# 黑名单列表
curl -s -X POST "https://www.pushplus.plus/api/open/topicUser/blacklistList" \
  -H "Content-Type: application/json" \
  -H "access-key: ACCESS_KEY" \
  -d '{"current":1,"pageSize":20,"params":{"topicId":1}}'

# 解除（id = 黑名单列表 id）
curl -s -X POST "https://www.pushplus.plus/api/open/topicUser/removeBlacklist?id=1" \
  -H "access-key: ACCESS_KEY"
```

黑名单列表项：`id`（解除时用）、`userId`、`nickName`、`openId`、`headImgUrl`、`createTime`（拉黑时间）。

---

## 六、渠道配置接口

### Webhook

基址：`https://www.pushplus.plus/api/open/webhook`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 列表 | POST | `/list` | 分页 |
| 详情 | GET | `/detail` | `webhookId` |
| 新增 | POST | `/add` | `webhookCode`, `webhookName`, `webhookType`, `webhookUrl` |
| 修改 | POST | `/edit` | 另加 `id` |

`webhookType`：1 企微机器人 / 2 钉钉 / 3 飞书 / 4 Server酱 / 50 bark / 6 企微应用 / 7 腾讯轻联 / 8 IFTTT / 9 集简云 / 10 Gotify / 11 WxPusher / 12 自定义。

自定义类型（12）可额外传 `httpMethod`、`headers`、`body`。

发送消息时 `/send` 的 `option` 填列表中的 `webhookCode`。

### 其他渠道只读列表

| 能力 | 方法 | 路径 |
|------|------|------|
| 微信公众号列表 | POST | `/api/open/mp/list` |
| 企业微信应用列表 | POST | `/api/open/cp/list` |
| 邮箱渠道列表 | POST | `/api/open/mail/list` |
| 邮箱详情 | GET | `/api/open/mail/detail?mailId=` |

企微 `cpCode`、邮箱 `mailCode` 可作为 `/send` 的 `option`。QQ 机器人的群配置（`qqCode`）见「九、QQ 机器人接口」。新消息ClawBot 不需要 `option`，见「八、新消息ClawBot 接口」。

---

## 七、微信 ClawBot 接口

基址：`https://www.pushplus.plus/api/open/clawBot`

| 能力 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 获取二维码 | GET | `/getBotQrcode` | 返回 `url`, `qrcode` |
| 扫码结果 | GET | `/getQrcodeStatus` | query: **`qrcode`**（二维码编号） |
| 绑定详情 | GET | `/botInfo` | `createTime`, `haveContextToken` |
| 解绑 | GET | `/unbind` | 无参数 |
| 获取发送消息 | GET | `/getMsg` | 数组：`type` 1 文字 / 3 语音；`text` 内容 |

绑定流程：调用 `/getBotQrcode` → 展示 `url` 给用户扫码 → 轮询 `/getQrcodeStatus?qrcode=` → 成功后可用 `/send` 且 `channel=clawbot`。

---

## 八、新消息ClawBot 接口

基址：`https://www.pushplus.plus/api/open/cmcc`

需先在手机 5G 消息的「新消息ClawBot」应用号中获取 Channel API Key，再调用绑定接口。发送消息时 `channel` 传 `cmcc`，不填 `option`。仅支持中国移动用户。页面操作见 [新消息ClawBot渠道使用说明](https://www.pushplus.plus/doc/channel/cmcc.html)。

| 能力 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 绑定 | POST | `/bind` | body: `apiKey`（必填，须以 `ak_` 或 `app_` 开头） |
| 查询绑定状态 | GET | `/info` | 无参数 |
| 解绑 | GET | `/unbind` | 无参数（不可逆，需确认） |
| 发送测试消息 | GET | `/test` | 无参数；未绑定返回「未绑定新消息ClawBot」 |

`info` 返回：`bound`（0 未绑定 / 1 已绑定）、`apiKeyMasked`（脱敏后的 API Key）、`createTime`（绑定时间）。

```bash
# 1. 绑定（apiKey 来自手机 5G 消息「新消息ClawBot」应用号）
curl -s -X POST "https://www.pushplus.plus/api/open/cmcc/bind" \
  -H "Content-Type: application/json" \
  -H "access-key: ACCESS_KEY" \
  -d '{"apiKey":"ak_xxxxxxxxxxxxxxxx"}'

# 2. 查询绑定状态，bound=1 即可用 channel=cmcc 发消息
curl -s "https://www.pushplus.plus/api/open/cmcc/info" -H "access-key: ACCESS_KEY"

# 3. 发送测试消息，到手机应用号中确认
curl -s "https://www.pushplus.plus/api/open/cmcc/test" -H "access-key: ACCESS_KEY"
```

绑定流程：用户从手机 5G 消息应用号复制 Channel API Key → `/bind` → `/info` 确认 `bound=1` → `/send` 且 `channel=cmcc`（建议 `template=txt`）。**不要在输出中展示完整 apiKey**。

---

## 九、QQ 机器人接口

基址：`https://www.pushplus.plus/api/open/qqBot`

除 pushplus 官方机器人外，用户可添加自己在 QQ 开放平台创建的机器人（自有机器人；普通用户 1 个，会员 5 个）。一个账号可绑定多个机器人，其中一个为**默认机器人**：`/send` 且 `channel=qq` 不填 `option` 时由默认机器人发给自己。下表中的 `botAppId` 取自 `/myBots` 返回的 `bots[].botAppId`。

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 获取绑定链接 | GET | `/getBindLink` | query: `refresh`（可选，true 使旧绑定码失效并重新生成）、`botAppId`（可选，不填为官方机器人；绑定自有机器人时必填） |
| 查询绑定状态 | GET | `/botInfo` | query: `botAppId`（可选，不填为默认机器人） |
| 解绑 | GET | `/unbind` | query: `botAppId`（可选，不填解绑官方机器人；需确认） |
| 已加入的 QQ 群列表 | GET | `/groupList` | query: `botAppId`（可选，不填返回全部） |
| 配置列表 | POST | `/list` | 分页 `current`, `pageSize` |
| 新增配置 | POST | `/add` | `qqName`, `qqCode` 必填；`sendType`（1 发给自己 / 2 发到群，默认 2）；`sendType=2` 需 `qqGroupId`；`sendType=1` 需 `botAppId` |
| 修改配置 | POST | `/edit` | `id`, `qqName`, `qqCode`（传原值，不可改）；`sendType`、`qqGroupId`、`botAppId` 同新增 |
| 删除配置 | DELETE | `/delete` | query: `id`（需确认） |
| 我的机器人列表 | GET | `/myBots` | 无参数 |
| 校验自有机器人凭证 | POST | `/customBot/preview` | `botAppId`, `appSecret`（仅校验不保存） |
| 添加自有机器人 | POST | `/customBot/add` | `botAppId`, `appSecret` |
| 修改自有机器人 AppSecret | POST | `/customBot/edit` | `botAppId`, `appSecret`（新值） |
| 刷新自有机器人头像昵称 | GET | `/customBot/refresh` | query: `botAppId` |
| 删除自有机器人 | DELETE | `/customBot/delete` | query: `botAppId`（会连带删除其绑定、群和配置；需确认） |
| 设置默认机器人 | GET | `/setDefault` | query: `botAppId`（须已绑定） |

`getBindLink` 返回：`url`（带参分享链接，用于生成二维码；已绑定该机器人时可能为空）、`bindCode`（绑定码，已是好友时需私聊发给机器人；认领 QQ 群也用此码）、`expireSeconds`（默认 300）、`botAppId`、`botName`、`botAvatar`、`botType`（1 官方 / 2 自有）。

`botInfo` 返回：`isBind`（0 未绑定 / 1 已绑定）、`receiveStatus`（1 可接收 / 0 用户已关闭单聊接收）、`createTime`、`botInfo{botId, username, avatar, botAppId, shareUrl, botType}`（`shareUrl` 可用于拉机器人进群）。`/customBot/preview` 返回的也是这个 `botInfo` 结构。

`myBots` 返回：`bots[]`（`botAppId`、`botId`、`username`、`avatar`、`shareUrl`、`botType`、`isBind`、`receiveStatus`、`isDefault`、`bindTime`；官方在前、自有在后）、`customBotCount`、`customBotLimit`、`webhookUrl`（需在 QQ 开放平台配置的回调地址）、`serverIps`（需加入 QQ 开放平台 IP 白名单）、`events`（需订阅的事件）。

`groupList` 项：`id`（新增配置时作为 `qqGroupId`）、`groupOpenId`、`groupRemark`、`status`（1 在群 / 0 已退群 / 2 群消息接收关闭）、`groupName`、`groupFingerMemo`、`groupClassText`、`groupTags`、`groupMemberNum`、`createTime`。

配置列表项：`id`、`qqName`、`qqCode`（**发送消息时作为 `option`**）、`sendType`（1 发给自己 / 2 发到 QQ 群）、`qqGroupId`、`groupRemark`、`groupOpenId`、`groupName`、`botAppId`、`botName`、`botAvatar`、`updateTime`。

配置约束：只用默认机器人发给自己时无需配置；同一 QQ 群、同一机器人的“发给自己”均不可重复创建；`qqCode` 创建后不可修改（最多 32 字符，仅字母、数字、下划线、中划线）；`qqName` 最多 64 字符；发到群时目标群须允许机器人主动消息；发给自己时 `botAppId` 须已绑定。

```bash
# 1. 取绑定链接，把 url 生成二维码给用户扫，或让用户私聊发送 bindCode
curl -s "https://www.pushplus.plus/api/open/qqBot/getBindLink" \
  -H "access-key: ACCESS_KEY"

# 2. 轮询绑定状态，isBind=1 即可用 channel=qq 发消息
curl -s "https://www.pushplus.plus/api/open/qqBot/botInfo" -H "access-key: ACCESS_KEY"

# 3. 查已加入的群，取 id 作为 qqGroupId 建配置
curl -s "https://www.pushplus.plus/api/open/qqBot/groupList" -H "access-key: ACCESS_KEY"

curl -s -X POST "https://www.pushplus.plus/api/open/qqBot/add" \
  -H "Content-Type: application/json" \
  -H "access-key: ACCESS_KEY" \
  -d '{"qqName":"交流群推送","qqCode":"qqgroup","sendType":2,"qqGroupId":1}'
```

```bash
# 自有机器人：先 /myBots 拿 webhookUrl、serverIps、events，提示用户在 QQ 开放平台配置好
curl -s "https://www.pushplus.plus/api/open/qqBot/myBots" -H "access-key: ACCESS_KEY"

# 校验凭证（不保存），确认昵称头像后再添加
curl -s -X POST "https://www.pushplus.plus/api/open/qqBot/customBot/preview" \
  -H "Content-Type: application/json" -H "access-key: ACCESS_KEY" \
  -d '{"botAppId":"102xxxxxx","appSecret":"APP_SECRET"}'
curl -s -X POST "https://www.pushplus.plus/api/open/qqBot/customBot/add" \
  -H "Content-Type: application/json" -H "access-key: ACCESS_KEY" \
  -d '{"botAppId":"102xxxxxx","appSecret":"APP_SECRET"}'

# 绑定该机器人，轮询到 isBind=1
curl -s "https://www.pushplus.plus/api/open/qqBot/getBindLink?botAppId=102xxxxxx" -H "access-key: ACCESS_KEY"
curl -s "https://www.pushplus.plus/api/open/qqBot/botInfo?botAppId=102xxxxxx" -H "access-key: ACCESS_KEY"

# 二选一：设为默认（不填 option 即由它发）；或建“发给自己”配置，发送时 option=mybot
curl -s "https://www.pushplus.plus/api/open/qqBot/setDefault?botAppId=102xxxxxx" -H "access-key: ACCESS_KEY"
curl -s -X POST "https://www.pushplus.plus/api/open/qqBot/add" \
  -H "Content-Type: application/json" -H "access-key: ACCESS_KEY" \
  -d '{"qqName":"自有机器人私聊","qqCode":"mybot","sendType":1,"botAppId":"102xxxxxx"}'
```

绑定流程：`/getBindLink`（自有机器人带 `botAppId`）→ 用户扫码加机器人好友（已是好友则私聊发送 `bindCode`）→ 轮询 `/botInfo`（同样带 `botAppId`）直到 `isBind=1` → `/send` 且 `channel=qq`（不填 `option` 由默认机器人发给自己）。发到群还需：把机器人拉进群并允许主动消息 → `/groupList` 取群 `id` → `/add` 建配置 → 发送时 `option` 填 `qqCode`。

自有机器人接入：`/myBots` 取 `webhookUrl`、`serverIps`、`events` 让用户在 QQ 开放平台配置回调地址、IP 白名单与事件订阅 → `/customBot/preview` 校验 → `/customBot/add` → 按上面的绑定流程绑定 → `/setDefault` 或建 `sendType=1` 配置。**`appSecret` 属于敏感凭证，不要在输出中回显**；凭证校验失败多为 IP 白名单未配置。

---

## 十、功能设置接口

基址：`https://www.pushplus.plus/api/open/setting`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 默认配置列表 | POST | `/listUserDefault` | 分页 |
| 默认配置详情 | GET | `/detailUserDefault` | `id` |
| 新增默认配置 | POST | `/addUserDefault` | `channel`, `option`, `pre`, `tokenId`（用户令牌为 0） |
| 修改默认配置 | POST | `/editUserDefault` | 另加 `id` |
| 删除默认配置 | DELETE | `/deleteUserDefault` | query: `id` |
| 接收限制 | GET | `/changeRecevieLimit` | `recevieLimit`：0 全部 / 1 不接收（参数名按官方拼写） |
| 开/关发送 | GET | `/changeIsSend` | `isSend`：0 禁用 / 1 启用 |
| 打开方式 | GET | `/changeOpenMessageType` | `openMessageType`：0 H5 / 1 小程序 |
| 插件转发 | GET | `/extension` | `forward`：0 否 / 1 是（微信消息同步插件/桌面端） |

默认渠道 `channel`：`wechat` / `cp` / `webhook` / `mail` / `sms` / `voice` / `extension` / `clawbot` / `cmcc` / `qq`。

---

## 十一、好友功能接口

基址：`https://www.pushplus.plus/api/open/friend`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 个人二维码 | GET | `/getQrCode` | 可选 `appId`, `content`, `second`, `scanCount` |
| 好友列表 | POST | `/list` | 分页；项含 `token`（发好友消息用）、`friendId`（拉黑/删除用） |
| 删除好友 | GET | `/deleteFriend` | query: `friendId` |
| 修改备注 | POST | `/editRemark` | `id`（列表 `id`）, `remark` |
| 加入黑名单 | POST | `/addBlacklist` | query: `friendId`（好友列表中的 **`friendId`**，不是 `id`） |
| 黑名单列表 | POST | `/blacklistList` | 分页 |
| 解除黑名单 | POST | `/removeBlacklist` | query: `id`（**黑名单列表**中的 `id`，不是 `friendId`） |

发送好友消息：`/send` 的 `to` 填好友列表中的 `token`，勿与 `topic` 同填。

拉黑说明：
- 加入后将**解除双方好友关系**，对方无法再添加你
- 不能将自己加入黑名单；**仅可将已有好友**加入黑名单
- 解除后**不会自动恢复好友关系**，需重新扫码添加

```bash
# 拉黑（friendId = 好友列表 friendId）
curl -s -X POST "https://www.pushplus.plus/api/open/friend/addBlacklist?friendId=1" \
  -H "access-key: ACCESS_KEY"

# 黑名单列表
curl -s -X POST "https://www.pushplus.plus/api/open/friend/blacklistList" \
  -H "Content-Type: application/json" \
  -H "access-key: ACCESS_KEY" \
  -d '{"current":1,"pageSize":20}'

# 解除（id = 黑名单列表 id）
curl -s -X POST "https://www.pushplus.plus/api/open/friend/removeBlacklist?id=1" \
  -H "access-key: ACCESS_KEY"
```

黑名单列表项：`id`（解除时用）、`friendId`、`nickName`、`headImgUrl`、`createTime`（拉黑时间）。

---

## 十二、预处理信息接口（需会员）

基址：`https://www.pushplus.plus/api/open/pre`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 列表 | POST | `/list` | 分页 |
| 详情 | GET | `/detail` | `preId` |
| 新增 | POST | `/add` | `content`, `preName`, `preCode`, `contentType`（1=JS） |
| 修改 | POST | `/edit` | 另加 `id` |
| 删除 | DELETE | `/delete` | query: `preId` |
| 测试代码 | POST | `/test` | `content`, `contentType`, `message` |

发送时 `/send` 的 `pre` 填 `preCode`。

---

## 十三、图片服务接口

图片约 30 天有效；可主动删除。

| 能力 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 获取上传凭证 | GET | `/api/open/userImage/uploadToken` | 返回 `uploadToken`, `uploadUrl`, `expiresIn` 等 |
| 上传图片 | POST | 凭证中的 `uploadUrl` | multipart：`token`=`uploadToken`，`file`=图片；**无需** access-key |
| 图片列表 | POST | `/api/open/userImage/list` | 分页 |
| 删除图片 | DELETE | `/api/open/userImage/delete` | query: `id` |

上传成功响应（七牛表单）含 `url`、`thumbnail`；`errno=0` 表示成功。可将 `url` 用于消息 content / `icon`。

---

## 十四、消息规则接口（需会员）

开启后，消息接口和邮件推送（`{令牌}@yp9.cn`）会先走规则匹配，再按规则改写标题、内容、渠道后发送。单账号最多 20 条规则；单条最多 20 个模板变量、5 个发送目标。用法教程：[消息规则](https://www.pushplus.plus/doc/function/rule.html)。

基址：`https://www.pushplus.plus/api/open/forwardRule`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 列表 | POST | `/list` | 分页 |
| 详情 | GET | `/detail` | query: `ruleId` |
| 新增 | POST | `/add` | `ruleName` 必填；可选 tokenId/sourceType/condition/variables/targets 等 |
| 修改 | POST | `/edit` | 另加 `id`；会整体覆盖变量和发送目标 |
| 删除 | DELETE | `/delete` | query: `ruleId`（不可撤销） |
| 启用停用 | GET | `/changeStatus` | query: `ruleId`, `status`（1启用/0停用） |
| 测试 | POST | `/test` | 模拟请求，**不会真正发送** |
| 获取总开关 | GET | `/setting` | 无参数 |
| 设置总开关 | GET | `/setting` | query: `mode` |

触发记录基址：`https://www.pushplus.plus/api/open/forwardLog`

| 能力 | 方法 | 路径 | 关键参数 |
|------|------|------|----------|
| 列表 | POST | `/list` | 分页；`params.ruleId` / `params.matchResult` 可选 |
| 详情 | GET | `/detail` | query: `logId` |

### 枚举

| 字段 | 值 |
|------|----|
| `tokenId` | `-1` 全部令牌 / `0` 用户令牌 / `>0` 消息令牌 id |
| `sourceType` | `0` 全部 / `1` 消息接口 / `2` 邮件 |
| `status` | `1` 启用 / `0` 停用 |
| `mode` | `0` 关闭 / `1` 开启且未命中仍按默认推送 / `2` 开启且未命中不推送 |
| `matchResult` | `0` 条件不满足 / `1` 已转发 / `2` 频率限制 / `3` 不在触发时间段 / `4` 执行异常 |
| 变量 `sourceType` | `1` 请求头 / `2` Query / `3` 请求体 / `4` URL 路径 / `5` 主题（邮件） |
| `extractType` | `1` 序列化数据 / `2` 正则 / `3` JSONPath / `4` 原始全文 |

`mode` 为 1 或 2 时需开通会员，否则返回「消息规则需开通会员后才能开启」。

```bash
# 开启总开关（未命中仍按默认推送）
curl -s "https://www.pushplus.plus/api/open/forwardRule/setting?mode=1" \
  -H "access-key: ACCESS_KEY"

# 新增规则
curl -s -X POST "https://www.pushplus.plus/api/open/forwardRule/add" \
  -H "Content-Type: application/json" \
  -H "access-key: ACCESS_KEY" \
  -d '{"ruleName":"阿里云监控多渠道","tokenId":-1,"sourceType":1,"condition":{"logic":"and","items":[{"varName":"alertState","operator":"eq","value":"ALERT"}]},"titleTemplate":"{{alertName}}","variables":[{"varName":"alertName","sourceType":3,"extractType":1,"extractKey":"alertName"}],"targets":[{"channel":"wechat","messageType":"one"}]}'

# 测试（不发送）
curl -s -X POST "https://www.pushplus.plus/api/open/forwardRule/test" \
  -H "Content-Type: application/json" \
  -H "access-key: ACCESS_KEY" \
  -d '{"sourceType":1,"body":"{\"alertState\":\"ALERT\",\"alertName\":\"ECS-内存\"}","conditionExpr":"alertState == '\''ALERT'\''","titleTemplate":"{{alertName}}","variables":[{"varName":"alertName","sourceType":3,"extractType":1,"extractKey":"alertName"},{"varName":"alertState","sourceType":3,"extractType":1,"extractKey":"alertState"}]}'

# 触发记录
curl -s -X POST "https://www.pushplus.plus/api/open/forwardLog/list" \
  -H "Content-Type: application/json" \
  -H "access-key: ACCESS_KEY" \
  -d '{"current":1,"pageSize":20,"params":{"matchResult":1}}'
```

---

## Agent 调用要点

1. **先发消息用 token，再查结果用 AccessKey**：`/send` 返回 `shortCode` → 开放接口查 `status`。
2. **破坏性操作**（删消息、删群组、删好友、删 QQ 群配置、删消息规则、拉黑好友/订阅人、解绑 ClawBot / 新消息ClawBot / QQ 机器人、删除自有 QQ 机器人、关发送）必须先向用户确认。拉黑会解除关系且对方无法再加入/添加，解除黑名单也不会自动恢复。
3. **分页**：多数列表 `pageSize` 最大 50。
4. **脱敏**：输出中遮盖 token、secretKey、accessKey、webhookUrl、邮箱密码等。
5. 完整字段与示例见 [开放接口文档](https://www.pushplus.plus/doc/guide/openApi.html)；发送参数见 [消息接口文档](https://www.pushplus.plus/doc/guide/api.html)。
