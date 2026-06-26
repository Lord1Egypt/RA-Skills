## Description: <br>
whoami lets agents load and update a user's remotely stored identity profile so they can tailor future task work to that user's background and preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MorvanZhou](https://clawhub.ai/user/MorvanZhou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use whoami to give agents access to a shared Markdown identity profile and to save profile updates for later conversations. It supports personalization workflows where the agent needs user background, preferences, or current context before continuing the original task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can read and overwrite persistent personal profile data. <br>
Mitigation: Install only when this cross-agent profile access is intended, keep secrets and sensitive personal details out of the profile, and review profile changes before saving. <br>
Risk: The local ~/.whoamiagent credential file grants access to the remote profile service. <br>
Mitigation: Protect the credential file, verify the service endpoint and setup URL, and rotate the API key if exposure is suspected. <br>
Risk: The update --file workflow deletes the file supplied after upload. <br>
Mitigation: Use a temporary file for profile updates and avoid passing existing files that should be preserved. <br>


## Reference(s): <br>
- [Profile Format Spec](references/profile_format.md) <br>
- [whoami service](https://whoamiagent.com) <br>
- [ClawHub skill page](https://clawhub.ai/MorvanZhou/whoami) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown profile content and concise command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes a remote profile through a local Python helper; update operations overwrite the stored profile.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
