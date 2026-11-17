## Description:

Create new skills, modify and improve existing skills, run evaluations and benchmarks, and optimize skill descriptions for triggering accuracy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shimmernight](https://clawhub.ai/user/shimmernight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create, revise, evaluate, benchmark, and package agent skills while incorporating human feedback. It supports both drafting new skills and improving existing skills through qualitative review, quantitative checks, and trigger-description optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local review viewer and packager can expose, corrupt, or unexpectedly affect local data when pointed at untrusted skill outputs or directories.

Mitigation: Use the viewer and packager only with trusted workspaces, review generated files before opening them, and avoid untrusted skill directories until the reported viewer and packaging issues are fixed.

Risk: Evaluation and description-optimization workflows can run subprocesses and local commands, including Claude CLI-based checks.

Mitigation: Run evaluations in an isolated workspace, inspect prompts and scripts before execution, and avoid granting access to sensitive directories.

Risk: The review viewer may launch a localhost server and has reported feedback authorization and automatic port-kill concerns.

Mitigation: Prefer static review output for untrusted material, or use an explicit unused port and verify no important local service is listening there.

Risk: Packaged skill archives may include unexpected content when packaging untrusted or poorly reviewed directories.

Mitigation: Inspect the source directory and generated archive contents before distribution or installation.

## Reference(s):

- [Skill Creator schemas](artifact/references/schemas.md)
- [ClawHub release page](https://clawhub.ai/shimmernight/skills/skill-creator-latest)
- [Publisher profile](https://clawhub.ai/user/shimmernight)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON snippets, shell command blocks, generated skill files, evaluation reports, HTML review pages, and packaged skill archives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify files in a skill workspace and may launch local evaluation or review workflows when used.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
