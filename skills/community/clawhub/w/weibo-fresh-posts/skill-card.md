## Description:

Monitors a Weibo following timeline by switching to the latest-posts feed, extracting posts by original publication time, deduplicating by original link, and writing daily Markdown digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hwb96](https://clawhub.ai/user/hwb96)

### License/Terms of Use:


## Use Case:

External OpenClaw users use this skill to keep a local Markdown digest of recent posts from their Weibo following timeline, reducing missed updates and preserving the original post text, summary, timestamp, author, and permalink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cron installer creates an ongoing OpenClaw task that continues using the logged-in Weibo browser profile.

Mitigation: Review the task name and schedule before installation, and document or add disable and uninstall steps before routine use.

Risk: The skill writes recurring local digest files that may contain Weibo post content from an authenticated session.

Mitigation: Store the digest directory in an appropriate local location, review retention needs, and avoid including credentials, cookies, or secrets in prompts or output files.

Risk: Timeline navigation or timestamp parsing failures could produce incomplete or misleading digests.

Mitigation: Use the built-in latest-timeline verification, skip unparseable timestamps, and review run summaries for skipped items or navigation failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hwb96/skills/weibo-fresh-posts)
- [Publisher profile](https://clawhub.ai/user/hwb96)
- [Workflow reference](references/workflow.md)
- [Markdown schema reference](references/markdown-schema.md)
- [Cron setup reference](references/cron-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with tabular digest rows and concise run summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily digest files under ~/weibo-digest and can create an optional recurring OpenClaw cron task.]

## Skill Version(s):

0.1.4 (source: server release metadata and artifact README publish command)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
