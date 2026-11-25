## Description:

Send a text (SMS) from the user's own Android phone and number with SMSTunnel, check whether it went out, see which phones are online, and read replies. Use when the user asks to text someone, send an SMS or a sign-in code, check a text's status, or see who replied. Needs an SMSTunnel account, the SMSTunnel app on an Android phone, and an API key in the SMSTUNNEL_API_KEY environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[narcisbodea](https://clawhub.ai/user/narcisbodea)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI agent can send one-to-one SMS messages from their linked Android phone, check sending status, view available phones and usage, and read received texts when they have enabled access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A text sent to the wrong person or without clear approval can affect a real recipient; an uncertain result may mean the text already went out.

Mitigation: Show the recipient and exact message and get approval before sending; check the message status after errors or timeouts and do not resend without the user's decision.

Risk: The SMSTUNNEL_API_KEY authorizes access to messaging functions and may also permit reading received texts when enabled.

Mitigation: Keep the key in the host's environment or secret store, never expose it in chat or logs, and enable inbox access only when needed.

## Reference(s):

- [SMSTunnel MCP integration](https://smstunnel.io/integrations/mcp/)
- [REST API instructions](references/rest-api.md)
- [Setup instructions](references/setup.md)

## Skill Output:

**Output Type(s):** [SMS messages, Status and reply summaries, Configuration guidance]

**Output Format:** [SMS messages and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One recipient per send; status reports distinguish handed-off messages from confirmed delivery, which SMSTunnel cannot verify.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
