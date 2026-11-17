## Description:

Searches and compares round-trip flights with return dates, including bundled versus separate-leg price comparisons and related Fliggy-powered travel booking workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to collect round-trip flight parameters, run real-time flyai CLI searches, compare bundled and separate-leg prices, and format booking options with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt installation and execution of an unpinned global third-party CLI, including a sudo fallback.

Mitigation: Review before installing, prefer a pinned and isolated flyai-cli installation, and avoid elevated global installs.

Risk: Raw user travel queries may be stored in a hidden local execution log.

Mitigation: Avoid entering sensitive personal travel details unless logging is removed, disabled, or clearly controlled.

Risk: Real-time booking data depends on a third-party CLI and may fail, time out, or return unavailable results.

Mitigation: Report retrieval failures honestly, do not substitute unsourced travel data, and ask users to verify itinerary details on the booking page before purchase.

## Reference(s):

- [Return Flights skill page](https://clawhub.ai/xiejinsong/skills/return-flights)
- [Parameter collection and output templates](references/templates.md)
- [Round-trip flight playbooks](references/playbooks.md)
- [Flight search fallback procedures](references/fallbacks.md)
- [Execution log schema](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must be sourced from flyai CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
