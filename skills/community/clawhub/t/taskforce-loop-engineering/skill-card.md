## Description:

Durable explicit task/project loops with verification, revisions, live progress, and governed completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ambitioncn](https://clawhub.ai/user/ambitioncn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a user explicitly requests a durable task or project loop. It guides queue setup, progress and verification checks, revisions, and human approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unreviewed or mismatched CLI release can execute package code or provide different behavior than the skill describes.

Mitigation: Review and pin the CLI release, then confirm the installed package and integration provide the capabilities you intend to use.

Risk: Persistent workers can use configured permissions and model budget, and a remotely reachable dashboard can expose task information.

Mitigation: Review the installation plan, worker permissions and budget; keep the dashboard local unless Tailnet access is intended and restricted.

Risk: The security review covers the bundled instructions, not the separate runtime or its claimed enforcement.

Mitigation: Assess the deployed runtime and integration independently before relying on their security controls.

## Reference(s):

- [Context budget](references/context-budget.md)
- [Frozen input verification](references/frozen-input-verification.md)
- [npm package and CLI commands](references/npm-package.md)
- [OpenClaw diagnostics](references/openclaw-diagnostics.md)
- [Scope and task acceptance](references/scope-task-acceptance.md)
- [Project repository (referenced by the skill)](https://github.com/ambitioncn/taskforce-loop-engineering)
- [npm package](https://www.npmjs.com/package/taskforce-loop-engineering)
- [ClawHub skill page](https://clawhub.ai/ambitioncn/skills/taskforce-loop-engineering)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for explicitly requested task and project loops; commands and deployment steps depend on the installed CLI and integration.]

## Skill Version(s):

0.16.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
