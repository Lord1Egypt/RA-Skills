## Description:

Manage communities, schedule posts, automate workflows, and run DM sequences across Skool, Circle, Mighty Networks, Discord, and Slack via the stickyhive CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexblr](https://clawhub.ai/user/alexblr)

### License/Terms of Use:

MIT-0

## Use Case:

External community operators, developers, and agent users use this skill to manage StickyHive communities, schedule and publish posts, configure automations, run DM sequences, and manage webhooks through CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, delete, reschedule, run, toggle, enroll, and create webhook actions that affect live community operations.

Mitigation: Use a least-privilege or sandbox API key and require explicit operator confirmation before executing state-changing commands.

Risk: A custom STICKYHIVE_API_URL can route authenticated requests, including the API key, to an untrusted destination.

Mitigation: Leave STICKYHIVE_API_URL unset unless the destination is controlled and trusted.

## Reference(s):

- [StickyHive ClawHub Skill Page](https://clawhub.ai/alexblr/skills/stickyhive)
- [StickyHive README](README.md)
- [StickyHive Skill Instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown command guidance; executed CLI commands return structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STICKYHIVE_API_KEY; STICKYHIVE_API_URL can override the API destination.]

## Skill Version(s):

0.1.1 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
