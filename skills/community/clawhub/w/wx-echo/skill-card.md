## Description: <br>
Wx Echo helps an agent extract WeChat todos, calendar items, and group-chat highlights, then post selected results to Discord Forum and Apple Calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lihanghang](https://clawhub.ai/user/lihanghang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users who run WeChat Desktop use this skill to monitor selected local chats, turn messages into follow-up tasks, calendar events, and daily digests, and publish those outputs to Discord Forum threads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill decrypts and scans private WeChat databases and stores sensitive keys, decrypted databases, and message data locally. <br>
Mitigation: Keep all_keys.json, collector.db, decrypted databases, and config files private, and restrict monitored chats before enabling recurring scans. <br>
Risk: Selected chat-derived content can be published to Discord Forum threads or Apple Calendar. <br>
Mitigation: Review monitored chats and generated posts or events before enabling cron tasks, and remove scheduled tasks when the skill is no longer in use. <br>
Risk: Setup can require sudo process-memory inspection and includes optional sshpass or raw curl token fallbacks. <br>
Mitigation: Run only on a trusted machine, avoid sshpass and raw curl token fallbacks where possible, and keep Discord and SSH credentials out of shared files. <br>


## Reference(s): <br>
- [Wx Echo ClawHub page](https://clawhub.ai/lihanghang/wx-echo) <br>
- [README](README.md) <br>
- [Skill setup guide](SKILL.md) <br>
- [Configuration example](config.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, YAML configuration, JSON extraction output, Discord Forum posts, and Apple Calendar events] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recurring cron prompts can refresh decrypted WeChat data, sync local collector state, and post only when new tasks, events, or digest items are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
