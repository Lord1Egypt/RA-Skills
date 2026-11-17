## Description:

Guide users to choose and purchase Taoflow VPN plans safely and efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taoflownetwork](https://clawhub.ai/user/taoflownetwork)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare Taoflow VPN purchase options, follow safe checkout steps, and handle onboarding or purchase troubleshooting with verified details only. Developers can use its API mode guidance for programmatic order creation, status checks, and WireGuard configuration retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent through VPN order creation and configuration retrieval.

Mitigation: Confirm plan details, payment network requirements, refund terms, and support channels on the official Taoflow site before purchase.

Risk: Access tokens, recovery keys, payment addresses, and order data may be sensitive.

Mitigation: Mask secrets in chat, avoid sharing full tokens or recovery keys unless necessary, and require explicit user confirmation before payment-related actions.

## Reference(s):

- [Taoflow VPN Official Site](https://taoflow.network)
- [Taoflow API Guide](https://taoflow.network/api.html)
- [Taoflow OpenAPI Specification](https://taoflow.network/openapi.json)
- [Taoflow Plugin Manifest](https://taoflow.network/.well-known/ai-plugin.json)
- [ClawHub Skill Page](https://clawhub.ai/taoflownetwork/skills/taoflow-buy-vpn)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Configuration instructions]

**Output Format:** [Markdown guidance with optional API request and WireGuard setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should avoid fabricating prices, policies, payment status, access tokens, or recovery keys.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
