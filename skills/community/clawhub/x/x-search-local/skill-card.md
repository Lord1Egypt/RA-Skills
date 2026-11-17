## Description:

Search X (Twitter) posts using the xAI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taotao666720](https://clawhub.ai/user/taotao666720)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search X/Twitter posts by keyword, handle filters, exclusions, date range, and optional image or video understanding, then present summarized results with citations to original posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to xAI using the user's XAI_API_KEY.

Mitigation: Use this skill only for intended X/Twitter searches and avoid including sensitive private information in queries.

Risk: Broad trigger wording may cause an agent to select the skill for general social-media requests.

Mitigation: Specify X or Twitter clearly when invoking the skill and review the proposed search before execution.

Risk: The skill calls an external API and may fail because of network, timeout, API, or credential errors.

Mitigation: Confirm XAI_API_KEY is configured and handle the JSON status or error output before relying on results.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [ClawHub skill page](https://clawhub.ai/taotao666720/skills/x-search-local)

## Skill Output:

**Output Type(s):** [text, JSON, citations]

**Output Format:** [JSON containing status, query, summarized text, citations, search count, and token usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY; supports handle filters, exclusions, date ranges, image understanding, and video understanding.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
