## Description:

Fetches and formats the two Wenxuecity News 24-hour ranking lists, hot ranking and discussion ranking, as Markdown or JSON for daily digests, monitoring, diffing, or automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyguo2010](https://clawhub.ai/user/tonyguo2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can fetch Wenxuecity News 24-hour hot and discussion rankings and turn them into Markdown or JSON for daily digests, monitoring, storage, or comparison workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch script can be pointed at arbitrary URLs, creating broader outbound HTTP access than the Wenxuecity ranking use case requires.

Mitigation: Run only in environments where arbitrary outbound HTTP GET requests are acceptable, or restrict the source URL to the intended Wenxuecity HTTPS host before deployment.

Risk: Ranking extraction depends on the live Wenxuecity page structure, so site changes can produce missing or partial results.

Mitigation: Validate the parser against the live source page after page layout changes and review partial outputs before relying on them in automation.

## Reference(s):

- [Wenxuecity News source page](https://www.wenxuecity.com/news/)
- [ClawHub skill page](https://clawhub.ai/tonyguo2010/skills/wenxuecity-news-rankings)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands]

**Output Format:** [Markdown or JSON ranking data, optionally written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes fetched timestamp, source URL, requested top count, hot_24h and discussion_24h groups, and optional image URLs.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
