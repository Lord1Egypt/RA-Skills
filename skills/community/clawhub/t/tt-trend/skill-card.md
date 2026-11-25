## Description:

Read-only TikTok trend research that searches public videos by keyword, retrieves creator videos and video comments, and returns structured JSON for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content creators, market researchers, and agent developers use this skill to explore TikTok trends, creator output, competitor content, and comment sentiment. It requires Node.js and a GUAIKEI_API_TOKEN.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis had medium confidence and partial file coverage, and runtime permission limits were not verified.

Mitigation: Review the skill and run it with limited permissions; provide its API token only in a trusted environment.

Risk: Timestamps use fixed Beijing time, which may not match the timezone expected in downstream reports.

Mitigation: Convert timestamps to the reporting timezone and label the timezone when aggregating results.

## Reference(s):

- [Usage options and output fields](artifact/references/options.md)
- [Setup and troubleshooting](artifact/references/faq.md)
- [Release notes](artifact/references/changelog.md)
- [GuaiKei API service](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/guaikei/skills/tt-trend)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns TikTok keyword search results, creator videos, or video comments; request limits depend on the account plan.]

## Skill Version(s):

1.1.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
