## Description:

Extracts Instagram user profiles, followers, and following lists using apidojo's Instagram User Scraper on Apify, returning public profile metadata and contact fields for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, outreach teams, and competitive intelligence analysts use this skill to find Instagram accounts by keyword, handle, profile URL, or user ID and export public profile metadata for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect personal data such as public emails, phone numbers, bios, and follower relationships.

Mitigation: Restrict access to exported files, minimize collection with maxItems and disabled follower/following options when possible, and confirm the use complies with applicable law and platform terms.

Risk: Large follower or following exports can increase collection volume and cost.

Mitigation: Set maxItems and only enable follower or following collection when it is needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-instagram-users-by-keyword)
- [Apify actor API endpoint](https://api.apify.com/v2/acts/apidojo~instagram-user-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON input examples; actor results may be exported as CSV or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return Instagram profile metadata, follower/following lists, and public contact fields when those collection options are enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
