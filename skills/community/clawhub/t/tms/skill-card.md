## Description: <br>
Control Telegram Media Server downloads over REST: add URLs or torrents, list status, delete downloads, and search via Prowlarr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikitadmitryuk](https://clawhub.ai/user/nikitadmitryuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let an agent manage a running Telegram Media Server instance through its REST API for media download, status, deletion, and torrent search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TMS API credentials can be exposed if pasted into chat or included in public assets. <br>
Mitigation: Keep TMS_API_KEY in per-skill or agent secret configuration and redact it from screenshots, logs, and listings. <br>
Risk: Deleting a download removes associated state and local files. <br>
Mitigation: List downloads first and confirm the exact id or title before deletion. <br>
Risk: The skill can add or remove downloads against a configured TMS instance. <br>
Mitigation: Install it only for TMS instances you control and restrict model invocation when only explicit user-requested actions should be allowed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nikitadmitryuk/tms) <br>
- [Telegram Media Server skill source](https://github.com/NikitaDmitryuk/telegram-media-server/tree/main/openclaw-skill-tms) <br>
- [Telegram Media Server README](https://github.com/NikitaDmitryuk/telegram-media-server#readme) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration guidance] <br>
**Output Format:** [Markdown guidance with REST request details and JSON request/response schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured TMS API endpoint and API key when authentication is enabled; torrent search depends on Prowlarr configuration.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release, SKILL.md frontmatter, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
