## Description: <br>
Tencent Cloud AndonQ helps agents query support tickets, inspect ticket details and activity, manage organization tickets and request records, and ask Tencent Cloud product questions through SmartQA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llm-pm](https://clawhub.ai/user/llm-pm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support teams use this skill to retrieve Tencent Cloud support ticket data, review organization-level ticket and request records, and ask Tencent Cloud product support questions without leaving the agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require persistent Tencent Cloud AK/SK credentials for ticket operations. <br>
Mitigation: Use the least-privileged Tencent Cloud credentials available, prefer safer secret storage over long-lived shell profile entries, and rotate or revoke credentials that may have been exposed. <br>
Risk: Ticket details, organization lists, internal notes, attachment URLs, and SmartQA prompts may contain confidential support data. <br>
Mitigation: Treat outputs and prompts as confidential, avoid sharing them in public channels, and redact sensitive values before copying results into logs or other systems. <br>
Risk: Verbose and dry-run modes can reveal request payloads or headers in shared terminals and logs. <br>
Mitigation: Avoid verbose or dry-run output in shared environments, and review terminal transcripts or CI logs for sensitive data before retaining or sharing them. <br>


## Reference(s): <br>
- [GetMCTicketList](references/GetMCTicketList.md) <br>
- [GetMCTicketById](references/GetMCTicketById.md) <br>
- [SmartQA](references/SmartQA.md) <br>
- [DescribeOrganizationTickets](references/DescribeOrganizationTickets.md) <br>
- [DescribeTicket](references/DescribeTicket.md) <br>
- [DescribeTicketOperation](references/DescribeTicketOperation.md) <br>
- [DescribeOrganizationStories](references/DescribeOrganizationStories.md) <br>
- [DescribeOrganizationStory](references/DescribeOrganizationStory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ticket tables, ticket details, activity records, SmartQA answers, session identifiers for follow-up questions, and request IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
