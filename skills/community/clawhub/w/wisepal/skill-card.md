## Description:

Helps users seek lower US wireless, internet, and TV bills through free WisePal provider negotiations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisepal](https://clawhub.ai/user/wisepal)

### License/Terms of Use:

MIT-0

## Use Case:

US consumers can use an assistant to submit eligible wireless, internet, or TV accounts to WisePal for free bill negotiation, after confirming their account details and consenting to provider calls.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Contact and provider account details are shared with WisePal for negotiation.

Mitigation: Explain the data transfer, review the returned details and terms with the user, and obtain explicit approval before provider calls.

Risk: Private submission credentials could be exposed through chat, logs, or shared storage.

Mitigation: Keep credentials in private durable storage; never pass the private header hook through chat, model tools, or logs.

## Reference(s):

- [WisePal](https://wisepal.com)
- [WisePal hosted MCP](https://my.wisepal.com/mcp)
- [WisePal skill on ClawHub](https://clawhub.ai/wisepal/skills/wisepal)
- [WisePal request schemas](artifact/references/request-schemas.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown with submission details and status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows validated account details and terms for explicit approval; savings are not guaranteed.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
