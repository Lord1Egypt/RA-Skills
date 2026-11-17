## Description:

Inspect Yandex Music via the MarshalX yandex-music library for search, current track lookup, liked tracks, playlists, and reusable token handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prtolem](https://clawhub.ai/user/prtolem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to inspect a Yandex Music account, search catalog content, view current playback state, list liked tracks and playlists, and make explicit like or unlike changes through a bundled helper script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper stores and forwards a reusable Yandex Music account token.

Mitigation: Prefer a temporary YM_TOKEN for one-off use, avoid passing tokens directly on the command line, and clear or replace saved tokens when they are no longer needed.

Risk: The helper can modify the user's liked tracks.

Mitigation: Use like and unlike commands only after explicit user confirmation and review the reported track before treating the action as intended.

Risk: Routine use depends on redirect-host handling and unpinned dependencies that the security guidance calls out for review.

Mitigation: Review or fix redirect-host validation and dependency pinning before routine or sensitive use.

## Reference(s):

- [Token and control notes](references/token-and-control.md)
- [ClawHub skill page](https://clawhub.ai/prtolem/skills/yandex-music)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read account state and may modify liked tracks when the user explicitly requests like or unlike actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
