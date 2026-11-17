## Description:

Integrate Trails cross-chain infrastructure using a widget, headless SDK, or direct API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameslawton](https://clawhub.ai/user/jameslawton)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to integrate Trails cross-chain payments, swaps, DeFi funding flows, and destination-chain contract execution into React, Next.js, backend, or non-React applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to inspect API-key locations, which can expose credentials if values are printed or copied.

Mitigation: Confirm only whether required keys exist and reference `TRAILS_API_KEY` or `NEXT_PUBLIC_TRAILS_API_KEY` by name; do not display or log secret values.

Risk: Generated blockchain transaction examples can move funds or execute high-impact DeFi actions.

Mitigation: Require explicit human confirmation before signing or executing transactions, use testnets first, and pin skill and npm package versions.

Risk: Generated backend or DeFi code may lack production controls.

Mitigation: Add authentication, authorization, schema validation, rate limits, recipient/token/chain allowlists, slippage limits, replay protection, and audit logging before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jameslawton/skills/trails)
- [Trails documentation](https://docs.trails.build)
- [Trails Docs MCP](https://docs.trails.build/mcp)
- [Trails API reference](https://docs.trails.build/api)
- [Trails SDK reference](https://docs.trails.build/sdk)
- [Trails overview](docs/TRAILS_OVERVIEW.md)
- [Integration decision tree](docs/INTEGRATION_DECISION_TREE.md)
- [Widget recipes](docs/WIDGET_RECIPES.md)
- [Headless SDK recipes](docs/HEADLESS_SDK_RECIPES.md)
- [API recipes](docs/API_RECIPES.md)
- [Calldata guide](docs/CALLDATA_GUIDE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript, TSX, JSON, environment variable, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API calls and transaction-flow examples; secret values should be referenced by environment variable name only.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
