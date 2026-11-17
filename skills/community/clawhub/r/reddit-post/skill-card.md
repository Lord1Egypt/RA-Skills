## Description:

Manages bookkeeping after manually approved Reddit drafts are posted, including moving files, adding Reddit URLs, updating active tasks, and logging outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lknezic](https://clawhub.ai/user/lknezic)

### License/Terms of Use:


## Use Case:

Operators using a manual Reddit publishing workflow use this skill after Luka confirms a post URL, so the agent can archive the posted draft, update task records, and capture outcome signals without submitting content to Reddit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled reference guidance includes account-warming and anti-detection language that could encourage platform-evasion behavior.

Mitigation: Review and rewrite that guidance as plain compliance guidance focused on subreddit rules, required disclosures, and stopping activity when moderation issues occur.

Risk: Incorrect bookkeeping could move or delete pending drafts before a post is confirmed.

Mitigation: Require a Reddit URL from Luka before moving drafts to posted storage, and confirm the posted copy exists before deleting the pending draft.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lknezic/skills/reddit-post)
- [Safety and Anti-Detection Rules](artifact/ref-safety.md)
- [Posting Settings Reference](artifact/ref-settings.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown file updates and task-log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bookkeeping updates after a human supplies a Reddit URL; it does not submit posts to Reddit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
