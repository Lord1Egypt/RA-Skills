## Description: <br>
Workplace manages multiple project directories with per-workspace agents, isolated memory, inter-agent communication, IDE context syncing, and chat UI controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dickwu](https://clawhub.ai/user/dickwu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize, switch, scan, link, and manage multiple project workplaces while coordinating project-specific agents, memory, sessions, deployment notes, and IDE context files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied workplace names or paths may trigger the confirmed command-injection issue identified by the security scan. <br>
Mitigation: Review and patch the initialization script before use, and avoid passing untrusted names, paths, or descriptions. <br>
Risk: The skill persistently mutates project directories, IDE context files, the home-directory workplace registry, and supermemory state. <br>
Mitigation: Run it only on trusted project paths after confirming the intended .workplace, IDE, registry, and memory writes. <br>
Risk: Initializing a parent folder may affect child repositories discovered as workplaces. <br>
Mitigation: Scope initialization and scanning to the specific project path unless child repositories are intended to be registered or changed. <br>


## Reference(s): <br>
- [ClawHub Workplace page](https://clawhub.ai/dickwu/workplace) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [README](README.md) <br>
- [Command Reference](references/commands.md) <br>
- [Agent System](references/agent-system.md) <br>
- [IDE Sync](references/ide-sync.md) <br>
- [Telegram UI](references/telegram-ui.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with shell commands, JSON or JSONC configuration, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workplace registry files, .workplace project files, IDE context files, deployment notes, and agent definitions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
