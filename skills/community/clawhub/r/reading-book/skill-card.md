## Description:

Coordinates a book-learning workflow that extracts chapters, generates Markdown study notes, builds Neo4j Cypher batches, imports them into Neo4j, tracks progress, and produces a final summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buruqinshouburu](https://clawhub.ai/user/buruqinshouburu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers can use this skill to turn Word or PDF books into structured study notes and a Neo4j-backed concept graph. It is intended for chapter-by-chapter learning workflows that need progress tracking, generated Markdown outputs, and graph import summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an embedded Neo4j credential.

Mitigation: Rotate or remove the embedded credential and require runtime secrets before installation or execution.

Risk: The release evidence reports under-scoped database and file writes.

Mitigation: Run in preview or dry-run mode first, review target Obsidian paths, and restrict filesystem and database permissions to the minimum needed.

Risk: Generated Cypher can mutate a Neo4j database.

Mitigation: Validate and parameterize Cypher inputs, review generated batches before execution, and use a least-privileged Neo4j account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/buruqinshouburu/skills/reading-book)
- [Book Learning Coordinator documentation](artifact/SKILL.md)
- [Book Chapter Extractor documentation](artifact/book-extractor.md)
- [Note Generator documentation](artifact/note-generator.md)
- [Neo4j Cypher Generator documentation](artifact/neo4j-cypher-generator.md)
- [Neo4j Importer documentation](artifact/neo4j-importer.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes and reports, JSON-like workflow summaries, Python and PowerShell command examples, and Cypher statements.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Obsidian Markdown files and may execute batched Neo4j database mutations when configured.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
