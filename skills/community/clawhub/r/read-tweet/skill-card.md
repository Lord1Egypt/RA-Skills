## Description:

Reads Twitter/X tweet content from shared tweet links and returns structured tweet details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sawzhang](https://clawhub.ai/user/sawzhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to read an X/Twitter post from a shared URL and present the author, posting time, engagement counts, tweet body, and media or link details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tweet URLs supplied to the skill may be sent to third-party proxy services such as fxtwitter or vxtwitter.

Mitigation: Use the skill only for tweet URLs the user is comfortable sharing with those proxy services.

Risk: Fallback linked-article fetching or broader search can expand what the agent retrieves beyond the original tweet.

Mitigation: Ask the user before fetching linked articles or using broader search fallbacks.

Risk: Thread or long-tweet handling may return only the first tweet or incomplete content.

Mitigation: Tell the user when a result may be partial and ask whether to retrieve additional thread context.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sawzhang/skills/read-tweet)
- [Primary tweet proxy endpoint pattern](https://api.fxtwitter.com/{username}/status/{tweet_id})
- [Fallback tweet proxy endpoint pattern](https://api.vxtwitter.com/{username}/status/{tweet_id})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with structured tweet fields and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include author, timestamp, engagement counts, tweet body, and media or link descriptions when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
