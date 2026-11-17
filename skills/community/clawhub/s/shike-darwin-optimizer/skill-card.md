## Description:

Shike Darwin Optimizer helps agents evaluate and improve installed Agent Skills through an 8-dimension rubric, test prompts, git-backed hill climbing, and human review checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjj2026](https://clawhub.ai/user/sjj2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate, iteratively improve, test, and report on Agent Skill quality. It is aimed at maintaining one or more SKILL.md files with measurable score changes and human approval before changes are kept.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to inspect and modify installed skill files.

Mitigation: Run it in a clean repository or disposable branch, use dry-run evaluation first, and review every diff before allowing writes or commits.

Risk: Generated optimization proposals may introduce incorrect or misleading instructions into a skill.

Mitigation: Require human approval at evaluation, optimization-plan, and result-review checkpoints, and keep only changes that improve measured results.

Risk: Live tests or package installation may execute in environments that contain secrets or unintended network access.

Mitigation: Sandbox live tests with no secrets or network access and verify package or ZIP sources before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sjj2026/skills/shike-darwin-optimizer)
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch)
- [skills.sh](https://skills.sh)
- [Nuwa Skill](https://github.com/alchaincyf/nuwa-skill)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks, score tables, diffs, and TSV-style result records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply edits to SKILL.md files, create test-prompts.json, record results.tsv entries, run sub-agent or dry-run evaluations, and use git commits or reverts when authorized.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
