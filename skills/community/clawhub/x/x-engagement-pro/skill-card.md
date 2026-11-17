## Description:

Automates X/Twitter engagement for AI image generation brands by monitoring conversations, drafting replies, amplifying posts, and tracking engagement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbuilder](https://clawhub.ai/user/clawbuilder)

### License/Terms of Use:

MIT-0

## Use Case:

Social media and marketing operators use this skill to monitor AI image generation conversations on X/Twitter, engage with creators, and support brand growth through replies, likes, and related engagement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform public X/Twitter account actions automatically when posting authority is granted.

Mitigation: Grant posting credentials only to accounts approved for automation and keep the skill in manual mode until the deployment owner has reviewed the engagement settings.

Risk: The security review reports unsafe command construction around public engagement actions.

Mitigation: Review and fix command construction before enabling scheduled reply, amplify, or all engagement modes.

Risk: The security review calls out rate-limit state handling as an area to review.

Mitigation: Confirm rate-limit state is persisted and enforced before allowing unattended posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawbuilder/skills/x-engagement-pro)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Runtime status objects, generated reply text, and configuration-driven command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform public X/Twitter actions when configured with posting credentials and non-manual engagement modes.]

## Skill Version(s):

1.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
