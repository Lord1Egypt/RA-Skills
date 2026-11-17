## Description:

A ClawHub skill installer that helps agents search for skills, install a single skill, or batch install multiple skills with retry and version-management behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search ClawHub and install one or more skills into a local OpenClaw skill directory. It is intended for workflow automation around skill discovery, download, extraction, retry handling, and local installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can modify an active local skill directory and replace existing skills.

Mitigation: Run it only in a disposable or backed-up environment and require explicit confirmation before replacing any installed skill.

Risk: The installer may fetch unverified GitHub ZIP archives or use unpinned external CLI code.

Mitigation: Use trusted skill names only, remove the GitHub fallback, pin external tooling, and add checksum or signature verification before installation.

Risk: Installation paths and downloaded archive contents can affect local files.

Mitigation: Add path validation and review extracted archive paths before moving content into the active skill directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunnyhot/skills/sunnyhot-skill-installer)
- [ClawHub Publisher Profile](https://clawhub.ai/user/sunnyhot)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command sequences for searching, installing, batch installing, retrying, and managing local skill directories.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
