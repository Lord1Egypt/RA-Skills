## Description:

Extracts slang definitions, cultural terms, and crowd-sourced meanings from Urban Dictionary using apidojo's Urban Dictionary Scraper on Apify for brand, content, and trend research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, brand researchers, social media analysts, content teams, and cultural marketers use this skill to look up internet slang, meme terminology, and brand-related cultural vocabulary, then compare definitions by approval, vote volume, and recency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may disclose slang keywords, brand names, Urban Dictionary URLs, or monitoring terms to Apify/apidojo.

Mitigation: Do not use secrets, confidential project names, personal data, or sensitive internal monitoring terms without a separate privacy review.

Risk: Urban Dictionary content can be explicit, offensive, outdated, or disputed.

Mitigation: Filter results downstream for professional use and review definitions by approval, vote volume, and recency before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/researching-internet-slang-and-cultural-trends)
- [Apify Urban Dictionary Scraper API endpoint](https://api.apify.com/v2/acts/apidojo~urbandictionary-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON, CSV, or table outputs from the actor]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The actor returns word, definition, usage example, author, upvotes, downvotes, and date; downstream filtering may be needed for explicit content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
