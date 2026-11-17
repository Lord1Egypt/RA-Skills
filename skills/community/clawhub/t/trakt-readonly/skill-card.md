## Description:

Read-only Trakt.tv skill for checking a user's currently watching item, recent episode history, watched shows list, stats, profile, and OAuth-backed playback progress using the Trakt API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisooki](https://clawhub.ai/user/dennisooki)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent retrieve read-only Trakt.tv activity, profile, stats, and playback-progress information for a configured Trakt account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth device-token helper can print account tokens into normal output.

Mitigation: Avoid the device-token command unless token output is redacted or stored through a secure secret mechanism; rotate any Trakt tokens that may have been printed into logs or transcripts.

Risk: The security verdict is suspicious because the OAuth path needs review before installation.

Mitigation: Review the OAuth flow before installing or enabling playback access; basic read-only commands using TRAKT_CLIENT_ID and TRAKT_USERNAME are lower impact.

## Reference(s):

- [Trakt API Quick Reference](references/trakt-api.md)
- [ClawHub Skill Page](https://clawhub.ai/dennisooki/skills/trakt-readonly)
- [Trakt API](https://api.trakt.tv)
- [Trakt OAuth Applications](https://trakt.tv/oauth/applications)
- [Trakt Device Activation](https://trakt.tv/activate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and text or JSON command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, TRAKT_CLIENT_ID, and TRAKT_USERNAME; OAuth playback and device-token commands require additional Trakt secrets.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
