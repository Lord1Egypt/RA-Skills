## Description:

Find and compare travel insurance plans, including medical coverage, trip cancellation, luggage protection, and emergency evacuation, using flyai CLI results powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel planners use this skill to search for travel insurance options and compare CLI-sourced results with booking links. It is intended for travel insurance queries covering medical, cancellation, luggage, delay, and evacuation needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and running a third-party CLI.

Mitigation: Review the CLI package source and prefer a pinned local install before using the skill.

Risk: Travel and insurance queries may be routed through a commercial travel service.

Mitigation: Avoid entering sensitive personal details unless the service and its data handling are acceptable for the intended use.

Risk: The skill may keep local logs containing raw user travel or insurance queries.

Mitigation: Disable logging when possible or redact stored queries before retaining or sharing logs.

## Reference(s):

- [Templates](artifact/references/templates.md)
- [Playbooks](artifact/references/playbooks.md)
- [Fallbacks](artifact/references/fallbacks.md)
- [Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown comparison tables with booking links and concise troubleshooting guidance when real-time retrieval fails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be sourced from flyai CLI results, include Book links from detailUrl values, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
