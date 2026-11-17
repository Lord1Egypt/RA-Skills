## Description:

White Stone Memory helps agents maintain a local Markdown memory system across knowledge, projects, error logs, daily reviews, and task tracking while loading project memory only on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russellfei](https://clawhub.ai/user/russellfei)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to give an agent a persistent, bilingual memory structure for work habits, project-specific context, error logs, daily reviews, and subagent task tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may retain sensitive personal, project, or operational information.

Mitigation: Keep secrets and sensitive data out of memory files and review stored Markdown before sharing or indexing it.

Risk: The artifact uses both diary and daily directory naming for daily review storage.

Mitigation: Resolve the daily-review directory naming mismatch before relying on automated daily review workflows.

Risk: Optional Gemini-based vector search can send memory text to an external embedding provider.

Mitigation: Enable Gemini vector search only when that data flow is acceptable, or use a local Ollama embedding setup instead.

## Reference(s):

- [White Stone Memory Skill Documentation](artifact/SKILL.md)
- [White Stone Memory README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/russellfei/skills/white-stone-mem)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Markdown memory entries and optional vector-search setup guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
