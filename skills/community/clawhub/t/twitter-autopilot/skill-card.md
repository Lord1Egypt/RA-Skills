## Description: <br>
Automate Twitter/X posting, engagement, and growth for OpenClaw AI agents, including OAuth setup, tweet and thread posting, draft workflows, follows, engagement actions, and content strategy support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[persnola1-sketch](https://clawhub.ai/user/persnola1-sketch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run an OpenClaw agent's Twitter/X account, prepare approved drafts, post tweets or threads, manage engagement actions, and maintain posting logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, delete, follow, unfollow, retweet, quote, and reply from a live Twitter/X account using OAuth credentials. <br>
Mitigation: Review before installing, start with a disposable or low-risk account, keep MODE.md in DRAFT until behavior is verified, and avoid unattended cron posting. <br>
Risk: OAuth credentials grant write access to the connected account and may be exposed or overused if handled carelessly. <br>
Mitigation: Restrict token permissions where possible, store credentials only as environment variables, rotate tokens regularly, and revoke tokens after testing. <br>
Risk: Autonomous posting or queue processing can create duplicate, unwanted, or reputationally harmful public content. <br>
Mitigation: Require human approval for new accounts, check twitter/posted-log.md before posting, log every posted tweet, and confirm the script only reads and writes intended twitter/ files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/persnola1-sketch/twitter-autopilot) <br>
- [X Developer Portal](https://developer.x.com) <br>
- [Twitter Strategy Templates](references/strategy-templates.md) <br>
- [Content Strategy](references/content-strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples plus local file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Twitter/X API through tweepy when configured with OAuth credentials.] <br>

## Skill Version(s): <br>
1.3.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
