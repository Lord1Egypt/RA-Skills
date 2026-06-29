## Description: <br>
Skill矩阵分发助手（免费版） helps skill creators publish, update, and manage free skills across Tencent SkillHub, 虾聊, 虾友SkillHub, GitHub, and ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingmuhuijianghu](https://clawhub.ai/user/qingmuhuijianghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, open-source contributors, and AI agent creators use this skill to prepare, validate, publish, update, and remove free skills across multiple skill marketplaces and GitHub. It provides conversational guidance plus command and API examples for platform-specific release flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores platform credentials in a local config.json and uses those credentials for publishing workflows. <br>
Mitigation: Use least-privileged platform tokens, keep credentials outside skill directories that may be uploaded, and review local config.json handling before installation. <br>
Risk: The skill can publish, update, or delete account content across several platforms. <br>
Mitigation: Keep dry-run or preview behavior enabled for destructive actions, require exact platform IDs before deletion, and review target records before execution. <br>
Risk: The installation flow references remote scripts. <br>
Mitigation: Review remote scripts and verify checksums before running installer commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingmuhuijianghu/skills/skill-matrix-publisher-free) <br>
- [Publisher profile](https://clawhub.ai/user/qingmuhuijianghu) <br>
- [虾友SkillHub](https://aiskillhub.vip) <br>
- [Tencent SkillHub](https://skillhub.cn) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for platform credentials and supports dry-run style confirmation before destructive deletion actions.] <br>

## Skill Version(s): <br>
3.7.15 (source: evidence release.version and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
