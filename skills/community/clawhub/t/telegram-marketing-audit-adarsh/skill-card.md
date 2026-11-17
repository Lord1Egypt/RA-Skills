## Description:

Handles the Telegram /marketing_audit command by running a marketing audit on an Instagram handle or website domain and returning the report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshvmore](https://clawhub.ai/user/adarshvmore)

### License/Terms of Use:


## Use Case:

Telegram bot operators and marketing teams use this skill to invoke a marketing audit from Telegram using an Instagram handle, website domain, or both, then receive a Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw downstream error messages may be returned to Telegram users.

Mitigation: Return a generic failure message in chat and keep detailed exception information in private logs.

Risk: The Telegram command could be invoked by unintended users if chat or user permissions are too broad.

Mitigation: Confirm who can invoke the command before installation and restrict access to authorized chats or users.

Risk: Collector credentials may be over-provisioned for the audit being run.

Mitigation: Configure only the downstream collector API keys actually needed for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adarshvmore/skills/telegram-marketing-audit-adarsh)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Telegram replies containing status text and a Markdown audit report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured marketing-orchestrator skill and the collector API keys needed for the requested audit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
