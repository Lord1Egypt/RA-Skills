## Description:

A persistent memory system for AI agents that saves only meaningful wisdom, goals, mistakes, and preferences, with optional automatic learning from interaction outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m7madash](https://clawhub.ai/user/m7madash)

### License/Terms of Use:


## Use Case:

External developers and agent users use this skill to give an agent a curated file-backed memory workflow for retaining durable preferences, goals, mistakes, and lessons across interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled memory files may contain behavior-shaping notes that affect future agent responses.

Mitigation: Review and clear the memory files before enabling the skill in a new workspace.

Risk: Automatic learning can preserve incorrect, stale, or sensitive lessons across sessions.

Mitigation: Require explicit approval for durable memory writes and provide a regular review path to inspect, edit, expire, or delete stored memories.

Risk: Shared or sensitive workspaces can expose remembered preferences, goals, or lessons to unintended users or tasks.

Mitigation: Use the skill only in controlled workspaces with appropriate access controls and memory hygiene procedures.

## Reference(s):

- [Selective Memory ClawHub release](https://clawhub.ai/m7madash/skills/selective-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and pseudocode examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recommendations for reading and updating local memory files; durable writes should be reviewed before use.]

## Skill Version(s):

2.0.0 (source: server release evidence and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
