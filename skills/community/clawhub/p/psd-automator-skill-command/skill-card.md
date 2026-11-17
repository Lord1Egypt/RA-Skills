## Description:

Dispatch PSD automation tasks through skill command entry while reusing the same /psd orchestrator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhrxy](https://clawhub.ai/user/dhrxy)

### License/Terms of Use:


## Use Case:

Developers and design automation users use this skill to invoke PSD automation tasks through a skill command while relying on an existing psd-automator core workflow. It supports structured task paths or natural-language requests for PSD edits and output generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PSD automation can modify local design files or create output files in user-selected locations.

Mitigation: Use --dry-run for unfamiliar tasks and review the PSD source path and output path before execution.

Risk: Broad natural-language requests may produce unintended edits when applied to sensitive design files.

Mitigation: Use specific task descriptions and avoid sensitive PSD files unless the underlying psd-automator core workflow is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dhrxy/skills/psd-automator-skill-command)
- [Publisher profile](https://clawhub.ai/user/dhrxy)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run guidance and references to PSD input and output paths.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
