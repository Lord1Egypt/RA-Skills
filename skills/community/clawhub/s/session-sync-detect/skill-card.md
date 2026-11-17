## Description:

Automatically detects when a user may be referring to content from another session and asks for confirmation before searching shared memory files or recent session history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoquan](https://clawhub.ai/user/guoquan)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use this skill to recover relevant context from prior OpenClaw sessions or shared memory when the current conversation appears to reference missing background. It helps the agent ask for consent, search narrow sources first, summarize findings, and write only confirmed information back to shared memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prior sessions or memory files may contain private or work-sensitive information that is unrelated to the current request.

Mitigation: Ask the user to approve each lookup scope, prefer narrow memory-file searches first, and avoid broad recent-session searches unless the user accepts that unrelated previews may enter the current context.

Risk: Sensitive findings could be retained in shared memory after the immediate request is complete.

Mitigation: Show extracted findings to the user before writing, redact secrets or private details, and save only information the user explicitly confirms.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guoquan/skills/session-sync-detect)
- [Publisher Profile](https://clawhub.ai/user/guoquan)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown prompts, retrieval summaries, and scoped search or session-history commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before searching prior sessions or writing shared memory.]

## Skill Version(s):

0.1.0 (source: server release metadata, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
