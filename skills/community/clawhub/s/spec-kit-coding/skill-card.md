## Description:

Spec-kit Coding orchestrates the GitHub Spec-Kit spec-driven development workflow in OpenClaw for project setup, toolchain setup, and SDD pipeline execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staok](https://clawhub.ai/user/staok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to initialize OpenClaw projects around GitHub Spec-Kit, establish project documentation and coding standards, and move features through specification, planning, tasking, implementation, review, and testing phases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow fetches executable tooling and third-party skills from GitHub into the OpenClaw workspace.

Mitigation: Run `setup.sh --check-only` first, review the listed downloads, and proceed with installation only after accepting those remote dependencies.

Risk: The project initialization workflow can remove existing `.claude` and `CLAUDE.md` agent configuration.

Mitigation: Use a new or backed-up project directory before initialization, and avoid running the cleanup step in projects with important existing agent configuration.

Risk: `--force` can reinstall tools and overwrite downloaded skill directories.

Mitigation: Avoid `--force` unless repair or refresh is necessary, and review generated `SOURCE.md` and manifest entries after reinstalling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/staok/skills/spec-kit-coding)
- [GitHub Spec-Kit](https://github.com/github/spec-kit)
- [C++ Coding Style Guidance](CodingGuidance/CppCodingStyle.md)
- [Top-Level Coding Guidance](CodingGuidance/TopLevelCodingGuidance.md)
- [Design Pattern Guidance](CodingGuidance/DesignPattern/DesignPattern.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, file templates, and task handoff prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project files, documentation, specs, tasks, and agent handoff instructions when the workflow is followed.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
