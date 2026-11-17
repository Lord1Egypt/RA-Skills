## Description:

Searches seasonal flights, including summer routes, winter schedules, holiday charters, and related travel options, using live flyai results powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search seasonal, summer, winter, holiday, and off-season flights with live CLI-backed results. It helps an agent collect route and date parameters, run the documented flight-search commands, and format bookable options in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a global npm CLI and includes a sudo fallback.

Mitigation: Use it only in environments where global npm installs are approved, and do not run the sudo fallback without explicit administrative review.

Risk: User travel details can be interpolated into shell commands.

Mitigation: Validate route, date, price, and journey parameters before execution and avoid unsafe shell interpolation.

Risk: The runbook describes persistent logs that may include raw user queries.

Mitigation: Disable or control local logging before users provide sensitive personal, passport, booking, or account details.

Risk: Flight results depend on a third-party CLI and travel service.

Mitigation: Disclose third-party routing to users and require live CLI output with booking links before presenting results.

## Reference(s):

- [Templates](artifact/references/templates.md)
- [Playbooks](artifact/references/playbooks.md)
- [Fallbacks](artifact/references/fallbacks.md)
- [Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output for flight results; raw JSON should not be shown to the user.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
