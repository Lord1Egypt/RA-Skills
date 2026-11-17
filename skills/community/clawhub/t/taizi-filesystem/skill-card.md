## Description:

Advanced filesystem operations - listing, searching, batch processing, and directory analysis for Clawdbot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to inspect directory contents, search files, copy matching files, render directory trees, and analyze filesystem structure from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package is missing the declared filesystem executable.

Mitigation: Prefer a ClawHub or package release that includes the executable and verify installation artifacts before enabling the skill.

Risk: The documentation points users toward unpinned external code with read-write filesystem access.

Mitigation: Use pinned, signed, or checksum-verified releases and restrict the skill to intended directories before running file operations.

Risk: Broad content searches can expose sensitive matched file content to the agent or logs.

Mitigation: Narrow search paths and patterns, avoid system-log examples unless necessary, and review matched content handling before use.

## Reference(s):

- [Taizi Filesystem on ClawHub](https://clawhub.ai/fresh3/skills/taizi-filesystem)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tabular, tree, list, or JSON-style filesystem output depending on the requested operation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
