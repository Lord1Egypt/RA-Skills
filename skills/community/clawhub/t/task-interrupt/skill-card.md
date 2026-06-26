## Description: <br>
Provides task interruption guidance and shell tools for stopping long-running agent work, cleaning resources, and preserving task state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyxlouspg](https://clawhub.ai/user/guyxlouspg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add stop-command handling, stop-flag checks, checkpointing, and cleanup behavior to long-running agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interrupt controls can stop or signal the wrong task when session IDs or process ownership are not scoped. <br>
Mitigation: Validate session IDs, bind stop requests to the correct owned session and process, and restrict who may trigger stop commands. <br>
Risk: Temporary stop-flag files can be tampered with or reused if they are not protected. <br>
Mitigation: Use restrictive file permissions, verify flag age and ownership before acting, and clear stale flags promptly. <br>
Risk: Checkpoint and state files may contain sensitive task data. <br>
Mitigation: Keep checkpoints minimal, avoid storing secrets, and apply a clear cleanup policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guyxlouspg/task-interrupt) <br>
- [OpenClaw documentation](https://openclaw.org/docs) <br>
- [AgentSkill specification](https://clawhub.com/specs/agent-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes stop-flag commands and integration guidance for session IDs, checkpoints, and cleanup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
