## Description:

Deterministic decision-ranking API with HTTP 402 payments and outcome credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zapkid](https://clawhub.ai/user/zapkid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to request deterministic LLM recommendations under cost, quality, workload, and fallback constraints. It also supports reporting execution outcomes to receive credits for later paid requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model-selection goals, constraints, workload estimates, and outcome data are sent to an external Which-LLM API.

Mitigation: Use the skill only when sharing this data with the external service is acceptable for the task and organization.

Risk: Paid requests may require wallet-backed USDC payment after an HTTP 402 response.

Mitigation: Require explicit user approval for every transfer and verify the chain, recipient, exact amount, and payment reference before sending funds.

Risk: Incorrect payment proof headers or mismatched transaction details can cause payment failure.

Mitigation: Match retry headers to the confirmed transaction and use the API troubleshooting guidance for PAYMENT_INVALID responses.

## Reference(s):

- [Which-LLM homepage](https://which-llm.com)
- [Which-LLM API base](https://api.which-llm.com)
- [Payment address documentation](https://which-llm.com/docs/payment-addresses)
- [Well-known agent metadata](https://which-llm.com/.well-known/agent.json)
- [Payment address text record](https://which-llm.com/.well-known/payment-address.txt)
- [ClawHub skill page](https://clawhub.ai/zapkid/skills/which-llm)
- [Publisher profile](https://clawhub.ai/user/zapkid)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides outbound HTTPS JSON calls to Which-LLM endpoints and handling of payment proof headers for paid requests.]

## Skill Version(s):

1.0.18 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
