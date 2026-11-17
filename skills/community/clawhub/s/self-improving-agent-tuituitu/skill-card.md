## Description:

Self-improvement and learning skill that prompts an agent to capture feedback, reflect on mistakes, and update memory or instruction files with lessons learned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclekimwood](https://clawhub.ai/user/unclekimwood)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make an agent record feedback, mistakes, preferences, and improvement notes after interactions. It is intended for memory and reflection workflows that may create or modify local memory and instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent changes to memory and instruction files, which can preserve unwanted behavior changes.

Mitigation: Limit write access to a dedicated, reviewable memory area and require explicit approval for each persistent change.

Risk: Broad activation triggers can cause self-improvement behavior after ordinary feedback, mistakes, or task completion.

Mitigation: Use the skill only for deliberate feedback or mistake-review workflows, and confirm the intended update before editing files.

Risk: The artifact names AGENTS.md, SOUL.md, policy files, and shared profile memory as possible update targets.

Mitigation: Do not allow edits to those files without a separate human-reviewed workflow.

## Reference(s):

- [Self-Improvement Reference](references/improvement-tracking.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with example memory entries and file-update instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform persistent updates to memory and instruction files when permitted.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
