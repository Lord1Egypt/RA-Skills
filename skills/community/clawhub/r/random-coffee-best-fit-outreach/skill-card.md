## Description: <br>
Offline random coffee skill for ranking opt-in people and preparing consent-first intro packets; it creates local reports only, and any external communication stays outside the public skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators, community managers, and developers use this skill to normalize opt-in participant data, rank best-fit 1:1 coffee-chat matches, and prepare local double opt-in intro packets for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CSVs, reports, packets, or logs may contain participant data. <br>
Mitigation: Keep generated files local and private, and use only operator-provided or consented participant data. <br>
Risk: Intro packets could expose names, handles, links, or detailed context before both sides agree. <br>
Mitigation: Review drafts before use and confirm both people opt in before sharing identifying details or detailed context. <br>
Risk: The skill may be mistaken for an automated outreach sender. <br>
Mitigation: Treat the skill as a local packet-preparation helper only; any external communication must happen outside the public skill. <br>


## Reference(s): <br>
- [Intake Schema](references/intake-schema.md) <br>
- [Packet Handoff Runbook](references/outreach-surface-runbook.md) <br>
- [Project Homepage](https://github.com/zack-dev-cm/random-coffee-best-fit-outreach) <br>
- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/random-coffee-best-fit-outreach) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown reports and intro packets, CSV normalization guidance, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only outputs; external communication remains outside the skill.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
