## Description:

Extracts comments from Instagram posts using apidojo's Instagram Comments Scraper on Apify, returning comment text, engagement counts, commenter metadata, and timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Social media analysts, community managers, and researchers use this skill to collect Instagram post comment datasets for sentiment analysis, community review, engagement reporting, or downstream research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported commenter names, IDs, profile links, pictures, and comment text can be personal data.

Mitigation: Limit maxItems and exported fields to what is necessary, restrict access to exports, and handle the data under applicable privacy, consent, retention, and deletion requirements.

Risk: Instagram collection may be inappropriate for private, deleted, restricted, or rate-limited posts.

Mitigation: Confirm the post can be accessed and processed for the intended purpose, reduce maxItems when rate limits occur, and avoid treating empty results as proof of no engagement.

Risk: Use of the Apify actor may need to comply with Instagram terms and external service requirements.

Mitigation: Confirm the collection workflow complies with Instagram terms, Apify requirements, and the user's applicable organizational policy before running exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-instagram-comments)
- [API Dojo publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor](https://apify.com/apidojo/instagram-comments-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON input examples, and CSV or JSON export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include comment text, engagement counts, commenter identifiers, profile links, profile pictures, and timestamps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
