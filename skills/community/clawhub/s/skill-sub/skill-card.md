## Description: <br>
skill-sub helps agents plan, manage, validate, and persist reusable multi-skill orchestration chains, including sequencing, branching, loops, scheduling checks, and gap-handling steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to turn repeatable multi-skill workflows into reusable chain definitions, execution plans, validation reports, and maintenance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist, rewrite, delete, and schedule reusable multi-skill workflows. <br>
Mitigation: Review saved chain contents, schedules, and planned file changes before use; require explicit confirmation before destructive deletion or schedule registration. <br>
Risk: Adhesion steps may use scripts or tools to fill workflow gaps. <br>
Mitigation: Require explicit confirmation before any adhesion step executes a script or tool, and inspect generated scripts or outputs before reuse. <br>
Risk: Memory and log references may expose additional local context to chain planning. <br>
Mitigation: Keep memory and log reference disabled unless the user accepts that context being read for workflow construction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/skill-sub) <br>
- [Workflow guide](references/workflow.md) <br>
- [Chain schema](references/chain_schema.md) <br>
- [Permissions and testing](references/permissions.md) <br>
- [Command reference](references/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-oriented guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include chain definitions, execution plans, validation findings, CLI commands, and configuration guidance.] <br>

## Skill Version(s): <br>
1.29.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
