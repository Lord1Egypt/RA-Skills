# vmware-debug Capabilities

Offline incident correlation. No network, no credentials, no writes to any VMware
system. This table covers the two stateless correlation tools; the twelve case
investigation-ledger tools (seven of which write, to the local ledger only) are
listed in `SKILL.md`, and their response sizes are not yet measured here.

| Tool | What it returns | Typical response tokens |
|---|---|---|
| `build_incident_timeline` | `{event_count, window, spikes:[{start,end,count,zscore}], hypotheses:[{category, score, summary, evidence_count, first_seen, last_seen, sample_text, suggested_check}], next_checks:[...]}` | 300–2000 (scales with hypotheses) |
| `list_symptom_categories` | `{items: [{category, example_keywords, suggested_check}], returned, limit, total, truncated, hint}` | ~400 |

`list_symptom_categories` returns the family list envelope — read the rows from
`items`. It has no `limit` parameter, which is exactly why the envelope matters:
`truncated: false` states that this is every category there is, rather than
leaving a model to guess whether it is holding page one. The catalogue is a
fixed in-process constant, so `total` is a real count and `limit` is `null`.

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

`storage`, `network`, `compute`, `ha_drs`, `host_lifecycle`, `power_lifecycle`,
`auth`, `platform`, `hardware`, `licensing`, `data_collection`.
See `references/routing.md` for keyword signatures and the skill each routes to.

`hardware`, `licensing` and `data_collection` were added after real alert titles
("Host TPM attestation alarm", "License will soon expire", "Objects are not
receiving data from adapter instance") matched no category at all. A roll-up
such as "Group population health is degraded" is deliberately left
uncategorized: it names no subsystem, and the cause is in one of its members.

`host_lifecycle` is a host changing its own availability state — maintenance
mode, shutdown, reboot, standby, connection loss, sync failure.
`power_lifecycle` is the VM-level equivalent. They are separate because they are
separate investigations: the second is a task question for vmware-aiops, the
first is a cluster, DPM, vLCM or drift question.

## Design properties

- **Zero cross-skill runtime deps** — correlation is pure functions over plain
  dicts; the agent fans out to other skills' read tools (踩坑 #21/#32).
- **JSON-serialisable output** — suitable for direct MCP responses.
- **Immutable** — inputs are never mutated; every function returns new values.
