## Description:

Finds zoos, aquariums, safari parks, wildlife sanctuaries, and related travel options using flyai CLI results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travel-focused agents use this skill to search for zoo, aquarium, safari, wildlife, and related booking options for a requested city, then present real-time results as user-facing Markdown with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a globally installed, unpinned external travel CLI.

Mitigation: Install a pinned and reviewed flyai CLI version in an isolated environment, and avoid automatic global installation during agent execution.

Risk: The skill can persist raw user queries in a local execution log when filesystem writes are available.

Mitigation: Disable or remove persistent raw-query logging, and avoid submitting sensitive personal or travel information unless logging controls are understood.

Risk: Travel results, prices, availability, and booking links come from an external CLI data source.

Mitigation: Treat returned booking details as third-party data and verify price, availability, and destination details before purchase.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/zoo-aquarium)
- [Skill Instructions](artifact/SKILL.md)
- [Output and Parameter Templates](artifact/references/templates.md)
- [Scenario Playbooks](artifact/references/playbooks.md)
- [Fallback Procedures](artifact/references/fallbacks.md)
- [Execution Log Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to include detailUrl-based Book links, avoid raw JSON, and follow the user's language.]

## Skill Version(s):

3.2.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
