## Description:

Automatically compresses AI conversation context with session summaries, task-scoped memory, and token budget checks to reduce long-session input size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thanksandyou](https://clawhub.ai/user/thanksandyou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long OpenClaw sessions within a smaller context budget by checking session health, summarizing history, and loading task-specific memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session summaries or selected file contents may be sent to the configured AI endpoint.

Mitigation: Verify the API URL and credentials before use, and avoid passing sensitive files or confidential session content.

Risk: AI-generated memory is persisted globally and may be loaded by future OpenClaw sessions.

Mitigation: Review generated memory before reuse, back up the memory directory, and isolate TOKEN_OPTIMIZER_MEMORY_DIR when testing or evaluating the skill.

Risk: Cleanup and uninstall paths can affect OpenClaw memory beyond this skill.

Mitigation: Do not run memory deletion commands unless intentional, and confirm the target directory before cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thanksandyou/skills/token-optimizer-off)
- [README.md](artifact/README.md)
- [INSTALL.md](artifact/INSTALL.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and script-generated text or JSON-like status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize session or selected file content, write Markdown memory summaries, and update session state under the configured memory directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
