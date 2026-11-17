## Description:

Post native X/Twitter threads by chaining reply-to calls via Twitter API v2 for multi-tweet content from a content pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to preview, post, and schedule native X/Twitter threads from prepared Markdown thread files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule real X/Twitter threads using local or environment credentials.

Mitigation: Use it only for intended posting workflows, verify the active X/Twitter account before execution, and require explicit confirmation before post, schedule, or fire actions.

Risk: The artifact documents use of an undeclared local OAuth credential store at ~/.xurl.

Mitigation: Prefer a single declared credential source and review local OAuth credentials before using the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/twitter-thread-scheduler)
- [Publisher Profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TWITTER_ACCESS_TOKEN; documented behavior includes outbound Twitter API calls and local queue/log files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
