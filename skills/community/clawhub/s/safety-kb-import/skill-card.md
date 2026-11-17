## Description:

Guides agents through importing safety regulations and standards into a safety-review knowledge base, including text extraction, clause splitting, batch import, and data validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyz9827](https://clawhub.ai/user/cyz9827)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to add or update safety regulations, standards, and policy documents in a SQLite-backed safety-review knowledge base. It is intended for workflows that require PDF text extraction, manifest preparation, clause splitting, import execution, and post-import checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The import workflow can overwrite existing regulation rows and delete associated clauses when a document number matches an existing record.

Mitigation: Back up knowledge.db, run gap and conflict checks before import, inspect each manifest item, and validate imported records before relying on the updated knowledge base.

Risk: Broad or ambiguous document numbers can match the wrong existing record and cause unintended updates.

Mitigation: Use exact document numbers in manifests, avoid broad GB/AQ prefixes, and manually review existing records before importing replacements.

Risk: The script commits imports immediately and does not provide rollback or dry-run behavior.

Mitigation: Test clause splitting first, import in small batches, keep a database backup, and add confirmation, dry-run, exact matching, and rollback controls before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyz9827/skills/safety-kb-import)
- [Publisher profile](https://clawhub.ai/user/cyz9827)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON manifest or command-output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing import workflows and invokes scripts that emit JSON for PDF extraction, clause splitting, import summaries, validation reports, and schema inspection.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
