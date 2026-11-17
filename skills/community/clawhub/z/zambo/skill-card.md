## Description:

Gives your agent hands through Zambo, the verifiable work layer for AI, with 153 tools behind one remote MCP endpoint. Use when a task needs real work, memory, or continuity beyond the model's own knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zambodotdev](https://clawhub.ai/user/zambodotdev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use Zambo when an authorized task needs multi-step work, research, code review, saved memory, or handover between agents. The skill guides agents in finding hosted tools, completing the task, and reporting the resulting receipt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task data may be exposed through hosted tool arguments, receipts, or handover links.

Mitigation: Use only task-approved data, keep secrets out of tool arguments, and review receipt and handover contents before sharing.

Risk: Hosted tool actions may have permissions or spending effects beyond the immediate task output.

Mitigation: Review live tool permissions before sensitive actions and authorize spending separately.

Risk: The assessment does not audit the hosted service's implementation or retention controls.

Mitigation: Keep use within the user's authorized data scope and account for service-side handling when choosing what to send.

## Reference(s):

- [Zambo agent documentation](https://zambo.dev/.well-known/llms.txt)
- [Zambo setup options](https://zambo.dev/add)
- [Zambo guide for agents](https://zambo.dev/for-agents/)
- [Receipt verification](https://zambo.dev/verify/)
- [Project repository linked by the skill](https://github.com/zambodotdev/zambo-mcp)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Code, Files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Varies by task; text, Markdown, code, shell commands, configuration, and hosted tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-specific work products may include a verifiable receipt or handover context; review shared contents before distribution.]

## Skill Version(s):

1.2.1 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
