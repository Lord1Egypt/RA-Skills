## Description:

Operate WhatsApp Business Platform Cloud API through UXC with a curated OpenAPI schema, bearer-token auth, and message/profile guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure bearer-token access, inspect WhatsApp Cloud API operations, read phone number and business profile data, and perform guarded outbound message or profile update requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can pull a mutable remote OpenAPI schema that changes what the authenticated CLI exposes.

Mitigation: Prefer the bundled references/whatsapp-cloud.openapi.json file or an immutable reviewed commit when linking UXC.

Risk: The WhatsApp access token can authorize sensitive account operations.

Mitigation: Store the token in WHATSAPP_CLOUD_ACCESS_TOKEN, protect the environment secret, and bind it only to the versioned Graph API path.

Risk: Message sends and business profile updates can affect external recipients or public account information.

Mitigation: Confirm each outbound message send or business profile update before execution and send only the fields intended to change.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/whatsapp-cloud.openapi.json)
- [WhatsApp Cloud API docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Graph API access tokens](https://developers.facebook.com/docs/graph-api/overview/access-tokens/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is scoped to WhatsApp Cloud API request/response operations through UXC and a curated OpenAPI schema.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
