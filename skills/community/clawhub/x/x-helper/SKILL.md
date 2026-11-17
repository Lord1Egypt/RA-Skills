---
name: x-helper
description: Full-featured X (Twitter) assistant — search, post with media, thread, DM, Lists, bookmarks, trends, articles, block/mute, and more. Pure Python stdlib.
version: 3.0.6
license: MIT-0
metadata:
  openclaw:
    emoji: 𝕏
    requires:
      bins: []
      env:
        - X_CLIENT_ID
        - X_BEARER_TOKEN
    permissions:
      network:
        - api.x.com
        - x.com
        - api.twitter.com
      filesystem:
        - ~/.x-helper/ (token cache, mode 0o600)
      env:
        - X_CLIENT_ID
        - X_BEARER_TOKEN
---

# X Helper

通过自然语言操作 X（Twitter）。纯 Python stdlib，覆盖 X API v2 完整能力。

搜帖子 · 查用户 · 发推（带图/视频/GIF） · 发线程 · 管书签 · 看趋势 · 发文章 · DM · Lists · 屏蔽/静音 · 关注/取关

> ⚠️ **数据外发提醒**：推文内容、私信、媒体文件、搜索查询、用户信息及 Bearer Token 将被发送至 X API 服务器（api.x.com / api.twitter.com）。请勿在自动化环境中处理敏感/机密内容。
>
> ⚠️ **凭据由你掌握**：推荐把 Bearer Token 放进自己的环境变量 `X_BEARER_TOKEN`（你自己执行 export，AI 只读取、不存储、不中转）。Token 通过 Python 内存传递，不会暴露在进程列表或 shell 历史中。

## 前置准备

### 1. 创建 X Developer App

