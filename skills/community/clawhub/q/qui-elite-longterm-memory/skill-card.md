## Description: <br>
A memory setup skill that guides agents to create durable session state, curated memory files, vector recall, git-notes, and optional cloud-backed fact extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent project memory to coding agents through local markdown files, semantic recall, git-notes, and optional SkillBoss-backed sync and extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages durable cross-session memory, which can retain secrets, private conversations, regulated data, or sensitive project details longer than intended. <br>
Mitigation: Define what may be stored before use, review generated memory files regularly, and avoid storing sensitive data without an explicit retention and deletion process. <br>
Risk: Optional cloud backup and fact extraction can send memory content to a third-party service. <br>
Mitigation: Disable or avoid cloud backup and extraction unless the user explicitly trusts the provider and has approved the data that may be transmitted. <br>
Risk: The skill requires a sensitive API credential for SkillBoss-backed features. <br>
Mitigation: Provide the API key only through the runtime environment, keep it out of project files and logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quincygunter/qui-elite-longterm-memory) <br>
- [Publisher profile](https://clawhub.ai/user/quincygunter) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1) <br>
- [memory-lancedb plugin](https://clawdhub.com/skills/lancedb-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create SESSION-STATE.md, MEMORY.md, and memory daily-log files when the CLI init or today commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
