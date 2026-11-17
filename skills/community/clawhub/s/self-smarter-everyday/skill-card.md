## Description:

Self-Smarter Everyday helps AI agents run a nightly self-improvement routine for self-reflection, self-audit, memory compaction, prompt evolution, skill gap analysis, and improvement planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akdira](https://clawhub.ai/user/akdira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add scheduled, auditable self-improvement workflows to AI agents, including nightly reflection, metrics review, prompt iteration, memory lifecycle management, and improvement planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unattended through scheduled execution.

Mitigation: Review before installation, use --skip-cron or avoid setup until persistence is explicitly approved, and run only in an isolated account or workspace.

Risk: The skill can mutate agent state, memory, and prompt variants.

Mitigation: Use dry-run modes where available and require human review before accepting proposed prompt, memory, skill, or configuration changes.

Risk: The security summary says privacy and safety promises are inconsistent across the package.

Mitigation: Do not place secrets in its configuration or examples, and verify documentation and implementation alignment before deployment.

## Reference(s):

- [Self-Smarter-Everyday: System Architecture Deep Dive](references/architecture.md)
- [Safety Boundaries for Self-Improving AI Agents](references/safety-boundaries.md)
- [Production Deployment Patterns for Self-Improving Agents](references/production-deployment.md)
- [Memory Systems Architecture for Self-Improving Agents](references/memory-systems.md)
- [Prompt Evolution: Self-Improving Prompts for AI Agents](references/prompt-evolution.md)
- [Evaluation Frameworks for Self-Improving Agents](references/evaluation-frameworks.md)
- [Self-Reflection Framework for AI Agents](references/self-reflection.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated local Markdown or JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local state, logs, memory, prompt, audit, metric, and plan files under the configured self-smarter directory.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact changelog top entry is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
