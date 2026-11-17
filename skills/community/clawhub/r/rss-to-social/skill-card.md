## Description:

Automatically monitor RSS feeds and post to social media. Schedule content, generate posts with AI, and publish to Twitter/LinkedIn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor configured RSS feeds, generate draft social posts for Twitter or LinkedIn, and manage posting cadence and deduplication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overstates automatic social posting relative to the artifact behavior and may mark items as posted after draft generation.

Mitigation: Treat generated posts as drafts until explicit publication controls and successful posting confirmation are reviewed.

Risk: The skill requests high-impact Twitter or LinkedIn account credentials without clearly scoped direct-posting safeguards.

Mitigation: Do not provide social account credentials unless the skill is updated to clearly implement and scope direct posting.

Risk: Configured feeds cause outbound network access to user-provided URLs.

Mitigation: Use only trusted public feed URLs and run the skill with restricted network access where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fly3094/skills/rss-to-social)
- [Publisher profile](https://clawhub.ai/user/fly3094)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated social post text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces RSS monitoring status, generated Twitter and LinkedIn post drafts, and configuration guidance based on environment variables.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
