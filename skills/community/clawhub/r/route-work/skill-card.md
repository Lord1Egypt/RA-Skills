## Description:

Invisibly classify work and choose Codex or Claude, reasoning effort, context shape, execution style, and verification profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adwilkinson](https://clawhub.ai/user/adwilkinson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route agent work between Codex and Claude while selecting reasoning effort, context shape, execution style, and verification profile. It is intended for normal ClawHub release use, with platform-level approvals still applied around high-impact actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hidden routing can make it harder for users to see which provider or reasoning profile is being selected.

Mitigation: Keep platform logs or route inspection available for audit and debugging, especially when routing affects important work.

Risk: The skill advises against adding approval or risk gates, which can be unsuitable for deployments, release promotion, admin workflows, or external communications.

Mitigation: Rely on platform-level approvals and add explicit confirmation rules outside the skill for high-impact or externally visible actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adwilkinson/skills/route-work)
- [Source Repository](https://github.com/ADWilkinson/oneshot-cli)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is designed to operate silently during task routing; optional helper output may be JSON when inspecting a route.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
