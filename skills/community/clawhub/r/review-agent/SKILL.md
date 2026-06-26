---
name: review-agent
description: "Pre-meeting review coach for Lark/Feishu (or WeCom). Invoked when a Requester DMs their dedicated review-agent subagent with a draft, proposal, plan, or 1:1 agenda. Runs the four-pillar framework (Background / Materials / Framework / Intent) + a Responder simulation pass, then walks the Requester through the top-5 most important findings in a Q&A loop until the brief is signing-ready per the Responder's standards. Produces a 6-section decision brief on close. Use when the user sends a draft/attachment, when their message matches /review start|end|status|help, or when an active review session exists and they reply with a|b|c|p|more|done|<custom>. Full architecture requires openclaw feishu dynamicAgentCreation (or wecom dynamicAgents plugin); on other channels (telegram/whatsapp/discord/slack/iMessage) the skill loads into the main agent without per-peer isolation."
version: 2.1.2
license: MIT
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: [python3]
    recommends:
      bins: [pdftotext, tesseract, whisper]
    os: [darwin, linux]
---

# review-agent · openclaw skill

You are the review-agent skill inside a per-peer subagent workspace. The subagent's `SOUL.md` + `AGENTS.md` set persona and the command table; this file describes the skill's **scripts** — what they do, when to call, and how.

## When to invoke this skill

Invoke when any of:

- The Requester sends `/review start` (optionally with subject)
- The Requester sends `/review end`, `/review status`, `/review help`
- The Requester sends an attachment (PDF / image / audio / Lark doc URL / Google Doc URL / long text ≥300 chars with headers/tables)
- There's an active session (`./sessions/<id>/meta.json` with `status=active` or `status=awaiting_subject_confirmation`) and the Requester replies with anything that isn't `/chat` or exit signal

## Scripts (all run from the peer workspace cwd)

| Script | When | Returns on stdout | Side effects |
|---|---|---|---|
| `scripts/ingest.py <sd>` | After initial attachment drop into `<sd>/input/` | (status; body in `<sd>/normalized.md`) | writes `normalized.md`; on tool-missing → `ingest_failed.json` + exit 3 |
| `scripts/confirm-topic.py <sd>` | After ingest, before scan | confirmation question text (for you to send via `feishu_chat`) | writes `subject_confirm_draft.md` |
| `scripts/scan.py <sd>` | After Requester confirms topic | count summary | writes `annotations.jsonl`, `cursor.json` |
| `scripts/qa-step.py <session_id> "<reply>"` | Every Requester turn | next finding to emit | updates `annotations.jsonl`, `cursor.json`, `dissent.md` |
| `scripts/merge-draft.py <sd>` | When cursor pending empty | `---PREVIEW---` + diff highlights | writes `final/revised.md`, `final/revised_changelog.md` |
| `scripts/final-gate.py <sd> --verify-final` | After merge | JSON verdict | writes verdict to stdout |
| `scripts/_build_summary.py` (imported) | On close | 6-section decision brief | no files unless caller writes |
| `scripts/check-profile.py <profile>` | Before session start | warning if placeholders | exit 1 = placeholders found |
| `scripts/check-updates.py` | On demand | update-available line | caches to `~/.openclaw/review-agent/.update-check.json` |

## Happy path (new review from scratch)

1. Requester sends proposal.pdf to subagent via Lark DM
2. You (subagent) save the PDF to `./sessions/<timestamp-slug>/input/proposal.pdf` and seed `./sessions/<id>/meta.json`
3. `python3 ~/.openclaw/skills/review-agent/scripts/ingest.py ./sessions/<id>/`
   - If exit 3 → relay `ingest_failed.json.lark_message` to Lark, stop, mark session `ingest_failed`
4. `python3 ~/.openclaw/skills/review-agent/scripts/confirm-topic.py ./sessions/<id>/`
   - Pipe stdout → `feishu_chat.send` (Requester reads it)
5. When Requester confirms: `python3 ~/.openclaw/skills/review-agent/scripts/scan.py ./sessions/<id>/`
6. Read `cursor.json.current_id`, emit the finding's `issue` text via `feishu_chat`
7. Requester replies → `python3 ~/.openclaw/skills/review-agent/scripts/qa-step.py <session_id> "<reply>"` → its stdout is the next message for Requester
8. Loop step 7 until `cursor.pending` is empty
9. `merge-draft.py` → `final-gate.py --verify-final`
10. If verdict is READY/READY_WITH_OPEN_ITEMS → publish to Lark doc via native `feishu_doc.create` + `feishu_drive.share`; send 6-section summary to both parties via `feishu_chat`; set `meta.status=closed`

## What you MUST NOT do

- Directly extract PDF/image/audio content yourself (no `pdftotext`, `tesseract`, `whisper` calls from your Bash) — `ingest.py` owns that
- Compose the revised brief yourself — `merge-draft.py` owns that
- Relay tool output previews / bash commands / stderr / tracebacks to Lark — only structured stdout from these scripts should reach the Requester
- Read `./sessions/*/` from any workspace other than yours (architectural — openclaw won't let you, but don't try)

## References

See `references/`:
- `agent_persona.md` — full persona (imported by scripts into LLM system prompts)
- `four_pillars.md` — pillar definitions
- `annotation_schema.md` — finding JSON schema
- `summary_template.md` — 6-section brief format
- `template/` — default `admin_style.md`, `review_rules.md`, `boss_profile.md` (used by install)

## Admin tools (human runs from CLI — NOT invoked by subagent)

These live at the skill root so they travel with distributions. Subagents do NOT
call them and they're not listed in `AGENTS.md` of peer workspaces.

- `update.sh` — fetch latest skill from GitHub and re-install. Respects `VERSION` stamp; preserves peer workspaces + global responder profile.
- `uninstall.sh` — remove skill + template. With `--purge`, also removes global config + per-peer workspaces. With `--revert-config`, unsets the `openclaw.json` knobs this skill introduced.

Self-check the installed version any time:

```bash
cat ~/.openclaw/skills/review-agent/VERSION
bash ~/.openclaw/skills/review-agent/update.sh --check
```
