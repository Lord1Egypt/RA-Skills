# Feedback and scoped request learning

Always tie feedback to an existing decision. The host interprets natural language and constructs JSON; the runtime validates structure/state, not whether a paraphrase really expresses the user’s intent. Exact user quotes and scope remain essential.

## Fix the current decision

Feedback JSON is `{"kind":"preference","text":"以后个人工具都优先少维护"}`. Kinds:

- `fact`, `preference`, `rubric`, `missing_option`, `exception`, `reject`: invalidate the old recommendation/selection; prepare corrected full input and run `decide --parent`.
- `select`: also requires `selected_option_id`. Only a current decision and an eligible candidate may be selected. A choice alone creates no policy.
- `defer`: records explicit deferral, no policy.
- `outcome`: records real observed outcome separately; it is not automatically a preference or ground truth about all related decisions.

To correct a mistaken pending selection, record the correction before recomputing. If new computation fails, the old result remains stale. Do not continue to use it as current.

## Explicit future preference

After feedback is recorded, create:

```json
{
  "scope": "personal-tools",
  "feedback_id": "fb_FROM_FEEDBACK_COMMAND",
  "explicit_future": true,
  "source_quote": "以后个人工具都优先少维护",
  "semantic_key": "maintenance-priority",
  "patch": {
    "preference": "个人工具优先减少持续维护，即使首次开发略多",
    "priority": ["maintenance", "first_effort"]
  }
}
```

Substitute actual returned IDs; never fabricate feedback. Quote must be an exact substring of the stored feedback. Set `explicit_future=true` only when the user actually specified future use, not because they selected/rejected an option. Meaning and scope are checked by the host; substring validation alone is not proof of future intent.

New explicit defaults supersede only an active explicit preference with the same scope and semantic key. Unrelated preferences remain active. For a revision, supply the full intended patch for that semantic key. A preference may have only text if priority is not settled. The runtime uses exact scope matching; new tasks in other scopes do not inherit it. Current explicit priority overrides learned priority. Exclude a conflicting policy for a one-off exception so its preference text is not sent either.

After `policy-new`, rerun the corrected decision; the new policy invalidates older decisions in that scope. Explain future scope in one sentence. Runtime state is local and shared across sessions on this device.

## Template improvement

Use `policy-new` with `explicit_future=false` and a patch containing a full `dimension` object to fix its instructions/criteria, or a proposed preference/priority if not yet explicit. It stays `candidate` and does not affect normal decisions.

Before trial, have real labels with sources and independent, distinct cases. The trials JSON is an array of 3–8 entries:

```json
{
  "role": "holdout",
  "input": {"scope": "same-as-policy", "goal": "...", "options": [], "dimensions": []},
  "expected_option": "A",
  "expected_next_step": "continue",
  "label_source": "Verified user tradeoff or objective evidence reference"
}
```

This is the entry shape, not a runnable empty case: fill complete valid inputs from independently labeled examples. Include `correction`, `holdout` and `counterexample`; expected option may be null for gather/ask/defer. Freeze expected answers before model calls. Do not use “new model agrees with itself” as a label, or copy the same case with cosmetic edits and call it a holdout.

`policy-trial` runs baseline and candidate, stores real responses, and requires at least one improvement plus all candidate cases correct. It can use up to 16 model calls (each with bounded transient retries); stay within task budget. Failure or inadequate data leaves the candidate inactive. `policy-adopt` requires a passing current trial and unchanged baseline. All real Jev calls are auditable; this small suite is not statistical calibration or proof of general improvement.

An adopted method patch overlays existing defaults; revoking it exposes the prior applicable policy set. On a verified regression, revoke the offending policy, record the new failure, and rerun the affected decision. Stop rather than repeatedly mutating templates until examples happen to pass. Do not change credentials, permissions, hard-constraint labels, model/action thresholds or executable code as learning.

`policy-revoke` stops future use and invalidates decisions derived from that policy. It does not delete historical data, revive superseded explicit preferences, or undo external actions. Reconcile derived policies when shared memory/user instructions supersede their source; the runtime does not automatically watch external memory systems.
