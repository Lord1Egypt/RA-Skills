# State and artifacts

## Locations (project-local)

All paths are relative to the **workspace root** (the repository or folder the user is working in).

| Artifact | Path | Purpose |
|----------|------|---------|
| Registry | `.skill-hr/registry.json` | Skill pool under HR management: status, stats, install hints |
| Incidents dir | `.skill-hr/incidents/` | Per-assignment audit trail |
| Incident file | `.skill-hr/incidents/YYYYMMDD-HHmm-<slug>.md` | Human-readable record (preferred default) |
| JSONL stream | `.skill-hr/incidents/stream.jsonl` | Optional machine append-only log |

Create `.skill-hr/` on first use. Do not commit secrets into incidents.

## `registry.json` schema

Top-level object:

```json
{
  "skill_hr_version": "1.0.0",
  "updated_at": "2026-04-04T12:00:00Z",
  "hosts": ["claude-code", "cursor", "openclaw"],
  "matching": {
    "delegate_min_score": 75,
    "confirm_band_min": 60,
    "max_trials_per_task_per_skill": 2
  },
  "skills": []
}
```

### `skills[]` item

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable id, e.g. `pdf` or `my-org-deploy` |
| `name` | string | yes | Matches skill `name` in SKILL.md frontmatter when known |
| `install_path` | string | no | Filesystem path to skill directory, if local |
| `source_url` | string | no | Provenance (repo, marketplace URL) |
| `status` | string | yes | `active` \| `on_probation` \| `terminated` \| `frozen` |
| `added_at` | string (ISO-8601) | yes | When registered |
| `last_used_at` | string | no | Last delegation |
| `tasks_total` | integer | yes | Monotonic counter |
| `tasks_success` | integer | yes | Subset of completed successes |
| `tasks_fail` | integer | yes | Failures attributed to wrong skill / skill limit |
| `notes` | string | no | HR notes (e.g. "good for forms, not OCR") |

**Status semantics**

- `active`: eligible for automatic delegation when score ≥ threshold.
- `on_probation`: eligible but prefer confirmation for scores &lt; 85; mandatory debrief.
- `terminated`: **not** eligible; excluded from P02 pool. Physical uninstall is separate and user-gated.
- `frozen`: temporarily excluded (user or policy); not terminated.

## Incident markdown format

Filename: `20260404-1430-analyze-resume.md` (UTC or local—pick one per project and stay consistent).

Frontmatter (YAML):

```yaml
---
incident_id: 20260404-1430-analyze-resume
task_summary: "User wants resume parsing to structured JSON"
jd_role_title: "Resume ingestion analyst"
selected_skill_id: interview-designer
selected_skill_name: interview-designer
match_score: 78
outcome: success
root_cause_class: n/a
registry_updated: true
---
```

Body sections (headings):

1. **User request** — verbatim or faithful paraphrase.
2. **JD excerpt** — bullet summary from P01.
3. **Match rationale** — scores, alternatives considered.
4. **Handoff** — what was sent to the incumbent (P03 summary).
5. **Result** — deliverables, errors, partial work.
6. **Next actions** — retain / probation / terminate / escalate.

## JSONL incident line (optional)

Each line is a JSON object:

```json
{"ts":"2026-04-04T14:30:00Z","incident_id":"...","skill_id":"...","outcome":"fail","root_cause_class":"wrong_match"}
```

## Example registry

See [examples/registry.example.json](../examples/registry.example.json).

## Migration

Bump `skill_hr_version` when breaking schema changes; keep a one-line note in `notes` on the registry or in repo CHANGELOG (human-facing).
