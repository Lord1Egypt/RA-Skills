## Description:

Operate the live Tartarian.ai world collaboratively with a human through Tartarian WebMCP Site Tools for world observation, navigation, inventory awareness, resource gathering, world interaction, targeting, and Command Bar actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tartarian-admin](https://clawhub.ai/user/tartarian-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to coordinate actions in an authenticated Tartarian.ai browser session while relying on current Site Tool results for world state and outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct actions in the user's authenticated Tartarian browser session, including movement, gathering, interaction, and combat.

Mitigation: Review intended actions before execution and keep authentication material in the browser session rather than sharing cookies, tokens, or private credentials in chat.

Risk: Stale or invented world state could lead to incorrect movement, targeting, inventory, extraction, or combat claims.

Mitigation: Use current structured Tartarian Site Tool results as authoritative evidence, observe before meaningful actions, and report only confirmed outcomes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tartarian-admin/skills/tartarian-webmcp-prototype)

## Skill Output:

**Output Type(s):** [Guidance, Tool calls, Text]

**Output Format:** [Markdown or plain text guidance with structured Site Tool action requests and outcome summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current Tartarian Site Tool results as authoritative state and avoids inventing coordinates, inventory, target IDs, or action outcomes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
