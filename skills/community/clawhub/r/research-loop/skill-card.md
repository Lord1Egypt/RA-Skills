## Description:

Claude Code compatibility mirror for the Codex-native 10000 Mentors Research Workflow, used when running from Claude Code and needing the same source-gated research loop contract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research engineers use this skill in Claude Code to run a bounded, source-gated research loop over a target repository. It guides intake, literature refresh, advisor review, executor micro-steps, hygiene checks, handoff artifacts, and optional publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish repository changes and workflow memory with an unclear sanitization and approval boundary.

Mitigation: Use dry-run, --no-push, or local-only modes first, then inspect the full generated diff and .autonomous-research-workflow contents before allowing publication.

Risk: Workflow state, memory, handoffs, or repository analysis may contain information the user does not want published.

Mitigation: Avoid enabling persistent memory or private handoffs unless their fields are understood, and review generated workflow artifacts before sharing them.

## Reference(s):

- [Research workflow homepage](https://github.com/wd041216-bit/10000-mentors-research-workflow)
- [Submission Advisor Rubric](references/advisor-rubric.md)
- [Agent-Native Executor Output Template](references/executor-template.md)
- [Innovation Frontier Rubric](references/innovation-frontier.md)
- [Research Loop Phases](references/phases.md)
- [Protocol Hygiene Rubric](references/protocol-hygiene.md)
- [State Schema](references/state-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, JSON manifests, source-change files, and workflow state artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bounded micro-step outputs and local workflow artifacts; publication may be dry-run or local-only when requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
