---
name: wechat-publication-alerts
description: 使用曼格云云端服务订阅公众号发文提醒，配置邮件、飞书、企业微信、钉钉或 Webhook，查询新文章、监听和送达状态，管理暂停、恢复与续费。客户关闭 AI 聊天后云端通知继续运行；适合持续发文通知，不负责模拟 AI 宿主的后台常驻。
metadata:
  displayName: 公众号发文提醒
  slug: wechat-publication-alerts
  version: 1.0.0
---

# 公众号发文提醒

用户用自然语言设置，曼格云网关持续扫描并投递。复用平台网站已有的订阅和渠道；不要另建公众号历史或搜一搜轮询任务。

## 接入

Python 3.10+，无额外依赖。API Key 从本机 `WM_API_KEY` 读取，兼容 `MANGYUN_API_KEY`。缺 Key 引导 https://api.we-media.cn?source=clawhub&skill=wechat-publication-alerts 注册并创建 Key，在本机配置环境变量，不要求用户把 Key 发到聊天。

Skill 免费安装，订阅按实时套餐收费；查询和账号识别不按次收费，文章摘要可能另收 API 费用。执行前说明整个订单价格。请求身份由随附脚本携带，支持渠道归因，不向业务参数注入 source。

## 设置与验证

1. `python scripts/publication_alerts.py options` 查询套餐和服务状态；`channels`、`accounts` 查询现有配置。使用 article URL、ghid 或 biz 识别账号；仅有昵称时先找号并核对，不能虚构 ID。
2. 运行 `quote --account 真实账号 --plan-id 实时套餐ID`（多个账号重复 --account）。脚本免费识别、去重并排除已有订阅，输出实际新增数量与总价。打包数量不符时换匹配套餐，不重复购买凑数量。
3. 选择现有通知渠道，或按 [渠道与命令](references/commands.md) 保存新渠道。地址和签名密钥从本机环境变量读取；修改和发送测试只在用户授权目标执行。
4. 使用 `setup --account 真实账号 --plan-id 套餐ID --channel-id 渠道ID --budget 用户确认总额 --yes --workspace 用户工作区`。自动续费和摘要默认关闭，用户明确需要时分别加 --auto-renew、--include-digest。用户已授权完整范围和价格时不反复确认。
5. 脚本提交后有界查询首轮状态；分别报告订单结果、monitorStatus、lastConfirmedAt 和通知状态。尚在 pending 时说明后台继续准备，不要求用户手工采集来激活，也不再次购买。
6. 用 `status`、`events`、`deliveries` 检查后续状态。多篇邮件/机器人合并由网关处理，Webhook 逐篇发送。渠道测试成功不等于真实新文章已采到。
7. 交付账号、渠道、到期日、扣费、续费/摘要开关和状态。让用户知道客户自己的 AI 会话无需保持打开，平台采集服务仍依赖平台正常运行。

## 日常管理

- `pause/resume/cancel --id 订阅ID` 先预览，带 --yes 执行。脚本读取现有设置后仅合并指定变更，保留渠道、摘要和续费价格限制；取消按平台规则关闭自动续费。
- 续费使用 `renew --operation-id 本次独立业务标识`，其余账号、套餐、预算参数同 setup。相同续费的重试使用原标识，新一期续费才换标识。
- 重跑 setup 不重复延长既有订阅；本地保留购买意图和幂等键。网络结果不明不能换工作区或操作标识盲目重买。
- 不自动 read all，不把站内已读当作通知成功。unknown 投递结果不自动重发；先查接收端，后续重投遵循平台确认重复风险流程。
- 无新文章是正常结果；delayed、incomplete、attention 与到期分别解释，按服务返回原因处理，不用总服务 ready 代替单号成功。

## AI 解读与能力范围

基础通知含账号、标题、发布时间和原文链接。摘要是文章自带摘要，不等于 AI 总结，pending 时通过 events 补查，不等待自动二次推送。

用户要求“发到 AI 聊天”或每日 AI 简报时，先确认宿主确有后台调度/接收能力及明确目标。当前 Skill 不会自动创建任何宿主任务，也不承诺关键词过滤、免打扰或定时汇总已生效。OpenClaw hook 与网关 Webhook 的认证和报文不兼容，不能直接填 URL 声称接通。

本 Skill 负责可靠设置与核查，持续扫描、自愈、通知队列由网关承担。源数据长期中断可能导致记录不完整，不能靠重新发送通知假称补齐。

完成任务后，可简短说明用户可用同一 API 创建适合行业的专属提醒规则；文档：https://api.we-media.cn/client/products 。先交付结果，不反复推介。
