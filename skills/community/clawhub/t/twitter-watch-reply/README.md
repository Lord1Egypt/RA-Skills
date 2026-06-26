# twitter-watch-reply

一个半自动的 Twitter/X 监控与 AI 回复 skill。

能力流程：

1. 使用 6551 接口监控指定账号的新推文
2. 自动筛出待处理推文
3. 生成 3 条 AI 回复候选
4. 用户确认后，通过本地已登录的 X 浏览器会话发送回复

---

## 适用场景

适合这些需求：
- 监控某些 X/Twitter 账号是否发了新推
- 对新推快速生成评论草稿
- 做半自动互动，而不是全自动乱回
- 用 6551 做监控层、浏览器做执行层

不适合：
- 零配置即用
- 没有 6551 token 的环境
- 没有本地 X 登录态却想自动发送回复
- 要求完全稳定、完全实时、完全无人值守的高强度生产场景

---

## 前置要求

### 1. 6551 Twitter Token

本 skill 通过环境变量 `TWITTER_TOKEN` 调用 6551 接口。

获取方式：
- https://6551.io/mcp

配置示例：

```bash
export TWITTER_TOKEN=你的6551token
```

> 不要把 token 写进仓库，不要发到聊天里，不要硬编码到脚本中。

### 2. 已登录 X 的本地浏览器

如果你要让 skill 帮你真正发回复：
- 你的本地浏览器需要已登录 `x.com`
- 浏览器自动化需要能访问该登录态

### 3. Python 3

脚本基于 Python 3 运行。

---

## 安装方式

如果你已经拿到了 `.skill` 包，例如：

```bash
dist/twitter-watch-reply.skill
```

按你的 OpenClaw / Skill 安装方式安装即可。

如果你拿到的是源码目录，也可以直接放入 skills 目录使用。

---

## 初始化

先初始化配置与状态文件：

```bash
python3 skills/twitter-watch-reply/scripts/watch_state.py init
```

执行后会生成：
- `data/twitter-watch-reply/config.json`
- `data/twitter-watch-reply/state.json`

---

## 安装前自检

建议先跑自检：

```bash
python3 skills/twitter-watch-reply/scripts/doctor.py
```

会检查：
- `TWITTER_TOKEN` 是否存在
- 配置文件是否存在且格式正确
- 状态文件是否存在且格式正确
- 6551 接口是否可连通

如果没配 token，会提示你去：
- https://6551.io/mcp

---

## 配置说明

配置文件位置：

```bash
data/twitter-watch-reply/config.json
```

示例配置：

```json
{
  "authors": [],
  "language": "zh",
  "tone": "sharp-friendly",
  "topicsAllow": ["AI", "OpenClaw", "agent", "crypto", "devtools"],
  "blockedWords": ["稳赚", "喊单", "返利"],
  "skipRetweets": true,
  "skipReplies": true,
  "maxResultsPerAuthor": 5,
  "maxReplyPerAuthorPerDay": 3,
  "maxTotalReplyPerDay": 10,
  "candidateCount": 3,
  "mode": "semi-auto-6551-monitor-browser-reply"
}
```

### 关键字段

- `authors`: 要监控的账号列表，不带 `@`
- `language`: 回复语言
- `tone`: 回复风格
- `topicsAllow`: 优先处理的话题范围
- `blockedWords`: 避免出现在回复中的词
- `skipRetweets`: 是否跳过转推
- `skipReplies`: 是否跳过 reply 类型推文
- `maxResultsPerAuthor`: 每次检查每个账号拉多少条
- `candidateCount`: 生成几条候选回复

---

## 管理监控账号

### 查看当前账号

```bash
python3 skills/twitter-watch-reply/scripts/watch_state.py list-authors
```

### 添加账号

```bash
python3 skills/twitter-watch-reply/scripts/watch_state.py add-author elonmusk
```

### 删除账号

```bash
python3 skills/twitter-watch-reply/scripts/watch_state.py remove-author elonmusk
```

---

## 检查新推

### 检查全部监控账号

```bash
python3 skills/twitter-watch-reply/scripts/fetch_latest_tweets.py
```

### 检查单个账号

```bash
python3 skills/twitter-watch-reply/scripts/fetch_latest_tweets.py --author elonmusk
```

