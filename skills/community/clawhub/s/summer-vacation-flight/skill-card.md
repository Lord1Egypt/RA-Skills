## Description:

Book summer vacation flights for July and August holiday travel, with support for related travel services such as hotels, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rental, powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search summer vacation flights for July and August routes, compare recommended, cheapest, fastest, or direct options, and present bookable results from flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned third-party flight CLI globally.

Mitigation: Require explicit approval before installation, prefer a pinned local CLI inside a sandbox, and verify the CLI version before use.

Risk: Route and travel-date details are sent to a third-party flight service.

Mitigation: Inform users before execution and avoid sending unnecessary personal or sensitive travel details.

Risk: User-provided city and date values are used to construct shell commands.

Mitigation: Validate origin, destination, and date inputs, quote command arguments, and use only documented flyai parameters.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown flight summaries and comparison tables with booking links, backed by flyai CLI execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must include booking links from detailUrl values and should omit unlinked flight options.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
