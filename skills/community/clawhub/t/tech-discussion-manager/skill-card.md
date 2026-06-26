## Description: <br>
标准化管理技术讨论全生命周期：讨论记录 → 决策沉淀 → 架构文档 → 开发规划。支持 Git 版本管理（可选）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ah0210](https://clawhub.ai/user/ah0210) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to record technical discussions, preserve decisions, generate architecture and development planning documents, and optionally record release versions in Git. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discussion records may save sensitive project details or secrets to disk. <br>
Mitigation: Use the skill only in intended workspaces, avoid recording secrets, and review generated markdown before sharing. <br>
Risk: The optional version-recording flow can commit or tag unintended workspace changes. <br>
Mitigation: Check git status and staged files before allowing the Git commit or tag step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ah0210/tech-discussion-manager) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ah0210) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, index tables, workspace directory structure, and optional Git command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates workspace-local discussion, decision, architecture, and development-plan files; optional Git commits and tags only when explicitly requested.] <br>

## Skill Version(s): <br>
0.8.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
