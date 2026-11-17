## Description:

SuperDev is a full-stack development skill suite for coordinating requirements analysis, architecture guidance, test-driven implementation, UI/UX review, supply-chain security checks, persistent memory, and workflow reflection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weedfire](https://clawhub.ai/user/weedfire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill suite to run a structured agent workflow from requirements through implementation, quality checks, security review, and memory-backed follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on development workflows may read and write persistent memory across tasks.

Mitigation: Review the configured memory path, scope or disable persistence when possible, and require confirmation before memory writes.

Risk: Security gate workflows may run external scanner tools, including npx-based tooling.

Mitigation: Pin or sandbox external scanner tools before use and require confirmation before scanner execution.

Risk: The server security verdict is suspicious because the suite combines broad auto-activation, global memory, and unpinned scanner behavior.

Mitigation: Review and scan the skill before deployment, with special attention to memory persistence and scanner invocation behavior.

## Reference(s):

- [SuperDev ClawHub skill page](https://clawhub.ai/weedfire/skills/super-dev-skills)
- [ClawHub publisher profile](https://clawhub.ai/user/weedfire)
- [agent-skills reference](https://github.com/addyosmani/agent-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request persistent memory writes and security scanner execution depending on host configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
