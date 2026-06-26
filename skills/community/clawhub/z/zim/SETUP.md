# Zim WhatsApp Agent — OpenClaw Setup

## Overview

The Zim WhatsApp agent is integrated into OpenClaw via:
1. A **skill registration** (symlinked into `~/.openclaw/skills/zim`)
2. A **wrapper script** (`scripts/zim-wa.sh`) that OpenClaw agents call via `exec`
3. **Stateful conversation** persisted in SQLite at `data/whatsapp_state.db`

## Architecture

```
WhatsApp Message
  → OpenClaw (Pimy / main agent)
  → Recognizes travel intent (Zim skill matched)
  → exec: bash zim-wa.sh "<message>" "whatsapp:<phone>"
  → Zim WhatsApp Agent (Python)
  → Returns JSON response
  → Pimy sends response back via WhatsApp
```

## What was configured

### 1. Skill Registration
- Symlinked `~/.openclaw/skills/zim → /home/ubuntu/.openclaw/workspace/zim`
- OpenClaw discovers skills from `~/.openclaw/skills/` and `/usr/lib/node_modules/openclaw/skills/`
- The Zim `SKILL.md` frontmatter triggers on travel-related queries

### 2. WhatsApp Handler Script
- **`scripts/zim-wa.sh`** — Shell wrapper, sets env vars, invokes Python handler
- **`scripts/zim-whatsapp-handler.py`** — Python bridge to `ZimWhatsAppAgent`
- Uses the `.venv` Python environment in the zim project directory
- Environment variables auto-set: `TRAVELPAYOUTS_TOKEN`, `TRAVELPAYOUTS_MARKER`

### 3. State Store Fix
- Fixed `SQLiteStateStore` to handle `datetime` serialization from Pydantic models
- Added `_DateTimeEncoder` class in `zim/state_store.py`
- State DB at `data/whatsapp_state.db` (auto-created)

### 4. SKILL.md Updated
- Added "WhatsApp Conversational Agent" section with invocation instructions
- Documents when to use WhatsApp agent vs CLI vs shell scripts

## How to use

### From OpenClaw agent (exec tool):
```bash
bash /home/ubuntu/.openclaw/workspace/zim/scripts/zim-wa.sh "Find flights DXB to CPH May 1" "whatsapp:+971544042230"
```

### Response format:
```json
{"response": "Found 3 flights...", "success": true}
```

### Send the `response` text back to the WhatsApp user.

## Conversation flow
1. User sends travel request → Zim returns search results (up to 3 options)
2. User replies 1/2/3 → Zim shows selection, asks YES/NO
3. YES → Booking confirmation + Aviasales/Hotellook deeplink
4. CANCEL at any point → Resets conversation

## Test results (2026-04-13)
- ✅ Flight search: "Find me a flight from Dubai to London on May 10" → returned results
- ✅ Option selection: "1" → showed flight details, asked for confirmation
- ✅ Booking confirmation: "yes" → returned Aviasales booking deeplink
- ⚠️ Hotel intent parsing: Some natural phrasings don't extract check-in date correctly
- ⚠️ Car intent parsing: "Rent a car Dubai Airport" doesn't extract pickup location
- These are Zim intent parser issues, not integration issues

## Environment variables
| Variable | Source |
|----------|--------|
| `TRAVELPAYOUTS_TOKEN` | Set in environment (required) |
| `TRAVELPAYOUTS_MARKER` | Set in environment (required for affiliate attribution) |

## Files modified/created
- `scripts/zim-wa.sh` — NEW: Shell wrapper for OpenClaw exec
- `scripts/zim-whatsapp-handler.py` — NEW: Python bridge script
- `zim/state_store.py` — MODIFIED: Added `_DateTimeEncoder` for datetime serialization
- `SKILL.md` — MODIFIED: Added WhatsApp agent section
- `SETUP.md` — NEW: This file

## Next steps to get Zim fully live on WhatsApp

### Required (for OpenClaw to discover & use the skill)
1. **Restart OpenClaw gateway** so it picks up the new skill symlink
2. **Test end-to-end**: Send a travel message on WhatsApp and verify Pimy routes it through Zim

### Recommended improvements
3. **Fix intent parser**: Hotel and car search don't reliably extract dates/locations from natural language
4. **Dedicated agent**: Consider adding a `zim` agent in OpenClaw config (`agents.list`) with WhatsApp channel routing for travel-only messages
5. **Stripe integration**: Set up `STRIPE_SECRET_KEY` for actual payment flows
6. **TTL tuning**: Default session TTL is 1 hour — may need extension for slow WhatsApp conversations
7. **Error monitoring**: Add logging/alerting for failed Travelpayouts API calls
