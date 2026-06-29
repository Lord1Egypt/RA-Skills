# vmware-debug Capabilities

Read-only, offline incident correlation. No network, no credentials, no writes.

| Tool | What it returns | Typical response tokens |
|---|---|---|
| `incident_timeline` | `{event_count, window, spikes:[{start,end,count,zscore}], hypotheses:[{category, score, summary, evidence_count, first_seen, last_seen, sample_text, suggested_check}], next_checks:[...]}` | 300–2000 (scales with hypotheses) |
| `list_symptom_categories` | `[{category, example_keywords, suggested_check}]` | ~400 |

## Correlation engine

- **Timeline**: events normalised to the unified envelope, sorted, and time-binned
  (auto bin width ≈ span/30, or caller-specified).
- **Spike detection**: z-score over bin counts (≥3 bins required for a baseline;
  flat series yields no false spikes).
- **Hypothesis ranking**: events clustered by symptom category (keyword match on
  text + entity), scored by summed severity weight, tie-broken by recency.
  Uncategorised events are kept visible, not dropped.
- **Next-check routing**: each category carries a concrete "which skill/tool to run
  next" suggestion — the value when the user doesn't know what to check.

## Symptom categories

`storage`, `network`, `compute`, `ha_drs`, `power_lifecycle`, `auth`, `platform`.
See `references/routing.md` for keyword signatures and the skill each routes to.

## Design properties

- **Zero cross-skill runtime deps** — correlation is pure functions over plain
  dicts; the agent fans out to other skills' read tools (踩坑 #21/#32).
- **JSON-serialisable output** — suitable for direct MCP responses.
- **Immutable** — inputs are never mutated; every function returns new values.
