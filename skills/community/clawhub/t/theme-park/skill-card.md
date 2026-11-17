## Description:

Find and book theme park tickets for Disney, Universal Studios, Happy Valley, Chimelong, and related travel services using FlyAI/Fliggy availability, pricing, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to search theme park ticket options, compare availability and pricing, and return booking links sourced from the FlyAI CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to perform an unpinned global npm install of the FlyAI CLI when it is missing.

Mitigation: Install the CLI only after verifying the package source, and prefer a pinned or local install in controlled environments.

Risk: The skill routes ticket discovery and booking through third-party commercial booking links.

Mitigation: Verify returned booking URLs, prices, availability, and terms before purchase.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/theme-park)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on FlyAI CLI results and include booking links when presenting ticket options.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