1. 打开 [X Developer Portal](https://developer.x.com)
2. 创建一个 Project + App，启用 **OAuth 2.0**
3. 注册回调 URL：`http://localhost:8080/callback`
4. 记下 **Client ID**（和可选的 Client Secret）

### 2. 配置访问令牌（推荐：自己放环境变量）

在你自己电脑的终端里执行（AI 不会看到你输入的 token）：

```bash
export X_BEARER_TOKEN='你的 X API Bearer Token'
```

> 💡 从 X Developer Portal 的 App 页面复制 Bearer Token，自己粘贴到终端。
> 这个 token 存在你自己的 shell 环境变量里，AI 只读取、不存储、不中转。

### 2b. OAuth 授权流程（仅用于获取 Token）

`auth authorize` 会跑一次 OAuth 2.0 浏览器授权，把 Token 缓存到
`~/.x-helper/auth.json`。**本 skill 不会自动读取该文件来发请求**——
授权完成后请把拿到的 Token 自己 `export X_BEARER_TOKEN=...` 再使用。
（缓存文件仅由你手动运行的 `auth status` / `auth logout` 读取。）

```bash
python3 scripts/x_client.py auth authorize --client-id YOUR_CLIENT_ID
```

### 3. 检查状态

```bash
python3 scripts/x_client.py auth status
```

---

## Triggers & Behavioral Rules

### 通用原则
- **写操作先确认** — 发推、删推、点赞、DM、关注、屏蔽等操作前，先展示概要并确认
- **默认简洁摘要** — 搜索结果默认 5-10 条
- **按需展开** — 用户说"详细点"再展示更多

### 搜索
- "搜一下 / 搜索 [关键词]" → `search posts`
- "搜全量 / 搜全部 [关键词]" → `search posts --archive`
- "搜用户 / 找 @[用户名]" → `search users`
- "搜新闻 / [话题] 的新闻" → `search news`

### 用户
- "看看 @[用户名]" → `user get`
- "我的主页 / 看看我的资料" → `user me`
- "[用户名] 最近发了什么" → `user timeline`
- "谁提到了我 / 我的提及" → `user mentions`
- "[用户名] 的关注者 / 关注了谁" → `user followers / following`
- "[用户名] 赞过什么" → `user liked`

### 推文
- "[内容] 帮我发一下" → `tweet post`（带 --media 可发图片）
- "删掉这条推 [ID]" → `tweet delete`
- "看看这条推 [ID]" → `tweet get`
- "给 [ID] 点赞 / 取消点赞" → `tweet like / unlike`
- "转发 [ID]" → `tweet retweet`

### 线程
- "帮我把这几条串成线程" → `thread post --text1 "" --text2 ""`

### 趋势
- "今天什么趋势" → `trends`
- "看看有哪些地点" → `trends list`

### 书签
- "我的书签" → `bookmark list`
- "收藏这条 [ID]" → `bookmark add`
- "取消收藏 [ID]" → `bookmark remove`

### 文章
- "帮我写一篇文章" → `article draft --title "" --text ""`
- "带格式的文章" → `article draft --title "" --text "" --rich`
- "发布 [ID]" → `article publish`

### DM
- "我的私信 / 最近消息" → `dm list`
- "和 [用户名] 的对话" → `dm conversation [conversation-id]`
- "给 [用户名] 发私信" → `dm send username text`
- "删掉那条消息 [ID]" → `dm delete`

### Lists
- "创建列表 [名称]" → `list create`
- "我的列表" → `list my`
- "列表 [ID] 的成员" → `list members`
- "把 @[用户名] 加入列表" → `list add-member`
- "从列表移除 @[用户名]" → `list remove-member`
- "关注列表 [ID]" → `list follow`
- "列表 [ID] 的推文" → `list posts`

### 屏蔽 / 静音
- "屏蔽 @[用户名]" → `block`
- "取消屏蔽 @[用户名]" → `unblock`
- "我屏蔽了谁" → `blocked`
- "静音 @[用户名]" → `mute`
- "取消静音 @[用户名]" → `unmute`
- "静音列表" → `muted`

### 关注
- "关注 @[用户名]" → `follow`
- "取关 @[用户名]" → `unfollow`

---

## 命令参考

### 搜索
```
  search posts <query> [--max N] [--archive]    搜帖子（--archive 全量归档）
  search users <query> [--max N]                 搜用户
  search news <query> [--max N]                  搜新闻
```

### 用户
```
  user get <username>                            用户信息
  user me                                        当前用户
  user timeline <username> [--max N]             最近推文
  user mentions <username> [--max N]             提及
  user followers <username> [--max N]            关注者
  user following <username> [--max N]            正在关注
  user liked <username> [--max N]                赞过的推文
```

### 推文
```
  tweet post <text> [--reply-to ID] [--media path]...
  tweet get <id>
  tweet delete <id>
  tweet like <id>
  tweet unlike <id>
  tweet retweet <id>
  tweet unretweet <id>
  tweet likers <id> [--max N]
  tweet retweeters <id> [--max N]
  tweet quote-tweets <id> [--max N]
```

### 线程
```
  thread post --text1 "第一段" --text2 "第二段" [--text3 "第三段" ...] [--media path]
```

### 趋势
```
  trends [--woeid N]
  trends list
```

### 书签
```
  bookmark list [--max N]
  bookmark add <tweet-id>
  bookmark remove <tweet-id>
```

### 文章
```
  article draft --title "标题" --text "内容" [--rich]
  article publish <article-id>
```

### DM
```
  dm list [--max N]
  dm conversation <id> [--max N]
  dm send <username> <text> --confirm
  dm delete <event-id> --confirm
```

> ⚠️ **私信敏感**：`dm conversation` 输出的是私信内容（非公开数据），不要外泄。
> `dm send` / `dm delete` 为不可逆操作，必须显式加 `--confirm` 才会执行。

### Lists
```
  list create <name> [--description <desc>]
  list get <id>
  list delete <id>
  list members <id> [--max N]
  list posts <id> [--max N]
  list followers <id> [--max N]
  list add-member <list-id> <username>
  list remove-member <list-id> <username>
  list follow <list-id>
  list unfollow <list-id>
  list my [--max N]
```

### 屏蔽 / 静音
```
  block <username>
  unblock <username>
  blocked [--max N]
  mute <username>
  unmute <username>
  muted [--max N]
```

### 关注
```
  follow <username>
  unfollow <username>
```

---

## 技术特性

- **429 自动重试** — 按 Retry-After header 等待，最多 3 次
- **分页** — likers/retweeters/members/followers/blocked/muted/DM 自动循环拿完
- **媒体上传** — 图片/GIF/视频，INIT→APPEND→FINALIZE 协议，视频自动轮询处理状态
- **线程推文** — 一次发多条串连推文
- **Articles 富文本** — `--rich` 支持 # 标题、**加粗**、*斜体*、列表
- **全量归档搜索** — `--archive` 走 `/tweets/search/all`（需对应 API tier）
- **Token 自动刷新** — offline.access scope，本地 JSON 存储

## 常见问题

**图片发推：** `python3 scripts/x_client.py tweet post "内容" --media photo.jpg --media photo2.png`

**发线程：** `python3 scripts/x_client.py thread post --text1 "第一段" --text2 "第二段"`

**看趋势指定地点：** `python3 scripts/x_client.py trends --woeid 23424856`（WOEID 23424856 = 日本）

**全量搜索：** `python3 scripts/x_client.py search posts "from:user since:2020-01-01" --archive`
