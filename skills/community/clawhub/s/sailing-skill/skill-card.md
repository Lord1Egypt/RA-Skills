## Description:

Sailing Sports Skill connects an agent to Sailing Sports MCP data for real-time table tennis, football, and motorsport schedules, scores, rankings, athlete and team information, and related sports Q&A.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyongfen2025](https://clawhub.ai/user/liyongfen2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query current table tennis, football, and motorsport event data, including schedules, results, rankings, player or driver details, and season standings. It is intended for sports information retrieval and excludes unrelated sports, betting, training advice, and other sports data platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may globally install an unpinned mcporter package.

Mitigation: Install mcporter yourself from a verified version, review setup.sh before execution, and avoid running setup as root.

Risk: The Sailing Sports API token is stored in plaintext in the global mcporter configuration.

Mitigation: Use a short-lived or limited token, restrict access to the mcporter config directory, and remove the sailing-sports-mcp config when the skill is no longer needed.

Risk: The skill sends requests to a third-party Sailing Sports endpoint.

Mitigation: Install only after confirming that the publisher and endpoint are trusted and that the endpoint's terms and privacy handling are acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/liyongfen2025/skills/sailing-skill)
- [Sailing Sports MCP endpoint](https://sailing.sports.qq.com/api/tteagent/sport_pub/mcp)
- [Sailing Sports token application](https://sailing.sports.qq.com/open/token-apply)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured tables or lists, JSON-backed MCP results, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The MCP tool returns JSON sports data that agents should present with clear scores, time zone notes when relevant, execution time, and Sailing Sports source attribution.]

## Skill Version(s):

1.0.23 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
