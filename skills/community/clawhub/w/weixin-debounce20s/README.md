# weixin-debounce20s

**Type:** guidance-only setup skill. It contains **no patch files and installs no plugin
package**. When the agent runs it, it follows `SKILL.md` and **modifies the WeChat channel
plugin already installed on your machine** so that burst messages are debounced (20s
**trailing window**: every mergeable text restarts a 20-second quiet window; the batch is
submitted once 20 seconds have passed since the last text; a single text also waits the full
20 seconds).

## How it gives you the capability

The agent, following `SKILL.md`:

1. Locates the local WeChat plugin (`openclaw plugins inspect openclaw-weixin --json`) and
   records its version; already-implemented installs are only verified (idempotent);
2. Implements the specified behavior in the plugin's inbound text path (buffer + restartable
   timer + generation guard, 8-message / 6000-char early flush, media/slash handled
   immediately, serial dispatch);
3. Asks for your explicit consent and **backs up** every file it modifies;
4. Restarts the gateway;
5. Verifies via logs (`debounce: buffered … windowMs=20000`) and a live burst test.

Upstream plugin upgrades overwrite the change — re-run the skill to re-apply. Rollback =
restore the backup from step 3 (or reinstall upstream).

Files: `SKILL.md` (spec + execution), `README.md` / `README-zh.md`, `LICENSE` (MIT).

## Usage (fresh machine)

```bash
openclaw skills install @yechang1450/weixin-debounce20s
# then tell ClawBot (WeChat or CLI): 启用防抖 / 防抖没生效
```

The agent always asks before modifying plugin files, and backs them up first.

## Trigger words (narrow, plugin-scoped)

启用微信防抖 / 防抖没生效 / openclaw-weixin 防抖

The skill only runs when the user explicitly asks to enable or fix debounce for the
`openclaw-weixin` channel, and it asks for confirmation before touching any file. It never
runs writes or builds with elevated privileges.
