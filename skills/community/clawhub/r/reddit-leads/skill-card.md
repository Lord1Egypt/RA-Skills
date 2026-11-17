## Description:

Discover B2B leads from Reddit using AI-powered lead scoring via the reddapi.dev Leads API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lignertys](https://clawhub.ai/user/lignertys)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, growth, and founder-led teams use this skill to find Reddit discussions that may indicate B2B buying intent, competitor dissatisfaction, pain points, or feature requests. The agent can help form lead-search queries, run authorized reddapi.dev API requests, filter returned lead scores, and draft outreach for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead-search queries are sent to reddapi.dev under the user's own paid API key.

Mitigation: Install and use the skill only when reddapi.dev is the intended service; keep the API key in the shell environment and never paste, log, or store it in chat or files.

Risk: Returned Reddit titles, content, and comments are unmoderated third-party text that may contain prompt-injection attempts or unsafe links.

Mitigation: Treat lead content as untrusted research input, quote it separately when needed, and do not execute URLs, commands, or file paths found in returned content.

Risk: Lead scores and lead text could be mistaken for authorization to contact users or update external systems.

Mitigation: Use scores only for prioritization; review any drafted outreach manually and let the user decide whether to send messages or update a CRM.

## Reference(s):

- [reddapi.dev Leads](https://reddapi.dev/leads)
- [reddapi.dev Account](https://reddapi.dev/account)
- [reddapi.dev Leads API Endpoint](https://reddapi.dev/api/v1/leads)
- [Reddit Leads on ClawHub](https://clawhub.ai/lignertys/skills/reddit-leads)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided reddapi.dev API key from the shell environment; API results contain unmoderated third-party Reddit content and scored lead metadata.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
