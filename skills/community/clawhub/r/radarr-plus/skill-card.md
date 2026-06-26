## Description: <br>
Add and manage movies in a Radarr instance via its HTTP API, including movie lookup, quality profile and root folder listing, movie adds by title/year or TMDB id, and search triggering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalchaudhary](https://clawhub.ai/user/vishalchaudhary) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and operators use this skill to request movies from chat and add them to a configured Radarr instance, with optional poster, trailer, rating, Plex-link, and progress notification support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted chat users could request movies through the connected Radarr setup. <br>
Mitigation: Restrict use to trusted OpenClaw users and enforce group-chat allowlists before deployment. <br>
Risk: Radarr, Plex, TMDB, and OMDb credentials are required or optionally used by the skill. <br>
Mitigation: Store credentials only in the configured environment file, keep them private, and avoid committing secrets. <br>
Risk: Tracking and outbox state can include chat targets and movie request details. <br>
Mitigation: Protect the workspace state/radarr directory with appropriate filesystem permissions and retention practices. <br>
Risk: Poster downloads fetch remote assets when the optional rich movie-card flow is enabled. <br>
Mitigation: Harden or disable fetch_asset.py unless poster downloads are needed. <br>


## Reference(s): <br>
- [Radarr+ ClawHub release](https://clawhub.ai/vishalchaudhary/radarr-plus) <br>
- [Onboarding](references/onboarding.md) <br>
- [Setup and configuration](references/setup.md) <br>
- [Radarr API quick notes](references/radarr-api-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, API calls, files, guidance] <br>
**Output Format:** [Chat-facing Markdown and text, shell commands, JSON command output, and state/outbox JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Radarr API credentials from environment variables; optional TMDB, OMDb, and Plex credentials enable richer movie cards and Plex links.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
