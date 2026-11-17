## Description:

Assists agents with posting tweets, replies, and quote reposts on Twitter/X using twitter-cli, with content confirmation and login-status support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiyea](https://clawhub.ai/user/baiyea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and publish Twitter/X posts, replies, or quote reposts from an agent workflow. It is also useful when an agent needs structured JSON results after checking Twitter/X login status or publishing content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts, replies, or quote reposts from the user's Twitter/X account.

Mitigation: Review the exact content, target tweet, account, and images before approving any posting action.

Risk: The skill depends on an unpinned third-party twitter-cli package.

Mitigation: Use a pinned reviewed version of twitter-cli in an isolated environment when deploying the skill.

Risk: Broad activation phrasing may increase the chance of unintended social posting.

Mitigation: Require explicit user confirmation before running post, reply, or quote scripts.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post, reply, quote, and login-status scripts support --json; posting actions use twitter-cli through the user's logged-in Twitter/X browser session.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
