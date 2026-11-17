## Description:

Spec-driven development framework for OpenClaw. Propose features, generate specs, spawn coding agents, validate implementations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chanbistec](https://clawhub.ai/user/chanbistec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use SpecClaw to manage spec-driven software changes from proposal through planning, agent execution, verification, and archive. It is suited for repositories where agents may create structured change files, run configured checks, and coordinate implementation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify repositories, run shell commands, spawn agents, and perform git operations.

Mitigation: Use it first in a disposable or well-backed-up repository and review generated specs, tasks, and diffs before accepting changes.

Risk: Configured test, lint, and build commands may execute project-defined shell commands during build or verification.

Mitigation: Review .specclaw/config.yaml before build or verify, and avoid running the skill on untrusted projects.

Risk: Optional GitHub sync can create or update issues using GitHub credentials.

Mitigation: Keep GitHub sync disabled unless needed, prefer authenticated gh CLI over stored tokens, and avoid storing personal access tokens in config.yaml.

Risk: Autonomous mode can continue proposal, planning, build, and verification workflows with limited human intervention.

Mitigation: Keep automation.auto_mode disabled unless the repository, configuration, and planned task scope have been reviewed.

## Reference(s):

- [Agent Prompt Templates](references/agent-prompts.md)
- [Build Engine Architecture & Reference](references/build-engine.md)
- [Workflow Examples](references/workflow-examples.md)
- [SpecClaw ClawHub Release](https://clawhub.ai/chanbistec/skills/specclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated project files, JSON script output, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write .specclaw project files, update task/status records, spawn implementation or verification agents, and run configured repository checks.]

## Skill Version(s):

0.6.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
