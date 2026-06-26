## Description: <br>
Adaptive local skill scheduler for OpenClaw that helps an agent decide when to suggest installed skill combinations for multi-step or cross-domain tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route complex user requests toward relevant local skills or skill combinations before proceeding with the task. It is intended for OpenClaw workflows where the agent can inspect local skill registries, propose routing options, and record routing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw user task text may be written to a persistent local routing log. <br>
Mitigation: Do not use the skill with secrets, credentials, personal data, or private business context unless logging is disabled or redacted. <br>
Risk: The scripts use fixed local workspace paths, which can cause routing or logging to target an unintended location. <br>
Mitigation: Review and adjust local paths before use, especially on shared machines or non-default OpenClaw installations. <br>
Risk: Routing suggestions can steer an agent toward unnecessary or unsuitable skills. <br>
Mitigation: Treat suggestions as advisory, limit the number of loaded skills, and honor user rejection without repeated prompts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/spikesubingrui-design/spike-skill-orchestrator) <br>
- [Publisher Profile](https://clawhub.ai/user/spikesubingrui-design) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-formatted routing results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed skill names, skill combinations, acceptance mode, and local routing-log entries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
