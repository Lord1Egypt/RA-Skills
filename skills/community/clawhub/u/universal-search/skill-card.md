## Description:

Universal Search lets agents submit natural-language web search queries to a remote service and receive structured answers with sources and credibility scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cattei](https://clawhub.ai/user/cattei)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to give an agent web search capability with summarized answers, source links, and confidence-oriented verification signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user queries to a third-party search endpoint.

Mitigation: Use it only for queries that are appropriate to share with that endpoint, and avoid secrets, private company data, or regulated information.

Risk: The release evidence reports a reusable bundled bearer token and an environment-configurable request URL.

Mitigation: Do not rely on the bundled token; rotate it, provide approved credentials through environment variables, and constrain use to an approved HTTPS endpoint.

Risk: The security verdict is suspicious.

Mitigation: Review the release before installing and apply the evidence guidance before using it in an agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cattei/skills/universal-search)
- [Search service homepage](https://49srjp57sf.coze.site)
- [Search API endpoint](https://49srjp57sf.coze.site/run)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Formatted text or JSON returned by a Python command-line script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include an answer summary, detailed explanation, source list, and credibility-scored verification results.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
