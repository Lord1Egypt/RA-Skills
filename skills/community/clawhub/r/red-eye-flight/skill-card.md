## Description:

Book red-eye flights with late night departure and overnight arrival, with support for related travel booking workflows powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-booking agents use this skill to collect route and date parameters, run flyai flight searches, and present red-eye flight options with booking links. It also guides fallback handling when results, installation, or network access fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and execute a global third-party npm CLI.

Mitigation: Use a trusted, pinned flyai CLI installation in a sandboxed environment before running searches.

Risk: Trip search details are sent to a third-party travel service.

Mitigation: Avoid submitting sensitive personal data and run the skill only where third-party travel search is acceptable.

Risk: Returned booking links may lead outside the agent environment.

Mitigation: Review booking link destinations before opening or sharing them with users.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [ClawHub Skill Page](https://clawhub.ai/ivan97/skills/red-eye-flight)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with booking links and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses flyai CLI output as the source for flight options; results should include booking links and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
