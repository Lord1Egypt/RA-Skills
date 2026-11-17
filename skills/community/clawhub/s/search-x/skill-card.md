## Description:

Real-time X/Twitter search powered by Grok-4 for finding tweets, trends, and discussions with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvanhorn](https://clawhub.ai/user/mvanhorn)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to search X/Twitter in real time through xAI, optionally filtering by date range, included handles, or excluded handles, and returning tweet text, timestamps, links, citations, or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, date filters, and handle filters are sent to xAI.

Mitigation: Use the skill only for queries that are appropriate to send to xAI, and avoid submitting sensitive or confidential search terms.

Risk: The skill requires an xAI API key and may read the local ~/.clawdbot/clawdbot.json configuration as a fallback credential source.

Mitigation: Keep XAI_API_KEY private, restrict local config file access, and review the local credential lookup before installation if shared skill config is not desired.

Risk: Returned tweets and citations may reflect fast-moving public discussion and should not be treated as verified facts by default.

Mitigation: Review linked citations and corroborate important claims before relying on the search output.

## Reference(s):

- [Search X on ClawHub](https://clawhub.ai/mvanhorn/skills/search-x)
- [xAI Documentation](https://docs.x.ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown text with tweet links and citations, links-only text, or full JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY; default search window is configurable with SEARCH_X_DAYS, and model selection is configurable with SEARCH_X_MODEL.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
