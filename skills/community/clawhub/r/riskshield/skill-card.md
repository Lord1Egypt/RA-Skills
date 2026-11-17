## Description:

RiskShield 案件审批自动化。使用 Playwright 浏览器自动化完成审批，支持 Pass/Refuse 两种操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoleizhang](https://clawhub.ai/user/haoleizhang)

### License/Terms of Use:

MIT-0

## Use Case:

Operations or risk-review users run this skill to automate RiskShield case approval workflows for pending cases, choosing Pass with a credit amount or Refuse with a refusal code. The skill uses Playwright automation to submit the decision and verify that the case closes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes reusable credentials and token material for RiskShield access.

Mitigation: Revoke exposed credentials and tokens, supply secrets through a managed secret channel, and exclude credential, token, and cookie files from any published package.

Risk: The skill can submit consequential approval or refusal decisions with unsafe defaults.

Mitigation: Remove fixed-case and default-decision behavior, require explicit user-directed case and action input, and run only under an isolated least-privilege account with human review before execution.

Risk: The artifact contains many debug and legacy automation scripts that increase operational ambiguity.

Mitigation: Publish only the vetted entrypoint and required support files, and exclude debug, test, and exploratory scripts from deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/haoleizhang/skills/riskshield)
- [Publisher Profile](https://clawhub.ai/user/haoleizhang)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command-line arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a case number, operation, optional refusal code, and optional approval amount as command inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
