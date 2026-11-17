## Description:

Playbook for authoring, running, evaluating, and improving Gina sandbox workflows with safe defaults and repeatable operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askginadotai](https://clawhub.ai/user/askginadotai)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to author, validate, run, evaluate, optimize, and roll back Gina sandbox workflows with explicit permissions, traceable artifacts, and repeatable operational checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow definitions can include powerful steps such as Bash or exec commands, filesystem access, KV operations, host-tool calls, external posting, or trading actions.

Mitigation: Review each workflow definition before running it, declare explicit side effects, keep step permissions narrow with allow and block rules, and validate the workflow before execution.

Risk: Secrets or sensitive data could be exposed if placed in workflow definitions, examples, artifacts, or logs.

Mitigation: Do not place raw secrets in definitions or logs, and inspect generated artifacts before sharing or retaining them.

Risk: Runtime errors, data shape changes, or degraded optimizations can produce failed runs or worse workflow behavior.

Mitigation: Use validation, run artifacts, evaluation records, baseline comparisons, and rollback steps to catch regressions and restore a prior workflow state.

## Reference(s):

- [Workflow CLI And Definition Reference](references/cli-and-definition.md)
- [Eval, Optimize, And Artifacts](references/eval-optimize-and-artifacts.md)
- [Polymarket Workflow Patterns](references/polymarket-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript, SQL, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce workflow definitions, runnable execution plans, artifact inspection steps, evaluation records, baseline comparisons, and rollback guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
