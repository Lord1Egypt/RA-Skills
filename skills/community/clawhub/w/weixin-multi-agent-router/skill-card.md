## Description: <br>
Design or implement single-entry multi-agent routing for OpenClaw Weixin setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeqiulee](https://clawhub.ai/user/zeqiulee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design or implement a Weixin plugin or extension that routes one account across configurable backend agents while preserving per-agent session isolation. It supports switching, status, reset, and summary-based handoff patterns for chat-facing multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loose natural-language command parsing could switch agents or reset context unexpectedly. <br>
Mitigation: Use exact or prefixed command matching and require confirmation for reset commands before applying state changes. <br>
Risk: Recent-history retention and handoff summaries could expose context across agents. <br>
Mitigation: Limit retained recent history and explicitly tell users when summaries are shared between agents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zeqiulee/weixin-multi-agent-router) <br>
- [Architecture](artifact/references/architecture.md) <br>
- [Commands](artifact/references/commands.md) <br>
- [Configurability](artifact/references/configurability.md) <br>
- [Validation](artifact/references/validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with configuration examples and implementation patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable design/reference skill; recommendations should be reviewed before live Weixin router deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
