## Description: <br>
Guides an agent to create NocoBase workflows, including triggers, conditions, data operations, SQL, and scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alexander-lq](https://clawhub.ai/user/Alexander-lq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and NocoBase administrators use this skill to plan, create, enable, inspect, and clean up automated workflows for collection events, schedules, conditional branches, SQL operations, and request nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide persistent or destructive NocoBase workflow administration, including enabling workflows and deleting workflows. <br>
Mitigation: Use least-privilege NocoBase access, test in staging first, and require explicit approval before any enable or delete action. <br>
Risk: Workflow nodes may modify data, run SQL, or send HTTP requests to external destinations. <br>
Mitigation: Require the agent to show the target collection, trigger, SQL, webhook destination, workflow ID, and workflow title before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown guidance with inline NocoBase workflow tool-call examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
