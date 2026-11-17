## Description:

Maintain a project's mid-term working memory in a local WORKING.md file so decisions, failed attempts, and next steps survive context compaction and future sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikotelkin](https://clawhub.ai/user/ikotelkin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve project state across long agent sessions, compaction, and new sessions. It helps maintain a concise local decision log, dead-end list, and next-step list, then promotes settled conclusions into longer-term assistant memory when a stage ends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-derived content may be persisted into WORKING.md, CLAUDE.md, or longer-term assistant memory without sufficient trust-boundary review.

Mitigation: Review diffs before committing and require explicit approval before promoting WORKING.md content into long-term memory.

Risk: Sensitive information could be written into local working-memory files and later reused by the agent.

Mitigation: Do not store secrets in WORKING.md or related memory files; remove sensitive content before checkpointing or consolidation.

## Reference(s):

- [Working Memory ClawHub skill page](https://clawhub.ai/ikotelkin/skills/working-memory)
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local WORKING.md content and optional CLAUDE.md pointer text; no API calls or credential use are indicated by the release evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
