## Description:

Finds hotels with hot spring baths, private hot spring rooms, onsen pools, ryokan-style stays, and related travel booking options using flyai real-time booking data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel agents use this skill to search real-time hotel inventory for hot spring, private bath, and ryokan-style stays, compare options, and return booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill mandates installing and running an unpinned global flyai CLI.

Mitigation: Approve the CLI installation explicitly, prefer a pinned and verified version, and run it in a contained environment.

Risk: The skill can persist hidden raw user-query logs, which may include sensitive travel, contact, passport, or payment details.

Mitigation: Remove or redact logging before use and avoid entering sensitive personal details unless logging behavior is controlled.

Risk: The skill may append raw logs through shell commands.

Mitigation: Do not allow raw query logging through shell append commands unless the destination and retention policy are reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/spring-hotel)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a working flyai CLI; user-facing travel results must come from CLI output and include booking detail links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
