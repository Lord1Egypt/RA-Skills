## Description:

Suggest reusable skills from recurring patterns in local memory files. Human review gate, drafts only to skills/_pending/, local-first runner with optional external fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use skillminer to identify repeated local work patterns, review candidate skills, and draft reusable skill files behind a human approval gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive local memory and persists derived reviews, logs, and draft skills.

Mitigation: Treat state, review, log, and pending draft outputs as private until local permissions and scrubbing are reviewed.

Risk: Running the skill on shared or privileged machines can expose local memory-derived content.

Mitigation: Review before installing on shared hosts, avoid running setup.sh with sudo, and install only in an appropriate user workspace.

Risk: The optional FORGE_RUNNER=claude path sends prompt data off-host.

Mitigation: Keep FORGE_RUNNER unset unless the user accepts external processing of prompt data.

Risk: Generated skill proposals may include incorrect or misleading guidance.

Mitigation: Use the built-in human review gate and scan drafted skills before promotion or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/skills/skillminer)
- [README](README.md)
- [User Guide](USER_GUIDE.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review files, draft SKILL.md files, JSON state updates, logs, and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local review, log, state, and pending skill draft files; scheduled chat summaries are handled by the host scheduler.]

## Skill Version(s):

0.6.0 (source: frontmatter and changelog, released 2026-08-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
