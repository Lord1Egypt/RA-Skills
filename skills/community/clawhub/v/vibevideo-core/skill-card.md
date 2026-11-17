## Description:

Log into bollo.video or vibevideo.io, list Studio projects with web links, create a Studio episode from a script with style, aspect-ratio, and project selection, and log out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vibevideo](https://clawhub.ai/user/vibevideo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate VibeVideo Studio from an agent workflow: authenticate to bollo.video or vibevideo.io, list Studio projects, and create AI video episodes from prompts or scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI handles account login workflow data and sends scripts to bollo.video or vibevideo.io.

Mitigation: Use it only when the user accepts that data transfer; prefer the default HTTPS endpoints and use --no-save for ephemeral login when appropriate.

Risk: Custom --api-base or --web-base values can direct account workflow data to untrusted origins.

Mitigation: Use the default bollo.video or vibevideo.io origins; a safer release should enforce HTTPS allowlisted origins.

Risk: Custom --session-file paths can overwrite or delete unintended local files.

Mitigation: Use the default OpenClaw secrets path and avoid custom session-file paths until session files are restricted to the intended secrets directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vibevideo/skills/vibevideo-core)
- [VibeVideo Studio](https://vibevideo.io)
- [Bollo Studio](https://bollo.video)
- [Architecture reference](references/architecture.md)
- [Provider integration checklist](references/provider-integration-checklist.md)
- [Current system map](references/current-system-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI JSON or text results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns project links, episode URLs, video IDs, and error context when available.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
