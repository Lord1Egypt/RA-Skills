## Description: <br>
Search candidates, manage jobs, view pipelines, track billing and team performance in Recruitly CRM via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willgary](https://clawhub.ai/user/willgary) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Recruiting teams and agents use this skill to query Recruitly CRM records, find candidates, inspect jobs and pipelines, and summarize team or billing activity through an MCP connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may retrieve candidate, client, company, job, billing, or team performance data visible to the connected Recruitly account. <br>
Mitigation: Use a least-privileged Recruitly account or token and avoid bringing sensitive CRM data into conversations unless organizational policy permits it. <br>
Risk: The required RECRUITLY_TOKEN could be exposed through shared logs, chat transcripts, or pasted configuration. <br>
Mitigation: Keep RECRUITLY_TOKEN out of shared logs and chats, and provide it through the local environment rather than hard-coding it in public configuration. <br>
Risk: Tenant-specific status and type labels may vary by account and language, leading to incorrect filters. <br>
Mitigation: Call list_options before filtering by status or type so the agent uses account-specific option values. <br>


## Reference(s): <br>
- [Recruitly](https://recruitly.io) <br>
- [Recruitly MCP Server](https://recruitly.io/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/willgary/recruitly-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls, Text, Markdown] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples; agent responses are text or markdown summaries from Recruitly CRM data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and RECRUITLY_TOKEN; search results are capped at 50 per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
