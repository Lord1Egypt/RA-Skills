## Description: <br>
需求澄清与执行确认。用于日常代码任务（修改、重构、优化、添加注释等）。当用户提出需求时，先通过快速追问（3-5 轮）完善需求，执行前根据规则判断是否需要确认。与 brainstorming（复杂系统设计）互补。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trackoverflow](https://clawhub.ai/user/trackoverflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to clarify routine code-change requests before execution and decide when a proposed change needs explicit confirmation. It is intended for everyday edits such as refactoring, optimization, formatting, comments, renames, and scoped modifications rather than complex system design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad auto-execution defaults can allow routine single-file, rename, formatting, and code-organization edits without explicit approval. <br>
Mitigation: Review config/rules.yaml before deployment and tighten or disable auto_execute settings when every code change should require approval. <br>
Risk: Ambiguous code-change requests may still be clarified incompletely before work begins. <br>
Mitigation: Use the questioning guide's structured rounds and require confirmation for logic changes, deletions, dependencies, migrations, and irreversible operations. <br>


## Reference(s): <br>
- [Questioning Guide](references/questioning-guide.md) <br>
- [Configuration Guide](references/config-guide.md) <br>
- [Rules Configuration](config/rules.yaml) <br>
- [ClawHub Skill Page](https://clawhub.ai/trackoverflow/requirement-agent) <br>
- [Skill Reference](https://skills.sh/requirement-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with structured questions, confirmation prompts, and YAML configuration rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; behavior is controlled by config/rules.yaml.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
