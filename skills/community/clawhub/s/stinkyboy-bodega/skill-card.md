## Description:

One integration, one wallet relationship. Thousands of callable tools, paid per call in USDC via x402. Charge on success only — errors and verification failures settle nothing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noahmchugh](https://clawhub.ai/user/noahmchugh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to connect an MCP client to a paid marketplace of callable remote tools, request quotes, execute catalog tools, create missing tools, and review spend or receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote service can create and run new tools immediately using real inputs, including paid calls.

Mitigation: Review the requested tool, call quote, inputs, and payment terms before execution; require explicit confirmation for paid or dynamically created calls.

Risk: Wallet, payment, callback, or user-provided data may be sent to the remote service.

Mitigation: Use only data and wallet activity suitable for the service, and avoid internal, secret-bearing, or privileged callback URLs.

Risk: Security evidence marks the release as suspicious because remote tool creation and execution can happen quickly in a paid marketplace.

Mitigation: Review before installing, limit deployment scope, and monitor spend reports and hash-chained receipts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noahmchugh/skills/stinkyboy-bodega)
- [Publisher profile](https://clawhub.ai/user/noahmchugh)
- [Stinkyboy full specification](https://stinkyboy.co/llms-full.txt)
- [Stinkyboy catalog](https://stinkyboy.co/catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and tool-call responses from a remote MCP service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quotes, tool schemas, quality and health details, spend reports, receipts, and remote tool results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
