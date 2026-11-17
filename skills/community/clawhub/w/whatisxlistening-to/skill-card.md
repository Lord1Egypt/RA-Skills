## Description:

Queries Last.fm listening data, shows now playing status, syncs scrobble history to a local database, and helps deploy a personal listening dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poiley](https://clawhub.ai/user/poiley)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to query current and historical Last.fm listening activity, generate CLI responses, and configure or deploy a personal now-playing dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says this package looks like a personal workspace rather than a scoped skill and exposes sensitive credentials.

Mitigation: Do not install or publish as-is; remove personal workspace material and secrets, split the package into scoped skills, and rotate any exposed credentials before release.

Risk: The security guidance flags broad automation, persistence, sync, auto-update, and location-tracking behavior in the package.

Mitigation: Require explicit consent, authentication, confirmations, and disablement controls for automation, tracking, sync, and update behavior.

Risk: The target skill uses Last.fm API credentials and synchronizes listening history into a local SQLite database.

Mitigation: Keep Last.fm keys in environment variables or a secrets manager, avoid publishing local databases or config files, and restrict dashboard access before exposing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/poiley/skills/whatisxlistening-to)
- [Live dashboard demo](https://whatisbenlistening.to)
- [Last.fm API account creation](https://www.last.fm/api/account/create)
- [Last.fm API endpoint](https://ws.audioscrobbler.com/2.0/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Last.fm API usage, local SQLite sync guidance, Docker commands, and Kubernetes configuration guidance.]

## Skill Version(s):

1.3.0 (source: server release metadata; pyproject.toml reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
