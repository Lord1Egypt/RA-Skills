## Description:

Monitor RSS feeds and send notifications when new content is published.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwd815813](https://clawhub.ai/user/lwd815813)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add RSS, Atom, or JSON feed URLs to a local watchlist, check feeds for new content, and optionally send update summaries to Feishu/Lark or schedule recurring checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured feed URLs and detected article history are stored locally under ~/.rss_monitor.

Mitigation: Use non-sensitive feed URLs where possible and protect or periodically clear the local ~/.rss_monitor data directory according to the deployment environment's data-handling requirements.

Risk: Scheduled checks fetch every configured feed from the host where the skill runs.

Mitigation: Add only trusted feed URLs and enable cron only on machines where those outbound requests are acceptable.

Risk: When FEISHU_WEBHOOK is set, update text can be sent to Feishu/Lark.

Mitigation: Configure the webhook only for intended destinations and avoid feeds whose titles or summaries contain sensitive internal information.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-line instructions and status text; the runtime script stores feed and history JSON under ~/.rss_monitor.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
