## Description:

Helps agents research public Reddit posts, comments, and communities through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to collect and analyze public Reddit content and community data, with cost estimates, pagination, and export guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reddit URLs, usernames, queries, filters, and result limits are sent to SocQ's hosted service.

Mitigation: Share only data appropriate for the service and review the requested scope before submitting.

Risk: The SocQ API key grants access to the service.

Mitigation: Keep SOCQ_API_KEY in the environment; do not put it in prompts, URLs, or saved commands.

Risk: Ad hoc npx execution may fetch a changing CLI package.

Mitigation: For tighter supply-chain control, use a vetted socq installation or a pinned @socq/cli version.

Risk: Large or repeated requests may incur credits.

Mitigation: Check the estimated cost and obtain confirmation before paid large-volume or multi-endpoint runs.

## Reference(s):

- [SocQ Reddit API documentation](https://docs.socq.ai/api-manual/reddit)
- [SocQ MCP and CLI integration guide](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools](https://github.com/SocQAPI/socq-devtools)
- [Reddit endpoint reference](references/platform.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown summaries with optional commands and raw export locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include endpoint, credit usage, task status, result count, and coverage caveats.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
