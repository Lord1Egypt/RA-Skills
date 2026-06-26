## Description: <br>
Create structured incident response runbooks with step-by-step procedures, escalation paths, and recovery actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, incident commanders, and on-call engineers use this skill to create or adapt incident response runbooks for service outages, database incidents, escalation paths, recovery procedures, and stakeholder communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example production commands for Kubernetes, databases, feature flags, and network policies could change live systems if copied directly. <br>
Mitigation: Treat commands as examples, adapt them to the target environment, verify targets, use least-privileged credentials, and require human approval for production-changing actions. <br>
Risk: Runbook templates can become incorrect or misleading if they are not tailored to current service ownership, dashboards, dependencies, and escalation paths. <br>
Mitigation: Review and test generated runbooks before deployment, and update them after incidents or operational changes. <br>


## Reference(s): <br>
- [Google SRE Book - Managing Incidents](https://sre.google/sre-book/managing-incidents/) <br>
- [PagerDuty Incident Response](https://response.pagerduty.com/) <br>
- [Atlassian Incident Management](https://www.atlassian.com/incident-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, SQL, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes template checklists, escalation matrices, communication examples, and verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
