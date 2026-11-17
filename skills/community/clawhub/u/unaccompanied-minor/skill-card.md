## Description:

Search for flights with unaccompanied minor service for children traveling alone, plus related travel booking tasks, powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-booking agents use this skill to collect route details, run Flyai/Fliggy flight searches, and present unaccompanied-minor flight options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run an unpinned global Flyai CLI.

Mitigation: Require explicit approval before installation, prefer a pinned audited package version, and run the CLI in a sandbox or project-local environment.

Risk: User-derived route, date, and price inputs are passed into shell commands.

Mitigation: Validate city, airport, date, and price values before execution and avoid adding parameters not listed by the skill.

Risk: Flight booking links may send users to external booking pages.

Mitigation: Check returned URLs before presenting booking links and clearly attribute results to Flyai/Fliggy CLI output.

## Reference(s):

- [Skill release page](https://clawhub.ai/liquanyu123/skills/unaccompanied-minor)
- [Parameter collection and output templates](artifact/references/templates.md)
- [Scenario playbooks](artifact/references/playbooks.md)
- [Failure recovery](artifact/references/fallbacks.md)
- [Execution runbook](artifact/references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from Flyai CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
