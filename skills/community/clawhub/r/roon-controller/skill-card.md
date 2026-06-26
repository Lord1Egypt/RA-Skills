## Description: <br>
Control Roon music player through Roon API with automatic Core discovery and zone filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puterjam](https://clawhub.ai/user/puterjam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers who run Roon can use this skill to let an agent discover a local Roon Core, select playback zones, control playback, and report current track information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a local Roon authorization token in ~/clawd/roon_config.json so it can reconnect later. <br>
Mitigation: Keep ~/clawd/roon_config.json private, consider user-only file permissions, and revoke the extension in Roon when the skill is no longer used. <br>
Risk: Installing the skill allows an agent to control playback on the user's Roon zones. <br>
Mitigation: Install it only when agent-controlled Roon playback is intended, and review available zones before issuing playback commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/puterjam/roon-controller) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Roon controller script](artifact/roon_controller.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python examples, shell commands, and JSON-like result dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Controls a local Roon player and stores connection configuration in ~/clawd/roon_config.json.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
