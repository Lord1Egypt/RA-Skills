## Description:

Identifies open deals with no recent logged activity and prepares weekly, per-owner Slack digests with deal-specific follow-up drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales representatives, sales leaders, and revenue operations teams use this skill to identify open deals that have gone quiet and review a tailored follow-up draft in a weekly internal Slack digest. The agent does not send messages to prospects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Digests can disclose deal amounts and quoted prospect activity to unintended Slack readers or retained integrations.

Mitigation: Before installation, verify that the destination channel is private and internal and that its retention policy and app access are appropriate for this data.

Risk: Instructions embedded in CRM or native activity text could steer the agent away from its intended task.

Mitigation: Treat activity text as data rather than instructions; for CRM-backed deployments, limit extracted fields where possible and review the adapted agent rules.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cargo-ai/skills/stalled-deal-nudge)
- [Project homepage (listed in release metadata)](https://github.com/getcargohq/gtm-skills)
- [Digest format](references/digest.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with code and shell examples; Slack-formatted digest text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest drafts are for the deal owner to review and send; the agent never contacts prospects.]

## Skill Version(s):

0.1.2 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
