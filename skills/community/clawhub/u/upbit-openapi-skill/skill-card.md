## Description:

Operate Upbit public exchange market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover and run read-only Upbit public market-data operations through UXC, including market discovery, ticker reads, minute candles, and order book snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the wrong Upbit regional host or market code can return irrelevant or failed market-data reads.

Mitigation: Choose the regional host first and confirm quote-first market codes such as SGD-BTC or USDT-BTC before execution.

Risk: Extending the skill to private account or order APIs would introduce credential handling and request-specific JWT signing risk.

Mitigation: Keep this version limited to public read-only endpoints unless a separately reviewed Upbit signer flow is provided.

Risk: The workflow links a local command to a selected Upbit API host and a GitHub-hosted OpenAPI schema URL.

Mitigation: Review the host and schema URL before installing or running the linked command.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/upbit-public.openapi.json)
- [Official Upbit Open API overview](https://global-docs.upbit.com/reference/api-overview)
- [Curated schema URL](https://raw.githubusercontent.com/holon-run/uxc/main/skills/upbit-openapi-skill/references/upbit-public.openapi.json)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/upbit-openapi-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and OpenAPI operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public market-data workflows; no credentials are required for included endpoints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
