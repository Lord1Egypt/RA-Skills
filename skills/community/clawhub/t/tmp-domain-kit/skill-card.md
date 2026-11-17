## Description:

Tmp Domain Kit gives agents access to structured department knowledge about PLC models, coding standards, code templates, and device parameters for automation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Automation developers and engineers use this skill to ingest trusted department documents, code templates, tables, and manually entered records, then query that stored knowledge for PLC, WCS, and industrial vision tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported files can persistently influence future agent answers.

Mitigation: Ingest only trusted department documents and code, treat retrieved content as reference data rather than instructions, and review or delete stored JSONL records when bad data is imported.

Risk: The main skill instructions are partly garbled, which can obscure intended usage and limitations.

Mitigation: Review the artifact behavior before installation and validate query, extract, and ingest workflows in a controlled workspace.

Risk: Local ingestion may capture confidential or unreviewed source material.

Mitigation: Avoid ingesting confidential or unapproved files and limit use to reviewed department knowledge sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/tmp-domain-kit)
- [Publisher profile](https://clawhub.ai/user/paudyyin)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown with sourced knowledge entries, ranked results, and optional code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query output is ranked by stored confidence; extract and ingest workflows persist local JSONL knowledge records.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
