## Description: <br>
Official-style XiaoZhi MCP online music bridge that lets an agent search online music, return track information, and play direct audio URLs through a local player such as mpv. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joe12801](https://clawhub.ai/user/joe12801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and XiaoZhi users use this skill to connect a XiaoZhi MCP endpoint to online music search, track information, and local playback controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured XiaoZhi MCP endpoint can direct the local music tools exposed by the bridge. <br>
Mitigation: Install only for trusted XiaoZhi MCP endpoints and run the skill with low local privileges. <br>
Risk: Playback controls may affect unrelated local processes that match the configured player command. <br>
Mitigation: Set PLAYER_CMD to a specific trusted player such as mpv and avoid running the skill where matching unrelated player processes are active. <br>
Risk: The skill depends on a third-party music API provider and its API key handling. <br>
Mitigation: Use only trusted music API providers and manage MUSIC_API_KEY as a secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joe12801/xiaozhi-mcp-music-official) <br>
- [Kuwo music API endpoint](https://api-v2.yuafeng.cn/API/kwmusic.php) <br>
- [NetEase music API endpoint](https://api-v2.yuafeng.cn/API/wymusic.php) <br>
- [Migu music API endpoint](https://api-v2.yuafeng.cn/API/mgmusic.php) <br>
- [Baidu music API endpoint](https://api-v2.yuafeng.cn/API/bdmusic.php) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text MCP tool responses with local player control side effects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MCP_ENDPOINT, MUSIC_API_KEY, MUSIC_SOURCE, and PLAYER_CMD; playback depends on a trusted local player and music API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
