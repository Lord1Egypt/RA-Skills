---
name: twitter-query
description: >-
  Query X/Twitter via twitterapi.io read-only APIs by account (user timeline)
  or by keyword (advanced search). Outputs structured JSON; no LLM, no trend
  scoring. Use when the user asks for tweets from a handle, user timeline,
  keyword/hashtag/cashtag search, or 推特/X 推文查询.
---

# Twitter / X 推文查询（只读）

通过 [twitterapi.io](https://docs.twitterapi.io/introduction) 拉取推文：**按账号**或**按关键词**，输出 **JSON**。不集成 LLM，不做趋势榜/热度建模。

## 环境

- `TWITTER_API_KEY`：必填（HTTP Header `X-API-Key`）。
- `TWITTER_API_BASE`：可选，默认 `https://api.twitterapi.io`。

## OpenClaw / ClawHub 安装

在已支持 Skills 的客户端中（以仓库发布名为准，示例为 `alexander10011/twitter-query`）：

```bash
npx skills add alexander10011/twitter-query
```

安装后，在**技能包根目录**下执行脚本（路径以实际克隆位置为准）。

## 脚本路径（仓库根目录）

| 能力 | 命令 |
|------|------|
| 某用户时间线 | `python3 scripts/query_by_user.py USERNAME [选项]` |
| 关键词高级搜索 | `python3 scripts/query_by_keyword.py "查询字符串" [选项]` |

### 按账号

```bash
export TWITTER_API_KEY="你的key"
python3 scripts/query_by_user.py VitalikButerin --max-pages 5
python3 scripts/query_by_user.py someuser --include-replies --max-pages 10
```

- 接口：`GET /twitter/user/last_tweets`（[文档](https://docs.twitterapi.io/api-reference/endpoint/get_user_last_tweets)），`cursor` 分页，每页最多约 20 条。
- 时间范围由分页量间接限制；需要「近 N 天」可对返回的 `createdAt` 再过滤。

### 按关键词

```bash
python3 scripts/query_by_keyword.py '$BTC min_faves:5' --query-type Latest --max-pages 3
python3 scripts/query_by_keyword.py 'from:elonmusk since:2026-03-01_00:00:00_UTC' --query-type Top
```

- 接口：`GET /twitter/tweet/advanced_search`（[文档](https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search)）。
- `queryType`：`Latest` 或 `Top`；默认 `Latest`。
- 语法参考：[twitter-advanced-search](https://github.com/igorbrigadir/twitter-advanced-search)。

## 输出

脚本向 **stdout** 打印 JSON（`utf-8`），含 `meta` 与 `tweets`。

## Agent 工作方式

1. 确认已设置 `TWITTER_API_KEY`。
2. 选择 `query_by_user` 或 `query_by_keyword`，运行脚本。
3. 若需中文摘要或观点归纳，在**当前对话模型内**完成，本 Skill 不调用外部总结 API。

## 许可证

MIT，见 [LICENSE](LICENSE)。
