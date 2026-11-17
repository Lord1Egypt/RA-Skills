## Description:

SoulFlow is a general-purpose AI workflow framework for OpenClaw that lets agents run custom multi-step workflows for development, operations, research, content, and automation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xtommythomas-dev](https://clawhub.ai/user/0xtommythomas-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use SoulFlow to define and run isolated multi-step OpenClaw workflows for code audits, bug fixes, feature work, deployments, content pipelines, research, and other automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a persistent worker agent with broad read, write, edit, exec, and browser access.

Mitigation: Install only in sandboxed or non-production OpenClaw environments and review the worker permissions before running workflows.

Risk: The worker can inherit existing GitHub, cloud, or other service credentials from configured agents.

Mitigation: Limit inherited credentials to services the workflow is intended to use, or run with isolated credentials.

Risk: Workflow JSON can cause file edits, command execution, deployments, and external service actions.

Mitigation: Review every workflow before execution, avoid untrusted workflow JSON, and back up important files before running modifying workflows.

Risk: Workflow prompts and results are retained locally as run state.

Mitigation: Avoid unnecessary sensitive inputs and monitor or remove local run records according to the deployment policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xtommythomas-dev/skills/soulflow)
- [ClawHub publisher profile](https://clawhub.ai/user/0xtommythomas-dev)
- [Artifact homepage](https://github.com/0xtommythomas-dev/soulflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown/text instructions, shell commands, JSON workflow files, and code or configuration changes produced by worker agent sessions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow outputs can include run state JSON and files modified by the worker according to selected workflow steps.]

## Skill Version(s):

1.1.2 (source: server release evidence; artifact package.json and changelog show 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
