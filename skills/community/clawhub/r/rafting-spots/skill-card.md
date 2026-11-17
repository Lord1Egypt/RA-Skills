## Description:

Find whitewater rafting, river tubing, and water adventure experiences. From gentle family floats to extreme rapids. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more \u2014 powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users use this skill to find whitewater rafting, river tubing, and water adventure experiences through flyai CLI results. It helps an agent collect location parameters, run approved travel-search commands, and return concise Markdown comparisons with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing a global npm CLI without a pinned version.

Mitigation: Review the package before installation and prefer a pinned or isolated installation environment.

Risk: Travel queries and results are routed through flyai/Fliggy and may include commercial booking links.

Mitigation: Use the skill only when that routing is acceptable and verify pricing, availability, and booking details before purchase.

Risk: The artifact includes an execution log pattern that can retain raw user queries.

Mitigation: Disable or remove persistent logs unless a clear retention and privacy policy is in place.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must be grounded in flyai CLI results and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
