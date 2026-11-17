## Description:

Spec-Driven Development (Spex) manages the full SDLC from requirement analysis and design to incremental implementation and submission through manual /spex command routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangxin](https://clawhub.ai/user/jiangxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use spex to turn requirements into specifications, todo lists, implementation steps, review loops, merge preparation, and archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initialization may install dependencies with broad environment impact.

Mitigation: Install only in trusted repositories and prefer an isolated virtual environment or manual dependency installation.

Risk: Repository-controlled configuration and hooks can influence actions run by the skill.

Mitigation: Inspect .spex.toml and hook definitions before allowing the skill to run them.

Risk: The skill can guide broad code and git mutations during apply, review, merge, and archive workflows.

Mitigation: Review generated specs, planned actions, diffs, and commits before merge or submission.

Risk: Specs from unfamiliar repositories or pull requests can steer code-writing agents.

Mitigation: Treat external specs as untrusted input and review them before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangxin/skills/spex)
- [Server-resolved GitHub source](https://github.com/jiangxin/spex/tree/master/skills/spex)
- [Skills specification reference](references/SKILLS-SPEC.md)
- [Apply review loop reference](references/apply-review-loop.md)
- [Compact SOP style reference](references/compact-sop-style.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON metadata, shell commands, and code or configuration changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual /spex command routing can create and update spec documents, todo metadata, review records, archives, and git commits.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and pyproject.toml report 0.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
