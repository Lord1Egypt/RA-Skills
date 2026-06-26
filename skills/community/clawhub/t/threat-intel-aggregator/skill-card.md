## Description: <br>
Aggregates and analyzes threat intelligence data to check targets against known threats and security risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, incident responders, compliance professionals, and developers use this skill to check IPs, domains, file hashes, and URLs against aggregated threat intelligence and receive consolidated risk findings and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked indicators are sent to the ToolWeb/api.mkkpro.com service and may be shared with upstream intelligence sources. <br>
Mitigation: Do not submit internal hostnames, secret-bearing URLs, customer data, or sensitive incident-response indicators unless organizational policy approves that disclosure. <br>
Risk: Threat intelligence results and remediation recommendations may affect security response decisions. <br>
Mitigation: Review high-impact actions such as blocking or escalation against internal evidence and response procedures before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/threat-intel-aggregator) <br>
- [Threat Intel Aggregator API Route](https://api.mkkpro.com/security/threat-intel-aggregator) <br>
- [Threat Intel Aggregator API Docs](https://api.mkkpro.com:8009/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON threat assessment with human-readable remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include threat status, findings, confidence scores, risk score, recommendations, and aggregation timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
