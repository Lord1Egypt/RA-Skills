## Description:

Generate an interactive HTML status page for the project at docs/status.html from TODO.md, CHANGELOG.md, git and the plan doc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bassemzohdy](https://clawhub.ai/user/bassemzohdy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to turn the project's TODO, changelog, Git state, and plan into a browsable status report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was incomplete because some referenced files were unavailable.

Mitigation: Check that the referenced files and the required todo core skill are available, and review them before relying on the report.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bassemzohdy/skills/todo-report)
- [GitHub source repository path (server-resolved provenance)](https://github.com/bassemZohdy/todo-skills/tree/main/plugin/skills/todo-report)

## Skill Output:

**Output Type(s):** [HTML, Files]

**Output Format:** [Self-contained interactive HTML status page]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a single file at docs/status.html; the page does not load resources from the network.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
