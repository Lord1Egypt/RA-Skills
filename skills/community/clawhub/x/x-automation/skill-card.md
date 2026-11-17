## Description:

Automates X posting workflows by scraping trends, generating tweet ideas, managing approval queues, and posting through a logged-in browser session without X API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nightfullstar](https://clawhub.ai/user/nightfullstar)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to help an agent gather X trends, draft social posts, queue content for review, and publish approved tweets from a logged-in browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in X browser session and publish public posts from the user's account.

Mitigation: Keep human approval mandatory for every post, review queued content before posting, and avoid whitelist or full-auto modes.

Risk: Persistent browser sessions and local JSON files may expose account context, scraped trends, queued tweets, or posting history.

Mitigation: Use an isolated browser profile where possible and review or delete local data files regularly.

Risk: Browser-based posting automation may create account, policy, or abuse risk if used aggressively.

Mitigation: Use conservative posting schedules and rate limits, avoid spam-like behavior, and pin dependencies before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nightfullstar/skills/x-automation)
- [Publisher profile](https://clawhub.ai/user/nightfullstar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated tweet text, and local JSON data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write trend, queue, and tweet-history JSON files under data/ and can publish public posts through the user's logged-in X browser session.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
