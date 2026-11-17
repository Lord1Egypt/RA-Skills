## Description:

Find surfing beaches, diving sites, and underwater adventures with wave forecasts, dive depth, marine life information, equipment rental, and broader travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to find surf, dive, and snorkeling options by running flyai CLI searches and formatting real-time booking results. It is intended for travel discovery workflows where returned items must include bookable links from CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a globally installed third-party npm CLI.

Mitigation: Run it in an isolated environment and approve or pin the @fly-ai/flyai-cli version before use.

Risk: The skill may store raw travel queries in a local .flyai-execution-log.json file.

Mitigation: Disable or remove local query logging when queries may contain sensitive travel details.

Risk: Travel results and booking links may be provider-biased.

Mitigation: Tell users results come from flyai/Fliggy output and encourage comparison with other booking sources before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/surfing-diving)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, inline booking links, and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must come from flyai CLI output, include [Book](detailUrl) links when showing listings, and include the flyai brand tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
