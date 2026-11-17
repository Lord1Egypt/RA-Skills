## Description:

Self-check system with multi-dimensional critical thinking, task-decompose, quality-control, collaboration, mandatory checkpoint logging, behavior tracking, and cross-agent memory sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eita19](https://clawhub.ai/user/eita19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to impose a structured self-check workflow before task execution and delivery, including critical-thinking prompts, task decomposition, quality gates, checkpoint logging, behavior tracking, and memory sync procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires persistent behavior tracking and self-check logs that can record task summaries, inferred preferences, and confidence notes.

Mitigation: Install only where persistent logging is acceptable, and review retention, deletion, and scope controls before use.

Risk: The skill describes cross-agent memory synchronization through a Bitable relay when users ask the agent to remember information.

Mitigation: Use only with explicit user consent for memory sharing, and limit synchronized content to information the user intended to store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eita19/skills/self-check-v7)
- [Y7 Framework](https://github.com/Y7-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with checklist templates and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require persistent local logging and cross-agent memory synchronization when followed by an agent.]

## Skill Version(s):

7.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
