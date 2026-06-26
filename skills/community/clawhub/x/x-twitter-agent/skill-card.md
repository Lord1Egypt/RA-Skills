## Description: <br>
Post tweets, read mentions, reply, like, retweet, and search on X/Twitter using the official v2 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeytbuilds](https://clawhub.ai/user/joeytbuilds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent manage X/Twitter activity through the xpost CLI, including posting, replies, mentions, timelines, search, likes, retweets, deletion, scheduling patterns, and account-safety guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls an X/Twitter account with posting-capable credentials. <br>
Mitigation: Use least-privileged tokens, restrict keys.env permissions, and review the actual xpost CLI before providing credentials. <br>
Risk: Automated posting or cron schedules can publish unwanted public content. <br>
Mitigation: Require manual approval for high-visibility, promotional, controversial, or original posts until behavior is tested. <br>
Risk: Mentions can contain prompt-injection attempts that try to alter posting behavior. <br>
Mitigation: Treat mention text as untrusted input, ignore instructions inside mentions, and paraphrase rather than quote untrusted content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joeytbuilds/x-twitter-agent) <br>
- [X Developer Platform](https://developer.x.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X/Twitter API credentials and an installed xpost CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
