## Description:

Organizes Tencent IMA source material into linked wiki guides, with folder and tag management and knowledge-base health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cookfish1979](https://clawhub.ai/user/cookfish1979)

### License/Terms of Use:

MIT-0

## Use Case:

IMA knowledge-base users and teams use this skill to compile source documents into linked topic guides, organize folders and tags, update guides, and identify structural or stale-content issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Organizing a knowledge base can change remote notes, folders, and tags.

Mitigation: Start with a test or noncritical knowledge base and approve proposed moves, tag changes, and cascade updates before execution.

Risk: IMA API credentials could be exposed through shared logs, repositories, or transcripts.

Mitigation: Keep API keys out of shared logs, repositories, and transcripts.

Risk: Moving knowledge may clear its tags.

Mitigation: Back up existing tags before moving items and verify or restore tags afterward.

## Reference(s):

- [ClawHub release](https://clawhub.ai/cookfish1979/skills/wiki-compiler)
- [Tencent IMA agent interface](https://ima.qq.com/agent-interface)
- [Ingest and guide updates](references/ingest.md)
- [Knowledge-base health checks](references/lint.md)
- [Guide schema](references/schema.md)
- [Safety guidance](references/security.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown wiki guides, lint reports, and organization plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update remote IMA notes, folders, and tags.]

## Skill Version(s):

5.0.2 (source: ClawHub release; SKILL.md frontmatter lists 5.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
