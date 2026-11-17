## Description:

Find hotels with free cancellation policy, using the flyai CLI to return real-time booking results with links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search for refundable hotel options and compare real-time booking results from the flyai CLI. It is intended for uncertain travel dates where free cancellation policy and booking links are important.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global flyai CLI.

Mitigation: Review the CLI publisher and package before installation, prefer manual reviewed installation, and run it in an isolated environment.

Risk: The skill can persist raw travel queries in an execution log.

Mitigation: Disable or avoid the execution log unless query retention is disclosed, controlled, and acceptable for the deployment.

Risk: Hotel availability, prices, and cancellation policies depend on real-time third-party booking data.

Mitigation: Require results to come from flyai CLI output and have users verify booking terms on the linked booking page before purchase.

## Reference(s):

- [Refundable Hotel skill page](https://clawhub.ai/xiejinsong/skills/refundable-hotel)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking-link tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hotel results must come from flyai CLI output and include Book links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
