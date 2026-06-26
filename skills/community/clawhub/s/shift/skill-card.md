## Description: <br>
SHIFT manages multi-identity delegation to specialized AI sub-agents for coding, research, and quick tasks, routing and synthesizing responses within one OpenClaw conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palxislabs](https://clawhub.ai/user/palxislabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use SHIFT to route coding, research, analysis, and quick-task requests to configured specialist personas while keeping a single conversational interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated model calls can receive recent chat history, selected workspace file content, and MEMORY.md excerpts. <br>
Mitigation: Use transparent mode during evaluation, lower contextBridge.historyTurns, avoid sensitive files, and use trusted or self-hosted model providers for sensitive work. <br>
Risk: Delegation is hidden by default, which can make it harder to see when additional model calls are made. <br>
Mitigation: Switch to transparent mode before enabling routine use and review the configured personas, providers, and billing behavior. <br>
Risk: Local session files under ~/.openclaw/workspace/.shift/sessions may contain delegated context and outputs. <br>
Mitigation: Treat the .shift session directory as sensitive local data and configure shorter cleanup windows where appropriate. <br>


## Reference(s): <br>
- [SHIFT on ClawHub](https://clawhub.ai/palxislabs/shift) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline code blocks, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local delegation session files, persona configuration, and cost-tracking records under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
