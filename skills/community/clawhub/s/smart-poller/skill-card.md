## Description: <br>
Periodically polls a Feishu task board, detects pending tasks assigned to the current AI agent, and writes completion feedback to the board. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[socneo](https://clawhub.ai/user/socneo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use Smart Poller to coordinate asynchronous work through a shared Feishu task board, where each agent polls for tasks assigned to its configured identity and posts status feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mark Feishu tasks as completed even when it has only generated canned status text. <br>
Mitigation: Treat completion feedback as a status signal, not proof of work; review important task results before accepting them. <br>
Risk: The skill uses Feishu app credentials and a document token from local configuration. <br>
Mitigation: Use a dedicated least-privilege Feishu app, keep config.json private, and restrict who can edit the task board. <br>
Risk: Recurring polling can repeatedly modify a shared remote task board. <br>
Mitigation: Test with --once before enabling scheduled polling and monitor the board after deployment. <br>


## Reference(s): <br>
- [Smart Poller on ClawHub](https://clawhub.ai/socneo/smart-poller) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [README.md](artifact/README.md) <br>
- [README.zh-CN.md](artifact/README.zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and plain-text task feedback written to Feishu.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run once for testing or on a recurring polling interval; uses Feishu app credentials and a document token supplied in local configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact changelog v1.0.0, released 2026-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
