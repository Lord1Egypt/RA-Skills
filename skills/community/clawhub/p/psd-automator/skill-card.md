## Description:

Automate PSD text replacement on Mac and Windows with Photoshop, dry-run safety, style-lock checks, rollback, and local PSD index cache.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhrxy](https://clawhub.ai/user/dhrxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design operations teams use this skill to route PSD or PSB edit requests into a structured task, modify Photoshop text layers or placed images, export PNG outputs, and return normalized execution results for chat workflows such as DingTalk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dry-run mode can still write audit data and may perform file copy or path-bridge preparation before returning a preview.

Mitigation: Review task files before execution, treat dry-run as a planning aid rather than a zero-write guarantee, and run in a constrained workspace when testing untrusted requests.

Risk: The local PSD index can persist a broad inventory of design files and metadata under the user's home directory.

Mitigation: Use explicit --root values for indexing, avoid broad Desktop or Documents defaults, and review or delete ~/.openclaw index and audit files when they are no longer needed.

Risk: Automatically routed chat requests can modify or export sensitive design assets if sender and output paths are not constrained.

Mitigation: Enforce sender allowlists, constrain task output paths, require dry-run review for untrusted input, and keep one write task per PSD at a time.

Risk: Style-lock soft retry can allow edits to proceed after a font or size mismatch.

Mitigation: Set styleLockSoftRetry to false when preserving text style integrity is required.

## Reference(s):

- [PSD Automator Task Schema](references/task-schema.json)
- [PSD Automator Error Codes](references/error-codes.md)
- [OpenClaw Subagent Routing](references/openclaw-subagent-routing.md)
- [ClawHub Skill Page](https://clawhub.ai/dhrxy/skills/psd-automator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, JSON task/result structures, shell commands, and generated PSD, PNG, ZIP, backup, index, and audit-log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit DingTalk image or file markers containing absolute output paths after successful PNG or ZIP export.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
