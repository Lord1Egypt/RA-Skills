## Description:

Validated CAG decision memory for OpenClaw tools, agents, and long-running project sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guideboardlabs](https://clawhub.ai/user/guideboardlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve, capture, validate, resolve, compress, import, and export durable project decisions during ongoing software work. It is intended for repositories, agent workflows, plugins, MCP servers, and multi-step implementations where prior decisions can affect later work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validated memories can make project decisions durable across sessions.

Mitigation: Validate a memory only after explicit user approval, a passing test tied to the decision, a PR or commit reference, or a clear request to remember it.

Risk: Retrieved memories may be stale, incomplete, or in tension with the current codebase.

Mitigation: Treat retrieved memories as constraints to check, read the current code before acting, and use the contradiction workflow when policy or implementation decisions change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guideboardlabs/skills/uncagd)

## Skill Output:

**Output Type(s):** [guidance, API Calls, markdown]

**Output Format:** [Markdown guidance with tool-call recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce portable memory handoff documents through memory export behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
