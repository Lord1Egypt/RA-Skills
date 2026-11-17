## Description:

Find Reddit threads ranking on Google Page 1 for keywords and draft contextual replies that naturally mention a product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aces1up](https://clawhub.ai/user/aces1up)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, founders, and growth teams use RedditRank to discover Reddit threads that may drive organic traffic and to draft replies for user review before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends email, API key, product descriptions, URLs, and Reddit thread context to the RedditRank service.

Mitigation: Use it only with data the user is comfortable sharing with that service, and review product and thread inputs before submitting requests.

Risk: API keys may be stored or displayed insecurely during setup or local use.

Mitigation: Run setup as a normal user, avoid sharing setup logs or screenshots, prefer environment variables where appropriate, and restrict permissions on ~/.redditrank/config.json.

Risk: Generated replies could be used for covert or spammy Reddit promotion.

Mitigation: Require user review before posting, never auto-post to Reddit, and encourage transparent replies that add genuine value to the conversation.

## Reference(s):

- [RedditRank ClawHub Listing](https://clawhub.ai/aces1up/skills/redditrank)
- [RedditRank Homepage](https://clawagents.dev/redditrank)
- [RedditRank API Base](https://clawagents.dev/reddit-rank/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with thread metadata, reply drafts, and inline setup or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the RedditRank service and may include product descriptions, URLs, Reddit thread context, fit scores, QA scores, usage status, and daily-limit guidance.]

## Skill Version(s):

1.0.2 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
