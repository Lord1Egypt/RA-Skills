## Description: <br>
Staff shift scheduling and management assistant for retail store managers and employees that answers shift queries, sends reminders, handles swap requests, and manages on-call routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail store managers and employees use this skill to answer personal and team shift questions, coordinate shift swaps and time-off requests, send reminders, and route on-call escalations to the current duty manager. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Employee schedule data and contact details may be exposed if the skill is connected to overly broad or public schedule sources. <br>
Mitigation: Use private, role-limited schedule sources and install only where the agent is authorized to access employee scheduling data. <br>
Risk: Personal shift answers, manager-wide schedule views, swap approvals, and time-off requests can reveal or change sensitive staffing information. <br>
Mitigation: Require authenticated staff identity for personal queries and restrict manager-wide views, schedule changes, approvals, archives, swap history, leave requests, and contact fields to approved roles. <br>
Risk: Schedule archives, swap history, leave requests, and contact fields can create unnecessary retention exposure. <br>
Mitigation: Define retention rules for schedule archives, swap history, leave requests, and contact fields before deployment. <br>


## Reference(s): <br>
- [Schedule Data Formats](references/schedule-formats.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fangwei-frank/shift-scheduler) <br>
- [Publisher Profile](https://clawhub.ai/user/fangwei-frank) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance, Configuration] <br>
**Output Format:** [Natural-language shift responses, approval messages, reminders, and structured schedule JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English and Chinese schedule queries and can surface validation warnings before schedule activation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
