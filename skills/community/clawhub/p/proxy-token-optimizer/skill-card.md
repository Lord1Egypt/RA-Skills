## Description:

Optimizes LLM token usage and API costs for the openclaw-manager proxy platform through model-tier routing, heartbeat cost reduction, context lazy loading, and usage analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyhit2005](https://clawhub.ai/user/whyhit2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform operators use this skill to reduce LLM proxy costs by selecting cheaper capable models, generating heartbeat configuration patches, recommending leaner context loading, and analyzing PostgreSQL-backed usage and quota data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated optimization guidance or AGENTS.md.optimized content could be inappropriate for a specific deployment if applied without review.

Mitigation: Review generated AGENTS.md.optimized and configuration patches before replacing project files or changing runtime settings.

Risk: Database-backed report and advisor commands read instance usage and quota data.

Mitigation: Run platform-side analytics only in environments where access to usage_records, instance metadata, and quota data is authorized and appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whyhit2005/skills/proxy-token-optimizer)
- [ClawHub publisher profile](https://clawhub.ai/user/whyhit2005)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON command output, and generated configuration snippets or AGENTS.md.optimized files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some platform-side outputs depend on PostgreSQL usage_records and quota data from an openclaw-manager environment.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
