## Description:

Manage Todoist tasks, projects, labels, and sections via the `todoist` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddyh](https://clawhub.ai/user/buddyh)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage Todoist tasks, projects, labels, sections, comments, and completed tasks through the `todoist` command-line interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Todoist API tokens can expose personal or business task data if typed directly into commands, stored in shell history, or shared through environment output.

Mitigation: Prefer interactive authentication, avoid pasting tokens into command history, and rotate the token if exposure is suspected.

Risk: The skill installs an unpinned third-party CLI through Homebrew or `go install ...@latest`.

Mitigation: Install only after trusting the publisher and review or pin the upstream CLI version before managed deployment.

## Reference(s):

- [Todoist developer integrations settings](https://todoist.com/app/settings/integrations/developer)
- [ClawHub skill page](https://clawhub.ai/buddyh/skills/todoist-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON-producing CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may use Todoist authentication and can request machine-readable output with `--json`.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
