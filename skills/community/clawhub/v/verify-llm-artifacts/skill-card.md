## Description:

Confirms or rejects findings from review-llm-artifacts before deletes or risky refactors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after review-llm-artifacts to verify each reported LLM artifact finding against local source evidence before risky refactors, deletions, or fix-llm-artifacts runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local project files and review findings as part of verification.

Mitigation: Run it only in projects where the agent is allowed to inspect source files and local .beagle review artifacts.

Risk: A stale or incomplete review report can lead to inconclusive or misleading verification results.

Mitigation: Use the required echo, id-lock, per-finding checklist, and output validation steps before acting on any result.

Risk: Cleanup based on unreviewed verification output could remove code that is still required.

Mitigation: Run automated fixes only for findings marked confirmed_issue and treat inconclusive findings as requiring human or product context.

## Reference(s):

- [Verification checklist](references/verification-checklist.md)
- [ClawHub skill page](https://clawhub.ai/anderskev/skills/verify-llm-artifacts)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and a JSON verification report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .beagle/llm-artifacts-verification.json and summarizes verification results for the agent user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
