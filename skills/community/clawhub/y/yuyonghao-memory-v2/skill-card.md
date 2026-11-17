## Description:

OpenClaw Memory V2 provides vector memory, knowledge graph links, Chinese named entity extraction, and automatic memory maintenance for agent applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating OpenClaw use this skill to store, search, retrieve, delete, and maintain conversation or document memories with semantic search and entity relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive conversation or document content in vector and graph stores.

Mitigation: Set explicit retention and deletion policies before deployment, and avoid storing secrets or regulated data unless the deployment is approved for that data.

Risk: Broad get, delete, clear, and maintenance APIs can expose, modify, archive, or remove stored memories.

Mitigation: Restrict who can call memory APIs, validate memory IDs, and require authorization for destructive operations.

Risk: Automatic maintenance can compress or archive low-priority memories, and an optional summarizer LLM can become a data egress path.

Mitigation: Review maintenance behavior before enabling automation and use only approved local or data-governed LLM summarizers.

Risk: The security scan guidance calls for updating flagged dependencies before use.

Mitigation: Review and update dependencies during installation, then rerun security checks in the target environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-memory-v2)
- [SKILL.md](artifact/SKILL.md)
- [Integration Guide](artifact/INTEGRATION.md)
- [Implementation Progress](artifact/PHASE5-PROGRESS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides integration guidance and API usage patterns for a JavaScript memory system.]

## Skill Version(s):

0.1.0 (source: evidence release, artifact SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
