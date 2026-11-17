## Description:

Mandatory risk-driven verification workflow for maintained-code changes. Use when implementing, fixing, refactoring, deleting, migrating, or reviewing code to identify all materially affected behavior, map failure risks to sufficient tests, execute required evidence, and report unresolved test gaps and residual risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when implementing or reviewing maintained-code changes to map changed behavior to material risks, select proportionate evidence, execute verification, and report residual test gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can slow normal code changes because it requires explicit impact mapping, evidence execution, and unresolved-risk reporting.

Mitigation: Apply the risk-proportionate portfolio described by the skill: keep small changes compact, select the cheapest stable boundary that exposes each material failure mode, and mark blocked evidence explicitly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wujiaming88/skills/test-code-change)
- [Evidence report template](references/evidence-report-template.md)
- [Frontend change verification](references/frontend-change-verification.md)
- [Change impact and risk analysis](references/impact-analysis.md)
- [Scientific test method selection](references/test-method-selection.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with traceability tables, status summaries, and command evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit status for each material risk: VERIFIED, NO-TEST-RATIONALE, or BLOCKED.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
