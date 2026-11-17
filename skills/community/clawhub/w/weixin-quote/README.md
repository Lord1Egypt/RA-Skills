# weixin-quote

**Type:** guidance-only setup skill. It contains **no patch files and installs no plugin
package**. When the agent runs it, it follows `SKILL.md` and **modifies the WeChat channel
plugin already installed on your machine** so that quoting a bot reply injects the full
quoted text into the model context.

## How it gives you the capability

The agent, following `SKILL.md`:

1. Locates the local WeChat plugin (`openclaw plugins inspect openclaw-weixin --json`) and
   records its version; already-implemented installs are only verified (idempotent);
2. Implements the specified behavior: record the server `message_id` (exact string) on send;
   on a quote, resolve by id proximity (≤1000) with a content-substring fallback; inject the
   full quoted text; mark unresolved quotes explicitly (never guess);
3. Handles the three required pitfalls — ids exceed `Number.MAX_SAFE_INTEGER` (use
   BigInt/string compare), timestamps are not a reliable primary key, and the index must
   persist across restarts (e.g. a small SQLite index);
4. Asks for your explicit consent and **backs up** every file it modifies;
5. Restarts the gateway and verifies via `[send-resp]` / `[quote-hit]` logs.

Upstream plugin upgrades overwrite the change — re-run the skill to re-apply. Rollback =
restore the backup from step 4 (or reinstall upstream).

Files: `SKILL.md` (spec + execution), `README.md` / `README-zh.md`, `LICENSE` (MIT).

## Usage (fresh machine)

```bash
openclaw skills install @yechang1450/weixin-quote
# then tell ClawBot: 启用引用 / 引用没生效
```

The agent always asks before modifying plugin files, and backs them up first.

## Trigger words (narrow, plugin-scoped)

启用微信引用上下文 / 修复 openclaw-weixin 引用匹配

The skill only runs when the user explicitly asks to enable or fix quote-context for the
`openclaw-weixin` channel, and it asks for confirmation before touching any file. It never
runs writes or builds with elevated privileges, and the retained quote index is local,
owner-only readable, with enforced expiry and caps.
