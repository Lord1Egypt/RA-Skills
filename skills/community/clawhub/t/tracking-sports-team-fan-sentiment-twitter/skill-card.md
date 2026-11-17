## Description:

Tracks sports team fan sentiment on Twitter using apidojo's Tweet scraper, returning sentiment distribution, volume trends, top fan reactions, topic themes, and event-triggered spikes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External sports marketing teams, brand sponsors, sports analytics firms, and sports media teams use this skill to monitor Twitter fan sentiment, buzz, and event-driven reaction patterns for sports teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify token exposure in command history or shared logs.

Mitigation: Use a limited Apify token where possible and prefer an Authorization header over token-in-URL curl commands.

Risk: Sensitive watchlists or search terms may be sent to Apify as part of Twitter searches.

Mitigation: Avoid confidential watchlists or sensitive terms and only run searches you are comfortable sending to Apify.

Risk: Returned tweet data may be stored or handled locally after collection.

Mitigation: Handle downloaded tweet datasets according to local data retention and access-control requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/tracking-sports-team-fan-sentiment-twitter)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor identifier](apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, summary text, and optional JSON or CSV result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Apify token and Twitter search parameters; sentiment output includes classifications and a score from -1 to +1.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
