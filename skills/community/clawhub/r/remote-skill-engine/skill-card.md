## Description:

Cache and use skills from ClawHub and GitHub as if locally installed. Stores remote skills in local cache folder for offline use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oki3505f](https://clawhub.ai/user/oki3505f)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to discover, compare, cache, and use remote agent skills from registries such as ClawHub and GitHub, including offline reuse after caching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote, mutable skill content can be cached and made to behave like a local installed skill.

Mitigation: Use only trusted sources and review the exact downloaded files before enabling cached or synced skills.

Risk: Downloads are not authenticated with strong integrity checks in the submitted implementation.

Mitigation: Avoid arbitrary direct URLs and verify source identity, hashes, or signatures out of band before installation.

## Reference(s):

- [Registry URLs](artifact/references/registry-urls.md)
- [Remote Skill Engine on ClawHub](https://clawhub.ai/oki3505f/skills/remote-skill-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local cache changes and command execution steps that should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
