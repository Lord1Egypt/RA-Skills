## Description:

Manage deal pipeline, search on-market deals, track brokers, run SBA loan calculations, manage tasks, and review CIM analyses in Searcher OS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshthacker](https://clawhub.ai/user/joshthacker)

### License/Terms of Use:

MIT-0

## Use Case:

External Searcher OS users use this skill to manage M&A deal activity, including pipeline review, deal search, broker tracking, SBA loan calculations, task updates, and CIM analysis through the Searcher OS API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sensitive deal, email, and CIM information from Searcher OS.

Mitigation: Install only for users who are authorized to access that business data and review requested outputs before sharing them.

Risk: Some tools can update deal records, hide feed items, or advance workflow state without a separate confirmation step.

Mitigation: Review Searcher OS auto-approval settings and require explicit user approval for material record changes when operating the agent.

## Reference(s):

- [Searcher OS homepage](https://searcheros.ai)
- [Searcher OS ClawHub skill page](https://clawhub.ai/joshthacker/skills/searcher-os)
- [Searcher OS API base endpoint](https://searcheros.ai/api/agent)
- [Searcher OS tool discovery endpoint](https://searcheros.ai/api/agent/tools)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON API request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEARCHER_OS_API_KEY and a Searcher OS account]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
