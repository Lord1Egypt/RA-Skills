## Description:

Winter Snow Travel helps agents plan snow and winter trips, including ski resorts, ice festivals, snow village stays, hot springs, aurora travel, and related booking tasks through FlyAI and Fliggy results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to produce winter destination options, booking-centered comparisons, and concise itineraries from live FlyAI CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires automatic use or installation of an unpinned global third-party CLI.

Mitigation: Pin the FlyAI CLI version, install it locally or in a sandbox, and ask the user before installation.

Risk: Travel queries and booking-centered results are routed through the FlyAI provider.

Mitigation: Tell users when queries will be sent to FlyAI or Fliggy and avoid sending sensitive personal details unless the user explicitly chooses to proceed.

Risk: The activation scope is broad for winter travel terms and may trigger outside explicit booking workflows.

Mitigation: Use the skill only for explicit winter travel planning or booking requests, and fall back to normal assistance for unrelated winter topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/winter-snow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI results and should not return raw JSON.]

## Skill Version(s):

3.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
