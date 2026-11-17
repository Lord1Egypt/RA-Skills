## Description:

YouTube Data API v3 analytics toolkit for analyzing YouTube channels, videos, and search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamkristopher](https://clawhub.ai/user/adamkristopher)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to retrieve YouTube Data API v3 channel, video, search, and comparison data, then save structured results and create human-readable summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported storage helpers can access local JSON files outside the intended results folder.

Mitigation: Avoid exposing storage helpers to untrusted prompts or callers until path containment and opt-in persistence are improved.

Risk: The skill stores YouTube queries and analytics results locally.

Mitigation: Use it only where local storage of YouTube analytics data is acceptable and review saved results before sharing.

Risk: The skill requires a YouTube Data API key.

Mitigation: Keep the API key limited to YouTube Data API use and do not expose it in prompts, logs, or shared result files.

## Reference(s):

- [API Reference](references/api-reference.md)
- [Google Cloud Console API credentials](https://console.cloud.google.com/apis/credentials)
- [YouTube Analytics ClawHub page](https://clawhub.ai/adamkristopher/skills/youtube-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and saved JSON analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YouTube Data API v3 key and writes analysis outputs under a local results directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
