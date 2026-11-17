## Description:

Willhaben CLI for searching Austria's largest classifieds marketplace. Search listings, view details, check seller profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pasogott](https://clawhub.ai/user/pasogott)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search Willhaben listings, inspect listing details, and check seller profiles from an agent-assisted command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and invokes a third-party CLI from the pasogott distribution channel.

Mitigation: Install only if you trust the publisher and channel; review or pin the upstream repository or release before source installation, and avoid elevated privileges unless necessary.

Risk: The artifact documents that the show command has a bug and that location filtering may include nearby regions.

Mitigation: Verify important listing details and location-sensitive results on willhaben.at before acting on them.

## Reference(s):

- [Willhaben CLI Repository](https://github.com/pasogott/whcli)
- [Willhaben CLI Issues](https://github.com/pasogott/whcli/issues)
- [Willhaben Homebrew Tap](https://github.com/pasogott/homebrew-tap)
- [willhaben.at](https://willhaben.at)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may request table, JSON, or CSV output from whcli.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
