## Description: <br>
AI Chief of Staff for solo businesses covering inbox triage, task prioritization, revenue tracking, decision journals, opportunity scoring, and weekly reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Clawdssen](https://clawhub.ai/user/Clawdssen) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
Solopreneurs and solo business operators use this skill to configure an agent as a lightweight chief of staff for inbox triage, task prioritization, revenue and expense tracking, opportunity screening, decision logging, and weekly business reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read business files and optional email or calendar data containing sensitive personal, client, financial, or credential information. <br>
Mitigation: Use read-only and least-privilege access where possible, and keep secrets, credentials, and unnecessary historical data out of tracked business files. <br>
Risk: Recurring heartbeat or cron reviews can create ongoing automated access to business context. <br>
Mitigation: Enable scheduled reviews only after deciding they belong in startup files, and periodically audit recurring tasks. <br>
Risk: Business, revenue, and opportunity guidance can be incomplete or misleading if source data is stale or unverified. <br>
Mitigation: Review generated dashboards and recommendations before acting, and independently verify revenue, expense, legal, and financial data. <br>


## Reference(s): <br>
- [Solopreneur Assistant on ClawHub](https://clawhub.ai/Clawdssen/solopreneur-assistant) <br>
- [Publisher profile: Clawdssen](https://clawhub.ai/user/Clawdssen) <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>
- [The Agent Ledger](https://www.theagentledger.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions, templates, and review formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to use business dashboard, decision journal, memory notes, and optional email or calendar context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
