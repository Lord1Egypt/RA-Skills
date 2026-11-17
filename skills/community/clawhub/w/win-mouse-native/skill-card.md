## Description:

Native Windows mouse control (move, click, drag) via user32.dll. Use when the user asks you to move the mouse, click, drag, or automate pointer actions on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lurklight](https://clawhub.ai/user/lurklight)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an agent perform explicit Windows mouse movements, clicks, and button down/up actions through local scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move and click the Windows pointer, which may trigger unintended UI actions or interact with sensitive prompts.

Mitigation: Use it only for explicit, supervised tasks, start with small reversible actions when uncertain, and avoid sensitive or destructive screens.

Risk: The provided scripts must be saved and run locally, including a PowerShell command that uses ExecutionPolicy Bypass.

Mitigation: Inspect the local script before renaming and running it, and install it only when local Windows mouse automation is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the local script returns one-line JSON objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows only; supports relative movement, absolute positioning, and left, right, or middle button actions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
