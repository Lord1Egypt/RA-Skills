## Description:

Create new skills, modify and improve existing skills, run evaluations, benchmark skill performance, and optimize skill descriptions for better triggering accuracy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanggd6](https://clawhub.ai/user/zhanggd6)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent authors use this skill to create, revise, evaluate, benchmark, and package agent skills through an iterative workflow. It helps define skill intent, draft skill instructions, run comparison evaluations, review feedback, and improve triggering descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with broad local development authority through file edits, shell commands, evaluation workspaces, and packaging scripts.

Mitigation: Use it only in trusted workspaces, review proposed file and command changes before execution, and keep sensitive local data outside evaluation and packaging paths.

Risk: Packaging untrusted skill directories can expose local data if symlinks are included.

Mitigation: Remove symlinks before packaging untrusted directories or fix the packager to reject or safely resolve symlinks.

Risk: The review viewer and generated reports may expose sensitive evaluation outputs or embedded script content.

Mitigation: Prefer static review output, avoid sensitive eval data in the viewer, and review generated HTML before sharing it.

## Reference(s):

- [Evaluation and benchmark schemas](artifact/references/schemas.md)
- [ClawHub Skill Creator release page](https://clawhub.ai/zhanggd6/skills/skill-creator2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, JSON files, shell commands, review reports, benchmark summaries, and optional packaged skill files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create skill files, evaluation workspaces, static HTML review pages, benchmark JSON/Markdown, and .skill packages when the user requests those workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