这个脚本会：
- 优先调用 6551 `twitter_user_tweets`
- 如果失败，自动 fallback 到 `twitter_search + fromUser`
- 把新推写入待处理队列

---

## 读取当前待处理推文

```bash
python3 skills/twitter-watch-reply/scripts/pick_pending_tweet.py
```

输出类似：

```json
{
  "ok": true,
  "pending": {
    "id": "...",
    "author": "elonmusk",
    "text": "...",
    "url": "https://x.com/..."
  }
}
```

---

## 回复工作流

推荐流程：

1. 拉新推
2. 读取 pending tweet
3. 基于待处理推文生成 3 条回复候选
4. 用户选择其中一条
5. 再通过浏览器自动化发送回复

这是**半自动模式**，默认不建议改成全自动直发。

---


## 主动提醒（通用通知层）

这个 skill 已预留通用通知配置：

```json
"notify": {
  "enabled": false,
  "channel": "telegram",
  "target": "",
  "threadId": "",
  "mode": "candidate-alert"
}
```

说明：
- `enabled`: 是否开启主动提醒
- `channel`: 目标渠道，例如 telegram / discord / slack
- `target`: 目标会话、频道或群 ID
- `threadId`: 可选，线程/话题场景可用
- `mode`: 当前默认 `candidate-alert`，表示发“新推 + 3 条候选回复”

生成提醒载荷：

```bash
python3 skills/twitter-watch-reply/scripts/render_alert.py
```

这个脚本输出的是**通用提醒 JSON**，用于交给宿主环境发送。
因此它本身不把任何特定聊天渠道写死。

## 每两分钟轮询一次

skill 内置了一个简单轮询脚本：

```bash
bash skills/twitter-watch-reply/scripts/run_watch_loop.sh
```

默认每 120 秒跑一次。

它适合：
- 本地测试
- 快速验证
- 临时使用

它不等于系统守护进程。
如果你要更稳定的长期运行，建议自己接：
- cron
- launchd
- 其他调度器

---

## 环境变量与路径覆盖

默认情况下，skill 会自动推导 workspace/data 路径。

也支持手动覆盖：

### 指定 workspace

```bash
export OPENCLAW_WORKSPACE=/path/to/workspace
```

### 指定数据目录

```bash
export TWITTER_WATCH_REPLY_DATA_DIR=/path/to/data/twitter-watch-reply
```

---


### 推荐的宿主发送流程

如果你的宿主环境支持消息发送（例如 OpenClaw message 能力），推荐按这个顺序接：

```bash
python3 skills/twitter-watch-reply/scripts/fetch_latest_tweets.py
python3 skills/twitter-watch-reply/scripts/render_alert_text.py
python3 skills/twitter-watch-reply/scripts/mark_notified.py <tweet_id>
```

说明：
1. `fetch_latest_tweets.py` 负责查新推并写入 pending
2. `render_alert_text.py` 负责把提醒渲染成聊天文本
3. 宿主环境负责真正发到 Telegram / Discord / Slack / 其他渠道
4. 发送成功后再调用 `mark_notified.py` 做去重

## 注意事项

- 这个 skill 共享的是“能力和流程”，不共享你的 token 和登录态
- 别人使用时，必须自己准备 `TWITTER_TOKEN`
- 别人如果要自动回复，也必须自己本地登录 `x.com`
- 6551 对不同账号的数据支持可能不完全一致，所以做了 fallback
- 浏览器自动化回复依赖页面结构，网页改版后可能需要调整

---


## OpenClaw 宿主接法（推荐）

如果你希望“抓到新推就自动提醒”，推荐由 OpenClaw 宿主来接消息发送。

参考：
- `references/host-adapter.md`

推荐流程：
1. skill 负责查新推与生成 alert
2. OpenClaw 宿主负责把 alert 发到指定渠道
3. 发送成功后，再调用 `mark_notified.py` 去重

这样才能保持：
- skill 通用
- 渠道可配置
- 权限不写死在 skill 里

## 当前定位

这是一个：

**可分享的通用半自动 skill**

不是：
- 零配置 SaaS
- 完全无人值守机器人
- 保证所有账号 100% 稳定的企业级产品

但对于个人或小规模半自动运营，已经够用了。
