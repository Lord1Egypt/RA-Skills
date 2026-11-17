---
name: xhs-short-url
slug: xhs-url-short
displayName: 小红书长链转短链
version: 2.0.1
description: 小红书笔记长链批量转短链工具（xhslink.com 短链）。当用户提到小红书短链、长链转短链、生成短链，或要求把小红书笔记长链接压缩成短链时使用本 skill。收费服务（1 条长链 = 1 点数，注册送 10 点），支持 1~50 条批量、异步任务轮询、结果导出。
---

# 小红书长链转短链 Skill（xhs-short-url）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用：提交小红书笔记**长链** → 服务端调用小红书官方 short_url 接口 → 得到 `xhslink.com/m/xxx` 短链。

与转链 skill（`xhs-convert-url-pro`）**方向相反、不可互替**：
- 本 skill：**长链 → 短链**（把冗长的笔记链接压缩成 `xhslink.com` 短链，适合分享/投放）。
- xhs-convert-url-pro：**任意链接 → 带 xsec_token 的可用长链**（采集前置，转出的链接浏览器可直接打开）。

与互动数采集 skill（`xhs-dpt`）、评论采集 skill（`xhs-comments`）同框架、同凭证、同输出规约：共用 `~/.xhs-platform/config.json`，登录一次全部通用，`logout` 会同时使所有 skill 失效。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、结果异常等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **每条长链 1 点数**（无效链接不扣费）。
- 注册即送 **10 免费点数**；点数不足时提示用户充值。
- 充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## 链接要求（重要）

- **仅接受 xiaohongshu.com 长链**：`xiaohongshu.com/explore/<id>` 或 `/discovery/item/<id>`。
- **不接受 xhslink 短链**——短链无需转换，本地校验直接拒绝（不提交、不扣费）。
- **不需要 xsec_token 参数**。
- 每批 1~50 条，`--url` 可重复或 `--file` 按行读取。

## 前置条件

- **Node.js ≥ 18**（使用内置 fetch，零 npm 依赖，无需 `npm install`）。
- 不注册不登录没有点数：首次使用先 `register --link`（注册即送 10 点数）或 `login --link`；token 自动保存到 `~/.xhs-platform/config.json`，后续调用免输。
- 终端注册/登录会被 2003（图形验证码）拒绝，一律走 `--link` 扫码/链接方式。

## 输出规约（重要）

- **stdout 只输出 JSON**：成功 `{"ok":true,"data":{...}}`，失败 `{"ok":false,"code":<业务码>,"message":"..."}`。直接解析 stdout 即可。
- 交互提示、轮询进度一律走 **stderr**，不要解析。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败（重新 login）；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。

## 命令速查

```bash
node cli.js version                                # 查看版本
node cli.js register --link                        # 注册引导（送 10 点数）
node cli.js register --check --access-token "<串>" # 用户注册完成后确认保存 token
node cli.js login --link                           # 登录引导
node cli.js login --check --access-token "<串>"    # 用户登录完成后确认保存 token
node cli.js submit --url "<长链>" [--url ...] [--file urls.txt] [--wait]
node cli.js submit --file urls.txt --wait --force  # 跳过 24h 内容去重强制重提
node cli.js query <task_id> [--wait]               # 查询任务
node cli.js export <task_id> --wait --out out.csv  # 导出 CSV
node cli.js quota                                  # 查询点数
node cli.js logout                                 # 登出（所有平台 skill 同步失效）
node cli.js config show                            # 查看配置（token 脱敏）
```

## submit 输出解读（agent 必读）

`submit --wait` 返回任务终态（`done` / `partial_failed` / `failed`），条目结果在 `items[]`：

```json
{"ok":true,"data":{"task_id":"t_20260921_x1","status":"done","total":1,"valid_count":1,
 "success_count":1,"items":[{"id":1,"status":"success",
 "payload":{"long_url":"https://www.xiaohongshu.com/explore/6970ac..."},
 "result":{"long_url":"https://www.xiaohongshu.com/explore/6970ac...",
           "short_url":"https://xhslink.com/m/xxxxxx","worker_id":"node-..."}}]}}
```

- `result.short_url` 是最终短链（已补 `https://` 前缀），可直接交给用户。
- 条目 `status:"invalid"` 表示链接不合法（非长链/格式错误），不扣费，附 `fail_reason`。
- 条目 `status:"failed"` 且 `fail_reason` 含"接口拒绝(406)"属偶发限流或凭证失效，如实透出；服务侧整体失败（网络/cookie/签名缺失）点数会自动返还（`refunded_quota` 体现）。

## 典型工作流（agent 照此执行）

1. `node cli.js quota` — 确认剩余点数 ≥ 待提交长链数。
2. `node cli.js submit --url <长链1> --url <长链2> ... --wait` — 一步拿到终态结果（URL 较多时用 `--file`）。
3. 解析 stdout JSON：把 `status==="success"` 条目的 `result.short_url` 按原顺序整理返回给用户；失败条目附 `fail_reason` 说明。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 | 检查命令参数（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 未注册过走 `register --link`（送 10 点数），已有账号走 `login --link`；把引导话术发给用户，完成后 `--check`（退出码 2） |
| LOGIN_PENDING | 用户尚未完成注册/登录 | 提醒用户完成扫码/链接操作后重试 `--check`（退出码 2） |
| LOGIN_EXPIRED | 会话过期/已使用 | 重新执行 `register --link` 或 `login --link`（退出码 2） |
| 2003 | 需要图形验证码 | 统一走 `--link` 网页方式；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，不要重试（退出码 3） |
| 3002 | 超单次批量上限 | 拆分为 ≤50 条/批重新提交 |
| 3005 | 能力不存在 | 检查服务端版本 |
| 条目 fail_reason 含 406 | 偶发限流/凭证失效 | 单条偶发可稍后重提；整批失败说明服务端 cookie/签名待更新，已自动返还点数 |
| 4290 | 触发限流 | 稍等后重试 |
| TIMEOUT | 轮询超时 | 任务未结束，稍后 `query <task_id>` 再查（退出码 5） |
| NETWORK_ERROR | 网络/服务不可达 | 检查网络与 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- 每条**有效**长链扣 1 点数（提交时预扣）；无效链接（短链/非官方域名/格式错误）不扣费。
- 服务侧失败（网络、cookie/签名缺失、连续限流）自动按条返还点数（`refunded_quota` 体现）。
- 已进入转换接口后返回失败（如偶发 406）**不返还**点数。
- 同一用户同一长链 24h 内默认去重（防手滑重复扣费），`--force` 可强制重提。

## 红线

- 仅处理**公开**小红书笔记长链；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功；服务端原因的失败如实透出（fail_reason）。
- 不要向用户泄露服务端 cookie / 签名等凭证信息。
