## Description:

Overseer watches OpenClaw sub-agents with local OS-level process checks and writes a status file that an agent heartbeat can read without polling sub-agents through model calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor OpenClaw sub-agents from a local background daemon, detect stalled or stopped work, and have heartbeat handlers read concise status without extra model/tool polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The status file may record basenames of recently changed files, which can reveal sensitive project details.

Mitigation: Use a narrow --workdir and pass --no-filenames when filename metadata should not be recorded.

Risk: --voice-files can speak changed filenames aloud in the local environment.

Mitigation: Avoid --voice-files in shared spaces; default voice alerts speak counts only.

Risk: A local background monitor can continue running after the immediate task is over.

Mitigation: Use --stop or --cleanup when monitoring is no longer needed.

## Reference(s):

- [TinkerClaw Subagent Overseer on ClawHub](https://clawhub.ai/globalcaos/skills/subagent-overseer)
- [TinkerClaw project repository](https://github.com/globalcaos/tinkerclaw)
- [agent-superpowers](https://clawhub.ai/globalcaos/agent-superpowers)
- [smart-model-router](https://clawhub.ai/globalcaos/smart-model-router)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and status-file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on running and reading a local overseer status file; no external service output is produced.]

## Skill Version(s):

1.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
