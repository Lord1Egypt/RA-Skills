## Description:

Proxyllm Account helps an agent sign up for ProxyLLM, handle checkout handoff, provision routing keys, wire provider lanes, and configure OpenAI-compatible gateway access with budgets and logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericslab](https://clawhub.ai/user/ericslab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and configure a ProxyLLM gateway account, then route agents through metered keys, fallback lanes, and an OpenAI-compatible base URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and configure a paid external LLM gateway account.

Mitigation: Require explicit operator confirmation before signup, OTP use, checkout handoff, routing-key creation, provider-lane wiring, or Codex subscription connection.

Risk: The account token and routing keys provide powerful access to account management and model routing.

Mitigation: Treat `sk_` and `pllm_` values as secrets, store them in a secret manager, revoke unused keys, and set budgets on routing keys before sharing them with sub-agents.

Risk: The optional MCP path uses an unpinned `npx -y` package execution.

Mitigation: Pin and review the package version or run it in a constrained sandbox before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericslab/skills/proxyllm-account)
- [ProxyLLM](https://proxyllm.ai)
- [ProxyLLM Agent Auth Manifest](https://proxyllm.ai/auth.md)
- [ProxyLLM OpenAPI Specification](https://proxyllm.ai/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands and environment variable settings; secrets are returned once by the external service and should be stored securely.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-07-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
