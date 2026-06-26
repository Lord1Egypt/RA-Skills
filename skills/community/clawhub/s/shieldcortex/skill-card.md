## Description: <br>
Memory and defence for AI agents: semantic recall, knowledge graph and decay, plus a memory firewall that scans and enforces against prompt injection, credential leaks and poisoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis-drakon](https://clawhub.ai/user/jarvis-drakon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use ShieldCortex to add local persistent memory, semantic recall, knowledge graph features, and memory-write security enforcement to agent workflows across OpenClaw, Claude Code, Cursor, and Codex. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has privileged memory and security authority over local agent workflows. <br>
Mitigation: Install only when that authority is acceptable, review setup prompts before accepting changes, and periodically inspect ShieldCortex memories and audit logs. <br>
Risk: The runtime hook can automatically remove legacy hook folders and copy itself into OpenClaw hook paths outside the documented setup flow. <br>
Mitigation: Back up or inspect existing ~/.openclaw and ~/.clawdbot hook folders before setup, then verify the installed hooks after setup completes. <br>
Risk: Auto-memory, proactive recall, and cloud sync can increase exposure of sensitive conversation or memory content if enabled without review. <br>
Mitigation: Keep auto-memory, proactive recall, and cloud sync disabled unless needed; review ~/.shieldcortex memories and audit logs for sensitive snippets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jarvis-drakon/skills/shieldcortex) <br>
- [ShieldCortex documentation](https://shieldcortex.ai/docs) <br>
- [ShieldCortex homepage](https://shieldcortex.ai) <br>
- [ShieldCortex npm package](https://www.npmjs.com/package/shieldcortex) <br>
- [Publisher GitHub profile](https://github.com/Drakon-Systems-Ltd) <br>
- [ShieldCortex changelog](https://shieldcortex.ai/changelog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local memory, audit, hook, and MCP configuration changes when the user runs the documented commands.] <br>

## Skill Version(s): <br>
4.42.4 (source: ClawHub release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
