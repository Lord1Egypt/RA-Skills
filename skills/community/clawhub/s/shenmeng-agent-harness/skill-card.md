## Description: <br>
Agent Harness helps agents create, configure, and manage ACP coding-agent sessions for Claude Code, Codex, and Gemini CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to route coding tasks to configured ACP agents, start persistent or one-shot sessions, send follow-up instructions, and monitor or terminate active agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate development work to persistent or one-shot coding agents that may modify or propose changes for workspace files. <br>
Mitigation: Confirm the target agent, task, workspace, files, timeout, and session mode before use, and review generated outputs before applying changes. <br>
Risk: The SkillPay integration includes an account-bound API key and external payment verification flow. <br>
Mitigation: Treat the bundled key and payment boundary as unresolved until reviewed, and avoid relying on the payment script for sensitive account controls. <br>
Risk: Delegated agents may receive sensitive private code or secrets if prompts and attachments are not scoped carefully. <br>
Mitigation: Do not send secrets or sensitive private code to external agents unless the configured provider and data-handling path are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-agent-harness) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with command, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ACP agent IDs, session modes, task prompts, timeouts, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
