## Description: <br>
Sanna governance governs tool calls transparently with constitution-based enforcement and cryptographic receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicallen-exd](https://clawhub.ai/user/nicallen-exd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route tool calls through Sanna governance, enforcing YAML constitution rules and recording receipts for allowed, blocked, or escalated actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external governance plugin for enforcement behavior. <br>
Mitigation: Review the @sanna-ai/openclaw plugin and its constitution settings before installation. <br>
Risk: Tool calls can be blocked or escalated, which may interrupt automated workflows. <br>
Mitigation: Test constitution rules in the target environment and define a clear human approval path for escalated actions. <br>


## Reference(s): <br>
- [Sanna Governance on ClawHub](https://clawhub.ai/nicallen-exd/sanna-governance) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown guidance with governed tool-call outcomes and persisted receipts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the @sanna-ai/openclaw plugin and node; governed tool calls may be allowed, blocked, or escalated for human approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
