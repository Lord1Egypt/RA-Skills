## Description:

Ultra Memory gives AI agents persistent cross-session memory with operation logging, session restore, keyword recall, summarization, and optional local semantic retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanjingya](https://clawhub.ai/user/nanjingya)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Ultra Memory to preserve work history across long or recurring tasks, recover prior sessions, and retrieve decisions, files, errors, and project context. It is intended for local memory workflows across Claude Code, OpenClaw, MCP, and REST API clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist broad work history in a local long-term memory store.

Mitigation: Use a private storage directory, avoid logging secrets, and scope storage per user or project.

Risk: The REST server can expose memory operations if made reachable without strong access controls.

Mitigation: Keep the server local by default and require a strong token before exposing it to shared or browser-accessible environments.

Risk: Shared environments may allow unintended access to session memory.

Mitigation: Review session ID validation and prefer isolated scopes for each user, project, or agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nanjingya/skills/ultra-memory)
- [Advanced configuration reference](references/advanced-config.md)
- [npm package](https://www.npmjs.com/package/ultra-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and local tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON, JSONL, and Markdown memory files when used in script, MCP, REST, or hook modes.]

## Skill Version(s):

4.3.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
