## Description:

Run a Reddit account within subreddit rules, karma phases, quotas, and removal recovery for posting from a cron or agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a single Reddit profile for scheduled posts and replies while respecting subreddit rules, karma gates, quotas, and recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent operates a real logged-in Reddit profile and can make public posts or replies attributed to the user.

Mitigation: Use only for an account the user intentionally wants an agent to operate, review top-level posts manually, and stop whenever the skill calls for human review.

Risk: Optional webhooks can send recap data, post or reply URLs, karma counts, and blocker text to third-party providers.

Mitigation: Keep alerts.webhook empty unless third-party recap sharing is intended and approved.

Risk: Automation challenges, rate limits, subreddit automation bans, or removals can put the Reddit account at risk if ignored.

Mitigation: Stop on CAPTCHA or challenge pages, respect subreddit rules and quotas, freeze subs after removals, and avoid communities that ban automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexbloch-ia/skills/reddit-account-operations)
- [OpenClaw homepage](https://openclaw.ai)
- [Repository listed in ClawHub metadata](https://github.com/AlexBloch-IA/reddit-account-operations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local markdown run logs and can send opt-in webhook recaps when configured.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
