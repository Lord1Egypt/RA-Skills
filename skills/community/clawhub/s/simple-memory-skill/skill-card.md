## Description: <br>
Zero-dependency AI memory system. No API keys needed. Pure local storage with smart search. Works everywhere. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add persistent local memory for preferences, decisions, lessons, and project context without API keys or cloud services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory may contain sensitive user or project information in plaintext. <br>
Mitigation: Avoid storing passwords, API keys, regulated personal data, or sensitive business details, and exclude SESSION-STATE.json, MEMORY.md, and memories/ from git, backups, and sync tools unless that exposure is intended. <br>
Risk: Stale or incorrect memories can influence future agent responses. <br>
Mitigation: Review memory-list, memory-stats, MEMORY.md, and stored memory files periodically, and delete or correct outdated entries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shianaixuexi-cell/simple-memory-skill) <br>
- [README](artifact/README.md) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local plaintext memory files such as SESSION-STATE.json, MEMORY.md, and memories/*.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
