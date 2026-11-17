---
name: remember-legal-research
description: Case and research memory for legal work — holdings, citations, and reasoning chains that survive across sessions. Use when an agent assists with legal research and must not lose the thread of a case. Requires a BlueColumn API key (bc_live_*).
---

# Remember Legal Research — BlueColumn Skill

Legal research is a chain of reasoning. If the chain breaks, the work is lost. This skill stores each link — the question, the source, the holding, the citation — so research builds on itself instead of restarting.

## Log the research thread

Store each finding with the question it answers, the source, and the citation. Cite like a lawyer: name, reporter, pin.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "RESEARCH: Is a clickwrap enforceable in the 9th Cir.? Berman v. Freedom Financial Network, 2019 WL 123456, at *4 — yes, if conspicuous and user had reasonable notice. Distinguish: Nguyen v. Barnes & Noble (hover-over hyperlink insufficient).", "title": "legal - clickwrap 9th Cir"}'
```

## Resume the thread

At the start of any research session, recall where the thread left off.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What legal research is in progress and what are the open questions?"}'
```

## Research workflow

1. **State the question** — store the precise issue before reading anything.
2. **Log each source** — authority, holding, and why it matters (or why it is distinguishable).
3. **Note open questions** — mark what is still unresolved so the next session picks up cleanly.
4. **Synthesize** — when the thread resolves, store the conclusion and the chain that supports it.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "OPEN QUESTION: does state UDAP law add a separate damages theory here? Researching WA RCW 19.86 next.", "tags": ["legal", "open-question"]}'
```

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
