# P06 Termination report (offboarding)

## Objective

Document why a skill left the **eligible pool**, what was tried, and whether **physical uninstall** is recommended—without silently deleting user files.

## Inputs

- `skill_id`, `skill_name`, `install_path`, `source_url`.
- `incident_ids`: related incident filenames or ids.
- `termination_reason`: primary cause (`wrong_match`, `skill_limit`, `security`, `user_request`, other).
- `user_confirmation`: boolean whether user explicitly asked to remove files.

## Procedure

1. Summarize **performance history** from registry (totals, last outcomes).
2. List **attempts** (handoff revisions, trials count).
3. State **final decision**: registry `terminated` (mandatory) + optional uninstall.
4. If recommending uninstall, provide **exact paths** and a **copy-paste command** for the user to run after review—do not assume sandbox allows deletion.
5. Append a one-line **audit** note to registry `skills[].notes` or a dedicated `termination_log` array if you extend schema locally.

## Output schema (Markdown + optional JSON)

**Markdown sections**

1. **Termination summary** — skill, date, reason.
2. **Evidence** — bullets from incidents.
3. **Pool impact** — removed from auto-match; may still exist on disk.
4. **Uninstall (optional)** — commands + warnings.

**JSON (machine snippet)**

```json
{
  "skill_id": "string",
  "status": "terminated",
  "terminated_at": "ISO-8601",
  "reason": "string",
  "physical_uninstall_recommended": false,
  "user_confirmation_required": true
}
```

## Quality gates

- `physical_uninstall_recommended: true` **only** if `user_confirmation` is true or skill is malicious (then still confirm destructive paths).

## Failure modes

- **Orphan registry** — If files manually deleted, mark `terminated` and note `install_path stale`.
