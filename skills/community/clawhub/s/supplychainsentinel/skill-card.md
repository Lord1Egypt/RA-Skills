## Description: <br>
Monitor supplier APIs, port delays, and weather in real-time to trigger automatic PO rerouting and stakeholder alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncreighton](https://clawhub.ai/user/ncreighton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Supply chain, procurement, logistics, and operations teams use this skill to monitor shipment, supplier, port, weather, and ERP signals, then generate disruption alerts, ETA updates, rerouting guidance, and purchase-order response actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic purchase-order creation or ERP updates could trigger unintended financial or operational changes. <br>
Mitigation: Disable automatic PO creation until validated and require human approval for all ERP or purchase-order writes. <br>
Risk: Live logistics, database, email, and Slack credentials could expose sensitive business data or allow broad outbound notifications. <br>
Mitigation: Use test or least-privilege credentials first, store secrets in a secret manager, and restrict Slack and email recipients. <br>
Risk: Long-running monitoring jobs may continue acting on stale thresholds or noisy external signals. <br>
Mitigation: Use clear stop controls, audit logs, conservative alert thresholds, and monitoring-only validation before enabling rerouting automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ncreighton/supplychainsentinel) <br>
- [Publisher profile](https://clawhub.ai/user/ncreighton) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, SQL, YAML, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API polling plans, supplier health summaries, ETA recalculation reports, Slack or email alert drafts, and ERP or purchase-order action recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
