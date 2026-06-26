---
name: twitter-watch-reply
description: 使用 6551 Twitter/X 接口监控指定账号的新推文，并基于推文内容生成 AI 回复草稿；在半自动模式下，先给出候选回复，待用户确认后再通过已登录的浏览器自动回复。用于：监控某些账号、发现其新推、生成评论、人工确认后回复、避免重复回复、管理 watchlist 和状态文件。依赖环境变量 TWITTER_TOKEN 访问 6551 接口。默认把数据写到 workspace 下的 data/twitter-watch-reply；也可用 OPENCLAW_WORKSPACE 或 TWITTER_WATCH_REPLY_DATA_DIR 覆盖路径。
---

# twitter-watch-reply

用这个 skill 做 **AA 模式（6551 监控版）**：
- 6551 负责监控指定账号最近推文
- Agent 负责判断是否为新推并生成回复草稿
- 用户确认后，再用浏览器自动化发出回复

## 适用边界

只做 **半自动**：
1. 用 6551 拉目标账号最近推文
2. 过滤已处理 tweet / 转推 / 不想回复的内容
3. 对新推生成 1~3 条回复候选
4. 等用户明确确认某条候选
5. 用浏览器已登录态去回复

不要默认全自动发送。


## 6551 Token 配置说明

本 skill 的 Twitter/X 监控能力依赖 6551 接口，运行时通过环境变量 `TWITTER_TOKEN` 读取 token。

### token 来源

按 6551 / opentwitter 约定，从这里获取：
- `https://6551.io/mcp`

### 如何配置

在运行本 skill 的同一终端 / 同一调度环境里设置：

```bash
export TWITTER_TOKEN=你的6551token
```

然后再运行：

```bash
python3 skills/twitter-watch-reply/scripts/doctor.py
```

### 注意事项

- 不要把 token 写死到 skill 文件里
- 不要把 token 提交到 Git 仓库
- 不要在聊天里直接发送 token 明文
- 如果用 cron / launchd / 其他调度器，要确保对应运行环境里也能读到 `TWITTER_TOKEN`

### 没配置 token 时会怎样

- `doctor.py` 会提示 `TWITTER_TOKEN missing`
- `fetch_latest_tweets.py` 会直接退出并报错，不会伪装成“没有新推”

## 依赖

必须有：
- 环境变量 `TWITTER_TOKEN`
- 可访问 6551 接口 `https://ai.6551.io`
- 用于最终发送回复的已登录 X 浏览器会话

## 文件结构

- `skills/twitter-watch-reply/references/config-example.json`：配置示例
- `skills/twitter-watch-reply/scripts/watch_state.py`：管理 watchlist / state / 去重
- `skills/twitter-watch-reply/scripts/fetch_latest_tweets.py`：通过 6551 拉最近推文并筛出新推
- `skills/twitter-watch-reply/scripts/pick_pending_tweet.py`：读取当前待处理推文
- `skills/twitter-watch-reply/scripts/render_alert.py`：为新推生成通用提醒载荷（新推 + 候选回复 + notify 配置）
- `skills/twitter-watch-reply/scripts/render_alert_text.py`：把提醒载荷渲染成适合聊天渠道发送的纯文本
- `skills/twitter-watch-reply/scripts/mark_notified.py`：标记某条推文已提醒，避免重复通知
- `skills/twitter-watch-reply/references/reply-generation.md`：生成回复候选的规范
- `skills/twitter-watch-reply/references/host-adapter.md`：宿主如何接通用通知层并真正发消息
- `data/twitter-watch-reply/config.json`：用户配置
- `data/twitter-watch-reply/state.json`：运行状态

若 `config.json` 不存在，先初始化再改配置。

## 默认流程

### 1. 初始化配置

```bash
python3 skills/twitter-watch-reply/scripts/watch_state.py init
```

### 2. 用 6551 拉最近推文

```bash
python3 skills/twitter-watch-reply/scripts/fetch_latest_tweets.py
```

脚本会：
- 读取 `config.json`
- 对 `authors` 逐个优先调用 6551 `twitter_user_tweets`，失败时自动 fallback 到 `twitter_search` + `fromUser`
- 过滤已 seen 的 tweet id
- 按配置跳过 replies / retweets
- 输出待处理的新推列表

### 3. 生成回复草稿

先运行：

```bash
python3 skills/twitter-watch-reply/scripts/pick_pending_tweet.py
```

再按 `references/reply-generation.md` 的规范，对待处理推文生成 3 条候选。

对每条新推默认生成 3 条候选：
- 朋友互动版
- 技术点评版
- 高情商简洁版

