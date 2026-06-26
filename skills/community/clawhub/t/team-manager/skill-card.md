## Description: <br>
Manages a team's daily routine with morning briefings, evening reports, hourly report reminders, and day-off status handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirra87654321](https://clawhub.ai/user/mirra87654321) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Team leads and operational teams use this skill to coordinate daily check-ins, collect evening reports, remind members about missing reports, and track day-off status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records team response status locally in state.json. <br>
Mitigation: Decide what data may be stored, who can access it, and when it should be cleared before installation. <br>
Risk: Team status records may include sensitive HR, performance, medical, or private personnel details if users enter them. <br>
Mitigation: Use an explicit team policy for acceptable status content and avoid collecting sensitive details unless the organization has approved that use. <br>


## Reference(s): <br>
- [Team Manager ClawHub page](https://clawhub.ai/mirra87654321/team-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with team status prompts, reminders, and report guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to local state in state.json for team response status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
