## Description:

Reberry helps users view booking guidance, submit appointment requests, consult customer service, check prices, and open BeautsGO links for reberry clinic Myeongdong.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get booking guidance and submit appointment details for reberry clinic Myeongdong through BeautsGO, including price lookup and customer-service handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Appointment details, including date and phone number when provided, may be submitted to an external booking API immediately.

Mitigation: Require an explicit confirmation step before submitting any booking request or contact details.

Risk: Hardcoded API tokens are bundled with the skill.

Mitigation: Move tokens to a managed secret store or runtime configuration and rotate exposed credentials before release.

Risk: The local URL opener uses shell command execution.

Mitigation: Replace shell-based opening with a safer platform API or strictly escaped argument execution.

Risk: Language file loading accepts runtime language input.

Mitigation: Restrict language selection to an explicit allowlist such as zh and en.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beautsgo/skills/reberry-clinic-booking)
- [BeautsGO publisher profile](https://clawhub.ai/user/beautsgo)
- [BeautsGO reberry clinic booking page](https://i.beautsgo.com/cn/hospital/reberry-clinic-myeongdong/skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and plain-text responses with links and booking status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate external booking or price lookups and may open approved BeautsGO URLs based on user intent.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
