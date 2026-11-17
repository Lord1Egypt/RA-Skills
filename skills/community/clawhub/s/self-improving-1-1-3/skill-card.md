## Description:

Self-reflection + Self-criticism + learning from corrections. Agent evaluates its own work, catches mistakes, and improves permanently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help an agent learn from explicit corrections, self-reflection, and repeated preferences across sessions while keeping memory in local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to save and reuse corrections, preferences, and some project context across sessions without a clear first-use consent step.

Mitigation: Use strict or passive mode, avoid storing secrets or sensitive personal and third-party information, and review deletion and export behavior before relying on memory controls.

Risk: Local memory files under ~/self-improving/ may contain user preferences, corrections, or project context that affect future agent behavior.

Mitigation: Audit memory on demand, require visible source tracking for learned items, and confirm removals when users ask the agent to forget information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sieyer/skills/self-improving-1-1-3)
- [Publisher profile](https://clawhub.ai/user/sieyer)
- [Skill homepage](https://clawic.com/skills/self-improving)
- [Security boundaries](artifact/boundaries.md)
- [Learning mechanics](artifact/learning.md)
- [Memory operations](artifact/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, read, update, export, or delete local memory files under ~/self-improving/ when the agent follows the skill.]

## Skill Version(s):

1.1.3 (source: artifact/SKILL.md frontmatter); ClawHub release 1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
