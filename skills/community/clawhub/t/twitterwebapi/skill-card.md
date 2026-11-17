## Description:

Provides Twitter/X tweet detail and search timeline requests that return tweet content, author information, timestamps, engagement data, and search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyriswu](https://clawhub.ai/user/kyriswu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch a single Twitter/X tweet by ID, search timelines by keyword, and present returned tweet data or request failure details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tweet IDs, search terms, cursors, and any provided AZT_API_KEY are sent to coze-js-api.devtool.uk.

Mitigation: Review the third-party service path before installation, avoid sensitive Twitter/X searches, and provide AZT_API_KEY through a protected environment secret.

Risk: The documented command-line AZT_API_KEY pattern can expose keys through prompts, logs, shell history, or process listings.

Mitigation: Prefer AZT_API_KEY from a protected environment secret and omit key values from prompts, logs, and command arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyriswu/skills/twitterwebapi)
- [Twitter tweet detail endpoint](https://coze-js-api.devtool.uk/twitter/fetch_tweet_detail)
- [Twitter search timeline endpoint](https://coze-js-api.devtool.uk/twitter/fetch_search_timeline)
- [DevTool plugin page](https://devtool.uk/plugin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summaries with optional raw JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalizes tweet detail and search responses into human-readable status, tweet, author, timestamp, engagement, link, and error fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
