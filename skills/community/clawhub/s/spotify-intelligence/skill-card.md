## Description:

Spotify intelligence skill with Python runners for auth, playback control, recommendations, feedback loop, governance, and explainable playlist decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanazumie](https://clawhub.ai/user/kanazumie)

### License/Terms of Use:


## Use Case:

Developers and Spotify users use this skill to authenticate with Spotify, control playback, build recommendations, log feedback, and generate explainable playlist cleanup or reorganization proposals backed by local SQLite state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Spotify playback, library, and playlist permissions.

Mitigation: Review the configured scopes before use and remove unused Spotify write scopes when playback or playlist mutation is not needed.

Risk: OAuth tokens and listening/profile data are stored locally.

Mitigation: Restrict permissions on data/tokens.json and the data directory, and avoid sharing the local SQLite database or token files.

Risk: Trusted configuration controls Spotify API endpoints, scopes, and local storage paths.

Mitigation: Keep config.json trusted and unchanged unless intentionally reviewing a configuration update.

Risk: Phone-context and relationship-status features can introduce sensitive personal context into recommendations.

Mitigation: Enable those context features only when the user explicitly wants that data used.

Risk: Playlist cleanup or reorganization actions can affect user playlists.

Mitigation: Use dry runs, staged proposals, preflight checks, and explicit human confirmation before applying playlist changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kanazumie/skills/spotify-intelligence)
- [Auth](references/auth.md)
- [Config](references/config.md)
- [Read Layer](references/read-layer.md)
- [Playback Control](references/playback-control.md)
- [Recommendation Layer](references/recommendation-layer.md)
- [Feedback Loop](references/feedback-loop.md)
- [Governance and Cost Guardrails](references/governance-cost.md)
- [Status Handover 2026-02-24](references/status-handover-2026-02-24.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; scripts emit JSON, text summaries, and SQLite-backed state updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Spotify OAuth credentials, may call Spotify APIs, and may read or write local token and SQLite files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
