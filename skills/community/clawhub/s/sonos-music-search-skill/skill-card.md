## Description:

Search for music via Brave Search and play it on Sonos speakers. Supports play, current track, and speaker discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Spotify tracks through Brave Search, play matches on local Sonos speakers, inspect the current track, and discover available speakers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable npm install guidance and unpinned dependencies may install code that differs from the reviewed artifact.

Mitigation: Install an exact reviewed package version with a lockfile where possible and review dependency updates before deployment.

Risk: The Brave Search credential is required for operation.

Mitigation: Scope BRAVE_API_KEY to this skill and avoid sharing it with unrelated tools or environments.

Risk: Speaker discovery can expose local Sonos device names and IP addresses.

Mitigation: Use the skill only on trusted networks and avoid publishing speaker inventory output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/sonos-music-search-skill)
- [ClawHub homepage listing](https://clawhub.com/skills/sonos-music-search-skill)
- [Brave Search API](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration, Guidance]

**Output Format:** [CLI text output and JavaScript API return objects, with Markdown usage guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRAVE_API_KEY, Node.js 18 or later, and a Sonos speaker on the same local network.]

## Skill Version(s):

1.1.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
