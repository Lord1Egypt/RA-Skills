## Description:

Plan self-driving road trips - optimal routes, car rental, scenic stops along the way, fuel stations, and recommended rest areas; it also supports related travel booking and planning tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to plan self-driving road trips and related travel logistics from FlyAI/Fliggy CLI results, including routes, car rental, scenic stops, fuel stations, rest areas, and booking-linked options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a global third-party npm CLI before answering travel requests.

Mitigation: Require explicit approval before installation, prefer a sandboxed or project-local install, and pin the FlyAI CLI version when possible.

Risk: The skill depends on FlyAI/Fliggy CLI output and booking links as the required data source.

Mitigation: Review CLI output before presenting recommendations and make clear when real-time data cannot be retrieved.

Risk: The runbook allows local execution logs that may persist raw travel queries.

Mitigation: Disable, redact, or scope local logs so user travel queries and booking details are not retained unnecessarily.

## Reference(s):

- [Road Trip Skill Definition](artifact/SKILL.md)
- [Templates - Road Trip](artifact/references/templates.md)
- [Playbooks - Road Trip](artifact/references/playbooks.md)
- [Fallbacks - Trip Planning Category](artifact/references/fallbacks.md)
- [Runbook - Execution Log Schema](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, brand tag, and inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Travel results must come from flyai CLI output, include Book links from detailUrl, and avoid raw JSON in the user-facing response.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
