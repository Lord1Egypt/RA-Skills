# 全生命周期坑（从零到发布）

本文件记录「搭建 + 业务 + 提审发布」层的坑。**部署层**的坑（tcb 建集合、
`fn invoke` Namespace bug、上传 IP 白名单、IPv6、trial env 区域）在
`wechat-miniprogram-cloudbase-deploy` skill 的 `references/pitfalls.md`，两套互补、不重复。

## 坑 1：集合清单漏一个 → `collection not exists`

**现象**：`collection.get:fail -502005 database collection not exists: user_stats`。

**根因**：代码里 `stats.js` 用了第 8 个集合 `user_stats`，但只建了 7 个集合。
云数据库集合不会自动创建（SDK 的 `.add()` 在集合不存在时会报错，不会隐式建）。

**教训**：**集合清单必须与代码实际用到的集合一一核对**。两个解法：
1. 写一个 `seed` 云函数，用 `ensureCollection` 遍历 ALL_COLLECTIONS 幂等建集合；
2. 更好的根治：**去掉多余的缓存集合**，统计类数据从事实表实时算（见 architecture.md 模式 3），
   从源头上减少集合数量，也就减少了「漏建」和「缓存不一致」两类坑。

## 坑 2：`用户不存在`——登录建号的时序竞争

**现象**：模拟器报 `MiniProgramError 用户不存在`，但通道（callFunction）是通的。

**根因**：`me` 页面在 `login` 云函数建号**之前**就请求了 `/api/users/me`。
`app.js` 的 `api.login()` 是异步的，页面 `onLoad` 的 `me()` 可能先跑，此时 `users`
集合里还没有这个 openid，返回「用户不存在」。

**解法**：`me()` 查不到用户时**幂等补建号**（含自动加入公开数据），并 try/catch 里
重查兜底并发（见 architecture.md 模式 1）。同理 `login` 云函数本身也要幂等建号。

**验证陷阱**：`tcb fn invoke api` 时没有 `OPENID`（`cloud.getWXContext()` 返回空），
`where({openid: undefined})` 单字段查询会抛「查询参数对象值不能均为 undefined」，
所以**无法用 tcb 命令行验证建号逻辑**，必须在真实小程序/模拟器里验。

## 坑 3：定时触发器写在 cloudbaserc.json 里没用

**现象**：`dailyPush` 每天 20:00 该触发却从不触发，但函数本身部署成功了。

**根因**：触发器只写在了 `cloudbaserc.json`，而云函数**自己的 `config.json` 里没有
`triggers`**。定时触发器的真正生效位置是函数目录的 `config.json`。

**解法**：`cloudfunctions/<fn>/config.json` 里写：
```json
{
  "permissions": { "openapi": ["subscribeMessage.send"] },
  "triggers": [{ "name": "dailyPushTimer", "type": "timer", "config": "0 0 20 * * * *" }]
}
```
然后 `tcb fn deploy <fn> --force` 重部署，再用 `tcb api scf ListTriggers` 确认
（注意：`tcb fn trigger` 只有 create/delete 没有 list 子命令）。

## 坑 4：订阅消息模板 ID 与 AppID 强绑定

**现象**：换了 AppID 后，旧模板 ID 调用 `subscribeMessage.send` 静默失败。

**根因**：订阅消息模板是**按 AppID 申请的**，换了 AppID，旧模板 `_v-Xwe-...` 就失效了。

**解法**：换 AppID 后，去新 AppID 后台 → 功能 → 订阅消息 → 公共模板库重新申请模板，
拿到新 ID 后**同时改两处**：
- `miniprogram/utils/config.js` 的 `SUBSCRIBE_TEMPLATE_ID`（前端请求授权用）
- `cloudfunctions/dailyPush/index.js` 的 `TEMPLATE_ID`（后端发送用）

改完要**重传前端 + 重部署 dailyPush** 双端都更新。

## 坑 5：订阅消息字段名必须与模板关键词顺序一致

**现象**：用户开了提醒，但 20:00 收不到推送，且**没有任何报错**（静默失败）。

**根因**：`subscribeMessage.send` 的 `data` 字段名（如 `thing1`/`time2`）必须与你
在后台申请的模板的**关键词类型和顺序**严格一一对应，否则微信直接丢弃，不报错。

**解法**：去后台「订阅消息 → 我的模板 → 详情」看关键词顺序（第 1 个是 thing？第 2 个
是 time？），把 `dailyPush/index.js` 里的 `data` 字段名改成一致。**改完要实测一次**
（自己开提醒等到 20:00，或临时把 cron 改成几分钟后触发），否则无法确认。

## 坑 6：换 AppID 后云环境要重新绑定

**现象**：换了新 AppID，前端上传成功，但扫码还是 `cloud.callFunction:fail`（网络异常）。

**根因**：云环境（`daka-xxx`）原本绑定旧 AppID 或腾讯云账号，换 AppID 后环境没跟过来。

**解法**（把已有环境绑到新 AppID，复用函数/集合/数据）：
1. 腾讯云控制台 `console.cloud.tencent.com` → 账号信息 → 登录方式 → 微信公众平台 →
   **关联**新 AppID 的小程序（一个腾讯云账号同时只能绑一个小程序，先解绑旧的）；
2. 微信开发者工具 → 云开发 → 设置 → 环境设置 → 管理我的环境 → **使用已有腾讯云环境** → 选原环境。

完成后可核对环境字段：`tcb api tcb DescribeEnvs` 看 `Source` 从 `qcloud` 变 `miniapp`、
`EnvChannel` 从 `qc_console` 变 `ide`，即转换成功。

## 坑 7：提审相关（类目 / 隐私 / 分享）

**类目**：个人主体的可选一级类目通常只有「生活服务/工具/体育」（无「教育」）。
打卡/习惯养成类工具最稳的是「生活服务 > 生活助手」，或「工具」下最接近的二级
（记事本/办公等）。**千万别选「社交」类目**——要额外资质、审核严、分享能力反而受限。

**隐私指引**：有两个入口，未上线只能用入口②——
- ① 后台直填（账号设置 → 服务内容声明 → 用户隐私保护指引）：仅对已发布生效；
- ② **提审时勾选**（提交审核页面底部「用户隐私保护指引设置」→ 采集用户隐私）：
  审核通过后生效，这是未上线时该走的。
勾选最小项：订阅消息 + 微信登录(openid)。**勾少了接口失效、勾多了被驳回**，别多勾。

**分享**：分享给好友/群是内置能力，**无需申请**。页面 JS 写了 `onShareAppMessage`，
右上角 `···` 自动出现「转发」。若按钮灰掉，原因是**没做 ICP 备案 + 微信认证**，
不是「没申请分享权限」。分享到朋友圈是另一回事（`onShareTimeline` + 受类目限制）。

## 坑 8：其他工程细节

- **`tcb fn invoke` 无法端到端验证**：它没有真实 OPENID，只能验 seed 这类不依赖
  用户的函数。业务逻辑的端到端验证必须在微信开发者工具/真机做（见 deploy skill Pitfall 2）。
- **查询有 100 条上限**：`db.collection().get()` 单次最多返回 100 条，多的要
  `limit()` + 分页，或用 `orderBy` + 游标。
- **`where` 不能全 undefined**：所有字段都是 undefined 的查询会抛错（见坑 2 验证陷阱）。
- **弱类型集合要写视图函数**：数据库字段是 camelCase，对外 API 用 `xxxView()` 转成
  前端要的格式，别把 `_id`、内部字段直接暴露。
