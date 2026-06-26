## Description: <br>
Task Router analyzes a user's request and routes it to the most appropriate downstream agent or skill based on configured keyword rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soroyue](https://clawhub.ai/user/soroyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to delegate incoming tasks to specialized agents or document/calendar-generation skills without manually choosing the route. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic keyword routing may delegate sensitive, financial, private-file, calendar, document, or business-data requests to downstream agents or skills. <br>
Mitigation: Review and trust the named downstream agents and skills before installation, and add confirmation or narrower routing rules for sensitive workflows. <br>
Risk: Broad keyword matches may route a request to the wrong downstream agent or skill. <br>
Mitigation: Confirm the selected route before acting on high-impact tasks or tune the routing rules to the user's environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soroyue/task-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Routing guidance in text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes are selected from keyword-based mappings to named downstream agents and skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
