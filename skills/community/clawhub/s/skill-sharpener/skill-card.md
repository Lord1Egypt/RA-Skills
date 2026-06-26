## Description: <br>
Skill Sharpener evaluates existing Agent Skill directories, reviews metadata, structure, content, examples, and scripts, and produces optimization recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxxxu](https://clawhub.ai/user/liuxxxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit Agent Skill quality, identify high-priority issues, and draft improvements before publishing or updating a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed fixes or rewrites could introduce incorrect or misleading skill guidance. <br>
Mitigation: Inspect the generated report and proposed changes before accepting edits or publishing the revised skill. <br>
Risk: The skill can be used to inspect local skill directories and may optionally modify files after approval. <br>
Mitigation: Point it only at the intended skill directory and keep backups until the edited skill has been verified. <br>


## Reference(s): <br>
- [Skill Quality Evaluation Checklist](references/checklist.md) <br>
- [Claude Agent Skills Best Practices](https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/best-practices) <br>
- [TRAE CN Skill Best Practices](https://docs.trae.cn/ide/best-practice-for-how-to-write-a-good-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code review findings, Guidance] <br>
**Output Format:** [Markdown report with optional shell commands and proposed edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose user-approved edits to skill files; review changes before accepting them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
