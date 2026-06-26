## Description: <br>
Inspect Yandex Music via the MarshalX yandex-music library for search, current track lookup, liked tracks, playlists, and reusable token handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prtolem](https://clawhub.ai/user/prtolem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect and manage Yandex Music account data through deterministic helper commands. It supports search, current-track inspection, liked tracks, playlist lookup, and explicit like or unlike operations after token setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Yandex Music OAuth token and can persist it in a workspace-local config file. <br>
Mitigation: Prefer YM_TOKEN for temporary use, persist only when needed, rely on auth-where/auth-clear for visibility and cleanup, and keep token handling local. <br>
Risk: Like and unlike commands can modify the user's Yandex Music account state. <br>
Mitigation: Confirm the target track before running like or unlike, especially when resolving a free-text query to a track. <br>
Risk: Current-track lookup exposes device and session metadata when Ynison returns it. <br>
Mitigation: Treat now-playing output as account and device-sensitive data and avoid sharing it unless needed for the task. <br>
Risk: The helper does not provide reliable live playback transport control. <br>
Mitigation: Use it only for the documented search, current-track, likes, playlists, like, and unlike workflows; do not claim pause, resume, next, previous, or cross-device playback control. <br>


## Reference(s): <br>
- [Token and control notes](references/token-and-control.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local helper script and may print account, playlist, track, and token-source status information with token previews redacted.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
