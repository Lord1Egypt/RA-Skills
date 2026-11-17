## Description:

Use a configured Titen MCP server to recall bounded evidence-grounded context, record verified durable signals, submit feedback, and coordinate checkpoints, leases, or handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramaaditya49](https://clawhub.ai/user/ramaaditya49)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent retrieve bounded Titen memory, write verified durable signals, submit feedback, and coordinate checkpoints or handoffs within an authorized subject and project scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause durable memory writes that influence future agent sessions.

Mitigation: Use only explicitly authorized subject_id and project_id values, choose narrow visibility and truthful trust levels, and review durable writes before treating them as persistent memory.

Risk: Recalled memory may be stale, conflicting, or untrusted.

Mitigation: Treat Titen memory as reference data, verify operational facts against current source or runtime evidence, and preserve uncertainty when recalled facts conflict.

Risk: Sensitive data could be captured if memory writes are used too broadly.

Mitigation: Do not store credentials, raw private conversations, chain of thought, prompts, embeddings, or routine command output.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown instructions with MCP tool names and operational constraints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Titen MCP memory service and authorized subject_id and optional project_id.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
