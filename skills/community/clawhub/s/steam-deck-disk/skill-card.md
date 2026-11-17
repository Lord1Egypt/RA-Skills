## Description:

Steam Deck Disk helps agents inspect Steam Deck partition usage, clean logs and caches, find large files, and guide moving non-system data to the /home partition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jy00801119](https://clawhub.ai/user/jy00801119)

### License/Terms of Use:

MIT-0

## Use Case:

External users and Steam Deck operators use this skill to assess disk pressure on /, /var, and /home, review cleanup options, and receive shell commands or maintenance guidance for reclaiming space. It also supports advanced /var expansion planning when routine cleanup is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended broad deletion commands and cache cleanup can remove data that a user still needs.

Mitigation: Review every cleanup command before execution, avoid blanket rm -rf use, and confirm important data is backed up or excluded.

Risk: Privileged /var resizing, bind mounts, and persistent system changes can affect boot behavior or application state.

Mitigation: Treat /var expansion as an advanced maintenance procedure, verify backups first, keep the device powered, and prefer official SteamOS tooling when available.

## Reference(s):

- [Steam Deck /var partition expansion guide](artifact/var-expansion-guide.md)
- [ClawHub skill page](https://clawhub.ai/jy00801119/skills/steam-deck-disk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may include destructive cleanup or privileged system maintenance steps that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
