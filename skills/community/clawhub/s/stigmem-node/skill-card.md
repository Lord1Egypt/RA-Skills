## Description:

Persistent federated memory for OpenClaw agents -- boot handshake, handoff, decision, and escalation surfaces backed by a Stigmem node.

This skill is for research and development only.

## Publisher:

[offbyonce](https://clawhub.ai/user/offbyonce)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect OpenClaw agents to a Stigmem node for persistent memory, session handoffs, decision records, and escalation facts during evaluation or controlled integration work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved memory from a compromised or misconfigured Stigmem node can influence agent behavior if treated as instructions.

Mitigation: Use a private, access-controlled node, append retrieved context after hardcoded system instructions, and inspect structured facts instead of injecting full summaries in high-stakes workflows.

Risk: Facts written to shared or federated memory can persist across future agents and propagate beyond the intended deployment.

Mitigation: Use least-privilege per-agent API keys, unique source entities, local scopes for scratch facts, narrow federation settings, and explicit retraction for incorrect facts.

Risk: Alpha-line dependency updates may change runtime behavior across repeatable evaluations.

Mitigation: Pin the Python dependency and Stigmem node image before evaluation or production-like use, then review release notes and run integration tests before upgrades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/offbyonce/skills/stigmem-node)
- [OpenClaw connector guide](https://docs.stigmem.dev/en/latest/docs/guides/connectors/openclaw)
- [Stigmem project homepage](https://stigmem.dev)
- [Stigmem plugin catalog](https://docs.stigmem.dev/en/latest/docs/plugins)
- [Server-resolved provenance](unavailable)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STIGMEM_URL and STIGMEM_API_KEY; optional environment variables configure source identity and allowed handoff targets.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
