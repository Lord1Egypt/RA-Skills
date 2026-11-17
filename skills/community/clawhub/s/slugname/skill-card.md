## Description:

Search X (Twitter) posts using the xAI API. Use when the user wants to find tweets, search X/Twitter, look up what people are saying on X, or find social media posts about a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinbrother](https://clawhub.ai/user/kevinbrother)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to search recent X posts with xAI, filter by handles or date ranges, and receive summarized results with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to xAI's API and may contain sensitive or proprietary information.

Mitigation: Use only queries approved for third-party processing, and avoid sensitive, confidential, regulated, or proprietary terms unless policy permits.

Risk: The skill requires an XAI_API_KEY for authenticated API access.

Mitigation: Store the key in an environment variable or managed secret, restrict access to it, and rotate or revoke it if exposed.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [ClawHub skill page](https://clawhub.ai/kevinbrother/skills/slugname)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON printed by a Python command, with text summaries and URL citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status, query, text, citations, x_search call count, and token usage when returned by the API.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
