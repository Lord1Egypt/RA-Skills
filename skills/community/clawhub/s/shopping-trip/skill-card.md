## Description:

Helps agents collect shopping-trip travel parameters, run the flyai CLI, and format live flight and travel booking results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent to plan shopping-focused travel and compare live booking options. The skill guides the agent to collect route and date details, execute flyai commands, and return Markdown results with booking links instead of relying on model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify the host by globally installing an unpinned npm package.

Mitigation: Require user approval before installation, prefer an isolated and pinned CLI install, and verify the installed flyai version before use.

Risk: User-derived travel parameters are passed to a third-party CLI.

Mitigation: Validate origin, destination, dates, and option values against the documented parameter table before running commands.

Risk: Booking links and prices come from a third-party travel service.

Mitigation: Only present results with detailUrl booking links, check booking-link domains before showing them, and make clear that live availability comes from the CLI output.

Risk: CLI failures or empty results could lead an agent to fabricate travel options.

Mitigation: Retry only as described in the fallback guidance, then stop or ask for alternate dates/routes instead of answering from model knowledge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivan97/skills/shopping-trip)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI results; should not output raw JSON or booking options without detailUrl links.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
