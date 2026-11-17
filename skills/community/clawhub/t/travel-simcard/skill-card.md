## Description:

Find international SIM card and eSIM options for overseas travel using flyai CLI results, including data packages, local numbers, coverage, prices, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to compare SIM card and eSIM options for a destination from live flyai CLI output. It formats results as concise booking-oriented Markdown with prices, coverage context, and bookable links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a global flyai CLI before answering travel queries.

Mitigation: Use a reviewed, pinned, isolated CLI installation and avoid unattended global npm installs.

Risk: Raw travel queries may be persisted in an execution log.

Mitigation: Disable or remove query logging before handling sensitive travel or personal details.

Risk: Booking links and real-time prices come from flyai output and may lead to third-party booking flows.

Mitigation: Review booking links and CLI results before purchase or sharing with users.

## Reference(s):

- [Skill Definition](artifact/SKILL.md)
- [Output Templates](artifact/references/templates.md)
- [Scenario Playbooks](artifact/references/playbooks.md)
- [Failure Recovery](artifact/references/fallbacks.md)
- [Execution Log Schema](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown comparison tables with inline booking links and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must be derived from flyai CLI output, include booking links from detailUrl values, and follow the user's input language.]

## Skill Version(s):

3.2.0 (source: evidence release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
