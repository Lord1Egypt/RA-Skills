## Description:

Create new skills, modify and improve existing skills, and measure skill performance through drafting, evaluation, benchmarking, and description optimization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plabzzxx](https://clawhub.ai/user/plabzzxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create or improve agent skills, run evaluation loops, compare skill behavior against baselines, and package finished skills for installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review and packaging helpers can expose local data or disrupt local services when used on untrusted skills.

Mitigation: Use the skill only in trusted or isolated workspaces, review it before installation, and inspect skill folders for symlinks before packaging.

Risk: Generated review pages for untrusted outputs or eval queries may expose users to unsafe embedded content until HTML embedding is fixed.

Mitigation: Avoid opening generated review pages for untrusted skills or untrusted eval content.

Risk: The local review viewer can interfere with services already using the selected port.

Mitigation: Avoid running the viewer on ports used by other local services.

Risk: Description optimization can send skill and eval content to Anthropic's API.

Mitigation: Use description optimization only with content appropriate for the configured API provider and workspace policy.

## Reference(s):

- [Skill Creator Claude README](README.md)
- [Skill Creator Schemas](references/schemas.md)
- [Claude Code](https://claude.ai/code)
- [ClawHub Skill Page](https://clawhub.ai/plabzzxx/skills/skill-creator-claude)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON files, Python-generated reports, shell commands, and packaged skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate evaluation workspaces, benchmark artifacts, review HTML, and packaged .skill archives when the user requests those workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
