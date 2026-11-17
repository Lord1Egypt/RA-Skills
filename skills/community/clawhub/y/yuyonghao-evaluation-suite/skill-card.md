## Description:

Evaluation Suite provides local JavaScript evaluators for RAG quality, reasoning quality, hallucination indicators, and batch evaluation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation engineers can use this skill to score generated answers, retrieved contexts, reasoning steps, and hallucination indicators in local AI evaluation workflows. It is most useful for quick heuristic checks and batch test reporting before deeper model or application review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package metadata appears malformed, which may prevent standard npm tooling from installing or running the package as documented.

Mitigation: Validate package.json and package-lock.json before installation, then run npm test in an isolated workspace.

Risk: README examples and implementation parameter names differ in places, so copied examples may fail or produce misleading evaluation results.

Mitigation: Check the source API signatures and quick test inputs before using results for release or quality decisions.

Risk: The evaluators use local heuristic scoring, so scores can miss semantic errors or overstate quality.

Mitigation: Treat outputs as triage signals and pair them with task-specific test sets, human review, or stronger evaluators for high-impact decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-evaluation-suite)
- [Publisher profile](https://clawhub.ai/user/yuyonghao-123)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with JavaScript and shell snippets; runtime evaluators return JSON-like result objects and summary reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local heuristic checks for RAG, reasoning, and hallucination indicators; batch APIs aggregate pass rates and average scores.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact package.json and SKILL.md cite 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
