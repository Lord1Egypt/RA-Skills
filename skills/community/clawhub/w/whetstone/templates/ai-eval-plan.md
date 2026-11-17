# AI evaluation plan: feature name

Optional. Write it before tuning prompts. Keep the evaluation set and results with the project, without unmasked personal data.

| Field | Value |
|---|---|
| Feature and users | What the model does, and for whom |
| Agent, model and configuration | Agent version, provider, model identifier and version, settings |
| Prompt and retrieval version | Commit or tag, index and chunking settings |
| Dataset, grader and rubric versions | Commit or tag of each |

## Metrics and thresholds

| Metric | Threshold | Current baseline |
|---|---|---|
| Recall at k | | |
| Groundedness | | |
| Correct refusal rate | | |
| Restricted-content leaks | 0 | |
| p95 latency and cost per request | | |

## Evaluation set

| Category | Count | Source |
|---|---|---|
| Typical tasks | | |
| No answer in the sources | | |
| Caller without access | | |
| Injected instructions in input or documents | | |
| Failed or interrupted tool call, judged by resulting state | | |
| Permission or index transition | | |
| Held out from tuning | | |

## When it runs

Every change to the prompt, model, retrieval settings, chunking or tools runs the fast suite, and a drop below a threshold fails the check. Before release, run the full suite from the same starting state and compare it case by case with the current version. Report results by scenario or user group beside the aggregate, and repeat trials when variability could change the decision.

## Results

| Date | Change and versions tested | Key metrics by scenario | Decision |
|---|---|---|---|
| | | | |
