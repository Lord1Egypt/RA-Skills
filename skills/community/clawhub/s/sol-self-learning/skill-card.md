## Description:

Persistent memory and self-improvement for AI agents - writes and refines its own memory files over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give OpenClaw agents local failure logging, pattern analysis, and reusable prevention rules after task failures or user corrections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs can retain failure details, command context, stack traces, user corrections, and preference changes across sessions.

Mitigation: Review and protect ~/.openclaw learning files, avoid logging secrets or tokens, and periodically remove stale or sensitive entries.

Risk: The wrapper can execute local commands supplied through its command argument and record their output when failures occur.

Mitigation: Run only trusted commands, keep command execution under normal workspace permissions, and review command strings before invoking the wrapper.

Risk: Automatic learning, cron, or auto-fix workflows may mark similar failures as fixed or add prevention rules without enough human review.

Mitigation: Use learn and auto-fix modes only after reviewing the generated pattern analysis and require human approval before enabling scheduled fix-all workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amrree/skills/sol-self-learning)
- [OpenClaw Docs](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and local JSON memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local learning records under ~/.openclaw and may emit command output, failure IDs, analysis reports, and fix summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
