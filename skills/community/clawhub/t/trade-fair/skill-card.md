## Description:

Book flights for trade fairs and exhibition travel. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-booking agents use this skill to search and present trade fair or exhibition flight options through the flyai CLI, including booking links and user-language-matched Markdown results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may globally install an unpinned third-party npm CLI before use.

Mitigation: Review before installing, prefer explicit user approval, and use a pinned or local package install where possible.

Risk: Flight-search details are sent to a commercial CLI service and results include service-provided booking links.

Mitigation: Disclose the booking provider and currency assumptions, and verify booking links before presenting them to users.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [ClawHub skill page](https://clawhub.ai/liquanyu123/skills/trade-fair)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands when setup or troubleshooting is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include a booking link for every listed result, and match the user's language.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
