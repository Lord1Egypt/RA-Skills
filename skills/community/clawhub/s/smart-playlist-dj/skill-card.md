## Description:

智慧情境 DJ，自動偵測心情/天氣/時段，生成最適合當下情境的播放列表並播放。支援 Morning/Work/Exercise/Sleep 等 10 種情境模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT

## Use Case:

External users and personal automation agents use this skill on macOS to generate context-aware playlists from time, weather, mood, and activity signals, then optionally control playback in Music.app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports an unsafe AppleScript search path that can allow a crafted song title or search query to become local command execution.

Mitigation: Fix AppleScript escaping before normal use, avoid untrusted track names or search terms, and review the generated Music.app automation before running playback commands.

Risk: The server guidance notes that use requires Music.app automation and stores Music metadata in ~/.smart-playlist-dj.

Mitigation: Install only after reviewing the skill, grant macOS automation deliberately, and periodically inspect or remove the local cache and configuration files.

Risk: The server guidance notes that the configured city is sent to wttr.in for weather-aware playlist selection.

Mitigation: Use a non-sensitive city value or disable weather-aware behavior when sharing location context is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuan905/skills/smart-playlist-dj)
- [Artifact README](README.md)
- [wttr.in weather service](https://wttr.in/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON playlist or TTS output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS Music.app automation and may write playlist state, track cache, and configuration under ~/.smart-playlist-dj.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
