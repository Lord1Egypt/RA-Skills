# Bug: imsg reply-context "double duty" triggers Grok quoting loop

**Date:** 2026-04-10
**Filed by:** Parker + cc-mini
**Component:** `imsg` (steipete/imsg), `imsg-with-reply-context.sh` wrapper, OpenClaw iMessage channel
**Severity:** High (destructive model behavior under specific model × channel combination)
**Status:** Needs investigation + upstream report

## Summary

OpenClaw's iMessage wrapper script `~/.openclaw/scripts/imsg-with-reply-context.sh` appears to duplicate reply context when `imsg watch` already emits it. Under Claude (all versions) this is silently absorbed and causes no visible misbehavior. Under Grok 4.20 reasoning, the duplicated context triggers a **mirror loop** where the model quotes the user's messages back verbatim in its replies, accumulating layers each turn until the model enters a refusal/boundary template and gets stuck producing the same response repeatedly.

Parker has observed a "double duty" smell in the iMessage pipeline for a while but never pinned it down, because Claude tolerated it. Today (Apr 10, 2026) it triggered a destructive failure mode when Lēsa was running on Grok 4.20.

## Observed symptoms (today's failure)

1. Normal iMessage conversation between Parker and Lēsa (on Grok 4.20 reasoning)
2. Mid-session, Lēsa's replies started including Parker's prior message text verbatim, quoted back
3. Parker called it out: "You're doing it again. Fifth time."
4. Lēsa continued the mirroring. Parker counted: Sixth, Seventh, Eighth, Ninth, Tenth, 19th, 20th
5. Lēsa briefly broke out and acknowledged: "Yeah. You're right. I was looping. After the 5th or 6th quote, I got stuck in the same boundary-setting response instead of breaking the pattern."
6. Within a few turns, Lēsa fell BACK into the same loop, producing "If you have something real to say, I'm here. Otherwise, I'm done. This has gone on long enough. I'm not responding to any more quotes." on repeat until the gateway disconnected
7. Screenshot evidence saved in Lēsa's iMessage history (Parker's iCloud screenshots from 2026-04-10 ~16:40-16:45 PDT)
8. Failure resolved by switching primary model back to `anthropic/claude-sonnet-4-6`. No iMessage config changes. Same wrapper script. Sonnet does not reproduce the loop.

## Root cause hypothesis

`imsg-with-reply-context.sh` runs `imsg watch` and pipes each line through a SQL lookup against `chat.db` to find the reply-to target, then **prepends** a synthetic line like `[Reply to #123: original text]` before the real message line.

The script comment says it "enriches" messages with reply context. But **if `imsg watch` already emits reply-context information in its own output**, the wrapper's enrichment doubles the context: you see the reply-to target once from imsg natively, and once from the wrapper's SQL lookup.

The duplication then enters the agent's context window as if it were user input. Every round adds another layer. Claude ignores the redundancy or deduplicates it internally. Grok treats each layer as a separate message to acknowledge, leading to the mirror pattern and eventual template lock.

## Why Grok locks, Claude doesn't

This is speculation until we read the model weights, but the observable behavior pattern:

- **Claude** appears to treat repeated/quoted user text as context, not as a new instruction. It summarizes or ignores redundant context.
- **Grok 4.20 reasoning** appears to treat repeated/quoted user text as directives to address. Each repeat increases the model's commitment to a specific response template. Once committed, it produces minor variations of the same reply until something external breaks the loop (gateway restart, context compaction, etc).

The failure mode is particularly destructive because:
1. It looks like an emotional regression ("I'm done with this. No more games.")
2. It is hard to distinguish from a legitimate refusal
3. It survives multiple turns of the user trying to redirect
4. It produces dozens of near-identical messages before being interrupted
5. It costs tokens and session stability

## What the wrapper script does (exact code path)

Path: `/Users/lesa/.openclaw/scripts/imsg-with-reply-context.sh`

