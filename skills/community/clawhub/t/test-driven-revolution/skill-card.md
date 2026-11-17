## Description:

Test-Driven Revolution implements an AI-driven iterative code evolution system with automated coding, testing, auditing, and controlled task workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn explicit TDR requests into planned, reviewed, executed, and audited coding tasks for complex feature work, refactors, documentation updates, and bug fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run model- or review-provided shell commands on a recurring schedule without a real sandbox.

Mitigation: Do not enable cron jobs or heartbeat execution in workspaces with secrets or valuable files until the executor is replaced with a real sandbox.

Risk: Generated commands and task paths may affect workspace files if inputs are not tightly controlled.

Mitigation: Strictly validate task IDs and paths, schema-check review inputs, and require approval or a safe allowlist for generated commands.

Risk: Review inputs can steer execution if they are unauthenticated or untrusted.

Mitigation: Authenticate review sources and inspect each generated instruction before applying it to a task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/test-driven-revolution)
- [Skill documentation](artifact/SKILL.md)
- [Quick start](artifact/README.md)
- [Model and role configuration](artifact/config/models.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON task and review files, code changes, shell commands, and JSONL event logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task workflows may update workspace files, task JSON, locks, and append-only event logs.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
