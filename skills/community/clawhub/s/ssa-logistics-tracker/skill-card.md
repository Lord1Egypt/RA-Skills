## Description: <br>
Tracks shipment status through the 17Track batch API, sends customer email notifications, and alerts on delivery exceptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators and developers use this skill to batch-refresh shipment status, maintain local shipment records, extract tracking numbers, notify customers, and surface shipping anomalies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic shipment workflows can use customer and order data to update shipment state and send customer or internal notifications without per-action confirmation. <br>
Mitigation: Run dry-run mode first, review alert recipients and notification rules, and use least-privilege 17Track and SMTP credentials before enabling scheduled runs. <br>
Risk: Automatic lost or returned transitions and domain-based order matching can misclassify shipments or customers. <br>
Mitigation: Review exception transitions before acting on them and avoid domain-based order matching for production customer data unless it has been explicitly validated. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cjboy007/ssa-logistics-tracker) <br>
- [17Track API](https://api.17track.net/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local state files and external shipment, email, and alerting services when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
