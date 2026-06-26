## Description: <br>
Bridge communication between subagents via sessions_send - pipeline, debate, broadcast, and aggregate patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanshojin](https://clawhub.ai/user/hanshojin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route messages among active OpenClaw subagents for pipeline, debate, broadcast, and aggregate workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages may be forwarded to the wrong active subagent or broadcast more widely than intended, including sensitive content. <br>
Mitigation: Use clear subagent names and explicit routing instructions; avoid broadcasting sensitive content unless every recipient is known. <br>
Risk: Subagent routing can fail when target subagents are no longer active or when cross-agent routing is not enabled. <br>
Mitigation: Confirm the target session is active and that required agent-to-agent configuration is enabled before routing messages. <br>


## Reference(s): <br>
- [Pipeline + Debate Commands](references/pipeline-debate-commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/hanshojin/subagent-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces routing guidance and command patterns for active subagent sessions; no files are produced by the skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
