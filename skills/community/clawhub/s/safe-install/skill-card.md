## Description:

Install OpenClaw skills through policy validation, ClawShield scanning, snapshot storage, and rollback controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Safe Install to add a local review gate before activating OpenClaw skills. It supports policy checks, ClawShield scanning, install history, rollback-ready snapshots, and rollback for locally managed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is a user-directed security installer, but the server security summary says its advertised policy protections have implementation gaps.

Mitigation: Treat it as an additional local review layer, not a hardened security boundary, and install only from trusted local skill sources.

Risk: Server security guidance warns that blockedPatterns and allowedSources should not be treated as non-bypassable controls.

Mitigation: Keep policies narrow, review candidate skills manually, and require explicit approval for caution or avoid scan results.

Risk: Server security guidance calls out symlink review until implementation gaps are fixed.

Mitigation: Inspect candidate skill directories for symlinks before installation or rollback, especially when sources are not fully trusted.

Risk: Using --force can deliberately override Avoid-level scan decisions.

Mitigation: Reserve --force for controlled testing or exceptional cases where the source and behavior have already been reviewed.

## Reference(s):

- [ClawHub Safe Install Page](https://clawhub.ai/mike007jd/skills/safe-install)
- [Publisher Profile](https://clawhub.ai/user/mike007jd)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Project Homepage](https://github.com/mike007jd/openclaw-skills/tree/main/safe-install)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON policy snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI workflows can emit table or JSON responses and write snapshots, active state, history, and policy files under the configured local store.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
