## Description:

Xlsx Cn helps agents create, read, edit, format, analyze, and recalculate Excel workbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

Anthropic Consumer or Commercial Terms of Service

## Use Case:

Developers and agents use this skill to create, modify, analyze, format, and validate Excel workbooks, including formula-driven financial models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LibreOffice automation may use an LD_PRELOAD shim that injects native code.

Mitigation: Run the skill only in an isolated environment and review or disable the shim before broader deployment.

Risk: Formula recalculation setup can leave persistent LibreOffice macro changes.

Mitigation: Use a disposable LibreOffice profile or back up existing macros, then remove or reset the macro profile after use.

Risk: Office archive extraction limits are not addressed for untrusted files.

Mitigation: Avoid untrusted Office files, or unpack them only in a sandbox with size, path, and resource limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/xlsx-cn)
- [Publisher profile](https://clawhub.ai/user/guohongbin-git)
- [OpenClaw fork metadata link](https://github.com/anthropics/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON status output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Office files when the agent follows the documented workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
