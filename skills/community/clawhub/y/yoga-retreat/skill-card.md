## Description:

Book flights for yoga retreats and wellness travel destinations. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to search flight options for yoga retreats and wellness travel, then review real-time booking links returned by the flyai CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may globally install an unpinned third-party npm CLI.

Mitigation: Review the package and installation environment before use; run it only where global npm installation is acceptable.

Risk: Travel searches and booking links are routed through a specific provider.

Mitigation: Verify booking URLs and terms before acting on any returned itinerary or purchase link.

Risk: The security summary notes weak execution safeguards around provider-specific booking output.

Mitigation: Review CLI output before sharing recommendations and avoid using results that lack the expected booking URL.

## Reference(s):

- [Skill page](https://clawhub.ai/liquanyu123/skills/yoga-retreat)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include provider booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
