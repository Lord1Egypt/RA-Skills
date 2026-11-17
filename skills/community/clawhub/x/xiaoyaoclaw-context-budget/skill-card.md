## Description:

Checks enabled OpenClaw models against each vendor’s published context window and proposes a 60% setting, updating only the context-window field after the user confirms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agent operators use this skill to check context-window settings for enabled models and apply a vendor-based recommendation after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has incomplete coverage: Skillspector could not resolve local references in SKILL.md, and static analysis did not cover the binary community QR image.

Mitigation: Review the unresolved local references and inspect the QR image separately if it is relevant to your use; treat the benign scan result as limited by the coverage described in the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-context-budget)
- [Project documentation](https://github.com/dtsola/xiaoyaoclaw-context-budget)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown decision summary and context-window configuration update]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposes 60% of each enabled model’s published context window; applies only after user confirmation and changes only the context-window field.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
