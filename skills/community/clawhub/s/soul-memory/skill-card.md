## Description: <br>
Soul Memory provides a local long-term memory system for OpenClaw agents, with memory indexing, search, automatic context injection, heartbeat consolidation, CLI access, and an optional web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofqin2026](https://clawhub.ai/user/kingofqin2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain local, searchable agent memory, retrieve relevant context before responses, and manage memory through CLI, plugin, heartbeat, and optional web interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read OpenClaw session logs, store conversation content, and inject stored memory into future prompts. <br>
Mitigation: Install only when persistent local memory is intended, avoid storing secrets or credentials, and periodically review saved memory files before enabling automatic injection. <br>
Risk: The installation flow modifies OpenClaw plugin configuration and persistent scheduling through heartbeat or cron-style automation. <br>
Mitigation: Review planned configuration changes before installation, keep backups of OpenClaw workspace and memory files, and disable the plugin or scheduled jobs when automatic memory processing is not needed. <br>
Risk: The plugin invokes local shell commands to run memory search before prompt construction. <br>
Mitigation: Review and patch the plugin shell execution path before enabling it, and restrict writable access to the Soul Memory workspace. <br>
Risk: The optional web dashboard can expose local conversation memory. <br>
Mitigation: Keep the web UI bound to localhost, add authentication before remote access, and avoid exposing it on shared or public networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingofqin2026/soul-memory) <br>
- [Publisher profile](https://clawhub.ai/user/kingofqin2026) <br>
- [Project homepage from ClawHub metadata](https://github.com/kingofqin2026/Soul-Memory-) <br>
- [Skill manifest and user documentation](artifact/SKILL.md) <br>
- [Installation guide](artifact/INSTALL_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets, plus JSON CLI and plugin configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local memory search results, distilled memory summaries, OpenClaw prepend context, status text, and configuration instructions.] <br>

## Skill Version(s): <br>
3.5.13 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
