## Description:

Automates Twitter/X posting, engagement, draft workflows, thread splitting, and growth planning for OpenClaw AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[persnola1-sketch](https://clawhub.ai/user/persnola1-sketch)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to configure an OpenClaw agent for Twitter/X account activity, including posting, replies, retweets, follows, queue-based publishing, and draft review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post, reply, retweet, delete, follow, and unfollow through a real Twitter/X account, creating public account impact.

Mitigation: Install only for accounts where agent read/write Twitter/X authority is acceptable, keep new or sensitive accounts in DRAFT mode, and review queued entries before posting.

Risk: Autonomous cron usage can publish repeated, unsuitable, or unintended content.

Mitigation: Avoid cron posting until the workflow is trusted, maintain the posted log, check for duplicate topics, and require approval for sensitive topics or high-impact tagging.

Risk: The workflow depends on Twitter/X credentials and Tweepy behavior.

Mitigation: Store credentials in environment variables, limit credential exposure, and consider pinning Tweepy in a virtual environment.

## Reference(s):

- [Twitter/X Developer Portal](https://developer.x.com)
- [Twitter API OAuth2 Token Endpoint](https://api.twitter.com/oauth2/token)
- [Content Strategy](references/content-strategy.md)
- [Twitter Strategy Templates](references/strategy-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python usage examples, and local queue/log file conventions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can produce public Twitter/X actions through API calls when credentials and auto-posting workflows are configured.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
