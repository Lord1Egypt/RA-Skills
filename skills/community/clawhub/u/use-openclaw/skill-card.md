## Description:

Explain how to use OpenClaw in a local environment. Use when the user asks how to find OpenClaw config or workspace files, how to add or inspect skills, how to understand the purpose of AGENTS.md or workspace notes, how to troubleshoot OpenClaw setup issues, or how to complete a common OpenClaw task step by step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selena000](https://clawhub.ai/user/selena000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect local OpenClaw configuration, workspace files, installed skills, logs, and extensions, then get concise operational guidance for setup, common tasks, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local OpenClaw configuration, workspace notes, user context, and logs that contain sensitive or personal information.

Mitigation: Ask the assistant to inspect only the specific file or log needed and redact secrets or personal details before summarizing.

Risk: When asked to fix setup or skill issues, the skill may propose edits to local OpenClaw configuration, workspace notes, or skill files.

Mitigation: Review proposed changes, keep edits limited to the smallest relevant file, and validate the result before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/selena000/skills/use-openclaw)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline file paths and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise summaries of inspected local files and minimal edit recommendations when requested.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
