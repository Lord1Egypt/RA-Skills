## Description:

Creates Shieldz crypto payment links or tip jars for a user-confirmed wallet and checks payment status through Shieldz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[denizyanbollu](https://clawhub.ai/user/denizyanbollu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create fixed-amount crypto payment links or reusable tip jars for a wallet they explicitly provide and confirm. Agents can also check received payment totals when the user supplies a Shieldz manage token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local MCP path downloads and runs a pinned npm package.

Mitigation: Prefer the disclosed REST or remote MCP flow; use the local npx path only after review and in a restricted environment.

Risk: External Shieldz calls transmit wallet, chain, asset, amount, memo or title, optional email, and status manage tokens to Shieldz.

Mitigation: Confirm the user's intent and exact fields before every external call, disclose what will be sent, and omit email unless the user explicitly opts in.

Risk: Manage URLs and manage tokens can expose payment totals and settings.

Mitigation: Treat manage URLs and manage tokens as private credentials; do not publish, log, or share them, and only use tokens supplied by the user.

Risk: Ambiguous payment requests could lead to unwanted payment link creation.

Mitigation: Ask for clarification and require explicit confirmation of wallet, chain, asset, amount or suggested amounts, memo or title, and email choice before creation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/denizyanbollu/skills/shieldz)
- [Shieldz REST API](https://shieldz.cash/api/v1/...)
- [Shieldz MCP Endpoint](https://shieldz.cash/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Shieldz payment URLs, status summaries, and handling guidance for private manage URLs or manage tokens.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
