## Description:

Set up and manage RingKit’s AI phone receptionist for a business, from importing its website and routing calls to provisioning a number and reviewing call summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omricohen](https://clawhub.ai/user/omricohen)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and operators can use the skill to configure an AI receptionist, route calls, set up a business phone number or forwarding, and review call activity. It guides the agent through RingKit API operations and leaves payment and sensitive account decisions with the owner.

### Deployment Geography for Use:

Global (US phone number provisioning is described)

## Known Risks and Mitigations:

Risk: The RingKit API key can grant access to business settings and call data, and a new key is shown only once.

Mitigation: Store RINGKIT_API_KEY securely and use read-only access when only reviewing calls.

Risk: Call records include transcripts and recordings, and webhook signatures do not provide confidentiality.

Mitigation: Restrict access to call data and send notifications only to authorized endpoints.

Risk: Number fees and per-minute AI charges can create ongoing costs.

Mitigation: Confirm ongoing charges with the owner before provisioning.

Risk: Releasing a number, revoking a key, or changing live call routing can disrupt the business.

Mitigation: Ask the owner before making these changes.

## Reference(s):

- [RingKit documentation](https://www.ringkit.com/docs)
- [RingKit OpenAPI specification](https://api.ringkit.com/openapi.json)
- [RingKit agent reference](https://api.ringkit.com/llms.txt)
- [RingKit MCP endpoint](https://api.ringkit.com/mcp)

## Skill Output:

**Output Type(s):** [Text guidance, API calls, Shell commands, Configuration instructions, Call summaries and transcripts]

**Output Format:** [Markdown guidance with curl and JSON examples; RingKit returns structured API data and call records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions depend on the business owner’s account, chosen call routing, and RingKit service responses.]

## Skill Version(s):

0.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
