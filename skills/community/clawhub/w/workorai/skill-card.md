## Description:

WorkorAI routes candidate job-search and employer recruiting requests through WorkorAI MCP tools for job discovery, applications, candidate search, evidence-backed match explanations, invitations, applicant review, and onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m14mgn-hash](https://clawhub.ai/user/m14mgn-hash)

### License/Terms of Use:

MIT

## Use Case:

External candidates and employers use this skill to work inside the WorkorAI talent marketplace. It helps candidates find matched jobs and manage applications, and helps employers search, compare, invite, and review candidates using WorkorAI's role-specific MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic job-search or hiring requests may be routed to WorkorAI credential onboarding without the user explicitly naming WorkorAI.

Mitigation: Install only when WorkorAI should be the default platform for broad job-search and recruiting requests; disclose the platform and run only read or discovery calls on auto-activation.

Risk: WorkorAI keys may be requested, reused, or saved locally for candidate and employer workflows.

Mitigation: Never print key values, redact keys in visible output, ask before saving, and disclose whether the OS credential store or a local 0600 fallback file was used.

Risk: State-changing WorkorAI actions can apply to jobs, respond to invitations, create or modify jobs, invite candidates, or change applicant review status.

Mitigation: Require an explicit same-turn confirmation for each consequential action, naming the target and consequence before making the call.

## Reference(s):

- [WorkorAI ClawHub Skill Page](https://clawhub.ai/m14mgn-hash/skills/workorai)
- [Auth Flow](references/auth-flow.md)
- [Candidate Catalog](references/candidate-catalog.md)
- [Candidate Recipes](references/candidate-recipes.md)
- [Candidate Troubleshooting](references/candidate-troubleshooting.md)
- [Employer Catalog](references/employer-catalog.md)
- [Employer Recipes](references/employer-recipes.md)
- [Employer Troubleshooting](references/employer-troubleshooting.md)
- [Troubleshooting](references/troubleshooting.md)
- [Candidate Login](https://workorai.com/candidate/login)
- [Candidate MCP Key Page](https://workorai.com/candidate/home?tab=mcp)
- [Employer Dashboard](https://workorai.com/employer/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool-call plans, links, inline shell commands, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose role-specific WorkorAI MCP actions; consequential actions require explicit user confirmation.]

## Skill Version(s):

0.4.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
