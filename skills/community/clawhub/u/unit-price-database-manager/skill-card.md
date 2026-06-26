## Description: <br>
Manage construction unit price databases: update prices, track vendors, apply location factors, maintain historical records. Essential for accurate estimating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction estimators, cost engineers, and project controls teams use this skill to maintain unit price records, look up current and historical prices, track vendor quotes, apply location factors, and identify stale pricing before estimates or bids are finalized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filesystem import and export operations can modify or expose construction unit price database files, including proprietary vendor pricing records. <br>
Mitigation: Use explicit project CSV paths, keep backups, and limit agent filesystem access to intended price database locations. <br>
Risk: Bulk escalation, location factor, or stale-price updates can affect estimates, bids, and cost-control decisions if applied incorrectly. <br>
Mitigation: Review bulk changes, documented factors, and generated reports before using updated prices in commercial estimates or bids. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured price records, reports, and optional Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write intended CSV price database files when the agent has filesystem access.] <br>

## Skill Version(s): <br>
2.0.0 (source: claw.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
