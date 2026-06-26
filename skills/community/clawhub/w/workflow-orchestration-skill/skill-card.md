## Description: <br>
Compiles complex business goals into statically validated workflow execution plans (Plan IR). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to break a multi-step business goal into a structured DAG plan, bind planned nodes to an allowed skill manifest, and validate the resulting Plan IR before a separate workflow engine executes it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation scripts update the plan file in place, which can change hashes, signatures, or the original audit artifact. <br>
Mitigation: Run validators on a working copy of plan.json when the original artifact must be preserved. <br>
Risk: Workflow plans can be mistaken for execution authority even though the skill only drafts and validates plans. <br>
Mitigation: Require downstream workflow-engine approval and human review for high-risk plans before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tuobadaidai/workflow-orchestration-skill) <br>
- [Orchestration Rules](references/orchestration_rules.md) <br>
- [DAG Patterns](references/dag_patterns.md) <br>
- [Scope Rules](references/scope_rules.md) <br>
- [Security Guardrails](references/security_guardrails.md) <br>
- [Plan IR Output Schema](assets/output_schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Structured Plan IR JSON with validation reports and supporting Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plans only; actual workflow execution is handled by a separate engine.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
