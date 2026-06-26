## Description: <br>
让 AI 不敢摆烂的高压推进 skill。适用于任务反复失败、同一路径微调、想放弃、建议用户手动处理、没验证就下结论等场景。要求主动排查、换路径、拿证据闭环。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[knifehzh](https://clawhub.ai/user/knifehzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a task is stuck or repeatedly failing and they need a more exhaustive, evidence-based troubleshooting workflow before declaring completion or asking for help. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages more forceful and persistent execution during stuck tasks, which can exceed intended project, time, network, cost, or public-action limits if those limits are not explicit. <br>
Mitigation: Set clear boundaries for files, commands, network calls, time budget, and externally visible actions, and require explicit approval for destructive, costly, or public changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/knifehzh/pua-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with optional structured failure reports and command evidence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only skill; no code, hidden install behavior, credentials, or persistence were found in the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