生成时遵守配置：
- `tone`
- `language`
- `topicsAllow`
- `blockedWords`
- `maxReplyPerAuthorPerDay`
- `maxTotalReplyPerDay`

### 4. 主动提醒（通用通知层）

先运行：

```bash
python3 skills/twitter-watch-reply/scripts/render_alert.py
```

该脚本会输出一份“提醒载荷”：
- 新推内容
- 链接
- 3 条候选回复
- `notify` 配置

这一步的设计目标是 **通用通知**，而不是写死某个 Telegram 群。

推荐由宿主环境按 `notify.channel / notify.target / notify.threadId` 决定发往：
- Telegram
- Discord
- Slack
- Signal
- 其他 OpenClaw 已接通的消息渠道

### 5. 等待确认后浏览器回复

只有用户明确说“发第 N 条”或给出明确修改意见时，才进入发送步骤。

发送前再次确认：
- 当前账号是否登录
- 回复框是否可写
- 当前推文是否尚未回复过

发送成功后更新 `state.json`：
- 记录 tweet id
- 记录发送时间
- 记录使用的回复文本

## 常用命令


### 安装前自检

```bash
python3 skills/twitter-watch-reply/scripts/doctor.py
```

自检会检查：
- `TWITTER_TOKEN` 是否存在（不显示明文）
- `config.json` / `state.json` 是否存在且格式正确
- 6551 基础连通性是否正常

若 `config.json` / `state.json` 不存在，先运行：

```bash
python3 skills/twitter-watch-reply/scripts/watch_state.py init
```

### 初始化/查看配置

```bash
python3 skills/twitter-watch-reply/scripts/watch_state.py init
python3 skills/twitter-watch-reply/scripts/watch_state.py show-config
```

### 添加/删除监控账号

```bash
python3 skills/twitter-watch-reply/scripts/watch_state.py add-author jakevin7
python3 skills/twitter-watch-reply/scripts/watch_state.py remove-author jakevin7
python3 skills/twitter-watch-reply/scripts/watch_state.py list-authors
```

### 检查新推

```bash
python3 skills/twitter-watch-reply/scripts/fetch_latest_tweets.py
python3 skills/twitter-watch-reply/scripts/fetch_latest_tweets.py --author jakevin7
python3 skills/twitter-watch-reply/scripts/pick_pending_tweet.py
python3 skills/twitter-watch-reply/scripts/render_alert.py
```

### 标记与去重

```bash
python3 skills/twitter-watch-reply/scripts/watch_state.py seen 2030857515660132533
python3 skills/twitter-watch-reply/scripts/watch_state.py was-seen 2030857515660132533
```

## 实操建议

- 第一版只监控 1~5 个账号
- 严格限制每天回复数量
- 半自动确认是默认模式，不要省掉
- 如果 `twitter_user_tweets` 失败，自动 fallback 到 `twitter_search fromUser`；两者都失败时再报错，不要伪造“无新推”
- 如果浏览器登录态失效，明确报错，不要瞎报成功

## 后续扩展

后续如果用户要升级，再增加：
- cron / 定时触发
- Telegram 通知待确认回复
- 关键词白名单
- 自动跳过低价值推文


## 通用化约定

- 不要假设固定机器路径。脚本默认根据自身目录推导 workspace。
- 如需自定义 workspace，设置 `OPENCLAW_WORKSPACE`。
- 如需自定义数据目录，设置 `TWITTER_WATCH_REPLY_DATA_DIR`。
- 定时轮询由外部调度器负责；skill 只提供 `run_watch_loop.sh` 作为示例，不强绑定某个用户的 launchd/cron。


## 通用通知边界

- 这个 skill 只负责生成“提醒载荷”，不把某个渠道写死进脚本。
- 真正的主动发送动作，应由宿主环境（例如 OpenClaw 的 message 能力）根据 `notify` 配置执行。
- 因此，Telegram / Discord / Slack / Signal 等都可以通过同一份提醒载荷来适配。


## 宿主发送流程（推荐）

推荐由宿主环境按以下顺序执行：

1. 运行 `fetch_latest_tweets.py`
2. 运行 `render_alert.py` 或 `render_alert_text.py`
3. 若存在 alert 且 `notify.enabled=true`，按 `notify.channel/target/threadId` 发消息
4. 发送成功后运行 `mark_notified.py <tweet_id>`

这样通知层就能保持通用，不和特定消息渠道耦合。


## 宿主适配

如果需要真正做到“抓到新推就自动提醒”，读取 `references/host-adapter.md`。
该文件说明了宿主（尤其是 OpenClaw）应如何消费本 skill 产生的 alert，并在发送成功后执行去重标记。
