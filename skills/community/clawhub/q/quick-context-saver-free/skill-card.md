## Description: <br>
Quick Context Saver Free helps an agent store, search, list, and export local memory using project files and a TF-IDF-style CLI workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent local memory for preferences, decisions, facts, lessons, and project context without a cloud memory service. It is suited to offline or privacy-sensitive workflows where the user intentionally wants selected context written to local project files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to persist user and project context broadly to local files, including sensitive information if the user provides it. <br>
Mitigation: Use it only when local memory is intended; avoid secrets, regulated personal data, and confidential project details unless local storage is acceptable, and periodically inspect or delete memory files. <br>
Risk: The workflow relies on a globally installed CLI package before local memory commands are run. <br>
Mitigation: Verify the CLI package source before running the global npm install and review proposed shell commands before execution. <br>
Risk: The free artifact describes local memory storage but does not provide encrypted storage for sensitive memories. <br>
Mitigation: Do not store sensitive records unless local filesystem protections meet the user's requirements, or use a storage approach with encryption and access controls. <br>


## Reference(s): <br>
- [Quick Context Saver Free on ClawHub](https://clawhub.ai/thcjp/skills/quick-context-saver-free) <br>
- [Publisher profile: thcjp](https://clawhub.ai/user/thcjp) <br>
- [Packaged SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON file examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an agent with tool use and command execution; memory contents are stored in local project files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
