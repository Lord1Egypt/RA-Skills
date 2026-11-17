## Description:

AndonQ helps agents query Tencent Cloud support tickets, organization tickets and stories, ticket activity, and Tencent Cloud SmartQA product support answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llm-pm](https://clawhub.ai/user/llm-pm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support staff use this skill to retrieve Tencent Cloud ticket information, inspect organization support records, and ask Tencent Cloud product support questions from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query sensitive Tencent Cloud support ticket data using user-provided credentials.

Mitigation: Use a least-privileged, revocable Tencent Cloud sub-account key and prefer session-only or secret-manager injection over plaintext shell-profile storage.

Risk: Organization ticket mode can expand the data scope to member tickets, UINs, descriptions, and operation records.

Mitigation: Use organization-wide queries only when the user explicitly requests them, and disclose the expanded scope before presenting results.

Risk: SmartQA sends questions and multi-turn context to Tencent Cloud services for processing.

Mitigation: Warn users before first SmartQA use and avoid sending secrets, internal hostnames, customer data, or other sensitive content.

Risk: Verbose and dry-run modes can expose request payloads, response data, or signed request metadata in terminal output.

Mitigation: Avoid verbose or dry-run output in shared terminals, logs, recordings, or transcripts.

## Reference(s):

- [GetMCTicketList](artifact/references/GetMCTicketList.md)
- [GetMCTicketById](artifact/references/GetMCTicketById.md)
- [SmartQA](artifact/references/SmartQA.md)
- [DescribeOrganizationTickets](artifact/references/DescribeOrganizationTickets.md)
- [DescribeTicket](artifact/references/DescribeTicket.md)
- [DescribeTicketOperation](artifact/references/DescribeTicketOperation.md)
- [DescribeOrganizationStories](artifact/references/DescribeOrganizationStories.md)
- [DescribeOrganizationStory](artifact/references/DescribeOrganizationStory.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON API results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ticket APIs require Tencent Cloud AK/SK environment variables; SmartQA can run without AK/SK.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
