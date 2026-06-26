## Description: <br>
Swarm reliability watchdog for OpenClaw - validates gateway/channel and every lane, performs bounded recovery, and emits auditable receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to check OpenClaw gateway, channel, and agent-lane health, run bounded recovery, and capture receipts for incident timelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer behavior may create recurring Telegram alerts to a fallback recipient when no Telegram default recipient is configured. <br>
Mitigation: Set an explicit Telegram default recipient or remove the fallback recipient before running setup.sh. <br>
Risk: Setup can create persistent OpenClaw cron jobs and the watchdog can restart the OpenClaw gateway. <br>
Mitigation: Review scripts/setup.sh before installation and run it only where persistent watchdog jobs and bounded gateway restarts are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tkuehnl/swarm-self-heal) <br>
- [Project homepage](https://github.com/cacheforge-ai/cacheforge-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and line-oriented watchdog receipts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Watchdog runs emit timestamp, targets, agent status fields, actions, verdict, and receipt lines.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
