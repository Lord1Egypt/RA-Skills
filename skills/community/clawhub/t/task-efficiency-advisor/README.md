# Task Efficiency Advisor

`task-efficiency-advisor` is an OpenClaw skill backed by a deterministic Python standard-library CLI. It recommends a device-aware, privacy-aware workflow without carrying out external actions.

## Usage

Create a request JSON file, then run:

```powershell
python .\scripts\task_efficiency_advisor.py recommend --input request.json --state-dir .local-state
```

Run the deterministic built-in synthetic demonstration without state or live integrations:

```powershell
python .\scripts\task_efficiency_advisor.py demo
```

Run the new strict synthetic qualification demonstration:

```powershell
python .\scripts\task_efficiency_advisor.py demo-strict
```

In OpenClaw, explicitly reference the model-visible skill while keeping the request in the same normal prompt:

```text
$task-efficiency-advisor Run the built-in synthetic food-quote demonstration and return the helper output.
```

`$task-efficiency-advisor` is the documented composable reference form. `/skill task-efficiency-advisor ...` is the generic standalone command form; a bare `/task-efficiency-advisor` is not the correct hyphenated direct-command spelling because generated slash names are sanitized.

Record explicitly successful feedback for later reuse:

```powershell
python .\scripts\task_efficiency_advisor.py feedback --input feedback.json --state-dir .local-state
```

The feedback object contains `request`, `successful: true`, `recommended_workflow`, and an optional `feedback_note`. Unsuccessful or ambiguous feedback is not stored.

## Input schema

Required fields:

- `task`: string or object. Structured task types are `dictated_notes_to_email_draft`, `organize_tasks_by_deadline`, and `compare_food_quotes`.
- `available_device`: the device actually available.
- `privacy_requirement`: the caller's privacy constraint.
- `user_preferences`: object, list, or string of supplied preferences.

Optional `data_classification` should be `synthetic` or `live`; when omitted, output says `unspecified` rather than guessing. Scenario-specific omissions are returned in `missing_information`.

### Food-quote fields

For `task.type: "compare_food_quotes"`:

- `task.budget` accepts a string such as `"under 25"` or `{ "operator": "under", "amount": "25.00" }`. `under` is strict: a total of exactly `25.00` fails `< 25.00`; use `at_most` for `<=`.
- `task.party_size` is checked only against each quote's explicit positive-integer `serves` value. Missing portions remain unresolved.
- `task.allergies` is a list such as `["peanut"]`. Each quote must explicitly provide both `allergen_information` and `cross_contamination_information` for every requested allergy. Missing or unclear facts never qualify and are never inferred safe.
- Each quote supplies `subtotal`, an itemized `fees` object, optional numeric `tip`, `charges_confirmed`, and optional `unknown_charges`. Every supplied fee and tip is included with decimal arithmetic. Missing fees, `charges_confirmed` other than `true`, or any unknown charge remains unresolved.
- When no quote satisfies all requested constraints, output contains the exact `decision` value `no qualifying option` and specific `clarification_questions`.

## Output schema

Every recommendation contains:

- `recommended_workflow`
- ordered `steps`, each with `approval_required`
- `required_tools`
- `suitability_rationale`
- `missing_information`
- `approval_required_actions`
- `workflow_learning`

Scenario outputs can also contain `draft`, `organized_tasks`, or `quote_comparison`. Qualified food comparisons add `decision`, optional `recommended_option`, and `clarification_questions`; every quote reports `qualifies`, `disqualifying_reasons`, and `unresolved_requirements`.

## Workflow learning

Workflow learning is compact local reuse of workflows that the user explicitly marked successful; it is **not model retraining**. The state file stores a task category, normalized device and privacy labels, a preference hash, the successful workflow text, and a short feedback note. It does not store raw notes, task titles, quote details, recipients, or credentials. Pass a separate temporary `--state-dir` in tests or sensitive one-off runs.

## Privacy and approvals

The helper performs local planning, text preparation, sorting, and decimal arithmetic only. Sending messages, purchasing, ordering, booking, posting, submitting, connecting accounts, and other external execution are never performed. They are returned as `approval_required_actions` with `status: not_executed`.

## Synthetic data versus live integrations

`resources/synthetic_scenarios.json` and all tests use clearly fictional synthetic data. The helper has no network integration and does not fetch live prices, deadlines, recipients, messages, accounts, or fees. For live inputs, the caller must supply the data, label it `live`, review privacy requirements, and separately approve any external action; even then this helper does not execute it.

## Tests

```powershell
python -m unittest discover -s tests -v
python -m py_compile scripts\task_efficiency_advisor.py tests\test_task_efficiency_advisor.py
python C:\Users\Yashk\AppData\Roaming\npm\node_modules\openclaw\skills\skill-creator\scripts\quick_validate.py .
```
