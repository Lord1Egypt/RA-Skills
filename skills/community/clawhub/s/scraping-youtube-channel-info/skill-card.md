## Description:

Extracts YouTube channel metadata, subscriber counts, video counts, and descriptions using apidojo's YouTube Channel Scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, influencer researchers, competitive analysts, and YouTube marketers use this skill to collect YouTube channel metadata by URL, handle, or keyword search for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube URLs, handles, keywords, country and language filters, and related parameters are sent to Apify for actor execution.

Mitigation: Use the skill only when this third-party transmission fits the user's account, data handling, and confidentiality requirements.

Risk: The customMapFunction input can transform each output object and may broaden downstream data exposure or processing behavior.

Mitigation: Review customMapFunction content before use and restrict it to expected transformations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-youtube-channel-info)
- [Apify YouTube Channel Scraper run endpoint](https://api.apify.com/v2/acts/apidojo~youtube-channel-scraper/runs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples; actor results may be returned as JSON or CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns channel metadata fields such as name, URL, description, subscriber count, video count, verification status, keywords, available countries, and tags.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
