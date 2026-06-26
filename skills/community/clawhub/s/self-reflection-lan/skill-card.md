## Description: <br>
Helps an agent keep structured local self-reflection notes for mistakes, lessons, feature requests, reusable snippets, and recurring patterns after work, errors, or new learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanlan314](https://clawhub.ai/user/lanlan314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain a local reflection journal that captures errors, reusable lessons, feature requests, snippets, and repeated-problem patterns in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reflection and memory notes may contain sensitive details from tasks or conversations. <br>
Mitigation: Review ~/.openclaw/workspace/reflections and ~/.openclaw/workspace/memory regularly, avoid storing secrets there, and apply workspace access controls appropriate to the environment. <br>
Risk: Optional scheduled reminders can run daily in the background. <br>
Mitigation: Enable the launchd schedule only when daily background execution is intended, and disable or remove it when reminders are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanlan314/self-reflection-lan) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with optional shell commands and local schedule configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local notes under reflections/ and memory/ when used as documented.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
