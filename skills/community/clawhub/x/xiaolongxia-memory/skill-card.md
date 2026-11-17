## Description:

Xiaolongxia Memory Manager helps agents set up a dual-track memory workflow using daily journals and a curated MEMORY.md file for session continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lg-haha](https://clawhub.ai/user/lg-haha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure persistent memory for AI assistants, including daily journals, long-term memory extraction, session-start context loading, and periodic maintenance. It is suited for OpenClaw and other agent platforms that can follow Markdown-based operating instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workspace memory can store broad user and project details across sessions without clear opt-in.

Mitigation: Require explicit opt-in before enabling memory, keep memory files out of source control, and avoid storing secrets or regulated personal data.

Risk: Long-term memory and daily journals can retain stale or unnecessary information.

Mitigation: Review stored entries regularly and define a clear process to delete or disable MEMORY.md and daily journals.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lg-haha/skills/xiaolongxia-memory)
- [Memory extraction examples](references/提炼示例.md)
- [MEMORY.md template](references/记忆模板.md)
- [General memory prompt template](references/通用prompt模板.md)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory file structures, prompt snippets, and maintenance guidance for persistent workspace memory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
