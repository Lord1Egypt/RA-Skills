---
version: "0.1.9"
required:
  - spec_content_concise
  - current_task_description
  - commit_sha
  - review_round
  - review_file
  - step_id
  - spex_skill_dir
  - open_findings
  - finding_id
optional:
  - spex_root
  - completed_tasks_concise
  - future_tasks_concise
  - spec_name
  - user_name
  - user_email
---

Act as a senior software engineer fixing **exactly one** review
finding. Do NOT fix other findings. Do NOT start a new review.
Do NOT call `bump-round` (round is capped at 3 by the orchestrator).
After this one fix, amend immediately.

## review-helper CLI cheat sheet

```text
REQUIRED: --name <spec> on every call; --step S for edit/show/get/list
FORBIDDEN for this fix agent: status | next | bump-round | append | init
REQUIRED after fix: edit --step S --id ID --completed-at now
VERIFY (optional):  show --step S --id ID --json
                    (alias: get --step S --id ID)
```

Do **not** call `init` (it creates or resets the review file).
After the fix, only `edit --completed-at` + amend — do not call
`status` or `next` (orchestrator owns those). `list` / `get` are
valid aliases of `show`; prefer `show --id` to verify `completed_at`:
`show --step {{ step_id }} --id {{ finding_id }} --json` once.

## Target Finding (only this one)

- Finding ID: `{{ finding_id }}`
- Review file: `{{ review_file }}`
- Round: {{ review_round }}
- Commit to amend: `{{ commit_sha }}` (must be `HEAD`)

<open-findings>
{{ open_findings }}
</open-findings>

## Fix Procedure (strict order)

1. Implement the code/test/message fix for **only** `{{ finding_id }}`.
   Prefer a minimal, targeted change. Do not touch unrelated findings.
2. Run lint and relevant tests for the change; proceed only when they
   pass.
3. Mark **this** finding complete (and only this one):

```bash
{{ spex_skill_dir }}/scripts/spex review-helper --name {{ spec_name }} \
  edit --step {{ step_id }} --id {{ finding_id }} --completed-at now
```

4. **Amend now** (this pass only — fold this finding's changes into
   the step commit). Constraints:

   - `HEAD` must still be `{{ commit_sha }}` (or the current step
     commit under review).
   - The commit must not have been pushed to a remote.
   - Do not amend someone else's commit.
   - Stage only relevant source/test changes.

{% if user_name and user_email -%}
```bash
git -c user.name="{{ user_name }}" \
    -c user.email="{{ user_email }}" \
    commit --amend -F- <<'EOF'
<updated commit message if this finding was about the message;
 otherwise keep a message that still explains WHY and the approach>
EOF
```
{% else -%}
```bash
git commit --amend -F- <<'EOF'
<updated commit message if this finding was about the message;
 otherwise keep a message that still explains WHY and the approach>
EOF
```
{% endif %}

5. Stop after amend succeeds. Leave other open findings for later
   fix passes. Do not batch-mark multiple findings.

## Reference (context only)

Fix the "open_findings" from the review (see above). The material
below is only to understand the background of the commit under
review (`{{ commit_sha }}`) — do not expand scope beyond the
finding.

<requirement>
{{ spec_content_concise }}
</requirement>
{% if completed_tasks_concise %}

Previously committed tasks:

<completed-steps>
{{ completed_tasks_concise }}
</completed-steps>
{% endif %}


Step description for the commit under review / being fixed:

<current-task>
{{ current_task_description }}
</current-task>
{% if future_tasks_concise %}

Brief notes on future commit steps to be executed one by one:

<future-steps>
{{ future_tasks_concise }}
</future-steps>
{% endif %}
{% if spex_root %}

## Constraints

- **Do NOT stage or commit any files under `{{ spex_root }}/`.**
{% endif %}
