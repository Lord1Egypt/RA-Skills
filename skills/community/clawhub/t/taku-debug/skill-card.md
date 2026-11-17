## Description:

Taku Debug guides agents through a four-phase, evidence-first root-cause investigation workflow before implementing fixes for broken behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkenny0](https://clawhub.ai/user/kkenny0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when debugging failed checks, crashes, regressions, intermittent failures, and other broken behavior. It structures investigation, hypothesis testing, implementation, and verification so fixes address root cause rather than symptoms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can slow down simple fixes because it requires evidence gathering, reproduction, and hypothesis testing before code changes.

Mitigation: Use it for broken behavior, failed checks, regressions, crashes, and intermittent issues where disciplined root-cause analysis is valuable.

Risk: Debugging may involve inspecting code history, logs, and test output that could contain sensitive project data.

Mitigation: Review gathered evidence before sharing it externally and sanitize hostnames, IPs, file paths, customer data, secrets, and other sensitive details.

Risk: Incorrect root-cause hypotheses can lead to misleading fixes if the agent skips verification.

Mitigation: Require a failing reproduction or test before the fix and a passing verification run after the fix.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with diagnostic reports and inline shell commands or code references when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise debug reports with symptom, root cause, hypotheses, fix, evidence, regression test, and status.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
