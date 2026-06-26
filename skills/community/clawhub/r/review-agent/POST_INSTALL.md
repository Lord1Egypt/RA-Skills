# 🔧 POST-INSTALL · Admin checklist

_You just installed `review-agent`. Read this ONCE and follow the 3 steps. Everything else is automatic._

## What you just got

A **per-peer review coach** for Lark. Every Requester who DMs your Lark bot gets a dedicated subagent that runs four-pillar review + Responder simulation + Q&A loop, then hands you a 6-section decision brief.

## Was it a ClawHub install or a bundle install?

**If you ran `clawhub install review-agent` (or `openclaw skills install review-agent`)** — you have the SKILL but you're missing the workspace template, `openclaw.json` patches, and the openclaw core patch that makes per-peer isolation work. Do this next:

```bash
git clone https://github.com/jimmyag2026-prog/review-agent-skill ~/code/review-agent-skill
cd ~/code/review-agent-skill
bash install.sh --enable-only
```

**If you ran `bash install.sh` from the bundle repo** — you're already set up. Skip to step 2.

## 3-step Admin checklist

### 1. Apply the openclaw source patch (one-time, until openclaw natively supports template-clone)

openclaw core's feishu `dynamicAgentCreation` creates a new peer workspace but **seeds it with a generic "memorist" persona by default**, not with our review-coach persona. The patch makes our template win:

```bash
python3 ~/code/review-agent-skill/install/openclaw_patches/feishu_seed_workspace_patch.py
openclaw gateway restart
```

Idempotent; safe to re-run after `openclaw update` overwrites the file.

### 2. Personalize the global Responder profile

Your review standards, pet peeves, decision style, "always-ask" questions. Bad default → generic reviews.

```bash
bash ~/code/review-agent-skill/assets/admin/setup-responder.sh
# opens ~/.openclaw/review-agent/responder-profile.md in $EDITOR
```

### 3. Restart and first-test

```bash
openclaw gateway restart
```

Then have a colleague (or a test Lark account) DM your bot a proposal or Lark wiki link. You should see in the gateway log:

```
creating dynamic agent "feishu-ou_xxx..."
review-agent: seeded <workspace>
dispatching to agent (session=agent:feishu-ou_xxx:main)
dispatch complete (queuedFinal=true, replies=1)
```

The Lark account receives a persona-correct reply. Done.

## Channel compatibility

Per-peer subagent auto-spawn is only supported on **feishu** (openclaw core) and **wecom** (via `@sunnoy/wecom` plugin). Other channels fall back to shared-main-agent mode:

| Channel | Per-peer subagent | Behavior |
|---|---|---|
| feishu / lark | ✅ | v2 full architecture |
| wecom | ✅ | v2 full architecture |
| telegram | ❌ | skill runs in main agent, all Requesters share context |
| whatsapp | ❌ | same |
| discord / slack / iMessage | ❌ | same |

Non-feishu/wecom channels are usable but without per-peer context isolation. For those you probably want hermes v1.x instead (`github.com/jimmyag2026-prog/review-agent`).

## Lark app scopes you'll likely need

For review-agent to pre-fetch Lark wiki/docx URLs the Requester sends, grant these in your Lark app console:

- `im:message:send_as_bot`  (outbound replies)
- `im:message`              (inbound reception)
- `docx:document`            (read Lark docx)
- `wiki:wiki:readonly`       (read Lark wiki)
- `drive:file` + `drive:drive` (share Lark docs to Responder + Requester)

Without these, the subagent will politely ask the Requester to paste text instead.

## Day-to-day admin

```bash
# check for updates
bash ~/.openclaw/skills/review-agent/update.sh --check

# update to latest
bash ~/.openclaw/skills/review-agent/update.sh

# dashboard
python3 ~/code/review-agent-skill/assets/admin/dashboard-server.py
# then browse http://127.0.0.1:8765

# remove a peer (e.g., colleague who left)
bash ~/code/review-agent-skill/assets/admin/remove-peer.sh ou_xxxxxxxx

# uninstall (keep sessions)
bash ~/.openclaw/skills/review-agent/uninstall.sh --yes

# uninstall everything INCLUDING all peer data (irreversible)
bash ~/.openclaw/skills/review-agent/uninstall.sh --yes --purge --revert-config
```

## Troubleshooting

- **`replies=0` on dispatch_complete** → subagent's `message` tool call has wrong `target`. Check the subagent's jsonl for bare open_ids. Our SOUL.md forbids this but older sessions may have cached. Clear: `rm -f ~/.openclaw/agents/feishu-ou_*/sessions/*.jsonl` then re-test.
- **Subagent replies with "Hey I just came online, who am I?"** → the feishu-seed patch didn't land. Run step 1 again and confirm `grep "review-agent local patch" /opt/homebrew/lib/node_modules/openclaw/dist/monitor-D9C3Olkl.js` returns a line.
- **"Thinking Process:" shows up in Lark replies** → SOUL.md didn't load. Check `~/.openclaw/workspace-feishu-<open_id>/SOUL.md` exists and contains "不要填 target 字段".
- **Each DM triggers a new `creating dynamic agent` log line** → harmless. openclaw re-spawns per-message due to an internal consistency quirk. The cp -R seed is idempotent; your workspace data is preserved.
- **`Access denied ... wiki:wiki:readonly`** → grant the Lark app the wiki scope (see "Lark app scopes" above).

## Full docs

- Monorepo (history + v1 hermes variant + design docs): https://github.com/jimmyag2026-prog/review-agent
- Standalone skill bundle: https://github.com/jimmyag2026-prog/review-agent-skill
- ClawHub: https://clawhub.com/skills/review-agent
- Field notes (every bug we've hit): `openclaw-v2/docs/FIELD_NOTES.md` in the monorepo
