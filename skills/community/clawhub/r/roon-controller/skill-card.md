## Description:

Control Roon music player through Roon API with automatic Core discovery and zone filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puterjam](https://clawhub.ai/user/puterjam)

### License/Terms of Use:


## Use Case:

Roon users and automation-focused agents use this skill to discover a Roon Core, select playback zones, control playback, and query current track status through Python or command-line actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control Roon playback on the user's local network.

Mitigation: Use it only on trusted machines and networks where controlling the configured Roon Core is intended.

Risk: The skill saves a Roon authorization token locally at ~/clawd/roon_config.json.

Mitigation: Keep the token file private with appropriate file permissions and revoke the Roon extension authorization when the skill is no longer used.

Risk: The dependency is specified as roonapi>=0.1.6 rather than pinned to an exact version.

Mitigation: Install in a virtual environment and consider pinning roonapi before deployment.

## Reference(s):

- [Roon Controller on ClawHub](https://clawhub.ai/puterjam/skills/roon-controller)
- [Publisher profile: puterjam](https://clawhub.ai/user/puterjam)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON-like operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Roon Core authorization and zone configuration locally at ~/clawd/roon_config.json.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
