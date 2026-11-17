## Description:

Searches X (Twitter) posts through the xAI API for tweets, social discussion, handle-filtered results, date ranges, and media-aware searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ywqsimmon](https://clawhub.ai/user/ywqsimmon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search X/Twitter content through xAI, including real-time topical searches, account filters, exclusion filters, date ranges, and optional image or video understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, handles, date filters, and optional media-analysis requests are sent to xAI using the user's XAI_API_KEY.

Mitigation: Use the skill only when external xAI processing is acceptable, and avoid confidential investigations or sensitive personal data unless that processing has been approved.

Risk: The skill returns social-media search summaries and citations that may be incomplete, stale, or influenced by source-platform availability.

Mitigation: Review cited original posts before relying on results for decisions, publication, or escalation.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [ClawHub skill page](https://clawhub.ai/ywqsimmon/skills/xsearchywq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON search results with text summaries, citations, search count, and token usage; agent-facing guidance may be rendered as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY; supports handle filters, excluded handles, date ranges, image understanding, and video understanding.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
