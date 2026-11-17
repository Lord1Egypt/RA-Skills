## Description:

Searches English-language social platforms, including Reddit posts, Twitter/X posts, and YouTube videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run targeted English-language searches across Reddit, Twitter/X, and YouTube and collect normalized result records for downstream review or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider credentials for TikHub and YouTube can be exposed when supplied as command-line arguments or included in unsanitized error output.

Mitigation: Prefer environment variables, use narrowly scoped provider keys with quotas, and sanitize command output before storing or sharing logs.

Risk: The release has a suspicious security verdict and requires review before installation or production use.

Mitigation: Install in a virtual environment, pin dependencies, review the scripts and security summary, and run only with the minimum credentials needed for the target platform.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-search-social-en)
- [Publisher profile](https://clawhub.ai/user/sensenova-skills)
- [Reddit search JSON endpoint](https://www.reddit.com/search.json)
- [TikHub API base](https://api.tikhub.io)
- [YouTube Data API search endpoint](https://www.googleapis.com/youtube/v3/search)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration guidance]

**Output Format:** [Standard JSON search-result objects emitted by command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include success, query, provider, items, and error fields; provider-specific item fields may include URLs, snippets, authors, timestamps, counts, channels, and thumbnails.]

## Skill Version(s):

2026.8.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
