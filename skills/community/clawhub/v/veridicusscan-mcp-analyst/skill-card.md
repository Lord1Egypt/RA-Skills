## Description:

Use when the user wants to inspect a prompt, local file, or public HTTPS URL with VeridicusScan through its MCP bridge, triage prompt-injection or hidden-instruction findings, explain coverage or redaction limits, export reports, or run runtime-defense workflows such as memory ingestion, selective disclosure, tool scoping, plan guarding, and action gating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabaaziz991-hash](https://clawhub.ai/user/sabaaziz991-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Security, IT, recruiting, compliance, and developer teams use this skill to route selected URLs, local files, prompts, and agent-runtime workflows through the VeridicusScan MCP bridge and summarize scanner risk, coverage, redaction limits, and relevant findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits user-selected URLs, files, prompts, and runtime-defense workflow data to a VeridicusScan MCP bridge.

Mitigation: Confirm the exact URL, file, prompt, or workflow before scanning and use this skill only when the VeridicusScan MCP bridge is intentionally connected.

Risk: Runtime-defense methods such as memory ingestion, tool scoping, plan guarding, and action gating can influence later agent decisions.

Mitigation: Run these workflows deliberately, preserve authoritative tool-scope values returned by the bridge, and avoid inventing or forging scope values.

Risk: Scan reports may be partial or redacted, including sanitized-only file contexts.

Mitigation: State coverage limits and redaction status explicitly, and prefer safe_context for downstream use when VeridicusScan returns sanitized_only.

## Reference(s):

- [MCP methods](references/mcp-methods.md)
- [AI job application screening](https://veridicuscan.app/ai-job-application-screening)
- [Local MCP automation for AI agents](https://veridicuscan.app/mcp-automation)
- [ClawHub skill page](https://clawhub.ai/sabaaziz991-hash/skills/veridicusscan-mcp-analyst)
- [Publisher profile](https://clawhub.ai/user/sabaaziz991-hash)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Concise operational Markdown summaries with method names, risk bands, scores, findings, coverage notes, and redaction notes when applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact MCP error codes, report-export guidance, and sanitized context recommendations when returned by VeridicusScan.]

## Skill Version(s):

0.1.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
