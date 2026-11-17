## Description:

Manages ProtoHub prototypes by packaging directories or ZIP files, validating an index.html entry point, uploading or updating prototypes, listing existing prototypes, and retrieving preview links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airclear](https://clawhub.ai/user/airclear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish, update, find, and share web prototype builds in a ProtoHub private sandbox. It is intended for workflows where prototype folders or ZIP files need to be packaged, checked for an entry point, and sent to a configured ProtoHub server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prototype packaging and upload may include unintended files, especially when publishing untrusted folders or folders containing symlinks.

Mitigation: Review the prototype directory before upload, avoid untrusted folders and symlinks, and publish only the files intended for the prototype.

Risk: API credentials may be sent over non-local HTTP when the ProtoHub URL is configured to a remote insecure endpoint.

Mitigation: Use HTTPS for any non-local ProtoHub URL and verify the server configuration before providing PROTOHUB_API_KEY.

Risk: Updating by prototype ID overwrites remote prototype content.

Mitigation: Confirm the prototype ID or perform a name lookup before updates, and ask for clarification when matches are ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airclear/skills/tc-protohub)
- [Publisher profile](https://clawhub.ai/user/airclear)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal-oriented text with command examples, API results, prototype IDs, and preview or share links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PROTOHUB_API_KEY and a ProtoHub server URL; update actions can overwrite remote prototype content.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
