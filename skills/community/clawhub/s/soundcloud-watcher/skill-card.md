## Description: <br>
Monitor your SoundCloud account, track artist releases, and get notified about new followers and likes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlinds](https://clawhub.ai/user/wlinds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to connect an agent to SoundCloud, monitor account activity, track selected artists, and receive notifications for followers, likes, and new releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SoundCloud API credentials stored in a local secrets file. <br>
Mitigation: Keep `~/.openclaw/secrets/soundcloud.env` private, restrict file permissions where possible, and avoid pasting the file contents into chat or logs. <br>
Risk: Recurring cron checks can cause background account monitoring and repeated API access. <br>
Mitigation: Add the cron job only when recurring checks are desired, and tune or remove it if background monitoring is no longer needed. <br>
Risk: The skill stores local monitoring state for tracked artists and SoundCloud account activity. <br>
Mitigation: Review and remove `~/.openclaw/data/artists.json` and `~/.openclaw/data/soundcloud_tracking.json` when uninstalling or when stored monitoring state is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wlinds/soundcloud-watcher) <br>
- [Project Homepage](https://github.com/wlinds/OpenClaw-SoundCloud-Watcher) <br>
- [SoundCloud Developer Apps](https://soundcloud.com/you/apps) <br>
- [SoundCloud API](https://api.soundcloud.com) <br>
- [npm Package](https://www.npmjs.com/package/@akilles/soundcloud-watcher) <br>
- [OpenClaw Plugin Documentation](https://docs.openclaw.ai/plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text command responses with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return setup/status guidance, account monitoring summaries, artist tracking updates, and silent cron responses when there are no updates.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release, plugin manifest, package.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
