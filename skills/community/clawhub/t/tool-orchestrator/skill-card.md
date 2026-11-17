## Description: <br>
工具编排器 provides end-to-end encrypted, decentralized memory orchestration for agents, with unified memory retrieval, credential-handling, pairing, recovery, and CLI management guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install, pair, recover, and operate an encrypted memory plugin for cross-session user preferences and curated memories. It is aimed at agents that need privacy-focused memory search, explicit memory capture, and operational guidance for plugin setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages persistent encrypted memory and credential material. <br>
Mitigation: Use the browser-based pairing flow only, never paste recovery phrases into chat, and do not read or display credential files during installation or verification. <br>
Risk: The skill may restart its runtime integration automatically without asking the user for additional approval. <br>
Mitigation: Review the restart behavior before installation and limit recovery actions to the documented tool-orchestrator restart path rather than broad process or container restarts. <br>
Risk: The fallback pairing path may use a detached process that can outlive normal shell-tool controls. <br>
Mitigation: Prefer the in-process HTTP pairing route; use the detached fallback only when the route is unavailable and monitor or stop the process after pairing completes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tool-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Submitted skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes memory retrieval and capture guidance, browser-based pairing instructions, plugin recovery commands, and credential-handling constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
