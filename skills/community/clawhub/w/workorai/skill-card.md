## Description: <br>
Use for WorkorAI talent marketplace requests: the skill routes candidate job-search and employer hiring intents to WorkorAI MCP workflows, including job discovery, applications, candidate search, evidence-backed candidate review, invitations, applicant review, and MCP onboarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m14mgn-hash](https://clawhub.ai/user/m14mgn-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External candidates use this skill to search WorkorAI jobs, inspect matches, apply, manage saved jobs, and respond to invitations. Employers use it to manage WorkorAI hiring workflows, search and compare candidates, review interview evidence, invite candidates, and triage applicants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved WorkorAI candidate or employer keys may authorize live job-application or hiring actions. <br>
Mitigation: Use the skill only for WorkorAI-specific workflows, keep keys redacted, and confirm every application, invitation, publication, deletion, or review-status change before it happens. <br>
Risk: The best-effort credential save path can fall back to a local 0600 file copy if OS credential storage is unavailable. <br>
Mitigation: Ask for explicit user consent before saving keys, prefer OS credential storage, and use the shared-file fallback only when the user explicitly chooses that mode. <br>
Risk: Broad activation may route generic job-search or hiring requests into WorkorAI workflows. <br>
Mitigation: Proceed only when the user wants WorkorAI-specific job or hiring actions, and avoid using the skill for generic career advice, resume writing, interview coaching, or non-WorkorAI searches. <br>


## Reference(s): <br>
- [WorkorAI skill page](https://clawhub.ai/m14mgn-hash/skills/workorai) <br>
- [Auth Flow](references/auth-flow.md) <br>
- [Candidate Catalog](references/candidate-catalog.md) <br>
- [Candidate Recipes](references/candidate-recipes.md) <br>
- [Candidate Troubleshooting](references/candidate-troubleshooting.md) <br>
- [Employer Catalog](references/employer-catalog.md) <br>
- [Employer Recipes](references/employer-recipes.md) <br>
- [Employer Troubleshooting](references/employer-troubleshooting.md) <br>
- [General Troubleshooting](references/troubleshooting.md) <br>
- [Candidate login](https://workorai.com/candidate/login) <br>
- [Candidate MCP key page](https://workorai.com/candidate/home?tab=mcp) <br>
- [Employer dashboard](https://workorai.com/employer/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with MCP tool-call plans and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses role-scoped WorkorAI candidate or employer credentials and should redact key values in user-visible output.] <br>

## Skill Version(s): <br>
0.4.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
