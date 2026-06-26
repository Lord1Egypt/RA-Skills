## Description: <br>
Evaluate-before-execute guardrail for OpenClaw agents that returns ALLOW, BLOCK, or ADVISE decisions before high-stakes tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanjeet-toosi](https://clawhub.ai/user/sanjeet-toosi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to evaluate proposed web search, booking, payment, and shell-command actions before execution. It helps agents enforce configured safety and preference policies by returning a structured decision and suggested alternative. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation inputs may include secrets, payment details, private travel data, or sensitive shell commands that are sent to configured LLM providers or logs. <br>
Mitigation: Redact sensitive payloads before evaluation, use only approved provider endpoints, and prefer a trusted local endpoint for sensitive deployments. <br>
Risk: The artifact contains conflicting packaged skill identities and install paths, including agent-sentinel at the package root and agent-eval-engine under skills/vigilance. <br>
Mitigation: Review the installed files before use and ask the publisher to reconcile the package identity, documented invocation path, and release metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sanjeet-toosi/vigilance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON decision output with Markdown handling guidance and shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns decision, severity, reason, and alternatives fields; may rely on configured LLM provider keys for judge-based checks.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
