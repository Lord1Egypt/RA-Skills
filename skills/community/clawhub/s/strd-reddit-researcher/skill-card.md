## Description:

Scans Reddit for posts matching keywords and summarizes findings using Bing search, Reddit JSON API, and Google fallback paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and product teams use this skill to find Reddit posts and comments matching keywords, identify pain points and common themes, and export findings as Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Reddit URLs may reveal sensitive research topics to public search engines or Reddit endpoints.

Mitigation: Use only approved, non-sensitive topics and avoid personal, confidential, or regulated data in REDDIT_KEYWORDS and input URL files.

Risk: Local cache files and exported Markdown reports may retain sensitive keywords, URLs, and summaries in a shared workspace.

Mitigation: Review, restrict, or delete cache and export directories after research, and store outputs only in approved locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/strd-reddit-researcher)
- [Publisher profile](https://clawhub.ai/user/kryzl19)
- [Reddit JSON API search endpoint](https://www.reddit.com/search.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text and Markdown reports with Reddit links and extracted post/comment summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write timestamped Markdown exports and local cache files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
