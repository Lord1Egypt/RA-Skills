## Description:

Collects the last 24 hours of popular posts from a specified subreddit, fetches post details and comments, and produces a Simplified Chinese daily digest in Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redisread](https://clawhub.ai/user/redisread)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content teams use this skill to gather recent activity from one subreddit and turn the posts and comments into a concise daily digest with summaries, key points, practical suggestions, inspiration, and social sharing copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented shell snippets use unquoted user-controlled subreddit and output path placeholders, which could allow a crafted value to run unintended commands.

Mitigation: Use only trusted subreddit names and output paths, and review or quote shell values before executing the generated command.

Risk: The skill runs a background Reddit-fetching command and creates local digest, temporary, and log files.

Mitigation: Run it in an expected workspace, confirm the configured output path, and review generated files before relying on or sharing the digest.

## Reference(s):

- [Output template](references/output-template.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration]

**Output Format:** [Markdown daily digest in Simplified Chinese, with temporary JSON files used during collection.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local digest, temporary detail, and log files under the configured output path.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
