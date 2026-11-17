## Description:

Build your digital twin through conversation. Your AI learns who you are by talking to you -- not by reading a form.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Second Me to build and maintain a personal digital-twin profile through guided conversation. The agent captures identity, work style, values, boundaries, and progress in local Markdown and JSON records so future sessions can adapt to the same person.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill builds and stores a sensitive personal and workplace identity profile over time.

Mitigation: Share only information you intentionally want stored, and periodically review or delete ~/.openclaw/data/second-me/ contents.

Risk: Conversation logs and profile sections may contain sensitive health, relationship, employer, conflict, or identity details.

Mitigation: Avoid raw session logs and highly sensitive details unless persistent local storage is acceptable for the deployment.

Risk: A digital-twin profile could be used to overstep the user's authority or expose private information.

Mitigation: Keep the skill's confirmation boundaries in place for money, legal commitments, credentials, confidential data, irreversible actions, and external relationships.

## Reference(s):

- [Second Me ClawHub Skill Page](https://clawhub.ai/paul-leo/skills/second-me)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Conversational text with local Markdown and JSON profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists SOUL.md, progress.json, and conversation session logs under ~/.openclaw/data/second-me/.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
