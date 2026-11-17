## Description:

Guides AI agents through workspace token audits, token-waste findings, and targeted cleanup with optional dry-run scans and tiktoken-based counting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scan AI-agent workspaces, identify high-token context files, and guide cleanup into lighter memory layouts. It is also used to re-scan workspaces and optionally configure concise agent response habits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter workspace files and persistent agent instructions during cleanup flows.

Mitigation: Prefer dry-run first, review proposed changes before approval, and create backups before any file modification.

Risk: Batch mode and brutal mode can make broad or persistent behavior changes with less per-item confirmation.

Mitigation: Use confirm mode for normal cleanup, enable batch or brutal mode only after reviewing the intended changes, and keep the documented disable or rollback path available.

Risk: The bundled installer can install unpinned third-party software and trigger tokenizer cache network behavior.

Mitigation: Avoid the installer unless that dependency and network behavior are acceptable; otherwise use the scanner's heuristic fallback or run installation in a controlled environment.

## Reference(s):

- [Token Saving Strategies](references/strategies.md)
- [Mode A: First-time Setup](references/mode-a-onboarding.md)
- [Mode B: On-demand Re-scan](references/mode-b-rescan.md)
- [tiktoken](https://github.com/openai/tiktoken)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write workspace scan history unless run with dry-run; precise token counts depend on optional tiktoken availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
