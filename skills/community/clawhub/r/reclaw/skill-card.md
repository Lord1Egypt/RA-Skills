## Description: <br>
Use when accessing memory, recording information, searching prior context, or managing subjects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxpetretta](https://clawhub.ai/user/maxpetretta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Reclaw to access persistent memory, search prior context, record user-specific facts, decisions, tasks, and questions, and manage subject history across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain user-specific information across sessions. <br>
Mitigation: Install only when persistent memory is desired, and periodically inspect or remove stored memory if the environment supports it. <br>
Risk: Historical imports and transcript retrieval may expose sensitive prior conversation content. <br>
Mitigation: Review the Reclaw/OpenClaw runtime and imported histories before use, and limit transcript retrieval to cases where the prior context is needed. <br>


## Reference(s): <br>
- [Reclaw ClawHub listing](https://clawhub.ai/maxpetretta/reclaw) <br>
- [Reclaw homepage](https://github.com/maxpetretta/reclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw environment with the Reclaw plugin and openclaw binary available.] <br>

## Skill Version(s): <br>
2026.3.11-3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
