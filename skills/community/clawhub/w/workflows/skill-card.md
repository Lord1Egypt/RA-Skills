## Description: <br>
Playbook for authoring, running, evaluating, and improving Gina sandbox workflows with safe defaults and repeatable operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askginadotai](https://clawhub.ai/user/askginadotai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workflow operators use this skill to create, validate, run, evaluate, optimize, and roll back Gina sandbox workflows with explicit permissions, side effects, and reproducible artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflows created from this playbook can run commands, call tools, read and write files, query SQL, and persist logs or KV data. <br>
Mitigation: Review each workflow definition before execution, scope permissions by step, declare side effects, avoid direct interpolation of untrusted input, and keep secrets out of inputs, logs, artifacts, and KV entries. <br>


## Reference(s): <br>
- [Workflow CLI And Definition Reference](references/cli-and-definition.md) <br>
- [Eval, Optimize, And Artifacts](references/eval-optimize-and-artifacts.md) <br>
- [Polymarket Workflow Patterns](references/polymarket-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/askginadotai/workflows) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, SQL, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe workflow definitions, run artifacts, evaluation records, and rollback paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
