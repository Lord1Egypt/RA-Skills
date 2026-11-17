## Description:

Live real-world data with no API key. 970+ pay-per-call x402 endpoints for finance, crypto, macro, travel, sports, health, legal. Free discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pulsenetwork](https://clawhub.ai/user/pulsenetwork)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to discover and, with explicit consent, access paid real-world data endpoints for current finance, crypto, macro, travel, sports, health, legal, and related tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls can spend wallet funds when payment tooling is configured.

Mitigation: Quote the endpoint and exact catalog or 402 challenge price before the first paid call, obtain explicit user consent, and enforce low per-call and daily spend caps.

Risk: The recommended MCP package handles wallet funds and private-key material.

Mitigation: Use a pinned and reviewed @pulsenetwork/mcp version, run it with least privilege, prefer a dedicated low-balance wallet, and avoid supplying a general-purpose private key.

Risk: External data responses may carry attribution and terms requirements.

Mitigation: Preserve attribution and terms links from responses when republishing or summarizing data.

## Reference(s):

- [PulseNetwork homepage](https://pulse.theaslangroupllc.com)
- [Agent index](https://pulse.theaslangroupllc.com/llms.txt)
- [Machine catalog](https://pulse.theaslangroupllc.com/.well-known/agent.json)
- [ClawHub skill listing](https://clawhub.ai/pulsenetwork/skills/pulsenetwork-paid-data)
- [PulseNetwork publisher profile](https://clawhub.ai/user/pulsenetwork)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with URLs, prices, configuration snippets, and structured JSON API responses when calls are made]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid calls require explicit user consent, exact price disclosure, and configured payment rails; free discovery remains available without a wallet.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
