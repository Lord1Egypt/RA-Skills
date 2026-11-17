## Description:

Use when the user asks to personalize their assistant, to use vardoger, or to analyze their OpenClaw conversation history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dstrupl](https://clawhub.ai/user/dstrupl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and assistant users use this skill to analyze OpenClaw conversation history with the vardoger CLI and generate persistent personalization instructions for assistant behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private conversation history.

Mitigation: Run it only after explicit user consent and only in trusted local environments.

Risk: The skill writes persistent assistant rules that can change future assistant behavior.

Mitigation: Review the generated markdown before writing it and keep a rollback path for the previous rules file.

Risk: The provided echo-based write example can mishandle generated markdown.

Mitigation: Use a safer stdin or file-based mechanism when passing personalization content to vardoger.

Risk: The vardoger commands need filesystem access outside the workspace.

Mitigation: Use a pinned, reviewed vardoger version and grant expanded file access only for the specific command being run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dstrupl/skills/vardoger-analyze)
- [dstrupl publisher profile](https://clawhub.ai/user/dstrupl)
- [Vardoger project page](https://github.com/dstrupl/vardoger)
- [pipx installation documentation](https://pipx.pypa.io/stable/installation/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown personalization guidance with shell commands and concise status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the vardoger CLI and explicit user consent before reading conversation history or writing persistent assistant rules.]

## Skill Version(s):

0.3.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
