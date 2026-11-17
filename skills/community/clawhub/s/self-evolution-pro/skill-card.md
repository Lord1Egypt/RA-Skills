## Description:

Self Evolution Pro helps an AI agent record lessons from conversations and errors, analyze root causes, maintain a knowledge graph and evolution metrics, sync learnings across sessions, and promote repeated patterns into reusable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windy-001-crypto](https://clawhub.ai/user/windy-001-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to help an agent capture corrections, errors, and recurring patterns, then organize those learnings into persistent logs, a knowledge graph, review metrics, and reusable skill drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill asks agents to persist, promote, share, and schedule conversation-derived content with too little user control.

Mitigation: Install and use it only when persistent learning files are desired, and review the exact content before it is saved, promoted, shared, scheduled, or published.

Risk: Automatic promotion can move repeated patterns into broader agent instructions or extracted skills.

Mitigation: Require explicit approval before any promotion to AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or a reusable skill.

Risk: Cross-session history access and subagent spawning can expose or propagate conversation-derived information beyond the current session.

Mitigation: Disable or gate cross-session history access, session messaging, and subagent spawning unless the destination, scope, and content have been reviewed.

Risk: Publishing extracted skills can send generated content to ClawHub.

Mitigation: Require explicit approval after reviewing the final skill content and destination before running any ClawHub publishing command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/windy-001-crypto/skills/self-evolution-pro)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and generated or updated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may maintain persistent learning files, draft extracted skills, schedule review workflows, and publish to ClawHub when explicitly approved.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
