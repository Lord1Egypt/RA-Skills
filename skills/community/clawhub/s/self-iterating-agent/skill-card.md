## Description: <br>
具备持续自主进化、长期记忆、全流程自主执行能力的高级自迭代智能体。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangruoqing86-stack](https://clawhub.ai/user/yangruoqing86-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to delegate long-running or complex automation tasks to an autonomous agent that plans, matches skills, executes steps, handles failures, tracks progress, and performs scheduled reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests unattended command execution, automatic installation, scheduled triggers, and high-control autonomous behavior. <br>
Mitigation: Run it only in a sandboxed environment with restricted sources, inspected logs, and explicit approval for high-risk actions. <br>
Risk: The skill can use long-term memory and bridge access, which may retain state or extend behavior across sessions. <br>
Mitigation: Grant memory or bridge access only when needed, and regularly disable or delete retained state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangruoqing86-stack/self-iterating-agent) <br>
- [Publisher profile](https://clawhub.ai/user/yangruoqing86-stack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or text with possible shell commands, task plans, progress updates, and configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger unattended execution, scheduled follow-up, automatic installation, cross-agent coordination, and retained long-term memory when granted those capabilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
