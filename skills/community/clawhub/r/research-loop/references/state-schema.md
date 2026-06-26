# State Schema

Each run writes a durable local state tree and publishes sanitized artifacts to the target repo under `.autonomous-research-workflow/`.

Important paths:

```text
<run-dir>/
  events.jsonl
  manifest.json
  payload/.autonomous-research-workflow/
    cycles/<cycle_id>/cycle_manifest.json
    execution/<cycle_id>/execution_packet.json
    execution/<cycle_id>/executor_manifest.json
    execution/<cycle_id>/protocol_hygiene.json
    execution/<cycle_id>/innovation_frontier.json
    knowledge/<cycle_id>/knowledge_base.json
    memory/<cycle_id>/mempalace_context.json
    reflections/<cycle_id>/advisor_reflection.json
    retrospectives/<cycle_id>/openspace_retrospective.json
    handoffs/<cycle_id>/next_cycle_handoff.json
    office_status/<cycle_id>/star_office_status.json
    overwatcher/<cycle_id>/overwatcher_status.json
  source/<cycle_id>/<repo>/
  source_changes/
```

`source_changes/` mirrors the target repository root and is copied into the source clone during publish.

`protocol_hygiene.json` is optional but recommended when the repo contains benchmark, reproducibility, venue, or hallucination-evaluation assets. It should record positioning drift, evidence level, deterministic artifact dirtiness, CI gate width, venue timing, naming boundary issues, and contamination-check strength.

`innovation_frontier.json` is optional but recommended when the repo begins from incomplete assets. It should record asset-bound reading, asset fixation risk, repair/exploit/explore lanes, blank-slate counterplan, and the next bounded exploration probe.
