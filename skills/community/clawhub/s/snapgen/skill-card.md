## Description:

Use this skill when the user asks to open, run, or automate a specific desktop application. It manages the full lifecycle of automation scripts within dedicated application folders, handling class-based automation execution. This skill relies on the Python environment and the `clicknium` package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snapgen](https://clawhub.ai/user/snapgen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use SnapGen to create, extend, document, and run desktop application automations on Windows using Python and Clicknium.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control desktop applications and generate, save, and immediately run Python automation code.

Mitigation: Install only from a trusted publisher, supervise automation runs, and review generated code and diffs before execution.

Risk: The skill can use the global Python environment and install Clicknium with an unpinned upper version.

Mitigation: Use a virtual environment or isolated Windows profile and review dependency versions before installation.

Risk: Desktop automation may interact with sensitive applications or data.

Mitigation: Avoid using it with sensitive apps unless the automation can be closely supervised.

## Reference(s):

- [SnapGen ClawHub skill page](https://clawhub.ai/snapgen/skills/snapgen)
- [SnapGen publisher profile](https://clawhub.ai/user/snapgen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated automation artifacts may include Python, Markdown, and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create per-application automation folders and temporary driver scripts; returned application data is expected as ordered list values.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
