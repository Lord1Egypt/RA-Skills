## Description:

Browse, install, switch, and manage SOUL.md personality files for OpenClaw agents from the soulsearching.ai directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stirman](https://clawhub.ai/user/stirman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to browse a remote SOUL.md catalog, install selected personality files, and switch the active workspace SOUL.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote catalog entries can persistently replace agent instructions.

Mitigation: Install only catalog entries from a trusted publisher, review SOUL.md content before activation, and keep a backup of the existing SOUL.md.

Risk: Unsafe soul IDs can escape the intended storage folder.

Mitigation: Avoid unusual catalog IDs until ID validation is added, and review file paths before overwriting or deleting local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stirman/skills/soul-searching)
- [soulsearching.ai directory](https://soulsearching.ai)
- [soulsearching.ai catalog endpoint](https://soulsearching.ai/souls.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash command examples and local SOUL.md file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch and cache a remote JSON catalog, store selected Markdown files under ~/.openclaw/souls, and copy an installed file to the workspace SOUL.md.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
