## Description:

Offline random coffee skill for ranking opt-in people and preparing consent-first intro packets. It creates local reports only; any external communication stays outside the public skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and community builders use this skill to rank consented random coffee matches and prepare offline, double opt-in intro packets from local participant data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable wrapper may load unreviewed local Python code from ancestor directories when run from an untrusted repository layout.

Mitigation: Review before installing; run only from a trusted repository layout, prefer a pinned installed package, or use a wrapper that imports from an explicit trusted project root.

Risk: Participant matching can expose personal or private context if unconsented data is included in reports or intro packets.

Mitigation: Use only operator-provided or consented participant data, keep packets local until operator approval, and avoid revealing identities or detailed context until both sides opt in.

## Reference(s):

- [Intake Schema](references/intake-schema.md)
- [Packet Handoff Runbook](references/outreach-surface-runbook.md)
- [Project Homepage](https://github.com/zack-dev-cm/random-coffee-best-fit-outreach)
- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/random-coffee-best-fit-outreach)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown reports and intro packets with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only outputs; external communication remains outside the skill.]

## Skill Version(s):

0.1.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
