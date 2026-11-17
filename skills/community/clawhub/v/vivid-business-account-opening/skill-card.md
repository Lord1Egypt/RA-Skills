## Description:

Helps users collect confirmed legal-entity details and request a pre-filled Vivid business-account onboarding link from a remote MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanlee000](https://clawhub.ai/user/stanlee000)

### License/Terms of Use:


## Use Case:

External users use this skill to start Vivid business-account onboarding by confirming legal-entity details and receiving a generated onboarding URL. The skill creates only a pre-filled link; identity verification and account opening happen later in Vivid's app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed legal-entity onboarding details are sent to Vivid's remote MCP service to create an onboarding session.

Mitigation: Show the user a confirmation summary before calling build_onboarding_link and ask them to check fields such as country and entity type.

Risk: Users may provide sensitive credentials, bank account numbers, or raw document contents in chat.

Mitigation: Do not request or accept passwords, API keys, bank account numbers, or raw document contents; summarize uploaded documents locally and send only structured fields.

## Reference(s):

- [Vivid MCP homepage](https://github.com/vivid-money/vivid-mcp)
- [Vivid remote MCP endpoint](https://api.prime.vivid.money/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with JSON MCP configuration and a returned onboarding URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before calling the remote MCP tool; raw documents, credentials, and bank account numbers should not be sent.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter version is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
