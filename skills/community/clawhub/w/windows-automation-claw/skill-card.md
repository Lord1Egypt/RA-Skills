## Description:

Automate Windows desktop tasks by launching apps, capturing screenshots, and simulating mouse and keyboard actions via PowerShell and Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaodu](https://clawhub.ai/user/xiaodu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation practitioners use this skill to perform Windows RPA-style desktop workflows, UI testing, data entry, and application control through command-line Python helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manipulate the live Windows desktop through mouse, keyboard, application launch, and process termination actions.

Mitigation: Use it only in controlled environments, require explicit confirmation for destructive or broad actions, and restrict allowed applications and processes.

Risk: Screenshot functions can capture visible information from the desktop or application windows.

Mitigation: Avoid sensitive screens, constrain screenshot output locations, and apply retention or redaction controls before sharing captured files.

Risk: PowerShell commands are built from user-provided values in several scripts.

Mitigation: Add strict input validation, argument allowlists, safe quoting or structured process APIs, and reject unexpected paths, process names, URLs, and window titles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaodu/skills/windows-automation-claw)
- [SKILL.md](artifact/SKILL.md)
- [Usage guide](artifact/使用说明.md)
- [Completion report](artifact/完成报告.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-style script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can produce screenshots, process/window listings, and success/error result objects.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
