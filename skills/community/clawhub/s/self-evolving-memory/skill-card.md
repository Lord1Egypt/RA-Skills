## Description: <br>
Orchestrates OpenClaw memory routing, promotion, hygiene, setup, and optional semantic recall across session state, daily notes, structured memory, root summaries, and enforcement files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hal-9909](https://clawhub.ai/user/hal-9909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and maintain a layered OpenClaw memory system. It helps agents capture task state, route durable preferences and system facts, promote stable knowledge, harden recurring issues into agent rules, and run setup or hygiene checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently manages OpenClaw memory files and may update agent-behavior files, which can affect future agent behavior. <br>
Mitigation: Review memory and rule-file changes before deployment, keep backups of existing memory or rule files, and point setup at the intended workspace. <br>
Risk: Memory content may include sensitive user or project information, and optional cloud embeddings can send memory-derived text to an external provider. <br>
Mitigation: Prefer local embeddings for sensitive memory unless the external provider and its data handling are trusted. <br>
Risk: The setup script copies templates and checks local configuration, so running it in the wrong workspace can create or modify the wrong memory structure. <br>
Mitigation: Inspect the setup script before execution and pass an explicit workspace path when auto-detection is ambiguous. <br>


## Reference(s): <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Embedding Setup Guide](references/embedding-setup.md) <br>
- [Runtime Protocol](references/runtime-protocol.md) <br>
- [Setup Checklist](references/setup-checklist.md) <br>
- [Skill Page](https://clawhub.ai/hal-9909/self-evolving-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and memory file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace memory files and recommended agent-behavior files when the memory action is clear.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
