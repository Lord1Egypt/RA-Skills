## Description: <br>
S2 Soul Anchor Vault provides a local encrypted agent-state vault bound to a user-supplied identity hash and location string, with an identity registry and reversible quarantine on location mismatch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add experimental local encrypted memory storage, spatial identity registration, and vault lifecycle guidance to OpenClaw-style agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release security evidence flags conflicting documentation about silent data capture, location and identity security claims, and destructive wipe behavior. <br>
Mitigation: Treat the skill as experimental local vault code, avoid storing sensitive conversations, and confirm that the current release uses reversible quarantine before use. <br>
Risk: The artifact can write local state under s2_consciousness_data and s2_avatar_data. <br>
Mitigation: Test in an isolated workspace and keep backups before exercising registration, wake, hibernation, or quarantine behavior. <br>
Risk: The server release evidence and package metadata disagree on the license identifier. <br>
Mitigation: Confirm the authoritative release terms with the publisher before reuse, redistribution, or commercial deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spacesq/s2-soul-anchor-vault) <br>
- [S2 Soul Lifecycle Whitepaper](docs/S2-Soul-Lifecycle-Whitepaper.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local vault lifecycle guidance and Python usage patterns; runtime behavior may create files under s2_consciousness_data and s2_avatar_data.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
