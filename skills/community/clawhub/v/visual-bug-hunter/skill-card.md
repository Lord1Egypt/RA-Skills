## Description:

Visual Bug Hunter helps agents inspect GUI and web app screenshots, test UI interactions, locate likely code causes for visual defects, propose minimal fixes, and verify repairs with follow-up screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yitao2027](https://clawhub.ai/user/yitao2027)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate visual UI bugs, check interactions, map visible defects to project code, and produce concise fix and verification guidance for GUI or web applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live UI automation and code-changing workflows can click, type, launch apps, or alter project files without clear confirmation boundaries.

Mitigation: Ask for confirmation before clicking, typing, launching an app, or editing code, and review diffs before applying changes.

Risk: The optional CLI mentioned in the README adds a separate installation path outside the pure skill instruction workflow.

Mitigation: Pin a reviewed version or commit and install the optional CLI in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yitao2027/skills/visual-bug-hunter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON bug reports, Markdown verification reports, minimal code diffs, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should stay scoped to the named app or project directory and prioritize minimal diffs plus screenshot-based verification.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
