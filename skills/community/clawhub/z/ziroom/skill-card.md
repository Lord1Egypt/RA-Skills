## Description:

Ziroom is a long-term rental decision guide that helps agents calculate true monthly rental cost, review common contract pitfalls, and guide deposit or move-out fee disputes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare Ziroom quoted rent against estimated true monthly cost, check rental contract terms, and prepare practical dispute-resolution steps for move-out or deposit deductions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The calculator uses approximate service-fee and electricity assumptions that can differ by city, property, and contract.

Mitigation: Verify rent, service fee, electricity price, and fixed fees against the signing page and contract before relying on the estimate.

Risk: Contract screenshots and rental documents may contain personal information.

Mitigation: Only provide such documents when the agent needs to review them, and redact unrelated personal details where practical.

Risk: Air-quality and health-related rental concerns require evidence beyond agent guidance.

Mitigation: Use qualified CMA testing or authoritative inspection results before treating a unit as safe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/ziroom)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text]

**Output Format:** [Markdown guidance with optional local shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes approximate rent, service-fee, and electricity calculations; actual contract and signing-page values should be verified by the user.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
