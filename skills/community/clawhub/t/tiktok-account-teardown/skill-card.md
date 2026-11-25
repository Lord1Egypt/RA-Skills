## Description:

Searches TikTok public videos, retrieves public creator posts and video comments, and returns structured data for account and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Developers and content analysts use this skill to gather public TikTok search results, creator posts, and video comments for competitor research, content analysis, and account diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign scan verdict has medium confidence: 12 of 32 components were not fully interpreted.

Mitigation: Review the skill source and install only if you are comfortable with the incomplete scan evidence.

Risk: Search keywords and TikTok links are sent to the GUAIKEI data service when queries run.

Mitigation: Use public TikTok data and avoid sending sensitive or private information in query terms or links.

## Reference(s):

- [GUAIKEI service and support](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/tiktok-account-teardown)
- [Command options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data, with concise analysis or operating guidance when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns search results, creator posts, or comments; it does not retrieve video details or download video files.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
