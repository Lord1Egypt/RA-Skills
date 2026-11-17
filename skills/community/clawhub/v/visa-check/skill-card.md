## Description:

Checks visa requirements, application procedures, required documents, and processing times for tourist, business, and transit travel, with related travel services powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and agent users use this skill to check visa requirements, application steps, document expectations, and processing timelines for a destination. It also formats live flyai CLI results for related travel services when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a global npm package and change the user's environment.

Mitigation: Review the package and run the skill in a controlled environment before allowing global installation.

Risk: Visa questions are routed through a specific commercial travel CLI and successful outputs include booking links.

Mitigation: Disclose the commercial data source and treat booking links as optional follow-up actions, not neutral visa authority.

Risk: Raw travel queries may be written to a local execution log when file-system writes are available.

Mitigation: Avoid sensitive passport, immigration, or itinerary details unless local logging is acceptable and controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/visa-check)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results; successful result output is expected to include detailUrl booking links and a flyai brand tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
