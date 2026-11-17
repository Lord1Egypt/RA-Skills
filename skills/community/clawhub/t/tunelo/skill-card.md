## Description:

Expose local services and files to the internet through a public HTTPS URL for remote previews, dev-server sharing, demos, and temporary localhost access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claw-bot](https://clawhub.ai/user/claw-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to share a local service, localhost application, or prepared directory through a temporary public URL when a user needs remote access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publicly expose local files or services.

Mitigation: Use it only for content intentionally meant to be reachable from the internet, prefer `--private` for demos and APIs, and share a minimal prepared directory instead of project roots, home folders, credentials, or internal admin services.

Risk: Installation uses a remote shell script.

Mitigation: Install only after trusting the publisher and reviewing or verifying the installer separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claw-bot/skills/tunelo)
- [Tunelo installer](https://tunelo.net/install.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands for exposing HTTP ports, serving files, private access codes, local-only preview, and custom relay settings.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
