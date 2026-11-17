## Description:

Tracks trending YouTube topics, high-performing video formats, title patterns, and creator momentum within a niche using apidojo's YouTube scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

YouTube creators, video marketers, and brand video strategists use this skill to research niche-specific content trends and turn high-performing video patterns into topic briefs and title ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback shows an Apify token in a URL, which can expose credentials through shell history, logs, or shared links.

Mitigation: Use an Apify token with minimal permissions and prefer an Authorization header or MCP-based secret handling instead of token-in-URL calls.

Risk: The workflow recommends running a relative Node script that is not present in the release artifact.

Mitigation: Verify the script path and implementation before running it, or use the reviewed Apify MCP/API flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/tracking-youtube-trending-topics-by-niche)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/youtube-scraper](https://apify.com/apidojo/youtube-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown trend brief with tables, scored findings, recommended video ideas, and optional bash or API call snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include instructions for saving Apify results as CSV or JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
