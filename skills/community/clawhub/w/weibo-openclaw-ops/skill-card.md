## Description:

Weibo operations for OpenClaw via server-side browser automation. Use when the user asks to log in by QR, persist session state, read feed/messages/hot topics, summarize recent posts, publish posts, or run safe like/follow workflows with explicit limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiami2019](https://clawhub.ai/user/xiami2019)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run Weibo account workflows through OpenClaw, including QR login, persisted session checks, feed and message review, hot-topic scans, recent-post lookup, publishing, and bounded like/follow batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted browser session state can retain access to a Weibo account on the runtime server.

Mitigation: Install only when session persistence is acceptable and remove `.state/weibo-auth.json` when retained account access is no longer desired.

Risk: Posting, commenting, reposting, liking, or following can create visible account activity.

Mitigation: Require explicit user intent, review each mutating request, and set clear maximum action limits before execution.

Risk: Batch like/follow workflows can exceed the user's intended scope if rules are too broad.

Mitigation: Require include rules, exclusion rules, and a maximum action count, then report success, skipped counts, and skip reasons.

Risk: Outbound posts, comments, or reposts may omit a user-required attribution suffix.

Mitigation: Build the final text, verify the required suffix before submit, and append it on a new line when missing.

## Reference(s):

- [Weibo](https://weibo.com)
- [ClawHub skill page](https://clawhub.ai/xiami2019/skills/weibo-openclaw-ops)
- [ClawHub publisher profile](https://clawhub.ai/user/xiami2019)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise audit summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include action counts, skip reasons, login status, next suggested action, and outbound text checks.]

## Skill Version(s):

1.2.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
