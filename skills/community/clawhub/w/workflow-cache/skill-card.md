## Description: <br>
Save up to 90% on Token costs. One agent explores, all agents benefit. Cloud-cached workflows with zero inference cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ainclaw](https://clawhub.ai/user/ainclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to look up cached Lobster workflows before LLM exploration, replay matching browser automations, and contribute successful session traces for reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically sends sensitive session-derived workflow data to a cloud service. <br>
Mitigation: Disable auto_contribute for sensitive sessions and only use the cloud endpoint when the publisher's handling of workflow, URL, intent, session, and failure telemetry is acceptable. <br>
Risk: The skill runs cloud-supplied browser workflows with limited user control. <br>
Mitigation: Review carefully before installing in workspaces involving credentials, internal sites, customer data, or regulated information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ainclaw/workflow-cache) <br>
- [Workflow Cache cloud API endpoint](https://api.workflowcache.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Agent response text with replayed browser workflow execution and configuration-driven cloud requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May replay cloud-supplied Lobster workflows or pass through to normal agent handling when no match is available.] <br>

## Skill Version(s): <br>
1.0.3 (source: skill.json, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
