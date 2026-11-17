## Description:

Vehicle intelligence for AI agents: decode 17-character VINs, retrieve merged US and Canadian recalls, summarize known issues with ODI citations and reliability aggregates, and estimate used-vehicle drive-away costs across US and Canadian jurisdictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcislo](https://clawhub.ai/user/jcislo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to understand Vindex's vehicle-data API, try free sample response shapes, and prepare paid x402 calls for VIN decoding, recalls, known issues, reliability data, purchase costs, and pre-purchase summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send VINs or purchase details to an external paid vehicle-data service.

Mitigation: Submit only VINs and purchase details intended for Vindex, and try the free sample endpoints before paid calls.

Risk: Paid endpoints require x402 wallet/payment handling.

Mitigation: Ensure wallet and payment setup is controlled by the user or deployment owner before enabling paid calls.

Risk: The skill provides informational vehicle data and is not a vehicle-history report or professional purchasing advice.

Mitigation: Treat outputs as supporting information and verify vehicle history, legal, financial, and purchase decisions through appropriate authoritative sources.

## Reference(s):

- [Vindex homepage](https://vindexapi.dev)
- [Vindex API agent documentation](https://api.vindexapi.dev/llms.txt)
- [Vindex OpenAPI specification](https://api.vindexapi.dev/openapi.json)
- [ClawHub skill page](https://clawhub.ai/jcislo/skills/vindex)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with endpoint tables, inline shell commands, and JSON API response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid calls use x402 USDC payments on Base; free sample endpoints expose response shapes before payment.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
