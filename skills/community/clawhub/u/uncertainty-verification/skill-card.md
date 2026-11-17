## Description:

Fact-checking and hallucination-detection guidance that prompts an agent to verify generated technical content, statistics, named references, code examples, and completed external actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack123255829](https://clawhub.ai/user/jack123255829)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agent operators use this skill to make an assistant more deliberate about checking facts, numbers, references, code runnability, and external-operation results before presenting work as complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add extra verification steps or confidence labels during routine technical work.

Mitigation: Use it where deliberate fact-checking is desired and allow the agent time to validate important claims, code, and completed actions.

Risk: The source instructions are written primarily in Chinese, which may be harder for users who do not read Chinese to review.

Mitigation: Have a qualified reviewer translate or review the instructions before deployment in teams that do not read Chinese.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jack123255829/skills/uncertainty-verification)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, code, shell commands]

**Output Format:** [Markdown guidance and confidence labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add verification labels such as VERIFIED, LIKELY, or UNCERTAIN to generated responses.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
