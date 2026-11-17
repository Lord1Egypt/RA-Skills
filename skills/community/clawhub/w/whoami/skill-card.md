## Description:

whoami lets agents load and update a remotely stored Markdown user identity profile so they can reuse the user's background, preferences, and personal context across AI tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morvanzhou](https://clawhub.ai/user/morvanzhou)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to give agents reusable personal context, retrieve a profile summary, and save updated profile details for later AI interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses personal profile data through a remote service.

Mitigation: Install only if remote profile storage is acceptable, keep the profile concise, and avoid saving secrets or sensitive personal data.

Risk: Endpoint or credential handling mistakes could expose profile data or long-lived credentials.

Mitigation: Verify the configured endpoint, do not paste long-lived API keys into chat or command-line arguments, and use only the intended one-time configuration flow.

Risk: The update workflow reads and deletes a file path supplied to the script.

Mitigation: Use update --file only with a disposable temporary file that was created specifically for the profile update.

## Reference(s):

- [whoami ClawHub skill page](https://clawhub.ai/morvanzhou/skills/whoami)
- [whoami profile format](references/profile_format.md)
- [whoamiagent service](https://whoamiagent.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown profile content with command-line status messages and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile content is intended to stay concise and within the documented 5000 character limit.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
