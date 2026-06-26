## Description: <br>
任务自动续接 checks a workspace in_progress.md file for unfinished tasks and reminds the agent to continue the relevant work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep agents aware of unfinished workspace tasks at startup, especially when work depends on continuing items tracked in in_progress.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace task notes could contain secrets or sensitive task details. <br>
Mitigation: Keep in_progress.md limited to task-tracking notes and avoid storing secrets there. <br>
Risk: Stale task notes could steer the agent toward old or superseded work. <br>
Mitigation: Keep in_progress.md current and give newer instructions when priorities change. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/freedompixels/task-auto-continue) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown status reminder] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill reads workspace task-tracking notes and does not modify files.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
