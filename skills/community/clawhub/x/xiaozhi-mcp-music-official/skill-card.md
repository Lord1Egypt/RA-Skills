## Description:

Xiaozhi Mcp Music Official lets a XiaoZhi MCP setup search online music, return track information, and play direct audio links through a local player such as mpv.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe12801](https://clawhub.ai/user/joe12801)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and XiaoZhi operators use this skill to connect a XiaoZhi MCP endpoint to online music search and local playback controls. It supports song search, fallback across music sources, track information responses, and basic play, pause, resume, and stop workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote MCP-invoked tools can stop, pause, or resume processes that match the configured player command.

Mitigation: Use only a trusted XiaoZhi MCP endpoint and a trusted, fixed PLAYER_CMD; prefer a version that tracks and signals only the player process it starts.

Risk: Music searches and the MUSIC_API_KEY are sent to third-party music APIs.

Mitigation: Use a trusted API provider and key, and disclose this data flow to users before deployment.

Risk: Dependency versions are broad ranges rather than reviewed fixed versions.

Mitigation: Pin reviewed dependency versions before operational deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joe12801/skills/xiaozhi-mcp-music-official)
- [Kuwo music API endpoint](https://api-v2.yuafeng.cn/API/kwmusic.php)
- [NetEase music API endpoint](https://api-v2.yuafeng.cn/API/wymusic.php)
- [Migu music API endpoint](https://api-v2.yuafeng.cn/API/mgmusic.php)
- [Baidu music API endpoint](https://api-v2.yuafeng.cn/API/bdmusic.php)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text MCP tool responses with local playback side effects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured XiaoZhi MCP endpoint, music API key, music source, and trusted local player command.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
