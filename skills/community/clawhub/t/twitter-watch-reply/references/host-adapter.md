# Host Adapter Reference

本 skill 的通知层设计为：**skill 负责生成提醒内容，宿主负责真正发送消息**。

## 适配目标

宿主（例如 OpenClaw）需要完成这 4 步：

1. 运行 `fetch_latest_tweets.py`
2. 运行 `render_alert.py` 或 `render_alert_text.py`
3. 如果存在 alert 且 `notify.enabled=true`，按 `notify.channel / target / threadId` 发送消息
4. 发送成功后，运行 `mark_notified.py <tweet_id>`

---

## 推荐接法：OpenClaw 宿主

如果宿主是 OpenClaw，推荐使用内置消息能力完成真正发送。

### notify 配置示例

```json
{
  "notify": {
    "enabled": true,
    "channel": "telegram",
    "target": "-1001234567890",
    "threadId": "289",
    "mode": "candidate-alert"
  }
}
```

### 宿主执行逻辑（伪代码）

```text
run fetch_latest_tweets.py
run render_alert.py
if alert exists and notify.enabled:
  render text
  call host message/send with:
    channel = notify.channel
    target = notify.target
    threadId = notify.threadId
    message = rendered text
  if send succeeds:
    run mark_notified.py <tweet_id>
```

---

## 为什么不把发消息写死到脚本里

因为真正的消息发送能力属于宿主环境，而不是 skill 本身。

这样设计的好处：
- 不绑定 Telegram
- 不绑定某个 bot token
- 可复用到 Discord / Slack / Signal / 其他 OpenClaw 渠道
- skill 可分享，权限不跟着 skill 走

---

## 常见宿主场景

### 场景 1：Telegram 群提醒
- `channel = telegram`
- `target = 群ID`
- `threadId = 话题ID（可选）`

### 场景 2：Discord 频道提醒
- `channel = discord`
- `target = 频道ID`

### 场景 3：Slack 频道提醒
- `channel = slack`
- `target = 频道ID或名称`

---

## 最小集成要求

宿主至少要能：
- 运行本地脚本
- 读取 JSON 输出
- 调用消息发送能力
- 在发送成功后再做去重标记

如果宿主不能做这四件事，这个 skill 仍可用于“手动提醒 + 半自动回复”，只是无法做到自动推送。
