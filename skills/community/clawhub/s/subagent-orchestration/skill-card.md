## Description:

Orchestrates OpenClaw subagents across worker, researcher, and council patterns with guidance for spawning, sandbox constraints, timeouts, configuration, and common failure recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahajahmed010](https://clawhub.ai/user/wahajahmed010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate local work, web research, and multi-model review to OpenClaw subagents while avoiding common sandbox, timeout, and context-passing failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated subagents may run local file or script operations with broad task context.

Mitigation: Review delegated tasks before execution and limit file or script work to trusted workspace paths.

Risk: Selected task context may be sent to web tools or cloud-hosted model subagents.

Mitigation: Do not include secrets, credentials, private keys, customer data, regulated data, or proprietary material unless that exposure has been explicitly approved.

Risk: The companion council skill may change independently.

Mitigation: Verify the companion council skill before use and prefer pinned versions where available.

## Reference(s):

- [Subagent Tool Access Reference](references/tool-access.md)
- [Council of LLMs companion skill](https://github.com/wahajahmed010/council-of-llms)
- [ClawHub skill page](https://clawhub.ai/wahajahmed010/skills/subagent-orchestration)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes subagent spawning examples, timeout recommendations, tool-access constraints, and failure-mode fixes.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
