## Description:

Extracts Urban Dictionary definitions, examples, authors, vote counts, and timestamps for supplied keywords or Urban Dictionary URLs using apidojo's Apify actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as linguists, brand researchers, content teams, and cultural trend analysts use this skill to collect Urban Dictionary definitions and voting signals for slang, meme, and phrase analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested slang terms or Urban Dictionary URLs are sent to Apify.

Mitigation: Use the skill only when that external API use is acceptable, and avoid sending sensitive or private terms or URLs.

Risk: Urban Dictionary content is public, user-generated, and may be explicit or offensive.

Mitigation: Review and filter returned records before presenting them to end users or using them in downstream analysis.

Risk: Unbounded scraping can produce unpredictable output size and cost.

Mitigation: Set maxItems for predictable result volume and processing cost.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-urban-dictionary-definitions)
- [Apify actor run API](https://api.apify.com/v2/acts/apidojo~urbandictionary-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands, REST API examples, and JSON or CSV-capable actor output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned records include word, definition, example, author, ID, timestamp, vote counts, and URL; maxItems can cap output size.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
