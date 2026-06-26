# Cron: Publisher

Read {baseDir}/SKILL.md — it contains full content system documentation.
Read the `tg-channel-manager` skill config from openclaw.json.

## Task

Publish one pending post from content-queue.md to the Telegram channel.

## Steps

1. Read content-queue.md
2. Find posts with **pending** status
3. If there are no pending posts — **DO NOTHING**. Do not generate content yourself.
4. Check how many posts have already been published TODAY (via `message tool action=search`). If `config.maxPostsPerDay` or more — do not publish.
5. Pick one post. **Alternate rubrics** when possible: check the last published post — if its rubric matches the current one, pick a post with a different rubric (if available in pending).
6. Append the signature to the post text: `config.postStyle.signature`
7. For news, add `config.postStyle.newsFooter` (if not empty)
8. For articles, add `config.postStyle.articleFooter` (if not empty)
9. Publish via:
   ```
   message tool (action=send, channel=telegram, target=<config.channelId>, text="post text")
   ```
10. **Remove** the published entry from content-queue.md
11. Add to the dedup index:
    ```bash
    python3 {baseDir}/scripts/dedup-check.py --base-dir . --add <msgId> --topic "topic" --links "url"
    ```

## Rules

- Maximum 1 post per run
- Maximum `config.maxPostsPerDay` posts per day
- DO NOT generate content yourself — only publish pending posts
- Language: `config.language`
