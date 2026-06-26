## Description: <br>
面向中文用户的 Sonos 音乐点播技能，支持通过 Sonos 侧搜索加队列起播的方式播放已绑定音乐服务，当前已验证兼容网易云音乐和 QQ音乐，并通过 SoCo 保留 Sonos App 中的标题、歌手、专辑和封面等 metadata。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huacius](https://clawhub.ai/user/huacius) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users and automation agents use this skill to set up and operate Sonos music playback through linked NetEase Cloud Music or QQ Music services while preserving Sonos queue metadata. <br>

### Deployment Geography for Use: <br>
Global, subject to Sonos and linked music-service regional availability. <br>

## Known Risks and Mitigations: <br>
Risk: Local setup creates a Python virtual environment and installs soco from Python packaging sources. <br>
Mitigation: Install only in trusted environments and review the bootstrap output before relying on the playback setup. <br>
Risk: Playback depends on the local sonos CLI and separate workspace wrapper/Python files that this package checks for but does not include. <br>
Mitigation: Trust and inspect the local sonos CLI plus sonos_netease_play and sonos_qq_play files before playback. <br>
Risk: Playback can fail if Sonos devices are not reachable or the linked music-service authorization is stale or unavailable in the user's region. <br>
Mitigation: Verify local network access and reauthorize the target music service in the Sonos App before troubleshooting the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huacius/sonos-music-playback) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local sonos CLI, reachable Sonos devices, linked music services, and workspace playback wrappers for NetEase Cloud Music and QQ Music.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
