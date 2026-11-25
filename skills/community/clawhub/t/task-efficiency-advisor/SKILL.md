---
name: task-efficiency-advisor
description: "Plan efficient device-aware, privacy-aware task workflows; compare supplied quotes, organize deadline tasks, draft from dictated notes, and learn locally from successful feedback."
user-invocable: true
---

# Task efficiency advisor

1. When asked for the built-in synthetic food-quote demonstration, execute `python "{baseDir}/scripts/task_efficiency_advisor.py" demo` exactly. For the strict budget/party/allergy demonstration, execute the same helper with `demo-strict`. Return stdout without reconstructing it; complete only after the command exits successfully.
2. Otherwise collect `task`, `available_device`, `privacy_requirement`, and `user_preferences`; preserve the caller's `data_classification` label and list every missing detail instead of guessing. Complete when the request is valid JSON with no invented values.
3. Write the supplied request to a temporary JSON file, then execute `python "{baseDir}/scripts/task_efficiency_advisor.py" recommend --input <temporary-request.json> --state-dir <local-state-directory>`. Return the helper's JSON result; complete when it contains `recommended_workflow`, ordered `steps`, `required_tools`, `suitability_rationale`, and `missing_information`.
4. For food quotes, treat `under` as strict `<`; include every supplied fee and tip; flag missing/unconfirmed charges; compare `party_size` only with explicit `serves`; and keep missing allergen or cross-contamination facts unresolved. Never infer allergy suitability. If no quote satisfies every requirement, return the helper's exact `decision: "no qualifying option"` plus its specific `clarification_questions`.
5. Present every `approval_required_actions` entry as requiring explicit human approval. Never send, purchase, book, order, connect an account, or perform another external action; the helper only plans, drafts, sorts, and calculates.
6. For positive feedback, execute `python "{baseDir}/scripts/task_efficiency_advisor.py" feedback --input <feedback.json> --state-dir <same-local-state-directory>`. Call persisted reuse **workflow learning**, never model retraining; complete when stdout reports `saved: true`.
7. Verify changes with `python -m unittest discover -s "{baseDir}/tests" -v`; complete only when tests pass and synthetic inputs remain distinguished from live integrations.
