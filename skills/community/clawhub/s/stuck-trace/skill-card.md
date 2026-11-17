## Description:

Stuck Trace helps an agent analyze project, collaboration, or decision blockers by reading available profile, memory, and recent conversation context, then producing a structured root-cause trace without making decisions for the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheyuy](https://clawhub.ai/user/sheyuy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill when a real project, collaboration, or decision process feels blocked and they want a concise structure of root-cause chains, decision forks, available paths, and reflective takeaways. It is intended for workspace agents that may have access to profile files, memory archives, and recent conversation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access broad profile, memory, and recent conversation data while analyzing blockers.

Mitigation: Approve the exact files and history sources before use, and exclude private logs or sensitive medical, financial, identity, and relationship records from accessible workspace context.

Risk: Outputs could overstate patterns if memory records are sparse or incomplete.

Mitigation: Use the skill's lower-depth mode when archives are missing, and treat cross-time patterns as observations requiring user review rather than facts.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/Sheyuy/agent-skills/tree/main/skills/stuck-trace)
- [Botlearn homepage](https://www.botlearn.ai)
- [ClawHub skill page](https://clawhub.ai/sheyuy/skills/stuck-trace)
- [Publisher profile](https://clawhub.ai/user/sheyuy)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown-style structured text with labeled sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by available context: a minimal four-section trace with no archive, or deeper sections when profile, memory, and recent conversation data are available.]

## Skill Version(s):

0.1.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
