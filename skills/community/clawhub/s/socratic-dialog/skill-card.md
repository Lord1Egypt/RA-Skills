## Description:

Socratic Dialogue helps agents handle high-stakes or ambiguous reasoning by anchoring operational definitions, cross-examining assumptions, and checking faithfulness before synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monikazapisek](https://clawhub.ai/user/monikazapisek)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this reasoning skill when high-stakes, ambiguous, or strategically loaded decisions require precise definitions, assumption testing, contradiction checks, and guarded synthesis. It is not intended for simple lookups, routine editing, fully specified computation, or situations where the user does not want iterative clarification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally slows direct answers and may add clarification turns for simple or urgent tasks.

Mitigation: Activate it only for high-stakes, ambiguous, or strategically loaded reasoning; use ordinary direct handling for simple lookups and tight-latency tasks.

Risk: The skill challenges assumptions and can surface contradictions, which may feel adversarial if applied outside its intended scope.

Mitigation: Frame challenges as reasoning checks, keep product, technical, budget, contractual, and operational decisions with the user, and stop when the user declines iterative clarification.

Risk: An agent may over-structure an underspecified decision without enough external facts.

Mitigation: Require operational definitions, ask the user or documented sources for missing variables, and label assumptions with explicit confidence before synthesis.

## Reference(s):

- [Socratic Dialogue ClawHub listing](https://clawhub.ai/monikazapisek/skills/socratic-dialog)
- [Methodology - Socratic Dialogue](references/methodology-socratic-dialogue.md)
- [Agent Skills open standard](https://agentskills.io)
- [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown dialogue with questions, assumptions, confidence notes, fixed parameters, and concise synthesis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reasoning-only output; the skill does not request tool, file, network, or environment access.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
