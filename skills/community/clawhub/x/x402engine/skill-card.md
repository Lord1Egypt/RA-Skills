## Description:

Pay-per-call API gateway skill that calls paid APIs for LLMs, image and video generation, travel, crypto, web search, code execution, audio, storage, and wallet data via x402 micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentc22](https://clawhub.ai/user/agentc22)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to route natural-language requests to paid x402 API services while signing micropayments from a configured wallet. It is suited to service access workflows where the agent must present results with payment cost and respect configured spend policy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend real wallet funds through x402 payments.

Mitigation: Use a dedicated wallet with minimal funds and require the agent to show cost and destination before any paid call.

Risk: Spend protections may be weak if no policy file is configured.

Mitigation: Configure X402_POLICY_PATH with strict per-transaction caps, daily caps, and recipient allowlists before enabling paid access.

Risk: The discovery catalog controls available services and payment recipients.

Mitigation: Verify the discovery endpoint and catalog recipients, or use a trusted self-hosted catalog through X402_DISCOVERY_URL.

Risk: Disabling autopreflight can bypass local policy checks before signing payments.

Mitigation: Keep X402_AUTOPREFLIGHT enabled unless a separate reviewed control provides equivalent preflight enforcement.

## Reference(s):

- [X402engine homepage](https://x402engine.app)
- [X402engine service catalog](https://x402engine.app/.well-known/x402.json)
- [ClawHub skill page](https://clawhub.ai/agentc22/skills/x402engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured JSON returned from paid API calls, with natural-language summaries and cost disclosure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute paid network requests through x402 and return service metadata including service id, name, and price.]

## Skill Version(s):

1.3.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
