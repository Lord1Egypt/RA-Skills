## Description:

Enables non-blocking AI agent execution by spawning parallel subagents for slow tasks, keeping the main agent responsive and efficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keugenek](https://clawhub.ai/user/keugenek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to structure long-running coding or research work around bounded turns, parallel subagents, progress reporting, and final result aggregation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad background execution, long shell commands, and recurring pollers.

Mitigation: Install only when that behavior is intended, review spawned commands, and run the skill in a sandboxed environment.

Risk: The bundled shark.sh can invoke Claude with permission bypass.

Mitigation: Avoid shark.sh unless the bypass flag is removed or the script is isolated in a sandbox.

Risk: State files and logs may contain task details, command output, or secrets.

Mitigation: Keep state files private and do not use the skill with commands or logs that may contain secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keugenek/skills/shark)
- [Project homepage](https://github.com/keugenek/shark-pattern)
- [Publisher profile](https://clawhub.ai/user/keugenek)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce progress summaries, timeout recommendations, background job status, and cleanup reports.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