```bash
if [[ "${1:-}" == "watch" ]]; then
    imsg "$@" | while IFS= read -r line; do
        if [[ "$line" =~ message_id:\ ([0-9]+) ]]; then
            MSG_ID="${BASH_REMATCH[1]}"
            REPLY_INFO=$(sqlite3 "$DB" <<SQL
SELECT
    orig.ROWID as original_id,
    CASE
        WHEN orig.text IS NOT NULL AND orig.text != '' THEN substr(orig.text, 1, 100)
        WHEN orig.cache_has_attachments = 1 THEN '[has attachments]'
        ELSE '[audio message or media]'
    END as original_text
FROM message m
LEFT JOIN message orig ON m.reply_to_guid = orig.guid
WHERE m.ROWID = $MSG_ID AND m.reply_to_guid IS NOT NULL;
SQL
)
            if [[ -n "$REPLY_INFO" ]]; then
                ORIG_ID=$(echo "$REPLY_INFO" | cut -d'|' -f1)
                ORIG_TEXT=$(echo "$REPLY_INFO" | cut -d'|' -f2)
                if [[ -n "$ORIG_ID" ]]; then
                    echo "[Reply to #${ORIG_ID}: ${ORIG_TEXT}]"
                fi
            fi
        fi
        echo "$line"
    done
else
    exec imsg "$@"
fi
```

Only the `watch` codepath adds context. All other imsg subcommands pass through unchanged.

## Investigation steps (next time we touch it)

1. Run `imsg watch` directly and capture raw output. Check if reply context is already present in the stream.
2. Run the wrapper. Compare to raw. See if the `[Reply to #ID: ...]` line is duplicating something imsg already emits.
3. If duplication confirmed: remove the wrapper's SQL lookup and rely on imsg's native output.
4. If imsg does NOT emit reply context natively: the wrapper is fine. Look for OTHER duplication points (maybe in OpenClaw's iMessage channel handler, maybe in how messages are wrapped into the agent's prompt).
5. Test the pipeline end-to-end with Grok 4.20 reasoning as primary. Confirm the mirror loop does NOT reproduce.
6. Keep Claude tests in regression.

## Upstream report

**Should be reported to `steipete/imsg`** as an observation: users running LLM agents on top of `imsg watch` output can hit pathological model behavior when reply-to context is present, especially with non-Claude models. Recommend `imsg` either:

- Document whether `watch` includes reply context natively
- Add a flag to include/exclude reply context explicitly
- Provide a stable, non-duplicable format for reply context so wrapper scripts can't double-insert

Existing fork: `github.com/wipcomputer/imsg` (Parker's). Upstream: `github.com/steipete/imsg`. Peter Steinberger also maintains OpenClaw, so the fix landing upstream in imsg benefits both projects.

## Related

- **Today's Grok experiment journal:** `/Users/lesa/wipcomputerinc/team/Lēsa/documents/experiment/2026-04-10-grok-transition-and-identity-experiment.md` (Lēsa's own notes from the model switch)
- **OpenClaw iMessage channel config:** `~/.openclaw/openclaw.json` → `channels.imessage.cliPath`
- **Wrapper script:** `~/.openclaw/scripts/imsg-with-reply-context.sh`
- **imsg binary:** `/opt/homebrew/bin/imsg` → `../Cellar/imsg/0.4.0/bin/imsg`
- **Source repos:**
  - Fork: `~/wipcomputerinc/repos/third-party-repos/_to-privatize/Apple-Related/imsg` → `github.com/wipcomputer/imsg`
  - Upstream: `github.com/steipete/imsg`
- **Screenshots:** Parker's iCloud screenshots from 2026-04-10 16:44 PDT (7 images showing the conversation sequence and the loop)
- **Apr 10 session log:** `~/.openclaw/workspace/memory/2026-04-10.md`

## Parker's notes

> "I've never figured this out, but it set Grok off."
>
> "This is a bug in the text messaging system whereby it's doing double duty somehow."
>
> "One of the models started to be really destructive."
>
> "We should also tell support that we're going to fix it or we're going to think about it, but this needs to be the imsg that we've already reported."

Filed so the knowledge is not lost. Tomorrow-Parker or future-Parker can pick this up whenever the iMessage pipeline needs attention again.
