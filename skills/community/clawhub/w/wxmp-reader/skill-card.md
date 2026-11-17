## Description:

Read and summarize WeChat Official Account articles by URL, extracting title, author, date, article text, and optional screenshots through local browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reedchan7](https://clawhub.ai/user/reedchan7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to read, summarize, analyze, or screenshot WeChat Official Account article links when standard web fetching cannot retrieve the content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can load arbitrary HTTP URLs in local browser automation if URL validation is not enforced.

Mitigation: Validate that inputs are WeChat article URLs on mp.weixin.qq.com before running browser scripts.

Risk: The browser automation can run Chrome with sandboxing disabled.

Mitigation: Run only in isolated environments or revise the scripts to keep Chrome sandboxing enabled where supported.

Risk: The documented workflow can send article screenshots automatically, including when the user only requested a summary.

Mitigation: Make screenshot sending opt-in or confirm before sending, then write screenshots only to a private temporary path and delete them after use.

Risk: The skill may depend on global or system package discovery for Chrome and playwright-core.

Mitigation: Prefer pinned local dependencies and verified Chrome paths for reproducible execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/reedchan7/skills/wxmp-reader)
- [Google Chrome Linux Signing Key](https://dl.google.com/linux/linux_signing_key.pub)
- [Google Chrome Linux Repository](http://dl.google.com/linux/chrome/deb/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown summary with optional JSON article metadata and PNG screenshot file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a temporary PNG screenshot that should be sent only when appropriate and deleted after use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
