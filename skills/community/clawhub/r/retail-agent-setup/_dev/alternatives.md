# Alternatives Considered

## Separate skill per step (not chosen)
**Why considered:** More modular; each step could be independently versioned and installed.
**Why rejected:** Too much friction for the target user (non-technical store owner). Installing
12 skills to set up one agent is a bad UX. Single-skill approach wins on simplicity.
**Revisit if:** Skills gain inter-dependency resolution (package.json-style) so a meta-skill
can auto-install its sub-skills.

---

## LLM-based CSV parsing instead of Python scripts (not chosen)
**Why considered:** No dependency install required; simpler for users.
**Why rejected:** LLMs are inconsistent on large structured data; token cost is prohibitive
for 500+ row catalogs; output schema varies across runs.
**Revisit if:** LLM context windows and structured output reliability improve to handle
10,000-row CSVs at < $0.01 reliably.

---

## Database backend for knowledge base (not chosen)
**Why considered:** Vector DB (Qdrant/Chroma) would enable semantic search over large catalogs.
**Why rejected:** Adds significant infrastructure complexity for a skill targeting SMB retail.
Most stores have < 1,000 SKUs; flat JSON in agent memory is sufficient.
**Revisit if:** A `retail-agent-pro` variant is built for large chains (10,000+ SKUs, multi-location).

---

## More than 6 preset roles (not chosen)
**Why considered:** Could enumerate 15+ retail roles (cashier, stock picker, area manager, etc.)
**Why rejected:** Too many choices creates decision paralysis. The 6 roles cover 90% of use cases.
The "All-in-One" role serves as a catch-all for small stores.
**Revisit if:** Usage data shows a common role type not covered (e.g., dedicated loyalty/CRM agent).

---

## Real-time sentiment analysis via external API (not chosen)
**Why considered:** External sentiment APIs (e.g., Baidu NLP) could score customer messages
and auto-escalate based on sentiment threshold.
**Why rejected:** Adds external API dependency, latency, and cost. The keyword-based
auto-escalation in Step 09 covers 95% of genuine escalation cases. LLM judgment handles
nuanced cases the keywords miss.
**Revisit if:** A high-volume customer service deployment needs sub-100ms escalation decisions.

---

## Per-channel persona (different name/tone for WeChat vs WeCom) (not chosen)
**Why considered:** Staff-facing agents should be more terse; customer-facing ones more warm.
**Why rejected:** Increases config complexity significantly. The role selection (Step 04) already
determines tone. A single persona config is easier for store owners to manage.
**Revisit if:** A "multi-role split" feature is requested — one agent instance serving both
staff and customer channels with channel-specific persona overrides.

---

## No launch threshold (just "launch when ready") (not chosen)
**Why considered:** Simpler UX — no score gate, just launch when the user feels ready.
**Why rejected:** Non-technical users underestimate readiness. Without a score gate,
agents go live with empty knowledge bases and create bad first impressions, leading to churn.
The 80-point threshold is a forcing function for quality.
