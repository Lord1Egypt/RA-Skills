## Description:

Compilation-over-retrieval knowledge wiki for OpenClaw agents. Drop sources in, get structured cross-referenced pages out. Knowledge compounds instead of disappearing. Based on Andrej Karpathy's LLM Wiki pattern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dobrinalexandru](https://clawhub.ai/user/dobrinalexandru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to maintain an agent-managed markdown wiki from curated sources, with ingestion, querying, cross-references, and periodic linting. It is intended for persistent knowledge and memory workflows where sourced wiki pages should compound across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory writes and automated wiki maintenance can preserve incorrect or misleading content.

Mitigation: Review generated wiki pages and lint reports before relying on them, especially after automated ingest or lint runs.

Risk: Queued URL ingestion can process untrusted or unsuitable sources.

Mitigation: Add only trusted sources to the ingestion queue and keep URL fetching constrained by the runtime's safety controls.

Risk: Cron automation and optional SuperMemory sync can expand the automation and data-sharing surface.

Mitigation: Keep cron jobs and SuperMemory sync disabled until the scheduled prompts, synced data, and sharing expectations have been reviewed.

## Reference(s):

- [Karpathy's LLM Wiki Pattern](references/karpathy-llm-wiki.md)
- [Original Karpathy LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Dual-memory plugin](https://clawhub.ai/skills/dual-memory)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates wiki pages, indexes, logs, ingestion queues, setup scaffolding, and concise ingest or lint reports.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
