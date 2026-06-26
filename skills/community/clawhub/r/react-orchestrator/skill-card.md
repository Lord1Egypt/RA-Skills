## Description: <br>
React Orchestrator routes agent tasks between fast ReAct execution and deeper Reflexion-style reasoning, with tool registration, execution history, structured LLM prompts, Code Mode, and human approval support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a dual-mode ReAct orchestrator that routes simple tasks to a fast path and complex tasks to a reflective planning path. It is suited for registering tools, executing agent workflows, reviewing execution histories, and adding Code Mode or human approval controls around higher-risk actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Code Mode snippets can run with the user's normal system permissions. <br>
Mitigation: Review before installing, run in an isolated workspace or container, and treat Code Mode as arbitrary code execution rather than a sandbox. <br>
Risk: Registered tools can perform sensitive actions such as file writes, network calls, shell commands, PowerShell execution, or generated-code execution. <br>
Mitigation: Use explicit tool allowlists, least-privilege environment variables, and separate human confirmation for network calls, file writes, PowerShell, and generated code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/react-orchestrator) <br>
- [Artifact README](artifact/README.md) <br>
- [Usage Guide](artifact/USAGE-GUIDE.md) <br>
- [ReAct Paper](https://arxiv.org/abs/2210.03629) <br>
- [Reflexion Paper](https://arxiv.org/abs/2303.11366) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JavaScript API results, JSON execution history, and Markdown with code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tool-call results, reasoning histories, approval requests, and generated JavaScript or PowerShell snippets.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
