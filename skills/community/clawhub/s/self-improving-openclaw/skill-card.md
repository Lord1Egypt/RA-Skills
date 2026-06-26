## Description: <br>
Self-Improving OpenClaw helps OpenClaw agents capture corrections, errors, feature requests, and recurring patterns in local workspace learning files, then review and promote stable patterns into tiered memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muhamadbasim](https://clawhub.ai/user/muhamadbasim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain a local learning loop for agent corrections, command failures, requested capabilities, and recurring workflow patterns. It supports private workspace memory review, promotion, demotion, archival, and transparent application of learned patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local workspace memory may retain corrections, preferences, errors, and recurring patterns longer than intended. <br>
Mitigation: Install only when persistent local memory is desired, periodically inspect .learnings and .self-improving, and archive or remove entries according to the documented workflow. <br>
Risk: Promoted memory could influence future agent behavior through AGENTS.md, SOUL.md, TOOLS.md, or MEMORY.md. <br>
Mitigation: Review promotions before relying on them long term, especially when entries affect operational rules, user preferences, or tool behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muhamadbasim/self-improving-openclaw) <br>
- [Project homepage](https://github.com/muhamadbasim/oktoclaw) <br>
- [Logging format](references/logging-format.md) <br>
- [Promotion and demotion rules](references/promotion-rules.md) <br>
- [Heartbeat review procedure](references/heartbeat-review.md) <br>
- [Workspace layout](references/workspace-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and workspace file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local workspace learning and memory files when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
