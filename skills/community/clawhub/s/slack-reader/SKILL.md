---
name: slack-thread
description: Read and summarize Slack channel history and thread conversations. Use when receiving Slack links (https://...slack.com/archives/...) or requests to view channel/thread/reply conversations, summarize discussions, or check recent messages in a channel.
---

# Slack Thread Reader

Script to fetch Slack channel history, threads, and individual replies.
Output is LLM-friendly format: one message per line, ascending order (oldest→newest), minimal whitespace.

## Script Location

`scripts/slack-thread.sh` (entry point) → `scripts/slack-thread.py` (main logic)

## Slack Link Structure

```
https://abstract-im.slack.com/archives/C0AE4MGLNUU
                                        ^^^^^^^^^^^
                                        Channel ID

https://abstract-im.slack.com/archives/C0AE4MGLNUU/p1770775935866499
                                        ^^^^^^^^^^^  ^^^^^^^^^^^^^^^^
                                        Channel ID    Message ts (parent)

https://abstract-im.slack.com/archives/C0AE4MGLNUU/p1770776063826049?thread_ts=1770775935.866499&cid=C0AE4MGLNUU
                                        ^^^^^^^^^^^  ^^^^^^^^^^^^^^^^            ^^^^^^^^^^^^^^^^     ^^^^^^^^^^^
                                        Channel ID    Reply ts (child)           Parent ts            Channel ID (duplicate)
```

- **pTS**: Timestamp in URL path. `p` + 10 digits (seconds) + 6 digits (microseconds). API uses `seconds.microseconds` format (e.g., `p1770775935866499` → `1770775935.866499`)
- **thread_ts**: Parent message ts of the thread. If present, it's a reply link
- **cid**: Duplicate channel ID info (for app deep links, ignored by script)
- **ts**: Unique ID and timestamp of a Slack message. Unique within a channel

## Usage

### 3 Modes

| Link Format | Mode | Behavior |
|-----------|------|------|
| `/archives/CHANNEL` | Channel | Fetch channel history |
| `/archives/CHANNEL/pTS` | Thread | Fetch full thread with ts as parent |
| `/archives/CHANNEL/pTS?thread_ts=...` | Reply | Fetch single reply only |

### Read Thread
```bash
scripts/slack-thread.sh https://abstract-im.slack.com/archives/CHANNEL/pTIMESTAMP
scripts/slack-thread.sh <channel-id> <thread-ts>
```

### Read Channel History
```bash
scripts/slack-thread.sh https://abstract-im.slack.com/archives/CHANNEL
scripts/slack-thread.sh <channel-id>
scripts/slack-thread.sh <channel-id> --limit 100
```

### Channel History + Thread Replies (Full)
```bash
scripts/slack-thread.sh <channel-id> --with-threads
scripts/slack-thread.sh <channel-id> --with-threads --thread-limit 5
```

### Read Single Reply
```bash
scripts/slack-thread.sh https://abstract-im.slack.com/archives/CHANNEL/pREPLY_TS?thread_ts=PARENT_TS&cid=CHANNEL
```

## Workflow

1. When given a Slack link or channel ID, use this script to fetch conversation history.
2. **⚠️ If the link type and request content don't match, always ask a clarifying question.**
   - Link formats: `/archives/CHANNEL` = channel, `/archives/CHANNEL/pTS` = thread, `/archives/CHANNEL/pTS?thread_ts=...` = reply
   - Example: If given a thread link but asked to "fetch channel history", ask for clarification
3. **When asked to summarize channel history**: Confirm "Should thread replies be included?" before deciding on `--with-threads`.
4. Summarize the fetched content or deliver it as-is.

## Options

| Option | Description | Default |
|------|------|--------|
| `--limit N` | Number of channel history messages (0=all) | 0 (all) |
| `--from YYYY-MM-DD` | Messages after this date only (channel mode) | none |
| `--to YYYY-MM-DD` | Messages up to this date only (channel mode) | none |
| `--with-threads` | Include thread replies inline | off |
| `--thread-limit N` | Max replies per thread (0=all) | 0 |
| `--desc` | Descending order (newest→oldest) | off (default ascending) |

## Output Format

### Sort Order: Ascending (oldest → newest, conversation flow)

Use `--desc` to switch to descending order.

### Reply Mode
```
[reply] ch:C0AE4MGLNUU(#dev-backend) thread:1770775935.866499
[2026-03-04T14:32:28|1770776063.826049] user1: Confirmed, will apply the fix
```

### Thread Mode
```
[thread] ch:C0AE4MGLNUU(#dev-backend) parent:1770775935.866499 replies:144 range:2026-02-25~2026-03-04
[participants] user1, user2, user3, absbot (4)
[2026-02-25T22:57:27|1770775935.866499] user1: Parent message (oldest)
[2026-03-04T14:31:05|1770776005.123456] user1: Second message
[2026-03-04T14:32:28|1770776063.826049] absbot: Latest message text 📎file.png [:thumbsup:user2,user3]
```

### Channel Mode
```
[channel] ch:C0AE4MGLNUU(#dev-backend) msgs:200 threads:3
[participants] user1, user2, user3, absbot (4)
[2026-03-04T14:29:00|1770775740.111111] user1: Message text
[2026-03-04T14:32:28|1770775948.222222] absbot: Message text [thread replies:13 latest:2026-03-04T16:00:00]
 [2026-03-04T14:30:00|1770775800.333333] user3: Thread reply (older)
 [2026-03-04T14:31:00|1770775860.444444] user2: Thread reply (newer)
```

### Output Elements

| Element | Format | Example |
|------|------|------|
| Timestamp+ID | ISO 8601 + ts | `[2026-02-11T17:45:56\|1770775935.866499]` |
| Sender | Real name (including bots) | `user1:`, `absbot:` |
| Mention | @name | `@user3` |
| Reaction | [:emoji:names] | `[:thumbsup:user2,user3]` |
| Attachment | 📎filename userID/fileID | `📎image.png U0ADM19GY6N/F0ADRC9PEHL` |
| Thread info | [thread replies:N latest:time] | `[thread replies:13 latest:2026-03-04T16:00:00]` |
| Inline reply | 1-space indentation | ` [ts] user: text` |
| Participants | [participants] names (N) | `[participants] user1, user2 (2)` |
| Channel name | ch:ID(#name) | `ch:C0AE4MGLNUU(#dev-backend)` |

### LLM Optimization

- Default ascending: LLM naturally follows conversation flow in chronological order
- Newlines/consecutive spaces within messages → collapsed to single space
- No decorative characters (📌, ---, ├ └ etc. removed)
- No blank lines (messages separated by single newline)
- Thread mode: fetches all messages without omission (automatic pagination)
- Each message includes ts (unique ID): enables referencing specific messages
- Attachment permalink shortened: shows only userID/fileID (removes URL-encoded filename duplication)
  - Output: `📎filename U0ADM19GY6N/F0ADRC9PEHL`
  - Full URL reconstruction: `https://abstract-im.slack.com/files/{userID}/{fileID}`

## Technical Details

### Pagination & Deduplication
- `conversations.replies` API duplicates parent message at `[0]` on every page
- Automatic deduplication via `seen_ts` set
- Cursor-based pagination collects all replies without omission
- `--limit` applies only in channel mode (thread mode always fetches all)

### Parallel Processing
- Channel name lookup and data fetch run concurrently (saves 1 round-trip)
- `--with-threads` fetches thread replies in parallel with up to 8 workers
- User name lookups also run in parallel with up to 5 workers

### User Cache
- User ID → real name cache at `~/.cache/slack-reader/users.json` (TTL 24 hours)
- Cached users are resolved instantly without API calls

### Rate Limit
- On 429 response, waits for `Retry-After` header duration then retries (max 3 attempts)
- Rate limit wait timestamp shared across parallel workers (prevents thundering herd)

### Error Handling
- In `--with-threads`, if an individual thread fetch fails, only that thread is skipped; the rest outputs normally
- Summary of failed thread count and ts printed to stderr

## Notes

- Bot must be a member of the channel. On `channel_not_found`, suggest `/invite @absbot`.
- Fetching only channel history without `--with-threads` may miss conversations inside threads.
