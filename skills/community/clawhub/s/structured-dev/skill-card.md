## Description:

Structured Dev guides coding agents through a review-first development workflow: research the codebase, write a plan, incorporate user annotations, create a task checklist, then implement while tracking progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lskun](https://clawhub.ai/user/lskun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to make agent-assisted coding more reviewable by requiring written research, a detailed plan, user annotations, and an implementation checklist before code changes begin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow creates or modifies project-local planning files under .dev/.

Mitigation: Review generated .dev/research.md and .dev/plan.md before allowing implementation, and decide whether .dev/ artifacts should be committed or ignored.

Risk: Broad trigger phrases can route normal coding requests into a document-heavy workflow.

Mitigation: Use the skill when explicit research, planning, or review gates are desired; disable or avoid it for small direct edits.

Risk: Plans or checklist items can encode incorrect assumptions if the research phase misses relevant architecture details.

Mitigation: Treat the research and plan files as review surfaces and require user approval before implementation.

## Reference(s):

- [Workflow Guide](references/workflow-guide.md)
- [Prompt Templates](references/prompt-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/lskun/skills/structured-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown planning files, checklist updates, code edits, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local .dev/research.md and .dev/plan.md files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
