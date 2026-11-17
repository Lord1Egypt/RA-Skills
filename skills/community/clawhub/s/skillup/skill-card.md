## Description:

SkillUp is a cross-platform skill publishing tool for packaging and syncing custom skills to GitHub, Xiaping Skill, OpenClaw CN, and ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjke84](https://clawhub.ai/user/cjke84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use SkillUp to validate, package, publish, status-check, install, or roll back agent skills across GitHub, Xiaping Skill, OpenClaw CN, and ClawHub. It is intended for publishing workflows that prefer command-line and API-based automation over browser-driven release steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw status workflows disable TLS certificate checking.

Mitigation: Avoid OpenClaw status or publish workflows until the TLS bypass is removed; prefer verified TLS CLI or API paths.

Risk: Publishing workflows can upload skill packages, use platform tokens, and create or update remote platform content.

Mitigation: Run check or dry-run first, scope publishing tokens narrowly, and review target platforms and configuration before publishing.

Risk: Install-local and rollback modes can replace local agent skill directories when explicitly invoked.

Mitigation: Use these modes only with trusted release assets and keep a backup or versioned source copy available before replacement.

## Reference(s):

- [ClawHub SkillUp page](https://clawhub.ai/cjke84/skills/skillup)
- [SkillUp homepage](https://github.com/cjke84/SkillUp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create packaged skill archives and publish-result JSON when invoked with result-file or default artifact settings.]

## Skill Version(s):

0.1.9 (source: frontmatter, manifest.toml, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
