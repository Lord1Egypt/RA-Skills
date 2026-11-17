## Description:

Personal memo and todo management system. Use when user expresses intent related to remembering, tracking, or managing tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yfsong0709](https://clawhub.ai/user/yfsong0709)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this OpenClaw skill to let an assistant add, complete, review, and summarize personal tasks through natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled test script can remove existing pending and completed memo files in a real OpenClaw workspace.

Mitigation: Run the test script only in a disposable workspace or after backing up existing memo files.

Risk: Optional hooks, shell profile changes, symlinks, or cron summaries can create persistent local execution.

Mitigation: Enable persistent setup only after reviewing the files and confirming the scheduled behavior is wanted.

Risk: Ambiguous duplicate yf-memo install directories can cause the assistant to run an unintended copy of the scripts.

Mitigation: Keep the skill in a trusted install path and remove duplicate yf-memo directories before use.

## Reference(s):

- [User Guide](references/user-guide.md)
- [Implementation Guide](references/implementation.md)
- [Path Resolution Guide](references/path-resolution.md)
- [Cross-Platform Test Script](references/test-cross-platform.sh)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and script-generated text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads local pending and completed task markdown files in the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
