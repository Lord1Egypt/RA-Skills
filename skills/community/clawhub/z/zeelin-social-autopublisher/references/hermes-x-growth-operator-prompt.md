# Hermes X Growth Operator Prompt

这个模板专门给 Hermes 做 X/Twitter 的定时运营，拆成两个独立任务：

1. 内容发布：定时发 1 条 AI 热点观点帖
2. 增长互动：搜索互关/求关注类帖子，用英文回复，单次 8 人

## 任务 A：定时 AI 热点发帖

```text
Use the zeelin-social-autopublisher skill.

Before posting, gather at least 2 current AI news signals from the web or browser results.
Compress them into one strong X topic with a clear judgment.

Run this script:
{SKILL_ROOT}/zeelin-social-autopublisher/scripts/run_x_growth_ops.sh

Arguments:
--topic "{TOPIC}"
--post-only

Requirements:
- Post to X/Twitter only
- Avoid short copy; write a dense single post with a hook, 2-3 concrete signals, and a forward-looking judgment
- Prefer latest AI infra, agent, model distribution, product, or hardware trends
- Return the run directory path
- Summarize whether the X post succeeded
```

## 任务 B：定时互关增长互动

```text
Use local Chrome/CDP-based X automation, not the official API.

Run this script:
{SKILL_ROOT}/zeelin-social-autopublisher/scripts/run_x_growth_ops.sh

Arguments:
--reply-only
--reply-limit 8
--reply-query "{QUERY}"

Requirements:
- Search X/Twitter for mutual-follow / follow-back style posts
- Reply in English only
- Keep replies friendly and slightly varied, not copy-pasted word-for-word every time
- Do not exceed 8 replies in one run
- Summarize how many replies succeeded vs failed
- If login is missing, say that X needs relogin in the visible Chrome profile
```

## 推荐 query

```text
("follow back" OR "follow for follow" OR f4f OR "mutual follow") (AI OR founder OR builder OR startup)
```
