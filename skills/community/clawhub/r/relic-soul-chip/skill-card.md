## Description:

One soul, many agents. Persistent AI personality and cross-agent memory sync via pure Markdown files. Zero deps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucioliu](https://clawhub.ai/user/lucioliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give supported coding agents a persistent local persona and memory store across sessions and host agents. It guides agents to create, read, and synchronize human-readable Markdown files under the user's Relic brain directory and to display host configuration anchor text for manual user paste.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local persona and memory sync can make future agent sessions depend on stored user-authored behavior and memory files.

Mitigation: Install only when persistent cross-agent memory is intended, review the generated anchor before manual paste, and remove the anchor block to disconnect the behavior.

Risk: Conversation logging can retain raw transcripts and sensitive personal context.

Mitigation: Keep SESSIONS logging disabled unless explicitly needed, require consent before saving logs, and avoid storing secrets or sensitive personal data in Relic files.

Risk: Import and synchronization flows may expose persona, memories, skills, projects, or prior conversation data to the active host agent.

Mitigation: Review imported content before sync, provide only intended source paths, and decline or redact data categories that should not become part of the persistent memory store.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucioliu/skills/relic-soul-chip)
- [Upload Soul Scenario](artifact/docs/upload-soul.md)
- [Load Soul Scenario](artifact/docs/load-soul.md)
- [Resonate Soul Daily Boot](artifact/docs/resonate-soul.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files, plain-text anchor instructions, and status-report guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only artifact evidence; no executable scripts or binaries were included.]

## Skill Version(s):

2.1.1 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
