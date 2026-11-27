---
name: xiaohongshu-note-summary
description: "小红书笔记总结 / Xiaohongshu (RedNote) note summary. 用户发来小红书笔记（xiaohongshu.com、xhslink.com、rednote.com 链接或整段分享文字），想知道「这篇笔记讲了什么」「值不值得看完」「结论和推荐是什么」时使用。读的是笔记本身：正文、每张图里的字（OCR）和图片描述，视频笔记读口播和画面文字；先给一段话总结和几条要点，每条要点附它出自第几张图或哪句原话，可以核对，不是凭标题猜。没有 Key 也能先免费看一条摘要；完整内容需要 LinkDigest API Key（注册送 10 积分）。不登录小红书、不要 Cookie、不下载图片；读不了不扣费。"
version: 1.0.1
homepage: https://linkdigest.dev/zh/xiaohongshu-biji-tiqu?ref=skill-xiaohongshu-note-summary
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":false,"description":"可选。LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-xiaohongshu-note-summary&next=/app/keys 创建，注册送 10 积分；没有 Key 时每个地址每天可免费看 2 条摘要"}],"homepage":"https://linkdigest.dev/zh/xiaohongshu-biji-tiqu?ref=skill-xiaohongshu-note-summary"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_); optional"
    help: "https://linkdigest.dev/signin?ref=skill-xiaohongshu-note-summary&next=/app/keys"
    required_for: "the text in every image and the full transcript; without it the script gives a free summary, up to 2 a day per address"
---
# 小红书笔记总结 (a Xiaohongshu note summary you can check against the note)

On Xiaohongshu the substance of an image note is usually written inside the pictures: the title is one line, the body a few more, and the page a server gets back repeats 「打开App查看更多」. An agent handed the link therefore tends to summarise the title. This skill reads the note itself and answers from what the pictures and the speech actually say.

## Steps for the agent

1. Read the link the user gave (a `xiaohongshu.com` or `rednote.com` link, an `xhslink.com` short link, or the whole share text). Pass it exactly as given, with its `xsec_token`:
   ```bash
   export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-xiaohongshu-note-summary&next=/app/keys  (optional, see below)
   python3 {baseDir}/scripts/linkdigest.py --format json "https://www.xiaohongshu.com/discovery/item/6a6bf662000000002402de7e?xsec_token=CBCe01s1uyd2C8uMx6ycYcnEwPV5_31OX1u_I19FCSd54=&xsec_source=app_share"
   ```
   The link in that command is a real sample note that has already been read: it answers in about a second and costs 0 credits, so it is the right thing to run when the user has not given a link yet or you want to check the key. Then ask the user for the note they mean (in the app: 分享 → 复制链接) and run the same command with it. Share text with quotes or line breaks goes in on standard input: `printf '%s' "$SHARE_TEXT" | python3 {baseDir}/scripts/linkdigest.py --format json -`.
2. Answer in this order:
   - one paragraph on what the note says;
   - the points in `key_points`, each followed by where it comes from: the picture (`images[i]`, its `ocr` text or `description`) or the line of `caption` or `transcript` that says it. Number pictures from 1 as the reader sees them;
   - whatever the author gives as the conclusion, the recommendation or the list of products and prices, as the note states them.
3. A point you cannot find in `caption`, an image's `ocr`, or `transcript` is dropped or marked 「笔记里没有找到」. Do not keep it on the title's word.
4. Offer the full text (「要每张图的文字全文吗？」) and do not paste it unasked. Say what the read cost (last line of stderr).

Never invent a link or a note id. A made-up id answers `422 not_a_post`, and a link with `<...>` left in it answers `400 placeholder_link`; both carry a `sample_url` and cost nothing, but nothing is read either.

## With and without a key

| | What comes back | Cost |
| --- | --- | --- |
| No `LINKDIGEST_API_KEY` | A summary: title, author, key points, counts. Up to 2 a day per address. | free |
| With a key | Everything below | credits, see Price |

Sign-up gives 10 credits once, no card.

## What a full read holds

- `title`, `author`, `posted_at`, `caption` (the body) and the tags.
- `images`: one entry per picture, in order, each with `ocr` (the words in the picture) and `description` (what the picture shows). `ocr_text` at the top level is the same words as one list of lines.
- For a video note: `transcript`, the speech by segment with start times. It is speech recognition (`transcript_source: asr`), so names, numbers and brand names can be misspelt. Tell the user to check those before quoting.
- `key_points`: the points, written from the above.
- `comments`: the first few comments the share page itself carries, on reads that have them (an older cached read may not). Not the whole comment section.
- In Markdown (drop `--format json`): the same, plus likes, saves, comments and shares as of the read.

## When the note cannot be read

- 「当前笔记暂时无法浏览」 or "not on the web right now": Xiaohongshu shows this note only inside its app or to a signed-in browser. Retrying the same link returns the same answer and nothing is charged. Tell the user so; do not try other spellings of the link. The reader's own signed-in browser with the extension (https://linkdigest.dev/extension) can read the page they see.
- A creator's profile link is read as the profile, not as a note: the creator's card and the titles and like, save and comment counts of the notes on the page's first screen. Xiaohongshu gives a signed-out visitor no links to those notes, so none come back; to summarise one of them, ask the user for that note's own share link.
- A product page or a search page is not a note: ask for one note's share link.
- A deleted or private note cannot be read by anyone.

## Other jobs

- The full text of every picture, without a summary: `xiaohongshu-note-to-text`.
- Many notes at once into one table: `xiaohongshu-batch-export`.
- What an audience wants, objects to and asks, with checked quotes: `xiaohongshu-consumer-insight`.
- Posts about a topic from the last 30 days, with a cited brief: `xiaohongshu-douyin-last-30-days`.

## Price and limits

An image note is typically 1 to 2 credits; a video note is 1 credit plus 1 per started minute. A note someone already read is 0. Top-ups are one-time and never expire: 50 credits ¥9.9 (支付宝) / $1.50, 250 credits ¥36 / $5.

It reads one public note at a time. It does not sign in, does not use anyone's cookie, does not search, post, like or download pictures.
