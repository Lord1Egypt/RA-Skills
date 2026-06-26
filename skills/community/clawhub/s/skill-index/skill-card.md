## Description: <br>
Multi-platform skill ranking and discovery system for 25,000+ skills across Tencent SkillHub, Xfyun SkillHub, and local installations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runze123](https://clawhub.ai/user/runze123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to discover, compare, rank, and install skills from Tencent SkillHub, Xfyun SkillHub, and local installations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install workflow can execute external skill installation commands. <br>
Mitigation: Prefer --dry-run first, verify the skill name, source, and publisher, and install only after explicit user confirmation. <br>
Risk: GitHub tokens or other configuration values may be stored locally if users add them to the skill configuration. <br>
Mitigation: Avoid storing sensitive tokens in plaintext config unless the local exposure risk is understood and acceptable. <br>


## Reference(s): <br>
- [Skill Rank Architecture](references/architecture.md) <br>
- [ClawHub release page](https://clawhub.ai/runze123/skill-index) <br>
- [Tencent SkillHub](https://skillhub.tencent.com) <br>
- [Xfyun SkillHub](https://skill.xfyun.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local SQLite ranking database and may invoke external skill installation CLIs when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
