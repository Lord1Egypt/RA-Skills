## Description: <br>
语义拆分与智能规划技能。将自然语言拆分为结构化需求块，基于5W2H维度提取与约束标注增强语义理解，双视角推理整合为单一执行步骤，支持自增强json沉淀机制。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to decompose user requests into structured semantic blocks, identify 5W2H details and constraint strength, and produce a single execution plan. It also guides agents in creating reusable JSON records for recurring task patterns when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist reusable JSON from prior tasks, which may capture sensitive, stale, or overly specific details. <br>
Mitigation: Keep generated JSON inside the intended semantic-split data directory, review records before reuse, and avoid storing sensitive details from past conversations or tasks. <br>
Risk: Scheduled or heavyweight automation can scan memory logs and write persistent JSON without a precise scope. <br>
Mitigation: Enable automation only with explicit source paths, date range, output directory, review step, and deletion or redaction rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/semantic-split) <br>
- [Publisher profile](https://clawhub.ai/user/ldxs001) <br>
- [Split rules](references/split_rules.md) <br>
- [Loading decision tree](references/loading_decision_tree.md) <br>
- [Planning rules](references/planning_rules.md) <br>
- [JSON schema](references/json_schema.md) <br>
- [Constraint annotation](references/constraint_annotation.md) <br>
- [Automation tasks](references/automation_tasks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured task plans, JSON schemas, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local reusable JSON records under the configured semantic-split data directory when the user confirms execution or automation.] <br>

## Skill Version(s): <br>
2.5.0 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
