## Description:

Search for music via Brave Search and play it on your Sonos speakers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Sonos users can use this skill to search for Spotify tracks through Brave Search and play the first matching result on a named Sonos speaker. It also supports checking the currently playing track from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Music searches are sent to Brave Search and may expose user intent or listening preferences to an external service.

Mitigation: Install only where that disclosure is acceptable, protect the Brave API key, and avoid submitting sensitive search terms.

Risk: The skill discovers and controls Sonos speakers on the local network.

Mitigation: Run it only on trusted networks and confirm the target speaker name before issuing play commands.

Risk: Dependency and API-key handling require operational review before shared or production use.

Mitigation: Pin or update dependencies as needed and review environment-variable handling for the deployment environment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/terrycarter1985/skills/sonos-music-search)
- [ClawHub homepage metadata](https://clawhub.com/skills/sonos-music-search)
- [Brave Search API](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, BRAVE_API_KEY, network access, a local Sonos speaker, and a Spotify account linked to Sonos.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
