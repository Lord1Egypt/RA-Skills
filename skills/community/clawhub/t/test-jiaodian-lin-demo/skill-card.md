## Description:

收费技能示例模板 - 带授权验证，演示如何在 ClawHub 发布付费技能

This skill is ready for commercial/non-commercial use.

## Publisher:

[lintqiu](https://clawhub.ai/user/lintqiu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this ClawHub skill as a paid-skill demo that checks a license key before running the gated example function.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included license check is a demo template and is not production-grade licensing.

Mitigation: Use a stronger licensing design before relying on this pattern for paid production access.

Risk: The skill reads SKILL_LICENSE_KEY from the environment.

Mitigation: Provide the license key only in trusted runtime environments and avoid logging or sharing it.

Risk: Generic trigger phrases may cause the skill to run in unintended conversations.

Mitigation: Narrow the trigger phrases before broad publication.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads SKILL_LICENSE_KEY from the environment before printing demo output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
