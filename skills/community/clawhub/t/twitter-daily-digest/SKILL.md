---
name: twitter-daily-digest
description: 批量获取并整理用户关注的所有 Twitter/X 账号最近 24 小时内的更新。当用户提到“每日推文摘要”“今日推文”“关注的人最近发了什么”“Twitter digest”“推特日报”“帮我看看推特”“刷推”，或要求查看单个/多个指定 X 账号最近动态时，都应触发此 skill。默认输出中文整合版正文；如需测试前 3 个或前 5 个账号，也应使用此 skill。
---

# Twitter 每日推文摘要

这套 skill 现在采用 **JSON 事实层 + agent 主观整理层** 的边界：

- 脚本负责：抓取、标准化、保存原始材料、同步 Notion
- agent 负责：判断什么值得看、怎么分组、怎么翻成中文、怎么发给用户

脚本不再是最终日报的“编辑器”。最终中文整合版由 agent 基于 JSON 自己完成。

## 前置条件

- 已安装并认证 twitter CLI
  - 包名：`twitter-cli`
  - 安装命令：`uv tool install twitter-cli`
  - 可执行文件名：`twitter`
- 如需代理：`export TWITTER_PROXY=http://127.0.0.1:7897`
- 如需 Notion：`~/.config/notion/api_key` 存在，且父页面已共享给 integration

验证：

```bash
twitter whoami
test -s ~/.config/notion/api_key && echo OK || echo MISSING
```

## 规范路径

规范源固定为：

```bash
~/.openclaw/shared-skills/twitter-daily-digest/
```

脚本固定入口：

```bash
python3 ~/.openclaw/shared-skills/twitter-daily-digest/scripts/fetch_digest.py
```

不要再依赖 `$SKILL_DIR` 或 `python` 命令名，OpenClaw 定时任务里优先用上面的固定入口。

## 标准工作流

### 1. 先抓 JSON 原始材料

日常全量抓取：

```bash
python3 ~/.openclaw/shared-skills/twitter-daily-digest/scripts/fetch_digest.py \
  --hours 24 \
  --output /tmp/twitter-digest.json \
  --json-only
```

如果用户只要前 3 个或前 5 个账号，直接用 `--sample-size`：

```bash
python3 ~/.openclaw/shared-skills/twitter-daily-digest/scripts/fetch_digest.py \
  --hours 24 \
  --sample-size 3 \
  --output /tmp/twitter-digest-3.json \
  --json-only
```

如果用户点名要看某几个账号，直接传 `--users`：

```bash
python3 ~/.openclaw/shared-skills/twitter-daily-digest/scripts/fetch_digest.py \
  --users "openai,anthropicai,trq212" \
  --hours 24 \
  --output /tmp/twitter-digest-users.json \
  --json-only
```

### 2. agent 读取 JSON，自行做主观整理

读取 `/tmp/twitter-digest.json` 后，由 agent 自己完成这些事情：

- 判断什么值得看，什么该跳过
- 判断是否保留转推
- 判断该怎么按话题分组
- 写 3 行核心结论
- 把英文内容翻成自然中文
- 组织成适合直接阅读的最终正文

不要把“什么值得看”的判断写死在脚本里。`tweets` 里的顺序只是脚本输出顺序，不代表最终优先级，agent 应自己判断。

### 3. 先保存本地正式版

最终中文版 Markdown 由 agent 自己写出，并保存到：

```bash
~/Desktop/ai-daily-digest-tool/digests/YYYY-MM-DD.md
```

这份文件才是正式版。Telegram 和 Notion 都应基于这同一份内容继续往下走。

### 4. 再发 Telegram 正文

把中文整合版直接作为正文发给用户：

- 发正文，不要只说“已保存到文件”
- 发纯文本聊天内容，不要直接扔 Markdown 源码
- 内容不能明显过短
- 太长就自动拆成多条连续消息
- 保留用户名、互动数据、链接这些事实信息

### 5. 最后把同一份 Markdown 写入 Notion

脚本只负责把**现成 Markdown** 写入 Notion，不再重新抓取 Twitter：

```bash
python3 ~/.openclaw/shared-skills/twitter-daily-digest/scripts/fetch_digest.py \
  --sync-only \
  --notion-markdown-input ~/Desktop/ai-daily-digest-tool/digests/YYYY-MM-DD.md \
  --notion-title "YYYY-MM-DD"
```

这样可以保证本地 / Telegram / Notion 三端内容一致。

## 脚本输出的事实材料

JSON 里最重要的字段：

- `accounts`：本次关注列表
- `accounts_with_recent_tweets`：最近时间窗口内有更新的账号和条数
- `failed_accounts`：抓取失败的账号及错误
- `tweets`：推文原始材料

单条 `tweet` 至少包含这些客观字段：

```json
{
  "id": "...",
  "url": "https://x.com/{screenName}/status/{id}",
  "text": "完整推文内容",
  "author": { "name": "...", "screenName": "..." },
  "metrics": {
    "likes": 0,
    "retweets": 0,
    "replies": 0,
    "views": 0,
    "bookmarks": 0
  },
  "createdAt": "...",
  "createdAtLocal": "2026-03-14 12:00",
  "createdAtTs": 0,
  "isRetweet": false,
  "quotedTweet": null
}
```

如果 `failed_accounts` 非空，说明这次抓取不是完整成功。agent 应在最终结果里识别这是“部分成功”，必要时提示用户或重试。

`accounts_with_recent_tweets` 现在也是客观统计，包含：

- `tweetCount`
- `latestTweetAtLocal`
- `latestTweetUrl`

## 常用参数

| 参数 | 说明 |
| --- | --- |
| `--output FILE` | JSON 输出路径 |
| `--json-only` | 显式声明只输出 JSON 事实层；当前默认抓取模式也是这一行为 |
| `--sync-only` | 只把现成 Markdown 写入 Notion，不重新抓 Twitter |
| `--users "a,b,c"` | 指定账号列表 |
| `--sample-size N` | 只抓前 N 个账号 |
| `--hours N` | 回溯 N 小时 |
| `--twitter-bin PATH` | 指定 twitter CLI 路径 |

脚本已经不再负责生成启发式 Markdown / chat 摘要，也不再内置“什么更值得看”的主观判断。

## 故障排除

### twitter: command not found

脚本自动按以下顺序查找 `twitter`：

1. `$TWITTER_BIN`
2. `$PATH` 中的 `twitter`
3. `~/.local/bin/twitter`
4. `/opt/homebrew/bin/twitter`
5. `/usr/local/bin/twitter`

cron / agent 环境推荐：

```bash
export TWITTER_BIN=$HOME/.local/bin/twitter
```

### Notion 同步失败

优先检查：

1. `~/.config/notion/api_key` 是否存在
2. 父页面是否共享给 integration
3. `--notion-markdown-input` 指向的文件是否存在

Notion 父页面：

- ID: `323dfb80-f233-811a-b597-f30cb2013145`
- 链接: https://www.notion.so/323dfb80f233811ab597f30cb2013145

### 备选手动命令

脚本不可用时，可直接用 twitter CLI 手动抓：

```bash
twitter whoami --yaml
twitter following <username> --max 200 --yaml
twitter user-posts <screenName> --max 10 --yaml --full-text
```
