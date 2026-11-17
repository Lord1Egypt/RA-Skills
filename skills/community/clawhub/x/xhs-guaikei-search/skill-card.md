## Description:

Searches public XiaoHongShu notes, retrieves note details and comments, and fetches public creator posts for trend research, competitor analysis, KOL screening, and comment insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content creators, analysts, and operations teams use this skill to collect structured public XiaoHongShu data for content research, account monitoring, comment analysis, and market trend review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API tokens, XiaoHongShu URLs, keywords, and requested limits to Guaikei API endpoints.

Mitigation: Use the skill only when Guaikei is trusted for the research target, keep GUAIKEI_API_TOKEN scoped and private, and rotate the token if exposure is suspected.

Risk: Generated logs may contain full URLs, xsec_token values, keywords, comments, and profile data.

Mitigation: Run the skill in a workspace with appropriate access controls and regularly delete or protect the logs directory.

Risk: The skill is limited to public XiaoHongShu data and can return empty or error results for unavailable, deleted, private, or unsupported content.

Mitigation: Treat empty or error responses as retrieval failures, verify inputs, and avoid fabricating analysis from missing data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-guaikei-search)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return status, request metadata, runtime metadata, and structured results; successful runs may also save JSON logs locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
