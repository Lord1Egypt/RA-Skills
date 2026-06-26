## Description: <br>
Govern a file-based shared-memory layer for OpenClaw multi-agent and subagent systems while preserving each agent's private memory and adding a separate, reviewable shared layer for stable user preferences, shared rules, and durable cross-agent facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiy29104983](https://clawhub.ai/user/jiy29104983) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to design, initialize, attach, maintain, and review a workspace-scoped shared-memory layer for multi-agent systems. It helps keep shared memory explicit, auditable, and separate from private assistant identity context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared memory may accidentally capture secrets or assistant identity context. <br>
Mitigation: Keep secrets and assistant identity context out of shared files, and review configured shared roots and memory sources before promotion. <br>
Risk: Attach or detach operations may leave local startup guidance inconsistent with the intended shared-memory state. <br>
Mitigation: Inspect AGENTS.md and SHARED_ATTACH.md after attach, detach, or repair operations. <br>


## Reference(s): <br>
- [Config Reference](references/config-reference.md) <br>
- [Shared Promotion Rules](references/shared-promotion-rules.md) <br>
- [Startup Guidance Rules](references/startup-guidance-rules.md) <br>
- [Status and Review Fields](references/status-review-fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command names, file-layout guidance, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable shared-memory governance instructions and configuration guidance; it does not include executable code.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
