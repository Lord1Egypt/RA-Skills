## Description: <br>
Self-improving AI memory system with intelligent context injection and adaptive learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheBobLoblaw](https://clawhub.ai/user/TheBobLoblaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use Rune to add persistent memory, relevant context injection, project recommendations, and session-learning workflows to agent interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer persistently changes the OpenClaw workflow and may modify HEARTBEAT.md and create or update memory files. <br>
Mitigation: Install only when persistent workflow integration is desired; review added files under ~/.openclaw/workspace and keep backups of HEARTBEAT.md and memory.db. <br>
Risk: Stored memories and extracted facts can contain sensitive session, document, project, or personal context if the user adds or extracts it. <br>
Mitigation: Avoid storing secrets or sensitive personal data, periodically review stored facts and generated FACTS.md, and use dry-run or review flows before importing documents. <br>
Risk: Optional cloud extraction can send document context to OpenAI or Anthropic when API keys are configured. <br>
Mitigation: Use local Ollama extraction for private documents, or unset OPENAI_API_KEY and ANTHROPIC_API_KEY before processing sensitive material. <br>
Risk: The package installs npm dependencies and a global CLI. <br>
Mitigation: Review package.json, run npm audit or the installer verification mode, and use an isolated environment for high-security deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheBobLoblaw/rune) <br>
- [Publisher profile](https://clawhub.ai/user/TheBobLoblaw) <br>
- [README](artifact/README.md) <br>
- [Security information](artifact/SECURITY.md) <br>
- [Integration guide](artifact/INTEGRATION-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local files, CLI commands, workflow hooks, and memory maintenance steps for the agent environment.] <br>

## Skill Version(s): <br>
1.1.5 (source: SKILL.md frontmatter, package.json, skill.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
