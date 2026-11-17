## Description:

Monitors Tom Doerr's X.com profile for new posts, verifies real GitHub links, sends Telegram approval messages, and can publish approved updates to X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbrokng](https://clawhub.ai/user/gbrokng)

### License/Terms of Use:

MIT-0

## Use Case:

External social media operators can use this skill to monitor Tom Doerr's X.com posts, identify real GitHub repository links, draft Portuguese-language updates, request Telegram approval, and publish approved posts to X.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring monitoring may run on an hourly schedule and continue after installation.

Mitigation: Confirm the intended schedule before enabling the skill and document how to remove or disable the cron job.

Risk: The skill can send messages to a hardcoded Telegram recipient and may post to X through an existing browser session.

Mitigation: Verify the Telegram destination, active X account, approval process, and final message text before any automated delivery.

Risk: Social posts may include incorrect or truncated GitHub links if link verification is skipped.

Mitigation: Follow the artifact's link validation workflow by resolving t.co redirects or confirming the repository directly on GitHub before posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gbrokng/skills/twitterbrowserpost)
- [Tom Doerr X profile](https://x.com/tom_doerr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and drafted social post text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use browser automation and Telegram/X delivery after approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
