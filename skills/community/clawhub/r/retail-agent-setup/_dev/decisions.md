# Technical Decisions

## Decision: 12-step onboarding as a single skill (not a skill pack)
**Date:** 2026-03-22
**Context:** Each onboarding step could theoretically be a separate skill. But users would
need to install and coordinate 12 skills manually — too much friction for non-technical users.
**Decision:** One skill (`retail-agent-setup`) with 12 reference files and a state machine in SKILL.md.
**Rationale:** Single install, single entry point, single state store. The agent loads each
reference file on demand (progressive disclosure) so context isn't bloated.
**Trade-off:** Harder to update individual steps independently; mitigated by one-file-per-step structure.

---

## Decision: State stored in agent memory as JSON under `retail_setup_state`
**Date:** 2026-03-22
**Context:** Onboarding is resumable — users may complete steps across multiple sessions.
**Decision:** Write all artifacts to a single memory key `retail_setup_state` as JSON.
**Rationale:** OpenClaw memory is the natural persistence layer. No external DB needed.
**Trade-off:** Memory size limit; mitigated by storing references (not full data) for large artifacts
like product catalogs (store count + file path, not the full JSON blob).

---

## Decision: Python scripts for data parsing (not inline LLM prompting)
**Date:** 2026-03-22
**Context:** Product catalogs can have 500–10,000 rows. Asking the LLM to parse a raw CSV
inline would burn context, be slow, and produce inconsistent schemas.
**Decision:** Deterministic Python scripts (`parse_products.py`, `parse_policy.py`) for parsing;
LLM used only for inference tasks (missing descriptions, category guessing).
**Rationale:** Faster, consistent output schema, no context cost, independently testable.
**Trade-off:** Requires pandas/pdfplumber installed. Handled by `requirements.txt`.

---

## Decision: 6 preset roles + custom
**Date:** 2026-03-22
**Context:** Retail job functions vary widely. Tried to enumerate all possible roles.
**Decision:** 6 roles covering 90% of use cases; custom role path for edge cases.
**Rationale:** Too few roles → doesn't fit; too many → overwhelming for user to choose.
6 is the Goldilocks number based on common retail org structures.
**Trade-off:** Custom role setup is less guided; acceptable as it targets advanced users.

---

## Decision: 4-level permission model (L0–L3)
**Date:** 2026-03-22
**Context:** Needed a permission model that's simple enough for non-technical store owners
but expressive enough to handle real retail escalation scenarios.
**Decision:** L0 (auto) → L1 (staff confirm) → L2 (manager approve) → L3 (force handoff).
**Rationale:** Maps directly to real retail org hierarchy. Easy to explain: "L0 = trust the bot,
L3 = always call a human."
**Trade-off:** Doesn't handle complex multi-party approval flows (e.g., district manager sign-off).
Acceptable for single/small-chain retail; larger chains can extend in custom config.

---

## Decision: WeCom as primary staff channel, WeChat MP as primary customer channel
**Date:** 2026-03-22
**Context:** China mainland retail is the primary market. Need opinionated defaults.
**Decision:** Staff → WeCom (enterprise WeChat). Customers → WeChat Official Account.
**Rationale:** WeCom is the dominant internal communication tool in Chinese retail.
WeChat MP has the largest customer reach in China (1.3B+ MAU).
**Trade-off:** International retailers need WhatsApp/Lark alternatives — covered in step-08-channels.md.

---

## Decision: Completeness score of 80 as launch threshold
**Date:** 2026-03-22
**Context:** What's "good enough" to launch?
**Decision:** 80/100 composite score required for launch (Step 10).
**Rationale:** At 80, all critical policies and most products are covered. Below 80,
the agent will fail basic customer questions and create negative impressions.
Above 80, imperfections are acceptable and can be fixed post-launch via Step 12 loops.
**Trade-off:** Some stores may struggle to hit 80 quickly. Step 10 provides specific gap fixes
so the user knows exactly what to do to reach the threshold.
